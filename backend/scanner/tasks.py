from celery import shared_task
from .models import ScanJob, ScanResult, ThreatReport
from .engines.static_analyzer import analyze_pe
from .engines.yara_engine import analyze_yara
from .engines.vt_client import check_file_hash
import sys
import os

# Add the parent directory to sys.path to easily import the ai_engine
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from ai_engine.ml.classifier import MalwareClassifier
from ai_engine.llm.threat_explainer import generate_explanation

@shared_task
def run_full_scan(job_id, file_path):
    try:
        job = ScanJob.objects.get(id=job_id)
        job.status = 'SCANNING'
        job.save()

        # Initialize result
        result = ScanResult.objects.create(job=job)
        engine_results = {}

        # 1. Static Analysis (Includes hashing)
        static_res = analyze_pe(file_path)
        engine_results['static'] = static_res

        # 2. YARA Matching
        yara_res = analyze_yara(file_path)
        engine_results['yara'] = yara_res
        
        # 3. VirusTotal Check (Using md5 if PE hash failed)
        import hashlib
        file_hash = static_res.get('imphash')
        if not file_hash:
             file_hash = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
             
        vt_res = check_file_hash(file_hash)
        engine_results['virustotal'] = vt_res
        
        # 4. Machine Learning Classification
        ml_classifier = MalwareClassifier()
        ml_res = ml_classifier.predict(static_res)
        engine_results['ml_classifier'] = ml_res
        
        # Determine threat level combining all engines
        threat_level = 'CLEAN'
        
        vt_malicious = vt_res.get('malicious', 0) if isinstance(vt_res, dict) else 0
        yara_matches_count = len(yara_res.get('matches', []))
        static_suspicious = len(static_res.get('suspicious_sections', []))
        suspicious_imports = len(static_res.get('suspicious_imports', []))
        timestamp_anomaly = 1 if static_res.get('compiler_timestamp_anomaly', False) else 0
        
        is_ml_malware = ml_res.get('is_malware', False)
        
        # New weighted detection score
        detection_score = (vt_malicious * 2) + \
                          (yara_matches_count * 2) + \
                          static_suspicious + \
                          (suspicious_imports * 0.5) + \
                          timestamp_anomaly + \
                          (3 if is_ml_malware else 0)
        
        if detection_score >= 5:
            threat_level = 'CRITICAL'
        elif detection_score >= 3:
            threat_level = 'HIGH'
        elif detection_score >= 1:
            threat_level = 'LOW'

        # Update Result
        result.threat_level = threat_level
        result.detection_count = detection_score
        result.ml_confidence_score = ml_res.get('confidence', 0.0)
        result.engine_results = engine_results
        result.save()

        # Job Completed
        job.status = 'COMPLETED'
        job.save()

        # Trigger AI Explanation
        generate_threat_report.delay(result.id)
    
    except Exception as e:
        if 'job' in locals():
            job.status = 'FAILED'
            job.save()
        print(f"Error in scan task: {e}")
        
    finally:
        # SECURE FILE HANDLING: Auto-delete the file after analysis
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Securely deleted analyzed file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file {file_path}: {e}")

@shared_task
def generate_threat_report(result_id):
    """ Celery task to generate the LLM explanation asynchronously so it doesn't block """
    try:
        result = ScanResult.objects.get(id=result_id)
        explanation = generate_explanation(result.threat_level, result.engine_results)
        
        ThreatReport.objects.create(
            result=result,
            llm_explanation=explanation
        )
    except Exception as e:
        print(f"Failed to generate AI report: {e}")
    except Exception as e:
        print(f"Failed to generate AI report: {e}")
