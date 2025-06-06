#!/usr/bin/env python3
"""
TTS Audio Generator for Behavioral Health Chapters

This script provides multiple options for converting the prepared text files
to high-quality audio using various TTS services.

Usage:
    python tts_audio_generator.py --service [service_name] --input [input_dir] --output [output_dir]

Supported services:
    - openai (requires API key, custom British voice)
    - elevenlabs (requires API key)
    - azure (requires API key) 
    - google (requires API key)
    - amazon (requires AWS credentials)
    - edge_tts (free, built-in)
    - gTTS (free, basic)

Requirements:
    pip install elevenlabs azure-cognitiveservices-speech google-cloud-texttospeech boto3 edge-tts gTTS pydub
"""

import os
import argparse
import asyncio
from pathlib import Path
from typing import Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSAudioGenerator:
    def __init__(self, service: str, output_dir: str):
        self.service = service
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Audio settings
        self.audio_settings = {
            'sample_rate': 44100,
            'bit_depth': 16,
            'speaking_rate': 0.9,  # Slightly slower for technical content
        }
    
    async def generate_audio_openai(self, text: str, output_file: str, voice: str = "nova"):
        """Generate audio using OpenAI TTS with custom British voice"""
        try:
            from openai import AsyncOpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable required")
            
            client = AsyncOpenAI(api_key=api_key)
            
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
            
            logger.info(f"Generating audio with OpenAI TTS (British voice): {output_file}")
            
            # Generate audio
            async with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
                instructions=instructions,
                response_format="mp3"
            ) as response:
                with open(output_file, "wb") as f:
                    async for chunk in response.iter_bytes():
                        f.write(chunk)
            
            logger.info(f"Saved: {output_file}")
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise

    async def generate_audio_elevenlabs(self, text: str, output_file: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        """Generate audio using ElevenLabs API"""
        try:
            from elevenlabs import generate, save, set_api_key
            
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                raise ValueError("ELEVENLABS_API_KEY environment variable required")
            
            set_api_key(api_key)
            
            logger.info(f"Generating audio with ElevenLabs: {output_file}")
            
            # Generate audio
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save audio
            save(audio, output_file)
            logger.info(f"Saved: {output_file}")
            
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
            raise
    
    async def generate_audio_azure(self, text: str, output_file: str, voice: str = "en-US-JennyNeural"):
        """Generate audio using Azure Cognitive Services"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            # Azure credentials
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            service_region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
            
            if not speech_key:
                raise ValueError("AZURE_SPEECH_KEY environment variable required")
            
            # Configure speech service
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            speech_config.speech_synthesis_voice_name = voice
            speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
            
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            
            logger.info(f"Generating audio with Azure: {output_file}")
            
            # Generate audio
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                with open(output_file, "wb") as f:
                    f.write(result.audio_data)
                logger.info(f"Saved: {output_file}")
            else:
                logger.error(f"Azure synthesis failed: {result.reason}")
                
        except Exception as e:
            logger.error(f"Azure error: {e}")
            raise
    
    async def generate_audio_edge_tts(self, text: str, output_file: str, voice: str = "en-US-JennyNeural"):
        """Generate audio using Edge TTS (free)"""
        try:
            import edge_tts
            
            logger.info(f"Generating audio with Edge TTS: {output_file}")
            
            # Generate audio
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
            
            logger.info(f"Saved: {output_file}")
            
        except Exception as e:
            logger.error(f"Edge TTS error: {e}")
            raise
    
    def generate_audio_gtts(self, text: str, output_file: str, lang: str = "en"):
        """Generate audio using gTTS (basic, free)"""
        try:
            from gtts import gTTS
            
            logger.info(f"Generating audio with gTTS: {output_file}")
            
            # Generate audio
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_file)
            
            logger.info(f"Saved: {output_file}")
            
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            raise
    
    async def process_chapter(self, chapter_file: Path) -> bool:
        """Process a single chapter file"""
        try:
            # Read chapter content
            with open(chapter_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Create output filename
            output_filename = chapter_file.stem + '.mp3'
            output_path = self.output_dir / output_filename
            
            # Skip if already exists
            if output_path.exists():
                logger.info(f"Skipping existing file: {output_filename}")
                return True
            
            # Generate audio based on service
            if self.service == 'openai':
                await self.generate_audio_openai(text, str(output_path))
            elif self.service == 'elevenlabs':
                await self.generate_audio_elevenlabs(text, str(output_path))
            elif self.service == 'azure':
                await self.generate_audio_azure(text, str(output_path))
            elif self.service == 'edge_tts':
                await self.generate_audio_edge_tts(text, str(output_path))
            elif self.service == 'gtts':
                self.generate_audio_gtts(text, str(output_path))
            else:
                logger.error(f"Unsupported service: {self.service}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing {chapter_file.name}: {e}")
            return False
    
    async def process_all_chapters(self, input_dir: str):
        """Process all chapters in the input directory"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            logger.error(f"Input directory not found: {input_dir}")
            return
        
        # Find all chapter text files
        chapter_files = list(input_path.glob('Chapter_*.txt'))
        chapter_files.sort()
        
        if not chapter_files:
            logger.error(f"No chapter files found in {input_dir}")
            return
        
        logger.info(f"Found {len(chapter_files)} chapters to convert")
        logger.info(f"Using TTS service: {self.service}")
        
        # Process chapters
        successful = 0
        for chapter_file in chapter_files:
            if await self.process_chapter(chapter_file):
                successful += 1
        
        logger.info(f"Successfully converted {successful}/{len(chapter_files)} chapters")
        
        # Create playlist file
        self.create_playlist(chapter_files)
    
    def create_playlist(self, chapter_files: List[Path]):
        """Create an M3U playlist file"""
        playlist_content = ['#EXTM3U', '#PLAYLIST:Behavioral Health Real Estate Development', '']
        
        for chapter_file in chapter_files:
            audio_filename = chapter_file.stem + '.mp3'
            # Extract chapter info for playlist
            chapter_match = chapter_file.stem.split('_')
            if len(chapter_match) >= 3:
                chapter_num = chapter_match[1]
                chapter_title = ' '.join(chapter_match[2:]).replace('_', ' ')
                playlist_content.append(f'#EXTINF:-1,Chapter {chapter_num}: {chapter_title}')
            else:
                playlist_content.append(f'#EXTINF:-1,{chapter_file.stem}')
            
            playlist_content.append(audio_filename)
            playlist_content.append('')
        
        playlist_file = self.output_dir / 'behavioral_health_audiobook.m3u'
        with open(playlist_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(playlist_content))
        
        logger.info(f"Created playlist: {playlist_file}")

def list_available_voices():
    """List available voices for different services"""
    print("\n🎙️  Available TTS Services and Recommended Voices:\n")
    
    print("1. OpenAI TTS (Premium, Custom British Voice) ⭐ RECOMMENDED")
    print("   - nova: Cambridge-educated British woman (behavioral health expert)")
    print("   - alloy: Alternative British voice option")
    print("   - echo: Professional British voice")
    print("   Custom personality: Calm, intelligent architectural historian")
    print("")
    
    print("2. ElevenLabs (Premium, Natural)")
    print("   - Rachel: 21m00Tcm4TlvDq8ikWAM (Professional, clear)")
    print("   - Josh: TxGEqnHWrfWFTfGW9XjX (Authoritative, male)")
    print("   - Bella: EXAVITQu4vr4xnSDxMaL (Warm, female)")
    print("")
    
    print("3. Azure Cognitive Services")
    print("   - en-US-JennyNeural (Professional female)")
    print("   - en-US-GuyNeural (Professional male)")
    print("   - en-US-AriaNeural (Clear, versatile)")
    print("")
    
    print("4. Edge TTS (Free, Good Quality)")
    print("   - en-US-JennyNeural")
    print("   - en-US-GuyNeural")
    print("   - en-US-SaraNeural")
    print("")
    
    print("5. Google Text-to-Speech")
    print("   - en-US-Neural2-F (Professional female)")
    print("   - en-US-Neural2-J (Professional male)")
    print("")
    
    print("6. gTTS (Free, Basic)")
    print("   - en (English, basic quality)")
    print("")

async def main():
    parser = argparse.ArgumentParser(description='Generate audio from TTS-prepared chapters')
    parser.add_argument('--service', choices=['openai', 'elevenlabs', 'azure', 'edge_tts', 'gtts'], 
                       default='openai', help='TTS service to use')
    parser.add_argument('--input', default='tts_prepared_chapters', 
                       help='Input directory with prepared text files')
    parser.add_argument('--output', default='tts_audio_output', 
                       help='Output directory for audio files')
    parser.add_argument('--voice', help='Voice ID/name to use')
    parser.add_argument('--list-voices', action='store_true', 
                       help='List available voices and exit')
    
    args = parser.parse_args()
    
    if args.list_voices:
        list_available_voices()
        return
    
    # Create audio generator
    generator = TTSAudioGenerator(args.service, args.output)
    
    # Process all chapters
    await generator.process_all_chapters(args.input)
    
    print(f"\n✅ Audio generation complete!")
    print(f"📁 Audio files saved to: {args.output}")
    print(f"🎵 Playlist created: {args.output}/behavioral_health_audiobook.m3u")

if __name__ == "__main__":
    asyncio.run(main()) 