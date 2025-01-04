import os
import re
from datetime import datetime, timedelta

# Define the directory path
directory_path = os.path.expanduser("~/Desktop/Moroccan-Drought-Segmentation-master/satellite_dataset")

# Function to extract numeric value from filename for files like "(1)"
def extract_number(filename):
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else float('inf')  # Handle filenames without numbers

# Function to extract timestamp from filename for files like "2025-01-02T154452.255.png"
def extract_timestamp(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{6}\.\d{3})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%dT%H%M%S.%f')
    else:
        return None

# Get list of files
all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# Sort files based on either numeric value or timestamp
sorted_files = sorted(all_files, key=lambda f: (extract_number(f), extract_timestamp(f) or datetime.min))

# Start date for renaming
current_date = datetime(2012, 1, 1)

# Loop through sorted files and rename them
for idx, filename in enumerate(sorted_files):
    # Determine the day (01, 11, or 21) for each file
    new_day = 1 + (idx % 3) * 10  # This will give us 1, 11, 21 as the day

    # Calculate the new month and year
    new_month = (current_date.month + (idx // 3)) % 12  # This moves to the next month after every 3 files
    new_year = current_date.year + ((current_date.month + (idx // 3)) // 12)  # Adjust the year after December (month 12)
    
    # Handle the transition if new_month is 0 (December case)
    if new_month == 0:
        new_month = 12
        new_year -= 1

    # Create the new date using calculated year, month, and day
    new_date = datetime(new_year, new_month, new_day)

    # Format the new filename as 'YYYY-MM-DD.png'
    new_filename = new_date.strftime('%Y-%m-%d') + '.png'
    
    # Define the full file path for old and new filenames
    old_file_path = os.path.join(directory_path, filename)
    new_file_path = os.path.join(directory_path, new_filename)
    
    # Rename the file
    #os.rename(old_file_path, new_file_path)
    print(f"Renamed: {filename} -> {new_filename}")