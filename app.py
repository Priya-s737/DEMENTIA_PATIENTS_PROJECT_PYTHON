"""
NeuroCare: Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients.
Role-Based Clinical Portal (Admin, Caregiver, Senior Mode) with Custom Image Uploads.
100% Strict Bilingual Localization (Pure Tamil & Pure English).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import shutil
from datetime import datetime
from PIL import Image

from config import APP_NAME, APP_SUBTITLE, VERSION, AUTHORS, INSTITUTION, COGNITIVE_DOMAINS, TRANSLATIONS, THEMES
from database.db_manager import DatabaseManager
from database.mock_data import seed_database_if_empty
from modules.personalization import PersonalizationEngine
from modules.adaptive_engine import AdaptiveDifficultyEngine, AdaptiveDecision
from modules.voice_assistant import VoiceAssistant
from modules.research_stats import ResearchStatsEngine

from games.memory_games import render_memory_game
from games.memory_increment_game import render_memory_increment_game
from games.memory_pairs_game import render_memory_pairs_game
from games.sudoku_game import render_sudoku_game
from games.attention_games import render_attention_game
from games.orientation_games import render_orientation_game
from games.language_games import render_language_game
from modules.motivational_story import render_motivational_story, generate_login_cocomelon_hero_html
from modules.celebration import render_celebration

# Page Setup
st.set_page_config(
    page_title="NeuroCare Health Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Storage & Database
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

db = DatabaseManager()
seed_database_if_empty(db)
personalization = PersonalizationEngine(db)
adaptive_engine = AdaptiveDifficultyEngine()
research_engine = ResearchStatsEngine()

# Custom Lively Animated Styling for Healthcare & Senior Application
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Mukta+Malar:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Mukta Malar', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* 1. ANIMATED TOP PORTAL HEADER */
    .portal-header {
        background: linear-gradient(-45deg, #1E3A8A, #2563EB, #0284C7, #0D9488);
        background-size: 300% 300%;
        animation: gradientShift 10s ease infinite;
        padding: 20px;
        border-radius: 16px;
        color: white;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .user-badge {
        background-color: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        animation: badgePulse 3s infinite ease-in-out;
    }
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 rgba(255,255,255,0); }
        50% { transform: scale(1.04); box-shadow: 0 0 12px rgba(255,255,255,0.4); }
    }

    /* 2. LIVELY BOUNCY ANIMATIONS ON ALL BUTTONS ACROSS THE ENTIRE APP */
    .stButton>button {
        font-size: 17px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        min-height: 48px !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4) !important;
    }
    .stButton>button:active {
        transform: scale(0.96) !important;
    }

    /* Primary Buttons Radiant Pulse */
    button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: 2px solid #60A5FA !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4) !important;
        animation: primaryBtnPulse 3s infinite ease-in-out !important;
    }
    @keyframes primaryBtnPulse {
        0%, 100% { box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4); }
        50% { box-shadow: 0 8px 24px rgba(96, 165, 250, 0.65); transform: translateY(-1px); }
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: translateY(-4px) scale(1.04) !important;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6) !important;
    }

    /* Secondary Buttons Styling & Animation */
    button[kind="secondary"] {
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    button[kind="secondary"]:hover {
        transform: translateY(-3px) scale(1.025) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.18) !important;
    }

    /* 3. LIVELY ANIMATIONS FOR ALL OPTION CARDS & IMAGES ACROSS ALL GAMES */
    div[data-testid="stColumn"] div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #1E293B !important;
        border: 2px solid #334155 !important;
        border-radius: 16px !important;
        padding: 14px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: center !important;
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="stColumn"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-6px) scale(1.025) !important;
        border-color: #60A5FA !important;
        box-shadow: 0 16px 32px rgba(37, 99, 235, 0.35) !important;
    }

    div[data-testid="stColumn"] [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        border-radius: 12px !important;
    }
    div[data-testid="stColumn"] [data-testid="stImage"] img {
        height: 190px !important;
        width: 100% !important;
        max-height: 190px !important;
        min-height: 190px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        display: block !important;
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div[data-testid="stColumn"] div[data-testid="stVerticalBlockBorderWrapper"]:hover img {
        transform: scale(1.06) !important;
    }

    div[data-testid="stColumn"] div.stButton {
        width: 100% !important;
        margin-top: 10px !important;
    }
    div[data-testid="stColumn"] div.stButton > button {
        font-size: 18px !important;
        font-weight: 800 !important;
        height: 52px !important;
        min-height: 52px !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
        background: #0F172A !important;
        color: #F8FAFC !important;
        border: 2px solid #3B82F6 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div[data-testid="stColumn"] div.stButton > button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
        border-color: #93C5FD !important;
        color: #FFFFFF !important;
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.45) !important;
    }

    /* 4. HIGH CONTRAST SUBHEADINGS & CAPTIONS FOR LOW VISION */
    .stCaption, 
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    .stMarkdown p.subheading {
        color: #1E3A8A !important; /* Deep Royal Navy Blue - maximum readable contrast */
        font-size: 16px !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
    }

    /* 5. GLOWING HIGH-CONTRAST METRICS CARDS (ELDERLY ACCESSIBLE) */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        border: 2px solid #38BDF8 !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.4) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        border-color: #60A5FA !important;
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.35) !important;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] *,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
        color: #93C5FD !important; /* Crisp Pastel Sky Blue */
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.4px !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] *,
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] > div {
        color: #FEF08A !important; /* Radiant Warm Gold */
        font-size: 28px !important;
        font-weight: 900 !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
    }

    /* 6. HIGH CONTRAST RADIO BUTTON LABELS */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label p {
        color: #0F172A !important; /* Deep dark bold text */
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    /* 7. TABS ANIMATION */
    button[data-baseweb="tab"] {
        transition: all 0.25s ease !important;
        font-weight: 800 !important;
        font-size: 16px !important;
    }
    button[data-baseweb="tab"]:hover {
        transform: translateY(-2px) !important;
        color: #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State for Authentication, Language, and Selected Game
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None
if "senior_mode_active" not in st.session_state:
    st.session_state.senior_mode_active = False
if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = None
if "app_lang" not in st.session_state:
    st.session_state.app_lang = "ta"  # Default to Tamil
if "active_game_key" not in st.session_state:
    st.session_state.active_game_key = "face_recall"
if "show_motivational_story" not in st.session_state:
    st.session_state.show_motivational_story = True

lang = st.session_state.app_lang
t = TRANSLATIONS[lang]

# Helper for resetting stimuli on state changes
def clear_all_stimuli():
    st.session_state.mem_stimulus = None
    st.session_state.mem_feedback = None
    st.session_state.mem_span_target_seq = []
    st.session_state.mem_span_user_seq = []
    st.session_state.mem_span_phase = "memorize"
    st.session_state.att_stimulus = None
    st.session_state.att_feedback = None
    st.session_state.tmt_state = None
    st.session_state.ori_stimulus = None
    st.session_state.ori_spatial_stim = None
    st.session_state.ori_feedback = None
    st.session_state.lang_stimulus = None
    st.session_state.lang_cat_stim = None
    st.session_state.lang_feedback = None
    st.session_state.sudoku_board = None
    st.session_state.sudoku_initial_board = None
    st.session_state.sudoku_history = []
    st.session_state.sudoku_completed = False
    st.session_state.sudoku_conflict_message = None
    st.session_state.sudoku_hint_message = None
    st.session_state.pairs_deck = None
    st.session_state.pairs_flipped = []
    st.session_state.pairs_matched = set()
    st.session_state.pairs_moves = 0
    st.session_state.pairs_completed = False
    st.session_state.pairs_feedback = None

# ==============================================================================
# 🔐 AUTHENTICATION GATE (IF NOT LOGGED IN) - ADULT COGNITIVE LONGEVITY SUITE
# ==============================================================================
if not st.session_state.auth_user and not st.session_state.senior_mode_active:
    # Sophisticated Adult Theme CSS: Deep Midnight, Slate & Warm Gold Palette
    st.markdown("""
    <style>
    /* Fullscreen Dignified Adult Wellness Palette */
    [data-testid="stAppViewContainer"], .stApp {
        background: radial-gradient(circle at 50% 15%, #1E293B 0%, #0F172A 55%, #020617 100%) !important;
        background-attachment: fixed !important;
        min-height: 100vh !important;
        color: #F8FAFC !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    .main .block-container {
        max-width: 1280px !important;
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
    }

    /* Subtle Ambient Floating Gold Embers */
    @keyframes riseEmberSlow {
        0% { transform: translateY(105vh) scale(0.8); opacity: 0; }
        40% { opacity: 0.6; }
        100% { transform: translateY(-100px) scale(1.2); opacity: 0; }
    }
    .bg-ember {
        position: fixed;
        border-radius: 50%;
        background: radial-gradient(circle, #FDE68A 20%, #F59E0B 80%);
        z-index: 0;
        pointer-events: none;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
    }
    .be-1 { left: 6%; width: 6px; height: 6px; animation: riseEmberSlow 16s infinite linear 0.5s; }
    .be-2 { left: 18%; width: 8px; height: 8px; animation: riseEmberSlow 20s infinite linear 4s; }
    .be-3 { left: 32%; width: 5px; height: 5px; animation: riseEmberSlow 18s infinite linear 2s; }
    .be-4 { right: 28%; width: 7px; height: 7px; animation: riseEmberSlow 19s infinite linear 5s; }
    .be-5 { right: 14%; width: 6px; height: 6px; animation: riseEmberSlow 15s infinite linear 1s; }
    .be-6 { right: 4%; width: 8px; height: 8px; animation: riseEmberSlow 22s infinite linear 7s; }

    /* Frosted Midnight Glassmorphism */
    .adult-portal-card {
        background: rgba(15, 23, 42, 0.88) !important;
        backdrop-filter: blur(16px) !important;
        border: 2px solid rgba(245, 158, 11, 0.45) !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
        padding: 24px 28px !important;
        margin-top: 12px !important;
    }
    
    /* Executive Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 23, 42, 0.95);
        padding: 8px 12px;
        border-radius: 20px;
        border: 1.5px solid rgba(245, 158, 11, 0.35);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 15.5px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        border-radius: 14px !important;
        padding: 10px 22px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #FEF08A !important;
        border: 1px solid rgba(245, 158, 11, 0.6) !important;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.2) !important;
    }
    </style>
    
    <!-- Subtle Golden Embers across entire viewport -->
    <div class="bg-ember be-1"></div>
    <div class="bg-ember be-2"></div>
    <div class="bg-ember be-3"></div>
    <div class="bg-ember be-4"></div>
    <div class="bg-ember be-5"></div>
    <div class="bg-ember be-6"></div>
    """, unsafe_allow_html=True)

    # Top Language Switcher Bar on Login Page
    top_c1, top_c2 = st.columns([3, 1.2])
    with top_c1:
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.85); border-radius: 20px; padding: 8px 20px; 
                        display: inline-flex; align-items: center; gap: 12px; border: 1.5px solid rgba(245, 158, 11, 0.4);
                        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);">
                <span style="font-size: 26px;">🧠</span>
                <span style="color: #FEF08A; font-weight: 900; font-size: 18px; letter-spacing: 0.2px;">NeuroCare Longevity Suite</span>
                <span style="color: #94A3B8; font-size: 13.5px; font-weight: 600;">• {'40+ நடுத்தர வயதினர் & முதியோருக்கான அறிவாற்றல் நலவாழ்வு தளம்' if lang == 'ta' else 'Cognitive Longevity & Memory Wellness for Adults (40+)'}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_c2:
        if st.session_state.app_lang == "ta":
            if st.button("🌐 Switch to English", key="login_lang_en_btn", use_container_width=True):
                st.session_state.app_lang = "en"
                clear_all_stimuli()
                st.rerun()
        else:
            if st.button("🌐 தமிழுக்கு மாற்றவும்", key="login_lang_ta_btn", use_container_width=True):
                st.session_state.app_lang = "ta"
                clear_all_stimuli()
                st.rerun()

    # Full-Width Dignified Adult Health & Longevity Hero Banner
    st.components.v1.html(generate_login_cocomelon_hero_html(lang=lang), height=230)

    # Interactive Fullscreen Portal Container
    c_left, c_mid, c_right = st.columns([0.08, 3.84, 0.08])
    with c_mid:
        # TABS: Senior & Adult Patient Launchpad FIRST as the primary 1-tap option!
        auth_tab_senior, auth_tab_caregiver, auth_tab_admin = st.tabs([
            f"🌿 {'நேரடி தொடக்கம் (1-Tap Direct Play)' if lang == 'ta' else 'Adult & Senior Launchpad (1-Tap Play)'}",
            f"👨‍⚕️ {'பராமரிப்பாளர் நுழைவு' if lang == 'ta' else 'Caregiver Access'}",
            f"🛡️ {'மருத்துவ நிபுணர்' if lang == 'ta' else 'Clinical Specialist Login'}"
        ])

        # ----------------------------------------------------------------------
        # TAB 1: ADULT & SENIOR DIRECT LAUNCHPAD (PRIMARY)
        # ----------------------------------------------------------------------
        with auth_tab_senior:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%); 
                            border: 2px solid rgba(245, 158, 11, 0.45); border-radius: 18px; padding: 18px 24px; 
                            margin-top: 10px; margin-bottom: 16px; display: flex; align-items: center; gap: 16px;
                            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);">
                    <span style="font-size: 38px;">🌿</span>
                    <div>
                        <div style="color: #FEF08A; font-weight: 800; font-size: 17px;">
                            {'வணக்கம்! எவ்வித கடவுச்சொல்லும் இன்றி நேரடியாக 1-கிளிக்கில் பயிற்சிகளைத் தொடங்கலாம்!' if lang == 'ta' else 'Welcome! Begin daily cognitive fitness exercises directly with one tap, no password required.'}
                        </div>
                        <div style="color: #CBD5E1; font-weight: 600; font-size: 14px; margin-top: 3px;">
                            {'நினைவாற்றல் ஜோடிகள், சுடோக்கு மற்றும் வாழ்வின் அனுபவ நினைவூட்டல் பயிற்சிகள் உங்களுக்காகத் தயார் ☕ 🌿' if lang == 'ta' else 'Memory Matching Pairs, Sudoku puzzles & Life Reminiscence exercises are ready for your daily routine ☕ 🌿'}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Showcase patient profiles with dignified adult professional backgrounds
            patients = db.get_all_patients()
            
            p_cols = st.columns(min(3, len(patients)))
            patient_descriptions = {
                1: ("ஓய்வுபெற்ற பேராசிரியர் • கர்நாடக இசை & கோயில் கலைகள்", "Retired Professor • Carnatic Music & Temple Architecture"),
                2: ("முன்னாள் பள்ளி முதல்வர் • வீட்டுத் தோட்டம் & குடும்ப நினைவுகள்", "Former Principal • Gardening & Family Reminiscence"),
                3: ("மூத்த மருத்துவர் • பழைய ரயில் பயணம் & செவ்வியல் இலக்கியம்", "Senior Physician • Vintage Rail & Classical Literature"),
                4: ("கார்ப்பரேட் மேலாண்மை • மன ஒருமைப்பாடு & புத்துணர்ச்சி", "Corporate Executive • Cognitive Focus & Resilience")
            }
            
            for idx, p in enumerate(patients[:3]):
                with p_cols[idx]:
                    desc_ta, desc_en = patient_descriptions.get(p["id"], ("அறிவாற்றல் நலவாழ்வு", "Cognitive Wellness"))
                    is_sel = (st.session_state.selected_patient_id == p["id"]) if "selected_patient_id" in st.session_state else (idx == 0)
                    border_color = "#F59E0B" if is_sel else "rgba(148, 163, 184, 0.3)"
                    bg_color = "rgba(30, 41, 59, 0.9)" if is_sel else "rgba(15, 23, 42, 0.75)"
                    p_cond = p.get("condition", "Cognitive Wellness")
                    
                    st.markdown(
                        f"""
                        <div style="background: {bg_color}; border: 2.5px solid {border_color}; 
                                    border-radius: 18px; padding: 16px 18px; text-align: center;
                                    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25); min-height: 165px;
                                    display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="font-size: 38px; margin-bottom: 4px;">{'👨‍🏫' if p['id']==1 else ('👩‍🏫' if p['id']==2 else '👨‍⚕️')}</div>
                                <div style="color: #FFFFFF; font-weight: 800; font-size: 16.5px;">{p['name']}</div>
                                <div style="color: #38BDF8; font-weight: 700; font-size: 13px;">{p['age']} {'வயது' if lang == 'ta' else 'yrs'} • {p_cond}</div>
                            </div>
                            <div style="color: #CBD5E1; font-size: 12.5px; font-weight: 600; margin-top: 8px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 4px 8px;">
                                💡 {desc_ta if lang == 'ta' else desc_en}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            p_opts = {f"{p['name']} ({p['age']} {'வயது' if lang == 'ta' else 'yrs'} - {p.get('condition', '')})": p["id"] for p in patients}
            chosen_p_label = st.selectbox("பயிற்சி செய்ய விரும்பும் சுயவிவரத்தைத் தேர்ந்தெடுக்கவும்" if lang == "ta" else "Select Profile for Today's Cognitive Session", list(p_opts.keys()))

            c_p_btn1, c_p_btn2 = st.columns(2)
            with c_p_btn1:
                if st.button("▶️ தமிழில் பயிற்சிகளைத் தொடங்குங்கள் 🌿", use_container_width=True, type="primary"):
                    st.session_state.app_lang = "ta"
                    st.session_state.selected_patient_id = p_opts[chosen_p_label]
                    clear_all_stimuli()
                    st.session_state.senior_mode_active = True
                    st.session_state.show_motivational_story = True
                    st.rerun()
            with c_p_btn2:
                if st.button("▶️ Begin Cognitive Exercises in English 🌟", use_container_width=True, type="primary"):
                    st.session_state.app_lang = "en"
                    st.session_state.selected_patient_id = p_opts[chosen_p_label]
                    clear_all_stimuli()
                    st.session_state.senior_mode_active = True
                    st.session_state.show_motivational_story = True
                    st.rerun()

        # ----------------------------------------------------------------------
        # TAB 2: CAREGIVER LOGIN / REGISTER
        # ----------------------------------------------------------------------
        with auth_tab_caregiver:
            st.subheader("👨‍⚕️ " + ("பராமரிப்பாளர் உள்நுழைவு" if lang == "ta" else "Caregiver Access"))
            with st.form("caregiver_login_form"):
                c_user = st.text_input("பயனர் பெயர்" if lang == "ta" else "Caregiver Username", placeholder="e.g. caregiver", value="caregiver")
                c_pass = st.text_input("கடவுச்சொல்" if lang == "ta" else "Password", type="password", placeholder="••••••••", value="Caregiver@123")
                c_sub = st.form_submit_button("🔑 " + ("உள்நுழைக" if lang == "ta" else "Log In as Caregiver"), use_container_width=True)

                if c_sub:
                    user = db.authenticate_user(c_user, c_pass)
                    if user and user["role"] == "caregiver":
                        st.session_state.auth_user = user
                        st.session_state.senior_mode_active = False
                        clear_all_stimuli()
                        st.toast(f"{'வணக்கம்' if lang == 'ta' else 'Welcome'}, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("தவறான பராமரிப்பாளர் விவரங்கள். 'caregiver' / 'Caregiver@123' முயற்சி செய்க." if lang == "ta" else "Invalid Caregiver credentials. Try 'caregiver' / 'Caregiver@123'")

            with st.expander("📝 " + ("புதிய பராமரிப்பாளர் கணக்கு பதிவு" if lang == "ta" else "Register New Caregiver Account")):
                with st.form("caregiver_reg_form"):
                    r_name = st.text_input("முழு பெயர்" if lang == "ta" else "Full Name", placeholder="e.g. Ananya Sharma")
                    r_user = st.text_input("விரும்பும் பயனர் பெயர்" if lang == "ta" else "Desired Username", placeholder="e.g. ananya")
                    r_pass = st.text_input("கடவுச்சொல்" if lang == "ta" else "Password", type="password")
                    r_phone = st.text_input("தொலைபேசி எண்" if lang == "ta" else "Contact Phone", placeholder="+91 98765 43210")
                    r_sub = st.form_submit_button("பதிவு செய்க" if lang == "ta" else "Register Account")
                    if r_sub and r_user and r_pass:
                        uid = db.register_user(r_user, r_pass, r_name, role="caregiver", phone=r_phone)
                        if uid:
                            st.success("கணக்கு வெற்றிகரமாக பதிவு செய்யப்பட்டது!" if lang == "ta" else "Account registered successfully! Please log in above.")
                        else:
                            st.error("இந்தப் பயனர் பெயர் ஏற்கனவே உள்ளது." if lang == "ta" else "Username already taken.")

            st.caption("💡 **" + ("பயிற்சி கணக்கு:" if lang == "ta" else "Demo Caregiver:") + "** `caregiver` | " + ("கடவுச்சொல்:" if lang == "ta" else "Password:") + " `Caregiver@123`")

        # ----------------------------------------------------------------------
        # TAB 3: CLINICAL SPECIALIST LOGIN
        # ----------------------------------------------------------------------
        with auth_tab_admin:
            st.subheader("🛡️ " + ("மருத்துவ நிபுணர் உள்நுழைவு" if lang == "ta" else "Clinical Specialist Login"))
            with st.form("admin_login_form"):
                a_user = st.text_input("நிர்வாகி பயனர் பெயர்" if lang == "ta" else "Specialist Username", value="admin")
                a_pass = st.text_input("கடவுச்சொல்" if lang == "ta" else "Password", type="password", value="admin123")
                a_sub = st.form_submit_button("🛡️ " + ("மருத்துவ நிபுணராக உள்நுழைக" if lang == "ta" else "Log In as Specialist"), use_container_width=True)

                if a_sub:
                    user = db.authenticate_user(a_user, a_pass)
                    if user and user["role"] == "admin":
                        st.session_state.auth_user = user
                        st.session_state.senior_mode_active = False
                        clear_all_stimuli()
                        st.toast(f"Admin: {user['full_name']}")
                        st.rerun()
                    else:
                        st.error("தவறான நிர்வாகி விவரங்கள்." if lang == "ta" else "Invalid Admin credentials.")
            st.caption("💡 **" + ("நிர்வாகி கணக்கு:" if lang == "ta" else "Demo Specialist:") + "** `admin` | `admin123`")

    st.stop()


# ==============================================================================
# 🔝 TOP NAVIGATION BAR (LOGGED IN OR SENIOR MODE)
# ==============================================================================
user = st.session_state.auth_user
user_role = user["role"] if user else ("patient" if st.session_state.senior_mode_active else "guest")
user_name = user["full_name"] if user else ("முதியோர் பயனாளி" if lang == "ta" else "Senior Patient")

c_head1, c_head2, c_head3 = st.columns([2.5, 1, 1])
with c_head1:
    role_badge = "மருத்துவ நிர்வாகி" if (lang == "ta" and user_role == "admin") else ("பராமரிப்பாளர்" if (lang == "ta" and user_role == "caregiver") else ("நோயாளி பிரிவு" if lang == "ta" else user_role.upper()))
    st.markdown(f"### 🧠 **NeuroCare** | <span style='font-size: 16px; color: #475569;'>{user_name} ({role_badge})</span>", unsafe_allow_html=True)
with c_head2:
    if st.session_state.app_lang == "ta":
        if st.button("🌐 Switch to English", key="lang_to_en_btn", use_container_width=True):
            st.session_state.app_lang = "en"
            clear_all_stimuli()
            st.rerun()
    else:
        if st.button("🌐 தமிழுக்கு மாற்றவும்", key="lang_to_ta_btn", use_container_width=True):
            st.session_state.app_lang = "ta"
            clear_all_stimuli()
            st.rerun()

with c_head3:
    logout_label = "🚪 வெளியேறு" if lang == "ta" else "🚪 Log Out"
    if st.button(logout_label, key="logout_btn", use_container_width=True):
        st.session_state.auth_user = None
        st.session_state.senior_mode_active = False
        st.session_state.selected_patient_id = None
        clear_all_stimuli()
        st.rerun()

st.divider()


# ==============================================================================
# 👵 SENIOR PATIENT MODE
# ==============================================================================
if st.session_state.senior_mode_active:
    patient_id = st.session_state.selected_patient_id
    if not patient_id:
        all_p = db.get_all_patients()
        patient_id = all_p[0]["id"] if all_p else 1
    
    current_patient = db.get_patient(patient_id)

    # Top View Selector: Motivational Story vs Cognitive Games Suite
    s_col_title, s_col_toggle = st.columns([2.5, 1.5])
    with s_col_title:
        st.markdown(f"## 🌿 {'அறிவாற்றல் நலவாழ்வு & நினைவாற்றல் மையம்' if lang == 'ta' else 'Adult & Senior Cognitive Longevity Suite'}")
        st.markdown(f"*{'வணக்கம்' if lang == 'ta' else 'Welcome'}! {t['welcome_patient']}*")
    with s_col_toggle:
        if st.session_state.show_motivational_story:
            if st.button("🧠 " + ("பயிற்சிகளுக்குச் செல்லவும்" if lang == "ta" else "Go to Cognitive Exercises"), key="toggle_to_games_btn", use_container_width=True, type="primary"):
                st.session_state.show_motivational_story = False
                st.rerun()
        else:
            if st.button("📖 " + ("வாழ்வின் உத்வேகக் கதை" if lang == "ta" else "View Inspiring Story"), key="toggle_to_story_btn", use_container_width=True):
                st.session_state.show_motivational_story = True
                st.rerun()

    # 1. MOTIVATIONAL ANIMATED STORYTELLING SCREEN (SHOWN AFTER LOGIN)
    if st.session_state.show_motivational_story:
        def on_proceed_to_games():
            st.session_state.show_motivational_story = False
            st.rerun()
        
        render_motivational_story(lang=lang, on_start_games_callback=on_proceed_to_games)

    # 2. SENIOR COGNITIVE GAMES SUITE (7 SPECIALIZED GAMES)
    else:
        c_m1, c_m2, c_m3 = st.columns([1, 1, 1.2])
        with c_m1:
            st.metric(label="தற்போதைய நிலை" if lang == "ta" else "Adaptive Level", value=f"{'நிலை' if lang == 'ta' else 'Level'} {current_patient['current_adaptive_level']} / 5")
        with c_m2:
            st.metric(label="அடிப்படை MMSE மதிப்பெண்" if lang == "ta" else "Baseline MMSE Score", value=f"{current_patient['baseline_mmse']} / 30")
        with c_m3:
            st.metric(label="பரிந்துரைக்கப்பட்ட பயிற்சி" if lang == "ta" else "Recommended Focus", value="சுடோக்கு & நினைவாற்றல்" if lang == "ta" else "Sudoku & Memory Pairs")

        st.markdown("### 🎮 " + ("பயிற்சியைத் தேர்ந்தெடுக்கவும் (டிமென்ஷியா & நினைவாற்றல் 7 பிரத்யேக பயிற்சிகள்):" if lang == "ta" else "Select Cognitive Activity (7 Specialized Dementia & Amnesia Games):"))

        # 7 Big, Distinct Visual Game Buttons for Seniors (Accessible Grid)
        g_col1, g_col2, g_col3, g_col4 = st.columns(4)
        with g_col1:
            is_active_1 = (st.session_state.active_game_key == "sudoku")
            if st.button("🧩 " + ("சுடோக்கு புதிர்" if lang == "ta" else "Senior Sudoku"), use_container_width=True, type="primary" if is_active_1 else "secondary"):
                st.session_state.active_game_key = "sudoku"
                clear_all_stimuli()
                st.rerun()

        with g_col2:
            is_active_2 = (st.session_state.active_game_key == "memory_pairs")
            if st.button("🃏 " + ("ஜோடி நினைவாற்றல்" if lang == "ta" else "Memory Pairs"), use_container_width=True, type="primary" if is_active_2 else "secondary"):
                st.session_state.active_game_key = "memory_pairs"
                clear_all_stimuli()
                st.rerun()

        with g_col3:
            is_active_3 = (st.session_state.active_game_key == "face_recall")
            if st.button("🖼️ " + ("நினைவுப் படம்" if lang == "ta" else "Photo Recall"), use_container_width=True, type="primary" if is_active_3 else "secondary"):
                st.session_state.active_game_key = "face_recall"
                st.session_state.mem_game_sub = "face_recall"
                clear_all_stimuli()
                st.rerun()

        with g_col4:
            is_active_4 = (st.session_state.active_game_key == "memory_increment")
            if st.button("🔢 " + ("நினைவு அதிகரிப்பு" if lang == "ta" else "Memory Span"), use_container_width=True, type="primary" if is_active_4 else "secondary"):
                st.session_state.active_game_key = "memory_increment"
                clear_all_stimuli()
                st.rerun()

        g_col5, g_col6, g_col7 = st.columns(3)
        with g_col5:
            is_active_5 = (st.session_state.active_game_key == "stroop")
            if st.button("🎨 " + ("வண்ணக் கவனம்" if lang == "ta" else "Color Stroop"), use_container_width=True, type="primary" if is_active_5 else "secondary"):
                st.session_state.active_game_key = "stroop"
                st.session_state.att_game_sub = "stroop"
                clear_all_stimuli()
                st.rerun()

        with g_col6:
            is_active_6 = (st.session_state.active_game_key == "orientation")
            if st.button("🕒 " + ("காலம் & இருப்பிடம்" if lang == "ta" else "Reality Orientation"), use_container_width=True, type="primary" if is_active_6 else "secondary"):
                st.session_state.active_game_key = "orientation"
                st.session_state.ori_game_sub = "temporal"
                clear_all_stimuli()
                st.rerun()

        with g_col7:
            is_active_7 = (st.session_state.active_game_key == "language")
            if st.button("🏷️ " + ("பொருள் அறிதல்" if lang == "ta" else "Object Naming"), use_container_width=True, type="primary" if is_active_7 else "secondary"):
                st.session_state.active_game_key = "language"
                st.session_state.lang_game_sub = "naming"
                clear_all_stimuli()
                st.rerun()

        st.divider()

        # Active Game Renderer (7 Distinct, Efficient Games)
        cur_game = st.session_state.active_game_key
        if cur_game == "sudoku":
            render_sudoku_game(current_patient, db=db, lang=lang)
        elif cur_game == "memory_pairs":
            render_memory_pairs_game(current_patient, db=db, lang=lang)
        elif cur_game == "face_recall":
            render_memory_game(current_patient, personalization, lang=lang)
        elif cur_game == "memory_increment":
            render_memory_increment_game(current_patient, lang=lang)
        elif cur_game == "stroop":
            render_attention_game(current_patient, lang=lang)
        elif cur_game == "orientation":
            render_orientation_game(current_patient, lang=lang)
        elif cur_game == "language":
            render_language_game(current_patient, lang=lang)


# ==============================================================================
# 🛡️ CLINICAL ADMIN PORTAL (STRUCTURED SEPARATION: CAREGIVER vs PATIENT vs RESEARCH)
# ==============================================================================
elif user and user["role"] == "admin":
    st.markdown("## 🛡️ " + ("மருத்துவ நிர்வாக கட்டுப்பாட்டு மையம்" if lang == "ta" else "Clinical Administration Oversight Portal"))
    st.caption("பராமரிப்பாளர் செயல்பாடுகள், நோயாளி அறிவாற்றல் முன்னேற்றம் மற்றும் ஆய்வுக் கட்டுரை புள்ளிவிவரங்கள்" if lang == "ta" else "Dedicated Oversight for Caregiver Processes, Patient Cognitive Trajectories, and Research Benchmark Analytics")

    all_users = db.get_all_users()
    caregivers = [u for u in all_users if u["role"] == "caregiver"]
    all_patients = db.get_all_patients()
    all_sessions = db.get_all_sessions_df()
    audit_logs = db.get_audit_logs(limit=100)

    # Top KPI Metrics Overview
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("👨‍⚕️ " + ("பராமரிப்பாளர்கள்" if lang == "ta" else "Active Caregivers"), len(caregivers))
    kpi2.metric("👵 " + ("பதிவான நோயாளிகள்" if lang == "ta" else "Registered Patients"), len(all_patients))
    kpi3.metric("🎮 " + ("பயிற்சி அமர்வுகள்" if lang == "ta" else "Cognitive Sessions"), len(all_sessions))
    kpi4.metric("📋 " + ("செயல் பதிவுகள்" if lang == "ta" else "Audit Logged Events"), len(audit_logs))

    st.markdown("---")

    # Clear top-level separation tabs
    tab_caregivers, tab_patients, tab_research = st.tabs([
        "👨‍⚕️ " + ("பராமரிப்பாளர் செயல்பாடுகள் & பணிகள்" if lang == "ta" else "Caregiver Actions & Process Oversight"),
        "👵 " + ("நோயாளி அறிவாற்றல் முன்னேற்றம்" if lang == "ta" else "Patient Cognitive Progress & Clinical State"),
        "📊 " + ("ஆய்வுக் கட்டுரை புள்ளிவிவர மையம்" if lang == "ta" else "Conference Research & Statistical Benchmark")
    ])

    # --------------------------------------------------------------------------
    # 👨‍⚕️ 1. CAREGIVER ACTIONS & PROCESS OVERSIGHT SECTION
    # --------------------------------------------------------------------------
    with tab_caregivers:
        st.markdown("### 👨‍⚕️ " + ("பராமரிப்பாளர் செயல்பாடுகள் மற்றும் பொறுப்புகள்" if lang == "ta" else "Caregiver Responsibilities & Action Tracking"))
        
        # Summary description card of what caregivers do
        with st.container(border=True):
            st.markdown(f"""
            #### 📌 {'பராமரிப்பாளர் என்ன செய்கிறார்?' if lang == 'ta' else 'What Caregivers Do in NeuroCare:'}
            - **1. {'நோயாளி பதிவு & மேலாண்மை' if lang == 'ta' else 'Patient Registration & Management'}:** {'புதிய நோயாளிகளைப் பதிவு செய்து, அவர்களின் அடிப்படை MMSE மதிப்பெண்களைக் கண்காணித்தல்.' if lang == 'ta' else 'Enrolling senior patients with diagnosis, baseline MMSE scores, and family profiles.'}
            - **2. {'நினைவுக் களஞ்சியத்தில் புகைப்படங்கள் பதிவேற்றம்' if lang == 'ta' else 'Reminiscence Photo & Memory Uploads'}:** {'குடும்ப புகைப்படங்கள், உறவினர்கள், செல்லப்பிராணிகள், பிடித்த இடங்கள் மற்றும் அன்றாட வேலைப் படங்களை பதிவேற்றுதல்.' if lang == 'ta' else 'Uploading actual personal family photos, loved ones, hometown places, and daily routine steps.'}
            - **3. {'பயிற்சி அமர்வுகளைத் தொடங்குதல்' if lang == 'ta' else 'Session Facilitation & Supervision'}:** {'முதியவர்களுக்கான 8 வகையான அறிவாற்றல் விளையாட்டுகளைத் தொடங்கி, அவர்களின் கவனத்தை வழிநடத்துதல்.' if lang == 'ta' else 'Initiating daily cognitive game routines for seniors and supervising their progress.'}
            - **4. {'மருத்துவ அறிக்கைகள் பதிவிறக்கம்' if lang == 'ta' else 'Clinical Progress & Report Export'}:** {'துல்லிய விகிதங்கள், பதில் வேகம் மற்றும் சோர்வு இடைவேளைகளைக் கண்காணித்து மருத்துவ அறிக்கைகளை உருவாக்குதல்.' if lang == 'ta' else 'Monitoring reaction latency, accuracy trajectories, and exporting clinical Markdown reports.'}
            """)

        # Caregiver Roster Table
        st.markdown("#### 👥 " + ("பதிவுசெய்த பராமரிப்பாளர்கள் பட்டியல்" if lang == "ta" else "Registered Caregiver Roster"))
        if caregivers:
            cg_data = []
            for cg in caregivers:
                c_patients = db.get_all_patients(caregiver_id=cg["id"])
                cg_data.append({
                    "ID": cg["id"],
                    "Username / பெயர்": cg["username"],
                    "Full Name / முழு பெயர்": cg["full_name"],
                    "Phone / தொலைபேசி": cg.get("phone", "N/A"),
                    "Assigned Patients / நோயாளிகள்": len(c_patients),
                    "Joined / பதிவு செய்த தேதி": cg.get("created_at", "N/A")
                })
            st.dataframe(pd.DataFrame(cg_data), use_container_width=True)
        else:
            st.info("பராமரிப்பாளர்கள் யாரும் பதிவு செய்யப்படவில்லை." if lang == "ta" else "No caregivers registered yet.")

        st.markdown("#### 📋 " + ("பராமரிப்பாளர் செயல் பதிவேடு (Audit Logs)" if lang == "ta" else "Caregiver Live Audit Logs & Event Trail"))
        st.write("பராமரிப்பாளர்கள் கணினியில் மேற்கொண்ட அனைத்து நடவடிக்கைகளின் விரிவான பதிவு:" if lang == "ta" else "Detailed chronological audit log of all caregiver actions (logins, uploads, session launches):")
        
        if not audit_logs.empty:
            cg_audit = audit_logs[audit_logs["role"] != "admin"] if "role" in audit_logs.columns else audit_logs
            st.dataframe(cg_audit if not cg_audit.empty else audit_logs, use_container_width=True)
        else:
            st.info("செயல் பதிவுகள் எதுவும் இல்லை." if lang == "ta" else "No audit logs recorded yet.")

    # --------------------------------------------------------------------------
    # 👵 2. PATIENT COGNITIVE PROGRESS & CLINICAL STATE SECTION
    # --------------------------------------------------------------------------
    with tab_patients:
        st.markdown("### 👵 " + ("நோயாளி அறிவாற்றல் முன்னேற்றம் மற்றும் மருத்துவ நிலை" if lang == "ta" else "Patient Cognitive Progress & Clinical State"))
        
        # Summary description card of what patients do
        with st.container(border=True):
            st.markdown(f"""
            #### 📌 {'நோயாளி என்ன செய்கிறார்?' if lang == 'ta' else 'What Patients Do in NeuroCare:'}
            - **1. {'8 வகை அறிவாற்றல் பயிற்சிகள்' if lang == 'ta' else 'Engaging in 8 Cognitive Activities'}:** {'குடும்ப புகைப்பட நினைவூட்டல், நிகழ்வு கால வரிசை, ஸ்ட்ரூப் வண்ணப் பயிற்சி, எண் வரிசை இணைப்பு, கடிகார நேரம், வீட்டு சூழல், பொருள் பெயர் மற்றும் வகைப்பாடு அறிதல்.' if lang == 'ta' else 'Familiar Face Recall, Routine Sequencing, Color Stroop, Trail Making, Reality Clock, Home Navigator, Object Naming, and Category Matching.'}
            - **2. {'பதில் வேகம் & துல்லியம்' if lang == 'ta' else 'Response Latency & Accuracy'}:** {'ஒவ்வொரு தொடுதிரை பதிலின் வேகம் மில்லி விநாடிகளில் துல்லியமாக அளவிடப்படுகிறது.' if lang == 'ta' else 'Patient response time (latency in seconds) and selection accuracy are measured per trial.'}
            - **3. {'தானியங்கி கடினத்தன்மை நிலை (Level 1 - 5)' if lang == 'ta' else 'Adaptive Difficulty Scaling (Levels 1 to 5)'}:** {'நோயாளி சரியாக பதிலளித்தால் நிலை உயரும்; சிரமப்பட்டால் எளிதாக்கப்படும்.' if lang == 'ta' else 'Automatically adjusts difficulty levels dynamically based on real-time performance.'}
            - **4. {'சோர்வு மேலாண்மை & ஓய்வு' if lang == 'ta' else 'Fatigue Detection & Breathing Breaks'}:** {'தொடர் பிழைகள் அல்லது தயக்கம் ஏற்பட்டால் அமைதியான 1 நிமிட சுவாச ஓய்வு வழங்கப்படுகிறது.' if lang == 'ta' else 'Triggers soothing 1-minute mindfulness breathing breaks when fatigue or agitation is detected.'}
            """)

        # All Patient Cohort Table
        st.markdown("#### 📋 " + ("அனைத்து நோயாளிகள் மருத்துவ விவரங்கள்" if lang == "ta" else "Comprehensive Patient Cohort Directory"))
        if all_patients:
            p_df = pd.DataFrame(all_patients)[["id", "name", "age", "condition", "baseline_mmse", "caregiver_name", "current_adaptive_level", "created_at"]]
            p_df.columns = ["ID", "Name / பெயர்", "Age / வயது", "Condition / மருத்துவ நிலை", "Baseline MMSE", "Caregiver / பராமரிப்பாளர்", "Level / நிலை", "Registered / பதிவு தேதி"]
            st.dataframe(p_df, use_container_width=True)

            # Patient Performance Scatter & Breakdown
            st.markdown("#### 📈 " + ("அறிவாற்றல் வேகம் vs துல்லியம் ஒப்பீடு" if lang == "ta" else "Cognitive Speed vs. Accuracy Trajectory"))
            if not all_sessions.empty:
                col_chart1, col_chart2 = st.columns(2)
                with col_chart1:
                    fig_all = px.scatter(
                        all_sessions,
                        x="avg_response_time_sec",
                        y="accuracy_pct",
                        color="patient_name",
                        size="total_trials",
                        title="பதில் வேகம் vs துல்லியம்" if lang == "ta" else "Response Latency (s) vs. Accuracy (%)",
                        labels={"avg_response_time_sec": "பதில் நேரம் (வி)" if lang == "ta" else "Response Latency (s)", "accuracy_pct": "துல்லியம் (%)" if lang == "ta" else "Accuracy (%)"}
                    )
                    fig_all.update_layout(template="plotly_white", height=350)
                    st.plotly_chart(fig_all, use_container_width=True)

                with col_chart2:
                    fig_dom = px.bar(
                        all_sessions.groupby("cognitive_domain")["accuracy_pct"].mean().reset_index(),
                        x="cognitive_domain",
                        y="accuracy_pct",
                        color="cognitive_domain",
                        title="அறிவாற்றல் பிரிவுகள் சராசரி துல்லியம் (%)" if lang == "ta" else "Mean Accuracy by Cognitive Domain (%)",
                        labels={"cognitive_domain": "பிரிவு" if lang == "ta" else "Domain", "accuracy_pct": "துல்லியம் (%)" if lang == "ta" else "Accuracy (%)"}
                    )
                    fig_dom.update_layout(template="plotly_white", height=350, showlegend=False)
                    st.plotly_chart(fig_dom, use_container_width=True)

            # Individual Patient Deep-Dive Selector
            st.markdown("#### 🔍 " + ("தனிப்பட்ட நோயாளி விவர ஆய்வு" if lang == "ta" else "Individual Patient Performance Deep-Dive"))
            p_select_map = {f"{p['name']} (ID: {p['id']})": p["id"] for p in all_patients}
            chosen_admin_p = st.selectbox("ஆய்வு செய்ய நோயாளியைத் தேர்ந்தெடுக்கவும்" if lang == "ta" else "Select Patient to Inspect", list(p_select_map.keys()))
            p_hist = db.get_patient_session_history(p_select_map[chosen_admin_p])
            
            if not p_hist.empty:
                st.dataframe(p_hist, use_container_width=True)
            else:
                st.info("இந்த நோயாளிக்கு இன்னும் பயிற்சி அமர்வுகள் பதிவு செய்யப்படவில்லை." if lang == "ta" else "No cognitive sessions recorded yet for this patient.")

        else:
            st.info("நோயாளி விவரங்கள் எதுவும் இல்லை." if lang == "ta" else "No patient records in database.")

    # --------------------------------------------------------------------------
    # 📊 3. CONFERENCE RESEARCH & STATISTICAL BENCHMARK
    # --------------------------------------------------------------------------
    with tab_research:
        st.markdown("### 📊 " + ("ஆய்வுக் கட்டுரை புள்ளிவிவர மையம் (RCT Benchmark N=30)" if lang == "ta" else "Conference Publication & RCT Statistical Benchmark (N=30)"))
        st.caption("NeuroCare Clinical Cognitive Assessment Platform | Randomized Controlled Trial Benchmark" if lang == "en" else "NeuroCare மருத்துவ அறிவாற்றல் மதிப்பீட்டு தளம் | சீரற்ற கட்டுப்பாட்டு சோதனை அளவுகோல்")
        
        rct_df = research_engine.generate_rct_dataset(n_participants=30, seed=42)
        exp_df = rct_df[rct_df["Group"] == "Experimental (NeuroCare)"]

        domains_to_test = [
            ("Episodic Memory", exp_df["Pre_Memory"].values, exp_df["Post_Memory"].values),
            ("Attention & Executive", exp_df["Pre_Attention"].values, exp_df["Post_Attention"].values),
            ("Temporal Orientation", exp_df["Pre_Orientation"].values, exp_df["Post_Orientation"].values),
            ("Language & Naming", exp_df["Pre_Language"].values, exp_df["Post_Language"].values)
        ]

        stats_dict = {}
        rows = []
        for d_name, pre, post in domains_to_test:
            res = research_engine.calculate_domain_statistics(pre, post)
            stats_dict[d_name] = res
            rows.append({
                "Cognitive Domain": d_name,
                "Pre-Test (M ± SD)": f"{res['mean_pre']:.2f} ± {res['std_pre']:.2f}",
                "Post-Test (M ± SD)": f"{res['mean_post']:.2f} ± {res['std_post']:.2f}",
                "Mean Gain (Δ)": f"+{res['mean_gain']:.2f}",
                "t-stat": res["t_statistic"],
                "p-value": "< 0.001" if res["p_value"] < 0.001 else f"{res['p_value']:.4f}",
                "Cohen's d": res["cohens_d"]
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        latex_code = research_engine.generate_latex_table(stats_dict)
        st.markdown("#### 📄 " + ("ஆய்வுக் கட்டுரைக்கான LaTeX அட்டவணை" if lang == "ta" else "LaTeX Table for Conference Paper"))
        st.code(latex_code, language="latex")



# ==============================================================================
# 👨‍⚕️ CAREGIVER PORTAL
# ==============================================================================
elif user and user["role"] == "caregiver":
    st.markdown(f"## 👨‍⚕️ {'பராமரிப்பாளர் மையம்' if lang == 'ta' else 'Caregiver Portal'} — **{user['full_name']}**")
    
    my_patients = db.get_all_patients(caregiver_id=user["id"])
    if not my_patients:
        all_p = db.get_all_patients()
        active_patient = all_p[0] if all_p else None
    else:
        active_patient = my_patients[0]

    if not active_patient:
        st.error("நோயாளி விவரங்கள் எதுவும் ஒதுக்கப்படவில்லை." if lang == "ta" else "No elder profile assigned to your caregiver account.")
        st.stop()

    # ── ONLY ONE DESIGNATED AREA SHOWING PATIENT'S NAME & PROFILE ──
    c_p_info, c_p_launch = st.columns([2.5, 1.5])
    with c_p_info:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); padding: 14px 20px; border-radius: 12px; border-left: 5px solid #3B82F6;">
                <div style="font-size: 17px; font-weight: bold; color: #F8FAFC;">
                    👤 {'பராமரிக்கப்படும் முதியவர்' if lang == 'ta' else 'Assigned Elder'}: <span style="color: #60A5FA;">{active_patient['name']}</span>
                </div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
                    {'வயது' if lang == 'ta' else 'Age'}: {active_patient['age']} | {'நிலை' if lang == 'ta' else 'Level'}: 🌟 Level {active_patient['current_adaptive_level']}/5 | {active_patient['condition']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c_p_launch:
        if st.button("👵 " + ("முதியோர் பயிற்சியைத் தொடங்கவும்" if lang == "ta" else "Launch Training Session"), use_container_width=True):
            st.session_state.selected_patient_id = active_patient["id"]
            clear_all_stimuli()
            st.session_state.senior_mode_active = True
            st.session_state.show_motivational_story = True
            db.log_audit(user["id"], user["username"], "caregiver", "LAUNCH_SESSION", f"Launched training session for elder ID {active_patient['id']}")
            st.rerun()

    tab_vault, tab_analytics, tab_report, tab_test_games = st.tabs([
        "📸 " + ("நினைவுக் களஞ்சியம் & புகைப்படங்கள்" if lang == "ta" else "Reminiscence Memory Vault & Photo Upload"),
        "📈 " + ("முன்னேற்றப் புள்ளிவிவரங்கள்" if lang == "ta" else "Progress Analytics"),
        "📄 " + ("மருத்துவ அறிக்கை" if lang == "ta" else "Clinical Assessment Report"),
        "🎮 " + ("பயிற்சிகளின் முன்னோட்டம்" if lang == "ta" else "Preview Specialized Games")
    ])

    # 1. MEMORY VAULT & LOCAL FILE UPLOAD (No patient name repeated)
    with tab_vault:
        st.subheader("🖼️ " + ("குடும்ப நினைவுக் களஞ்சியம்" if lang == "ta" else "Personal Memory Anchors"))
        st.write("குடும்ப புகைப்படங்கள், விருப்பமான இடங்கள் மற்றும் பொருட்களை உங்கள் கணினியில் இருந்து பதிவேற்றவும்:" if lang == "ta" else "Upload your actual family photos, memories, hometown places, or routine steps directly from your computer:")

        with st.form("upload_memory_form", clear_on_submit=True):
            st.markdown("#### ➕ " + ("புதிய குடும்ப புகைப்படம் சேர்க்க" if lang == "ta" else "Add New Family Photo / Cherished Memory"))
            c_v1, c_v2 = st.columns(2)
            with c_v1:
                cat = st.selectbox("பிரிவு" if lang == "ta" else "Memory Category", ["family", "place", "routine", "hobby", "object"])
                lbl_en = st.text_input("Name / Title (English)", placeholder="e.g. Mother, Taj Mahal, Dog Lucky")
                det_en = st.text_input("Description / Cue (English)", placeholder="e.g. Your loving mother")
            with c_v2:
                lbl_ta = st.text_input("பெயர் / தலைப்பு (தமிழ்)", placeholder="எ.கா: அம்மா, தாஜ் மஹால், வளர்ப்பு நாய்")
                det_ta = st.text_input("விளக்கம் / உறவு முறை (தமிழ்)", placeholder="எ.கா: உங்கள் பாசமிகு தாய்")

            uploaded_file = st.file_uploader("📂 " + ("கணினியில் இருந்து புகைப்படத்தைத் தேர்ந்தெடுக்கவும் (.jpg, .png, .jpeg)" if lang == "ta" else "Upload Local Image File from Computer (.jpg, .png, .jpeg)"), type=["png", "jpg", "jpeg", "webp"])

            submit_mem = st.form_submit_button("💾 " + ("புகைப்படத்தைச் சேமிக்கவும்" if lang == "ta" else "Save Photo & Anchor to Patient Vault"), use_container_width=True)

            if submit_mem and (lbl_en or lbl_ta):
                saved_rel_path = ""
                if uploaded_file is not None:
                    safe_filename = f"p{active_patient['id']}_{int(time.time())}_{uploaded_file.name.replace(' ', '_')}"
                    file_dest = os.path.join(UPLOADS_DIR, safe_filename)
                    with open(file_dest, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_rel_path = os.path.join("uploads", safe_filename)

                final_lbl_en = lbl_en if lbl_en else lbl_ta
                final_lbl_ta = lbl_ta if lbl_ta else lbl_en

                db.add_memory(
                    patient_id=active_patient["id"],
                    category=cat,
                    label_en=final_lbl_en,
                    label_ta=final_lbl_ta,
                    detail_en=det_en if det_en else final_lbl_en,
                    detail_ta=det_ta if det_ta else final_lbl_ta,
                    image_path=saved_rel_path
                )
                clear_all_stimuli()
                db.log_audit(user["id"], user["username"], "caregiver", "UPLOAD_MEMORY", f"Uploaded memory '{final_lbl_en}' with local image for {active_patient['name']}")
                st.success("புகைப்படம் வெற்றிகரமாகச் சேமிக்கப்பட்டது!" if lang == "ta" else f"Memory anchor '{final_lbl_en}' saved successfully!")
                st.rerun()

        memories = db.get_patient_memories(active_patient["id"])
        if memories:
            st.markdown(f"**{'சேமிக்கப்பட்ட நினைவுகள்' if lang == 'ta' else 'Current Memory Gallery'} ({len(memories)} {'படங்கள்' if lang == 'ta' else 'items'}):**")
            m_cols = st.columns(3)
            for idx, m in enumerate(memories):
                with m_cols[idx % 3]:
                    with st.container(border=True):
                        img_path = m.get("image_path", "")
                        if img_path and os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)
                        else:
                            st.info("📷 " + ("நினைவுப் படம்" if lang == "ta" else "Photo Anchor"))
                        
                        m_title = m['label_ta'] if lang == 'ta' else m['label_en']
                        m_desc = m['detail_ta'] if lang == 'ta' else m['detail_en']
                        st.markdown(f"**{m_title}**")
                        st.caption(f"📁 `{m['category']}` | 💡 {m_desc}")
                        if st.button("🗑️ " + ("நீக்குக" if lang == "ta" else "Delete"), key=f"del_mem_{m['id']}_{lang}"):
                            db.delete_memory(m["id"])
                            clear_all_stimuli()
                            st.toast("நினைவு நீக்கப்பட்டது." if lang == "ta" else "Memory deleted.")
                            st.rerun()
        else:
            st.info("நினைவுகள் எதுவும் இன்னும் சேர்க்கப்படவில்லை." if lang == "ta" else "No memories added yet. Upload a family photo above!")

    # 2. ANALYTICS (No patient name repeated)
    with tab_analytics:
        st.subheader("📈 " + ("முன்னேற்றப் புள்ளிவிவரங்கள்" if lang == "ta" else "Longitudinal Performance & Analytics"))
        history = db.get_patient_session_history(active_patient["id"])

        if not history.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("மொத்த அமர்வுகள்" if lang == "ta" else "Total Sessions", len(history))
            c2.metric("சராசரி துல்லியம்" if lang == "ta" else "Mean Accuracy", f"{history['accuracy_pct'].mean():.1f}%")
            c3.metric("சராசரி பதில் வேகம்" if lang == "ta" else "Mean Reaction Time", f"{history['avg_response_time_sec'].mean():.2f}{'வி' if lang == 'ta' else 's'}")

            fig_acc = px.line(
                history,
                x="session_timestamp",
                y="accuracy_pct",
                color="cognitive_domain",
                markers=True,
                title="துல்லிய முன்னேற்றம் (%)" if lang == "ta" else "Cognitive Accuracy (%) by Domain Across Longitudinal Sessions"
            )
            fig_acc.update_layout(template="plotly_white", height=360)
            st.plotly_chart(fig_acc, use_container_width=True)
        else:
            st.info("பயிற்சி பதிவுகள் எதுவும் இல்லை." if lang == "ta" else "No session records logged yet for this patient.")

    # 3. CLINICAL REPORT
    with tab_report:
        st.subheader("📄 " + ("மருத்துவ மதிப்பீட்டு அறிக்கை" if lang == "ta" else "Export Clinical Summary Report"))
        history = db.get_patient_session_history(active_patient["id"])
        
        mean_acc = f"{history['accuracy_pct'].mean():.1f}%" if not history.empty else "N/A"
        mean_rt = f"{history['avg_response_time_sec'].mean():.2f}s" if not history.empty else "N/A"
        report_text = f"""# NEUROCARE CLINICAL ASSESSMENT REPORT
**Patient Name:** {active_patient['name']} | **Age:** {active_patient['age']} | **Condition:** {active_patient['condition']}  
**Baseline MMSE:** {active_patient['baseline_mmse']}/30 | **Current Level:** Level {active_patient['current_adaptive_level']}/5  
**Assigned Caregiver:** {user['full_name']}  
**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

---
### Cognitive Performance
- Total Sessions: {len(history)}
- Overall Accuracy: {mean_acc}
- Mean Response Time: {mean_rt}
"""
        st.markdown(report_text)
        st.download_button("📥 " + ("மருத்துவ அறிக்கையைப் பதிவிறக்குக (.MD)" if lang == "ta" else "Download Report (.MD)"), data=report_text, file_name="Clinical_Assessment_Report.md", use_container_width=True)

    # 4. TEST & PREVIEW ALL GAMES & MOTIVATIONAL STORY (FOR CAREGIVERS)
    with tab_test_games:
        st.subheader("🎮 " + ("பிரத்யேக பயிற்சிகள் மற்றும் உத்வேகக் கதையின் நேரடி முன்னோட்டம்" if lang == "ta" else "Test & Preview Specialized Cognitive Games & Motivational Story"))
        st.write("பராமரிப்பாளர்கள் அனைத்து பயிற்சிகளையும் மற்றும் அனிமேஷன் கதையையும் முன்னோட்டமாகப் பார்க்கலாம்:" if lang == "ta" else "Caregivers can preview and test any of the 7 specialized cognitive activities or the animated motivational story:")

        g_opts_ta = [
            "🧩 1. முதியோர் சுடோக்கு புதிர் (Senior Sudoku Challenge)",
            "🃏 2. ஜோடி நினைவாற்றல் விளையாட்டு (Memory Matching Pairs)",
            "📖 3. தினசரி உத்வேக அனிமேஷன் கதை (Motivational Story Theater)",
            "🖼️ 4. நினைவுப் புகைப்படம் அறிதல் (Photo Recall)",
            "🔢 5. நினைவுத்திறன் அதிகரிப்புப் பயிற்சி (Memory Span Increment)",
            "🎨 6. வண்ணக் கவனக்குவிப்புப் பயிற்சி (Color Stroop Task)",
            "🕒 7. காலம் & இருப்பிட விழிப்புணர்வு (Reality Orientation)",
            "🏷️ 8. பொருள் & வகைப்பாடு அறிதல் (Semantic Language Match)"
        ]
        g_opts_en = [
            "🧩 1. Senior Sudoku Challenge (4x4 Mini-Grid & Symbols)",
            "🃏 2. Memory Matching Pairs Challenge",
            "📖 3. Daily Motivational Animated Story Theater",
            "🖼️ 4. Familiar Photo Recall (Reminiscence)",
            "🔢 5. Memory Span Increment Challenge",
            "🎨 6. Color Stroop Attention Task",
            "🕒 7. Reality & Spatial Orientation",
            "🏷️ 8. Semantic Object & Category Match"
        ]

        g_prev = st.selectbox(
            "பயிற்சியைத் தேர்ந்தெடுக்கவும்" if lang == "ta" else "Select Activity to Preview",
            options=g_opts_ta if lang == "ta" else g_opts_en
        )

        st.divider()
        if ("Sudoku" in g_prev) or ("சுடோக்கு" in g_prev):
            render_sudoku_game(active_patient, db=db, lang=lang)
        elif ("Matching Pairs" in g_prev) or ("ஜோடி" in g_prev):
            render_memory_pairs_game(active_patient, db=db, lang=lang)
        elif ("Motivational" in g_prev) or ("உத்வேக" in g_prev):
            render_motivational_story(lang=lang)
        elif ("Photo Recall" in g_prev) or ("புகைப்படம்" in g_prev):
            st.session_state.mem_game_sub = "face_recall"
            render_memory_game(active_patient, personalization, lang=lang)
        elif ("Increment" in g_prev) or ("அதிகரிப்பு" in g_prev):
            render_memory_increment_game(active_patient, lang=lang)
        elif ("Stroop" in g_prev) or ("வண்ண" in g_prev):
            st.session_state.att_game_sub = "stroop"
            render_attention_game(active_patient, lang=lang)
        elif ("Reality" in g_prev) or ("காலம்" in g_prev):
            st.session_state.ori_game_sub = "temporal"
            render_orientation_game(active_patient, lang=lang)
        elif ("Semantic" in g_prev) or ("பொருள்" in g_prev):
            st.session_state.lang_game_sub = "naming"
            render_language_game(active_patient, lang=lang)



# Footer
st.divider()
st.caption(f"© 2026 {APP_NAME} | {'அறிவாற்றல் மற்றும் நினைவாற்றல் மறுவாழ்வு தளம்' if lang == 'ta' else 'Clinical Cognitive Assessment & Memory Assistance Platform'}")
