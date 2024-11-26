# app.py

from preprocessing import prepare_features
from flask import Flask, request, render_template
import numpy as np
from model import predict_valuation
from data_fetching import fetch_influencer_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        influencer_username = request.form['username']
        platform = request.form['platform']
        
        # Fetch influencer data from the selected platform
        influencer_data = fetch_influencer_data(platform, influencer_username)
        
        if influencer_data:
            # Prepare data for prediction
            input_features = prepare_features(influencer_data)
            
            # Predict valuation
            valuation = predict_valuation(input_features)
            
            return render_template('result.html', valuation=valuation, username=influencer_username)
        else:
            error_message = "Unable to retrieve data for the provided username."
            return render_template('index.html', error=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)