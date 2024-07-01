from finance_manager import FinanceManager
from datetime import datetime

manager = FinanceManager('config.yaml')

# Import transactions from another CSV file
manager.import_transactions('data/import_transactions.csv')

# Print all transactions
transactions = manager.get_transactions()
for transaction in transactions:
    print(transaction)

# # Generate monthly report
# monthly_report = manager.generate_report('monthly')
# for period, data in monthly_report.items():
#     print(f"{period}: Income = {data['Income']}, Expense = {data['Expense']}")

# # Generate annual report
# annual_report = manager.generate_report('annual')
# for period, data in annual_report.items():
#     print(f"{period}: Income = {data['Income']}, Expense = {data['Expense']}")

# manager.plot_report(monthly_report, 'monthly')

# detailed_monthly_report = manager.generate_detailed_report('monthly')
# for period, categories in detailed_monthly_report.items():
#     print(f"{period}:")
#     for category, data in categories.items():
#         print(f"  {category}: Income = {data['Income']}, Expense = {data['Expense']}")


try:
    # Add valid transaction
    manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Salary', 5000, 'Income')
    # Add invalid transaction
    manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Groceries', 'invalid_amount', 'Expense')
except ValueError as e:
    print(f"Error: {e}")

# Print all transactions
transactions = manager.get_transactions()
for transaction in transactions:
    print(transaction)