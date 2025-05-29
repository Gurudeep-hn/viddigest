"""
YouTube video information service
"""

import re
import requests
from typing import Dict, Optional
from config.settings import get_settings

settings = get_settings()

class YouTubeService:
    """Service for extracting YouTube video information"""
    
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    async def get_video_info(self, video_id: str) -> Dict[str, str]:
        """Get video metadata using available methods"""
        methods = [
            self._get_info_from_api,
            self._get_info_from_oembed,
            self._get_minimal_info
        ]
        
        for method in methods:
            try:
                result = await method(video_id)
                if result:
                    return result
            except Exception:
                continue
        
        return self._get_minimal_info(video_id)
    
    async def _get_info_from_api(self, video_id: str) -> Dict[str, str]:
        """Get video info using YouTube Data API"""
        if not self.api_key:
            raise Exception("No API key")
        
        url = f"{self.base_url}/videos"
        params = {
            'part': 'snippet,contentDetails,statistics',
            'id': video_id,
            'key': self.api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('items'):
            raise Exception("Video not found")
        
        item = data['items'][0]
        snippet = item['snippet']
        statistics = item.get('statistics', {})
        duration = item['contentDetails']['duration']
        
        return {
            'title': snippet['title'],
            'duration': self._parse_duration(duration),
            'views': self._format_views(statistics.get('viewCount', '0')),
            'channel': snippet['channelTitle'],
            'description': snippet.get('description', ''),
            'published_at': snippet['publishedAt']
        }
    
    async def _get_info_from_oembed(self, video_id: str) -> Dict[str, str]:
        """Get basic video info using oEmbed API"""
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'title': data.get('title', f'YouTube Video'),
            'duration': 'Unknown',
            'views': 'Unknown',
            'channel': data.get('author_name', 'Unknown'),
            'description': '',
            'published_at': ''
        }
    
    def _get_minimal_info(self, video_id: str) -> Dict[str, str]:
        """Return minimal video info as fallback"""
        return {
            'title': 'YouTube Video',
            'duration': 'Unknown',
            'views': '--',
            'channel': 'YouTube',
            'description': '',
            'published_at': ''
        }
    
    def _parse_duration(self, duration: str) -> str:
        """Parse ISO 8601 duration to readable format"""
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return "0:00"
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def _format_views(self, views: str) -> str:
        """Format view count to readable format"""
        try:
            count = int(views)
            if count >= 1000000:
                return f"{count/1000000:.1f}M"
            elif count >= 1000:
                return f"{count/1000:.1f}K"
            else:
                return str(count)
        except:
            return "Unknown"