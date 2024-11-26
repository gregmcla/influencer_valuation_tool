from typing import Dict, Optional
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, api_service):
        self.api_service = api_service

    def calculate_growth_metrics(self, profile: Dict) -> Dict:
        try:
            return {
                'viewer_retention': self._calculate_retention(profile),
                'revenue_per_viewer': self._calculate_rpm(profile),
                'growth_rate': self._calculate_growth_rate(profile),
                'engagement_score': self._calculate_engagement_score(profile)
            }
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {str(e)}")
            return {}

    def compare_streamers(self, streamer1: str, streamer2: str, platform: str) -> Dict:
        try:
            profile1 = self.api_service.get_profile_data(streamer1, platform)
            profile2 = self.api_service.get_profile_data(streamer2, platform)
            
            metrics = ['followers', 'avg_viewers', 'engagement_rate', 'total_revenue']
            comparison = {}
            
            for metric in metrics:
                val1 = profile1.get(metric, 0)
                val2 = profile2.get(metric, 0)
                diff_percent = ((val1 - val2) / val2 * 100) if val2 != 0 else 0
                
                comparison[metric] = {
                    'streamer1': val1,
                    'streamer2': val2,
                    'difference': round(diff_percent, 2),
                    'winner': streamer1 if val1 > val2 else streamer2
                }
            
            return comparison
        except Exception as e:
            logger.error(f"Comparison failed: {str(e)}")
            raise

    def _calculate_retention(self, profile: Dict) -> float:
        avg_viewers = profile.get('avg_viewers', 0)
        peak_viewers = profile.get('peak_viewers', 1)
        return round((avg_viewers / peak_viewers) * 100, 2) if peak_viewers else 0

    def _calculate_rpm(self, profile: Dict) -> float:
        total_revenue = profile.get('total_revenue', 0)
        avg_viewers = profile.get('avg_viewers', 1)
        return round(total_revenue / avg_viewers, 2) if avg_viewers else 0

    def _calculate_growth_rate(self, profile: Dict) -> float:
        # Simplified growth rate calculation
        engagement = profile.get('engagement_rate', 0)
        stream_frequency = len(profile.get('stream_schedule', [])) / 7
        return round(engagement * stream_frequency * 100, 2)

    def _calculate_engagement_score(self, profile: Dict) -> float:
        avg_viewers = profile.get('avg_viewers', 0)
        engagement = profile.get('engagement_rate', 0)
        stream_frequency = len(profile.get('stream_schedule', [])) / 7
        
        normalized_viewers = min(avg_viewers / 10000, 1)
        normalized_engagement = min(engagement * 100, 1)
        
        score = (normalized_viewers * 0.4 + 
                normalized_engagement * 0.3 + 
                stream_frequency * 0.3)
        
        return round(score * 100, 2)