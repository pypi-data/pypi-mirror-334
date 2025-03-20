
# Create your views here.
from django.shortcuts import render
from database_report.models import DatabaseMetrics
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def database_data(request):
    # for getting database metrics
    database_metrics = DatabaseMetrics()
    get_database_metrics = database_metrics.collect_database_metrics()
    
    return Response (get_database_metrics)

@api_view(['GET'])
def get_odoo_file_health(request):
    # for getting odoo database file health
    database_metrics = DatabaseMetrics()
    get_odoo_file_health = database_metrics.odoo_file_health()
    
    return Response (get_odoo_file_health)

@api_view(['GET'])
def get_concurrent_session_count(request):

    concurrent_session_count = DatabaseMetrics().get_concurrent_session_count()
    return Response (concurrent_session_count)