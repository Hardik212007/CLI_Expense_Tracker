# Expense Tracker CLI

A lightweight, feature-rich command-line expense tracker built with Python and SQLite. Track your spending, set budgets, get smart insights, and visualize trends — all from your terminal.

---

## Getting Started

### Prerequisites

- **Python 3.6+** (no external dependencies required — uses only the standard library)

### Installation

```bash
git clone https://github.com/Hardik212007/CLI_Expense_Tracker.git
```

### Run

```bash
python3 expense_tracker.py --help
```

> The SQLite database (`expense_tracker.db`) is created automatically in the project directory the first time you run any command.

---

## Usage

All commands follow this pattern:

```bash
python3 expense_tracker.py <command> [arguments] [options]
```

---

### Add an Expense

```bash
python3 expense_tracker.py add <amount> <category> "<description>" [--date YYYY-MM-DD]
```

| Argument        || Description                                      |
|-----------------|----------|--------------------------------------------------|
| `amount`        |       | The expense amount (e.g., `50`, `12.99`)         |
| `category`      |     | Category name (e.g., `food`, `transport`, `rent`)|
| `description`   |      | A short description of the expense               |
| `--date`        |   | Date in `YYYY-MM-DD` format (defaults to today)  |

**Examples:**

```bash
# Add a food expense for today
python3 expense_tracker.py add 50 food "Dinner with friends"

# Add a transport expense with a specific date
python3 expense_tracker.py add 15 transport "Uber ride" --date 2026-06-01

# Add a utilities expense
python3 expense_tracker.py add 120 utilities "Electricity bill"
```

---


| Option          | Description                        |
|-----------------|------------------------------------|
| `--category`    | Filter by a specific category      |
| `--start-date`  | Show expenses from this date onward|
| `--end-date`    | Show expenses up to this date      |

**Examples:**

```bash
# List all expenses
python3 expense_tracker.py list

# List only food expenses
python3 expense_tracker.py list --category food

# List expenses in a date range
python3 expense_tracker.py list --start-date 2026-06-01 --end-date 2026-06-30
```

### Spending Summary

View a visual breakdown of spending by category for a given month.

```bash
python3 expense_tracker.py summary [--month YYYY-MM]
```

| Option     | Description                                       |
|------------|---------------------------------------------------|
| `--month`  | Month in `YYYY-MM` format (defaults to current month) |

**Example:**

```bash
python3 expense_tracker.py summary
python3 expense_tracker.py summary --month 2026-05
```

**Sample Output:**

```
Spending Summary for 2026-06
------------------------------------------------------------
food            | $50.00   | ██████████████████████████████
transport       | $15.00   | █████████
```

---

### Budget Management

Set monthly spending limits per category and track them.

#### Set a Budget

```bash
python3 expense_tracker.py budget set <category> <amount>
```

#### View All Budgets

```bash
python3 expense_tracker.py budget view
```

**Examples:**

```bash
# Set a $200 budget for food
python3 expense_tracker.py budget set food 200

# Set a $50 budget for transport
python3 expense_tracker.py budget set transport 50

# View all budgets
python3 expense_tracker.py budget view
```

---

### Smart Insights

Get an intelligent summary of your spending for the current month, including budget alerts.

```bash
python3 expense_tracker.py insights
```

**Sample Output:**

```
Smart Spending Insights 
----------------------------------------
Total spent this month: $185.00
Highest spending category: food ($120.00)

Budget Alerts:
   Over budget in food: Spent $120.00 / Budget $100.00
   Nearing budget in transport: Spent $42.00 / Budget $50.00
  All other categories within budget!
```

---

### Delete an Expense

```bash
python3 expense_tracker.py delete <id>
```

**Example:**

```bash
# Delete expense with ID 3
python3 expense_tracker.py delete 3
```

> Use `python3 expense_tracker.py list` to find the ID of the expense you want to delete.

---

### Export to CSV

Export all your expense data to a CSV file.

```bash
python3 expense_tracker.py export [--file FILENAME]
```

| Option   | Description                                                  |
|----------|--------------------------------------------------------------|
| `--file` | Custom output filename (defaults to `expenses_export_YYYY-MM-DD.csv`) |

**Examples:**

```bash
# Export with default filename
python3 expense_tracker.py export

# Export to a custom file
python3 expense_tracker.py export --file my_expenses.csv
```

---

### Month-over-Month Trends

See how your total spending changes month to month with directional indicators.

```bash
python3 expense_tracker.py trends
```

**Sample Output:**

```
Month-over-Month Trends
----------------------------------------
2026-04 | $320.00
2026-05 | $450.00  (↗ +$130.00)
2026-06 | $185.00  (↘ -$265.00)
```

---

## Key Features
| Feature                  | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| **Zero Dependencies**    | Uses only Python's standard library — no `pip install` needed      |
| **SQLite Storage**       | Data persists locally in a single `expense_tracker.db` file        |
| **Category Filtering**   | Filter expenses by category, start date, and end date              |
| **Visual Summaries**     | Bar-chart-style spending breakdown directly in the terminal        |
| **Budget Tracking**      | Set per-category budgets and get alerts when nearing or exceeding them |
| **Smart Insights**       | Automated analysis with over-budget warnings and spending highlights |
| **CSV Export**           | Export all data to CSV for use in Excel, Google Sheets, etc.       |
| **Trend Analysis**       | Month-over-month spending trends with directional arrows           |
| **Auto-dated Entries**   | Expenses default to today's date, with optional manual override    |

---

## Project Structure

```
FastTrack/
├── expense_tracker.py      # Main application script
├── expense_tracker.db      # SQLite database (auto-created on first run)
├── readme.md               # This file
└── expenses_export_*.csv   # Exported CSV files (generated via export command)
```

---

