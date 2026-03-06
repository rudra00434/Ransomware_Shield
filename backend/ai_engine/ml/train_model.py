import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_data(num_samples=5000):
    """
    Generate synthetic data for training the Malware Classifier.
    Features: ['entropy', 'suspicious_sections', 'is_pe']
    Target: 0 (Clean), 1 (Malware)
    """
    logger.info(f"Generating {num_samples} synthetic samples...")
    data = []
    
    # 1. Generate Clean Files (Target = 0)
    # Characteristics: Normal entropy (4.0 - 6.5), few/no suspicious sections, mostly valid PEs
    num_clean = num_samples // 2
    for _ in range(num_clean):
        is_pe = np.random.choice([0, 1], p=[0.05, 0.95]) # Most clean files are valid PEs
        entropy = np.round(np.random.uniform(3.5, 6.8), 2)
        suspicious_sections = np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
        data.append([entropy, suspicious_sections, is_pe, 0])

    # 2. Generate Malware / Ransomware (Target = 1)
    # Characteristics: High entropy (often packed/encrypted > 7.0), multiple suspicious sections, often valid PEs
    num_malware = num_samples - num_clean
    for _ in range(num_malware):
        is_pe = np.random.choice([0, 1], p=[0.1, 0.9])
        
        # Ransomware often has very high entropy
        entropy_type = np.random.choice(['high', 'extreme'], p=[0.4, 0.6])
        if entropy_type == 'high':
            entropy = np.round(np.random.uniform(6.5, 7.5), 2)
        else:
            entropy = np.round(np.random.uniform(7.5, 8.0), 2)
            
        suspicious_sections = np.random.randint(1, 10) # 1 to 9 suspicious sections
        data.append([entropy, suspicious_sections, is_pe, 1])
        
    # 3. Add Edge Cases
    # Clean file but packed (High entropy, 0 suspicious sections)
    for _ in range(50):
        data.append([np.round(np.random.uniform(7.0, 7.8), 2), 0, 1, 0])
        
    # Malware but low entropy (Dropper/Downloader)
    for _ in range(50):
        data.append([np.round(np.random.uniform(4.0, 5.5), 2), np.random.randint(2, 5), 1, 1])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['entropy', 'suspicious_sections', 'is_pe', 'target'])
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

def train_and_save_model():
    # 1. Generate Data
    df = generate_synthetic_data(num_samples=10000)
    
    X = df[['entropy', 'suspicious_sections', 'is_pe']]
    y = df['target']
    
    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Train Gradient Boosting Classifier
    logger.info("Training Gradient Boosting Classifier...")
    model = GradientBoostingClassifier(
        n_estimators=200, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # 4. Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model Accuracy: {accuracy * 100:.2f}%")
    logger.info("\nClassification Report:\n" + classification_report(y_test, y_pred))
    
    # 5. Save Model
    # Determine save path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(os.path.dirname(current_dir), '..', 'ml_models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'malware_classifier.pkl')
    joblib.dump(model, model_path)
    logger.info(f"Successfully saved new high-accuracy model to: {model_path}")

if __name__ == "__main__":
    train_and_save_model()
