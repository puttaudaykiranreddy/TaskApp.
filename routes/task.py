from flask import Blueprint, request, jsonify
from db import get_db

task_bp = Blueprint('task', __name__)

# ---------------- CREATE TASK ----------------
@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    title = data.get("title")
    description = data.get("description")
    project_id = data.get("project_id")
    assigned_to = data.get("assigned_to")
    deadline = data.get("deadline")

    if not title or not project_id or not assigned_to:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO tasks (title, description, project_id, assigned_to, deadline)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, project_id, assigned_to, deadline))

        conn.commit()
        return jsonify({"message": "Task created successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()


# ---------------- GET TASKS ----------------
@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = request.args.get("user_id")
    role = request.args.get("role", "member")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if role == "admin":
        cursor.execute("""
            SELECT t.*, u.name as assignee_name, p.name as project_name 
            FROM tasks t
            LEFT JOIN users u ON t.assigned_to = u.id
            LEFT JOIN projects p ON t.project_id = p.id
        """)
    else:
        cursor.execute("""
            SELECT t.*, u.name as assignee_name, p.name as project_name 
            FROM tasks t
            LEFT JOIN users u ON t.assigned_to = u.id
            LEFT JOIN projects p ON t.project_id = p.id
            WHERE t.assigned_to = %s
        """, (user_id,))

    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks)


# ---------------- UPDATE TASK ----------------
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    status = data.get("status")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE tasks SET status=%s WHERE id=%s
        """, (status, task_id))

        conn.commit()
        return jsonify({"message": "Task updated"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()


# ---------------- DELETE TASK ----------------
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()

        return jsonify({"message": "Task deleted"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()