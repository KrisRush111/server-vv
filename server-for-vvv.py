from flask import Flask, request, jsonify
import pymysql
import hashlib

app = Flask(__name__)

# Подключение к MySQL (InfinityFree)
conn = pymysql.connect(
    host='sql110.infinityfree.com',
    port=3306,
    user='epiz_12345678',
    password='ТВОЙ_ПАРОЛЬ',
    database='if0_39352956_vuntdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nickname = data.get('nickname')
    email = data.get('email')
    password = data.get('password')
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    identity = data.get('identity')
    class_number = data.get('class_number')
    class_letter = data.get('class_letter')
    course = data.get('course')
    direction = data.get('direction')
    main_school = data.get('main_school_name')
    extra_school = data.get('extra_school_name')

    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO users (nickname, email, password_hash, identity, class_number, class_letter, course, direction, main_school_name, extra_school_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nickname, email, password_hash, identity, class_number, class_letter, course, direction, main_school, extra_school))
            conn.commit()
        return jsonify({'status': 'ok'}), 201
    except pymysql.err.IntegrityError:
        return jsonify({'status': 'email_exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, password_hash))
        user = cur.fetchone()
        if user:
            return jsonify({'status': 'ok', 'user': user}), 200
        else:
            return jsonify({'status': 'invalid'}), 401

if __name__ == '__main__':
    app.run()
