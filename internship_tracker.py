import json
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = "internship_hours.json"

# ===============================
# data functions
# ===============================

def load_data():
    """load internship data, or create default data."""

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

                # make sure entries is a list
                if not isinstance(data.get("entries"), list):
                    data["entries"] = []

                # make sure minimum_required_hours exists
                if "minimum_required_hours" not in data:
                    data["minimum_required_hours"] = 0

                return data

        except json.JSONDecodeError:
            print("Error reading data file. Creating new data file.")

    return {
        "minimum_required_hours": 0,
        "entries": []
    }


def save_data(data):
    """save internship hours data."""

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# ===============================
# helper functions
# ===============================

def get_date():
    """get date from user input."""

    while True:
        date = input(
            "Date (YYYY-MM-DD, leave blank for today): "
        ).strip()

        if not date:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def get_hours():
    """get hours worked from user input."""

    while True:
        try:
            hours = float(input("Hours worked: "))

            if hours < 0:
                print("Hours cannot be negative.")
                continue

            if hours > 24:
                print("Hours cannot exceed 24 in a single day.")
                continue

            return hours

        except ValueError:
            print("Invalid number of hours.")


def get_total_hours(data):
    """calculate total hours worked."""

    return sum(
        entry["hours"] for entry in data["entries"]
    )


def get_sorted_entries(data):
    """return entries sorted by date."""

    return sorted(
        data["entries"],
        key=lambda entry: entry["date"]
    )


def print_line():
    """print a line separator."""

    print("-" * 70)


# ===============================
# add an entry
# ===============================

def add_entry(data):

    print("\n--- ADD HOURS WORKED ---")
    print_line()

    date = get_date()
    hours = get_hours()

    description = input(
        "What did you work on? (optional): "
    ).strip()

    location = input(
        "Where did you work? (Office / Remote / Other, optional): "
    ).strip()

    entry = {
        "date": date,
        "hours": hours,
        "description": description,
        "location": location
    }

    data["entries"].append(entry)

    save_data(data)

    print()
    print(f"Added {hours:.2f} hours for {date}.")


# ===============================
# view entries
# ===============================

def view_entries(data):

    entries = get_sorted_entries(data)

    if not entries:
        print("\nNo entries found.")
        return

    print("\n--- VIEW HOURS WORKED ---")
    print_line()

    print(
        f"{'#':<4}"
        f"{'Date':<15}"
        f"{'Hours':<10}"
        f"{'Location':<15}"
        f"{'Description'}"
    )

    print_line()

    for index, entry in enumerate(entries, start=1):
        print(
            f"{index:<4}"
            f"{entry['date']:<15}"
            f"{entry['hours']:<10.2f}"
            f"{entry['location'] or '--':<15}"
            f"{entry['description'] or '--'}"
        )


# ===============================
# edit entries
# ===============================

def edit_entry(data):

    entries = get_sorted_entries(data)

    if not entries:
        print("\nNo entries found.")
        return

    view_entries(data)

    try:
        choice = int(
            input("\nEnter the entry number to edit: ")
        )

        if choice < 1 or choice > len(entries):
            print("Invalid entry number.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    entry = entries[choice - 1]

    print("\nLeave a field blank to keep the current value.")

    # date
    new_date = input(
        f"Date (YYYY-MM-DD) [{entry['date']}]: "
    ).strip()

    if new_date:
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            entry["date"] = new_date

        except ValueError:
            print(
                "Invalid date format. Keeping the current date."
            )

    # hours
    new_hours = input(
        f"Hours worked [{entry['hours']}]: "
    ).strip()

    if new_hours:
        try:
            hours = float(new_hours)

            if 0 <= hours <= 24:
                entry["hours"] = hours

            else:
                print(
                    "Hours must be between 0 and 24. "
                    "Keeping the current hours."
                )

        except ValueError:
            print(
                "Invalid number of hours. "
                "Keeping the current hours."
            )

    # description
    new_description = input(
        f"Description [{entry['description']}]: "
    ).strip()

    if new_description:
        entry["description"] = new_description

    # location
    new_location = input(
        f"Location [{entry['location']}]: "
    ).strip()

    if new_location:
        entry["location"] = new_location

    save_data(data)

    print()
    print("Entry updated.")


# ===============================
# delete entries
# ===============================

def delete_entry(data):

    entries = get_sorted_entries(data)

    if not entries:
        print("\nNo entries found.")
        return

    view_entries(data)

    try:
        choice = int(
            input("\nEnter the entry number to delete: ")
        )

        if choice < 1 or choice > len(entries):
            print("Invalid entry number.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    entry = entries[choice - 1]

    confirm = input(
        f"Are you sure you want to delete the entry "
        f"for {entry['date']}? (y/n): "
    ).strip().lower()

    if confirm == "y":
        data["entries"].remove(entry)
        save_data(data)
        print("Entry deleted.")

    else:
        print("Deletion cancelled.")


# ===============================
# dashboard
# ===============================

def view_dashboard(data):

    total_hours = get_total_hours(data)

    minimum_required_hours = data.get(
        "minimum_required_hours",
        0
    )

    remaining = max(
        minimum_required_hours - total_hours,
        0
    )

    number_of_entries = len(data["entries"])

    average_hours = (
        total_hours / number_of_entries
        if number_of_entries > 0
        else 0
    )

    print("\n--- DASHBOARD ---")
    print_line()

    print(f"Total hours worked: {total_hours:.2f}")
    print(
        f"Minimum required hours: "
        f"{minimum_required_hours:.2f}"
    )
    print(f"Remaining hours: {remaining:.2f}")
    print(f"Number of entries: {number_of_entries}")
    print(
        f"Average hours per entry: "
        f"{average_hours:.2f}"
    )

    # progress
    if minimum_required_hours > 0:

        percentage_completed = (
            total_hours / minimum_required_hours
        ) * 100

        print(
            f"Percentage completed: "
            f"{percentage_completed:.2f}%"
        )

    else:
        print("Minimum required hours not set.")


# ===============================
# weekly summary
# ===============================

def view_weekly_summary(data):

    if not data["entries"]:
        print("\nNo entries found.")
        return

    weekly_hours = defaultdict(float)

    for entry in data["entries"]:

        date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        )

        year, week, _ = date.isocalendar()

        key = f"{year}-W{week:02d}"

        weekly_hours[key] += entry["hours"]

    print("\n--- WEEKLY SUMMARY ---")
    print_line()

    for week, hours in sorted(
        weekly_hours.items()
    ):
        print(
            f"{week}: {hours:.2f} hours"
        )


# ===============================
# monthly summary
# ===============================

def view_monthly_summary(data):

    if not data["entries"]:
        print("\nNo entries found.")
        return

    monthly_hours = defaultdict(float)

    for entry in data["entries"]:

        date = datetime.strptime(
            entry["date"],
            "%Y-%m-%d"
        )

        key = f"{date.year}-{date.month:02d}"

        monthly_hours[key] += entry["hours"]

    print("\n--- MONTHLY SUMMARY ---")
    print_line()

    for month, hours in sorted(
        monthly_hours.items()
    ):
        print(
            f"{month}: {hours:.2f} hours"
        )


# ===============================
# required hours
# ===============================

def set_required_hours(data):

    try:

        hours = float(
            input(
                "Enter the minimum required hours: "
            )
        )

        if hours < 0:
            print(
                "Minimum required hours "
                "cannot be negative."
            )
            return

        data["minimum_required_hours"] = hours

        save_data(data)

        print(
            "Minimum required hours updated."
        )

    except ValueError:
        print(
            "Invalid input. Please enter "
            "a valid number."
        )


# ===============================
# main menu
# ===============================

def main():

    data = load_data()

    while True:

        print("\n--- INTERNSHIP HOURS TRACKER ---")
        print_line()

        print("1. Add hours worked")
        print("2. View hours worked")
        print("3. Edit an entry")
        print("4. Delete an entry")
        print("5. View dashboard")
        print("6. View weekly summary")
        print("7. View monthly summary")
        print("8. Set minimum required hours")
        print("9. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            add_entry(data)

        elif choice == "2":
            view_entries(data)

        elif choice == "3":
            edit_entry(data)

        elif choice == "4":
            delete_entry(data)

        elif choice == "5":
            view_dashboard(data)

        elif choice == "6":
            view_weekly_summary(data)

        elif choice == "7":
            view_monthly_summary(data)

        elif choice == "8":
            set_required_hours(data)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print(
                "Invalid choice. Please try again."
            )


if __name__ == "__main__":
    main()