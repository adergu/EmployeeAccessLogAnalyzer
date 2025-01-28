from src.data_validator import DataValidator
from src.log_summary import LogSummary

def main():
    file_path = "log.csv"  # Replace with the path to your log file

    try:
        # Step 1: Validate the log
        print("Validating the log file...")
        valid_rows, invalid_rows = DataValidator.validate_log(file_path)

        print("\nInvalid Rows:")
        print(invalid_rows)

        # Save valid rows to a temporary file for processing
        valid_rows_file = "valid_rows.csv"
        valid_rows.to_csv(valid_rows_file, index=False)

        # Step 2: Generate a summary from valid rows
        print("\nGenerating the summary for valid rows...")
        summary = LogSummary.generate_summary(valid_rows_file)

        print("\nEmployee Log Summary:")
        print(summary)

        # Optionally save the summary to a CSV file
        summary.to_csv("log_summary.csv", index=False)

        print("\nSummary saved to 'log_summary.csv'.")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()