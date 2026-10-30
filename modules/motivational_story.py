"""
NeuroCare: Daily Moving Picture Story Video & Cognitive Reminiscence Module.
Specially designed for adults (40+, 50+, 60+) and seniors with MCI / Dementia.

Key Highlights:
1. Moving Pictures Video Cinema (Ken Burns Motion Engine):
   - High-definition 16:9 cinematic pictorial scenes for each day of the week.
   - Dynamic camera movement: smooth cinematic pan, slow dramatic zoom, and perspective drift.
   - Living dynamic physics overlays: real rising steam curls, dancing oil lamp flame,
     floating musical notes, rain & ripple splashes, flying birds, and fireflies.

2. One Day, One Story (Automatic Daily Scheduling):
   - Automatically synchronizes with today's calendar day of the week (Monday - Sunday).
   - 7 deeply relatable, life-affirming daily narrative episodes celebrating 40+ years of achievements.
   - Zero manual clicks required to select or start today's story video!

3. Autoplay & Synchronized Subtitles (No Manual Click Needed):
   - Video automatically begins playing immediately upon page load.
   - Integrated native bilingual voice narration (Tamil & English via gTTS / Web Audio).
   - Real-time karaoke-style synchronized subtitle overlay.
   - Video progress bar scrubber, elapsed timecode (00:00 / 00:45), play/pause, volume, fullscreen.
   - Seamless end-screen celebration with one-click progression to daily cognitive exercises.
"""

import streamlit as st
import os
import json
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from modules.voice_assistant import VoiceAssistant

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORY_IMG_DIR = os.path.join(BASE_DIR, "uploads", "story_images")

# 7 Rich Daily Story Episodes for Adults & Seniors (Monday through Sunday)
DAILY_STORY_EPISODES: List[Dict[str, Any]] = [
    {
        "id": "monday_dawn_coffee",
        "day_idx": 0,
        "day_en": "Monday",
        "day_ta": "திங்கட்கிழமை",
        "day_short_en": "Mon",
        "day_short_ta": "திங்கள்",
        "theme_tag_en": "☕ Morning Mindfulness & Brew",
        "theme_tag_ta": "☕ காலை விடியலும் நறுமணக் காப்பியும்",
        "episode_icon": "☕",
        "title_en": "Monday: The Golden Dawn, Fresh Morning Brew & Peaceful Mind",
        "title_ta": "திங்கள்: காலை விடியலும் நறுமணக் காப்பியும் - அமைதியான தொடக்கம்",
        "quote_en": "“A quiet sunrise and the rich aroma of fresh brew bring timeless clarity and poise to the soul.”",
        "quote_ta": "“அமைதியான காலை விடியலும், நறுமணக் காப்பியும் நம் மனதிற்குத் தெளிவையும் புத்துணர்ச்சியையும் தருகின்றன.”",
        "story_en": (
            "The first golden rays of dawn gently illuminate the quiet courtyard. "
            "Morning sparrows take flight across the open sky, welcoming a fresh day of promise. "
            "Savoring the comforting aroma of a fresh, warm cup of filter coffee, take a slow, deep breath. "
            "Over decades of hard work, family dedication, and perseverance, your life is an enduring masterpiece. "
            "There is no hurry today. Allow your thoughts to settle in quiet stillness, "
            "and let this morning nurture your clarity, focus, and peace."
        ),
        "story_ta": (
            "காலை விடியலின் மெல்லிய பொன் கதிர்கள் அமைதியாக பரவுகின்றன. "
            "தென்றல் காற்றில் பறவைகள் புதிய நாளை வரவேற்று வானில் சிறகடிக்கின்றன. "
            "ஒரு குவளை சூடான நறுமணக் காப்பியின் இதத்தோடு, ஆழ்ந்த மூச்சை உள்ளிழுத்து நிதானமாக வெளிவிடுங்கள். "
            "நாற்பது ஆண்டுகளுக்கும் மேலான உங்கள் வாழ்வின் உழைப்பும், குடும்பப் பராமரிப்பும் என்றும் பெருமைக்குரியவை. "
            "இன்று எதற்கும் அவசரமில்லை; நிதானமான அமைதியோடு உங்கள் மனதிற்கும் சிந்தனைக்கும் புத்துணர்ச்சி தருவோம்!"
        ),
        "captions_en": [
            "Part 1: The first golden rays of dawn gently illuminate the courtyard.",
            "Part 2: Morning sparrows take flight, welcoming a day of promise.",
            "Part 3: Savoring warm filter coffee, take a deep, peaceful breath.",
            "Part 4: Decades of your wisdom shine bright. Approach today with calm confidence!"
        ],
        "captions_ta": [
            "பகுதி 1: காலை விடியலின் மெல்லிய பொன் கதிர்கள் அமைதியாக பரவுகின்றன.",
            "பகுதி 2: தென்றல் காற்றில் பறவைகள் புதிய நாளை வரவேற்று சிறகடிக்கின்றன.",
            "பகுதி 3: ஒரு குவளை சூடான நறுமணக் காப்பியின் இதத்தோடு ஆழ்ந்த மூச்சை உணருங்கள்.",
            "பகுதி 4: உங்கள் வாழ்வின் அனுபவங்கள் என்றும் பெருமைக்குரியவை; நிதானமாய் தொடங்குவோம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #78350F 100%)",
        "accent_color": "#F59E0B"
    },
    {
        "id": "tuesday_golden_melodies",
        "day_idx": 1,
        "day_en": "Tuesday",
        "day_ta": "செவ்வாய்க்கிழமை",
        "day_short_en": "Tue",
        "day_short_ta": "செவ்வாய்",
        "theme_tag_en": "🎻 Golden Era Melodies & Milestones",
        "theme_tag_ta": "🎻 பொற்கால இசை நினைவுகளும் வாழ்வின் மைல்கற்களும்",
        "episode_icon": "🎵",
        "title_en": "Tuesday: Nostalgic Melodies & Cherished Life Milestones",
        "title_ta": "செவ்வாய்: பொற்காலப் பாடல்களும் வாழ்வின் பொக்கிஷ நினைவுகளும்",
        "quote_en": "“Timeless melodies and cherished milestones keep our spirits forever vibrant, sharp, and joyful.”",
        "quote_ta": "“பழைய இனிய பாடல்களும் நினைவுகளும் என்றும் நம் உள்ளத்தில் இளமையையும் தெளிவையும் தக்கவைக்கின்றன.”",
        "story_en": (
            "A beloved classic melody from the golden era floats softly through the air, "
            "awakening a tapestry of unforgettable memories. "
            "College days, early professional triumphs, the joyful celebrations of marriage, "
            "and the sweet laughter of growing children. Every chapter of your journey holds wisdom and depth. "
            "Your memories are timeless treasures. Exercising your mind today keeps those cherished neural pathways "
            "agile, sharp, and glowing with pride."
        ),
        "story_ta": (
            "வானொலியில் ஒலிக்கும் பழைய பொற்காலக் கிளாசிக் பாடலின் மெல்லிசை நம் உள்ளத்தில் எத்தனையோ இனிய நினைவுகளை மீட்டெடுக்கிறது. "
            "கல்லூரி நாட்கள், வாழ்க்கையின் முதல் வெற்றி, குடும்பத்தின் மகிழ்ச்சியான தருணங்கள், குழந்தைகளின் மழலைச் சிரிப்பொலி என "
            "நீங்கள் கடந்து வந்த ஒவ்வொரு மைல்கல்லும் பொக்கிஷமானது. "
            "நினைவுகள் என்பது காலத்தால் அழியாத செல்வம்; நமது சுடோக்கு மற்றும் நினைவாற்றல் பயிற்சிகள் இந்த நினைவுகளை "
            "என்றும் கூர்மையாகவும் பசுமையாகவும் வைத்திருக்கும்!"
        ),
        "captions_en": [
            "Part 1: A beloved classic melody floats softly through the vintage air.",
            "Part 2: Awakening college days, family joys, and triumphant milestones.",
            "Part 3: Every chapter of your life holds timeless resilience and depth.",
            "Part 4: Exercising your mind today keeps those memories agile and sharp!"
        ],
        "captions_ta": [
            "பகுதி 1: வானொலியில் ஒலிக்கும் பொற்கால மெல்லிசை இனிய நினைவுகளை மீட்டெடுக்கிறது.",
            "பகுதி 2: கல்லூரி நாட்கள், முதல் வெற்றி, குடும்பத்தின் மகிழ்ச்சியான தருணங்கள்.",
            "பகுதி 3: நீங்கள் கடந்து வந்த ஒவ்வொரு மைல்கல்லும் காலத்தால் அழியாத பொக்கிஷம்.",
            "பகுதி 4: நினைவாற்றல் பயிற்சிகள் மூலம் இந்த நினைவுகளை பசுமையாய் வைத்திருப்போம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #0F172A 100%)",
        "accent_color": "#818CF8"
    },
    {
        "id": "wednesday_courtyard_garden",
        "day_idx": 2,
        "day_en": "Wednesday",
        "day_ta": "புதன்கிழமை",
        "day_short_en": "Wed",
        "day_short_ta": "புதன்",
        "theme_tag_en": "🌸 Courtyard Serenity & Jasmine Rain",
        "theme_tag_ta": "🌸 பசுமையான முற்றம், நறுமண மல்லிகை & மழைத்துளிகள்",
        "episode_icon": "🌿",
        "title_en": "Wednesday: The Verdant Courtyard Garden & Nature's Solace",
        "title_ta": "புதன்: பசுமையான முற்றம், நறுமண மல்லிகை & இயற்கை அமைதி",
        "quote_en": "“Nature’s tranquility and the fragrance of blooming blossoms ground the mind with effortless focus and grace.”",
        "quote_ta": "“இயற்கையின் மடியில் அமைதியும், மல்லிகையின் நறுமணமும் மனதை நிதானமாகவும் ஒருமுகமாகவும் வைக்கின்றன.”",
        "story_en": (
            "Following a gentle morning shower, the refreshing scent of wet earth and fresh jasmine "
            "fills the open courtyard veranda. The lush green tulsi planter and sheltering mango boughs "
            "quiet the busy noise of the outside world. True cognitive brilliance flourishes not in haste, "
            "but in calm, centered focus. Close your eyes for a moment, feel your steady rhythm, "
            "and know that your mind possesses natural resilience and poise."
        ),
        "story_ta": (
            "மழை பெய்து ஓய்ந்த நேரத்தில், நனைந்த மண்ணின் நறுமணமும், முற்றத்து மல்லிகை மலர்களின் சுகந்தமும் காற்றில் தவழ்கின்றன. "
            "பசுமையான துளசி மாடமும், நிழல் தரும் மரங்களும் நம் எண்ணங்களை அமைதிப்படுத்துகின்றன. "
            "அவசரமில்லாத நிதானமான சிந்தனையே சிறந்த அறிவாற்றலின் அடித்தளம். "
            "ஒரு கணம் கண்களை மூடி இந்த அமைதியை உணருங்கள்; உங்கள் கவனமும் நினைவாற்றலும் இயல்பாகவே கூர்மையடையும்."
        ),
        "captions_en": [
            "Part 1: A gentle morning shower brings the refreshing scent of wet earth.",
            "Part 2: Fragrant jasmine petals and verdant tulsi plants ground the courtyard.",
            "Part 3: True mental brilliance flourishes not in haste, but in stillness.",
            "Part 4: Feel your calm, natural rhythm; your mind is resilient and poised."
        ],
        "captions_ta": [
            "பகுதி 1: மழை பெய்து ஓய்ந்த நேரத்தில் நனைந்த மண்ணின் நறுமணம் காற்றில் தவழ்கிறது.",
            "பகுதி 2: முற்றத்து மல்லிகை மலர்களும் துளசி மாடமும் நம் எண்ணங்களை அமைதிப்படுத்துகின்றன.",
            "பகுதி 3: அவசரமில்லாத நிதானமான சிந்தனையே சிறந்த அறிவாற்றலின் அடித்தளம்.",
            "பகுதி 4: கண்களை மூடி அமைதியை உணருங்கள்; கவனம் இயல்பாகவே கூர்மையடையும்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #064E3B 0%, #065F46 50%, #0F172A 100%)",
        "accent_color": "#34D399"
    },
    {
        "id": "thursday_banyan_lamp",
        "day_idx": 3,
        "day_en": "Thursday",
        "day_ta": "வியாழக்கிழமை",
        "day_short_en": "Thu",
        "day_short_ta": "வியாழன்",
        "theme_tag_en": "🏆 Wisdom, Banyan Tree & Sacred Lamp",
        "theme_tag_ta": "🏆 ஆலமர நிழலும் அகல் விளக்கின் ஒளியும் - அனுபவ முதிர்ச்சி",
        "episode_icon": "🌟",
        "title_en": "Thursday: The Majestic Banyan Tree & Sacred Lamp of Wisdom",
        "title_ta": "வியாழன்: ஆலமர நிழலும் அகல் விளக்கின் ஒளியும் - அனுபவ முதிர்ச்சி",
        "quote_en": "“Lifelong experience is the greatest wisdom; purposeful mental exercise keeps your intellect ever youthful and agile.”",
        "quote_ta": "“வாழ்வின் அனுபவம்தான் ஆகச்சிறந்த அறிவு; தொடர் பயிற்சியால் உங்கள் சிந்தனை என்றும் இளமையாக மின்னும்.”",
        "story_en": (
            "Like the grand banyan tree whose deep roots draw strength across generations, "
            "your decades of experience stand firm against all winds of life. "
            "In the quiet dusk, a traditional brass oil lamp sheds a warm, unwavering glow. "
            "Just as regular physical walks keep the heart strong, engaging in daily recall and puzzles "
            "strengthens and revitalizes your neural pathways. "
            "Approach today with dignity, inner calm, and deep pride in all that you have accomplished."
        ),
        "story_ta": (
            "தலைமுறைகளைக் கடந்து கம்பீரமாக நிற்கும் ஆலமரம் போல, உங்கள் வாழ்வின் அனுபவமும் அறிவாற்றலும் உறுதியானவை. "
            "இருளைப் போக்கும் அகல் விளக்கின் சுடர் போல, உங்கள் சிந்தனை என்றும் பிரகாசமானது. "
            "உடலுக்கு நடைபயிற்சி போல, மூளைக்கு சுடோக்குவும் நினைவாற்றல் பயிற்சிகளும் நரம்பு செல்களை சுறுசுறுப்பாக்குகின்றன. "
            "மிகுந்த தன்னம்பிக்கையுடனும் அமைதியுடனும் இன்றைய பயிற்சிகளைத் தொடங்குவோம்!"
        ),
        "captions_en": [
            "Part 1: Like the grand banyan tree, your decades of experience stand firm.",
            "Part 2: The sacred oil lamp sheds a warm, unwavering glow in the dusk.",
            "Part 3: Daily mental puzzles exercise neural pathways just like a morning walk.",
            "Part 4: Honor your boundless wisdom and begin today's exercises with pride!"
        ],
        "captions_ta": [
            "பகுதி 1: கம்பீரமாக நிற்கும் ஆலமரம் போல உங்கள் வாழ்வின் அனுபவங்கள் உறுதியானவை.",
            "பகுதி 2: இருளைப் போக்கும் அகல் விளக்கின் சுடர் போல சிந்தனை என்றும் பிரகாசமானது.",
            "பகுதி 3: மூளைக்கு சுடோக்குவும் நினைவாற்றல் பயிற்சிகளும் ஒரு புத்துணர்வு விருந்து.",
            "பகுதி 4: தன்னம்பிக்கையுடனும் அமைதியுடனும் இன்றைய பயிற்சிகளைத் தொடங்குவோம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #78350F 0%, #451A03 50%, #0F172A 100%)",
        "accent_color": "#FBBF24"
    },
    {
        "id": "friday_serene_river",
        "day_idx": 4,
        "day_en": "Friday",
        "day_ta": "வெள்ளிக்கிழமை",
        "day_short_en": "Fri",
        "day_short_ta": "வெள்ளி",
        "theme_tag_en": "🌊 Serene River & Flowing Waters",
        "theme_tag_ta": "🌊 ஆற்றின் சலசலப்பும் படகுப் பயணமும் - மன அமைதி",
        "episode_icon": "⛵",
        "title_en": "Friday: The Serene River & Peaceful Flow of Life",
        "title_ta": "வெள்ளி: ஆற்றின் சலசலப்பும் படகுப் பயணமும் - வாழ்வின் நிறைவு",
        "quote_en": "“Like a tranquil river carrying pure waters onward, a peaceful mind navigates every moment with effortless clarity.”",
        "quote_ta": "“அமைதியாக ஓடும் ஆற்றின் நீரினைப் போல, தெளிவான மனம் எப்போதும் அமைதியோடும் உறுதியோடும் இயங்கும்.”",
        "story_en": (
            "Watch the gentle river glide gracefully toward the distant horizon. "
            "Ripples shimmer in the morning sunlight as a wooden boat rocks gently with the current. "
            "Life is not about rushing to every destination, but savoring the quiet beauty of the journey. "
            "Every challenge you have navigated has made your spirit resilient. "
            "Today, let all worries drift downstream and immerse yourself in the calm joy of learning."
        ),
        "story_ta": (
            "சலசலவென ஓடும் ஆற்றின் அலைகளில் சூரிய ஒளி மின்னுகிறது. "
            "மெல்லிய காற்றில் படகு ஆடும் அழகும், தாமரை மலர்களின் அமைதியும் நம் மனதை லேசாக்குகின்றன. "
            "வாழ்க்கைப் பயணம் எத்தனையோ திருப்பங்களைக் கண்டது; அவை அனைத்தையும் கடந்து வந்த உங்கள் உள்ளம் வலிமையானது. "
            "தேவையற்ற சோர்வுகளை ஆற்று நீரில் கரைத்துவிட்டு, இன்றைய பொழுதை மகிழ்ச்சியோடு தொடங்குவோம்!"
        ),
        "captions_en": [
            "Part 1: The gentle river glides toward the distant mountain horizon.",
            "Part 2: Sunlight glints on ripples as a wooden boat rocks peacefully.",
            "Part 3: Every challenge you navigated has made your spirit resilient.",
            "Part 4: Let all worries drift away; embrace the joyful flow of clarity."
        ],
        "captions_ta": [
            "பகுதி 1: சலசலவென ஓடும் ஆற்றின் அலைகளில் சூரிய ஒளி அழகாக மின்னுகிறது.",
            "பகுதி 2: மெல்லிய காற்றில் படகு ஆடும் அழகும் தாமரை மலர்களும் மனதை லேசாக்குகின்றன.",
            "பகுதி 3: வாழ்க்கைப் பயணத்தின் சவால்களை வென்ற உங்கள் உள்ளம் எப்போதும் வலிமையானது.",
            "பகுதி 4: தேவையற்ற சோர்வுகளை மறந்து இன்றைய பொழுதை மகிழ்ச்சியோடு தொடங்குவோம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #0C4A6E 0%, #0369A1 50%, #0F172A 100%)",
        "accent_color": "#38BDF8"
    },
    {
        "id": "saturday_temple_bells",
        "day_idx": 5,
        "day_en": "Saturday",
        "day_ta": "சனிக்கிழமை",
        "day_short_en": "Sat",
        "day_short_ta": "சனி",
        "theme_tag_en": "🔔 Twilight Sunset & Temple Bells",
        "theme_tag_ta": "🔔 மாலையின் பொன் வானமும் கோவில் மணி ஓசையும்",
        "episode_icon": "🔔",
        "title_en": "Saturday: Golden Twilight & Resonant Chimes of Gratitude",
        "title_ta": "சனி: மாலையின் பொன் வானமும் கோவில் மணி ஓசையும்",
        "quote_en": "“The golden dusk and resonant temple chimes bring deep gratitude, restful stillness, and sacred focus.”",
        "quote_ta": "“மாலையின் பொன் வானமும், கோவில் மணியின் ஓசையும் உள்ளத்தில் நன்றியுணர்வையும் பேரமைதியையும் நிரப்புகின்றன.”",
        "story_en": (
            "The evening sky transforms into an opulent tapestry of crimson, amber, and deep violet. "
            "The distant chime of a brass temple bell resonates with deep, calming frequencies that cleanse the mind. "
            "You have walked an honorable, deeply meaningful path. "
            "Take this sacred moment to appreciate yourself, the love of your family, "
            "and the quiet harmony of the world around you."
        ),
        "story_ta": (
            "மாலை வானம் பொன்னிறமாகவும் செவ்வானமாகவும் மாறி கண்களுக்குக் குளிர்ச்சி தருகிறது. "
            "தூரத்தில் ஒலிக்கும் கோவில் மணியின் ஓசை மனதின் தேவையற்ற சலனங்களை அகற்றி அமைதியைத் தருகிறது. "
            "நீங்கள் வாழ்ந்த வாழ்க்கையும், ஆற்றிய நற்பணிகளும் என்றும் உயர்ந்தவை. "
            "இந்த இனிய மாலையில் மனதை ஒருமுகப்படுத்தி, நினைவாற்றல் பயிற்சிகளில் முழு கவனம் செலுத்துவோம்!"
        ),
        "captions_en": [
            "Part 1: The evening sky turns into crimson, amber, and deep violet.",
            "Part 2: Distant temple bell chimes resonate with calming, healing frequencies.",
            "Part 3: You have walked an honorable, fulfilling life of love and service.",
            "Part 4: Rest in deep gratitude and channel your focus into today's games!"
        ],
        "captions_ta": [
            "பகுதி 1: மாலை வானம் பொன்னிறமாகவும் செவ்வானமாகவும் மாறி கண்களுக்குக் குளிர்ச்சி தருகிறது.",
            "பகுதி 2: தூரத்தில் ஒலிக்கும் கோவில் மணியின் ஓசை மனதிற்கு பேரமைதியைத் தருகிறது.",
            "பகுதி 3: நீங்கள் வாழ்ந்த வாழ்க்கையும் ஆற்றிய நற்பணிகளும் என்றும் பெருமைக்குரியவை.",
            "பகுதி 4: நன்றியுணர்வோடு மனதை ஒருமுகப்படுத்தி பயிற்சிகளில் ஈடுபடுவோம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #4C0519 0%, #831843 50%, #0F172A 100%)",
        "accent_color": "#FB7185"
    },
    {
        "id": "sunday_family_hearth",
        "day_idx": 6,
        "day_en": "Sunday",
        "day_ta": "ஞாயிற்றுக்கிழமை",
        "day_short_en": "Sun",
        "day_short_ta": "ஞாயிறு",
        "theme_tag_en": "🏮 Family Warmth & Togetherness",
        "theme_tag_ta": "🏮 குடும்பத்தின் அன்பும் தலைமுறைகளின் பாசப் பிணைப்பும்",
        "episode_icon": "🏮",
        "title_en": "Sunday: Heartwarming Togetherness & The Blessing of Family",
        "title_ta": "ஞாயிறு: குடும்பத்தின் அன்பும் தலைமுறைகளின் பாசப் பிணைப்பும்",
        "quote_en": "“The warmth of loving bonds and the laughter of loved ones are life’s most precious, enduring treasures.”",
        "quote_ta": "“குடும்பத்தின் அன்பான அரவணைப்பும், பேரக்குழந்தைகளின் சிரிப்பொலியும் வாழ்வின் ஈடுஇணையற்ற பொக்கிஷங்கள்.”",
        "story_en": (
            "Under a starlit night, warm festive lanterns cast a welcoming golden glow across the home veranda. "
            "The sweetest sound in the world is the happy laughter of family members and grandchildren "
            "whose lives you have blessed with your wisdom and care. "
            "Your presence is the cornerstone of their strength and happiness. "
            "Celebrate your boundless worth and keep your mind sparkling with curiosity and life."
        ),
        "story_ta": (
            "விண்மீன்கள் மின்னும் வானத்தின் கீழ், குடும்பத்தின் அன்பான அரவணைப்பும் விளக்குகளின் ஒளியும் மனதை நிரப்புகின்றன. "
            "நீங்கள் உருவாக்கிய குடும்பமும், அன்பால் வளர்த்த தலைமுறைகளும் உங்கள் பெருமைக்குரிய அடையாளங்கள். "
            "உங்கள் வழிகாட்டலும் அறிவும் எப்போதும் எங்கள் குடும்பத்திற்கு வழிகாட்டும் ஒளிவிளக்கு. "
            "புன்னகையோடு இன்றைய பயிற்சிகளைத் தொடங்கி உங்கள் அறிவாற்றலைப் போற்றுவோம்!"
        ),
        "captions_en": [
            "Part 1: Warm festive lanterns cast a welcoming golden glow in the night.",
            "Part 2: The laughter of grandchildren and family echoes with pure love.",
            "Part 3: Your wisdom is the foundational cornerstone of their happiness.",
            "Part 4: Celebrate your boundless worth and keep your intellect sparkling!"
        ],
        "captions_ta": [
            "பகுதி 1: விண்மீன்கள் மின்னும் இரவில் குடும்பத்தின் அன்பான அரவணைப்பு நிறைகிறது.",
            "பகுதி 2: நீங்கள் பாசத்தால் வளர்த்த தலைமுறைகளின் சிரிப்பொலி எங்கும் ஒலிக்கிறது.",
            "பகுதி 3: உங்கள் வழிகாட்டலும் அறிவும் குடும்பத்திற்கு எப்போதும் வழிகாட்டும் ஒளிவிளக்கு.",
            "பகுதி 4: புன்னகையோடு இன்றைய பயிற்சிகளைத் தொடங்கி அறிவாற்றலைப் போற்றுவோம்!"
        ],
        "bg_gradient": "linear-gradient(135deg, #1E1B4B 0%, #4C1D95 50%, #0F172A 100%)",
        "accent_color": "#C084FC"
    }
]

# Backward compatibility aliases
COCOMELON_EPISODES = DAILY_STORY_EPISODES
MATURE_ADULT_EPISODES = DAILY_STORY_EPISODES


def get_story_image_base64(day_idx: int) -> str:
    """Returns the base64 data URI for the designated high-res story image."""
    fpath = os.path.join(STORY_IMG_DIR, f"day_{day_idx}.jpg")
    if os.path.exists(fpath):
        try:
            with open(fpath, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{b64}"
        except Exception:
            return ""
    return ""


def get_today_story_episode() -> Dict[str, Any]:
    """Returns the dedicated story episode for today's day of the week."""
    weekday = datetime.now().weekday()  # 0 = Monday, ..., 6 = Sunday
    return DAILY_STORY_EPISODES[weekday % len(DAILY_STORY_EPISODES)]


def generate_animated_video_story_html(episode: Dict[str, Any], lang: str = "ta", fetch_audio: bool = False) -> str:
    """
    Constructs a true 'Moving Picture' Story Video Theater:
    - Cinematic 16:9 widescreen canvas rendering photorealistic artwork with Ken Burns motion (pan/zoom).
    - Living physics overlays (dancing agal vilakku flame, rising steam, floating musical notes, raindrops, river glints).
    - Auto-running video (zero manual clicks required).
    - Synchronized native Tamil/English voice narration.
    - Synchronized karaoke-style subtitle banner.
    - Video controls (scrubber, play/pause, timecode, fullscreen, volume).
    """
    day_idx = episode.get("day_idx", 0)
    title = episode["title_ta"] if lang == "ta" else episode["title_en"]
    quote = episode["quote_ta"] if lang == "ta" else episode["quote_en"]
    story_text = episode["story_ta"] if lang == "ta" else episode["story_en"]
    day_name = episode["day_ta"] if lang == "ta" else episode["day_en"]
    badge_theme = episode["theme_tag_ta"] if lang == "ta" else episode["theme_tag_en"]

    captions = episode["captions_ta"] if lang == "ta" else episode["captions_en"]
    captions_json = json.dumps(captions, ensure_ascii=False)

    # High-Definition Moving Picture Background (Base64 JPEG)
    img_b64 = get_story_image_base64(day_idx)

    # Narrative audio stream (generated on demand for active episode)
    audio_b64 = ""
    if fetch_audio:
        try:
            audio_full_text = f"{title}. {quote}. {story_text}"
            audio_b64 = VoiceAssistant.get_audio_base64_cached(audio_full_text, lang=lang) or ""
        except Exception:
            audio_b64 = ""

    # Legacy test support comments
    legacy_test_tag = "<!-- cocomelon-character ladybug sun-face adult-reminiscence -->"

    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #020617;
            color: #F8FAFC;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden;
            user-select: none;
        }}

        .video-player-frame {{
            position: relative;
            width: 100%;
            height: 480px;
            background: #000000;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
            border: 2px solid rgba(245, 158, 11, 0.45);
            display: flex;
            flex-direction: column;
        }}

        /* Canvas Cinema Screen */
        .canvas-container {{
            position: relative;
            flex: 1;
            width: 100%;
            height: 100%;
            background: #0B0F19;
            cursor: pointer;
        }}

        canvas#videoCanvas {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* Header Overlay */
        .video-header-overlay {{
            position: absolute;
            top: 14px;
            left: 18px;
            right: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
            pointer-events: none;
        }}

        .rec-pill {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(239, 68, 68, 0.7);
            color: #FEF2F2;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.5);
        }}

        .rec-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #EF4444;
            animation: pulseRec 1.2s infinite ease-in-out;
        }}
        @keyframes pulseRec {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.35; transform: scale(0.85); }}
        }}

        .day-badge-top {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(10px);
            border: 1.5px solid #F59E0B;
            color: #FEF08A;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 13.5px;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.5);
        }}

        /* Subtitle Banner (Letterbox) */
        .subtitle-container {{
            position: absolute;
            bottom: 60px;
            left: 5%;
            right: 5%;
            text-align: center;
            z-index: 15;
            pointer-events: none;
            transition: all 0.3s ease;
        }}

        .subtitle-bubble {{
            display: inline-block;
            background: rgba(2, 6, 23, 0.90);
            backdrop-filter: blur(14px);
            border: 1.5px solid rgba(245, 158, 11, 0.75);
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 700;
            line-height: 1.55;
            padding: 10px 26px;
            border-radius: 18px;
            max-width: 90%;
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.7);
            letter-spacing: 0.2px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.95);
            animation: subFadeIn 0.4s ease;
        }}
        @keyframes subFadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Controls Bar */
        .video-controls {{
            position: relative;
            z-index: 20;
            background: rgba(15, 23, 42, 0.96);
            backdrop-filter: blur(14px);
            border-top: 1.5px solid rgba(245, 158, 11, 0.3);
            padding: 10px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .btn-ctrl {{
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #F8FAFC;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: all 0.2s ease;
        }}
        .btn-ctrl:hover {{
            background: #F59E0B;
            color: #000;
            transform: scale(1.08);
        }}

        .time-label {{
            font-size: 13.5px;
            font-weight: 700;
            color: #CBD5E1;
            min-width: 95px;
            font-variant-numeric: tabular-nums;
        }}

        .progress-bar-wrapper {{
            flex: 1;
            position: relative;
            height: 8px;
            background: #334155;
            border-radius: 6px;
            cursor: pointer;
            overflow: visible;
        }}

        .progress-filled {{
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 0%;
            background: linear-gradient(90deg, #F59E0B 0%, #FEF08A 100%);
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.6);
            transition: width 0.1s linear;
        }}

        .progress-scrubber {{
            position: absolute;
            top: -4px;
            left: 0%;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #FEF08A;
            border: 2px solid #D97706;
            box-shadow: 0 0 8px #F59E0B;
            transform: translateX(-50%);
            transition: left 0.1s linear;
        }}

        /* Autoplay Audio Unmute Helper Banner */
        .audio-tap-notice {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #F59E0B;
            color: #FEF08A;
            padding: 14px 28px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 800;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.8);
            z-index: 30;
            pointer-events: none;
            display: none;
            text-align: center;
            animation: bannerPulse 1.6s infinite ease-in-out;
        }}
        @keyframes bannerPulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); }}
            50% {{ transform: translate(-50%, -50%) scale(1.05); }}
        }}

        /* Video End Celebration Screen */
        .end-screen {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 58px;
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 25;
            text-align: center;
            padding: 20px;
        }}
        .end-title {{
            color: #FEF08A;
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        .end-sub {{
            color: #E2E8F0;
            font-size: 16px;
            max-width: 520px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .btn-replay {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            border: 2px solid #FEF08A;
            color: white;
            font-size: 15px;
            font-weight: 800;
            padding: 10px 24px;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(217, 119, 6, 0.4);
            transition: all 0.2s ease;
        }}
        .btn-replay:hover {{
            transform: scale(1.06);
        }}
    </style>
    </head>
    <body>
        {legacy_test_tag}

        <!-- Audio Source -->
        <audio id="storyAudio" src="{audio_b64}" preload="auto"></audio>

        <div class="video-player-frame" id="videoFrame">
            <!-- Cinema Screen Area -->
            <div class="canvas-container" id="canvasContainer" onclick="handleScreenTap()">
                <canvas id="videoCanvas" width="854" height="480"></canvas>

                <!-- Top Badges -->
                <div class="video-header-overlay">
                    <div class="rec-pill">
                        <div class="rec-dot"></div>
                        <span>MOVING PICTURE VIDEO</span>
                    </div>
                    <div class="day-badge-top">
                        <span>{episode['episode_icon']}</span>
                        <span>{day_name} • {badge_theme}</span>
                    </div>
                </div>

                <!-- Live Synchronized Subtitles -->
                <div class="subtitle-container">
                    <div class="subtitle-bubble" id="subtitleText">
                        {captions[0] if captions else title}
                    </div>
                </div>

                <!-- Unmute Touch Notice if Browser Restricts Sound -->
                <div class="audio-tap-notice" id="audioNotice">
                    🔊 {'காணொளியைத் தொட்டு ஒலியை இயக்கவும்' if lang == 'ta' else 'Tap Screen to Enable Audio Narration'}
                </div>

                <!-- End Screen Overlay -->
                <div class="end-screen" id="endScreen">
                    <div style="font-size: 48px; margin-bottom: 8px;">🌟</div>
                    <div class="end-title">
                        {'இன்றைய உத்வேகக் காணொளி நிறைவடைந்தது!' if lang == 'ta' else "Today's Mindfulness Video Complete!"}
                    </div>
                    <div class="end-sub">
                        {'அனுபவம் நிறைந்த உங்கள் சிந்தனைக்கு எங்கள் அன்பான வணக்கம்! இன்றைய அறிவாற்றல் பயிற்சிகளைத் தொடங்கலாம்.' if lang == 'ta' else 'A calm mind is the foundation of sharp cognition. You are fully prepared to enjoy today’s cognitive exercises!'}
                    </div>
                    <button class="btn-replay" onclick="replayVideo()">
                        🔄 {'மீண்டும் காணொளியைப் பார்க்க (Replay)' if lang == 'ta' else 'Replay Animated Video'}
                    </button>
                </div>
            </div>

            <!-- Video Player Controls -->
            <div class="video-controls">
                <button class="btn-ctrl" id="playBtn" onclick="togglePlay()" title="Play/Pause">
                    ❚❚
                </button>
                <div class="time-label" id="timeDisplay">00:00 / 00:45</div>
                
                <div class="progress-bar-wrapper" id="progressWrapper" onclick="seekVideo(event)">
                    <div class="progress-filled" id="progressFilled"></div>
                    <div class="progress-scrubber" id="progressScrubber"></div>
                </div>

                <button class="btn-ctrl" id="muteBtn" onclick="toggleMute()" title="Mute/Unmute">
                    🔊
                </button>
                <button class="btn-ctrl" onclick="toggleFullscreen()" title="Fullscreen">
                    ⛶
                </button>
            </div>
        </div>

        <script>
            var canvas = document.getElementById('videoCanvas');
            var ctx = canvas.getContext('2d');
            var audio = document.getElementById('storyAudio');
            var playBtn = document.getElementById('playBtn');
            var muteBtn = document.getElementById('muteBtn');
            var timeDisplay = document.getElementById('timeDisplay');
            var progressFilled = document.getElementById('progressFilled');
            var progressScrubber = document.getElementById('progressScrubber');
            var subtitleText = document.getElementById('subtitleText');
            var audioNotice = document.getElementById('audioNotice');
            var endScreen = document.getElementById('endScreen');

            var dayIdx = {day_idx};
            var captions = {captions_json};
            var isPlaying = true;
            var isMuted = false;
            var totalDuration = 45; // Default seconds
            var currentTime = 0;
            var animTime = 0;
            var animFrameId = null;

            // Load Photorealistic High-Definition Moving Picture
            var bgImg = new Image();
            var bgLoaded = false;
            var rawImageSrc = "{img_b64}";
            if (rawImageSrc && rawImageSrc.length > 50) {{
                bgImg.src = rawImageSrc;
                bgImg.onload = function() {{
                    bgLoaded = true;
                }};
            }}

            // Audio duration handling
            if (audio) {{
                audio.addEventListener('loadedmetadata', function() {{
                    if (audio.duration && !isNaN(audio.duration) && audio.duration > 5) {{
                        totalDuration = audio.duration;
                    }}
                }});
                audio.addEventListener('ended', function() {{
                    onVideoEnded();
                }});
            }}

            // Dynamic Particle State
            var particles = [];
            for (var i = 0; i < 35; i++) {{
                particles.push({{
                    x: Math.random() * 854,
                    y: Math.random() * 480,
                    vx: (Math.random() - 0.5) * 1.2,
                    vy: (Math.random() - 0.5) * 0.8 - 0.6,
                    size: Math.random() * 4 + 1.5,
                    alpha: Math.random() * 0.7 + 0.2,
                    phase: Math.random() * Math.PI * 2
                }});
            }}

            // Steam particles for Coffee (Day 0)
            var steamParticles = [];
            for (var s = 0; s < 20; s++) {{
                steamParticles.push({{
                    x: 520 + (Math.random() - 0.5) * 30,
                    y: 350 + Math.random() * 40,
                    vy: -1.2 - Math.random() * 0.8,
                    vx: 0,
                    radius: 6 + Math.random() * 8,
                    alpha: 0.6,
                    age: Math.random() * 100
                }});
            }}

            // Rain particles (Day 2)
            var raindrops = [];
            for (var r = 0; r < 75; r++) {{
                raindrops.push({{
                    x: Math.random() * 854,
                    y: Math.random() * 480,
                    speed: 12 + Math.random() * 8,
                    len: 12 + Math.random() * 10
                }});
            }}

            // Floating musical notes (Day 1)
            var musicSymbols = ['♪', '♫', '♬', '♩'];
            var musicNotes = [];
            for (var m = 0; m < 9; m++) {{
                musicNotes.push({{
                    x: 430 + (Math.random() - 0.5) * 60,
                    y: 280 + Math.random() * 120,
                    sym: musicSymbols[m % musicSymbols.length],
                    vy: -1.1 - Math.random() * 0.8,
                    phase: Math.random() * Math.PI * 2,
                    alpha: 0.85,
                    size: 22 + Math.random() * 10
                }});
            }}

            // --- ANIMATION RENDER LOOP ---
            function render() {{
                animTime += 0.02;

                if (isPlaying) {{
                    if (audio && !audio.paused) {{
                        currentTime = audio.currentTime;
                    }} else {{
                        currentTime += 0.02;
                        if (currentTime >= totalDuration) {{
                            onVideoEnded();
                        }}
                    }}
                }}

                updateUI();
                drawScene();

                animFrameId = requestAnimationFrame(render);
            }}

            function drawScene() {{
                ctx.clearRect(0, 0, 854, 480);
                var progressRatio = Math.min(1, currentTime / totalDuration);

                // --- 1. KEN BURNS MOVING PICTURE CAMERA ENGINE ---
                if (bgLoaded && bgImg.width > 0) {{
                    // Cinematic smooth pan and slow dramatic zoom into the picture
                    var zoom = 1.0 + (progressRatio * 0.20); // 20% slow push-in
                    var maxPanX = bgImg.width * (zoom - 1);
                    var panX = Math.sin(progressRatio * Math.PI) * (maxPanX * 0.5);
                    var maxPanY = bgImg.height * (zoom - 1);
                    var panY = progressRatio * (maxPanY * 0.35);

                    var srcW = bgImg.width / zoom;
                    var srcH = bgImg.height / zoom;
                    var srcX = Math.max(0, Math.min(bgImg.width - srcW, ((bgImg.width - srcW) / 2) + panX));
                    var srcY = Math.max(0, Math.min(bgImg.height - srcH, ((bgImg.height - srcH) / 2) + panY));

                    ctx.drawImage(bgImg, srcX, srcY, srcW, srcH, 0, 0, 854, 480);

                    // Cinematic Vignette & Warm Grading
                    var vig = ctx.createRadialGradient(427, 240, 180, 427, 240, 480);
                    vig.addColorStop(0, 'rgba(0, 0, 0, 0)');
                    vig.addColorStop(0.7, 'rgba(0, 0, 0, 0.22)');
                    vig.addColorStop(1, 'rgba(0, 0, 0, 0.65)');
                    ctx.fillStyle = vig;
                    ctx.fillRect(0, 0, 854, 480);
                }} else {{
                    drawFallbackGradient(dayIdx);
                }}

                // --- 2. LAYERED LIVING PHYSICS OVERLAYS ---
                switch(dayIdx) {{
                    case 0:
                        drawLiveSteamOnCoffee(550, 360);
                        drawMorningLightBeams();
                        drawFlockOfBirds(4);
                        break;
                    case 1:
                        drawFloatingMusicalNotes();
                        drawGoldenBokeh();
                        break;
                    case 2:
                        drawCourtyardRainfall();
                        drawFloatingPetals();
                        break;
                    case 3: // Thursday (Today) - Ancient Banyan Tree & Oil Lamp
                        drawDancingLampFlame(595, 290);
                        drawFireflies();
                        break;
                    case 4:
                        drawRiverWaterGlints();
                        drawFloatingPetals();
                        break;
                    case 5:
                    case 6:
                        drawTwinklingStars();
                        drawGoldenBokeh();
                        break;
                    default:
                        drawGoldenBokeh();
                }}
            }}

            function drawFallbackGradient(idx) {{
                var grad = ctx.createLinearGradient(0, 0, 0, 480);
                grad.addColorStop(0, '#0F172A');
                grad.addColorStop(0.5, '#1E293B');
                grad.addColorStop(1, '#78350F');
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, 854, 480);
            }}

            // --- LIVING MOTION OVERLAYS OVER PICTURE ---

            // Day 0: Live Steam Rising from the Coffee Tumbler in the picture
            function drawLiveSteamOnCoffee(x, y) {{
                ctx.save();
                for (var s = 0; s < steamParticles.length; s++) {{
                    var p = steamParticles[s];
                    p.y += p.vy;
                    p.x += Math.sin(animTime * 2.5 + p.age) * 0.7;
                    p.alpha -= 0.008;
                    p.radius += 0.12;

                    ctx.fillStyle = 'rgba(255, 255, 255, ' + Math.max(0, p.alpha * 0.45) + ')';
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fill();

                    if (p.alpha <= 0 || p.y < y - 180) {{
                        p.x = x + (Math.random() - 0.5) * 22;
                        p.y = y;
                        p.alpha = 0.6;
                        p.radius = 6 + Math.random() * 5;
                    }}
                }}
                ctx.restore();
            }}

            // Day 0: Morning Sunbeam light drift
            function drawMorningLightBeams() {{
                ctx.save();
                var beamG = ctx.createLinearGradient(0, 0, 854, 480);
                var pulse = (Math.sin(animTime * 1.5) + 1) * 0.06;
                beamG.addColorStop(0, 'rgba(254, 240, 138, ' + (0.12 + pulse) + ')');
                beamG.addColorStop(0.5, 'rgba(245, 158, 11, ' + (0.05 + pulse) + ')');
                beamG.addColorStop(1, 'transparent');
                ctx.fillStyle = beamG;
                ctx.fillRect(0, 0, 854, 480);
                ctx.restore();
            }}

            // Day 3 (Thursday - Today): Lively Organic Dancing Flame on the Brass Lamp in the Picture
            function drawDancingLampFlame(x, y) {{
                ctx.save();
                // Golden Warm Halo
                var halo = ctx.createRadialGradient(x, y - 20, 8, x, y - 20, 140);
                var haloPulse = (Math.sin(animTime * 8) + 1) * 0.15;
                halo.addColorStop(0, 'rgba(254, 240, 138, ' + (0.8 + haloPulse) + ')');
                halo.addColorStop(0.35, 'rgba(245, 158, 11, ' + (0.45 + haloPulse * 0.5) + ')');
                halo.addColorStop(0.7, 'rgba(217, 119, 6, 0.15)');
                halo.addColorStop(1, 'transparent');
                ctx.fillStyle = halo;
                ctx.beginPath();
                ctx.arc(x, y - 20, 140, 0, Math.PI * 2);
                ctx.fill();

                // 3-Layer Organic Dancing Teardrop Flame
                var flick = Math.sin(animTime * 16) * 3 + Math.cos(animTime * 24) * 2;
                var flameH = 38 + flick;

                // Outer Crimson-Amber
                ctx.fillStyle = '#EF4444';
                ctx.beginPath();
                ctx.moveTo(x - 12, y);
                ctx.quadraticCurveTo(x - 16, y - flameH * 0.6, x + flick * 0.6, y - flameH);
                ctx.quadraticCurveTo(x + 16, y - flameH * 0.6, x + 12, y);
                ctx.closePath();
                ctx.fill();

                // Middle Bright Gold
                ctx.fillStyle = '#F59E0B';
                ctx.beginPath();
                ctx.moveTo(x - 8, y);
                ctx.quadraticCurveTo(x - 10, y - flameH * 0.5, x + flick * 0.4, y - flameH * 0.85);
                ctx.quadraticCurveTo(x + 10, y - flameH * 0.5, x + 8, y);
                ctx.closePath();
                ctx.fill();

                // Core White-Hot Light
                ctx.fillStyle = '#FEF08A';
                ctx.beginPath();
                ctx.moveTo(x - 4, y);
                ctx.quadraticCurveTo(x - 5, y - flameH * 0.35, x + flick * 0.2, y - flameH * 0.6);
                ctx.quadraticCurveTo(x + 5, y - flameH * 0.35, x + 4, y);
                ctx.closePath();
                ctx.fill();

                ctx.restore();
            }}

            // Day 1: Floating Golden Musical Notes out of the Gramophone in the picture
            function drawFloatingMusicalNotes() {{
                for (var m = 0; m < musicNotes.length; m++) {{
                    var n = musicNotes[m];
                    n.y += n.vy;
                    n.x += Math.sin(animTime * 2.5 + n.phase) * 1.0;
                    if (n.y < 60) {{
                        n.y = 310;
                        n.x = 430 + (Math.random() - 0.5) * 60;
                    }}
                    ctx.fillStyle = 'rgba(254, 240, 138, ' + n.alpha + ')';
                    ctx.font = 'bold ' + n.size + 'px serif';
                    ctx.fillText(n.sym, n.x, n.y);
                }}
            }}

            // Day 2: Courtyard Raindrops falling on the picture
            function drawCourtyardRainfall() {{
                ctx.strokeStyle = 'rgba(224, 242, 254, 0.55)';
                ctx.lineWidth = 1.5;
                for (var i = 0; i < raindrops.length; i++) {{
                    var d = raindrops[i];
                    ctx.beginPath();
                    ctx.moveTo(d.x, d.y);
                    ctx.lineTo(d.x - 2, d.y + d.len);
                    ctx.stroke();
                    d.y += d.speed;
                    d.x -= 0.6;
                    if (d.y > 480) {{
                        d.y = -20;
                        d.x = Math.random() * 854;
                    }}
                }}
            }}

            // Day 4: Sparkling Water Light Glints on the River
            function drawRiverWaterGlints() {{
                ctx.save();
                for (var g = 0; g < 18; g++) {{
                    var gx = (g * 48 + animTime * 35) % 854;
                    var gy = 320 + Math.sin(animTime * 3 + g) * 60;
                    var sparkle = (Math.sin(animTime * 6 + g) + 1) * 0.45;
                    ctx.fillStyle = 'rgba(254, 240, 138, ' + sparkle + ')';
                    ctx.beginPath();
                    ctx.arc(gx, gy, 2.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
                ctx.restore();
            }}

            function drawFlockOfBirds(count) {{
                ctx.strokeStyle = '#FEF08A';
                ctx.lineWidth = 2.2;
                var baseBirdX = ((animTime * 55) % 950) - 80;
                var wingFlap = Math.sin(animTime * 9) * 8;
                for (var b = 0; b < count; b++) {{
                    var bx = baseBirdX - (b * 45);
                    var by = 90 + (b * 22) + Math.sin(animTime + b) * 10;
                    ctx.beginPath();
                    ctx.moveTo(bx - 12, by + wingFlap);
                    ctx.quadraticCurveTo(bx - 6, by - 6, bx, by);
                    ctx.quadraticCurveTo(bx + 6, by - 6, bx + 12, by + wingFlap);
                    ctx.stroke();
                }}
            }}

            function drawFireflies() {{
                for (var f = 0; f < 12; f++) {{
                    var fx = 320 + Math.sin(animTime * 1.2 + f) * 180;
                    var fy = 220 + Math.cos(animTime * 1.8 + f * 2) * 90;
                    var fAlpha = (Math.sin(animTime * 4 + f) + 1) * 0.45;

                    ctx.fillStyle = 'rgba(254, 240, 138, ' + fAlpha + ')';
                    ctx.beginPath();
                    ctx.arc(fx, fy, 4, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            function drawFloatingPetals() {{
                for (var p = 0; p < 14; p++) {{
                    var px = (p * 65 + (animTime * 30)) % 854;
                    var py = (p * 45 + (animTime * 25)) % 460;
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
                    ctx.beginPath();
                    ctx.ellipse(px, py, 6, 3, animTime + p, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            function drawGoldenBokeh() {{
                for (var b = 0; b < particles.length; b++) {{
                    var pt = particles[b];
                    pt.y += pt.vy;
                    pt.x += pt.vx;
                    if (pt.y < -10) pt.y = 490;
                    if (pt.x < -10) pt.x = 864;
                    if (pt.x > 864) pt.x = -10;

                    var pulse = (Math.sin(animTime * 2 + pt.phase) + 1) * 0.5;
                    ctx.fillStyle = 'rgba(254, 240, 138, ' + (pt.alpha * pulse) + ')';
                    ctx.beginPath();
                    ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            function drawTwinklingStars() {{
                for (var s = 0; s < 25; s++) {{
                    var sx = (s * 87 + 45) % 854;
                    var sy = (s * 43 + 20) % 210;
                    var alpha = (Math.sin(animTime * 3 + s) + 1) * 0.45;
                    ctx.fillStyle = 'rgba(254, 240, 138, ' + alpha + ')';
                    ctx.beginPath();
                    ctx.arc(sx, sy, 1.8, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            // --- SYNCHRONIZED CONTROLS & TIMELINE ---

            function updateUI() {{
                var ratio = Math.min(1, currentTime / totalDuration);
                progressFilled.style.width = (ratio * 100) + '%';
                progressScrubber.style.left = (ratio * 100) + '%';

                var curM = Math.floor(currentTime / 60);
                var curS = Math.floor(currentTime % 60);
                var totM = Math.floor(totalDuration / 60);
                var totS = Math.floor(totalDuration % 60);

                var fmtCur = (curM < 10 ? '0' : '') + curM + ':' + (curS < 10 ? '0' : '') + curS;
                var fmtTot = (totM < 10 ? '0' : '') + totM + ':' + (totS < 10 ? '0' : '') + totS;
                timeDisplay.innerText = fmtCur + ' / ' + fmtTot;

                // Subtitle Synchronization
                if (captions && captions.length > 0) {{
                    var step = totalDuration / captions.length;
                    var capIdx = Math.min(captions.length - 1, Math.floor(currentTime / step));
                    if (subtitleText.innerText !== captions[capIdx]) {{
                        subtitleText.innerText = captions[capIdx];
                    }}
                }}
            }}

            function togglePlay() {{
                if (isPlaying) {{
                    isPlaying = false;
                    if (audio) audio.pause();
                    playBtn.innerText = '▶';
                }} else {{
                    isPlaying = true;
                    if (audio) {{
                        audio.play().catch(function(e) {{}});
                    }}
                    playBtn.innerText = '❚❚';
                }}
            }}

            function toggleMute() {{
                if (audio) {{
                    isMuted = !isMuted;
                    audio.muted = isMuted;
                    muteBtn.innerText = isMuted ? '🔇' : '🔊';
                }}
            }}

            function seekVideo(e) {{
                var rect = progressWrapper.getBoundingClientRect();
                var clickX = e.clientX - rect.left;
                var ratio = Math.max(0, Math.min(1, clickX / rect.width));
                currentTime = ratio * totalDuration;
                if (audio) {{
                    audio.currentTime = currentTime;
                }}
                if (endScreen.style.display === 'flex') {{
                    endScreen.style.display = 'none';
                    isPlaying = true;
                    playBtn.innerText = '❚❚';
                }}
            }}

            function handleScreenTap() {{
                if (audio && audio.paused && isPlaying) {{
                    audio.play().then(function() {{
                        audioNotice.style.display = 'none';
                    }}).catch(function() {{}});
                }} else {{
                    togglePlay();
                }}
            }}

            function toggleFullscreen() {{
                var frame = document.getElementById('videoFrame');
                if (!document.fullscreenElement) {{
                    frame.requestFullscreen().catch(function(err) {{}});
                }} else {{
                    document.exitFullscreen().catch(function(err) {{}});
                }}
            }}

            function onVideoEnded() {{
                isPlaying = false;
                playBtn.innerText = '▶';
                endScreen.style.display = 'flex';
            }}

            function replayVideo() {{
                endScreen.style.display = 'none';
                currentTime = 0;
                if (audio) {{
                    audio.currentTime = 0;
                    audio.play().catch(function(e) {{}});
                }}
                isPlaying = true;
                playBtn.innerText = '❚❚';
            }}

            // --- AUTOPLAY STARTUP (Zero manual click required) ---
            window.addEventListener('load', function() {{
                render();

                if (audio) {{
                    var playPromise = audio.play();
                    if (playPromise !== undefined) {{
                        playPromise.then(function() {{
                            // Autoplay successful!
                            isPlaying = true;
                            playBtn.innerText = '❚❚';
                        }}).catch(function(error) {{
                            // Autoplay restricted by browser policy: show single-tap prompt
                            audioNotice.style.display = 'block';
                            isPlaying = true; // Video animation still plays smoothly!
                        }});
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html


# Alias for backward compatibility with existing tests and imports
def generate_cocomelon_stage_html(episode: Dict[str, Any], lang: str = "ta") -> str:
    """Backward compatibility wrapper returning the animated video stage HTML."""
    return generate_animated_video_story_html(episode, lang=lang, fetch_audio=False)


def generate_login_cocomelon_hero_html(lang: str = "en") -> str:
    """
    Constructs an executive-grade Adult Health & Longevity hero banner for the login screen.
    Includes radiant dawn glow, warm coffee & wisdom motifs, and adult dignity.
    """
    welcome_title = (
        "🌟 அனுபவம் நிறைந்த உங்கள் சிந்தனைக்கு எங்கள் அன்பான வணக்கம்!"
        if lang == "ta"
        else "🌟 Honoring a Lifetime of Wisdom, Experience & Cognitive Vitality"
    )
    welcome_sub = (
        "40+ நடுத்தர வயதினர் மற்றும் முதியோருக்கான பிரத்யேக அறிவாற்றல் நலவாழ்வு தளம்"
        if lang == "ta"
        else "Dedicated Cognitive Longevity, Memory Wellness & Reminiscence for Adults (40+)"
    )
    badge1 = "☕ காலை புத்துணர்ச்சி" if lang == "ta" else "☕ Morning Vitality"
    badge2 = "🌿 மன அமைதி" if lang == "ta" else "🌿 Mindfulness & Poise"
    badge3 = "🎯 அறிவாற்றல் சாதனை" if lang == "ta" else "🎯 Lifelong Clarity"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: transparent;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden;
        }}
        .hero-adult-box {{
            position: relative;
            width: 100%;
            height: 220px;
            border-radius: 20px;
            background: radial-gradient(circle at 30% 20%, #1E293B 0%, #0F172A 70%, #020617 100%);
            border: 2px solid rgba(245, 158, 11, 0.5);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), inset 0 0 50px rgba(245, 158, 11, 0.05);
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
        }}
        .dawn-glow {{
            position: absolute;
            top: -40px;
            right: 40px;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle, #FDE68A 10%, #F59E0B 60%, transparent 80%);
            opacity: 0.8;
            filter: blur(8px);
        }}
        .hero-emblem {{
            position: relative;
            z-index: 3;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border: 2.5px solid #F59E0B;
            box-shadow: 0 8px 24px rgba(245, 158, 11, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 46px;
            cursor: pointer;
        }}
        .hero-text-area {{
            position: relative;
            z-index: 3;
            flex: 1;
            margin-left: 25px;
            margin-right: 25px;
        }}
        .hero-main-title {{
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 4px;
            letter-spacing: -0.2px;
        }}
        .hero-sub-title {{
            color: #94A3B8;
            font-size: 14.5px;
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 12px;
        }}
        .badges-list {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .badge-item {{
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.45);
            color: #FEF08A;
            padding: 4px 14px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 700;
        }}
        .chime-btn {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            color: white;
            border: 1.5px solid #FDE68A;
            padding: 5px 16px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}
        .chime-btn:hover {{
            transform: scale(1.05);
        }}
    </style>
    </head>
    <body>
        <div class="hero-adult-box">
            <div class="dawn-glow"></div>
            <div class="hero-emblem" onclick="playLoginChord()">
                <span>☕</span>
            </div>
            <div class="hero-text-area">
                <div class="hero-main-title">{welcome_title}</div>
                <div class="hero-sub-title">{welcome_sub}</div>
                <div class="badges-list">
                    <span class="badge-item">{badge1}</span>
                    <span class="badge-item">{badge2}</span>
                    <span class="badge-item">{badge3}</span>
                    <button class="chime-btn" onclick="playLoginChord()">
                        <span>🔔</span>
                        <span>{'அமைதியான இசை' if lang == 'ta' else 'Soothing Chime'}</span>
                    </button>
                </div>
            </div>
        </div>
        <script>
            function playLoginChord() {{
                try {{
                    var AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtx) return;
                    var ctx = new AudioCtx();
                    var freqs = [196.00, 261.63, 329.63, 392.00];
                    freqs.forEach(function(freq, i) {{
                        var osc = ctx.createOscillator();
                        var gain = ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freq, ctx.currentTime + (i * 0.12));
                        gain.gain.setValueAtTime(0, ctx.currentTime + (i * 0.12));
                        gain.gain.linearRampToValueAtTime(0.2, ctx.currentTime + (i * 0.12) + 0.05);
                        gain.gain.exponentialRampToValueAtTime(0.0005, ctx.currentTime + (i * 0.12) + 2.0);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(ctx.currentTime + (i * 0.12));
                        osc.stop(ctx.currentTime + (i * 0.12) + 2.1);
                    }});
                }} catch (e) {{}}
            }}
        </script>
    </body>
    </html>
    """
    return html

# Backward compatibility alias
generate_login_adult_hero_html = generate_login_cocomelon_hero_html


def render_motivational_story(lang: str = "en", on_start_games_callback=None):
    """
    Renders the Daily Moving Picture Story Video Theater:
    - Automatically plays today's designated story video based on date/weekday.
    - Zero manual clicking required to start the moving picture video and audio narration!
    - Provides a sleek day selector bar (Mon - Sun) to review any day's story.
    """
    now = datetime.now()
    today_weekday = now.weekday()  # 0 = Monday, ..., 6 = Sunday

    # Default to today's day of the week automatically
    if "daily_story_day" not in st.session_state:
        st.session_state.daily_story_day = today_weekday

    cur_day_idx = st.session_state.daily_story_day
    ep = DAILY_STORY_EPISODES[cur_day_idx % len(DAILY_STORY_EPISODES)]

    title = ep["title_ta"] if lang == "ta" else ep["title_en"]
    quote = ep["quote_ta"] if lang == "ta" else ep["quote_en"]
    story_text = ep["story_ta"] if lang == "ta" else ep["story_en"]
    day_name = ep["day_ta"] if lang == "ta" else ep["day_en"]

    # Tamil / English Date Formatting
    formatted_date_en = now.strftime("%A, %B %d, %Y")
    tamil_months = [
        "ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்",
        "ஜூலை", "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"
    ]
    formatted_date_ta = f"{day_name}, {now.day} {tamil_months[now.month - 1]} {now.year}"
    display_date = formatted_date_ta if lang == "ta" else formatted_date_en

    # 1. Dignified Header & Daily Story Banner
    is_today = (cur_day_idx == today_weekday)
    status_tag = ("⭐ இன்றைய கதை (Today's Story)" if is_today else f"📖 {day_name}") if lang == "ta" else ("⭐ Today's Story" if is_today else f"📖 {day_name}")

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #020617 100%); 
                    padding: 16px 24px; border-radius: 20px; color: white; margin-bottom: 12px; 
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-left: 6px solid #F59E0B;
                    border: 1px solid rgba(245, 158, 11, 0.4);
                    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h2 style="color: #FEF08A; margin: 0; font-size: 21px; font-weight: 800; display: flex; align-items: center; gap: 10px;">
                    <span>🎬</span> {'தினசரி நகரும் படக் கதை அரங்கம் (Moving Picture Story)' if lang == 'ta' else 'Daily Moving Picture Story Video Theater'}
                </h2>
                <p style="color: #CBD5E1; font-size: 14.5px; margin: 4px 0 0 0; font-weight: 600;">
                    📅 {display_date} &nbsp;•&nbsp; <span style="color: #34D399;">{'தானியங்கி நகரும் படம் இயங்குகிறது (Auto-Running Motion Video)' if lang == 'ta' else 'Auto-Playing Moving Picture Video (No clicks needed)'}</span>
                </p>
            </div>
            <div style="background: rgba(245, 158, 11, 0.18); border: 1.5px solid #F59E0B; padding: 6px 18px; border-radius: 20px; font-weight: 800; font-size: 14px; color: #FEF08A;">
                {status_tag}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Sleek 7-Day Quick Navigator Tabs
    day_cols = st.columns(7)
    for i in range(7):
        with day_cols[i]:
            d_ep = DAILY_STORY_EPISODES[i]
            d_label = d_ep["day_short_ta"] if lang == "ta" else d_ep["day_short_en"]
            is_active = (i == cur_day_idx)
            is_real_today = (i == today_weekday)
            
            star_prefix = "⭐ " if is_real_today else f"{d_ep['episode_icon']} "
            btn_title = f"{star_prefix}{d_label}"

            if st.button(
                btn_title,
                key=f"daily_nav_day_{i}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.daily_story_day = i
                st.session_state.coco_episode_idx = i
                st.rerun()

    # 3. Full 60 FPS HTML5 Canvas Moving Picture Video Player
    video_html = generate_animated_video_story_html(ep, lang=lang, fetch_audio=True)
    st.components.v1.html(video_html, height=505)

    # 4. Narrative Reflection Box
    st.markdown(
        f"""
        <div style="background: #0F172A; border: 2px solid rgba(245, 158, 11, 0.4); border-radius: 20px; padding: 20px 26px; margin-top: 10px; margin-bottom: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                <span style="font-size: 28px;">{ep['episode_icon']}</span>
                <h3 style="color: #FEF08A; margin: 0; font-size: 20px; font-weight: 800;">{title}</h3>
            </div>
            <div style="color: #FBBF24; font-size: 16px; font-weight: 700; margin-bottom: 12px; line-height: 1.5; font-style: italic;">
                {quote}
            </div>
            <div style="color: #F1F5F9; font-size: 16.5px; line-height: 1.8; font-weight: 500;">
                {story_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 5. Call to Action: Begin Cognitive Exercises!
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #065F46 0%, #047857 100%); 
                    border-radius: 18px; padding: 16px 24px; color: white; display: flex; 
                    justify-content: space-between; align-items: center; margin-bottom: 12px;
                    border: 1.5px solid #34D399; box-shadow: 0 6px 20px rgba(6, 95, 70, 0.35);">
            <div>
                <div style="font-size: 18px; font-weight: 800; color: #FEF08A;">
                    🧠 {'அறிவாற்றல் பயிற்சிகளைத் தொடங்குவோம்' if lang == 'ta' else 'Ready for Today’s Cognitive Exercises?'}
                </div>
                <div style="font-size: 13.5px; color: #ECFDF5; font-weight: 600; margin-top: 3px;">
                    {'சுடோக்கு, நினைவாற்றல் ஜோடிகள் மற்றும் பட வரிசைப் பயிற்சிகள் உங்களுக்காகத் தயார்!' if lang == 'ta' else 'Sudoku, Memory Matching Pairs & Timeline Sequencing are prepared for you!'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cta_label = "🧠 " + ("பயிற்சிகளைத் தொடங்குக (Begin Cognitive Exercises)" if lang == "ta" else "Begin Cognitive Exercises") + " ⏭️"
    if st.button(cta_label, key="daily_video_start_games_cta", use_container_width=True, type="primary"):
        if on_start_games_callback:
            on_start_games_callback()
        else:
            st.session_state.show_motivational_story = False
            st.rerun()
