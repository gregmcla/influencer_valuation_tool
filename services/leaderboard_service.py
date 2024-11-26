
from typing import List, Dict
from .mock_api_service import MockAPIService

class LeaderboardService:
    def __init__(self):
        self.api_service = MockAPIService()
        self.platforms = ['twitch', 'youtube_gaming']
        
    def get_top_streamers(self, sort_by: str = 'followers') -> List[Dict]:
        all_streamers = []
        
        for platform in self.platforms:
            try:
                platform_data = self.api_service.mock_data.get(platform, {})
                for username, data in platform_data.items():
                    streamer_data = self.api_service.get_profile_data(username, platform)
                    streamer_data['username'] = username
                    streamer_data['platform'] = platform
                    all_streamers.append(streamer_data)
            except Exception as e:
                print(f"Error processing platform {platform}: {str(e)}")
                continue
        
        return self._sort_streamers(all_streamers, sort_by)
    
    def _sort_streamers(self, streamers: List[Dict], sort_by: str) -> List[Dict]:
        valid_sort_fields = {
            'followers': lambda x: x.get('followers', 0),
            'total_revenue': lambda x: x.get('total_revenue', 0),
            'engagement_rate': lambda x: x.get('engagement_rate', 0)
        }
        
        sort_key = valid_sort_fields.get(sort_by, valid_sort_fields['followers'])
        return sorted(streamers, key=sort_key, reverse=True)