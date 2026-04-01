# SmartCore AI - Complete Setup Guide

## Overview

This repo contains the **SmartCore Voice Agent** (Pipecat + Gemini Flash 2.0).
Your full SmartCore AI stack consists of three systems:

| System | URL | Purpose |
|--------|-----|---------|
| Botpress Chatbot | http://localhost:3000 | Text chat AI assistant |
| n8n Social Media Creator | http://localhost:5678 | Auto-posts to 7 platforms 2x/day |
| Voice Agent (this repo) | http://localhost:7860 | Voice AI using Gemini Flash 2.0 |

---

## Step 1: Get Your API Keys

### 1a. Google API Key (FREE - used by both Voice Agent AND n8n)
1. Go to https://aistudio.google.com
2. Click "Get API key" → "Create API key"
3. Copy the key (starts with AIza...)

### 1b. Deepgram API Key (FREE tier - for voice speech-to-text)
1. Go to https://deepgram.com → Sign up free
2. Go to Dashboard → API Keys → Create API Key
3. Copy the key

### 1c. Cartesia API Key (for voice text-to-speech)
1. Go to https://cartesia.ai → Sign up
2. Go to Settings → API Keys → Create Key
3. Copy the key

### 1d. Daily.co API Key (FREE tier - for WebRTC voice transport)
1. Go to https://dashboard.daily.co → Sign up free
2. Go to Developers → API Keys → Copy key
3. Create a room: Rooms → Create Room → Copy the room URL

### 1e. Social Media Platform Tokens (for n8n posting)
You need API tokens/credentials for each platform you want to use:
- **Instagram**: Meta Developer App → Instagram Basic Display API token
- **X (Twitter)**: developer.twitter.com → App → Bearer Token
- **LinkedIn**: LinkedIn Developer App → OAuth 2.0 Access Token
- **Facebook**: Meta Developer App → Page Access Token
- **TikTok**: developers.tiktok.com → App → Access Token
- **YouTube**: Google Cloud Console → YouTube Data API v3 → API Key
- **Snapchat**: developers.snap.com → App → Token

---

## Step 2: Set Up Voice Agent (Docker)

```bash
# 1. Clone this repo
git clone https://github.com/henrikboee/smartcore-voice-agent.git
cd smartcore-voice-agent

# 2. Copy and fill in your API keys
cp .env.example .env
# Edit .env with your actual keys:
#   GOOGLE_API_KEY=AIza...
#   DEEPGRAM_API_KEY=...
#   CARTESIA_API_KEY=...
#   DAILY_API_KEY=...
#   DAILY_ROOM_URL=https://your-domain.daily.co/your-room

# 3. Build and run with Docker
docker-compose up --build -d

# 4. Check it's running
docker-compose logs -f
```

---

## Step 3: Configure n8n Social Media Workflow

1. Log in to n8n at http://localhost:5678
2. Open the "Social Media Creator – Gemini Flash 2.0" workflow
3. Click on the "Gemini Flash 2.0 Generate Content" node
4. Expand the x-goog-api-key header → replace the value with your Google API key
5. For each social platform node (Instagram, X, LinkedIn, etc.):
   - Click the node → find the Authorization header
   - Replace the placeholder with your platform token
6. Click "Publish" (top right) to activate the workflow
7. It will automatically post at 9 AM EST and 6 PM EST daily

### n8n Environment Variable Method (alternative)
Instead of hardcoding keys in nodes, you can set them as environment variables in n8n's Docker compose:
```yaml
environment:
  - GOOGLE_API_KEY=your_key_here
```
Then use `{{ $env.GOOGLE_API_KEY }}` in node expressions.

---

## Step 4: Botpress Chatbot

Botpress is already set up at http://localhost:3000
- Bot name: SmartCore AI Chatbot
- Status: Ready (trained)
- To access: Log in → Go to Studio → SmartCore AI Chatbot

---

## Posting Schedule

The n8n workflow posts automatically at:
- **9:00 AM EST** (2:00 PM UTC) — peak US morning + EU afternoon
- **6:00 PM EST** (11:00 PM UTC) — peak US evening + EU night

Content is generated fresh by Gemini Flash 2.0 for each platform.
