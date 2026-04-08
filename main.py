#!/usr/bin/env python3
"""
🎬 AI YOUTUBE SHORTS GENERATOR v4.0 - FULLY DEBUGGED
Production-Ready | GitHub Actions Debug-Ready | Fully Instrumented
"""

import os
import sys
import json
import asyncio
import random
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

print("[INIT] Python startup - importing dependencies...", flush=True)

# ============================================================================
# IMPORTS WITH DETAILED FEEDBACK
# ============================================================================

IMPORTS_STATUS = {}

def import_module(name: str, package: str) -> bool:
    """Try to import module and report status"""
    try:
        __import__(name)
        IMPORTS_STATUS[name] = "✓"
        print(f"  ✓ {name} imported", flush=True)
        return True
    except ImportError as e:
        IMPORTS_STATUS[name] = f"✗ {str(e)}"
        print(f"  ✗ {name} FAILED: {e}", flush=True)
        return False

print("\n[IMPORTS] Checking dependencies...", flush=True)

# Critical imports
if not import_module("requests", "requests"):
    sys.exit(1)
if not import_module("edge_tts", "edge-tts"):
    sys.exit(1)
if not import_module("moviepy.editor", "moviepy"):
    sys.exit(1)

# Optional imports
import_module("librosa", "librosa")
import_module("dotenv", "python-dotenv")

import requests
import edge_tts
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

try:
    import librosa
    LIBROSA_AVAILABLE = True
except:
    LIBROSA_AVAILABLE = False

try:
    from dotenv import load_dotenv
except:
    load_dotenv = None

print("\n[INIT] ✓ All critical imports successful\n", flush=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Centralized configuration"""
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920
    VIDEO_FPS = 30
    VIDEO_CODEC = "libx264"
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_DURATION_MIN = 4.5
    AUDIO_DURATION_MAX = 9.5
    SCRIPT_MIN_WORDS = 15
    SCRIPT_MAX_WORDS = 60
    OUTPUT_DIR = Path("output")
    LOG_DIR = Path("logs")
    GROQ_TIMEOUT = 30
    GROQ_MODEL = "mixtral-8x7b-32768"

# ============================================================================
# ENTERPRISE LOGGER WITH DEBUG OUTPUT
# ============================================================================

class Logger:
    """Production logger with file + console output"""
    
    def __init__(self):
        self.log_dir = Config.LOG_DIR
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"agent_{timestamp}.log"
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("ShortsAgent")
        self._log_startup()
    
    def _log_startup(self):
        """Log startup information"""
        self.info("\n" + "="*80)
        self.info("🎬 AI YOUTUBE SHORTS GENERATOR v4.0 - STARTUP")
        self.info("="*80)
        self.info(f"Timestamp: {datetime.now().isoformat()}")
        self.info(f"Log file: {self.log_file}")
        self.info(f"Python: {sys.version}")
        self.info(f"Platform: {sys.platform}")
        self.info(f"CWD: {os.getcwd()}")
        self.info(f"Output dir: {Config.OUTPUT_DIR}")
        self.info("")
        self.info("Import Status:")
        for mod, status in IMPORTS_STATUS.items():
            self.info(f"  {mod}: {status}")
        self.info("="*80 + "\n")
    
    def info(self, msg):
        self.logger.info(msg)
        print(msg, flush=True)
    
    def error(self, msg):
        self.logger.error(msg)
        print(f"ERROR: {msg}", flush=True)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
        print(f"WARNING: {msg}", flush=True)

# ============================================================================
# CONTENT LIBRARY
# ============================================================================

HOOKS = [
    "You won't believe what happened next...",
    "Wait for the twist at the end",
    "This will change your life",
    "Try not to blink",
    "The ending will shock you",
]

CATEGORIES = [
    {"name": "life_hacks", "topics": ["productivity", "organization"]},
    {"name": "psychology", "topics": ["persuasion", "focus", "memory"]},
    {"name": "science", "topics": ["physics", "biology", "space"]},
    {"name": "tech", "topics": ["smartphones", "apps"]},
    {"name": "motivation", "topics": ["success", "mindset"]},
]

COLORS = [(0, 102, 204), (34, 139, 34), (255, 16, 240), (75, 0, 130), (0, 0, 0)]
VOICES = ["en-US-AriaNeural", "en-US-GuyNeural", "en-US-JennyNeural"]

# ============================================================================
# SCRIPT GENERATOR
# ============================================================================

class ScriptGenerator:
    """Generate viral scripts with detailed logging"""
    
    def __init__(self, api_key: str, logger: Logger):
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")
        
        self.api_key = api_key
        self.logger = logger
        self.logger.info("✓ ScriptGenerator initialized")
    
    def generate(self) -> Optional[Dict]:
        """Generate script with full instrumentation"""
        try:
            hook = random.choice(HOOKS)
            category = random.choice(CATEGORIES)
            topic = random.choice(category["topics"])
            
            self.logger.info(f"📝 Category: {category['name']}, Topic: {topic}")
            self.logger.info(f"📝 Hook: {hook}")
            
            prompt = f"""Create YouTube Shorts script: {topic}
Hook: "{hook}"
Duration: 5-8 seconds
Words: 15-60
Output: Script only"""
            
            self.logger.debug(f"API Call - URL: https://api.groq.com/openai/v1/chat/completions")
            self.logger.debug(f"API Call - Model: {Config.GROQ_MODEL}")
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": Config.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=Config.GROQ_TIMEOUT
            )
            
            self.logger.debug(f"API Response - Status: {response.status_code}")
            response.raise_for_status()
            
            script = response.json()["choices"][0]["message"]["content"].strip()
            word_count = len(script.split())
            
            self.logger.info(f"✅ Script generated: {word_count} words")
            self.logger.debug(f"Script: {script[:100]}...")
            
            if Config.SCRIPT_MIN_WORDS <= word_count <= Config.SCRIPT_MAX_WORDS:
                return {
                    "script": script,
                    "hook": hook,
                    "category": category["name"],
                    "topic": topic
                }
            else:
                self.logger.error(f"❌ Invalid word count: {word_count}")
                return None
        
        except Exception as e:
            self.logger.error(f"❌ Script generation failed: {e}")
            self.logger.debug(traceback.format_exc())
            return None

# ============================================================================
# TEXT-TO-SPEECH ENGINE
# ============================================================================

class TTS:
    """Generate speech with debugging"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.logger.info("✓ TTS Engine initialized")
    
    def generate(self, script: str, output_dir: Path) -> Optional[Path]:
        """Generate audio with full logging"""
        try:
            voice = random.choice(VOICES)
            self.logger.info(f"🎤 TTS - Voice: {voice}")
            
            audio_path = asyncio.run(self._generate(script, voice, output_dir))
            
            if audio_path and audio_path.exists():
                size = audio_path.stat().st_size / 1024
                self.logger.info(f"✅ Audio generated: {size:.1f} KB")
                self.logger.debug(f"Audio path: {audio_path}")
                return audio_path
            
            self.logger.error("❌ Audio file not created")
            return None
        
        except Exception as e:
            self.logger.error(f"❌ TTS failed: {e}")
            self.logger.debug(traceback.format_exc())
            return None
    
    async def _generate(self, text: str, voice: str, output_dir: Path) -> Optional[Path]:
        """Async TTS"""
        try:
            output_path = output_dir / "audio.mp3"
            self.logger.debug(f"Generating audio to: {output_path}")
            
            communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%")
            await communicate.save(str(output_path))
            
            self.logger.debug("Audio generation complete")
            return output_path
        except Exception as e:
            self.logger.error(f"❌ Async TTS failed: {e}")
            return None

# ============================================================================
# VIDEO COMPOSER
# ============================================================================

class VideoComposer:
    """Compose videos with extensive logging"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.logger.info(f"✓ VideoComposer initialized: {Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}")
    
    def compose(self, audio_path: Path, script: str, hook: str, output_dir: Path) -> Optional[Path]:
        """Compose video with full instrumentation"""
        audio_clip = None
        background = None
        final = None
        
        try:
            self.logger.info("🎬 Starting video composition")
            
            # Load audio
            self.logger.debug(f"Loading audio: {audio_path}")
            audio_clip = AudioFileClip(str(audio_path))
            duration = audio_clip.duration
            self.logger.info(f"Audio duration: {duration:.2f}s")
            
            # Create background
            color = random.choice(COLORS)
            self.logger.debug(f"Background color: {color}")
            background = ColorClip(
                size=(Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT),
                color=color,
                duration=duration
            )
            self.logger.info("✓ Background created")
            
            # Add text
            clips = [background]
            try:
                hook_clip = TextClip(
                    hook,
                    fontsize=72,
                    color='white',
                    method='caption',
                    size=(Config.VIDEO_WIDTH - 60, None),
                    align='center'
                ).set_position(('center', 200)).set_duration(min(2, duration))
                clips.append(hook_clip)
                self.logger.info("✓ Hook text added")
            except Exception as e:
                self.logger.warning(f"⚠️  Hook text failed: {e}")
            
            try:
                script_clip = TextClip(
                    script,
                    fontsize=48,
                    color='white',
                    method='caption',
                    size=(Config.VIDEO_WIDTH - 60, None),
                    align='center'
                ).set_position(('center', 'center')).set_start(0.5).set_duration(max(0, duration - 0.5))
                clips.append(script_clip)
                self.logger.info("✓ Script text added")
            except Exception as e:
                self.logger.warning(f"⚠️  Script text failed: {e}")
            
            # Compose
            video = CompositeVideoClip(clips)
            final = video.set_audio(audio_clip)
            
            # Export
            output_path = output_dir / "short.mp4"
            self.logger.info(f"💾 Exporting to: {output_path}")
            
            final.write_videofile(
                str(output_path),
                fps=Config.VIDEO_FPS,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            if output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                self.logger.info(f"✅ Video created: {size_mb:.2f} MB")
                self.logger.debug(f"Video path: {output_path}")
                return output_path
            else:
                self.logger.error("❌ Video file not created after export")
                return None
        
        except Exception as e:
            self.logger.error(f"❌ Video composition failed: {e}")
            self.logger.debug(traceback.format_exc())
            return None
        
        finally:
            # Cleanup
            self.logger.debug("Cleaning up resources")
            for clip in [audio_clip, background, final]:
                if clip:
                    try:
                        clip.close()
                    except:
                        pass

# ============================================================================
# MAIN AGENT
# ============================================================================

class Agent:
    """Main orchestrator"""
    
    def __init__(self, groq_key: str, logger: Logger):
        self.groq_key = groq_key
        self.logger = logger
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Config.OUTPUT_DIR / f"run_{self.run_id}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Agent run ID: {self.run_id}")
        self.logger.info(f"Output directory: {self.output_dir}")
        
        self.script_gen = ScriptGenerator(groq_key, logger)
        self.tts = TTS(logger)
        self.video = VideoComposer(logger)
        
        self.stats = {"created": 0, "failed": 0, "errors": []}
    
    def generate(self) -> Optional[Dict]:
        """Generate single short"""
        try:
            self.logger.info("\n" + "="*80)
            self.logger.info("📹 GENERATING YOUTUBE SHORT")
            self.logger.info("="*80)
            
            # Script
            self.logger.info("[1/4] Script generation...")
            script_data = self.script_gen.generate()
            if not script_data:
                raise Exception("Script generation failed")
            
            # Audio
            self.logger.info("[2/4] TTS conversion...")
            audio_path = self.tts.generate(script_data["script"], self.output_dir)
            if not audio_path:
                raise Exception("TTS failed")
            
            # Video
            self.logger.info("[3/4] Video composition...")
            video_path = self.video.compose(
                audio_path=audio_path,
                script=script_data["script"],
                hook=script_data["hook"],
                output_dir=self.output_dir
            )
            if not video_path:
                raise Exception("Video composition failed")
            
            # Metadata
            self.logger.info("[4/4] Saving metadata...")
            metadata = {
                "script": script_data["script"],
                "hook": script_data["hook"],
                "category": script_data["category"],
                "generated_at": datetime.now().isoformat(),
                "video_file": str(video_path.relative_to(Config.OUTPUT_DIR))
            }
            
            metadata_file = self.output_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"✓ Metadata saved: {metadata_file}")
            
            self.stats["created"] += 1
            self.logger.info("\n✅ SHORT GENERATED SUCCESSFULLY!")
            
            return metadata
        
        except Exception as e:
            self.logger.error(f"\n❌ GENERATION FAILED: {e}")
            self.logger.debug(traceback.format_exc())
            self.stats["failed"] += 1
            self.stats["errors"].append(str(e))
            return None
    
    def run(self) -> bool:
        """Run complete pipeline"""
        try:
            self.logger.info("\n" + "█"*80)
            self.logger.info("█  🎬 STARTING PIPELINE")
            self.logger.info("█"*80)
            
            result = self.generate()
            
            # Save report
            report_path = self.output_dir / "report.json"
            self.stats["output_dir"] = str(self.output_dir)
            with open(report_path, 'w') as f:
                json.dump(self.stats, f, indent=2)
            
            self.logger.info(f"\n✓ Report saved: {report_path}")
            
            # Summary
            self.logger.info("\n" + "█"*80)
            self.logger.info("█  📊 EXECUTION SUMMARY")
            self.logger.info("█"*80)
            self.logger.info(f"█  Created: {self.stats['created']}")
            self.logger.info(f"█  Failed: {self.stats['failed']}")
            self.logger.info(f"█  Output: {self.output_dir}")
            self.logger.info("█"*80 + "\n")
            
            # Verify files exist
            self.logger.info("✓ Verifying output files...")
            mp4_files = list(self.output_dir.glob("*.mp4"))
            json_files = list(self.output_dir.glob("*.json"))
            self.logger.info(f"  MP4 files: {len(mp4_files)}")
            self.logger.info(f"  JSON files: {len(json_files)}")
            
            return self.stats["created"] > 0
        
        except Exception as e:
            self.logger.error(f"❌ FATAL: {e}")
            self.logger.debug(traceback.format_exc())
            return False

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Entry point with full debugging"""
    exit_code = 1
    
    try:
        # Setup
        print("[MAIN] Initializing logger...", flush=True)
        logger = Logger()
        
        # Create directories
        Config.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        Config.LOG_DIR.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"✓ Output directory: {Config.OUTPUT_DIR}")
        logger.info(f"✓ Log directory: {Config.LOG_DIR}")
        
        # Load env
        if load_dotenv:
            logger.info("Loading .env file...")
            load_dotenv()
        
        # Get API key
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            logger.error("GROQ_API_KEY not found in environment")
            logger.error("Set it via: export GROQ_API_KEY='your-key'")
            logger.error("Or in .env file")
            return 1
        
        logger.info("✓ GROQ_API_KEY loaded")
        logger.info("✓ All systems ready\n")
        
        # Run agent
        agent = Agent(groq_key, logger)
        success = agent.run()
        
        exit_code = 0 if success else 1
    
    except Exception as e:
        logging.critical(f"CRITICAL ERROR: {e}")
        logging.error(traceback.format_exc())
        exit_code = 1
    
    finally:
        print(f"\n[MAIN] Exiting with code: {exit_code}", flush=True)
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
