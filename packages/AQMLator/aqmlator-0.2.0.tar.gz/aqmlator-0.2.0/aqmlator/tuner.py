"""
=============================================================================

    This module contains the classes that use optuna for different kinds of
    optimizations - mainly model and hyperparameter.

=============================================================================

    Copyright 2023 ACK Cyfronet AGH. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

=============================================================================

    This work was supported by the EuroHPC PL project funded at the Smart Growth
    Operational Programme 2014-2020, Measure 4.2 under the grant agreement no.
    POIR.04.02.00-00-D014/20-00.

=============================================================================
"""

__author__ = "Tomasz Rybotycki"

import abc
import json
import uuid
import warnings
from enum import StrEnum
from math import ceil, floor, prod, sqrt
from os import environ
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union

import optuna
import pennylane as qml
import pennylane.numpy as np
import requests
from numpy.typing import NDArray
from optuna.exceptions import ExperimentalWarning
from optuna.samplers import TPESampler
from pennylane.optimize import (
    AdamOptimizer,
    GradientDescentOptimizer,
    NesterovMomentumOptimizer,
)
from pennylane.templates.embeddings import AmplitudeEmbedding, AngleEmbedding
from pennylane.templates.layers import BasicEntanglerLayers, StronglyEntanglingLayers
from sklearn.metrics import silhouette_score  # TR: It has bounds.
from torch import Tensor
from torch.utils.data import DataLoader

from aqmlator.qml import (
    QMLModel,
    QNNBinaryClassifier,
    QNNClassifier,
    QNNLinearRegression,
    QuantumKernelBinaryClassifier,
    RBMClustering,
)
from aqmlator.server import status_update_endpoint

# TODO TR:  Should those be global?

binary_classifiers: Dict[str, Dict[str, Any]] = {
    "QNN": {
        "constructor": QNNBinaryClassifier,
        "kwargs": {
            "batch_size": (15, 25),  # Might need to be data size-dependent instead.
        },
        "fixed_kwargs": {},
        "n_layers": (1, 3),
    },
    "QEK": {
        "constructor": QuantumKernelBinaryClassifier,
        "kwargs": {},
        "fixed_kwargs": {},
        "n_layers": (3, 5),
    },
}

regressors: Dict[str, Dict[str, Any]] = {
    "QNN": {
        "kwargs": {
            "batch_size": (15, 25),  # Might need to be data size-dependent instead.
        },
        "n_layers": (1, 3),
        "constructor": QNNLinearRegression,
    }
}

clustering: Dict[str, Dict[str, Any]] = {
    "RBM": {
        "constructor": RBMClustering,
        "kwargs": {
            "lbae_n_layers": (1, 2),  # TR: lbae_n_layers > 2 poses problems.
            "fireing_threshold": (0.6, 0.99),
        },
    }
}

data_embeddings: Dict[str, Dict[str, Any]] = {
    "ANGLE": {"constructor": AngleEmbedding, "kwargs": {}, "fixed_kwargs": {}},
    "AMPLITUDE": {
        "constructor": AmplitudeEmbedding,
        "kwargs": {},
        "fixed_kwargs": {"pad_with": 0, "normalize": True},
    },
}

optimizers: Dict[str, Dict[str, Any]] = {
    "NESTEROV": {
        "constructor": NesterovMomentumOptimizer,
        # Hyperparameters range taken from
        # https://cs231n.github.io/neural-networks-3/
        "kwargs": {
            "stepsize": {"min": 0.00001, "max": 0.1},
            "momentum": {"min": 0.5, "max": 0.9},
        },
    },
    "ADAM": {
        "constructor": AdamOptimizer,
        # Hyperparameters range taken from arXiv:1412.6980.
        "kwargs": {
            "stepsize": {
                "min": 0.00001,
                "max": 0.1,
            },
            "beta1": {
                "min": 0,
                "max": 0.9,
            },
            "beta2": {"min": 0.99, "max": 0.9999},
        },
    },
}

layer_types: Dict[str, Dict[str, Any]] = {
    "BASIC": {"constructor": BasicEntanglerLayers},
    "STRONGLY_ENTANGLING": {
        "constructor": StronglyEntanglingLayers,
    },
}


class MLTaskType(StrEnum):
    BINARY_CLASSIFICATION = "BINARY_CLASSIFICATION"
    CLASSIFICATION = "CLASSIFICATION"
    REGRESSION = "REGRESSION"
    GROUPING = "GROUPING"


class OptunaOptimizer(abc.ABC):
    """
    A class for all `optuna`-based optimizers that takes care of the common boilerplate
    code, especially in the constructor.
    """

    def __init__(
        self,
        features: Union[Sequence[Sequence[float]], NDArray[np.float32]],
        classes: Optional[Sequence[int]],
        *,
        study_name: str = "",
        add_uuid: bool = True,
        n_trials: int = 10,
        n_cores: int = 1,
        n_seeds: int = 1,
    ) -> None:
        """
        A constructor for the `OptunaOptimizer` class.

        :param features:
            The lists of features of the objects that are used during the training.
        :param classes:
            A list of classes or function values corresponding to the given lists of
            features.
        :param study_name:
            The name of the `optuna` study. If the study with this name is already
            stored in the DB, the tuner will continue the study.
        :param add_uuid:
            Flag for specifying if uuid should be added to the `study_name`.
        :param n_cores:
            The number of cores that `optuna` can use. The (default) value :math:`-1`
            means all of them.
        :param n_trials:
            The number of trials after which the search will be finished.
        :param n_seeds:
            Number of seeds checked per `optuna` trial.
        """
        self._x: Union[Sequence[Sequence[float]], NDArray[np.float32]] = features
        self._y: Optional[Sequence[int]] = classes

        self._study_name: str = study_name

        if add_uuid:
            self._study_name += str(uuid.uuid1())

        self._n_trials: int = n_trials
        self._n_cores: int = n_cores
        self._n_seeds: int = n_seeds

    @staticmethod
    def _get_storage() -> Optional[str]:
        return environ["aqmlator_database_url"]


class ModelFinder(OptunaOptimizer):
    """
    A class for finding the best QNN model for given data and task.
    """

    # TODO TR:  Make it so that the supervised and unsupervised learning parts use
    #           the same pipeline.

    # TODO TR:  Maybe separate class for clustering?

    def __init__(
        self,
        task_type: str,
        features: Union[Sequence[Sequence[float]], NDArray[np.float32]],
        classes: Optional[Sequence[int]] = None,
        *,
        device: Optional[qml.devices.Device] = None,
        study_name: str = "QML_Model_Finder_",
        add_uuid: bool = True,
        minimal_accuracy: float = 0.8,
        n_cores: int = -1,
        n_trials: int = 100,
        n_epochs: int = 10,
        n_seeds: int = 5,
        coupling_map: Optional[List[List[int]]] = None,
        d_wave_access: bool = False,
    ):
        """
        A constructor for `ModelFinder` class.

        :param features:
            Features of the objects to be classified. Their order should correspond to
            that of `classes`.
        :param classes:
            Classes of the classified objects. Their order should correspond to that
            of `features`.
        :param study_name:
            The name of the `optuna` study. If the study with this name is already
            stored in the DB, the finder will continue the study.
        :param device:
            The device on which to run the model.
        :param add_uuid:
            Flag for specifying if uuid should be added to the `study_name`.
        :param minimal_accuracy:
            Minimal accuracy after which the training will end.
        :param n_cores:
            The number of cores that `optuna` can use. The (default) value :math:`-1`
            means all of them.
        :param n_trials:
            The number of trials after which the search will be finished.
        :param n_epochs:
            The number of QNN training epochs.
        :param n_seeds:
            Number of seeds checked per `optuna` trial.
        :param coupling_map:
            A list of connected qubits.
        :param d_wave_access:
            Flag for specifying if the model could be run on the D-Wave machine.
        """
        super().__init__(
            features=features,
            classes=classes,
            study_name=study_name,
            add_uuid=add_uuid,
            n_trials=n_trials,
            n_cores=n_cores,
            n_seeds=n_seeds,
        )

        # A dict that will be string models taken under consideration during the
        # model finding.
        self._models_dict: Dict[str, Any] = {}

        self._task_type: str = task_type

        self._n_epochs: int = n_epochs

        self._minimal_accuracy: float = minimal_accuracy

        self._optuna_objective_functions: Dict[
            str, Callable[[optuna.trial.Trial], float]
        ] = {
            MLTaskType.BINARY_CLASSIFICATION: self._simple_model_objective_function,
            MLTaskType.CLASSIFICATION: self._classification_objective_function,
            MLTaskType.REGRESSION: self._simple_model_objective_function,
            MLTaskType.GROUPING: self._grouping_model_objective_function,
        }

        self._optuna_postfix: str = ""

        self.dev: qml.devices.Device = device
        self.device_coupling_map: Optional[List[List[int]]] = coupling_map

        self.d_wave_access: bool = d_wave_access

        try:
            requests.post(
                status_update_endpoint,
                data=json.dumps({self._study_name: "Waiting..."}),
                timeout=1,
            )
        except requests.exceptions.ConnectionError as e:
            print(e)

    def find_model(self) -> None:
        """
        Finds the QNN model that best fits the given data.
        """
        try:
            requests.post(
                status_update_endpoint,
                data=json.dumps({self._study_name: "Tuning..."}),
                timeout=1,
            )
        except requests.exceptions.ConnectionError as e:
            print(e)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ExperimentalWarning)
            sampler: TPESampler = TPESampler(
                seed=0, multivariate=True, group=True  # For experiments repeatability.
            )

        study: optuna.study.Study = optuna.create_study(
            sampler=sampler,
            study_name=self._study_name,
            load_if_exists=True,
            storage=self._get_storage(),
        )

        study.optimize(
            self._optuna_objective_functions[self._task_type],
            n_trials=self._n_trials,
            n_jobs=self._n_cores,
        )

        try:
            requests.post(
                status_update_endpoint,
                data=json.dumps({self._study_name: "Done."}),
                timeout=1,
            )
        except requests.exceptions.ConnectionError as e:
            print(e)

    def _simple_model_objective_function(self, trial: optuna.trial.Trial) -> float:
        """
        Default objective function of the `optuna` optimizer for the model finding. It
        is meant to work for all the simple (single) models.

        :Note:
            Instead of optimizing the hyperparameters, as `optuna` usually does, this
            optimizes the structure of the VQC for the model.

        :param trial:
            The `optuna` Trial object used to randomize and store the
            results_reconstruction of the optimization.

        :return:
            The average number of calls made to the quantum device (which `optuna`
            wants to minimize).
        """
        self._initialize_model_dict()

        model_type: str = trial.suggest_categorical(
            "model_type" + self._optuna_postfix, list(self._models_dict)
        )

        kwargs: Dict[str, Any] = self._suggest_supervised_model_kwargs(
            trial, model_type
        )

        model: QMLModel = self._models_dict[model_type]["constructor"](**kwargs)

        return self._evaluate_supervised_model(model)

    def _grouping_model_objective_function(self, trial: optuna.trial.Trial) -> float:
        """
        Objective function of the `optuna` optimizer for grouping model finder.

        :param trial:
            The `optuna` Trial object used to randomize and store the values
            used in the optimization.

        :return:
            The average clustering score obtained by the model.
        """
        self._initialize_model_dict()

        model_type: str = trial.suggest_categorical(
            "model_type" + self._optuna_postfix, list(self._models_dict)
        )

        kwargs: Dict[str, Any] = self._suggest_unsupervised_model_kwargs(
            trial, model_type
        )

        model: RBMClustering = self._models_dict[model_type]["constructor"](**kwargs)

        return self._evaluate_unsupervised_model(model)

    def _initialize_model_dict(self) -> None:
        """
        Initializes the models dict used during the model finding.

        :Note:
            The (non-binary) classification task uses binary classification dict to
            create a complex (classification) model.
        """
        self._models_dict = binary_classifiers

        if self._task_type == MLTaskType.REGRESSION:
            self._models_dict = regressors

        if self._task_type == MLTaskType.GROUPING:
            self._models_dict = clustering

    def _evaluate_unsupervised_model(self, model: RBMClustering) -> float:
        """
        Evaluates the performance of the given model. The evaluation is based on the
        Silhouette score (which takes values from [-1, 1]). The higher the score, the
        better the model.

        :param model:
            A `RBMClustering` model to evaluate.

        :return:
            The average Silhouette score obtained by the model.
        """
        score: float = 0
        score_x = np.array(self._x).reshape(
            len(self._x), int(prod(np.array(self._x[0]).shape))
        )

        data: Sequence[Tuple[Tensor, Tensor]] = [
            (Tensor(val), Tensor([-1])) for val in self._x
        ]

        # Type ignore the following line, because Torch isn't type-hinted well enough.
        data_loader: DataLoader[Tuple[Tensor, Tensor]] = DataLoader(
            data,  # type: ignore
            batch_size=10,  # TR TODO: Make this a parameter?
            shuffle=True,
            num_workers=1,
            persistent_workers=True,
        )

        for seed in range(self._n_seeds):
            model.rbm.rng = np.random.MT19937(seed)

            model.fit(data_loader)

            labels: List[Tuple[int, ...]] = [
                tuple(t) for val in data_loader for t in model.predict(val[0])
            ]

            group_labels: List[Tuple[int, ...]] = list(set(labels))
            groups: List[int] = [group_labels.index(label) for label in labels]

            # Protect against all objects being in the same group. Remember that optuna
            # aim to MINIMIZE the objective function!
            if len(set(groups)) > 1:
                score -= silhouette_score(score_x, groups)
            else:
                score += 1

        return score / self._n_seeds

    def _evaluate_supervised_model(self, model: QMLModel) -> float:
        """
        Evaluates the performance of the given model. The evaluation is based on the
        number of calls to the quantum machine (which are _expensive_) during the
        fitting.

        :param model:
            A `QMLModel` to evaluate.

        The mean number of calls to the quantum machine during the fitting.
        """

        with qml.Tracker(self.dev, persistent=False) as tracker:
            for seed in range(self._n_seeds):
                model.dev = self.dev
                model.seed(seed)

                model.fit(self._x, self._y)

        return tracker.totals["executions"] / self._n_seeds

    def _classification_objective_function(self, trial: optuna.trial.Trial) -> float:
        """
        Objective function of the `optuna` optimizer for classification model finder.

        :param trial:
            The `optuna` Trial object used to randomize and store the
            results_reconstruction of the optimization.

        :return:
            The average number of calls made to the quantum device (which `optuna`
            wants to minimize).
        """
        self._initialize_model_dict()

        n_classes: int = len(np.unique(self._y))

        binary_classifiers_kwargs: List[Dict[str, Any]] = []

        for i in range(n_classes):
            self._optuna_postfix = f"_({i})"

            kwargs: Dict[str, Any] = self._suggest_supervised_model_kwargs(trial, "QNN")
            kwargs["device"] = self.dev

            binary_classifiers_kwargs.append(kwargs)

        qnn_binary_classifiers: List[QNNBinaryClassifier] = []

        for i in range(n_classes):
            qnn_binary_classifiers.append(
                QNNBinaryClassifier(**binary_classifiers_kwargs[i])
            )

        classifier: QNNClassifier = QNNClassifier(
            wires=range(len(self._x)),
            n_classes=n_classes,
            binary_classifiers=qnn_binary_classifiers,
        )

        self._optuna_postfix = ""

        return self._evaluate_supervised_model(classifier)

    def _suggest_supervised_model_kwargs(
        self, trial: optuna.trial.Trial, model_type: str
    ) -> Dict[str, Any]:
        """
        Suggests the kwargs for the specified (qml) model.

        :param trial:
            An optuna trial object for parameters selection.
        :param model_type:
            A string describing the type of the model. Note that the
            `self._models_dict` has to be initialized properly, prior to calling
            this method.

        :return:
            Returns the suggested kwargs for the selected (qml) model type.
        """
        kwargs: Dict[str, Any] = {
            "wires": len(self._x[0]),
            "n_layers": trial.suggest_int(
                "n_layers" + self._optuna_postfix,
                self._models_dict[model_type]["n_layers"][0],
                self._models_dict[model_type]["n_layers"][1],
            ),
            "n_epochs": self._n_epochs,
            "accuracy_threshold": self._minimal_accuracy,
        }

        # TR: Might need to be extended for different arguments type at some point.
        kwargs_data: Dict[str, Any] = self._models_dict[model_type]["kwargs"]

        for kwarg in kwargs_data:
            kwargs[kwarg] = trial.suggest_int(
                kwarg + self._optuna_postfix,
                kwargs_data[kwarg][0],
                kwargs_data[kwarg][1],
            )

        self._suggest_embedding(trial, kwargs)
        self._suggest_layers(trial, kwargs)

        return kwargs

    def _suggest_unsupervised_model_kwargs(
        self, trial: optuna.trial.Trial, model_type: str
    ) -> Dict[str, Any]:
        """
        Suggests the kwargs for the specified (unsupervised learning) model.

        :param trial:
            An optuna trial object for parameters selection.
        :param model_type:
            A string describing the type of the model. Note that the
            `self._models_dict` has to be initialized properly, prior to calling
            this method.

        :return:
            Returns the suggested kwargs for the selected model type.
        """
        # TR: The input shape has to be of form (1, actual_shape).
        lbae_input_shape: Tuple[int] = (1,) + np.array(self._x[0]).shape
        lbae_input_size: int = prod(lbae_input_shape)

        kwargs: Dict[str, Any] = {
            "lbae_input_shape": lbae_input_shape,
            "lbae_out_channels": trial.suggest_int(
                name="lbae_out_channels",
                low=floor(sqrt(lbae_input_size)),
                high=ceil(0.75 * lbae_input_size),
            ),
        }

        kwargs["rbm_n_visible_neurons"] = kwargs["lbae_out_channels"]

        kwargs["rbm_n_hidden_neurons"] = trial.suggest_int(
            name="rbm_n_hidden_neurons",
            low=floor(sqrt(kwargs["lbae_out_channels"])),
            high=ceil(0.75 * kwargs["lbae_out_channels"]),
        )  # Heuristic.

        # TR: Might need to be extended for different arguments type at some point.
        kwargs_data: Dict[str, Any] = self._models_dict[model_type]["kwargs"]

        kwargs["lbae_n_layers"] = trial.suggest_int(
            "lbae_n_layers" + self._optuna_postfix,
            kwargs_data["lbae_n_layers"][0],
            kwargs_data["lbae_n_layers"][1],
        )

        kwargs["fireing_threshold"] = trial.suggest_float(
            "fireing_threshold" + self._optuna_postfix,
            kwargs_data["fireing_threshold"][0],
            kwargs_data["fireing_threshold"][1],
        )

        kwargs["n_epochs"] = self._n_epochs

        return kwargs

    def _suggest_embedding(
        self, trial: optuna.trial.Trial, kwargs: Dict[str, Any]
    ) -> None:
        """
        Using 'optuna', suggest the embedding and its `kwargs`. Everything is then added
        to the given `kwargs`.

        :param trial:
            Optuna `Trial` object that "suggests" the parameters values.
        :param kwargs:
            A dictionary of keyword arguments that will be used to initialize the
            QML model.
        """
        embedding_type: str = trial.suggest_categorical(
            "embedding" + self._optuna_postfix, list(data_embeddings)
        )

        kwargs["embedding_method"] = data_embeddings[embedding_type]["constructor"]

        embedding_kwargs: Dict[str, Any] = {"wires": range(kwargs["wires"])}

        embedding_kwargs.update(data_embeddings[embedding_type]["fixed_kwargs"])

        kwargs["embedding_kwargs"] = embedding_kwargs

    def _suggest_layers(
        self, trial: optuna.trial.Trial, kwargs: Dict[str, Any]
    ) -> None:
        """
        Using `optuna`, suggest the order of layers in the VQC based on the `kwargs`
        given.

        :param trial:
            Optuna `Trial` object that "suggests" the parameters values.
        :param kwargs:
            A dictionary of keyword arguments that will be used to initialize the
            QML model.
        """
        layers: List[Type[qml.operation.Operation]] = []

        for i in range(kwargs["n_layers"]):
            layer_type: str = trial.suggest_categorical(
                f"layer_{i}" + self._optuna_postfix, list(layer_types)
            )
            layers.append(layer_types[layer_type]["constructor"])

            # TR:   So far all the layer types begin with (N_LAYERS, N_WIRES) tuple, and
            #       then proceed with some additional parameters. This may need to be
            #       rethought later.

        kwargs["layers"] = layers
        kwargs.pop("n_layers")

    def __del__(self) -> None:
        try:
            requests.post(
                status_update_endpoint,
                data=json.dumps({self._study_name: "Delete"}),
                timeout=1,
            )
        except requests.exceptions.ConnectionError as e:
            print(e)


class HyperparameterTuner(OptunaOptimizer):
    """
    This class contains the optuna-based tuner for ML Training hyperparameters.

    TODO TR:    Consider renaming this class, as it's only used by the supervised
                learning models (as of now).
    """

    def __init__(
        self,
        features: Sequence[Sequence[float]],
        classes: Sequence[int],
        model: QMLModel,
        *,
        study_name: str = "QML_Hyperparameter_Tuner_",
        add_uuid: bool = True,
        n_trials: int = 10,
        n_cores: int = 1,
        n_seeds: int = 1,
    ) -> None:
        """
        A constructor for the `HyperparameterTuner` class.

        :param features:
            The lists of features of the objects that are used during the training.
        :param classes:
            A list of classes corresponding to the given lists of features.
        :param model:
            A model to be trained.
        :param study_name:
            The name of the `optuna` study. If the study with this name is already
            stored in the DB, the tuner will continue the study.
        :param add_uuid:
            Flag for specifying if uuid should be added to the `study_name`.
        :param n_cores:
            The number of cores that `optuna` can use. The (default) value :math:`-1`
            means all of them.
        :param n_trials:
            The number of trials after which the search will be finished.
        :param n_seeds:
            Number of seeds checked per `optuna` trial.
        """
        super().__init__(
            features=features,
            classes=classes,
            study_name=study_name,
            add_uuid=add_uuid,
            n_trials=n_trials,
            n_cores=n_cores,
            n_seeds=n_seeds,
        )

        self._model: QMLModel = model

    def find_hyperparameters(self) -> None:
        """
        Finds the (sub)optimal training hyperparameters.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ExperimentalWarning)
            sampler: TPESampler = TPESampler(
                seed=0, multivariate=True, group=True  # For experiments repeatability.
            )

        study: optuna.study.Study = optuna.create_study(
            sampler=sampler,
            study_name=self._study_name,
            load_if_exists=True,
            storage=self._get_storage(),
        )

        study.optimize(
            self._optuna_objective, n_trials=self._n_trials, n_jobs=self._n_cores
        )

    @staticmethod
    def _suggest_optimizer(trial: optuna.trial.Trial) -> GradientDescentOptimizer:
        """

        :param trial:
            The `optuna.trial.Trial` object used to randomize and store the
            results_reconstruction of the optimization.
        :return:
            The suggested optimizer.
        """

        optimizer_type: str = trial.suggest_categorical("optimizer", list(optimizers))

        kwargs_data: Dict[str, Any] = optimizers[optimizer_type]["kwargs"]
        kwargs: Dict[str, Any] = {}

        # TR: Might need rebuilding for int and str kwargs.
        for kwarg in kwargs_data:
            kwargs[kwarg] = trial.suggest_float(
                kwarg, kwargs_data[kwarg]["min"], kwargs_data[kwarg]["max"]
            )

        optimizer: GradientDescentOptimizer = optimizers[optimizer_type]["constructor"](
            **kwargs
        )

        return optimizer

    def _optuna_objective(self, trial: optuna.trial.Trial) -> float:
        """
        Objective function of the `optuna` optimizer.

        :param trial:
            The `optuna` Trial object used to randomize and store the
            results_reconstruction of the optimization.
        :return:
        """
        self._model.optimizer = self._suggest_optimizer(trial)

        with qml.Tracker(self._model.dev, persistent=False) as tracker:
            for _ in range(self._n_seeds):
                self._model.weights = np.zeros_like(self._model.weights)

                if self._y is not None:
                    self._model.fit(self._x, self._y)

        return tracker.totals["executions"] / self._n_seeds
