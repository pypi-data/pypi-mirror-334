from django.urls import path
# from database_report import views
from database_report  import views

urlpatterns = [
    path("database-data/",views.database_data,name="database-data"),
    path("get-odoo-file-health/",views.get_odoo_file_health,name="get-odoo-file-health"),
    path("get-session-count/",views.get_concurrent_session_count,name="get-session-count"),


]
