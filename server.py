import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

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
    employee_id = data.get('employee_id')  # ✅ New field

    if not all([name, surname, email, password, employee_id]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ? OR employee_id = ?', (email, employee_id)).fetchone()

    if existing_user:
        conn.close()
        return jsonify({'success': False, 'message': 'Email or Employee ID already exists'}), 400

    conn.execute(
        '''INSERT INTO users 
        (name, surname, email, phone, canteen_name, canteen_location, password, employee_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (name, surname, email, phone, canteen_name, canteen_location, password, employee_id)
    )
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/log-scan', methods=['POST'])
def log_scan():
    data = request.get_json()
    qr_data = data.get('qr_data')

    if not qr_data:
        return jsonify({'success': False, 'message': 'No QR data provided'}), 400

    employee_id = qr_data.strip()

    try:
        conn = get_db_connection()

        # 🔍 Check if employee exists
        employee = conn.execute(
            'SELECT * FROM users WHERE employee_id = ?',
            (employee_id,)
        ).fetchone()

        if not employee:
            conn.close()
            return jsonify({'success': False, 'message': 'Employee not registered'}), 404

        # ✅ Employee exists, log the scan
        conn.execute(
            'INSERT INTO scans (employee_id, timestamp, raw_data) VALUES (?, CURRENT_TIMESTAMP, ?)',
            (employee_id, qr_data)
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
    user = conn.execute(
        'SELECT * FROM users WHERE employee_id = ?', (emp_id,)
    ).fetchone()
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

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    if request.method == 'POST':
        data = request.get_json()
        employee_id = data.get('employee_id')

        if not employee_id:
            return jsonify({'success': False, 'message': 'No employee ID provided'}), 400

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE employee_id = ?', (employee_id,)).fetchone()

        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Employee not found'}), 404

        scans = conn.execute(
            'SELECT timestamp FROM scans WHERE employee_id = ? ORDER BY timestamp DESC',
            (employee_id,)
        ).fetchall()
        conn.close()

        return jsonify({
            'success': True,
            'employee': dict(user),
            'scans': [row['timestamp'] for row in scans]
        })

    return render_template('statistics.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

if __name__ == '__main__':
    app.run(debug=True)
