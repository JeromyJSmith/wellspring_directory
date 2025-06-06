# TTS Audio Generation Guide

## 🎯 Quick Start

Your behavioral health chapters have been processed and are ready for
text-to-speech conversion!

### 1. Install Dependencies

```bash
uv sync --extra tts
```

### 2. Test Voices (Interactive)

```bash
uv run python voice_tester.py
```

### 3. Generate Audio (Recommended - Custom British Voice)

```bash
export OPENAI_API_KEY="your_openai_key_here"
uv run python tts_audio_generator.py --service openai
```

### Alternative: Generate Audio (Free Option)

```bash
uv run python tts_audio_generator.py --service edge_tts
```

### 3. Result

- 19 high-quality MP3 files (one per chapter)
- Total audio length: ~15-20 hours
- Professional audiobook ready for listening

---

## 📁 What Was Created

### Processed Text Files

- **Location**: `tts_prepared_chapters/`
- **Format**: Clean text files optimized for TTS
- **Processing**: Removed markdown, expanded abbreviations, improved
  pronunciation

### Key Improvements Made:

✅ **Markdown Removed**: Headers, bullets, formatting stripped\
✅ **Abbreviations Expanded**: DBIA → Design-Build Institute of America (first
use)\
✅ **Pronunciation Enhanced**: "e.g." → "for example", "vs." → "versus"\
✅ **Chapter Intros Added**: "Chapter 1: Foundations" spoken introduction\
✅ **Technical Terms Preserved**: Maintains professional terminology while
improving flow

---

## 🎙️ TTS Service Options

### 1. **Edge TTS** (Recommended for most users)

- **Cost**: FREE
- **Quality**: High (Neural voices)
- **Setup**: No API keys needed
- **Best For**: Getting started quickly

```bash
uv run python tts_audio_generator.py --service edge_tts --voice en-US-JennyNeural
```

### 2. **ElevenLabs** (Highest quality)

- **Cost**: ~$22/month for 30,000 characters
- **Quality**: Exceptional (human-like)
- **Setup**: Requires API key
- **Best For**: Professional audiobooks

```bash
# Set environment variable
export ELEVENLABS_API_KEY="your_api_key_here"
uv run python tts_audio_generator.py --service elevenlabs
```

### 3. **Azure Cognitive Services**

- **Cost**: Pay-per-use (~$4 per 1M characters)
- **Quality**: Excellent (Neural voices)
- **Setup**: Requires Azure subscription
- **Best For**: Enterprise users

```bash
export AZURE_SPEECH_KEY="your_key_here"
export AZURE_SPEECH_REGION="eastus"
uv run python tts_audio_generator.py --service azure
```

### 4. **gTTS** (Basic option)

- **Cost**: FREE
- **Quality**: Basic
- **Setup**: No API keys needed
- **Best For**: Testing/prototyping

```bash
uv run python tts_audio_generator.py --service gtts
```

---

## 🎨 Voice Selection

### Professional Voices (Recommended)

- **Jenny Neural**: Clear, professional female voice
- **Guy Neural**: Authoritative male voice
- **Aria Neural**: Versatile, warm tone

### Check Available Voices

```bash
uv run python tts_audio_generator.py --list-voices
```

---

## ⚙️ Advanced Usage

### Custom Voice Selection

```bash
uv run python tts_audio_generator.py --service edge_tts --voice en-US-GuyNeural
```

### Specify Input/Output Directories

```bash
uv run python tts_audio_generator.py \
  --input tts_prepared_chapters \
  --output my_audiobook \
  --service edge_tts
```

### Process Single Chapter (for testing)

```bash
uv run python tts_audio_generator.py --service edge_tts --input tts_prepared_chapters --output test_audio
```

---

## 📊 Expected Output

### File Structure

```
tts_audio_output/
├── Chapter_01_Foundations.mp3          (~45 min)
├── Chapter_02_Strategic_Planning.mp3   (~60 min)
├── Chapter_03_Team_Assembly.mp3        (~75 min)
├── ...
├── Chapter_19_Call_to_Action.mp3       (~25 min)
└── behavioral_health_audiobook.m3u     (Playlist)
```

### Audio Specifications

- **Format**: MP3
- **Quality**: 44.1 kHz, 16-bit
- **Speaking Rate**: Optimized for technical content
- **File Size**: ~5-15 MB per chapter

---

## 🎵 Using the Generated Audio

### 1. **Playlist File**

Open `behavioral_health_audiobook.m3u` in:

- VLC Media Player
- iTunes/Apple Music
- Spotify (local files)
- Any audio player that supports M3U

### 2. **Individual Chapters**

Each MP3 file can be:

- Uploaded to audiobook apps
- Shared with team members
- Used for presentations
- Embedded in learning platforms

### 3. **Mobile Listening**

- Copy to smartphone/tablet
- Import to audiobook apps (Audible, Apple Books)
- Stream via cloud storage (Dropbox, Google Drive)

---

## 🚀 Quick Commands Cheat Sheet

```bash
# Basic generation (free, good quality)
python tts_audio_generator.py

# High-quality with ElevenLabs
export ELEVENLABS_API_KEY="sk-..."
python tts_audio_generator.py --service elevenlabs

# Different voice
python tts_audio_generator.py --voice en-US-GuyNeural

# Check available voices
python tts_audio_generator.py --list-voices

# Custom output location
python tts_audio_generator.py --output my_custom_audiobook
```

---

## 📋 Content Overview

Your audiobook covers:

1. **Foundations** - Industry overview and principles
2. **Strategic Planning** - Market research and feasibility
3. **Team Assembly** - Building expert teams
4. **Site Selection** - Location analysis and criteria
5. **Stakeholder Support** - Community engagement
6. **Community Engagement** - Public relations and advocacy
7. **Financial Planning** - Funding and budgeting strategies
8. **Design Process** - Architectural planning
9. **Design Best Practices** - Evidence-based design principles
10. **Construction Management** - Project execution
11. **Best Practices** - Industry standards and guidelines
12. **Operations Planning** - Facility management preparation
13. **Quality Metrics** - Performance measurement
14. **Technology Integration** - Modern healthcare tech
15. **Sustainability** - Environmental considerations
16. **Risk Management** - Project risk mitigation
17. **Case Studies** - Real-world examples
18. **Implementation** - Putting it all together
19. **Call to Action** - Moving forward with projects

**Total Runtime**: Approximately 15-20 hours of professional content

---

## 🎯 Next Steps

1. **Choose your TTS service** (Edge TTS recommended for first run)
2. **Run the generator** with your preferred settings
3. **Test a chapter** to ensure quality meets your needs
4. **Generate the full audiobook**
5. **Create your playlist** and start listening!

The content is now ready to be transformed into a professional audiobook that
will make this comprehensive behavioral health real estate development guide
accessible in audio format.
