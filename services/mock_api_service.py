import json
import random
from pathlib import Path

class MockAPIService:
    def __init__(self):
        try:
            data_path = Path(__file__).parent.parent / 'data' / 'mock_data.json'
            with open(data_path, 'r') as f:
                self.mock_data = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load mock data: {str(e)}")

    def get_profile_data(self, username: str, platform: str) -> dict:
        if not username or not platform:
            raise ValueError("Username and platform are required")
            
        platform_data = self.mock_data.get(platform.lower(), {})
        profile = platform_data.get(username.lower())
        
        if not profile:
            raise ValueError(f"Profile not found for {username} on {platform}")
            
        return profile