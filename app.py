# app.py

from flask import Flask, render_template, request
import logging
import os
from services.mock_api_service import MockAPIService

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask with explicit template folder
app = Flask(__name__, 
           template_folder=os.path.abspath('templates'))

# Debug info
logger.info(f"Template folder: {app.template_folder}")
logger.info(f"Available templates: {os.listdir(app.template_folder)}")

api_service = MockAPIService()

@app.template_filter('format_number')
def format_number(value):
    return "{:,.0f}".format(value)

def calculate_valuation(profile_data, platform):
    base_value = profile_data.get('estimated_cost_per_post', 0)
    engagement_multiplier = 1 + (profile_data.get('engagement_rate', 0) * 10)
    frequency = profile_data.get('post_frequency', 1)
    monthly_valuation = base_value * engagement_multiplier * frequency * 4
    return round(monthly_valuation)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            platform = request.form.get('platform')
            logger.debug(f"Request: username={username}, platform={platform}")
            
            profile_data = api_service.get_profile_data(username, platform)
            valuation = calculate_valuation(profile_data, platform)
            
            return render_template('result.html', 
                                profile=profile_data,
                                username=username,
                                platform=platform,
                                valuation=valuation)
        return render_template('index.html')
    except Exception as e:
        logger.exception("Error in index route")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)