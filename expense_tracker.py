import argparse
import sqlite3
import datetime
import csv
import sys
import os

DB_FILE = "expense_tracker.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                amount REAL NOT NULL
            )
        ''')
        conn.commit()

def add_expense(args):
    date = args.date or datetime.date.today().isoformat()
    with get_db() as conn:
        conn.execute('INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)',
                     (args.amount, args.category.lower(), args.description, date))
        conn.commit()
    print(f"Added expense: ${args.amount:.2f} in '{args.category}' on {date}")

def list_expenses(args):
    query = 'SELECT * FROM expenses WHERE 1=1'
    params = []
    if args.category:
        query += ' AND category = ?'
        params.append(args.category.lower())
    if args.start_date:
        query += ' AND date >= ?'
        params.append(args.start_date)
    if args.end_date:
        query += ' AND date <= ?'
        params.append(args.end_date)
    query += ' ORDER BY date DESC'
    
    with get_db() as conn:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        
    if not rows:
        print("No expenses found.")
        return
        
    print(f"{'ID':<5} | {'Date':<10} | {'Category':<15} | {'Amount':<10} | {'Description'}")
    print("-" * 70)
    for row in rows:
        print(f"{row['id']:<5} | {row['date']:<10} | {row['category']:<15} | ${row['amount']:<9.2f} | {row['description']}")

def summary(args):
    month = args.month or datetime.date.today().strftime('%Y-%m')
    query = 'SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? GROUP BY category'
    
    with get_db() as conn:
        cursor = conn.execute(query, (f'{month}%',))
        rows = cursor.fetchall()
        
    if not rows:
        print(f"No expenses found for {month}.")
        return
        
    max_amount = max(row['total'] for row in rows)
    print(f"Spending Summary for {month}")
    print("-" * 60)
    for row in rows:
        bar_length = int((row['total'] / max_amount) * 30) if max_amount > 0 else 0
        bar = '█' * bar_length
        print(f"{row['category']:<15} | ${row['total']:<8.2f} | {bar}")

def manage_budget(args):
    if args.action == 'set':
        with get_db() as conn:
            conn.execute('INSERT OR REPLACE INTO budgets (category, amount) VALUES (?, ?)',
                         (args.category.lower(), args.amount))
            conn.commit()
        print(f"Set budget for '{args.category}' to ${args.amount:.2f}")
    elif args.action == 'view':
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM budgets')
            rows = cursor.fetchall()
            if not rows:
                print("No budgets set.")
                return
            print(f"{'Category':<15} | {'Budget Amount':<15}")
            print("-" * 35)
            for row in rows:
                print(f"{row['category']:<15} | ${row['amount']:<14.2f}")

def insights(args):
    month = datetime.date.today().strftime('%Y-%m')
    with get_db() as conn:
        expenses_cursor = conn.execute('SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? GROUP BY category', (f'{month}%',))
        expenses = {row['category']: row['total'] for row in expenses_cursor.fetchall()}
        
        budgets_cursor = conn.execute('SELECT * FROM budgets')
        budgets = {row['category']: row['amount'] for row in budgets_cursor.fetchall()}
        
    if not expenses:
        print("Not enough data for insights this month.")
        return
        
    total_spent = sum(expenses.values())
    highest_category = max(expenses, key=expenses.get)
    
    print("💡 Smart Spending Insights 💡")
    print("-" * 40)
    print(f"Total spent this month: ${total_spent:.2f}")
    print(f"Highest spending category: {highest_category} (${expenses[highest_category]:.2f})")
    
    print("\nBudget Alerts:")
    alerts = 0
    for cat, spent in expenses.items():
        if cat in budgets:
            budget = budgets[cat]
            if spent > budget:
                print(f"  🚨 Over budget in {cat}: Spent ${spent:.2f} / Budget ${budget:.2f}")
                alerts += 1
            elif spent > budget * 0.8:
                print(f"  ⚠️  Nearing budget in {cat}: Spent ${spent:.2f} / Budget ${budget:.2f}")
                alerts += 1
    if alerts == 0:
        print("  ✅ All categories within budget!")

def delete_expense(args):
    with get_db() as conn:
        cursor = conn.execute('DELETE FROM expenses WHERE id = ?', (args.id,))
        if cursor.rowcount > 0:
            print(f"Deleted expense ID {args.id}")
            conn.commit()
        else:
            print(f"Expense ID {args.id} not found.")

def export_csv(args):
    filename = args.file or f"expenses_export_{datetime.date.today().isoformat()}.csv"
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM expenses ORDER BY date DESC')
        rows = cursor.fetchall()
        
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Amount', 'Category', 'Description', 'Date'])
        for row in rows:
            writer.writerow([row['id'], row['amount'], row['category'], row['description'], row['date']])
            
    print(f"Exported {len(rows)} expenses to {filename}")

def trends(args):
    query = "SELECT substr(date, 1, 7) as month, SUM(amount) as total FROM expenses GROUP BY month ORDER BY month"
    with get_db() as conn:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        
    if not rows:
        print("No data available for trends.")
        return
        
    print("Month-over-Month Trends")
    print("-" * 40)
    prev_total = None
    for row in rows:
        month = row['month']
        total = row['total']
        trend = ""
        if prev_total is not None:
            diff = total - prev_total
            if diff > 0:
                trend = f" (↗ +${diff:.2f})"
            elif diff < 0:
                trend = f" (↘ -${abs(diff):.2f})"
            else:
                trend = " (→ $0.00)"
        print(f"{month} | ${total:<8.2f}{trend}")
        prev_total = total

def main():
    init_db()
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add
    parser_add = subparsers.add_parser("add", help="Add a new expense")
    parser_add.add_argument("amount", type=float, help="Expense amount")
    parser_add.add_argument("category", type=str, help="Category (e.g., food, transport)")
    parser_add.add_argument("description", type=str, help="Description of the expense")
    parser_add.add_argument("--date", type=str, help="Date in YYYY-MM-DD format (default: today)")
    parser_add.set_defaults(func=add_expense)
    
    # List
    parser_list = subparsers.add_parser("list", help="List expenses")
    parser_list.add_argument("--category", type=str, help="Filter by category")
    parser_list.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser_list.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser_list.set_defaults(func=list_expenses)
    
    # Summary
    parser_summary = subparsers.add_parser("summary", help="Spending summary with visual bars")
    parser_summary.add_argument("--month", type=str, help="Month in YYYY-MM format (default: current month)")
    parser_summary.set_defaults(func=summary)
    
    # Budget
    parser_budget = subparsers.add_parser("budget", help="Manage budgets")
    budget_subparsers = parser_budget.add_subparsers(dest="action", required=True)
    
    budget_set = budget_subparsers.add_parser("set", help="Set budget for a category")
    budget_set.add_argument("category", type=str, help="Category name")
    budget_set.add_argument("amount", type=float, help="Budget amount")
    
    budget_view = budget_subparsers.add_parser("view", help="View all budgets")
    parser_budget.set_defaults(func=manage_budget)
    
    # Insights
    parser_insights = subparsers.add_parser("insights", help="Smart spending insights")
    parser_insights.set_defaults(func=insights)
    
    # Delete
    parser_delete = subparsers.add_parser("delete", help="Delete an expense")
    parser_delete.add_argument("id", type=int, help="Expense ID to delete")
    parser_delete.set_defaults(func=delete_expense)
    
    # Export
    parser_export = subparsers.add_parser("export", help="Export expenses to CSV")
    parser_export.add_argument("--file", type=str, help="Output filename")
    parser_export.set_defaults(func=export_csv)
    
    # Trends
    parser_trends = subparsers.add_parser("trends", help="Month-over-month spending trends")
    parser_trends.set_defaults(func=trends)
    
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
