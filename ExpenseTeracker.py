# =========================================
# EXPENSE TRACKER PROJECT WITH PIE CHART
# =========================================

import csv
import os
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"


# =========================================
# Create CSV File If Not Exists
# =========================================

if not os.path.exists(FILE_NAME):

    with open(FILE_NAME, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Amount", "Category", "Date"])


# =========================================
# Add Expense
# =========================================

def add_expense():

    try:
        amount = float(input("Enter Amount: ₹"))

    except ValueError:

        print("Invalid Amount! Please enter numbers only.\n")
        return

    category = input("Enter Category: ")
    date = input("Enter Date (DD-MM-YYYY): ")

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

        print("\n========== ALL EXPENSES ==========")

        for row in reader:
            print(row)

        print()


# =========================================
# Show Total Expense
# =========================================

def show_total():

    total = 0

    with open(FILE_NAME, "r") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            total += float(row[0])

    print(f"\nTotal Expense = ₹{total}\n")


# =========================================
# Search By Category
# =========================================

def search_category():

    search = input("Enter Category To Search: ")

    found = False

    with open(FILE_NAME, "r") as file:

        reader = csv.reader(file)

        next(reader)

        print(f"\nExpenses Under '{search}' Category:\n")

        for row in reader:

            if row[1].lower() == search.lower():

                print(row)

                found = True

    if not found:
        print("No Expenses Found!")

    print()

# =========================================
# Expense Pie Chart
# =========================================

def show_graph():

    categories = {}

    with open(FILE_NAME, "r") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            amount = float(row[0])
            category = row[1]

            if category in categories:

                categories[category] += amount

            else:

                categories[category] = amount

    # No Data Check
    if len(categories) == 0:

        print("No Expense Data Available!\n")
        return

    # Pie Chart
    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%'
    )

    plt.title("Expense Distribution")

    plt.show()

# =========================================
# Main Menu
# =========================================

while True:

    print("========== EXPENSE TRACKER ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total Expense")
    print("4. Search By Category")
    print("5. Show Expense Pie Chart")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    # Add Expense
    if choice == "1":

        add_expense()

    # View Expenses
    elif choice == "2":

        view_expenses()

    # Show Total
    elif choice == "3":

        show_total()

    # Search Category
    elif choice == "4":

        search_category()

    # Show Pie Chart
    elif choice == "5":

        show_graph()

    # Exit
    elif choice == "6":

        print("Exiting Program...")
        break

    # Invalid Choice
    else:

        print("Invalid Choice! Please Try Again.\n")