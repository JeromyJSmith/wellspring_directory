#!/usr/bin/env python3
"""
Voice Testing Tool for TTS Services

This tool lets you test different voices with sample text from your chapters
before deciding which voice to use for the full audiobook generation.

Usage:
    python voice_tester.py
"""

import os
import asyncio
import tempfile
import platform
import subprocess
from pathlib import Path
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceTester:
    def __init__(self):
        # Sample text from your chapters for testing
        self.sample_texts = {
            "short": "The foundation of any successful behavioral health real estate project is a clear understanding of community demand.",
            
            "medium": """The foundation of any successful behavioral health real estate project is a clear understanding of community demand. Objective, data-driven market research and needs assessments transform vague intentions into strategic, actionable plans grounded in local realities. These facilities become sanctuaries for healing, engines for community health, and assets for long-term public well-being.""",
            
            "technical": """Behavioral health projects operate within a dense web of rules, standards, and shifting policy priorities. Success depends on anticipating these constraints early and embedding them into the design and planning process. Key regulatory concerns include licensing requirements from state agencies like the Department of Health Care Services and Office of Statewide Health Planning and Development."""
        }
        
        # Available voices for each service
        self.voices = {
            "openai": {
                "Cambridge British Expert (RECOMMENDED)": "nova",
                "Alternative British Voice": "alloy",
                "Professional British Voice": "echo"
            },
            "edge_tts": {
                "Jenny (Professional Female)": "en-US-JennyNeural",
                "Guy (Professional Male)": "en-US-GuyNeural", 
                "Sara (Clear Female)": "en-US-SaraNeural",
                "Davis (Authoritative Male)": "en-US-DavisNeural",
                "Aria (Warm Female)": "en-US-AriaNeural",
                "Jason (Confident Male)": "en-US-JasonNeural",
                "Nancy (Business Female)": "en-US-NancyNeural",
                "Tony (Business Male)": "en-US-TonyNeural"
            },
            "gtts": {
                "Standard English": "en"
            }
        }
        
        self.temp_dir = Path(tempfile.gettempdir()) / "voice_tests"
        self.temp_dir.mkdir(exist_ok=True)
    
    def play_audio(self, audio_file: str):
        """Play audio file using system default player"""
        try:
            system = platform.system().lower()
            if system == "darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            elif system == "linux":
                subprocess.run(["aplay", audio_file], check=True)
            elif system == "windows":
                subprocess.run(["start", audio_file], shell=True, check=True)
            else:
                logger.warning(f"Unsupported platform: {system}")
                print(f"Please manually play: {audio_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error playing audio: {e}")
            print(f"Could not play audio automatically. File saved at: {audio_file}")
        except FileNotFoundError:
            logger.error("Audio player not found")
            print(f"Audio file created at: {audio_file}")
    
    async def test_openai_voice(self, voice_id: str, text: str) -> str:
        """Generate sample audio with OpenAI TTS"""
        try:
            from openai import AsyncOpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("❌ OPENAI_API_KEY environment variable required for OpenAI TTS")
                return None
            
            client = AsyncOpenAI(api_key=api_key)
            output_file = self.temp_dir / f"openai_test_{voice_id}.mp3"
            
            # Custom British voice instructions for behavioral health content
            instructions = """Affect/Personality:
A well-educated young British woman with a calm, confident demeanor — imagine a Cambridge-educated architectural historian who now works in sustainable real estate development. She's friendly, insightful, and deeply believes in the social value of her work.

Tone:
Elegant and composed with a natural warmth. Think of someone who can guide you through complex topics while making you feel gently supported — as if you were sitting beside her in a sunlit room with a cup of tea. She speaks with precision, but never comes across as rigid or formal.

Pronunciation:
Standard Received Pronunciation (RP), with clearly articulated consonants and melodic vowel inflections. Avoid overly posh or theatrical British stereotypes. Use crisp articulation for phrases like:
• "community alignment"
• "feasibility analysis" 
• "clinical integration"
Words like project, process, and data should be pronounced in the British style ("PRO-ject", "PRO-cess", "DAH-tuh"). Avoid Americanisms.

Emotion:
Calm, intelligent, and nurturing. She's enthusiastic about behavioral health real estate as a force for good — not flashy, but deeply rooted in purpose. She evokes trust and curiosity, as if she's mentoring the listener into a more thoughtful worldview. Occasionally, a soft smile can be heard through her voice, especially when describing the human side of planning."""
            
            logger.info(f"Generating sample with OpenAI {voice_id}...")
            
            # Generate audio
            async with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice_id,
                input=text,
                instructions=instructions,
                response_format="mp3"
            ) as response:
                with open(output_file, "wb") as f:
                    async for chunk in response.iter_bytes():
                        f.write(chunk)
            
            return str(output_file)
            
        except ImportError:
            logger.error("openai not installed. Run: pip install openai")
            return None
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return None

    async def test_edge_voice(self, voice_id: str, text: str) -> str:
        """Generate sample audio with Edge TTS"""
        try:
            import edge_tts
            
            output_file = self.temp_dir / f"edge_test_{voice_id.replace('-', '_')}.mp3"
            
            logger.info(f"Generating sample with {voice_id}...")
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(str(output_file))
            
            return str(output_file)
            
        except ImportError:
            logger.error("edge-tts not installed. Run: pip install edge-tts")
            return None
        except Exception as e:
            logger.error(f"Edge TTS error: {e}")
            return None
    
    def test_gtts_voice(self, lang: str, text: str) -> str:
        """Generate sample audio with gTTS"""
        try:
            from gtts import gTTS
            
            output_file = self.temp_dir / f"gtts_test_{lang}.mp3"
            
            logger.info(f"Generating sample with gTTS ({lang})...")
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(output_file))
            
            return str(output_file)
            
        except ImportError:
            logger.error("gTTS not installed. Run: pip install gTTS")
            return None
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            return None
    
    async def test_voice_interactive(self, service: str, voice_name: str, voice_id: str, text: str):
        """Test a voice and play the sample"""
        print(f"\n🎙️  Testing: {voice_name} ({service})")
        print(f"📝 Sample text: {text[:100]}...")
        
        # Generate audio
        if service == "openai":
            audio_file = await self.test_openai_voice(voice_id, text)
        elif service == "edge_tts":
            audio_file = await self.test_edge_voice(voice_id, text)
        elif service == "gtts":
            audio_file = self.test_gtts_voice(voice_id, text)
        else:
            print(f"❌ Service {service} not implemented for testing")
            return
        
        if audio_file and Path(audio_file).exists():
            print(f"🔊 Playing sample...")
            self.play_audio(audio_file)
            
            # Get user feedback
            while True:
                choice = input("\n👍 Rate this voice (1-5, 's' for skip, 'r' for replay): ").strip().lower()
                if choice in ['1', '2', '3', '4', '5']:
                    rating = int(choice)
                    if rating >= 4:
                        print(f"✅ Great choice! Voice: {voice_name} (ID: {voice_id})")
                        return {"name": voice_name, "id": voice_id, "service": service, "rating": rating}
                    else:
                        print("📝 Noted. Let's try another voice.")
                        break
                elif choice == 's':
                    print("⏭️  Skipping this voice...")
                    break
                elif choice == 'r':
                    print("🔄 Replaying...")
                    self.play_audio(audio_file)
                else:
                    print("❓ Please enter 1-5, 's' to skip, or 'r' to replay")
        else:
            print("❌ Could not generate audio sample")
        
        return None
    
    async def run_voice_testing(self):
        """Interactive voice testing session"""
        print("🎯 Voice Testing for Behavioral Health Audiobook")
        print("=" * 60)
        
        # Choose sample text
        print("\n📝 Choose sample text type:")
        print("1. Short sentence (quick test)")
        print("2. Medium paragraph (balanced)")
        print("3. Technical content (full test)")
        
        while True:
            text_choice = input("\nEnter choice (1-3): ").strip()
            if text_choice == "1":
                sample_text = self.sample_texts["short"]
                break
            elif text_choice == "2":
                sample_text = self.sample_texts["medium"]
                break
            elif text_choice == "3":
                sample_text = self.sample_texts["technical"]
                break
            else:
                print("Please enter 1, 2, or 3")
        
        print(f"\n📄 Using sample text:\n\"{sample_text[:150]}{'...' if len(sample_text) > 150 else ''}\"")
        
        # Choose service
        print(f"\n🛠️  Available TTS Services:")
        print("1. OpenAI TTS (Premium, Custom British Voice) - ⭐ RECOMMENDED")
        print("2. Edge TTS (Free, High Quality)")
        print("3. gTTS (Free, Basic Quality)")
        print("4. Test All Services")
        
        while True:
            service_choice = input("\nEnter choice (1-4): ").strip()
            if service_choice in ["1", "2", "3", "4"]:
                break
            print("Please enter 1, 2, 3, or 4")
        
        recommended_voices = []
        
        # Test OpenAI TTS voices
        if service_choice in ["1", "4"]:
            print(f"\n🎙️  Testing OpenAI TTS Voices (Custom British)...")
            print("=" * 50)
            
            for voice_name, voice_id in self.voices["openai"].items():
                result = await self.test_voice_interactive("openai", voice_name, voice_id, sample_text)
                if result:
                    recommended_voices.append(result)
                
                # Ask if user wants to continue
                if len(recommended_voices) > 0:
                    continue_choice = input(f"\n🤔 Found {len(recommended_voices)} good voice(s). Continue testing? (y/n): ").strip().lower()
                    if continue_choice == 'n':
                        break
        
        # Test Edge TTS voices
        if service_choice in ["2", "4"] and len(recommended_voices) == 0:
            print(f"\n🎙️  Testing Edge TTS Voices...")
            print("=" * 40)
            
            for voice_name, voice_id in self.voices["edge_tts"].items():
                result = await self.test_voice_interactive("edge_tts", voice_name, voice_id, sample_text)
                if result:
                    recommended_voices.append(result)
                
                # Ask if user wants to continue
                if len(recommended_voices) > 0:
                    continue_choice = input(f"\n🤔 Found {len(recommended_voices)} good voice(s). Continue testing? (y/n): ").strip().lower()
                    if continue_choice == 'n':
                        break
        
        # Test gTTS if selected
        if service_choice in ["3", "4"] and len(recommended_voices) == 0:
            print(f"\n🎙️  Testing gTTS...")
            print("=" * 40)
            
            for voice_name, voice_id in self.voices["gtts"].items():
                result = await self.test_voice_interactive("gtts", voice_name, voice_id, sample_text)
                if result:
                    recommended_voices.append(result)
        
        # Show recommendations
        print(f"\n🎯 Voice Testing Complete!")
        print("=" * 60)
        
        if recommended_voices:
            print(f"✅ Your recommended voices (rated 4+ stars):")
            for i, voice in enumerate(recommended_voices, 1):
                print(f"{i}. {voice['name']} ({voice['service']}) - Rating: {voice['rating']}/5")
                print(f"   Command: python tts_audio_generator.py --service {voice['service']} --voice {voice['id']}")
        else:
            print("📝 No voices rated 4+ stars. You can still use any voice with the generator:")
            print("   python tts_audio_generator.py --service edge_tts --voice en-US-JennyNeural")
        
        # Generate full audiobook option
        if recommended_voices:
            print(f"\n🚀 Ready to generate your audiobook?")
            best_voice = recommended_voices[0]  # Highest rated
            
            generate_choice = input(f"Generate full audiobook with {best_voice['name']}? (y/n): ").strip().lower()
            if generate_choice == 'y':
                print(f"\n🎬 Generating full audiobook...")
                print(f"Command: python tts_audio_generator.py --service {best_voice['service']} --voice {best_voice['id']}")
                
                # Actually run the generator
                try:
                    from tts_audio_generator import TTSAudioGenerator
                    generator = TTSAudioGenerator(best_voice['service'], 'tts_audio_output')
                    await generator.process_all_chapters('tts_prepared_chapters')
                    print(f"✅ Audiobook generation complete!")
                except Exception as e:
                    logger.error(f"Error generating audiobook: {e}")
                    print(f"❌ Error occurred. Please run manually:")
                    print(f"python tts_audio_generator.py --service {best_voice['service']} --voice {best_voice['id']}")
        
        # Cleanup temp files
        self.cleanup_temp_files()
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file in self.temp_dir.glob("*.mp3"):
                file.unlink()
            print(f"\n🧹 Cleaned up temporary test files")
        except Exception as e:
            logger.warning(f"Could not clean temp files: {e}")

def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import openai
    except ImportError:
        missing.append("openai")
    
    try:
        import edge_tts
    except ImportError:
        missing.append("edge-tts")
    
    try:
        import gtts
    except ImportError:
        missing.append("gTTS")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print(f"Install with: uv sync --extra tts")
        return False
    
    return True

async def main():
    """Main function"""
    print("🎙️  TTS Voice Testing Tool")
    print("=" * 60)
    
    if not check_dependencies():
        return
    
    tester = VoiceTester()
    await tester.run_voice_testing()

if __name__ == "__main__":
    asyncio.run(main()) 