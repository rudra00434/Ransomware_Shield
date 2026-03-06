from django.db import models
from django.conf import settings

class ScanJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SCANNING', 'Scanning'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, db_index=True) # SHA256
    file_size = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_name} ({self.status})"

class ScanResult(models.Model):
    LEVEL_CHOICES = [
        ('CLEAN', 'Clean'),
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Threat')
    ]

    job = models.OneToOneField(ScanJob, on_delete=models.CASCADE, related_name='result')
    threat_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='CLEAN')
    detection_count = models.IntegerField(default=0)
    engine_results = models.JSONField(default=dict)
    ml_confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.job.file_name} - {self.threat_level}"

class ThreatReport(models.Model):
    result = models.OneToOneField(ScanResult, on_delete=models.CASCADE, related_name='report')
    llm_explanation = models.TextField()
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
