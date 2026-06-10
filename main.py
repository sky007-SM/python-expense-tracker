# Python Expense Tracker

from datetime import datetime  # Imported datetime to get date of entry
from typing import (
    Iterator,
    TypedDict,
)  # Imported Iterator and TypedDict for type hinting
from re import search  # Imported search from regular method for format validation


# Explicit type hinting via TypedDIct for expense_entries
class ExpenseEntries(TypedDict):
    item_category: list[str]
    item_name: list[str]
    item_cost: list[float]
    item_entry_date: list[str]
    record_list: list[str]


type expense_entries = ExpenseEntries

# Constants for File Location and File Header and Entry Format Specifiers
EXPENSES_FILE_NAME: str = "file-manager/text-files/expenses.txt"
EXPENSE_TRACKER_HEADER: str = "CATEGORY | ITEM_NAME | ITEM_COST | DATE\n"
FORMAT_TYPE_1: str = r"^[a-zA-Z0-9]+\s\:\s[a-zA-Z0-9]+\s\:\s\$\d+\s\:\s\d+\-\d+\-\d+$"
FORMAT_TYPE_2: str = r"^\w+\s\|\s\w+\s\|\s\w+\s\|\s\w+$"


# Function that deletes expenses history
def clear_records() -> None:
    # File open in write mode erases entire file before writing
    with open(EXPENSES_FILE_NAME, "w") as file:
        file.write(EXPENSE_TRACKER_HEADER)
    print("Expense History has been Erased ")


# Function that displays text file content
def view_expenses(counter: int) -> Iterator[str]:
    try:
        # File open in read mode for accessing data
        with open(EXPENSES_FILE_NAME, "r") as file:
            # Conditions for file format integrity preservation
            if counter == 0:
                line: str
                format_match: bool = False
                # Returns newline character as well with each line
                for line in file:
                    format_match = search(FORMAT_TYPE_1, line)
                    if counter > 0:
                        if format_match:
                            yield line  # Generator used for streaming file content
                    counter += (
                        1  # Used to eliminate and include Header in record produced
                    )
            else:
                line: str
                format_match: bool = False
                # Returns newline character as well with each line
                for line in file:
                    if counter == 1:
                        format_match = search(FORMAT_TYPE_2, line)
                    else:
                        format_match = search(FORMAT_TYPE_1, line)
                    if counter > 0:
                        if format_match:
                            yield line  # Generator used for streaming file content
                    counter += (
                        1  # Used to eliminate and include Header in record produced
                    )
    # Handles File not found error
    except FileNotFoundError:
        print(f"Sorry, the file {EXPENSES_FILE_NAME} does not exist")


# Function that collects data and merges it to for an entry
def add_item() -> str:
    category: str = input("Enter Category of item: ").strip().title()
    item_name: str = input("Enter name of item: ").strip().tite()
    # Loop that Ensures only digits are entered
    while True:
        amount: str = input("Enter Cost of item: ").strip().lstrip("$")
        # Boolean operation ensures either case is valid
        format_match: bool = (
            search(r"\d+\.\d+", amount) or amount.isdigit()
        )  # Search method to check expression format with
        if format_match:
            break
        print("Error: Invalid Input Enter a number")
    now: datetime = datetime.now()  # Date time variable initialised
    entry_date: str = now.strftime("%Y-%m-%d")  # Date collected as string
    expense_entry: str = (
        f"{category} : {item_name} : ${amount} : {entry_date}\n"  # Ensures format is maintained
    )
    return expense_entry


# Function that adds the data entry to file
def add_expense() -> None:
    # File open in append and read mode, does not erase contents but can write only at end of file
    with open(EXPENSES_FILE_NAME, "a+") as file:
        file.write(str(add_item()))  # Invokes add item function
        print(f"Expense Successfully Added")


# Function that summarizes expenditure
def show_summary() -> None:
    # Loop that ensures valid input
    while True:
        try:
            expense_budget: float = float(input("Enter the Budget for Expenses: "))
            break
        except ValueError:
            print(
                "Error: Invalid number input, please enter a valid number"
            )  # Handles Invalid character input
    # Invokes view expenses and use generator converted to list object
    records: list[str] = list(
        view_expenses(0)
    )  # Important to convert to list object via list type caster
    # Dictionary to seperate value fields
    expense_details: expense_entries = {
        "item_category": [],
        "item_name": [],
        "item_cost": [],
        "item_entry_date": [],
    }
    entries_present: bool = False
    record: str
    for record in records:
        record_list = record.split(" : ")
        expense_details["item_entry_date"].append(record_list.pop())
        expense_details["item_cost"].append(float((record_list.pop()).lstrip("$")))
        expense_details["item_name"].append(record_list.pop())
        expense_details["item_category"].append(record_list.pop())

    if expense_details["item_cost"]:
        total_expense: float = sum(expense_details["item_cost"])
        most_expensive_item: float = max(expense_details["item_cost"])
        most_expensive_item_name: str = expense_details["item_name"][
            expense_details["item_cost"].index(most_expensive_item)
        ]
        entries_present = True
    print("\n======= Expense Summary =======\n")
    print(f"Total No. of Items: {len(records)}")
    # Guard to prevent invoking max and sum function in empty list
    if entries_present:
        print(f"Total Expense: ${total_expense}")
        print(
            f"\nMost Expensive Item:\n  {most_expensive_item_name} = ${most_expensive_item}"
        )
        print("\n======= Budget Summary =======\n")
        if total_expense > expense_budget:
            print(
                f"Warning: Spendings exceeded budget by ${total_expense - expense_budget}"
            )
        elif total_expense < expense_budget:
            print(
                f"Spendings maintained within budget \nRemaining Amount: ${expense_budget -total_expense}"
            )
        elif total_expense == expense_budget:
            print(f"Expenses Have Consumed Entire Budget")
    else:
        print("No Expense entries present")


# Function that provides menu interface
def menu() -> None:
    print(f"======= Python Expense Tracker =======")
    while True:

        print(f"\n1. Add Item Expense")
        print(f"2. View Current Expenses")
        print(f"3. Summarize Expenses")
        print(f"4. Clear Expense History")
        print(f"\n\n Quit -q\n")

        choice: str = (input("Enter your choice (1, 2, 3, 4 or q): ")).lower().strip()

        while choice not in ["1", "2", "3", "4", "q"]:  # Handles Invalid choice input
            print("\nInvalid choice entry")
            choice = input("Enter your choice (1, 2, 3, 4 or q): ").lower().strip()
        print("\n")
        if choice == "1":
            add_expense()
        elif choice == "2":
            records: list[str] = list(
                view_expenses(1)
            )  # Invokes view expenses and use generator converted to list object
            record: str
            for record in records:
                print(record)
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print(f"Warning: You cannot restore deleted records")
            confirm: str = (
                input("Are you sure you want to delete expense history (y/n): ")
                .lower()
                .strip()
            )
            while confirm not in ["y", "n"]:  # Handles Invalid choice input
                print("\nInvalid choice entry")
                confirm_retry: str = input("Enter your choice (y/n): ").lower().strip()
                confirm = confirm_retry
            if confirm == "y":
                clear_records()  # Invokes clear history function
            else:
                continue  # resumes back to menu without return to menu option
        elif choice == "q":
            break

        print(f"\nReturn to Menu -r\t\t2. Quit -q ")
        action: str = (input("Enter your choice (r/q): ")).lower().strip()
        while action not in ["r", "q"]:  # Handles Invalid choice input
            print("\nInvalid choice entry")
            action = input("Enter your choice (r/q): ").lower().strip()

        if action == "q":
            break


# The main function
def main() -> None:
    # File open in append and read mode, does not erase contents but can write only at end of file
    with open(EXPENSES_FILE_NAME, "a+") as file:
        title: str = ""
        file.seek(0)  # Used to set cursor at beginning
        line: str
        # Loop that checks if header exist
        for line in file:
            title = line
            break
        if title != EXPENSE_TRACKER_HEADER:  # Condition that adds header if not present
            record_list: list[str] = list(
                view_expenses(0)
            )  # Invokes view expenses and stores entire file in temporary list
            file.seek(0)
            file.truncate()  # Deletes all content via the file within currently opened instance
            file.write(EXPENSE_TRACKER_HEADER)
            if record_list:
                file.writelines(record_list)

    menu()


# Guard header in case imported
if __name__ == "__main__":
    main()
