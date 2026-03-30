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

@ui_bp.route("/Admin/userlist")
def userlist():
    return render_template("/Admin/userlist.html")

@ui_bp.route("/Manager/dashboard")
def manager_dashboard():
    return render_template("/Manager/dashboard.html")

@ui_bp.route("/Employee/dashboard")
def employee_dashboard():
    return render_template("/Employee/dashboard.html")