from django.urls import path
from .views import GeneratePDFReportView

urlpatterns = [
    path('download/<int:result_id>/', GeneratePDFReportView.as_view(), name='download-report'),
]
