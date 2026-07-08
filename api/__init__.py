from .auth_routes import auth_routes
from .user_routes import user_routes
from .task_routes import task_routes
from .dashboard_routes import dashboard_routes
from .department_routes import department_routes
from .performance_routes import metric_routes

__all__ = ['auth_routes', 'user_routes','task_routes', 'dashboard_routes', 'department_routes', 'metric_routes']