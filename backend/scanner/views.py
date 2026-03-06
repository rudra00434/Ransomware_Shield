import hashlib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ScanJob
from .serializers import ScanJobSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import os

class FileUploadView(APIView):
    # AllowAny for initial testing, later change to IsAuthenticated if desired
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_size = uploaded_file.size
        
        # Calculate SHA256 Hash
        sha256_hash = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            sha256_hash.update(chunk)
        file_hash = sha256_hash.hexdigest()

        # Check if already scanned recently
        existing_job = ScanJob.objects.filter(file_hash=file_hash).order_by('-created_at').first()
        if existing_job and existing_job.status == 'COMPLETED':
            serializer = ScanJobSerializer(existing_job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new Job
        user = request.user if request.user.is_authenticated else None
        job = ScanJob.objects.create(
            user=user,
            file_name=file_name,
            file_hash=file_hash,
            file_size=file_size,
            status='PENDING'
        )

        # Save to temp storage
        uploaded_file.seek(0)
        rel_path = default_storage.save(f"temp_scans/{uuid.uuid4()}_{file_name}", ContentFile(uploaded_file.read()))
        absolute_file_path = default_storage.path(rel_path)

        # Trigger Celery Task
        from .tasks import run_full_scan
        run_full_scan.delay(job.id, absolute_file_path)
        
        serializer = ScanJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ScanStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            job = ScanJob.objects.get(pk=pk)
            serializer = ScanJobSerializer(job)
            return Response(serializer.data)
        except ScanJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
