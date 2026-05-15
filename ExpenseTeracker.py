# =========================================
# EXPENSE TRACKER PROJECT WITH PIE CHART
# =========================================

import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"


# =========================================
# Create CSV File If Not Exists
# =========================================

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category", "Date"])


# =========================================
# Add Expense
# =========================================

def add_expense():
    # Validate amount
    try:
        amount = float(input("Enter Amount: ₹"))
        if amount <= 0:
            print("Amount must be greater than zero.\n")
            return
    except ValueError:
        print("Invalid Amount! Please enter numbers only.\n")
        return

    category = input("Enter Category: ").strip()
    if not category:
        print("Category cannot be empty.\n")
        return

    # Validate date
    date = input("Enter Date (DD-MM-YYYY): ").strip()
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format! Please use DD-MM-YYYY.\n")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, date])

    print("Expense Added Successfully!\n")


# =========================================
# View Expenses
# =========================================

def view_expenses():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n========== ALL EXPENSES ==========")
    print(f"{'Amount':<12} {'Category':<20} {'Date'}")
    print("-" * 42)

    for row in rows[1:]:
        print(f"₹{float(row[0]):<11.2f} {row[1]:<20} {row[2]}")

    print()


# =========================================
# Show Total Expense
# =========================================

def show_total():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    if not rows:
        print("\nNo expenses recorded yet.\n")
        return

    total = sum(float(row[0]) for row in rows if row)
    print(f"\nTotal Expense = ₹{total:.2f}\n")


# =========================================
# Search By Category
# =========================================

def search_category():
    search = input("Enter Category To Search: ").strip()

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    matches = [row for row in rows if row and row[1].lower() == search.lower()]

    if not matches:
        print(f"\nNo expenses found under '{search}' category.\n")
        return

    category_total = sum(float(row[0]) for row in matches)

    print(f"\nExpenses Under '{search}' Category:\n")
    print(f"{'Amount':<12} {'Category':<20} {'Date'}")
    print("-" * 42)

    for row in matches:
        print(f"₹{float(row[0]):<11.2f} {row[1]:<20} {row[2]}")

    print(f"\nCategory Total = ₹{category_total:.2f}\n")


# =========================================
# Delete an Expense
# =========================================

def delete_expense():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("\nNo expenses to delete.\n")
        return

    print("\n========== SELECT EXPENSE TO DELETE ==========")
    print(f"{'No.':<5} {'Amount':<12} {'Category':<20} {'Date'}")
    print("-" * 50)

    for i, row in enumerate(rows[1:], start=1):
        print(f"{i:<5} ₹{float(row[0]):<11.2f} {row[1]:<20} {row[2]}")

    try:
        choice = int(input("\nEnter expense number to delete (0 to cancel): "))
    except ValueError:
        print("Invalid input.\n")
        return

    if choice == 0:
        print("Delete cancelled.\n")
        return

    if choice < 1 or choice > len(rows) - 1:
        print("Invalid number.\n")
        return

    deleted = rows.pop(choice)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"\nDeleted: ₹{float(deleted[0]):.2f} | {deleted[1]} | {deleted[2]}\n")


# =========================================
# Clear Expense History
# =========================================

def clear_history():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("\nNo expenses to clear.\n")
        return

    print("\n========== CLEAR EXPENSE HISTORY ==========")
    print("1. Clear All Expenses")
    print("2. Clear By Month (MM-YYYY)")
    print("3. Clear By Date Range (DD-MM-YYYY to DD-MM-YYYY)")
    print("0. Cancel")

    choice = input("Enter Your Choice: ").strip()

    header = rows[0]
    data_rows = rows[1:]

    # ----- Clear All -----
    if choice == "1":
        confirm = input("Are you sure you want to delete ALL expenses? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.\n")
            return

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)

        print("All expenses cleared successfully!\n")

    # ----- Clear By Month -----
    elif choice == "2":
        month_input = input("Enter Month (MM-YYYY): ").strip()
        try:
            target = datetime.strptime(month_input, "%m-%Y")
        except ValueError:
            print("Invalid format! Use MM-YYYY.\n")
            return

        kept = []
        removed = 0
        for row in data_rows:
            if not row:
                continue
            row_date = datetime.strptime(row[2], "%d-%m-%Y")
            if row_date.month == target.month and row_date.year == target.year:
                removed += 1
            else:
                kept.append(row)

        if removed == 0:
            print(f"No expenses found for {month_input}.\n")
            return

        confirm = input(f"Delete {removed} expense(s) from {month_input}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.\n")
            return

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(kept)

        print(f"{removed} expense(s) from {month_input} deleted successfully!\n")

    # ----- Clear By Date Range -----
    elif choice == "3":
        start_input = input("Enter Start Date (DD-MM-YYYY): ").strip()
        end_input = input("Enter End Date (DD-MM-YYYY): ").strip()

        try:
            start_date = datetime.strptime(start_input, "%d-%m-%Y")
            end_date = datetime.strptime(end_input, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format! Use DD-MM-YYYY.\n")
            return

        if start_date > end_date:
            print("Start date cannot be after end date.\n")
            return

        kept = []
        removed = 0
        for row in data_rows:
            if not row:
                continue
            row_date = datetime.strptime(row[2], "%d-%m-%Y")
            if start_date <= row_date <= end_date:
                removed += 1
            else:
                kept.append(row)

        if removed == 0:
            print(f"No expenses found between {start_input} and {end_input}.\n")
            return

        confirm = input(f"Delete {removed} expense(s) between {start_input} and {end_input}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.\n")
            return

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(kept)

        print(f"{removed} expense(s) deleted successfully!\n")

    elif choice == "0":
        print("Cancelled.\n")

    else:
        print("Invalid Choice!\n")


# =========================================
# Expense Pie Chart
# =========================================

def show_graph():
    categories = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    if not rows:
        print("No Expense Data Available!\n")
        return

    for row in rows:
        if not row:
            continue
        amount = float(row[0])
        category = row[1]
        categories[category] = categories.get(category, 0) + amount

    plt.figure(figsize=(7, 7))
    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title("Expense Distribution by Category")
    plt.tight_layout()
    plt.show()


# =========================================
# Main Menu
# =========================================

def main():
    initialize_file()

    while True:
        print("========== EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expense")
        print("4. Search By Category")
        print("5. Delete an Expense")
        print("6. Clear Expense History")
        print("7. Show Expense Pie Chart")
        print("8. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            search_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            clear_history()
        elif choice == "7":
            show_graph()
        elif choice == "8":
            print("Exiting Program. Goodbye!\n")
            break
        else:
            print("Invalid Choice! Please Try Again.\n")


if __name__ == "__main__":
    main()
