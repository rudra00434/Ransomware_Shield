import yara
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Global cache for compiled YARA rules
COMPILED_RULES = None
COMPILED_RULES_TIME = 0

def load_yara_rules():
    global COMPILED_RULES
    global COMPILED_RULES_TIME
    rule_dir = os.path.join(settings.BASE_DIR, 'yara_rules')
    
    if not os.path.exists(rule_dir):
        logger.warning(f"Yara rules directory not found: {rule_dir}")
        return None
        
    filepaths = {}
    for root, dirs, files in os.walk(rule_dir):
        for file in files:
            if file.endswith('.yar'):
                filepaths[file] = os.path.join(root, file)
                
    if not filepaths:
        logger.warning("No Yara rules found in directory.")
        return None
        
    try:
        COMPILED_RULES = yara.compile(filepaths=filepaths)
        COMPILED_RULES_TIME = os.path.getmtime(rule_dir) # simple cache invalidation
        logger.info(f"Successfully compiled {len(filepaths)} YARA rule files.")
        return COMPILED_RULES
    except Exception as e:
        logger.error(f"Failed to compile YARA rules: {e}")
        return None

def analyze_yara(file_path):
    global COMPILED_RULES
    results = {
        'matches': [],
        'error': None
    }
    try:
        # Use cached rules if available
        if not COMPILED_RULES:
            rules = load_yara_rules()
        else:
            rules = COMPILED_RULES
            
        if not rules:
            results['error'] = 'No compiled YARA rules available.'
            return results
            
        # timeout prevents ReDoS (Regex Denial of Service)
        matches = rules.match(file_path, timeout=30)
        
        for match in matches:
            results['matches'].append({
                'rule': match.rule,
                'tags': match.tags,
                'meta': match.meta,
                # Extracted strings can be large, we'll keep it disabled by default
                # 'strings': [[s[0], s[1], s[2].decode('utf-8', errors='ignore')] for s in match.strings[:5]] 
            })
            
    except yara.TimeoutError:
         results['error'] = 'YARA scan timed out (possible complex rule / large file).'
    except Exception as e:
        results['error'] = str(e)
        
    return results
