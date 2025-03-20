from rest_framework.decorators import api_view
from rest_framework.response import Response
from module_quality.models import ModuleQuality

# Create your views here.
@api_view(['GET'])
def get_modules_installed(request):
    modules_installed = ModuleQuality().modules_installed()
    return Response (modules_installed)

@api_view(['GET'])
def get_count_of_code(request):
    count_of_code = ModuleQuality().count_lines_of_code_in_modules()
    return Response (count_of_code)

@api_view(['GET'])
def get_module_naming(request):
    module_naming = ModuleQuality().get_module_naming()
    return Response(module_naming)

@api_view(['GET'])
def get_count_of_non_stored_fields(request):
    non_stored_fields = ModuleQuality().count_of_non_stored_fields()
    return Response(non_stored_fields)

@api_view(['GET'])
def get_module_load_time(request):
    module_load_time = ModuleQuality().module_load_time()
    return Response(module_load_time)

@api_view(['GET'])
def get_pep_module_filter(request):
    pep_module_filter = ModuleQuality().pep_module_filter()
    return Response(pep_module_filter)

@api_view(['GET'])
def get_pep_standard_template(request):
    pep_standard_template = ModuleQuality().pep_standard_template()
    return Response(pep_standard_template)

@api_view(['GET'])
def get_function_counts(request):
    function_counts = ModuleQuality().function_counts()
    return Response(function_counts)