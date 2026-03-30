from flask import Blueprint

ui_bp = Blueprint(
    "ui",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

from . import routing, dashboard_ui, task_ui, report_ui