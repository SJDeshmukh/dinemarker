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
    phone = data.get('phone')
    canteen_name = data.get('canteen_name')
    canteen_location = data.get('canteen_location')

    if not all([name, surname, email, password]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if existing_user:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    conn.execute(
        '''INSERT INTO users 
        (name, surname, email, phone, canteen_name, canteen_location, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (name, surname, email, phone, canteen_name, canteen_location, password)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True})
@app.route('/log-scan', methods=['POST'])
def log_scan():
    data = request.get_json()
    print("Received QR data:", data)
    qr_data = data.get('qr_data')


    if not qr_data:
        return jsonify({'success': False, 'message': 'No QR data provided'}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO scans (qr_data, timestamp) VALUES (?, CURRENT_TIMESTAMP)',
            (qr_data,)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print("Scan logging error:", e)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
@app.route('/get-employee', methods=['POST'])
def get_employee():
    data = request.get_json()
    emp_id = data.get('employee_id')

    if not emp_id:
        return jsonify({'success': False, 'message': 'No Employee ID provided'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (emp_id,)).fetchone()
    conn.close()

    if user:
        return jsonify({
            'success': True,
            'data': {
                'name': user['name'],
                'surname': user['surname'],
                'email': user['email'],
                'phone': user['phone'],
                'canteen_name': user['canteen_name'],
                'canteen_location': user['canteen_location']
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


# @app.route('/home')
# def home():
#     return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
