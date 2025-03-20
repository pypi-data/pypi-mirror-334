from django.urls import path
from login_app import views

urlpatterns = [
    path('odoo-setup',views.odoo_setup_view,name='odoo-setup')
]
