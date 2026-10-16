"""
Difficulty management module for NeuroCare Cognitive Platform.
Provides accessible Easy, Medium, and Hard level selection across all 5 cognitive games
with instant stimulus adaptation and pure bilingual localization.
"""

import streamlit as st
from typing import Tuple, Dict, Any

DIFFICULTY_METADATA = {
    "easy": {
        "en": "🟢 Easy",
        "ta": "🟢 எளிது",
        "num": 1,
        "badge_color": "#16A34A"
    },
    "medium": {
        "en": "🟡 Medium",
        "ta": "🟡 நடுத்தரம்",
        "num": 2,
        "badge_color": "#D97706"
    },
    "hard": {
        "en": "🔴 Hard",
        "ta": "🔴 கடினம்",
        "num": 3,
        "badge_color": "#DC2626"
    }
}

def render_difficulty_selector(
    game_key: str,
    lang: str = "en",
    default_lvl: int = 2
) -> Tuple[str, int]:
    """
    Renders an elderly-friendly, high-contrast Easy / Medium / Hard difficulty selector.
    Automatically syncs with session state and regenerates stimuli upon level change.
    
    Returns:
        (difficulty_str, difficulty_num): ('easy'|'medium'|'hard', 1|2|3)
    """
    diff_state_key = f"{game_key}_difficulty"
    if diff_state_key not in st.session_state:
        if default_lvl <= 1:
            st.session_state[diff_state_key] = "easy"
        elif default_lvl in (2, 3):
            st.session_state[diff_state_key] = "medium"
        else:
            st.session_state[diff_state_key] = "hard"

    current_diff = st.session_state[diff_state_key]

    opts_ta = ["🟢 எளிது", "🟡 நடுத்தரம்", "🔴 கடினம்"]
    opts_en = ["🟢 Easy", "🟡 Medium", "🔴 Hard"]
    opts = opts_ta if lang == "ta" else opts_en

    val_to_idx = {"easy": 0, "medium": 1, "hard": 2}
    idx_to_val = {0: "easy", 1: "medium", 2: "hard"}
    current_idx = val_to_idx.get(current_diff, 1)

    # Specialized descriptive subtitles by game
    game_subtitles_ta = {
        "sudoku": "எளிது: அதிக குறிப்புகள் (4 கட்டங்கள்) | நடுத்தரம்: சமநிலை | கடினம்: தீவிர கவனம்",
        "memory_pairs": "எளிது: 3 ஜோடிகள் (6 அட்டைகள்) | நடுத்தரம்: 4 ஜோடிகள் (8 அட்டைகள்) | கடினம்: 6 ஜோடிகள் (12 அட்டைகள்)",
        "memory_increment": "எளிது: 2 படங்கள் | நடுத்தரம்: 3 படங்கள் | கடினம்: 4 படங்கள்",
        "memory": "எளிது: 2 தேர்வுகள் | நடுத்தரம்: 3 தேர்வுகள் | கடினம்: 4 தேர்வுகள்",
        "attention": "எளிது: 2 தேர்வுகள் | நடுத்தரம்: 3 தேர்வுகள் | கடினம்: 4 தேர்வுகள்",
        "orientation": "எளிது: 2 தேர்வுகள் | நடுத்தரம்: 3 தேர்வுகள் | கடினம்: 4 தேர்வுகள்",
        "language": "எளிது: 2 தேர்வுகள் | நடுத்தரம்: 3 தேர்வுகள் | கடினம்: 4 தேர்வுகள்"
    }
    game_subtitles_en = {
        "sudoku": "Easy: More Clues (4 to fill) | Medium: Balanced | Hard: Deep Focus",
        "memory_pairs": "Easy: 3 Pairs (6 Cards) | Medium: 4 Pairs (8 Cards) | Hard: 6 Pairs (12 Cards)",
        "memory_increment": "Easy: 2 Items | Medium: 3 Items | Hard: 4 Items",
        "memory": "Easy: 2 Options | Medium: 3 Options | Hard: 4 Options",
        "attention": "Easy: 2 Options | Medium: 3 Options | Hard: 4 Options",
        "orientation": "Easy: 2 Options | Medium: 3 Options | Hard: 4 Options",
        "language": "Easy: 2 Options | Medium: 3 Options | Hard: 4 Options"
    }
    sub_text = game_subtitles_ta.get(game_key, "எளிது: 2 தேர்வுகள் | நடுத்தரம்: 3 தேர்வுகள் | கடினம்: 4 தேர்வுகள்") if lang == "ta" else game_subtitles_en.get(game_key, "Easy: 2 Options | Medium: 3 Options | Hard: 4 Options")

    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%); 
                    padding: 8px 16px; border-radius: 10px; margin-bottom: 12px; 
                    border-left: 5px solid #3B82F6; display: flex; align-items: center; justify-content: space-between;">
            <div style="font-weight: 700; font-size: 15px; color: #F8FAFC;">
                🎯 {'கடினத்தன்மை நிலை' if lang == 'ta' else 'Difficulty Level'}: 
                <span style="color: {DIFFICULTY_METADATA[current_diff]['badge_color']}; margin-left: 6px;">
                    {DIFFICULTY_METADATA[current_diff]['ta' if lang == 'ta' else 'en']}
                </span>
            </div>
            <div style="font-size: 14px; font-weight: 700; color: #F8FAFC; text-shadow: 0 1px 3px rgba(0,0,0,0.6);">
                {sub_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_label = st.radio(
        label="Difficulty Level",
        options=opts,
        index=current_idx,
        horizontal=True,
        key=f"diff_sel_{game_key}_{lang}",
        label_visibility="collapsed"
    )

    selected_idx = opts.index(selected_label)
    selected_diff = idx_to_val[selected_idx]

    # If the user toggled the difficulty, immediately reset the stimulus and rerun
    if selected_diff != current_diff:
        st.session_state[diff_state_key] = selected_diff
        
        # Invalidate active stimulus caches for clean regeneration
        if game_key == "memory":
            st.session_state.mem_stimulus = None
            st.session_state.mem_feedback = None
        elif game_key == "memory_increment":
            st.session_state.mem_span_target_seq = []
            st.session_state.mem_span_user_seq = []
            st.session_state.mem_span_level = 2 if selected_diff == "easy" else (3 if selected_diff == "medium" else 4)
            st.session_state.mem_span_phase = "memorize"
        elif game_key == "sudoku":
            st.session_state.sudoku_board = None
            st.session_state.sudoku_initial_board = None
            st.session_state.sudoku_history = []
            st.session_state.sudoku_completed = False
            st.session_state.sudoku_conflict_message = None
            st.session_state.sudoku_hint_message = None
        elif game_key == "memory_pairs":
            st.session_state.pairs_deck = None
            st.session_state.pairs_flipped = []
            st.session_state.pairs_matched = set()
            st.session_state.pairs_completed = False
            st.session_state.pairs_feedback = None
        elif game_key == "attention":
            st.session_state.att_stimulus = None
            st.session_state.att_feedback = None
            st.session_state.tmt_state = None
        elif game_key == "orientation":
            st.session_state.ori_stimulus = None
            st.session_state.ori_spatial_stim = None
            st.session_state.ori_feedback = None
        elif game_key == "language":
            st.session_state.lang_stimulus = None
            st.session_state.lang_cat_stim = None
            st.session_state.lang_feedback = None
        
        st.rerun()

    num_map = {"easy": 1, "medium": 2, "hard": 3}
    return selected_diff, num_map[selected_diff]
