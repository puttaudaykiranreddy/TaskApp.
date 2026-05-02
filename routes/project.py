from flask import Blueprint, request, jsonify
from db import get_db

project_bp = Blueprint('project', __name__)

# ---------------- CREATE PROJECT ----------------
@project_bp.route("/projects", methods=["POST"])
def create_project():
    data = request.json

    name = data.get("name")
    created_by = data.get("user_id")

    if not name or not created_by:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Insert project
        cursor.execute(
            "INSERT INTO projects (name, created_by) VALUES (%s, %s)",
            (name, created_by)
        )
        project_id = cursor.lastrowid

        # Add creator as admin in project_members
        cursor.execute(
            "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)",
            (project_id, created_by, "admin")
        )

        conn.commit()

        return jsonify({"message": "Project created", "project_id": project_id})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()


# ---------------- GET PROJECTS ----------------
@project_bp.route("/projects", methods=["GET"])
def get_projects():
    user_id = request.args.get("user_id")
    role = request.args.get("role", "member")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if role == "admin":
        cursor.execute("SELECT * FROM projects")
    else:
        query = """
        SELECT p.* FROM projects p
        JOIN project_members pm ON p.id = pm.project_id
        WHERE pm.user_id = %s
        """
        cursor.execute(query, (user_id,))
        
    projects = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(projects)


# ---------------- ADD MEMBER ----------------
@project_bp.route("/projects/<int:project_id>/add-member", methods=["POST"])
def add_member(project_id):
    data = request.json

    user_id = data.get("user_id")   # person to add
    added_by = data.get("added_by") # who is adding

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Check if added_by is admin
    cursor.execute(
        "SELECT role FROM project_members WHERE project_id=%s AND user_id=%s",
        (project_id, added_by)
    )
    result = cursor.fetchone()

    if not result or result["role"] != "admin":
        return jsonify({"error": "Only admin can add members"}), 403

    try:
        cursor.execute(
            "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)",
            (project_id, user_id, "member")
        )
        conn.commit()

        return jsonify({"message": "Member added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()