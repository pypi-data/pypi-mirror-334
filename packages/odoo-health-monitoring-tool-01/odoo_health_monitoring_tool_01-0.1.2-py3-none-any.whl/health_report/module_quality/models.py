from django.db import models
from login_app.methods import xmlrpc_connection

# Create your models here.

class ModuleQuality(models.Model):


    def modules_installed(self):
        installed_modules = xmlrpc_connection(model_name="module.quality",function_name="modules_installed")
        return installed_modules
    
    def count_lines_of_code_in_modules(self):
        count_of_code = xmlrpc_connection(model_name="module.quality",function_name="count_lines_of_code_in_modules")
        return count_of_code
    
    def get_module_naming(self):
        module_naming = xmlrpc_connection(model_name='module.quality',function_name='module_naming_conventions')
        return module_naming
    
    def count_of_non_stored_fields(self):
        count_of_non_stored_fields = xmlrpc_connection(model_name='module.quality',function_name='count_of_non_stored_fields')
        return count_of_non_stored_fields
    
    def module_load_time(self):
        module_load_time = xmlrpc_connection(model_name='module.quality',function_name='module_load_time')
        return module_load_time
    
    def pep_module_filter(self):
        pep_module_filter = xmlrpc_connection(model_name='module.quality',function_name='pep_module_filter')
        return pep_module_filter
    
    def pep_standard_template(self):
        pep_standard_template = xmlrpc_connection(model_name='module.quality',function_name='pep_standard_template')
        return pep_standard_template
    
    def function_counts(self):
        function_counts = xmlrpc_connection(model_name='module.quality',function_name='function_counts')
        return function_counts
    
    def function_counts(self):
        function_counts = xmlrpc_connection(model_name='module.quality',function_name='function_counts')
        return function_counts