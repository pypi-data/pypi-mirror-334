"""
This module is used to map urls path with view method
"""

from django.urls import path
from system_report import views

urlpatterns = [
    path(
        # "",views.system_report,name='',
        'system-data/',views.system_report,name="system-data"
    )
]
