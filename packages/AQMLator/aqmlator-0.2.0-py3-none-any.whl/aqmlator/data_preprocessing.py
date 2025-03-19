"""
=============================================================================

    This module contains all the utilities used for data preprocessing (some initial
    analysis, normalization, ...).

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


from copy import deepcopy
from typing import List, Sequence, Tuple, TypeVar, Union

from sklearn.preprocessing import MinMaxScaler

from aqmlator.data_acquisition import LearningDatum, SupervisedLearningDatum

AqmlatorDatum = TypeVar("AqmlatorDatum", LearningDatum, SupervisedLearningDatum)


def get_attributes(
    data: Sequence[LearningDatum],
) -> List[Tuple[Union[float, str], ...]]:
    """
    A method for extracting the attributes from a `Sequence` of the `LearningDatum`.

    :param data:
        A `Sequence` of `LearningDatum` from which the attributes will be extracted.

    :return:
        A list of attributes from given `LearningDatum` sequence. The order of the
        returned classes is the same as in the given data.
    """
    arguments: List[Tuple[Union[float, str], ...]] = []

    for datum in data:
        arguments.append(datum.datum_attributes)

    return arguments


def get_targets(
    data: Sequence[SupervisedLearningDatum],
) -> List[Union[float, str, int]]:
    """
    A method for extracting the classes (or target values) from a `Sequence` of the
    `SupervisedLearningDatum`.

    :param data:
        A `Sequence` of `SupervisedLearningDatum` from which the classes will be
        extracted.

    :return:
        A list of classes from given `SupervisedLearningDatum` sequence. The order of
        the returned classes is the same as in the given data.
    """
    targets: List[Union[float, str, int]] = []

    for datum in data:
        targets.append(datum.datum_target)

    return targets


class LearningDatumMinMaxScaler:
    """
    A class for rescaling the `datum_attributes` of the `LearningDatum`. It's meant
    to extend the required functionality of `sklearn.preprocessing.MinMaxScaler`.
    """

    def __init__(self, feature_range: Tuple[float, float] = (0, 1)):
        """
        A constructor for `LearningDatumMinMaxScaler`.

        :param feature_range:
            The range to which the values of learning datum attributes will be reduced.
            Notice that it's expected for the first value to be smaller than the
            second.
        """
        self._feature_range = feature_range

    def fit_transform(self, data: Sequence[AqmlatorDatum]) -> Sequence[AqmlatorDatum]:
        """
        Transforms the attributes of the `LearningDatum` objects so that they are
        within the bounds given by the `feature_range` specified in the constructor.

        :Note:
            We expect the datum_attributes to be of type `float` (not `str`, which is
            also formally allowed.

        :param data:
            A list of LearningDatum of which attributes will be transformed.

        :return:
            A list of transformed `LearningDatum`.
        """
        arguments: List[Tuple[Union[float, str], ...]] = get_attributes(data)

        fitted_attributes: List[Tuple[float, ...]] = MinMaxScaler(
            self._feature_range
        ).fit_transform(arguments)

        fitted_data: Sequence[AqmlatorDatum] = deepcopy(data)

        for i in range(len(data)):
            fitted_data[i].datum_attributes = fitted_attributes[i]

        return fitted_data
