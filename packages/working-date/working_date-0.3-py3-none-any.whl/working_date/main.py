import sys
import datetime

def add_working_days(start_date, num_working_days):
    current_date = start_date
    while num_working_days > 0:
        current_date += datetime.timedelta(days=1)
        # Check if the current day is a weekday (Monday to Friday)
        if current_date.weekday() < 5:  # Monday=0, Sunday=6
            num_working_days -= 1
    return current_date

def get_date():
    # Get the number of working days from the command line argument
    if len(sys.argv) != 2:
        print("Usage: add_working_days.py <number_of_working_days>")
        sys.exit(1)

    try:
        num_working_days = int(sys.argv[1])
    except ValueError:
        print("Please provide an integer value for the number of working days.")
        sys.exit(1)

    # Get the current date
    current_date = datetime.date.today()

    # Calculate the new date after adding the working days
    new_date = add_working_days(current_date, num_working_days)

    # Print the result
    print(f"Current date: {current_date}")
    print(f"New date after adding {num_working_days} working days: {new_date}")