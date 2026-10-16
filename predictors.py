from abc import ABC, abstractmethod
import math

from exceptions import OutOfSampleError


class Predictor(ABC):

    def __init__(self, historical_data):
        """
        Store historical DataTable.
        """
        self.historical_data = historical_data

    def check_in_range(self, patient):
        for i in range(1, 10):
            name = f"Feature{i}"
            low = self.historical_data.get_column_min(name)
            high = self.historical_data.get_column_max(name)
            if patient[name] < low or patient[name] > high:
                raise OutOfSampleError(f"{name} with value {patient[name]} is outside historical range [{low}, {high}]")

    @abstractmethod
    def predict(self, patient):
        """
        Make a prediction for one patient.
        """
        pass


class MajorityClassPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)
        self.majority_class = None
        tumor_type = self.historical_data.get_column("TumorType")
        benign = tumor_type.count(0.0)
        malignant = tumor_type.count(1.0)
        if benign > malignant:
            self.majority_class = 0.0
        else:
            self.majority_class = 1.0 

    def predict(self, patient):
        self.check_in_range(patient)
        return self.majority_class


class NearestNeighborPredictor(Predictor):

    def __init__(self, historical_data):
        super().__init__(historical_data)

    def distance(self, patient1, patient2):
        total = 0
        for i in range(1, 10):
            name = f"Feature{i}"
            total += (patient1[name] - patient2[name]) ** 2
        return math.sqrt(total)
        

    def predict(self, patient):
        self.check_in_range(patient)

        best_distance = float("inf")
        best_label = None

        for i in range(self.historical_data.get_num_rows()):
            row = self.historical_data.get_row(i)
            d = self.distance(patient, row)
            if d < best_distance:
                best_distance = d
                best_label = row["TumorType"]
        return best_label

