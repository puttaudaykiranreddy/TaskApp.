# Team Task Manager

A premium, modern task management application built with Flask and MySQL. Featuring a sleek glassmorphism design, role-based access control, and dynamic dashboards.

![TaskApp Landing Page](static/hero_illustration.png)

## 🚀 Features

- **Premium Design**: Modern "dark-mode" UI with glassmorphism effects and fluid animations.
- **Role-Based Access Control**:
  - **Admins**: Can create projects, create tasks, and assign them to members. They see global productivity stats.
  - **Members**: Can view assigned tasks and update their status (Pending, In Progress, Completed).
- **Project Management**: Organize tasks into specific projects.
- **Dynamic Dashboards**: Real-time insights into total, completed, pending, and overdue tasks.
- **Secure Authentication**: Password hashing using `bcrypt` and session management.
- **Toast Notifications**: Interactive feedback for all user actions.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (Fetch API)
- **Icons**: FontAwesome 6
- **Fonts**: Outfit, Inter (Google Fonts)
- **Deployment Ready**: Configured for Railway deployment.

## 📦 Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd task-manager
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Create a MySQL database named `task_manager`.
   - Update `db.py` or set environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).

4. **Run the application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000`.

## 🌐 Deployment (Railway)

This app is configured for easy deployment on **Railway**:

1. Push your code to a GitHub repository.
2. Connect your repo to Railway.
3. Provision a MySQL database in your Railway project.
4. Add the database connection details as Environment Variables in your app settings:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `DB_PORT`

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
