import os
import pytest
from src.finance_manager import FinanceManager
from datetime import datetime

@pytest.fixture
def manager():
    return FinanceManager('data/test_transactions.csv')

def test_add_transaction(manager):
    manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Salary', 5000, 'Income')
    transactions = manager.get_transactions()
    assert len(transactions) == 1
    assert transactions[0][1] == 'Salary'
    assert float(transactions[0][2]) == 5000

def test_invalid_transaction(manager):
    with pytest.raises(ValueError):
        manager.add_transaction(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Groceries', 'invalid_amount', 'Expense')