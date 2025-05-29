"""
YouTube transcript extraction service
"""

import re
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from config.settings import get_settings

settings = get_settings()

class TranscriptService:
    """Service for extracting and processing YouTube transcripts"""
    
    def __init__(self):
        self.max_length = settings.MAX_TRANSCRIPT_LENGTH
    
    async def get_transcript(self, video_id: str) -> Optional[str]:
        """Get and process video transcript"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = self._find_best_transcript(transcript_list)
            
            if not transcript:
                return None
            
            transcript_data = transcript.fetch()
            return self._process_transcript(transcript_data)
            
        except (NoTranscriptFound, TranscriptsDisabled):
            return None
        except Exception:
            return None
    
    def _find_best_transcript(self, transcript_list):
        """Find the best available transcript"""
        # Try manual English first
        try:
            return transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
        except:
            pass
        
        # Try auto-generated English
        try:
            return transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB'])
        except:
            pass
        
        # Try any manual transcript
        for transcript in transcript_list:
            if not transcript.is_generated:
                return transcript
        
        # Try any auto-generated transcript
        for transcript in transcript_list:
            if transcript.is_generated:
                return transcript
        
        return None
    
    def _process_transcript(self, transcript_data: List[Dict]) -> str:
        """Process raw transcript data into clean text"""
        if not transcript_data:
            return ""
        
        full_text = ""
        for entry in transcript_data:
            text = entry.get('text', '')
            if text:
                cleaned_text = self._clean_text(text)
                if cleaned_text:
                    full_text += cleaned_text + " "
        
        # Limit length
        if len(full_text) > self.max_length:
            full_text = full_text[:self.max_length] + "..."
        
        return full_text.strip()
    
    def _clean_text(self, text: str) -> str:
        """Clean transcript text"""
        if not text:
            return ""
        
        # Remove brackets and music notation
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'♪.*?♪', '', text)
        
        # Remove common artifacts
        text = re.sub(r'\[Music\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[Applause\]', '', text, flags=re.IGNORECASE)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive filler words
        text = re.sub(r'\b(um|uh|er|ah)\b', '', text, flags=re.IGNORECASE)
        
        return text.strip()