const BASE = window.location.origin;

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(BASE + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    })
    .then(r => r.json())
    .then(d => {
        if (d.user_id) {
            localStorage.setItem("role", d.role);
            localStorage.setItem("user_id", d.user_id);
            localStorage.setItem("user_name", d.name || "User");
            window.location.href = "/dashboard-page";
        } else {
            showToast(d.error || "Login failed");
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Error connecting to server");
    });
}

function logout() {
    localStorage.clear();
    window.location.href = "/";
}

/* DASHBOARD */
function loadDashboard() {
    const id = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    fetch(BASE + "/dashboard?user_id=" + id + "&role=" + role)
    .then(r => r.json())
    .then(d => {
        document.getElementById("total").innerText = d.total_tasks;
        document.getElementById("completed").innerText = d.completed;
        document.getElementById("pending").innerText = d.pending;
        document.getElementById("overdue").innerText = d.overdue;
    });
}

/* TASKS */
function createTask() {

     if (!document.getElementById("title").value) {
        showToast("Title is required");
        return;
    }
    const id = localStorage.getItem("user_id");
    const project_id = document.getElementById("projectSelect").value;

    const assigned_to = document.getElementById("assigneeSelect") ? document.getElementById("assigneeSelect").value : id;

    fetch(BASE + "/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            title: document.getElementById("title").value,
            description: document.getElementById("desc").value,
            project_id: project_id,
            assigned_to: assigned_to,
            deadline: document.getElementById("deadline").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            showToast(data.error);   // ✅ show backend error
        } else {
            showToast("Task created successfully");  // ✅ success
            loadTasks();

            // 👇 CLEAR FORM HERE (see next section)
            document.getElementById("title").value = "";
            document.getElementById("desc").value = "";
            document.getElementById("deadline").value = "";
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Something went wrong");  // ✅ HERE
    });
}

function loadTasks() {
    const id = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    fetch(BASE + "/tasks?user_id=" + id + "&role=" + role)
    .then(r => r.json())
    .then(tasks => {

        if (tasks.length === 0) {
            document.getElementById("taskList").innerHTML =
                "<tr><td colspan='7' style='text-align: center'>No tasks found</td></tr>";
            return;
        }

        let html = "";

        tasks.forEach(t => {

            html += `<tr>
                <td>${t.title}</td>
                <td>${t.project_name || '-'}</td>
                <td>${t.assignee_name || 'Unassigned'} (ID: ${t.assigned_to})</td>
                <td>${t.deadline ? new Date(t.deadline).toLocaleDateString() : 'No deadline'}</td>
                <td>
                    <span class="status ${t.status || 'pending'}">
                        ${(t.status || 'pending').replace('_', ' ')}
                    </span>
                </td>
                <td>
                    <select class="status-select" onchange="updateStatus(${t.id}, this.value)">
                        <option value="pending" ${t.status==="pending"?"selected":""}>Pending</option>
                        <option value="in_progress" ${t.status==="in_progress"?"selected":""}>In Progress</option>
                        <option value="completed" ${t.status==="completed"?"selected":""}>Completed</option>
                    </select>
                </td>
                <td>
                    <button class="delete-btn" onclick="deleteTask(${t.id})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            </tr>`;
        });

        document.getElementById("taskList").innerHTML = html;
    });
}

function loadUsers() {
    fetch(BASE + "/users")
    .then(r => r.json())
    .then(users => {
        const select = document.getElementById("assigneeSelect");
        if (!select) return;
        
        if (users.length === 0) {
            select.innerHTML = "<option value=''>No users found</option>";
            return;
        }
        
        let options = "<option value=''>Assign To...</option>";
        users.forEach(u => {
            if (u.role === 'member') {
                options += `<option value="${u.id}">${u.name} (${u.role})</option>`;
            }
        });
        select.innerHTML = options;
    })
    .catch(err => console.error("Error loading users:", err));
}
function signup() {
    fetch(BASE + "/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
            role: document.getElementById("role").value
        })
    })
    .then(r => r.json())
    .then(d => {
        if (d.error) {
            showToast(d.error);
        } else {
            showToast("Signup successful");
            setTimeout(() => {
                window.location.href = "/login-page";
            }, 1000);
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Error connecting to server");
    });
}

function applyRoleUI() {
    const role = localStorage.getItem("role");

    const adminPanel = document.getElementById("adminPanel");

    if (role !== "admin" && adminPanel) {
        adminPanel.style.display = "none";
    }
}
function updateStatus(id, status) {
    fetch(BASE + "/tasks/" + id, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({status})
    }).then(() => loadTasks());
}
function loadProjects() {
    const user_id = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    fetch(BASE + "/projects?user_id=" + user_id + "&role=" + role)
    .then(res => res.json())
    .then(projects => {

        const select = document.getElementById("projectSelect");

        // ✅ ADD THIS BLOCK HERE
        if (projects.length === 0) {
            select.innerHTML = "<option>No projects found</option>";
            return;
        }

        // ✅ NORMAL FLOW
        let options = "";

        projects.forEach(p => {
            options += `<option value="${p.id}">${p.name}</option>`;
        });

        select.innerHTML = options;
    })
    .catch(err => {
        console.error(err);
        showToast("Failed to load projects");
    });
}
function deleteTask(id) {
    fetch(BASE + "/tasks/" + id, {
        method: "DELETE"
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showToast(data.error);
        } else {
            showToast("Task deleted successfully");
            loadTasks();
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Error deleting task");
    });
}
function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

/* PROJECTS PAGE */
function createProject() {
    const name = document.getElementById("projectName").value;
    const user_id = localStorage.getItem("user_id");

    if (!name) {
        showToast("Project name is required");
        return;
    }

    fetch(BASE + "/projects", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name: name, user_id: user_id})
    })
    .then(r => r.json())
    .then(d => {
        if (d.error) {
            showToast(d.error);
        } else {
            showToast("Project created successfully");
            document.getElementById("projectName").value = "";
            loadProjectsTable();
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Error creating project");
    });
}

function loadProjectsTable() {
    const user_id = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    fetch(BASE + "/projects?user_id=" + user_id + "&role=" + role)
    .then(res => res.json())
    .then(projects => {
        const tbody = document.getElementById("projectsListTable");
        if (!tbody) return;

        if (projects.length === 0) {
            tbody.innerHTML = "<tr><td colspan='3' style='text-align: center'>No projects found</td></tr>";
            return;
        }

        let html = "";
        projects.forEach(p => {
            html += `<tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.created_by}</td>
            </tr>`;
        });
        tbody.innerHTML = html;
    })
    .catch(err => console.error(err));
}

/* AUTO LOAD */
(function setupSidebar() {
    const userName = localStorage.getItem("user_name");
    const role = localStorage.getItem("role");
    const sidebarUser = document.getElementById("sidebarUser");
    if (sidebarUser && userName) {
        sidebarUser.innerText = `Welcome, ${userName} (${role})`;
    }
})();

if (window.location.pathname === "/dashboard-page") {
    loadDashboard();
}

if (window.location.pathname === "/projects-page") {
    applyRoleUI();
    loadProjectsTable();
}

if (window.location.pathname === "/tasks-page") {
    applyRoleUI();
    loadProjects();
    loadUsers();
    loadTasks();
}