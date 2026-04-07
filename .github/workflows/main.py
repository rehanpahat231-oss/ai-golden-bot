#!/usr/bin/env python3
"""
🎬 AI YouTube Shorts Generator - All-In-One Production Agent
Generates viral YouTube Shorts automatically using AI
- Script generation (Groq LLM)
- TTS conversion (edge-tts)
- Video composition (moviepy)
- Fully automated via GitHub Actions
"""

import os
import sys
import json
import asyncio
import random
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, field

# ============================================================================
# IMPORTS & DEPENDENCIES
# ============================================================================

try:
    from loguru import logger
    import requests
    import edge_tts
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
    import librosa
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

# ============================================================================
# CONFIGURATION - ALL IN ONE PLACE
# ============================================================================

@dataclass
class VideoConfig:
    width: int = 1080
    height: int = 1920
    fps: int = 30
    duration_min: float = 5.0
    duration_max: float = 8.0
    target_duration: float = 6.5
    bitrate: str = "8000k"
    codec: str = "libx264"
    preset: str = "medium"
    aspect_ratio: str = "9:16"

@dataclass
class AudioConfig:
    sample_rate: int = 44100
    channels: int = 2
    duration_min: float = 4.5
    duration_max: float = 9.5
    default_volume: float = 0.8

# ============================================================================
# VIRAL CONTENT LIBRARY - PSYCHOLOGY-DRIVEN
# ============================================================================

VIRAL_HOOKS = [
    {"hook": "You won't believe what happened next...", "category": "curiosity_gap"},
    {"hook": "Wait for the twist at the end", "category": "anticipation"},
    {"hook": "This will change your life", "category": "transformation"},
    {"hook": "Try not to blink", "category": "challenge"},
    {"hook": "The ending will shock you", "category": "emotional_spike"},
    {"hook": "This is why you're struggling", "category": "problem_solving"},
    {"hook": "Only 1% know this secret", "category": "scarcity"},
    {"hook": "Scientists HATE this one trick", "category": "controversy"},
    {"hook": "I can't believe this is real", "category": "disbelief"},
    {"hook": "Stop scrolling, watch this", "category": "direct_appeal"},
    {"hook": "This happens to everyone", "category": "relatability"},
    {"hook": "The truth they don't want you to know", "category": "conspiracy"},
]

CONTENT_CATEGORIES = [
    {"name": "life_hacks", "topics": ["productivity", "organization", "time_saving"]},
    {"name": "psychology", "topics": ["persuasion", "focus", "memory", "motivation"]},
    {"name": "science_facts", "topics": ["physics", "biology", "space", "nature"]},
    {"name": "technology", "topics": ["smartphones", "apps", "keyboard_shortcuts"]},
    {"name": "motivation", "topics": ["success", "mindset", "habits", "goals"]},
    {"name": "finance", "topics": ["investing", "saving", "passive_income"]},
    {"name": "health_fitness", "topics": ["workouts", "nutrition", "wellness"]},
    {"name": "entertainment", "topics": ["movie_facts", "celebrity_trivia", "gaming"]},
]

@dataclass
class ColorScheme:
    name: str
    primary: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    text_primary: Tuple[int, int, int]

COLOR_SCHEMES = [
    ColorScheme("ocean_sunset", (0, 102, 204), (255, 153, 0), (255, 255, 255), (255, 255, 255)),
    ColorScheme("forest_glow", (34, 139, 34), (255, 215, 0), (240, 255, 240), (255, 255, 255)),
    ColorScheme("neon_pink", (255, 16, 240), (0, 255, 200), (255, 255, 255), (255, 255, 255)),
    ColorScheme("deep_purple", (75, 0, 130), (255, 69, 0), (255, 255, 255), (255, 255, 255)),
    ColorScheme("cyber_black", (0, 0, 0), (0, 255, 127), (255, 0, 127), (0, 255, 127)),
]

# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger():
    """Configure loguru logger"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"agent_{timestamp}.log"
    
    logger.remove()
    logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}", level="DEBUG")
    logger.add(sys.stdout, format="<level>{level: <8}</level> | {message}", level="INFO", colorize=True)
    
    return log_file

# ============================================================================
# SCRIPT GENERATOR - GROQ LLM
# ============================================================================

class ScriptGenerator:
    """Generate viral scripts using Groq API"""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not set")
        self.api_key = api_key
        self.model = "mixtral-8x7b-32768"
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        logger.info("✓ ScriptGenerator initialized")
    
    def generate(self) -> Optional[Dict]:
        """Generate viral script"""
        try:
            hook_data = random.choice(VIRAL_HOOKS)
            category_data = random.choice(CONTENT_CATEGORIES)
            topic = random.choice(category_data["topics"])
            
            hook = hook_data["hook"]
            category = category_data["name"]
            
            logger.info(f"📝 Generating: {category}/{topic} | Hook: {hook}")
            
            # Call Groq API
            prompt = f"""Create a viral YouTube Shorts script about: {topic}
Using hook: "{hook}"
Category: {category}
Duration: 5-8 seconds (spoken naturally)

Requirements:
- Hook in first 2 seconds with curiosity/emotion
- Punchy, simple language (no complex terms)
- Loop-able structure (viewers rewatch)
- Build to satisfying payoff/twist
- 20-150 words total
- Include psychological triggers

Output ONLY the script text, no explanations."""
            
            response = requests.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 200
                },
                timeout=30
            )
            
            response.raise_for_status()
            script = response.json()["choices"][0]["message"]["content"].strip()
            
            # Validate
            word_count = len(script.split())
            if 20 <= word_count <= 150:
                logger.info(f"✓ Script generated ({word_count} words)")
                return {"script": script, "hook": hook, "category": category, "topic": topic}
            else:
                logger.warning(f"⚠ Invalid word count: {word_count}")
                return None
        
        except Exception as e:
            logger.error(f"❌ Script generation failed: {e}")
            return None

# ============================================================================
# TEXT-TO-SPEECH ENGINE - EDGE-TTS
# ============================================================================

class TextToSpeechEngine:
    """Generate speech from text using edge-tts"""
    
    def __init__(self):
        self.voices = [
            "en-US-AriaNeural",
            "en-US-GuyNeural",
            "en-US-JennyNeural",
            "en-US-AmberNeural"
        ]
        logger.info("✓ TextToSpeechEngine initialized")
    
    def generate(self, script: str, output_dir: Path) -> Optional[Path]:
        """Generate audio from script"""
        try:
            rate = self._calculate_rate(script)
            voice = random.choice(self.voices)
            
            logger.info(f"🎤 TTS: voice={voice}, rate={rate}")
            
            audio_path = asyncio.run(self._generate_async(script, voice, rate, output_dir))
            
            if audio_path and Path(audio_path).exists():
                logger.info(f"✓ Audio generated: {Path(audio_path).stat().st_size / 1024:.1f} KB")
                return audio_path
            return None
        
        except Exception as e:
            logger.error(f"❌ TTS failed: {e}")
            return None
    
    async def _generate_async(self, text: str, voice: str, rate: str, output_dir: Path) -> Optional[Path]:
        """Async TTS generation"""
        try:
            output_path = output_dir / "audio.mp3"
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
            await communicate.save(str(output_path))
            return output_path
        except Exception as e:
            logger.error(f"TTS async error: {e}")
            return None
    
    def _calculate_rate(self, script: str) -> str:
        """Optimize speech rate based on script length"""
        word_count = len(script.split())
        target_duration = 6.5
        required_wps = word_count / target_duration
        default_wps = 2.2
        rate_change = ((required_wps - default_wps) / default_wps) * 100
        rate_change = max(-30, min(30, rate_change))
        return f"+{int(rate_change)}%" if rate_change > 0 else f"{int(rate_change)}%"

# ============================================================================
# VIDEO COMPOSER - MOVIEPY
# ============================================================================

class VideoComposer:
    """Compose professional vertical videos"""
    
    def __init__(self):
        self.config = VideoConfig()
        logger.info(f"✓ VideoComposer initialized: {self.config.width}x{self.config.height}")
    
    def compose(self, audio_path: Path, script: str, hook: str, output_dir: Path) -> Optional[Path]:
        """Compose video from audio and text"""
        try:
            logger.info("🎬 Composing video...")
            
            # Load audio
            audio_clip = AudioFileClip(str(audio_path))
            duration = min(audio_clip.duration, self.config.duration_max)
            
            # Create background
            colors = random.choice(COLOR_SCHEMES)
            background = ColorClip(
                size=(self.config.width, self.config.height),
                color=colors.primary,
                duration=duration
            )
            
            # Add hook text
            hook_clip = TextClip(
                hook,
                fontsize=72,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(self.config.width - 60, None),
                align='center'
            ).set_position(('center', 200)).set_duration(min(2, duration))
            
            # Add script text
            script_clip = TextClip(
                script,
                fontsize=48,
                color='white',
                font='Arial',
                method='caption',
                size=(self.config.width - 60, None),
                align='center'
            ).set_position(('center', 'center')).set_start(0.5).set_duration(max(0, duration - 0.5))
            
            # Compose
            video = CompositeVideoClip([background, hook_clip, script_clip])
            final = video.set_audio(audio_clip)
            
            # Export
            output_path = output_dir / "short.mp4"
            logger.info(f"💾 Exporting to {output_path}")
            
            final.write_videofile(
                str(output_path),
                fps=self.config.fps,
                codec=self.config.codec,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Cleanup
            background.close()
            video.close()
            final.close()
            audio_clip.close()
            
            file_size = Path(output_path).stat().st_size / (1024 * 1024)
            logger.info(f"✓ Video created: {file_size:.2f} MB")
            return output_path
        
        except Exception as e:
            logger.error(f"❌ Video composition failed: {e}")
            logger.error(traceback.format_exc())
            return None

# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class AIYouTubeShortsAgent:
    """Main orchestration engine"""
    
    def __init__(self, groq_api_key: str):
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("output") / f"run_{self.run_id}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.script_gen = ScriptGenerator(groq_api_key)
        self.tts_engine = TextToSpeechEngine()
        self.video_composer = VideoComposer()
        
        self.stats = {
            "run_id": self.run_id,
            "created": 0,
            "failed": 0,
            "errors": []
        }
        
        logger.info(f"🚀 Agent initialized - Run ID: {self.run_id}")
    
    def generate_short(self) -> Optional[Dict]:
        """Generate single YouTube Short"""
        try:
            logger.info("\n" + "="*80)
            logger.info("📹 GENERATING YOUTUBE SHORT")
            logger.info("="*80)
            
            # Step 1: Generate Script
            logger.info("\n[1/4] Generating viral script...")
            script_data = self.script_gen.generate()
            if not script_data:
                raise Exception("Script generation failed")
            
            # Step 2: Generate Audio
            logger.info("\n[2/4] Converting to speech...")
            audio_path = self.tts_engine.generate(script_data["script"], self.output_dir)
            if not audio_path:
                raise Exception("TTS failed")
            
            # Step 3: Compose Video
            logger.info("\n[3/4] Composing video...")
            video_path = self.video_composer.compose(
                audio_path=audio_path,
                script=script_data["script"],
                hook=script_data["hook"],
                output_dir=self.output_dir
            )
            if not video_path:
                raise Exception("Video composition failed")
            
            # Step 4: Save Metadata
            logger.info("\n[4/4] Saving metadata...")
            metadata = {
                "script": script_data["script"],
                "hook": script_data["hook"],
                "category": script_data["category"],
                "topic": script_data["topic"],
                "video": str(video_path),
                "generated_at": datetime.now().isoformat()
            }
            
            metadata_file = self.output_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats["created"] += 1
            logger.info("\n✅ SHORT GENERATED SUCCESSFULLY!")
            logger.info(f"📊 Video: {Path(video_path).stat().st_size / (1024*1024):.2f} MB")
            
            return metadata
        
        except Exception as e:
            logger.error(f"\n❌ GENERATION FAILED: {e}")
            logger.error(traceback.format_exc())
            self.stats["failed"] += 1
            self.stats["errors"].append(str(e))
            return None
    
    def run(self) -> bool:
        """Run full pipeline"""
        try:
            logger.info("\n" + "="*80)
            logger.info("🎬 AI YOUTUBE SHORTS AGENT - FULL PIPELINE")
            logger.info("="*80)
            
            # Generate shorts
            result = self.generate_short()
            
            # Save report
            report_path = self.output_dir / "report.json"
            with open(report_path, 'w') as f:
                json.dump(self.stats, f, indent=2)
            
            logger.info("\n" + "="*80)
            logger.info("📊 EXECUTION SUMMARY")
            logger.info("="*80)
            logger.info(f"✓ Created: {self.stats['created']}")
            logger.info(f"✗ Failed: {self.stats['failed']}")
            logger.info(f"Run ID: {self.run_id}")
            logger.info("="*80 + "\n")
            
            return self.stats["created"] > 0
        
        except Exception as e:
            logger.error(f"Fatal pipeline error: {e}")
            logger.error(traceback.format_exc())
            return False

# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        # Setup
        log_file = setup_logger()
        load_dotenv()
        
        # Create directories
        Path("output").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
        logger.info("\n" + "="*80)
        logger.info("🎬 AI YOUTUBE SHORTS AGENT")
        logger.info("="*80)
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info(f"Log file: {log_file}")
        
        # Validate API key
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            logger.error("❌ GROQ_API_KEY not set")
            logger.error("Get free API key from: https://console.groq.com")
            return 1
        
        logger.info("✓ GROQ_API_KEY configured")
        
        # Run agent
        agent = AIYouTubeShortsAgent(groq_api_key)
        success = agent.run()
        
        return 0 if success else 1
    
    except Exception as e:
        logger.critical(f"FATAL ERROR: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
