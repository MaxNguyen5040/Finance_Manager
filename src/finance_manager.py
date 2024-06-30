import csv
from datetime import datetime

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
