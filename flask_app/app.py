from user_manager import UserManager
from functools import wraps
from flask import session
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

user_manager = UserManager('data/users.csv')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate_user(username, password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    username = session['username']
    manager.load_user_transactions(username)
    if request.method == 'POST':
        filter_criteria = {
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'category': request.form.get('category'),
            'type': request.form.get('type')
        }
        transactions = manager.filter_transactions(username, **filter_criteria)
    else:
        transactions = manager.get_transactions(username)
    return render_template('index.html', transactions=transactions.to_dict(orient='records'))

@app.route('/sort', methods=['POST'])
@login_required
def sort_transactions():
    username = session['username']
    by = request.form['sort_by']
    ascending = request.form.get('ascending', 'true').lower() == 'true'
    transactions = manager.sort_transactions(username, by, ascending)
    return render_template('index.html', transactions=transactions.to_dict(orient='records'))

@app.route('/plot/expense-trend')
@login_required
def plot_expense_trend():
    username = session['username']
    fig = manager.plot_expense_trend(username)
    if fig:
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return base64.b64encode(output.getvalue()).decode('utf8')
    else:
        flash('No expense data to plot.')
        return redirect(url_for('index'))

@app.route('/plot/income-trend')
@login_required
def plot_income_trend():
    username = session['username']
    fig = manager.plot_income_trend(username)
    if fig:
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return base64.b64encode(output.getvalue()).decode('utf8')
    else:
        flash('No income data to plot.')
        return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    username = session['username']
    settings = user_manager.get_user_settings(username)
    return render_template('profile.html', settings=settings)

@app.route('/update-settings', methods=['POST'])
@login_required
def update_settings():
    username = session['username']
    settings = {
        'preferred_currency': request.form['preferred_currency']
    }
    user_manager.update_user_settings(username, settings)
    flash('Settings updated successfully!')
    return redirect(url_for('profile'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user_manager.add_user(username, password)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e))
    return render_template('register.html')