from data_representation import DataTable
from predictors import MajorityClassPredictor, NearestNeighborPredictor
from exceptions import OutOfSampleError


def main():

    # Load datasets
    historical = DataTable("data/cancer_historical.csv")
    new_cases = DataTable("data/cancer_new_cases.csv")
    labels = DataTable("data/cancer_new_cases_labels.csv")

    # Fill missing values
    means = historical.calc_missing_val()
    new_cases.calc_missing_val(means)
    
    # Create predictors
    mode_predictor = MajorityClassPredictor(historical)
    nn_predictor = NearestNeighborPredictor(historical)


    mode_predictions = []
    nn_predictions = []


    # Predict every new case
    for i in range(new_cases.get_num_rows()):
        patient = new_cases.get_row(i)

        try:
            mode_predictions.append(mode_predictor.predict(patient))
        
        except OutOfSampleError as e:
            mode_predictions.append(None)
            print(f"Case {i} (mode): {e}")

        try:
            nn_predictions.append(
                nn_predictor.predict(patient)
            )

        except OutOfSampleError as e:
            nn_predictions.append(None)
            print(f"Case {i} (Nearest Neighbor): {e}")


    # Get true labels
    actual_labels = labels.get_column("TumorType")

    # Accuracy
    print(
        "Mode accuracy:",
        calculate_accuracy(mode_predictions, actual_labels)
    )

    print(
        "Nearest Neighbor accuracy:",
        calculate_accuracy(nn_predictions, actual_labels)
    )

    # Cases that fall outside historical min/max
    print(mode_predictions.count(None), nn_predictions.count(None))


if __name__ == "__main__":
    main()

