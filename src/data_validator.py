import pandas as pd

class DataValidator:
    @staticmethod
    def validate_log(file_path):
        """
        Validate the input log for missing data.

        Args:
            file_path (str): Path to the input CSV file.

        Returns:
            tuple: (valid_rows, invalid_rows)
        """
        try:
            # Load the CSV file
            log_data = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading the CSV file: {e}")

        # Check required columns
        required_columns = ['Employee Name', 'Event', 'Timestamp']
        for col in required_columns:
            if col not in log_data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Identify incomplete rows
        missing_name = log_data['Employee Name'].isna()
        missing_event = log_data['Event'].isna()
        missing_timestamp = log_data['Timestamp'].isna()

        # Report incomplete rows
        invalid_rows = log_data[missing_name | missing_event | missing_timestamp].copy()
        invalid_rows['Missing Field'] = invalid_rows.apply(
            lambda row: ", ".join(
                [
                    field for field, missing in zip(
                        ['Employee Name', 'Event', 'Timestamp'],
                        [
                            pd.isna(row['Employee Name']),
                            pd.isna(row['Event']),
                            pd.isna(row['Timestamp'])
                        ]
                    ) if missing
                ]
            ),
            axis=1
        )

        # Filter valid rows
        valid_rows = log_data[~(missing_name | missing_event | missing_timestamp)]

        return valid_rows, invalid_rows

if __name__ == "__main__":
    # Example usage
    file_path = "log.csv"  # Replace with the path to your log file

    try:
        valid_rows, invalid_rows = DataValidator.validate_log(file_path)

        print("Valid Rows:")
        print(valid_rows)

        print("\nInvalid Rows:")
        print(invalid_rows)
    except ValueError as e:
        print(f"Error: {e}")