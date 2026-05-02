from flask import Flask, render_template
from routes.auth import auth_bp
from routes.project import project_bp
from routes.task import task_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/tasks-page")
def tasks_page():
    return render_template("tasks.html")

@app.route("/projects-page")
def projects_page():
    return render_template("projects.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")
if __name__ == "__main__":
    app.run(debug=True)