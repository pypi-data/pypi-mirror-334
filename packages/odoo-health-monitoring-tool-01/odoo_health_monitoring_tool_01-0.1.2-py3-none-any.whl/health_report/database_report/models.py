# -*- coding: utf-8 -*-
from datetime import timedelta
import os
from pprint import pprint
import psutil
from django.db import connections,models
import math
from django.utils.timezone import now
# import pytz
import xmlrpc.client
from login_app.methods import xmlrpc_connection
from login_app.models import OdooSetup


DB_SETTING_NAME = 'postgresql'
ODOO_DATA_DIR = "/var/lib/odoo/filestore/"


class DatabaseMetrics(models.Model):
    """Class representing the database metrics"""
    _name = 'database.metrics'
    _description = 'Database Metrics'

    def collect_database_metrics(self):
        """Collect database performance metrics"""
        database_metrics =xmlrpc_connection("database.metrics", "collect_metrics")
        return database_metrics

    def odoo_file_health(self):
        """Fetch Odoo's file health from PostgreSQL"""

        odoo_file_health = xmlrpc_connection(model_name="database.metrics",function_name="odoo_file_health")
        return odoo_file_health
        # tz = pytz.utc  # Ensure timezone consistency
        # current_time = now().astimezone(tz)
        # # attachments = cursor.fetchall()
        # odoo_setup = OdooSetup.objects.filter().first()
        # url = odoo_setup.url
        # database=odoo_setup.database_name
        # user = odoo_setup.username
        # password = odoo_setup.api_token
        # # Authenticate using the common endpoint
        # common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')

        # uid = common.authenticate(database, user, password, {})
        # if uid:
        #     # Now connect to the object endpoint
        #     model = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        #     attachments = model.execute_kw(database, uid, password, 'ir.attachment', 'search_read', 
        #                                [[]], {'fields': ['id', 'store_fname','datas', 'create_date','write_date', 'file_size', 'mimetype']})

        #     # uploaded files in last 30 days
        #     thirty_days_ago = (current_time - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        #     uploaded_files_list = [att for att in attachments if att['create_date'] and att['create_date'] >= thirty_days_ago]
        #     uploaded_files = len(uploaded_files_list)

        #     # Calculate average file size (in MB)

        #     total_size = sum([len(file['datas']) for file in uploaded_files_list]) / uploaded_files
        #     avg_size_tb = total_size / (1024*1024*1024*1024)
        #     exponent = math.floor(math.log10(avg_size_tb)) if avg_size_tb > 0 else 0
        #     coefficient = avg_size_tb / (10 ** exponent)  # Get coefficient
        #     average_size = f"{coefficient:.3f} × 10^{exponent}"

        #     # Missing files (files without a store_fname updated in the last 30 days)
        #     missing_files = len([att for att in uploaded_files_list if not att.get('store_fname')])

        #     # File types
        #     file_types = {}
        #     for att in uploaded_files_list:
        #         mimetype = att.get('mimetype', 'unknown')
        #         file_types[mimetype] = file_types.get(mimetype, 0) + 1

        #     # File size distribution
        #     size_distribution = {}
        #     for att in uploaded_files_list:
        #         size_mb = (att.get('file_size', 0))
        #         if size_mb < 10 * 1024:
        #             size_distribution['Small (<10KB)'] = size_distribution.get('Small (<10KB)', 0) + 1
        #         elif size_mb < 100 * 1024:
        #             size_distribution['Medium (10KB-100KB)'] = size_distribution.get('Medium (10KB-100KB)', 0) + 1
        #         elif size_mb < 500 * 1024:
        #             size_distribution['Large (100KB-500KB)'] = size_distribution.get('Large (100KB-500KB)', 0) + 1
        #         else:
        #             size_distribution['Very Large (>500KB)'] = size_distribution.get('Very Large (>500KB)', 0) + 1

        #     # safe upload limit 
        #     free_disk_space = psutil.disk_usage('/').free
        #     free_disk_space_mb = free_disk_space / (1024 * 1024)
        #     available_memory = psutil.virtual_memory().available
        #     available_memory_mb = available_memory / (1024 * 1024)
        #     cpu_usage = psutil.cpu_percent(interval=1)
        #     disk_limit_mb = free_disk_space_mb * 0.1
        #     memory_limit_mb = available_memory_mb * 0.2

        #     if cpu_usage > 80:
        #         cpu_limit_mb = 5  # Limit to 5MB if CPU usage is high
        #     else:
        #         cpu_limit_mb = 100  # 100MB if CPU usage is low

        #     safe_upload_limit = min(disk_limit_mb, memory_limit_mb, cpu_limit_mb)

        #     # Total file size in MB
        #     total_size_mb = sum([len(file['datas']) for file in uploaded_files_list]) / (1024 ** 2)

        #     return {
        #         'uploaded_files': uploaded_files,
        #         'average_size': average_size,
        #         'missing_files': missing_files,
        #         'file_types': file_types,
        #         'file_distribution': size_distribution,
        #         'safe_upload_limit': safe_upload_limit,
        #         'total_size_mb': round(total_size_mb, 2)
        #     }
        # else:
        #     print('Connection failed')
        
    def get_concurrent_session_count(self):
        """Fetch Concurrent sesssions"""
        session_count = xmlrpc_connection(model_name="database.metrics",function_name="get_concurrent_session_count")
        return session_count 