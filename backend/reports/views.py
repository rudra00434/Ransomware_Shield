from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

from scanner.models import ScanResult

class GeneratePDFReportView(APIView):
    # Depending on requirements, could be IsAuthenticated
    permission_classes = [AllowAny]

    def get(self, request, result_id):
        try:
            # Fetch the scan result
            scan_result = ScanResult.objects.get(id=result_id)
            threat_report = getattr(scan_result, 'report', None)
            
            # Prepare context for the template
            context = {
                'scan_id': scan_result.id,
                'job_id': scan_result.job.id,
                'file_name': scan_result.job.file_name,
                'status': scan_result.job.status,
                'upload_time': scan_result.job.created_at,
                'threat_level': scan_result.threat_level,
                'detection_count': scan_result.detection_count,
                'engine_results': scan_result.engine_results,
                'ai_explanation': threat_report.llm_explanation if threat_report else "No AI Explanation generated yet."
            }

            # Render HTML template
            html_string = render_to_string('reports/pdf_template.html', context)
            
            # Generate PDF
            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)
            
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="Threat_Report_{scan_result.job.file_name}.pdf"'
                return response
            
            return Response({'error': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except ScanResult.DoesNotExist:
            return Response({'error': 'Scan Result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
