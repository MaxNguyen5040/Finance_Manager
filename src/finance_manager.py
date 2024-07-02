# src/finance_manager.py
import csv
import yaml
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    def filter_transactions(self, username, start_date=None, end_date=None, category=None, type=None):
        df = self.transactions.get(username, pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency']))
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]
        if category:
            df = df[df['category'] == category]
        if type:
            df = df[df['type'] == type]
        return df

    def sort_transactions(self, username, by, ascending=True):
        df = self.transactions.get(username, pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency']))
        return df.sort_values(by=by, ascending=ascending)
    
    def plot_expense_trend(self, username):
        df = self.transactions.get(username, pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency']))
        df['date'] = pd.to_datetime(df['date'])
        expense_df = df[df['type'] == 'Expense']
        if expense_df.empty:
            return None

        plt.figure(figsize=(10, 6))
        sns.lineplot(x='date', y='amount', data=expense_df)
        plt.title('Expense Trend')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.tight_layout()
        return plt.gcf()

    def plot_income_trend(self, username):
        df = self.transactions.get(username, pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'currency']))
        df['date'] = pd.to_datetime(df['date'])
        income_df = df[df['type'] == 'Income']
        if income_df.empty:
            return None

        plt.figure(figsize=(10, 6))
        sns.lineplot(x='date', y='amount', data=income_df)
        plt.title('Income Trend')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.tight_layout()
        return plt.gcf()
    
    def export_transactions(self, username, filename='transactions.csv'):
        if username not in self.transactions:
            raise ValueError('User does not exist')
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['date', 'category', 'amount', 'currency', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in self.transactions[username]:
                writer.writerow(transaction)

    def get_spending_by_category(self, username):
        if username not in self.transactions:
            raise ValueError('User does not exist')
        spending_by_category = {}
        for transaction in self.transactions[username]:
            if transaction['type'] == 'Expense':
                category = transaction['category']
                amount = transaction['amount']
                if category in spending_by_category:
                    spending_by_category[category] += amount
                else:
                    spending_by_category[category] = amount
        return spending_by_category