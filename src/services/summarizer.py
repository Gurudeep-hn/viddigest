"""
AI-powered video summarization service
"""

import re
from typing import Dict, List
from config.settings import get_settings

# Optional Groq import
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

settings = get_settings()

class VideoSummarizer:
    """Service for generating AI-powered video summaries"""
    
    def __init__(self):
        self.client = None
        self.use_ai = False
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client if available"""
        if not GROQ_AVAILABLE or not settings.GROQ_API_KEY:
            return
        
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.use_ai = True
        except Exception:
            pass
    
    def is_model_loaded(self) -> bool:
        """Check if AI model is available"""
        return self.use_ai and self.client is not None
    
    async def summarize(self, transcript: str, video_title: str) -> Dict:
        """Generate comprehensive video summary"""
        if self.use_ai and self.client:
            try:
                return await self._ai_summarize(transcript, video_title)
            except Exception:
                pass
        
        return self._rule_based_summarize(transcript, video_title)
    
    async def _ai_summarize(self, transcript: str, video_title: str) -> Dict:
        """Generate summary using AI"""
        # Limit transcript for API efficiency
        if len(transcript) > 4000:
            transcript = transcript[:4000] + "..."
        
        summary = await self._generate_ai_summary(transcript, video_title)
        key_points = await self._generate_ai_key_points(transcript)
        timestamps = self._generate_timestamps(transcript)
        
        return {
            'summary': summary,
            'key_points': key_points,
            'timestamps': timestamps
        }
    
    async def _generate_ai_summary(self, transcript: str, video_title: str) -> str:
        """Generate summary using Groq AI"""
        prompt = f"Summarize this YouTube video in 2-3 clear sentences:\n\nTitle: {video_title}\n\nTranscript: {transcript}\n\nSummary:"
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You create concise, helpful video summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return self._extract_simple_summary(transcript)
    
    async def _generate_ai_key_points(self, transcript: str) -> List[str]:
        """Generate key points using Groq AI"""
        prompt = f"Extract 4-5 key points from this transcript:\n\n{transcript[:2000]}\n\nKey points:"
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You extract clear, actionable key points."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            return self._parse_key_points(response.choices[0].message.content)
        except Exception:
            return self._extract_simple_key_points(transcript)
    
    def _rule_based_summarize(self, transcript: str, video_title: str) -> Dict:
        """Generate summary using rule-based approach"""
        return {
            'summary': self._extract_simple_summary(transcript),
            'key_points': self._extract_simple_key_points(transcript),
            'timestamps': self._generate_timestamps(transcript)
        }
    
    def _extract_simple_summary(self, transcript: str) -> str:
        """Extract summary using text analysis"""
        sentences = [s.strip() for s in transcript.split('.') if s.strip() and len(s.strip()) > 10]
        
        if len(sentences) < 2:
            return "This video covers important topics discussed in the content."
        
        summary = f"{sentences[0]}. {sentences[-1] if len(sentences) > 1 else ''}"
        
        if len(summary) > 300:
            summary = summary[:300] + "..."
        
        return summary
    
    def _extract_simple_key_points(self, transcript: str) -> List[str]:
        """Extract key points using keyword analysis"""
        sentences = [s.strip() for s in transcript.split('.') if s.strip()]
        key_points = []
        
        keywords = ['important', 'key', 'main', 'first', 'second', 'remember']
        
        for sentence in sentences:
            if 20 <= len(sentence) <= 100:
                if any(kw in sentence.lower() for kw in keywords):
                    key_points.append(sentence)
                    if len(key_points) >= 5:
                        break
        
        if len(key_points) < 3:
            key_points = [
                "Video provides educational content",
                "Multiple concepts are explained",
                "Information is presented clearly"
            ]
        
        return key_points[:5]
    
    def _generate_timestamps(self, transcript: str) -> List[str]:
        """Generate timestamps based on content length"""
        words = len(transcript.split())
        duration = words / 150  # Estimate speaking rate
        
        if duration < 3:
            return ["00:00 - Introduction", "01:30 - Main Content"]
        elif duration < 8:
            return [
                "00:00 - Introduction",
                "02:00 - Main Discussion",
                "04:30 - Key Points",
                "06:00 - Conclusion"
            ]
        else:
            return [
                "00:00 - Introduction",
                "02:30 - Topic Overview",
                "05:00 - Main Content",
                "08:00 - Key Examples",
                "10:30 - Summary"
            ]
    
    def _parse_key_points(self, points_text: str) -> List[str]:
        """Parse key points from AI response"""
        lines = points_text.split('\n')
        points = []
        
        for line in lines:
            line = line.strip()
            line = re.sub(r'^\d+\.\s*', '', line)
            line = re.sub(r'^[-•*]\s*', '', line)
            
            if line and len(line) > 10:
                points.append(line)
        
        return points[:5] if points else self._extract_simple_key_points("")