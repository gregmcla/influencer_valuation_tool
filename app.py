# app.py

from flask import Flask, render_template, request, jsonify
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Create mock_data.json
data = {
    "instagram": {
        "kimkardashian": {
            "followers": 364000000,
            "avg_likes": 2800000,
            "avg_comments": 12500,
            "engagement_rate": 0.078,
            "post_frequency": 1.2,
            "estimated_cost_per_post": 850000,
            "niche": ["fashion", "lifestyle", "beauty"]
        },
        "cristiano": {
            "followers": 605000000,
            "avg_likes": 5200000,
            "avg_comments": 25000,
            "engagement_rate": 0.086,
            "post_frequency": 0.8,
            "estimated_cost_per_post": 1200000,
            "niche": ["sports", "lifestyle", "fitness"]
        }
    },
    "tiktok": {
        "charlidamelio": {
            "followers": 150000000,
            "avg_likes": 5000000,
            "avg_comments": 30000,
            "engagement_rate": 0.12,
            "post_frequency": 2.5,
            "estimated_cost_per_post": 400000,
            "niche": ["dance", "lifestyle", "entertainment"]
        }
    }
}

# Load mock data
def load_mock_data():
    try:
        with open('mock_data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading mock data: {e}")
        return {}

mock_data = load_mock_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            platform = request.form.get('platform')
            
            if not username or not platform:
                return render_template('index.html', error="Please provide both username and platform")
            
            # Get data from mock_data
            platform_data = mock_data.get(platform, {})
            profile_data = platform_data.get(username, {})
            
            if not profile_data:
                return render_template('index.html', error="User not found")
                
            return render_template('result.html', 
                                profile=profile_data,
                                username=username,
                                platform=platform)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return render_template('index.html', error=str(e))
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)