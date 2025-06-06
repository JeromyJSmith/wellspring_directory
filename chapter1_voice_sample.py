#!/usr/bin/env python3
"""
Chapter 1 Voice Sample Generator
Generate a sample audio from the first chapter using OpenAI TTS with custom British voice
"""

import asyncio
import os
import sys
from pathlib import Path
from openai import AsyncOpenAI

async def generate_chapter1_sample():
    """Generate a voice sample from Chapter 1"""
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Please set your OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your_key_here'")
        return False
    
    # Read Chapter 1 content
    chapter_file = Path("tts_prepared_chapters/Chapter_01_Foundations.txt")
    if not chapter_file.exists():
        print(f"❌ Chapter file not found: {chapter_file}")
        return False
    
    with open(chapter_file, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    # Extract a meaningful sample (first few sections)
    sample_text = """Chapter 1: Foundations of Behavioral Health Real Estate Development

"The greatest wealth is health." – Virgil

Understanding the Urgent Demand for Behavioral Health Facilities

Across the United States and especially in California, mental health and substance use crises have reached historic highs. The lack of adequate infrastructure to meet these needs has left vulnerable populations underserved and communities strained.

In this landscape, the integration of behavioral health and real estate development has become more than a niche concern; it is a public necessity.

A behavioral health facility is not merely a space for treatment; it is a living, breathing part of the healing process. Its design, location, accessibility, and functionality can make the difference between a successful recovery and a missed opportunity for care.

When thoughtfully executed, these facilities become sanctuaries for healing, engines for community health, and assets for long-term public well-being.

California, long at the forefront of innovation, diversity, and population growth, is uniquely positioned to redefine how these facilities are imagined and delivered. As demand for behavioral health care rises, so too must our ability to deliver environments that foster dignity, empower recovery, and meet urgent needs with timely, strategic precision."""
    
    # Custom British voice instructions
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
        client = AsyncOpenAI(api_key=api_key)
        
        print("🎙️ Generating Chapter 1 voice sample...")
        print(f"📝 Sample length: ~{len(sample_text.split())} words (~2-3 minutes)")
        print("🇬🇧 Using custom British voice (Cambridge-educated architectural historian)")
        
        # Generate audio
        output_file = "Chapter_01_Voice_Sample.mp3"
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="nova",
            input=sample_text,
            instructions=instructions,
            response_format="mp3"
        ) as response:
            with open(output_file, "wb") as f:
                async for chunk in response.iter_bytes():
                    f.write(chunk)
        
        print(f"✅ Sample generated successfully!")
        print(f"🔊 File saved as: {output_file}")
        print(f"📏 File size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
        # Try to play automatically on macOS
        import platform
        import subprocess
        if platform.system() == "Darwin":
            try:
                print("🎵 Playing sample...")
                subprocess.run(["afplay", output_file], check=True)
            except:
                print("💡 To play manually: open Chapter_01_Voice_Sample.mp3")
        else:
            print(f"💡 To play manually: {output_file}")
        
        print("\n" + "="*60)
        print("🎯 VOICE SAMPLE EVALUATION")
        print("="*60)
        print("Listen for these British voice characteristics:")
        print("✓ Cambridge-educated, professional tone")
        print("✓ Standard Received Pronunciation (RP)")
        print("✓ British pronunciations: 'PRO-ject', 'PRO-cess'")
        print("✓ Warm, nurturing delivery with intellectual authority")
        print("✓ Natural pacing with thoughtful pauses")
        print("\nIf you like this voice, generate the full audiobook with:")
        print("uv run python tts_audio_generator.py --service openai --voice nova")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating sample: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(generate_chapter1_sample())
    if success:
        print("\n🎧 Enjoy your Chapter 1 voice sample!")
    else:
        print("\n❌ Sample generation failed. Please check your setup and try again.") 