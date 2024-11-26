# preprocessing.py

import numpy as np

def prepare_features(influencer_data):
    # Extract necessary features from influencer_data
    follower_count = influencer_data.get('follower_count', 0)
    engagement_rate = influencer_data.get('engagement_rate', 0.0)
    
    # Create a feature array
    input_features = np.array([follower_count, engagement_rate])
    return input_features