"""
=============================================================================

    This module contains tests for the functionalities in the data_acquisition module.

=============================================================================

    Copyright 2022 ACK Cyfronet AGH. All Rights Reserved.

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

import csv
import locale
import os
import unittest
from typing import List, Tuple, Union

from aqmlator.data_acquisition import (
    CSVDataReceiver,
    LearningDatum,
    SupervisedLearningDatum,
)


class TestDataAcquisition(unittest.TestCase):
    """
    A `TestCase` class for data_acquisition module.
    """

    def setUp(self) -> None:
        """
        Sets up the tests.
        """
        csv_learning_data: List[List[float]] = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        csv_data_targets: List[int] = [1, 2]

        self._learning_data: List[LearningDatum] = [
            LearningDatum(tuple(data)) for data in csv_learning_data
        ]

        self._supervised_learning_data: List[SupervisedLearningDatum] = [
            SupervisedLearningDatum(tuple(csv_learning_data[i]), csv_data_targets[i])
            for i in range(len(csv_data_targets))
        ]

        with open(
            "learning_data.csv", "w", newline="", encoding=locale.getpreferredencoding()
        ) as f:
            writer = csv.writer(f, "excel")
            for data in csv_learning_data:
                writer.writerow(data)

        with open(
            "supervised_learning_data.csv",
            "w",
            newline="",
            encoding=locale.getpreferredencoding(),
        ) as f:
            writer = csv.writer(f, "excel")
            for i in range(len(csv_data_targets)):
                writer.writerow(csv_learning_data[i] + [csv_data_targets[i]])

    def tearDown(self) -> None:
        """
        Ensures that the files created during the tests are deleted.
        """
        self._ensure_deleted("learning_data.csv")
        self._ensure_deleted("supervised_learning_data.csv")

    @staticmethod
    def _ensure_deleted(file_path: str) -> None:
        """
        Ensures that the file on under the given path is deleted.

        :param file_path:
            A path to the file that should be deleted.
        """
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def test_learning_datum_equality(self) -> None:
        """
        Tests if equality of learning datum was implemented properly.
        """
        x: Tuple[Union[float, str], ...] = (1.23, "lol")
        x2: Tuple[Union[float, str], ...] = (3.21, "nie_lol")
        datum_1: LearningDatum = LearningDatum(x)
        datum_2: LearningDatum = LearningDatum(x)
        datum_3: LearningDatum = LearningDatum(x2)

        self.assertTrue(
            datum_2 == datum_1, "LearningDatum equality implementation has an error."
        )

        self.assertFalse(
            datum_1 == datum_3, "LearningDatum objects shouldn't be equal!"
        )

    def test_supervised_learning_datum_equality(self) -> None:
        """
        Tests if equality of SupervisedLearningDatum was implemented properly.
        """
        x: Tuple[Union[float, str], ...] = (1.23, "lol")
        x2: Tuple[Union[float, str], ...] = (3.21, "nie_lol")
        y: Union[float, str, int] = 1
        datum_1: SupervisedLearningDatum = SupervisedLearningDatum(x, y)
        datum_2: SupervisedLearningDatum = SupervisedLearningDatum(x, y)
        datum_3: SupervisedLearningDatum = SupervisedLearningDatum(x, int(y) + 1)
        datum_4: SupervisedLearningDatum = SupervisedLearningDatum(x2, y)

        self.assertTrue(
            datum_2 == datum_1,
            "SupervisedLearningDatum equality implementation has an error.",
        )

        self.assertFalse(
            datum_1 == datum_3, "SupervisedLearningDatum objects shouldn't be equal!"
        )

        self.assertFalse(
            datum_1 == datum_4, "SupervisedLearningDatum objects shouldn't be equal!"
        )

    def test_csv_learning_data_reading(self) -> None:
        """
        Checks if the (unsupervised) learning data is properly read from the file.
        """
        receiver: CSVDataReceiver = CSVDataReceiver()

        data: List[LearningDatum] = receiver.receive_data("learning_data.csv")

        self.assertTrue(
            len(data) == len(self._learning_data),
            "Received (unsupervised) learning data don't have proper size.",
        )

        for i in range(len(data)):
            self.assertTrue(
                self._learning_data[i] == data[i], "LearningDatum wasn't read properly."
            )

    def test_csv_supervised_data_reading(self) -> None:
        """
        Checks if the supervised learning data is properly read from the file.
        """
        receiver: CSVDataReceiver = CSVDataReceiver(target_index=3)

        data: List[LearningDatum] = receiver.receive_data(
            "supervised_learning_data.csv"
        )

        self.assertTrue(
            len(data) == len(self._supervised_learning_data),
            "Received supervised learning data don't have proper size.",
        )

        for i in range(len(data)):
            self.assertTrue(
                self._supervised_learning_data[i] == data[i],
                "SupervisedLearningDatum wasn't read properly.",
            )


if __name__ == "__main__":
    unittest.main()
