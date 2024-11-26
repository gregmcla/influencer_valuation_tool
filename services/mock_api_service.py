import json
from pathlib import Path
from typing import Dict, Optional

class MockAPIService:
    def __init__(self):
        self._init_mock_data()

    def _init_mock_data(self) -> None:
        try:
            data_path = Path(__file__).parent.parent / 'data' / 'mock_data.json'
            with open(data_path, 'r') as f:
                self.mock_data = json.load(f)
        except FileNotFoundError:
            raise RuntimeError("Mock data file not found. Ensure mock_data.json exists in the data directory.")
        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON format in mock_data.json")

    def get_profile_data(self, username: str, platform: str) -> Dict:
        self._validate_inputs(username, platform)
        platform_data = self.mock_data.get(platform.lower(), {})
        profile = platform_data.get(username.lower(), {})
        
        if not profile:
            raise ValueError(f"Profile not found for {username} on {platform}")
        
        return self._enrich_profile_data(profile, platform)

    def _validate_inputs(self, username: str, platform: str) -> None:
        if not username or not isinstance(username, str):
            raise ValueError("Invalid username")
        if platform not in ['twitch', 'youtube_gaming']:
            raise ValueError("Invalid platform. Must be 'twitch' or 'youtube_gaming'")

    def _enrich_profile_data(self, profile: Dict, platform: str) -> Dict:
        # Add calculated fields
        profile['total_revenue'] = self._calculate_total_revenue(profile, platform)
        profile['engagement_rate'] = profile.get('engagement_rate', 0)
        return profile

    def _calculate_total_revenue(self, profile: Dict, platform: str) -> float:
        if platform == 'twitch':
            return sum([
                profile.get('sub_revenue', 0),
                profile.get('bit_revenue', 0),
                profile.get('donation_revenue', 0),
                profile.get('sponsorship_value', 0)
            ])
        return sum([
            profile.get('membership_revenue', 0),
            profile.get('superchat_revenue', 0),
            profile.get('sponsorship_value', 0),
            profile.get('merchandise_revenue', 0)
        ])