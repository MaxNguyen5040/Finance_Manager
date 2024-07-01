# src/finance_manager.py
import csv
import yaml
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InvalidTransactionTypeError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class InvalidDateError(Exception):
    pass

class FinanceManager:
    def __init__(self, config_file):
        logging.info('Initializing FinanceManager')
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        self.data_file = config['data_file']

    def add_transaction(self, date, category, amount, type):
        logging.info(f'Adding transaction: {date}, {category}, {amount}, {type}')
        if type not in ['Income', 'Expense']:
            raise InvalidTransactionTypeError("Type must be 'Income' or 'Expense'")
        if not isinstance(amount, (int, float)):
            raise InvalidAmountError("Amount must be a number")
        if not isinstance(date, str):
            raise InvalidDateError("Date must be a string in YYYY-MM-DD HH:MM:SS format")
        try:
            datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise InvalidDateError("Date format is incorrect")

        with open(self.data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, type])

    def get_transactions(self):
        transactions = []
        with open(self.data_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                transactions.append(row)
        return transactions

    def generate_report(self, period='monthly'):
        transactions = self.get_transactions()
        report = defaultdict(lambda: {'Income': 0, 'Expense': 0})

        for transaction in transactions:
            date, category, amount, type = transaction
            if period == 'monthly':
                key = date[:7]  # YYYY-MM
            else:
                key = date[:4]  # YYYY

            report[key][type] += float(amount)

        return report

    def generate_detailed_report(self, period='monthly'):
        transactions = self.get_transactions()
        report = defaultdict(lambda: defaultdict(lambda: {'Income': 0, 'Expense': 0}))

        for transaction in transactions:
            date, category, amount, type = transaction
            if period == 'monthly':
                key = date[:7]  # YYYY-MM
            else:
                key = date[:4]  # YYYY

            report[key][category][type] += float(amount)

        return report

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
