import pdfplumber
import json
import re
from datetime import datetime

def assign_time(prayer_time_dict, prayer, value, previous_day_data=None):
    """Assigns the time for a prayer, falling back to previous day's data if value is missing."""
    if value != "“":
        prayer_time_dict[prayer] = value
    elif previous_day_data:
        # Use previous day's data if the current value is missing
        prayer_time_dict[prayer] = previous_day_data.get(prayer, None)
    else:
        # Optionally set to None if no data available
        prayer_time_dict[prayer] = None

def parse_line_to_dict(line, previous_day_data, current_month_year):
    """Parses a line into a structured dictionary with corrected column alignment."""
    parts = line.split()
    if parts[0] == '1':
        if len(parts) == 15:
            # Deletes unnecessary data
            del parts[3]
            del parts[3]
        else:
            del parts[3]

    try:
        # Extract day as integer
        day = int(parts[0])
        day_name = parts[1]  # Extract day name (e.g., MON, TUE)

        if day == 1:
            current_month_year["month"] += 1
            if current_month_year["month"] > 12:  # Prevent rollover
                current_month_year["month"] = 12


        # Use current month and year directly without automatic rollover
        month = current_month_year["month"]
        year = current_month_year["year"]

        # Check for invalid dates
        if not (1 <= day <= 31):
            raise ValueError(f"Invalid day {day} for month {month} in year {year}")

        # Assuming the existing code where you extract the date and format it
        date_obj = datetime(year, month, day)

        # Get the full day name (e.g., "Monday", "Tuesday")
        day_name = date_obj.strftime("%A")  # Full weekday name (e.g., "Monday")

        # Format the full date
        date_formatted = date_obj.strftime("%d %B %Y")

        # Extract Hijri date
        hijri_date = parts[2]

        # Extract beginning times in the correct order
        beginning_times = {}
        # Extract jamaat times
        jamat_times = {}

        # Define the correct order for beginning_times and jamat_times keys
        beginning_keys = ["fajr", "sunrise", "zuhr", "asr", "maghrib", "isha"]
        jamat_keys = ["fajr", "zuhr", "asr", "maghrib", "isha"]

        for i in range(len(parts)):
            if parts[0] == '1':
                # Handle the first entry (and update previous_day_data if necessary)
                if i == 2 and parts[i] != "“":
                    hijri_date = parts[i]
                elif i == 3:
                    assign_time(beginning_times, "fajr", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["fajr"] = parts[i]
                elif i == 4:
                    assign_time(beginning_times, "sunrise", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["sunrise"] = parts[i]
                elif i == 5:
                    assign_time(beginning_times, "zuhr", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["zuhr"] = parts[i]
                elif i == 6:
                    assign_time(beginning_times, "asr", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["asr"] = parts[i]
                elif i == 11:
                    assign_time(beginning_times, "maghrib", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["maghrib"] = parts[i]
                elif i == 7:
                    assign_time(beginning_times, "isha", parts[i], previous_day_data["beginning_times"])
                    previous_day_data["beginning_times"]["isha"] = parts[i]
                elif i == 8:
                    assign_time(jamat_times, "fajr", parts[i], previous_day_data["jamat_times"])
                    previous_day_data["jamat_times"]["fajr"] = parts[i]
                elif i == 9:
                    assign_time(jamat_times, "zuhr", parts[i], previous_day_data["jamat_times"])
                    previous_day_data["jamat_times"]["zuhr"] = parts[i]
                elif i == 10:
                    assign_time(jamat_times, "asr", parts[i], previous_day_data["jamat_times"])
                    previous_day_data["jamat_times"]["asr"] = parts[i]
                elif i == 11:
                    assign_time(jamat_times, "maghrib", parts[i], previous_day_data["jamat_times"])
                    previous_day_data["jamat_times"]["maghrib"] = parts[i]
                elif i == 12:
                    assign_time(jamat_times, "isha", parts[i], previous_day_data["jamat_times"])
                    previous_day_data["jamat_times"]["isha"] = parts[i]
            else:
                # Handle the rest of the entries
                if i == 2 and parts[i] != "“":
                    hijri_date = parts[i]
                elif i == 3:
                    assign_time(beginning_times, "fajr", parts[i], previous_day_data["beginning_times"])
                elif i == 4:
                    assign_time(beginning_times, "sunrise", parts[i], previous_day_data["beginning_times"])
                elif i == 5:
                    assign_time(beginning_times, "zuhr", parts[i], previous_day_data["beginning_times"])
                elif i == 6:
                    assign_time(beginning_times, "asr", parts[i], previous_day_data["beginning_times"])
                elif i == 11:
                    assign_time(beginning_times, "maghrib", parts[i], previous_day_data["beginning_times"])
                elif i == 7:
                    assign_time(beginning_times, "isha", parts[i], previous_day_data["beginning_times"])
                elif i == 8:
                    assign_time(jamat_times, "fajr", parts[i], previous_day_data["jamat_times"])
                elif i == 9:
                    assign_time(jamat_times, "zuhr", parts[i], previous_day_data["jamat_times"])
                elif i == 10:
                    assign_time(jamat_times, "asr", parts[i], previous_day_data["jamat_times"])
                elif i == 11:
                    assign_time(jamat_times, "maghrib", parts[i], previous_day_data["jamat_times"])
                elif i == 12:
                    assign_time(jamat_times, "isha", parts[i], previous_day_data["jamat_times"])

        # Ensure the times are in the correct order
        beginning_times = {key: beginning_times.get(key) for key in beginning_keys}
        jamat_times = {key: jamat_times.get(key) for key in jamat_keys}
        jamat_times["maghrib"] = beginning_times["maghrib"]

        return {
            "date": date_formatted,
            "day": day_name,
            "hijri_date": hijri_date,
            "beginning_times": beginning_times,
            "jamat_times": jamat_times,
        }, True  # valid flag set to True
    except Exception as e:
        print(f"Error parsing line: {line}, Error: {e}")
        return None, False  # Return None and invalid flag if there's an error

def pdf_to_structured_json(pdf_file_path, json_file_path, start_month=0, start_year=2025):
    data = []
    current_month_year = {"month": start_month, "year": start_year}

    previous_day_data = None  # Start with no previous day data

    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                lines = page.extract_text().split("\n")
                for line in lines:
                    if re.match(r"^\d{1,2} \w{3}", line):  # Matches lines starting with a date
                        parsed_data, valid = parse_line_to_dict(line, previous_day_data or {"beginning_times": {}, "jamat_times": {}}, current_month_year)
                        if valid:
                            data.append(parsed_data)
                            previous_day_data = parsed_data
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data successfully structured and saved to {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
pdf_to_structured_json("taiyabah_timetable_2025.pdf", "structured_output.json")
