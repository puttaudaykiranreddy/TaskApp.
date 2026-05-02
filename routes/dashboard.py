from flask import Blueprint, request, jsonify
from db import get_db
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = request.args.get("user_id")
    role = request.args.get("role", "member")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        if role == "admin":
            # Total tasks
            cursor.execute("SELECT COUNT(*) as total FROM tasks")
            total = cursor.fetchone()["total"]

            # Completed
            cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE status='completed'")
            completed = cursor.fetchone()["completed"]

            # Pending
            cursor.execute("SELECT COUNT(*) as pending FROM tasks WHERE status='pending'")
            pending = cursor.fetchone()["pending"]

            # Overdue
            cursor.execute("""
                SELECT COUNT(*) as overdue FROM tasks 
                WHERE deadline < %s AND status != 'completed'
            """, (date.today(),))
            overdue = cursor.fetchone()["overdue"]
        else:
            # Total tasks
            cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE assigned_to=%s", (user_id,))
            total = cursor.fetchone()["total"]

            # Completed
            cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE assigned_to=%s AND status='completed'", (user_id,))
            completed = cursor.fetchone()["completed"]

            # Pending
            cursor.execute("SELECT COUNT(*) as pending FROM tasks WHERE assigned_to=%s AND status='pending'", (user_id,))
            pending = cursor.fetchone()["pending"]

            # Overdue
            cursor.execute("""
                SELECT COUNT(*) as overdue FROM tasks 
                WHERE assigned_to=%s AND deadline < %s AND status != 'completed'
            """, (user_id, date.today()))
            overdue = cursor.fetchone()["overdue"]

        return jsonify({
            "total_tasks": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue
        })

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()