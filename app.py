# app.py

from flask import Flask, render_template, request, abort
import logging
import os
from services.mock_api_service import MockAPIService
from services.leaderboard_service import LeaderboardService
from services.analytics_service import AnalyticsService
from services.cache_service import cached
from werkzeug.exceptions import NotFound

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask with explicit template folder
app = Flask(__name__, 
           template_folder=os.path.abspath('templates'))

# Debug info
logger.info(f"Template folder: {app.template_folder}")
logger.info(f"Available templates: {os.listdir(app.template_folder)}")

# Initialize services
api_service = MockAPIService()
leaderboard_service = LeaderboardService()
analytics_service = AnalyticsService(api_service)

@app.template_filter('format_number')
def format_number(value):
    return "{:,.0f}".format(value)

def calculate_valuation(profile_data, platform):
    base_value = profile_data.get('estimated_cost_per_post', 0)
    engagement_multiplier = 1 + (profile_data.get('engagement_rate', 0) * 10)
    frequency = profile_data.get('post_frequency', 1)
    monthly_valuation = base_value * engagement_multiplier * frequency * 4
    return round(monthly_valuation)

def calculate_streamer_revenue(profile_data, platform):
    try:
        if platform == 'twitch':
            monthly = (
                profile_data.get('sub_revenue', 0) +
                profile_data.get('bit_revenue', 0) +
                profile_data.get('donation_revenue', 0) +
                profile_data.get('sponsorship_value', 0)
            )
        elif platform == 'youtube_gaming':
            monthly = (
                profile_data.get('membership_revenue', 0) +
                profile_data.get('superchat_revenue', 0) +
                profile_data.get('sponsorship_value', 0) +
                profile_data.get('merchandise_revenue', 0)
            )
        return monthly
    except Exception as e:
        logger.error(f"Revenue calculation error: {str(e)}")
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            platform = request.form.get('platform', '').strip()
            
            if not username or not platform:
                raise ValueError("Both username and platform are required")
            
            profile_data = api_service.get_profile_data(username, platform)
            revenue = calculate_streamer_revenue(profile_data, platform)
            analytics = analytics_service.calculate_growth_metrics(profile_data)
            
            return render_template('result.html', 
                                profile=profile_data,
                                username=username,
                                platform=platform,
                                revenue=revenue,
                                analytics=analytics)
        return render_template('index.html')
    except Exception as e:
        logger.exception("Error in index route")
        return render_template('index.html', error=str(e))

@app.route('/compare', methods=['GET', 'POST'])
def compare_streamers():
    try:
        if request.method == 'POST':
            streamer1 = request.form.get('streamer1')
            streamer2 = request.form.get('streamer2')
            platform = request.form.get('platform')
            
            if not all([streamer1, streamer2, platform]):
                raise ValueError("All fields are required")
            
            comparison = analytics_service.compare_streamers(
                streamer1=streamer1,
                streamer2=streamer2,
                platform=platform
            )
            
            return render_template('compare.html',
                                comparison=comparison,
                                platform=platform)
        return render_template('compare.html')
    except ValueError as e:
        return render_template('compare.html', error=str(e))
    except Exception as e:
        logger.exception("Error in compare route")
        return render_template('error.html', error="Comparison failed"), 500

@app.route('/analytics/<platform>/<username>')
@cached(ttl_hours=1)
def streamer_analytics(platform, username):
    try:
        profile_data = api_service.get_profile_data(username, platform)
        analytics = analytics_service.calculate_growth_metrics(profile_data)
        
        return render_template('analytics.html',
                             profile=profile_data,
                             analytics=analytics,
                             platform=platform,
                             username=username)
    except Exception as e:
        logger.exception("Error in analytics route")
        return render_template('index.html', error=str(e))

@app.route('/leaderboard')
def leaderboard():
    try:
        sort_by = request.args.get('sort_by', 'followers')
        all_streamers = leaderboard_service.get_top_streamers(sort_by)
        
        return render_template('leaderboard.html', 
                             streamers=all_streamers,
                             current_sort=sort_by)
    except Exception as e:
        logger.exception("Error in leaderboard route")
        return render_template('error.html', error="Failed to load leaderboard"), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True)