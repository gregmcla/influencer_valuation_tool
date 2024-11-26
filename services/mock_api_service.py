import json
import random
import time
from pathlib import Path

class MockAPIService:
    def __init__(self):
        data_path = Path(__file__).parent.parent / 'data' / 'mock_data.json'
        with open(data_path, 'r') as f:
            self.mock_data = json.load(f)
    
    def get_profile_data(self, username: str, platform: str) -> dict:
        self._simulate_network_delay()
        
        if random.random() < 0.1:
            raise Exception("API rate limit exceeded")
            
        platform_data = self.mock_data.get(platform, {})
        profile = platform_data.get(username.lower())
        
        if not profile:
            raise Exception("Profile not found")
            
        return profile

    def _simulate_network_delay(self):
        delay = random.uniform(0.1, 0.8)
        time.sleep(delay)