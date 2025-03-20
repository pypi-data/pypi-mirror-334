from django.urls import path
from module_quality import views

urlpatterns = [
    path('get-modules-installed/',views.get_modules_installed,name="get-modules-installed"),
    path('get-count-of-code/',views.get_count_of_code,name="get-count-of-code"),
    path('get-module-naming/',views.get_module_naming,name="get-module-naming"),
    path('get-non-stored-fields/',views.get_count_of_non_stored_fields,name="get-non-stored-fields"),
    path('get-module-load-time/',views.get_module_load_time,name="get-module-load-time"),
    path('get-pep-module-filter/',views.get_pep_module_filter,name="get-pep-module-filter"),
    path('get-pep-standard-template/',views.get_pep_standard_template,name="get-pep-standard-template"),
    path('get-function-counts/',views.get_function_counts,name="get-function-counts"),
]
