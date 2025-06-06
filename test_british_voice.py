#!/usr/bin/env python3
"""
Test script for OpenAI TTS with custom British voice
"""

import asyncio
import os
from openai import AsyncOpenAI

async def test_british_voice():
    """Test the OpenAI TTS with custom British voice instructions"""
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Please set your OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your_key_here'")
        return
    
    client = AsyncOpenAI(api_key=api_key)
    
    # Sample text from your chapters
    sample_text = """The foundation of any successful behavioural health real estate project is a clear understanding of community demand. Objective, data-driven market research and needs assessments transform vague intentions into strategic, actionable plans grounded in local realities."""
    
    # Your custom British voice instructions
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

    try:
        print("🎙️ Generating sample audio with custom British voice...")
        
        # Generate audio
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="nova",
            input=sample_text,
            instructions=instructions,
            response_format="mp3"
        ) as response:
            with open("british_voice_test.mp3", "wb") as f:
                async for chunk in response.iter_bytes():
                    f.write(chunk)
        
        print("✅ Audio generated successfully!")
        print("🔊 File saved as: british_voice_test.mp3")
        print("🎧 Play the file to hear your custom British voice!")
        
        # Try to play automatically on macOS
        import platform
        import subprocess
        if platform.system() == "Darwin":
            try:
                subprocess.run(["afplay", "british_voice_test.mp3"], check=True)
                print("🎵 Playing audio...")
            except:
                pass
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_british_voice()) 