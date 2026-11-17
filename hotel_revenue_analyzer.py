import csv
import math
from collections import defaultdict


def main():
    filename = input("Enter CSV file name: ").strip()

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: CSV file is empty.")
                return

            reader.fieldnames = [name.strip() for name in reader.fieldnames]

            required = ["Date", "RoomType", "RoomsSold", "Rate"]

            if not all(col in reader.fieldnames for col in required):
                print("Error: Required columns are missing.")
                return

            daily_revenue = defaultdict(float)
            room_revenue = defaultdict(float)
            valid_count = 0

            for row_number, row in enumerate(reader, start=2):

                date = (row.get("Date") or "").strip()
                room_type = (row.get("RoomType") or "").strip()

                try:
                    rooms = float(row["RoomsSold"])
                    rate = float(row["Rate"])
                except (ValueError, TypeError):
                    print(f"Warning: Row {row_number} skipped - Invalid numbers.")
                    continue

                if not math.isfinite(rooms) or not math.isfinite(rate):
                    print(f"Warning: Row {row_number} skipped - Invalid numbers.")
                    continue

                if rooms < 0 or rate < 0:
                    print(f"Warning: Row {row_number} skipped - Negative values.")
                    continue

                if not date or not room_type:
                    print(f"Warning: Row {row_number} skipped - Missing data.")
                    continue

                revenue = rooms * rate

                daily_revenue[date] += revenue
                room_revenue[room_type] += revenue
                valid_count += 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    except PermissionError:
        print("Error: Cannot access the CSV file.")
        return

    print("Valid records analysed:", valid_count)

    if valid_count == 0:
        print("No valid records found.")
        return

    print("\n1. Daily revenue")
    print("2. Revenue by room type")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        print("\nDaily Revenue")

        for date, amount in daily_revenue.items():
            print(f"{date} : Rs. {amount:.0f}")

        total = sum(daily_revenue.values())
        best_day = max(daily_revenue, key=daily_revenue.get)

        print(f"Total revenue: Rs. {total:.0f}")
        print(
            f"Best day: {best_day} "
            f"(Rs. {daily_revenue[best_day]:.0f})"
        )

    elif choice == "2":
        print("\nRevenue by Room Type")

        total = sum(room_revenue.values())

        for room_type, amount in room_revenue.items():
            share = amount / total * 100 if total > 0 else 0

            print(
                f"{room_type} : Rs. {amount:.0f} "
                f"({share:.2f}%)"
            )

        print(f"Total revenue: Rs. {total:.0f}")

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
