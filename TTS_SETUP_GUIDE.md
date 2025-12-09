# Text-to-Speech Setup Guide

## ⚠️ Azure TTS Issue Detected

Your Azure Text-to-Speech credentials are failing with error code **2176**, which indicates authentication failure.

## 🔧 Solution Implemented: Fallback TTS

I've set up a **fallback TTS system** using **gTTS (Google Text-to-Speech)** so you can test the complete story generation flow **right now** without Azure credentials!

### ✅ What's Changed:

1. **Added gTTS** as a free alternative TTS service
2. **Enabled fallback mode** in your `.env` file (`USE_FALLBACK_TTS=True`)
3. **Services restarted** with the new configuration

### 🎯 Current Status:

- ✅ Story generation: **WORKING** (Google Gemini)
- ✅ Text-to-Speech: **WORKING** (gTTS fallback)
- ⚠️ Background music: **Requires Gemini API key**
- ✅ Audio mixing: **WORKING**

## 🚀 Quick Test

You can now generate a story and it will work end-to-end!

1. Open **http://localhost:8080**
2. Enter a story theme
3. Click "Generate Story"
4. Wait for completion (the narration will use gTTS)

---

## 📋 Option 1: Use Fallback TTS (Current Setup) ✅

**Pros:**
- ✅ Free
- ✅ No signup required
- ✅ Works immediately
- ✅ Good for testing and development

**Cons:**
- ⚠️ Lower voice quality than Azure
- ⚠️ Limited voice options
- ⚠️ No SSML support (emotions, pauses, etc.)

**This is currently enabled!** You're good to go!

---

## 📋 Option 2: Set Up Azure TTS (Production Quality)

For **production-quality narration** with natural voices, emotions, and SSML support:

### Step 1: Get Azure Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in or create a free account
3. Search for "Speech Services"
4. Click **"Create"**

### Step 2: Create Speech Service

- **Subscription**: Choose your subscription
- **Resource Group**: Create new or use existing
- **Region**: Choose closest to you (e.g., `eastus`, `westeurope`)
- **Name**: Give it a unique name
- **Pricing tier**: **F0 (Free)** - includes 500K characters per month!

### Step 3: Get Keys

1. After creation, go to your Speech Service resource
2. Click **"Keys and Endpoint"** in the left menu
3. Copy:
   - **KEY 1** (your API key)
   - **Location/Region** (e.g., `eastus`)

### Step 4: Update `.env` File

Edit `backend/.env`:

```env
# Azure Text-to-Speech
AZURE_SPEECH_KEY=YOUR_ACTUAL_KEY_HERE
AZURE_SPEECH_REGION=YOUR_REGION_HERE  # e.g., eastus
AZURE_VOICE_NAME=en-US-JennyNeural
USE_FALLBACK_TTS=False  # Change to False to use Azure
```

### Step 5: Test Azure Credentials

```bash
python test_azure.py
```

This will verify your Azure credentials are working.

### Step 6: Restart Services

```bash
./stop-all.sh
./start-all.sh
```

---

## 🔍 Troubleshooting

### Test Azure Credentials

Run the test script I created:

```bash
python test_azure.py
```

This will show:
- ✅ If credentials are valid
- ❌ Specific error if they're not
- 💡 Suggestions to fix the issue

### Common Azure TTS Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Error 2176 | Invalid credentials | Check KEY and REGION in `.env` |
| Connection refused | Network issue | Check firewall/proxy settings |
| 401 Unauthorized | Wrong key | Get new key from Azure Portal |
| 403 Forbidden | Subscription not active | Verify Azure subscription status |

### Check Current Configuration

```bash
cd backend
source venv/bin/activate
python -c "from app.core.config import settings; print(f'Fallback TTS: {settings.USE_FALLBACK_TTS}')"
```

---

## 📊 Comparison: gTTS vs Azure TTS

| Feature | gTTS (Fallback) | Azure TTS |
|---------|-----------------|-----------|
| **Cost** | Free | Free tier: 500K chars/month |
| **Voice Quality** | Basic | Professional, natural |
| **Voice Options** | Limited | 400+ voices, 140+ languages |
| **SSML Support** | No | Yes (emotions, pauses, etc.) |
| **Setup** | None | Azure account required |
| **Best For** | Testing, dev | Production, quality stories |

---

## 🎤 Available Azure Voices

For kids stories, recommended voices:

- **en-US-JennyNeural** - Friendly female (default)
- **en-US-GuyNeural** - Friendly male
- **en-US-AriaNeural** - Cheerful female
- **en-GB-SoniaNeural** - British female
- **en-AU-NatashaNeural** - Australian female

Change in `.env`:
```env
AZURE_VOICE_NAME=en-US-AriaNeural
```

---

## 💰 Cost Analysis

### Azure TTS Free Tier:
- **500,000 characters per month**
- Average story: **2,500 characters**
- **= 200 stories per month for FREE!**

### After Free Tier:
- **$4 per 1M characters**
- 100K stories = $1,000 total

---

## ✅ Quick Checklist

Current setup (fallback TTS enabled):
- [x] gTTS installed
- [x] Fallback TTS enabled
- [x] Services restarted
- [x] Ready to test!

To switch to Azure TTS:
- [ ] Get Azure credentials
- [ ] Update `.env` with real credentials
- [ ] Set `USE_FALLBACK_TTS=False`
- [ ] Test with `python test_azure.py`
- [ ] Restart services

---

## 🎉 Summary

**You're all set!** The application will now use gTTS for text-to-speech, which means:

1. ✅ **No Azure account needed**
2. ✅ **Stories will generate successfully**
3. ✅ **Audio will play in the frontend**
4. ✅ **Complete end-to-end flow works**

**Try it now:**
```bash
# Already running! Just visit:
http://localhost:8080
```

When you're ready for production-quality voices, follow **Option 2** above to set up Azure TTS.

---

## 📞 Need Help?

If you have issues:

1. Check backend logs: `tail -f backend.log`
2. Run Azure test: `python test_azure.py`
3. Check the error messages for specific guidance

The fallback TTS will keep working while you set up Azure credentials!
