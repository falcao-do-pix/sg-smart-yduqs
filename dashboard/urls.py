from django.urls import path
from .views import login_view_dashboard, dashboard_view, logout_view_dashboard

urlpatterns = [
    path("dashboard/login/", login_view_dashboard, name="login_dashboard"),
    path("dashboard/home/", dashboard_view, name="dashboard"),
    path("dashboard/logout/", logout_view_dashboard, name="logout_dashboard"),
]
