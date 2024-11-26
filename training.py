# training.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_model():
    # Load your dataset
    data = pd.read_csv('data/influencer_dataset.csv')
    
    # Feature selection
    X = data[['follower_count', 'engagement_rate']]  # Example features
    y = data['valuation']  # Target variable
    
    # Train the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Ensure the models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    joblib.dump(model, 'models/valuation_model.pkl')

if __name__ == '__main__':
    train_model()