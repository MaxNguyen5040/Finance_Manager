import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


class FinanceManager:
    def __init__(self, data_file):
        self.data_file = data_file

    def add_transaction(self, date, category, amount, type):
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