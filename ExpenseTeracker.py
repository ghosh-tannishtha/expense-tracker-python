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
        print("6. Show Expense Pie Chart")
        print("7. Exit")

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
            show_graph()
        elif choice == "7":
            print("Exiting Program. Goodbye!\n")
            break
        else:
            print("Invalid Choice! Please Try Again.\n")


if __name__ == "__main__":
    main()