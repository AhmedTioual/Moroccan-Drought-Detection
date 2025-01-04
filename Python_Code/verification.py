import os
from datetime import datetime, timedelta

if __name__ == "__main__":
    
    # Define the path to the file
    file_path = os.path.expanduser("~/Desktop/Moroccan-Drought-Segmentation-master/dates.txt")

    # Read the file and parse dates
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract the days from the start dates
    days = []
    for line in lines:
        if "From" in line and "until" in line:
            start_date_str = line.split(" ")[1]  # Extract the date after "From"
            day = int(start_date_str.split("-")[2])  # Get the day part
            days.append(day)

    # Verify the sequence 01, 11, 21 repeats
    expected_pattern = [1, 11, 21]
    issues = []

    for i, day in enumerate(days):
        expected_day = expected_pattern[i % len(expected_pattern)]
        if day != expected_day:
            issues.append(f"Issue at line {i + 1}: Expected day {expected_day} but found {day}")

    # Output results
    if issues:
        print("Day pattern verification issues found:")
        for issue in issues:
            print(issue)
    else:
        print("All dates follow the day pattern 01, 11, 21.")