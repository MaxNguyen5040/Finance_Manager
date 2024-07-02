# src/finance_manager.py
import csv
import yaml
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import pandas as pd


class InvalidTransactionTypeError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class InvalidDateError(Exception):
    pass

class FinanceManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.transactions = {}
    
    def load_user_transactions(self, username):
        try:
            self.transactions[username] = pd.read_csv(f'data/{username}_transactions.csv')
        except FileNotFoundError:
            self.transactions[username] = pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency'])

    def save_user_transactions(self, username):
        self.transactions[username].to_csv(f'data/{username}_transactions.csv', index=False)

    def add_transaction(self, username, date, category, amount, type, currency):
        new_transaction = pd.DataFrame([[date, category, amount, type, currency]], columns=['date', 'category', 'amount', 'type', 'currency'])
        self.transactions[username] = pd.concat([self.transactions[username], new_transaction], ignore_index=True)
        self.save_user_transactions(username)
    
    def get_transactions(self, username):
        return self.transactions.get(username, pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency']))

    def plot_report(self, report, period='monthly'):
        periods = sorted(report.keys())
        incomes = [report[period]['Income'] for period in periods]
        expenses = [report[period]['Expense'] for period in periods]

        plt.figure(figsize=(10, 5))
        plt.plot(periods, incomes, label='Income')
        plt.plot(periods, expenses, label='Expense')
        plt.xlabel('Period')
        plt.ylabel('Amount')
        plt.title(f'{period.capitalize()} Report')
        plt.legend()
        plt.show()

    def import_transactions(self, import_file):
        with open(import_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                date, category, amount, type = row
                self.add_transaction(date, category, float(amount), type)

    def plot_expense_categories(self, period='monthly'):
        transactions = self.get_transactions()
        categories = defaultdict(float)

        for transaction in transactions:
            date, category, amount, type = transaction
            if type == 'Expense':
                if period == 'monthly' and date.startswith(period):
                    categories[category] += float(amount)
                elif period == 'annual' and date.startswith(period):
                    categories[category] += float(amount)

        plt.figure(figsize=(10, 5))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title('Expense Categories')
        plt.show()
