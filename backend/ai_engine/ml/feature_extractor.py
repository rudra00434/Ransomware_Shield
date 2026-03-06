import json

class FeatureExtractor:
    def extract(self, pe_data):
        """
        Extract numerical features from the static analyzer results
        to pass into the trained Random Forest model.
        Features: ['entropy', 'suspicious_sections', 'is_pe']
        """
        if not pe_data:
            return [[0.0, 0, 0]]
            
        entropy = pe_data.get('entropy', 0.0)
        suspicious_sections = len(pe_data.get('suspicious_sections', []))
        is_pe = 1 if pe_data.get('is_pe', False) else 0
        
        # Scikit-Learn expects a 2D array for predictions
        return [[entropy, suspicious_sections, is_pe]]
