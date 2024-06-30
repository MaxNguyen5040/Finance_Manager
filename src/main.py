# src/main.py
from finance_manager import FinanceManager
from datetime import datetime

manager = FinanceManager('data/transactions.csv')

# Add example transactions
manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Salary', 5000, 'Income')
manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Groceries', -150, 'Expense')
manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Rent', -1000, 'Expense')

# Print all transactions
transactions = manager.get_transactions()
for transaction in transactions:
    print(transaction)

