from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import requests
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_key_here' # !! IMPORTANT: Change this to a strong, random key !!

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect unauthenticated users to the login page

# Get the API key from environment variables
API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# Basic check to ensure the API key is set
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable not set. Please set it before running the app.")

# --- User Management (In-memory for demonstration - NOT for production) ---
# In a real application, you'd use a database (e.g., SQLAlchemy with SQLite)
users = {} # {username: {'password_hash': 'hashed_password', 'id': 'user_id', 'name': '', 'email': '', 'phone_number': ''}}
user_id_counter = 0

class User(UserMixin):
    def __init__(self, id, username, password_hash, name, email, phone_number):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    # This loop is inefficient for many users; a database query would be better.
    for user_data in users.values():
        if user_data['id'] == int(user_id):
            return User(user_data['id'], user_data['username'], user_data['password_hash'],
                        user_data['name'], user_data['email'], user_data['phone_number'])
    return None

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        city = request.form['city']
        print(f"Searching for city: {city}")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        print(f"API URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon']
            }
        else:
            weather_data = {'error': 'City not found'}
    return render_template('index.html', weather=weather_data, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_info = users.get(username)
        if user_info and check_password_hash(user_info['password_hash'], password):
            user = User(user_info['id'], username, user_info['password_hash'],
                        user_info['name'], user_info['email'], user_info['phone_number'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global user_id_counter
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        if username in users:
            flash('Username already exists. Please choose a different one.', 'warning')
        elif email in [u['email'] for u in users.values() if 'email' in u]: # Check if email already exists
            flash('Email already registered. Please use a different one or log in.', 'warning')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            user_id_counter += 1
            users[username] = {
                'id': user_id_counter,
                'username': username,
                'password_hash': hashed_password,
                'name': name,
                'email': email,
                'phone_number': phone_number
            }
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required # Requires user to be logged in to access this route
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Example of a protected route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user)


if __name__ == '__main__':
    # You would typically set OPENWEATHER_API_KEY in your environment before running
    # For local testing, you might temporarily set it here (uncomment and replace with your key):
    # os.environ['OPENWEATHER_API_KEY'] = 'YOUR_OPENWEATHER_API_KEY'
    app.run(debug=True)