# Python Expense Tracker

A command-line expense tracking application written in Python that allows users to record expenses, store them in a text file, analyze spending habits, identify costly purchases, and compare expenses against a budget.

## Features

* Add expense records
* Categorize expenses
* Automatic date tracking
* Store expense history in a text file
* View recorded expenses
* Expense summary generation
* Total spending calculation
* Most expensive item identification
* Budget tracking and comparison
* Remaining budget calculation
* Budget overrun warnings
* Expense history deletion
* Header validation and file repair
* Generator-based file reading
* Decimal expense support
* Input validation using regular expressions
* Menu-driven interface
* Type-safe implementation using `TypedDict`

## Concepts Used

* Functions
* Lists
* Dictionaries
* TypedDict
* Type Aliases
* Type Hinting
* Constants
* Strings
* File Handling
* Generators
* Iterators
* Loops
* Conditional Statements
* User Input Handling
* Input Validation
* Exception Handling
* Regular Expressions (`re.search`)
* Date and Time Handling with `datetime`
* List Operations (`append()`, `pop()`)
* String Processing (`split()`, `strip()`, `lstrip()`)
* Aggregation Functions (`sum()`, `max()`)
* Boolean Logic

## Run

```bash
python3 main.py
```

## Expense Record Format

```text
CATEGORY : ITEM_NAME : $ITEM_COST : YYYY-MM-DD
```

### Example

```text
Food : Burger : $150.50 : 2026-06-08
Transport : Bus Ticket : $40.00 : 2026-06-08
Entertainment : Movie Ticket : $250.75 : 2026-06-08
```

## Menu Options

| Option | Description           |
| ------ | --------------------- |
| 1      | Add Item Expense      |
| 2      | View Current Expenses |
| 3      | Summarize Expenses    |
| 4      | Clear Expense History |
| q      | Quit Application      |

## Expense Summary Output

The summary includes:

* Total number of expense entries
* Total amount spent
* Most expensive item purchased
* User budget comparison
* Remaining budget calculation
* Budget exceeded warning
* Empty expense history detection

## File Structure

```text
file-manager/
└── text-files/
    └── expenses.txt
```

## Data Storage

The application stores expenses in a plain text file and automatically maintains the required header format:

```text
CATEGORY | ITEM_NAME | ITEM_COST | DATE
```

If the header is missing or corrupted, the application automatically restores it while preserving existing expense records.

## Type Definitions

The project uses a custom `TypedDict` structure to organize expense data:

```python
class ExpenseEntries(TypedDict):
    item_category: list[str]
    item_name: list[str]
    item_cost: list[float]
    item_entry_date: list[str]
    record_list: list[str]
```

This improves readability, maintainability, and type safety throughout the application.
