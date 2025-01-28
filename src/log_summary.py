
import pandas as pd
from datetime import datetime, timedelta

class LogSummary:
    @staticmethod
    def generate_summary(file_path):
        """
        Generate a summary of employee logs.

        Args:
            file_path (str): Path to the input CSV file.

        Returns:
            pd.DataFrame: Summary report for each employee.
        """
        try:
            # Load the CSV file
            log_data = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading the CSV file: {e}")

        # Ensure the required columns are present
        required_columns = ['Employee Name', 'Event', 'Timestamp']
        for col in required_columns:
            if col not in log_data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Convert the Timestamp column to datetime
        log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'], errors='coerce')

        # Sort data by Employee Name and Timestamp
        log_data = log_data.sort_values(by=['Employee Name', 'Timestamp'])

        # Initialize summary list
        summary = []

        # Group by Employee Names
        for employee, group in log_data.groupby('Employee Name'):
            total_check_ins = 0
            total_time = timedelta(0)
            errors = []
            in_time = None

            for _, row in group.iterrows():
                event = row['Event']
                timestamp = row['Timestamp']

                if event == 'Check-In':
                    if in_time is not None:
                        errors.append("Multiple Check-Ins without Check-Out")
                    in_time = timestamp
                    total_check_ins += 1
                elif event == 'Check-Out':
                    if in_time is None:
                        errors.append("Check-Out without prior Check-In")
                    else:
                        time_spent = timestamp - in_time
                        if time_spent < timedelta(minutes=30):
                            errors.append("Stay shorter than 30 minutes")
                        if time_spent > timedelta(hours=10):
                            errors.append("Stay longer than 10 hours")
                        total_time += time_spent
                        in_time = None

            if in_time is not None:
                errors.append("Check-In without Check-Out")

            # Add the summary for the employees
            summary.append({
                'Employee Name': employee,
                'Total Check-Ins': total_check_ins,
                'Cumulative Time (hours)': total_time.total_seconds() / 3600,
                'Errors': ", ".join(errors) if errors else "None"
            })
        # Convert summary to DataFrame
        summary_df = pd.DataFrame(summary)
        return summary_df

if __name__ == "__main__":
    # Example usage
    file_path = "log.csv"  # Replace with the path to your log file

    try:
        summary_df = LogSummary.generate_summary(file_path)
        print("Employee Log Summary:")
        print(summary_df)
        # Optionally, save the summary to a CSV file
        summary_df.to_csv("log_summary.csv", index=False)
    except ValueError as e:
        print(f"Error: {e}")
