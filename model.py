# model.py

import joblib

def predict_valuation(input_features):
    # Load the trained model
    model = joblib.load('models/valuation_model.pkl')
    # Predict the valuation
    valuation = model.predict([input_features])[0]
    return valuation