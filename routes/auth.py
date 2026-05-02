from flask import Blueprint, request, jsonify
from db import get_db
import bcrypt

auth_bp = Blueprint('auth', __name__)

# ---------------- SIGNUP ----------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    role = data.get("role", "member")

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_pw, role))
        conn.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        error_msg = str(e)
        if "1062" in error_msg:
            return jsonify({"error": "An account with this email already exists. Please log in!"}), 400
        return jsonify({"error": "An error occurred while creating your account."}), 500

    finally:
        cursor.close()
        conn.close()


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({
                "message": "Login successful",
                "user_id": user["id"],
                "role": user["role"],
                "name": user["name"]
            })
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

# ---------------- GET USERS ----------------
@auth_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)