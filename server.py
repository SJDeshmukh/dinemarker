import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Path to your SQLite database
DB_PATH = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route('/dashboard')
def dashboard():
    return render_template('home.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')

    if not all([name, surname, email, password]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if existing_user:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    conn.execute(
        'INSERT INTO users (name, surname, email, password) VALUES (?, ?, ?, ?)',
        (name, surname, email, password)
    )
    conn.commit()
    conn.close()
    print("Data inserted in database")
    return jsonify({'success': True})
@app.route('/camera')
def camera():
    return render_template('camera.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
