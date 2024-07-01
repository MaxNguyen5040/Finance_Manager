import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import yaml


class FinanceManager:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        self.data_file = config['data_file']

    def add_transaction(self, date, category, amount, type):
        with open(self.data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, type])

    def import_transactions(self, import_file):
        with open(import_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                date, category, amount, type = row
                self.add_transaction(date, category, float(amount), type)

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
    
    def add_transaction(self, date, category, amount, type):
        if type not in ['Income', 'Expense']:
            raise ValueError("Type must be 'Income' or 'Expense'")
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")
        if not isinstance(date, str):
            raise ValueError("Date must be a string in YYYY-MM-DD HH:MM:SS format")
        try:
            datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Date format is incorrect")

        with open(self.data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, type])