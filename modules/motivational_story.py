"""
Adult-Appropriate Daily Cognitive Inspiration & Reminiscence Storytelling Module.
Tailored specifically for adults aged 40+, 50+, 60+, and seniors with MCI / Dementia.
Replaces childish cartoon themes with:
- Deeply relatable, life-affirming reminiscence stories honoring 40+ years of achievements
- Nostalgic themes: Morning coffee, classic music era, courtyard garden, wisdom & legacy
- Serene ambient animation: Dawn sunrise, steaming cup of brew, gentle jasmine petals, golden aura
- Pure native Tamil and English audio narration with dignified cadence
"""

import streamlit as st
import time
from typing import Dict, Any, List
from modules.voice_assistant import VoiceAssistant

# 4 Dignified, Nostalgic, Life-Affirming Stories for Adults (40s, 50s, 60s, 70s+)
COCOMELON_EPISODES = [
    {
        "id": "morning_coffee_walk",
        "title_en": "Part 1: The Golden Dawn, Morning Coffee & Peaceful Mindfulness",
        "title_ta": "பகுதி 1: காலை விடியலும் நறுமணக் காப்பியும் - அமைதியான தொடக்கம்",
        "quote_en": "“A quiet sunrise and the rich aroma of fresh brew bring timeless clarity, poise, and peace to the soul.”",
        "quote_ta": "“அமைதியான காலைப் பொழுதும், புதிய நறுமணக் காப்பியும் நம் மனதிற்குத் தெளிவையும் புத்துணர்ச்சியையும் தருகின்றன.”",
        "story_en": (
            "The first golden rays of dawn gently illuminate the quiet morning. "
            "A gentle breeze rustles through the courtyard trees, and distant birds welcome the new day. "
            "Savoring the comforting aroma of a fresh, warm cup of filter coffee, take a slow, deep breath. "
            "Your decades of hard work, family care, and perseverance are an inspiring legacy. "
            "There is no hurry today. Allow your thoughts to settle in quiet stillness, "
            "and let this morning nurture your clarity, focus, and peace."
        ),
        "story_ta": (
            "காலை விடியலின் மெல்லிய பொன் கதிர்கள் அமைதியாக பரவுகின்றன. "
            "தென்றல் காற்றில் மரங்களின் மெல்லிய சலசலப்பும், தூரத்தில் ஒலிக்கும் பறவைகளின் குரலும் மனதிற்கு ஒரு நிம்மதியான அமைதியைத் தருகின்றன. "
            "ஒரு குவளை சூடான நறுமணக் காப்பியின் இதத்தோடு, ஆழ்ந்த மூச்சை உள்ளிழுத்து நிதானமாக வெளிவிடுங்கள். "
            "நாற்பது ஆண்டுகளுக்கும் மேலான உங்கள் வாழ்வின் உழைப்பும், குடும்பப் பராமரிப்பும் என்றும் பெருமைக்குரியவை. "
            "இன்று எதற்கும் அவசரமில்லை; நிதானமான அமைதியோடு உங்கள் மனதிற்கும் சிந்தனைக்கும் புத்துணர்ச்சி தருவோம்!"
        ),
        "bg_theme": "radial-gradient(circle at 50% 30%, #1E293B 0%, #0F172A 70%, #020617 100%)",
        "episode_icon": "☕",
        "badge_en": "☕ Morning Mindfulness & Brew",
        "badge_ta": "☕ காலை அமைதியும் நறுமணக் காப்பியும்",
        "bubble_text_en": "Embrace the tranquility of a fresh morning dawn.",
        "bubble_text_ta": "காலை விடியலின் அமைதியை மனதார உணர்வோம்."
    },
    {
        "id": "golden_melodies",
        "title_en": "Part 2: Nostalgic Melodies & Cherished Life Milestones",
        "title_ta": "பகுதி 2: பொற்காலப் பாடல்களும் வாழ்வின் பொக்கிஷ நினைவுகளும்",
        "quote_en": "“Timeless melodies and cherished milestones keep our spirits forever vibrant, sharp, and joyful.”",
        "quote_ta": "“பழைய இனிய பாடல்களும் நினைவுகளும் என்றும் நம் உள்ளத்தில் இளமையையும் தெளிவையும் தக்கவைக்கின்றன.”",
        "story_en": (
            "A beloved classic melody from the golden era floats softly through the air, "
            "stirring a tapestry of unforgettable memories. "
            "College days, early professional triumphs, the joyful celebrations of marriage, "
            "and the sweet laughter of growing children. Every chapter of your journey holds wisdom and depth. "
            "Your memories are timeless treasures. Exercising your mind today keeps those cherished pathways "
            "agile, sharp, and glowing with pride."
        ),
        "story_ta": (
            "வானொலியில் ஒலிக்கும் பழைய பொற்காலக் கிளாசிக் பாடலின் மெல்லிசை நம் உள்ளத்தில் எத்தனையோ இனிய நினைவுகளை மீட்டெடுக்கிறது. "
            "கல்லூரி நாட்கள், வாழ்க்கையின் முதல் வெற்றி, குடும்பத்தின் மகிழ்ச்சியான தருணங்கள், குழந்தைகளின் மழலைச் சிரிப்பொலி என "
            "நீங்கள் கடந்து வந்த ஒவ்வொரு மைல்கல்லும் பொக்கிஷமானது. "
            "நினைவுகள் என்பது காலத்தால் அழியாத செல்வம்; நமது சுடோக்கு மற்றும் நினைவாற்றல் பயிற்சிகள் இந்த நினைவுகளை "
            "என்றும் கூர்மையாகவும் பசுமையாகவும் வைத்திருக்கும்!"
        ),
        "bg_theme": "radial-gradient(circle at 50% 30%, #312E81 0%, #1E1B4B 60%, #0F172A 100%)",
        "episode_icon": "🎵",
        "badge_en": "🎻 Golden Era Nostalgia",
        "badge_ta": "🎻 பொற்கால இசை நினைவுகள்",
        "bubble_text_en": "Precious memories keep the intellect forever young.",
        "bubble_text_ta": "இனிய நினைவுகள் அறிவை என்றும் இளமையாய் வைத்திருக்கும்."
    },
    {
        "id": "courtyard_garden",
        "title_en": "Part 3: The Verdant Courtyard Garden & Nature's Solace",
        "title_ta": "பகுதி 3: பசுமையான முற்றம், நறுமண மல்லிகை & இயற்கை அமைதி",
        "quote_en": "“Nature’s tranquility and the fragrance of blooming blossoms ground the mind with effortless focus and grace.”",
        "quote_ta": "“இயற்கையின் மடியில் அமைதியும், மல்லிகையின் நறுமணமும் மனதை நிதானமாகவும் ஒருமுகமாகவும் வைக்கின்றன.”",
        "story_en": (
            "Following a gentle evening shower, the refreshing scent of wet earth and fresh jasmine "
            "fills the open courtyard veranda. The lush green tulsi planter and sheltering mango boughs "
            "quiet the busy noise of the outside world. True cognitive brilliance flourishes not in haste, "
            "but in calm, centered focus. Close your eyes for a moment, feel your steady rhythm, "
            "and know that your mind possesses natural resilience and poise."
        ),
        "story_ta": (
            "மழை பெய்து ஓய்ந்த மாலை நேரத்தில், நனைந்த மண்ணின் நறுமணமும், முற்றத்து மல்லிகை மலர்களின் சுகந்தமும் காற்றில் தவழ்கின்றன. "
            "பசுமையான துளசி மாடமும், நிழல் தரும் மரங்களும் நம் எண்ணங்களை அமைதிப்படுத்துகின்றன. "
            "அவசரமில்லாத நிதானமான சிந்தனையே சிறந்த அறிவாற்றலின் அடித்தளம். "
            "ஒரு கணம் கண்களை மூடி இந்த அமைதியை உணருங்கள்; உங்கள் கவனமும் நினைவாற்றலும் இயல்பாகவே கூர்மையடையும்."
        ),
        "bg_theme": "radial-gradient(circle at 50% 30%, #064E3B 0%, #022C22 60%, #0F172A 100%)",
        "episode_icon": "🌿",
        "badge_en": "🌸 Courtyard Serenity & Jasmine",
        "badge_ta": "🌸 நறுமண மல்லிகையும் மன அமைதியும்",
        "bubble_text_en": "Calm mindfulness is the foundation of sharp cognition.",
        "bubble_text_ta": "நிதானமான அமைதியே கூர்மையான அறிவின் அடித்தளம்."
    },
    {
        "id": "wisdom_legacy",
        "title_en": "Part 4: Wisdom, Legacy & Cognitive Vitality",
        "title_ta": "பகுதி 4: வாழ்வின் அனுபவ முதிர்ச்சியும் அறிவாற்றல் பெருமையும்",
        "quote_en": "“Lifelong experience is the greatest wisdom; purposeful mental exercise keeps your intellect ever youthful and agile.”",
        "quote_ta": "“வாழ்வின் அனுபவம்தான் ஆகச்சிறந்த அறிவு; தொடர் பயிற்சியால் உங்கள் சிந்தனை என்றும் இளமையாக மின்னும்.”",
        "story_en": (
            "Over four decades of rich life experience is an extraordinary wealth that only time can bestow. "
            "Having steered through challenges, supported family, and contributed meaningfully to society, "
            "your cognitive depth commands the utmost respect. "
            "Just as a daily morning walk strengthens the heart, engaging in Sudoku and recall puzzles "
            "strengthens neural connections. Approach these exercises with pride, confidence, and peace."
        ),
        "story_ta": (
            "நாற்பத்தைந்து ஆண்டுகளுக்கு மேலான வாழ்வின் அனுபவம் என்பது எவராலும் எளிதில் பெற்றுவிட முடியாத மாபெரும் சொத்து. "
            "சவால்களை வென்று, குடும்பத்தையும் சமுதாயத்தையும் வழிநடத்திய உங்கள் சிந்தனைத் திறன் என்றும் போற்றத்தக்கது. "
            "உடலுக்கு நடைபயிற்சி போல, மூளைக்கு சுடோக்குவும் நினைவாற்றல் பயிற்சிகளும் ஒரு புத்துணர்வு விருந்து. "
            "முழு தன்னம்பிக்கையுடனும் மகிழ்ச்சியுடனும் வாருங்கள், இன்றைய பயிற்சிகளைத் தொடங்குவோம்!"
        ),
        "bg_theme": "radial-gradient(circle at 50% 30%, #78350F 0%, #451A03 60%, #0F172A 100%)",
        "episode_icon": "🌟",
        "badge_en": "🏆 Wisdom & Mental Agility",
        "badge_ta": "🏆 அனுபவ முதிர்ச்சியும் கூர்மையான அறிவும்",
        "bubble_text_en": "Honoring a lifetime of wisdom and intellectual strength.",
        "bubble_text_ta": "உங்கள் வாழ்வின் அனுபவத்திற்கு எங்கள் மரியாதைக்குரிய வணக்கம்."
    }
]

# Backward compatibility alias
MATURE_ADULT_EPISODES = COCOMELON_EPISODES


def generate_cocomelon_stage_html(episode: Dict[str, Any], lang: str) -> str:
    """
    Constructs an elegant, serene adult mindfulness stage.
    Features:
    - Serene dawn horizon with radiant glowing sunrise (no cartoon faces)
    - Steaming cup of morning brew with rising aroma vapors (☕)
    - Subtle floating golden embers, leaves, and gentle light rays
    - Dignified serif quotes and badges
    - Web Audio API calming tanpura / piano harmony
    """
    bubble_text = episode["bubble_text_ta"] if lang == "ta" else episode["bubble_text_en"]
    badge_text = episode["badge_ta"] if lang == "ta" else episode["badge_en"]

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

        .adult-theater-box {{
            position: relative;
            width: 100%;
            height: 340px;
            border-radius: 24px;
            background: {episode['bg_theme']};
            border: 3px solid rgba(245, 158, 11, 0.6);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 35px;
        }}

        /* Radiant Sun */
        .serene-sun {{
            position: absolute;
            top: 25px;
            right: 45px;
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: radial-gradient(circle, #FEF08A 20%, #F59E0B 75%, #D97706 100%);
            box-shadow: 0 0 45px rgba(245, 158, 11, 0.65), 0 0 90px rgba(245, 158, 11, 0.35);
            animation: sunGlow 5s infinite ease-in-out;
            z-index: 2;
        }}
        @keyframes sunGlow {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 45px rgba(245, 158, 11, 0.65); }}
            50% {{ transform: scale(1.06); box-shadow: 0 0 65px rgba(245, 158, 11, 0.85); }}
        }}

        /* Steaming Cup Motif */
        .steam-motif {{
            position: relative;
            z-index: 4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: rgba(30, 41, 59, 0.7);
            border: 2px solid rgba(245, 158, 11, 0.5);
            backdrop-filter: blur(8px);
            font-size: 54px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            animation: cupFloat 4s infinite ease-in-out;
        }}
        @keyframes cupFloat {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-8px); }}
        }}

        /* Subtle Floating Particles */
        .particle {{
            position: absolute;
            border-radius: 50%;
            background: #FDE68A;
            opacity: 0.6;
            animation: floatUp 7s infinite ease-in-out;
            pointer-events: none;
        }}
        .p1 {{ width: 5px; height: 5px; left: 15%; bottom: -10px; animation-delay: 0.5s; }}
        .p2 {{ width: 8px; height: 8px; left: 35%; bottom: -10px; animation-delay: 2s; }}
        .p3 {{ width: 6px; height: 6px; right: 30%; bottom: -10px; animation-delay: 1.2s; }}
        .p4 {{ width: 7px; height: 7px; right: 15%; bottom: -10px; animation-delay: 3s; }}

        @keyframes floatUp {{
            0% {{ transform: translateY(0px); opacity: 0; }}
            40% {{ opacity: 0.7; }}
            100% {{ transform: translateY(-360px); opacity: 0; }}
        }}

        /* Center Reflective Card */
        .center-card {{
            position: relative;
            z-index: 4;
            flex: 1;
            margin-left: 28px;
            margin-right: 90px;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border: 2px solid rgba(245, 158, 11, 0.45);
            border-radius: 20px;
            padding: 18px 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }}

        .card-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid #F59E0B;
            color: #FEF08A;
            font-size: 13px;
            font-weight: 800;
            padding: 3px 14px;
            border-radius: 20px;
            margin-bottom: 8px;
        }}

        .card-quote {{
            color: #FFFFFF;
            font-size: 17px;
            font-weight: 700;
            line-height: 1.5;
            margin-bottom: 8px;
            font-style: italic;
        }}

        .card-subtext {{
            color: #CBD5E1;
            font-size: 14.5px;
            font-weight: 500;
        }}

        .melody-btn {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            color: white;
            border: 1.5px solid #FDE68A;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 10px;
            box-shadow: 0 3px 10px rgba(217, 119, 6, 0.35);
            transition: all 0.2s ease;
        }}
        .melody-btn:hover {{
            transform: scale(1.04);
        }}
    </style>
    </head>
    <body>
        <div class="adult-theater-box">
            <!-- Radiant Dawn Sun -->
            <div class="serene-sun"></div>

            <!-- Gentle Rising Particles -->
            <div class="particle p1"></div>
            <div class="particle p2"></div>
            <div class="particle p3"></div>
            <div class="particle p4"></div>

            <!-- Steaming Cup / Motif -->
            <div class="steam-motif" onclick="playAmbientChord()">
                <span>{episode['episode_icon']}</span>
            </div>

            <!-- Center Reflective Story Card -->
            <div class="center-card">
                <div class="card-pill">{badge_text}</div>
                <div class="card-quote">“{episode['quote_ta' if lang == 'ta' else 'quote_en']}”</div>
                <div class="card-subtext">{bubble_text}</div>
                <div>
                    <button class="melody-btn" onclick="playAmbientChord()">
                        <span>🎵</span>
                        <span>{'அமைதியான பாரம்பரிய இசை' if lang == 'ta' else 'Play Soothing Melody'}</span>
                    </button>
                </div>
            </div>
        </div>

        <script>
            // Ambient Meditative Tanpura / Classical Piano Chord (C-G-C-E)
            function playAmbientChord() {{
                try {{
                    var AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtx) return;
                    var ctx = new AudioCtx();
                    var freqs = [130.81, 196.00, 261.63, 329.63, 392.00];
                    freqs.forEach(function(freq, i) {{
                        var osc = ctx.createOscillator();
                        var gain = ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freq, ctx.currentTime + (i * 0.1));
                        gain.gain.setValueAtTime(0, ctx.currentTime + (i * 0.1));
                        gain.gain.linearRampToValueAtTime(0.18, ctx.currentTime + (i * 0.1) + 0.08);
                        gain.gain.exponentialRampToValueAtTime(0.0005, ctx.currentTime + (i * 0.1) + 2.2);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(ctx.currentTime + (i * 0.1));
                        osc.stop(ctx.currentTime + (i * 0.1) + 2.3);
                    }});
                }} catch (e) {{}}
            }}
        </script>
    </body>
    </html>
    """
    return html


def generate_login_cocomelon_hero_html(lang: str = "en") -> str:
    """
    Constructs a sophisticated, executive-grade Adult Health & Longevity hero banner for the login screen.
    Includes:
    - Midnight & Gold palette with radiant dawn glow
    - Warm steam coffee & mindfulness motifs
    - Dignified adult welcome honoring decades of wisdom and resilience
    - Web Audio API soothing chord button
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

        /* Dawn Glow */
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

        /* Emblem Motif */
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

        /* Text Area */
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

            <!-- Left Coffee / Wisdom Motif -->
            <div class="hero-emblem" onclick="playLoginChord()">
                <span>☕</span>
            </div>

            <!-- Center Content -->
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


# Alias for backward compatibility
generate_login_adult_hero_html = generate_login_cocomelon_hero_html


def render_motivational_story(lang: str = "en", on_start_games_callback=None):
    """
    Renders the adult-appropriate daily reminiscence and mindfulness story theater
    with 100% audible native Tamil & English voice audio.
    """
    if "coco_episode_idx" not in st.session_state:
        st.session_state.coco_episode_idx = 0

    ep_idx = st.session_state.coco_episode_idx
    ep = COCOMELON_EPISODES[ep_idx]

    title = ep["title_ta"] if lang == "ta" else ep["title_en"]
    quote = ep["quote_ta"] if lang == "ta" else ep["quote_en"]
    story_text = ep["story_ta"] if lang == "ta" else ep["story_en"]

    # Dignified Header Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 60%, #020617 100%); 
                    padding: 18px 24px; border-radius: 20px; color: white; margin-bottom: 15px; 
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35); border-left: 6px solid #F59E0B;
                    border: 1px solid rgba(245, 158, 11, 0.4);
                    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h2 style="color: #FEF08A; margin: 0; font-size: 22px; font-weight: 800; display: flex; align-items: center; gap: 10px;">
                    <span>🌿</span> {'தினசரி மன அமைதி & நினைவாற்றல் உத்வேகக் கதை' if lang == 'ta' else 'Daily Reminiscence & Cognitive Mindfulness Story'}
                </h2>
                <p style="color: #CBD5E1; font-size: 14.5px; margin: 4px 0 0 0; font-weight: 600;">
                    {'40+ நடுத்தர வயதினர் மற்றும் முதியோருக்கான வாழ்வின் அனுபவ நினைவுகளும் மனத்தெளிவும்' if lang == 'ta' else 'Calming Reminiscence, Life Wisdom & Mindfulness Tailored for Adults & Seniors (40+)'}
                </p>
            </div>
            <div style="background: rgba(245, 158, 11, 0.2); border: 1.5px solid #F59E0B; padding: 6px 18px; border-radius: 20px; font-weight: 800; font-size: 15px; color: #FEF08A;">
                {ep_idx + 1} / {len(COCOMELON_EPISODES)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render Refined Ambient Stage
    stage_html = generate_cocomelon_stage_html(ep, lang)
    st.components.v1.html(stage_html, height=355)

    # Narrative Reflection Box
    st.markdown(
        f"""
        <div style="background: #0F172A; border: 2px solid rgba(245, 158, 11, 0.5); border-radius: 20px; padding: 24px 28px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 32px;">{ep['episode_icon']}</span>
                <h3 style="color: #FEF08A; margin: 0; font-size: 21px; font-weight: 800;">{title}</h3>
            </div>
            <div style="color: #FBBF24; font-size: 17px; font-weight: 700; margin-bottom: 14px; line-height: 1.5; font-style: italic;">
                {quote}
            </div>
            <div style="color: #F1F5F9; font-size: 17.5px; line-height: 1.85; font-weight: 500;">
                {story_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 100% Audible Native Tamil & English Audio Commentary
    audio_full_text = f"{title}. {quote}. {story_text}"
    audio_bytes = VoiceAssistant.get_audio_bytes(audio_full_text, lang=lang)

    col_audio_btn, col_native_audio = st.columns([1.2, 1.8])
    with col_audio_btn:
        st.components.v1.html(
            VoiceAssistant.get_speech_html(audio_full_text, lang=lang),
            height=72
        )
    with col_native_audio:
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")

    # Navigation Controls
    col_prev, col_dots, col_next = st.columns([1.5, 2, 1.5])
    
    with col_prev:
        prev_label = "⏮️ " + ("முந்தைய பகுதி" if lang == "ta" else "Previous Part")
        if st.button(prev_label, use_container_width=True, disabled=(ep_idx == 0), key="adult_story_prev_btn"):
            st.session_state.coco_episode_idx = max(0, ep_idx - 1)
            st.rerun()

    with col_dots:
        pill_cols = st.columns(len(COCOMELON_EPISODES))
        for i in range(len(COCOMELON_EPISODES)):
            with pill_cols[i]:
                is_cur = (i == ep_idx)
                pill_label = f"{COCOMELON_EPISODES[i]['episode_icon']} {i+1}"
                if st.button(
                    pill_label, 
                    key=f"adult_story_pill_{i}", 
                    use_container_width=True,
                    type="primary" if is_cur else "secondary"
                ):
                    st.session_state.coco_episode_idx = i
                    st.rerun()

    with col_next:
        if ep_idx < len(COCOMELON_EPISODES) - 1:
            next_label = ("அடுத்த பகுதி" if lang == "ta" else "Next Part") + " ⏭️"
            if st.button(next_label, use_container_width=True, key="adult_story_next_btn"):
                st.session_state.coco_episode_idx = ep_idx + 1
                st.rerun()
        else:
            first_label = "🔄 " + ("மீண்டும் வாசிக்க" if lang == "ta" else "Read Again")
            if st.button(first_label, use_container_width=True, key="adult_story_restart_btn"):
                st.session_state.coco_episode_idx = 0
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Dignified Call to Action: Begin Cognitive Exercises!
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #065F46 0%, #047857 100%); 
                    border-radius: 18px; padding: 18px 26px; color: white; display: flex; 
                    justify-content: space-between; align-items: center; margin-bottom: 12px;
                    border: 1.5px solid #34D399; box-shadow: 0 6px 20px rgba(6, 95, 70, 0.35);">
            <div>
                <div style="font-size: 19px; font-weight: 800; color: #FEF08A;">
                    🧠 {'அறிவாற்றல் பயிற்சிகளைத் தொடங்கலாம்' if lang == 'ta' else 'Ready for Today’s Cognitive Exercises?'}
                </div>
                <div style="font-size: 14px; color: #ECFDF5; font-weight: 600; margin-top: 3px;">
                    {'சுடோக்கு, நினைவாற்றல் ஜோடிகள் மற்றும் காலவரிசைப் பயிற்சிகள் உங்களுக்காகத் தயார்!' if lang == 'ta' else 'Sudoku, Memory Matching Pairs & Timeline Sequencing are prepared for you!'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cta_label = "🧠 " + ("பயிற்சிகளைத் தொடங்குக (Begin Cognitive Exercises)" if lang == "ta" else "Begin Cognitive Exercises") + " ⏭️"
    if st.button(cta_label, key="adult_story_start_games_cta", use_container_width=True, type="primary"):
        if on_start_games_callback:
            on_start_games_callback()
        else:
            st.session_state.show_motivational_story = False
            st.rerun()
