from virustotal3.core import Files
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def check_file_hash(file_hash):
    """
    Checks the given file hash (SHA256, MD5, etc.) against VirusTotal's database.
    """
    vt_api_key = getattr(settings, 'VT_API_KEY', None)
    if not vt_api_key:
        logger.warning("VT_API_KEY not set. Skipping VirusTotal check.")
        return {'status': 'skipped', 'message': 'API key not configured'}

    try:
        vt_files = Files(vt_api_key)
        report = vt_files.info_file(file_hash)
        
        # Extract relevant info from the massive VT response
        attributes = report.get('data', {}).get('attributes', {})
        stats = attributes.get('last_analysis_stats', {})
        results = attributes.get('last_analysis_results', {})
        
        return {
            'status': 'success',
            'malicious': stats.get('malicious', 0),
            'suspicious': stats.get('suspicious', 0),
            'undetected': stats.get('undetected', 0),
            'total': sum(stats.values()),
            'engines_detected': [engine for engine, details in results.items() if details.get('category') in ('malicious', 'suspicious')]
        }
        
    except Exception as e:
        logger.error(f"VirusTotal API Error: {e}")
        return {'status': 'error', 'message': str(e)}
