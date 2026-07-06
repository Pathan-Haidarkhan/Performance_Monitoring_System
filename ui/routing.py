from flask import render_template
from ui import ui_bp


@ui_bp.route("/")
def login_page():
    return render_template("login.html")


@ui_bp.route("/login")
def login():
    return render_template("login.html")


@ui_bp.route("/Admin/dashboard")
def admin_dashboard():
    return render_template("/Admin/dashboard.html")

@ui_bp.route("/Admin/userManagement")
def userlist():
    return render_template("/Admin/userManagement.html")

@ui_bp.route("/Admin/addUser")
def adduser():
    return render_template("/Admin/addUser.html")


@ui_bp.route("/Admin/editUser/<int:userId>")
def editUser(userId):
    return render_template("/Admin/editUser.html", userId = userId)


@ui_bp.route("/Manager/dashboard")
def manager_dashboard():
    return render_template("/Manager/dashboard.html")

@ui_bp.route("/Employee/dashboard")
def employee_dashboard():
    return render_template("/Employee/dashboard.html")