from .feature_extractor import FeatureExtractor
import joblib
import os
import logging

logger = logging.getLogger(__name__)

class MalwareClassifier:
    def __init__(self):
        self.extractor = FeatureExtractor()
        
        # Load the generated pickle model dynamically
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models', 'malware_classifier.pkl')
        try:
            self.model = joblib.load(model_path)
            logger.info("Successfully loaded Random Forest Malware Classifier.")
        except Exception as e:
            logger.error(f"Failed to load ML model from {model_path}: {e}")
            self.model = None

    def predict(self, static_analysis_results):
        features = self.extractor.extract(static_analysis_results)
        
        if not self.model:
            # Fallback heuristic if the model fails to load
            entropy = features[0][0]
            suspicious = features[0][1]
            if entropy > 7.0 and suspicious > 2:
                return {'is_malware': True, 'confidence': 0.85}
            return {'is_malware': False, 'confidence': 0.60}
            
        try:
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Probability array contains [prob_clean, prob_malware]
            confidence = probabilities[1] if prediction == 1 else probabilities[0]
            
            return {
                'is_malware': bool(prediction == 1),
                'confidence': float(confidence)
            }
        except Exception as e:
            logger.error(f"ML Prediction error: {e}")
            return {'is_malware': False, 'confidence': 0.0}
