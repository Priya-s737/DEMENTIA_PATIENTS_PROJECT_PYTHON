"""
Adult-Appropriate Dignified Celebration Module for Correct Answers & Game Milestones.
Designed specifically for adults aged 40+, 50+, 60+, and seniors with MCI / Dementia.
Replaces childish cartoon animals and baby nursery rhymes with:
- Inspiring praise honoring cognitive clarity, wisdom, and lifelong accomplishments
- Elegant, luxurious visual motifs (golden laurels, blooming lotus, serene starlight)
- Warm, resonant acoustic chord synthesized via Web Audio API (soothing meditative chord)
- Pure native Tamil and English audio narration with dignified cadence
"""

import streamlit as st
import random
import os
import time
from typing import Dict, Any, Optional
from modules.voice_assistant import VoiceAssistant

# Inspiring, Respectful Praise Moments for Adults (40s, 50s, 60s, 70s+)
CELEBRATION_MOMENTS = [
    {
        "id": "clarity",
        "title_ta": "மனத்தெளிவும் கூர்மையான நினைவாற்றலும் 🌿",
        "title_en": "Cognitive Clarity & Sharp Recall 🌿",
        "text_ta": "அற்புதமான நினைவாற்றல்! அனுபவமும் கூர்மையான கவனமும் என்றும் நிலைத்திருக்கும் சிறந்த பலம். உங்கள் பதில் மிகச் சரியானது!",
        "text_en": "Outstanding cognitive clarity! Decades of experience and sharp attention shine through. That is the exact correct answer!",
        "motif": "🌿",
        "theme_color": "#059669",
        "badge_ta": "✨ கூர்மையான கவனம்",
        "badge_en": "✨ Sharp Focus"
    },
    {
        "id": "precision",
        "title_ta": "நேர்த்தியான முடிவும் ஆழ்ந்த அறிவாற்றலும் 🪷",
        "title_en": "Analytical Precision & Inner Poise 🪷",
        "text_ta": "நேர்த்தியான முடிவு! நிதானமான சிந்தனையும் தெளிவான அறிவாற்றலும் உங்கள் தனிச்சிறப்பு. உங்கள் பகுப்பாய்வு திறன் அருமை!",
        "text_en": "Masterful precision! Calm deliberation and clear reasoning are your hallmarks. Excellent analytical problem-solving!",
        "motif": "🪷",
        "theme_color": "#D97706",
        "badge_ta": "✨ ஆழ்ந்த சிந்தனை",
        "badge_en": "✨ Deep Intellect"
    },
    {
        "id": "vitality",
        "title_ta": "சுறுசுறுப்பான மனமும் புத்துணர்ச்சியும் ☕",
        "title_en": "Agile Mind & Intellectual Vitality ☕",
        "text_ta": "சிறப்பான சாதனை! சுறுசுறுப்பான மனமும் புத்துணர்ச்சியான கவனமும் என்றும் உங்கள் வாழ்வின் சிறந்த பொக்கிஷம்!",
        "text_en": "Brilliant achievement! Active intellectual vitality and deep concentration keep your mind agile, healthy, and sharp!",
        "motif": "☕",
        "theme_color": "#2563EB",
        "badge_ta": "✨ அறிவுப் புத்துணர்ச்சி",
        "badge_en": "✨ Mental Vitality"
    },
    {
        "id": "wisdom",
        "title_ta": "அனுபவத்தின் வெற்றியும் அறிவின் ஒளியும் 🌟",
        "title_en": "Triumph of Wisdom & Lifelong Intellect 🌟",
        "text_ta": "அனுபவத்தின் வெற்றி! நாற்பது ஆண்டுகளுக்கும் மேலான உங்கள் வாழ்வின் அனுபவம் என்றும் பெருமைக்குரியது. உங்கள் மனவலிமை சிறக்க வாழ்த்துகள்!",
        "text_en": "Triumph of intellect! Over four decades of rich life experience and wisdom illuminate your sharp focus with timeless grace.",
        "motif": "🌟",
        "theme_color": "#7C3AED",
        "badge_ta": "✨ அனுபவ முதிர்ச்சி",
        "badge_en": "✨ Lifelong Wisdom"
    }
]

# Backward compatibility alias
CELEBRATION_RHYMES = CELEBRATION_MOMENTS


def generate_celebration_stage_html(moment_data: Dict[str, Any], lang: str = "ta") -> str:
    """
    Constructs a sophisticated, mature celebration stage for adults:
    - Deep Midnight & Gold aesthetic
    - Floating golden aura particles and serene laurel motifs
    - Web Audio API soothing acoustic chord synthesizer (meditative, resonant)
    - Dignified audio praise narration in Tamil or English
    """
    text_content = moment_data["text_ta"] if lang == "ta" else moment_data["text_en"]
    title_content = moment_data["title_ta"] if lang == "ta" else moment_data["title_en"]
    badge_content = moment_data["badge_ta"] if lang == "ta" else moment_data["badge_en"]

    audio_src = VoiceAssistant.get_audio_base64_cached(text_content, lang=lang)

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

        .adult-celebration-box {{
            position: relative;
            width: 100%;
            height: 380px;
            border-radius: 24px;
            background: radial-gradient(circle at 50% 20%, #1E293B 0%, #0F172A 70%, #020617 100%);
            border: 3px solid #F59E0B;
            box-shadow: 0 16px 45px rgba(245, 158, 11, 0.25), inset 0 0 60px rgba(245, 158, 11, 0.08);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 24px 28px;
        }}

        /* Subtle Floating Gold Embers */
        .ember {{
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, #FDE68A 20%, #F59E0B 80%);
            opacity: 0.65;
            animation: floatEmber 6s infinite ease-in-out;
            pointer-events: none;
        }}
        .e-1 {{ width: 8px; height: 8px; left: 10%; bottom: -10px; animation-duration: 5.5s; }}
        .e-2 {{ width: 6px; height: 6px; left: 25%; bottom: -10px; animation-duration: 7s; animation-delay: 1s; }}
        .e-3 {{ width: 10px; height: 10px; right: 20%; bottom: -10px; animation-duration: 6.2s; animation-delay: 0.5s; }}
        .e-4 {{ width: 7px; height: 7px; right: 8%; bottom: -10px; animation-duration: 8s; animation-delay: 2s; }}

        @keyframes floatEmber {{
            0% {{ transform: translateY(0px) scale(0.8); opacity: 0; }}
            40% {{ opacity: 0.75; }}
            100% {{ transform: translateY(-400px) scale(1.2); opacity: 0; }}
        }}

        /* Dignified Emblem Header */
        .emblem-wrapper {{
            position: relative;
            z-index: 3;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
            border: 3px solid #FEF08A;
            box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4);
            animation: emblemPulse 3s infinite ease-in-out;
            font-size: 38px;
            cursor: pointer;
        }}
        @keyframes emblemPulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4); }}
            50% {{ transform: scale(1.08); box-shadow: 0 12px 32px rgba(245, 158, 11, 0.65); }}
        }}

        /* Respectful Praise Card */
        .praise-card {{
            position: relative;
            z-index: 4;
            width: 100%;
            max-width: 760px;
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(14px);
            border: 2px solid rgba(245, 158, 11, 0.5);
            border-radius: 20px;
            padding: 18px 26px;
            text-align: center;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        }}

        .praise-badge {{
            display: inline-block;
            background: rgba(245, 158, 11, 0.18);
            border: 1.5px solid #F59E0B;
            color: #FEF08A;
            font-weight: 800;
            font-size: 14.5px;
            letter-spacing: 0.3px;
            padding: 4px 18px;
            border-radius: 30px;
            margin-bottom: 8px;
        }}

        .praise-title {{
            color: #FFFFFF;
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }}

        .praise-text {{
            color: #E2E8F0;
            font-size: 16px;
            font-weight: 600;
            line-height: 1.6;
            margin-bottom: 12px;
        }}

        /* Audio & Melody Controls */
        .audio-actions {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
        }}

        .btn-mature {{
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: #FFFFFF;
            border: 1.5px solid #93C5FD;
            border-radius: 24px;
            padding: 8px 20px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .btn-mature:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5);
        }}

        .btn-chime {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            border-color: #FDE68A;
            color: #FFF;
        }}
        .btn-chime:hover {{
            box-shadow: 0 6px 18px rgba(217, 119, 6, 0.5);
        }}
    </style>
    </head>
    <body>
        <div class="adult-celebration-box">
            <!-- Subtle Gold Embers -->
            <div class="ember e-1"></div>
            <div class="ember e-2"></div>
            <div class="ember e-3"></div>
            <div class="ember e-4"></div>

            <!-- Central Dignified Emblem -->
            <div class="emblem-wrapper" onclick="playAcousticChord()">
                <span>{moment_data['motif']}</span>
            </div>

            <!-- Praise & Reflection Card -->
            <div class="praise-card">
                <div class="praise-badge">{badge_content}</div>
                <div class="praise-title">{title_content}</div>
                <div class="praise-text">“{text_content}”</div>

                <div class="audio-actions">
                    <button class="btn-mature" onclick="playVoiceNarration()">
                        <span id="play_icon">🔊</span>
                        <span id="play_label">{'குரல்வழிக் கருத்து' if lang == 'ta' else 'Listen to Commentary'}</span>
                    </button>
                    <button class="btn-mature btn-chime" onclick="playAcousticChord()">
                        <span>🔔</span>
                        <span>{'அமைதியான இசை' if lang == 'ta' else 'Serene Chime'}</span>
                    </button>
                </div>
            </div>

            <!-- Native Voice Audio Element -->
            {'<audio id="moment_audio" src="' + audio_src + '" preload="auto"></audio>' if audio_src else ''}

            <script>
                // Web Audio API - Soothing Meditative Acoustic Piano / Harp Chord (C Major 9)
                function playAcousticChord() {{
                    try {{
                        var AudioCtx = window.AudioContext || window.webkitAudioContext;
                        if (!AudioCtx) return;
                        var ctx = new AudioCtx();
                        // Warm, soothing, contemplative frequencies: C4 (261.63), E4 (329.63), G4 (392.00), B4 (493.88), D5 (587.33)
                        var frequencies = [261.63, 329.63, 392.00, 493.88, 587.33];
                        frequencies.forEach(function(freq, i) {{
                            var osc = ctx.createOscillator();
                            var gain = ctx.createGain();
                            osc.type = 'sine'; // pure, meditative sine tone
                            osc.frequency.setValueAtTime(freq, ctx.currentTime + (i * 0.12));
                            gain.gain.setValueAtTime(0, ctx.currentTime + (i * 0.12));
                            gain.gain.linearRampToValueAtTime(0.22, ctx.currentTime + (i * 0.12) + 0.05);
                            gain.gain.exponentialRampToValueAtTime(0.0005, ctx.currentTime + (i * 0.12) + 1.8);
                            osc.connect(gain);
                            gain.connect(ctx.destination);
                            osc.start(ctx.currentTime + (i * 0.12));
                            osc.stop(ctx.currentTime + (i * 0.12) + 1.9);
                        }});
                    }} catch (e) {{
                        console.log("Audio error:", e);
                    }}
                }}

                function playVoiceNarration() {{
                    playAcousticChord();
                    var aud = document.getElementById("moment_audio");
                    var lbl = document.getElementById("play_label");
                    var icn = document.getElementById("play_icon");
                    if (aud) {{
                        aud.currentTime = 0;
                        aud.play();
                        if (lbl) lbl.innerText = "{'கருத்து ஒலிக்கிறது...' if lang == 'ta' else 'Playing Voice...'}";
                        if (icn) icn.innerText = "🎶";
                        aud.onended = function() {{
                            if (lbl) lbl.innerText = "{'குரல்வழிக் கருத்து' if lang == 'ta' else 'Listen to Commentary'}";
                            if (icn) icn.innerText = "🔊";
                        }};
                    }}
                }}

                // Gentle chime on load
                window.addEventListener('load', function() {{
                    playAcousticChord();
                    setTimeout(function() {{
                        var aud = document.getElementById("moment_audio");
                        if (aud) aud.play().catch(function(e){{ console.log('Autoplay prevented', e); }});
                    }}, 350);
                }});
            </script>
        </div>
    </body>
    </html>
    """
    return html


def render_celebration(rhyme_idx: Optional[int] = None, lang: str = "ta", on_continue=None):
    """
    Displays the refined, adult-appropriate celebratory modal honoring accuracy and wisdom.
    """
    if rhyme_idx is None:
        rhyme_idx = random.randint(0, len(CELEBRATION_MOMENTS) - 1)

    moment_data = CELEBRATION_MOMENTS[rhyme_idx % len(CELEBRATION_MOMENTS)]

    # Rich Mature Celebration Stage with Acoustic Harmony & Voice Commentary
    st.components.v1.html(
        generate_celebration_stage_html(moment_data, lang=lang),
        height=390
    )

    # Dignified Continue Action
    c_left, c_mid, c_right = st.columns([1, 2, 1])
    with c_mid:
        cont_label = "🌟 " + ("அடுத்த நிலைக்குத் தொடரலாம் (Continue)" if lang == "ta" else "Continue to Next Challenge") + " ⏭️"
        if st.button(cont_label, key=f"adult_cel_btn_{time.time()}", use_container_width=True, type="primary"):
            if on_continue:
                on_continue()
            else:
                st.session_state.show_celebration = False
                st.rerun()
