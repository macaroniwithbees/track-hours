import json
import os
from datetime import datetime

FILE_NAME = "internship_hours.json"

def load_data():
    """load internship data, or create default data file"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    return {
        "minimum_required_hours": 0,
        "entries": {}
    }

def save_data(data):
    """save internship hours data"""
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def add_hours(data):
    date = input("Date (YYYY-MM-DD, leave blank for today): ").strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    try:
        hours = float(input("Hours worked: "))
    except ValueError:
        print("Invalid number of hours.")
        return

    data["entries"][date] = hours
    save_data(data)

    print(f"Added {hours} hours for {date}.")

def view_summary(data):
    total_hours = sum(data["entries"].values())
    required = data["minimum_required_hours"]
    remaining = max(0, required - total_hours)

    print("\n--- INTERNSHIP SUMMARY ---")
    print(f"Total hours worked: {total_hours}")
    print(f"Minimum required hours: {required}")
    print(f"Remaining hours to complete: {remaining}\n")

    if required > 0 and total_hours >= required:
        print("Congratulations! Minimum required internship hours achieved!")

    print("\n--- DAILY ENTRIES ---")

    if not data["entries"]:
        print("No entries yet.")
    else:
        for date, hours in sorted(data["entries"].items()):
            print(f"{date}: {hours:.2f} hours")

def set_required_hours(data):
    try:
        hours = float(input("Enter minimum required internship hours: "))
        data["minimum_required_hours"] = hours
        save_data(data)
        print("Minimum required hours updated.")
    except ValueError:
        print("Invalid number of hours.")

def main():
    data = load_data()

    while True:
        print("\n--- INTERNSHIP HOURS TRACKER ---")
        print("1. Add hours worked")
        print("2. View summary")
        print("3. Set minimum required hours")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_hours(data)
        elif choice == "2":
            view_summary(data)
        elif choice == "3":
            set_required_hours(data)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
