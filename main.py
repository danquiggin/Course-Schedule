import csv
from datetime import datetime

def parse_time(time_str, am_pm=None):
    """
    Parse the time string and assign AM/PM based on time.
    """
    if not time_str:
        raise ValueError(f"Time string is empty: {time_str}")

    # Remove any extra whitespace and check if time is in 12-hour format already
    time_str = time_str.strip()

    # If no AM/PM is provided, add AM/PM based on the hour
    if 'AM' not in time_str and 'PM' not in time_str:
        hour = int(time_str.split(":")[0])

        # Adjust AM/PM based on the time range
        if 8 <= hour <= 11:  # Between 8:00 AM and 11:59 AM
            am_pm = 'AM'
        elif 1 <= hour < 8 or 11<hour<13:  # Between 1:00 PM and 5:59 PM
            am_pm = 'PM'
        else:
            raise ValueError(f"Invalid time range: {time_str}")

        # Add AM/PM to the time string
        time_str += f" {am_pm}"

    try:
        # Now parse the string to datetime and return in 12-hour format
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        return time_obj.strftime("%I:%M %p")  # Return the 12-hour AM/PM formatted time
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

def convert_schedule_to_events(csv_filename, output_js_filename):
    events = []
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Days/Time']:  # Check if Days/Time column is not empty
                try:
                    days_time = row['Days/Time'].strip()
                    days, time_range = days_time.split(' ', 1)  # Split days and time range
                    title = row['Title']  # Class Title
                    instructor = row['Instructor']
                    room = row['Room']
                    modality = row['Modality']
                    capacity = row['Capacity']
                    year=row['Year']

                    start_time, end_time = time_range.split(' - ')  # Split start and end time

                    # Convert times to a consistent format (if needed)
                    start_time = parse_time(start_time)
                    end_time = parse_time(end_time)

                    # Map days to numerical representation
                    days_of_week = []
                    if 'M' in days:
                        days_of_week.append(1)  # Monday
                    if 'T' in days:
                        days_of_week.append(2)  # Tuesday
                    if 'W' in days:
                        days_of_week.append(3)  # Wednesday
                    if 'Th' in days:
                        days_of_week.append(4)  # Thursday
                    if 'F' in days:
                        days_of_week.append(5)  # Friday

                    event = {
                        "title": title,
                        "startTime": start_time,
                        "endTime": end_time,
                        "daysOfWeek": days_of_week,
                        "extendedProps": {
                            "instructor": instructor,
                            "room": room,
                            "modality": modality,
                            "capacity": capacity,
                            "year": year
                        }
                    }

                    events.append(event)

                except ValueError:
                    print(f"Skipping online class: {row}")  # If there's an issue with parsing, skip this row

        # Write the events to the output JS file in the format needed
    with open(output_js_filename, 'w') as js_file:
        js_file.write('const events = ' + str(events) + ';')


convert_schedule_to_events('schedule.csv', 'events.js')