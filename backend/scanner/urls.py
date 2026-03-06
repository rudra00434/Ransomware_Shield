from django.urls import path
from .views import FileUploadView, ScanStatusView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('jobs/<int:pk>/', ScanStatusView.as_view(), name='scan_status'),
]
