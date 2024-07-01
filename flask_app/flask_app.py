from flask import Flask, render_template, request, redirect, url_for, flash
from src.finance_manager import FinanceManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
manager = FinanceManager('config.yaml')

@app.route('/')
def index():
    transactions = manager.get_transactions()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    category = request.form['category']
    amount = float(request.form['amount'])
    type = request.form['type']
    currency = request.form['currency']
    try:
        manager.add_transaction(date, category, amount, type, currency)
        flash('Transaction added successfully!')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
