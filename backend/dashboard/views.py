from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from scanner.models import ScanJob, ScanResult

class DashboardStatsView(APIView):
    # Depending on requirements, could be IsAuthenticated
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now()
        thirty_days_ago = today - timedelta(days=30)
        seven_days_ago = today - timedelta(days=7)

        # 1. KPI Stats
        total_scans_7d = ScanJob.objects.filter(created_at__gte=seven_days_ago).count()
        total_scans_previous_7d = ScanJob.objects.filter(
            created_at__gte=seven_days_ago - timedelta(days=7),
            created_at__lt=seven_days_ago
        ).count()
        
        # Calculate % change for Total Scans (avoid division by 0)
        if total_scans_previous_7d > 0:
            scan_change = ((total_scans_7d - total_scans_previous_7d) / total_scans_previous_7d) * 100
        else:
            scan_change = 100 if total_scans_7d > 0 else 0

        # Threat counts (All time or last 7 days depending on preference, let's do all time for KPI totals except as noted)
        critical_threats = ScanResult.objects.filter(threat_level='CRITICAL').count()
        suspicious_files = ScanResult.objects.filter(threat_level__in=['LOW', 'MEDIUM', 'HIGH']).count()
        clean_files = ScanResult.objects.filter(threat_level='CLEAN').count()
        total_completed = ScanResult.objects.count()
        
        clear_rate = (clean_files / total_completed * 100) if total_completed > 0 else 100

        # 2. Recent Detections (Last 5 malicious/suspicious)
        recent_detections = ScanResult.objects.exclude(threat_level='CLEAN').order_by('-created_at')[:5]
        recent_detections_data = [
            {
                'id': res.id,
                'file_name': res.job.file_name,
                'threat_level': res.threat_level,
                'created_at': res.created_at.isoformat()
            } for res in recent_detections
        ]

        # 3. Timeline Chart Data (Last 7 days)
        timeline_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            day_str = date.strftime('%a') # Mon, Tue, etc.
            
            # Count results for this specific day
            day_results = ScanResult.objects.filter(
                created_at__date=date.date()
            ).values('threat_level').annotate(count=Count('threat_level'))
            
            day_stats = {'name': day_str, 'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Clean': 0}
            for res in day_results:
                level = res['threat_level'].capitalize()
                if level in day_stats:
                    day_stats[level] = res['count']
                    
            timeline_data.append(day_stats)

        return Response({
            'kpi': {
                'total_scans_7d': total_scans_7d,
                'scan_change_pct': round(scan_change, 1),
                'critical_threats': critical_threats,
                'suspicious_files': suspicious_files,
                'clean_files': clean_files,
                'clear_rate': round(clear_rate, 1)
            },
            'recent_detections': recent_detections_data,
            'timeline': timeline_data
        })
