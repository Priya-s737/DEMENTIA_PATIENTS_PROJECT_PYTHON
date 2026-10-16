"""
Memory Matching Pairs Game:
Specifically designed for Alzheimer's, Dementia, Amnesia, and MCI Rehabilitation.
Features:
- Visual Card-Flipping Concentration Game for short-term working memory & recall
- Injects real caregiver-uploaded reminiscence photos from Memory Vault
- 3 Senior-Accessible Difficulty Levels:
    * Easy: 3 Pairs (6 Cards, 2x3 Grid) - Gentle & Fatigue-Safe
    * Medium: 4 Pairs (8 Cards, 2x4 Grid) - Balanced Everyday Routine
    * Hard: 6 Pairs (12 Cards, 3x4 Grid) - Active Memory Challenge
- High-contrast visual cards with photos, icons, and pure bilingual labels
- Immediate celebratory positive reinforcement without time stress
- Full audio voice narration via Web Speech API
- Automated session telemetry and longitudinal logging to SQLite database
"""

import streamlit as st
import time
import os
import random
from typing import Dict, Any, List, Optional
from modules.voice_assistant import VoiceAssistant
from modules.difficulty import render_difficulty_selector
from modules.celebration import render_celebration, CELEBRATION_RHYMES

# Standard Curated Senior Reminiscence Memory Cards with Local Picture Assets
STANDARD_MEMORY_PAIRS_CATALOG = [
    {
        "id": "lamp",
        "name_en": "Brass Lamp",
        "name_ta": "பித்தளை விளக்கு",
        "icon": "🪔",
        "img": "uploads/visual_cards/brass_lamp.jpg"
    },
    {
        "id": "coffee",
        "name_en": "Morning Coffee",
        "name_ta": "காலை காபி",
        "icon": "☕",
        "img": "uploads/visual_cards/coffee.jpg"
    },
    {
        "id": "spectacles",
        "name_en": "Reading Glasses",
        "name_ta": "மூக்குக் கண்ணாடி",
        "icon": "👓",
        "img": "uploads/visual_cards/spectacles.jpg"
    },
    {
        "id": "temple",
        "name_en": "Meenakshi Temple",
        "name_ta": "மீனாட்சி அம்மன் கோவில்",
        "icon": "🛕",
        "img": "uploads/visual_cards/temple.jpg"
    },
    {
        "id": "rose",
        "name_en": "Fragrant Rose",
        "name_ta": "மணக்கும் ரோஜா",
        "icon": "🌹",
        "img": "uploads/visual_cards/rose.jpg"
    },
    {
        "id": "clock",
        "name_en": "Vintage Clock",
        "name_ta": "சுவர்க் கடிகாரம்",
        "icon": "🕰️",
        "img": "uploads/visual_cards/clock.jpg"
    },
    {
        "id": "dog",
        "name_en": "Loving Pet Dog",
        "name_ta": "வளர்ப்பு நாய்",
        "icon": "🐕",
        "img": "uploads/visual_cards/dog.jpg"
    },
    {
        "id": "apple",
        "name_en": "Sweet Apple",
        "name_ta": "சுவையான ஆப்பிள்",
        "icon": "🍎",
        "img": "uploads/visual_cards/apple.jpg"
    }
]


def build_pair_deck(patient_id: int, num_pairs: int, db=None) -> List[Dict[str, Any]]:
    """
    Constructs a shuffled deck of paired cards.
    Prioritizes real caregiver-uploaded family photos from the Memory Vault,
    supplemented with recognizable everyday cultural memory cards.
    """
    selected_items = []
    
    # 1. Fetch personal caregiver memories from DB if available
    if db:
        try:
            vault_mems = db.get_patient_memories(patient_id)
            for m in vault_mems:
                img_path = m.get("image_path", "")
                if img_path and os.path.exists(img_path):
                    selected_items.append({
                        "id": f"vault_{m['id']}",
                        "name_en": m["label_en"],
                        "name_ta": m["label_ta"],
                        "icon": "🖼️",
                        "img": img_path
                    })
        except Exception:
            pass

    # 2. Add standard curated items if we need more
    for item in STANDARD_MEMORY_PAIRS_CATALOG:
        if len(selected_items) >= num_pairs:
            break
        # Avoid duplicate IDs
        if not any(x["id"] == item["id"] for x in selected_items):
            selected_items.append(item)

    # Slice to exact count
    final_items = selected_items[:num_pairs]

    # Duplicate each item to make a pair
    deck = []
    for pair_idx, item in enumerate(final_items):
        card_a = {
            "card_id": f"{item['id']}_A",
            "pair_key": item["id"],
            "name_en": item["name_en"],
            "name_ta": item["name_ta"],
            "icon": item["icon"],
            "img": item["img"]
        }
        card_b = {
            "card_id": f"{item['id']}_B",
            "pair_key": item["id"],
            "name_en": item["name_en"],
            "name_ta": item["name_ta"],
            "icon": item["icon"],
            "img": item["img"]
        }
        deck.extend([card_a, card_b])

    random.seed(int(time.time() * 1000) % 100000)
    random.shuffle(deck)
    return deck


def render_memory_pairs_game(patient: Dict[str, Any], db=None, lang: str = "en"):
    """
    Renders the Concentration / Memory Matching Pairs Game.
    """
    st.markdown(f"### 🃏 {'ஜோடி நினைவாற்றல் விளையாட்டு (Memory Matching Pairs)' if lang == 'ta' else 'Memory Matching Pairs Challenge'}")
    sub_title_text = (
        "மறைந்துள்ள பட அட்டைகளைத் திறந்து ஒரே மாதிரியான ஜோடிகளைக் கண்டறியவும்"
        if lang == "ta"
        else "Flip over the cards to find and remember matching pairs of cherished photos and items."
    )
    st.markdown(
        f"""
        <div style="background: #EFF6FF; border-left: 5px solid #2563EB; padding: 10px 16px; border-radius: 8px; margin-bottom: 14px;">
            <span style="color: #1E3A8A; font-size: 16px; font-weight: 700;">
                ℹ️ {sub_title_text}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- FULLSCREEN CELEBRATION MODAL WITH BALLOONS, ANIMALS & RHYMES ---
    if st.session_state.get("pairs_show_celebration", False):
        def on_continue():
            st.session_state.pairs_show_celebration = False
            st.rerun()
        render_celebration(
            rhyme_idx=st.session_state.get("pairs_celebration_idx", 0),
            lang=lang,
            on_continue=on_continue
        )
        return

    curr_lvl = patient.get("current_adaptive_level", 2)
    diff_str, diff_num = render_difficulty_selector("memory_pairs", lang=lang, default_lvl=curr_lvl)

    # Pairs count based on difficulty
    pairs_count_map = {"easy": 3, "medium": 4, "hard": 6}
    target_pairs = pairs_count_map.get(diff_str, 3)

    # Session State Initialization
    if "pairs_diff_tracked" not in st.session_state or st.session_state.pairs_diff_tracked != diff_str:
        st.session_state.pairs_diff_tracked = diff_str
        st.session_state.pairs_deck = build_pair_deck(patient["id"], target_pairs, db=db)
        st.session_state.pairs_flipped = []  # Indices of currently flipped unmatched cards (0, 1, or 2)
        st.session_state.pairs_matched = set()  # Set of matched indices
        st.session_state.pairs_moves = 0
        st.session_state.pairs_start_time = time.time()
        st.session_state.pairs_completed = False
        st.session_state.pairs_feedback = None

    if "pairs_deck" not in st.session_state:
        st.session_state.pairs_deck = build_pair_deck(patient["id"], target_pairs, db=db)
    if "pairs_flipped" not in st.session_state:
        st.session_state.pairs_flipped = []
    if "pairs_matched" not in st.session_state:
        st.session_state.pairs_matched = set()
    if "pairs_moves" not in st.session_state:
        st.session_state.pairs_moves = 0
    if "pairs_start_time" not in st.session_state:
        st.session_state.pairs_start_time = time.time()
    if "pairs_completed" not in st.session_state:
        st.session_state.pairs_completed = False
    if "pairs_feedback" not in st.session_state:
        st.session_state.pairs_feedback = None

    deck = st.session_state.pairs_deck
    flipped = st.session_state.pairs_flipped
    matched = st.session_state.pairs_matched

    # Immediate Interactive Celebration when a correct matching pair is clicked!
    if st.session_state.get("pairs_show_celebration", False):
        c_idx = st.session_state.get("pairs_celebration_idx", 0)
        def on_cont_pair():
            st.session_state.pairs_show_celebration = False
            st.rerun()
        render_celebration(rhyme_idx=c_idx, lang=lang, on_continue=on_cont_pair)
        return

    # Top Status Bar
    m1, m2, m3 = st.columns(3)
    matched_pairs_count = len(matched) // 2
    m1.metric(
        label="கண்டறிந்த ஜோடிகள்" if lang == "ta" else "Pairs Matched",
        value=f"{matched_pairs_count} / {target_pairs} 🎯"
    )
    m2.metric(
        label="முயற்சிகள் (Moves)" if lang == "ta" else "Total Turns",
        value=f"{st.session_state.pairs_moves}"
    )
    diff_labels_ta = {"easy": "🟢 எளிது (3 ஜோடிகள்)", "medium": "🟡 நடுத்தரம் (4 ஜோடிகள்)", "hard": "🔴 கடினம் (6 ஜோடிகள்)"}
    diff_labels_en = {"easy": "🟢 Easy (3 Pairs)", "medium": "🟡 Medium (4 Pairs)", "hard": "🔴 Hard (6 Pairs)"}
    m3.metric(
        label="தேர்ந்தெடுத்த நிலை" if lang == "ta" else "Active Level",
        value=diff_labels_ta.get(diff_str, "") if lang == "ta" else diff_labels_en.get(diff_str, "")
    )

    # Audio guidance
    voice_prompt = (
        "அட்டைகளை ஒவ்வொன்றாகத் திறந்து, அவற்றின் இருப்பிடத்தை நினைவில் வைத்து சரியான ஜோடிகளை இணையுங்கள்."
        if lang == "ta"
        else "Tap cards one by one to reveal them. Memorize where each item is to find all matching pairs."
    )
    st.markdown("---")

    st.markdown("""
    <style>
        .pair-card-front {
            animation: cardFlipIn 0.35s ease-out;
        }
        @keyframes cardFlipIn {
            0% { transform: scaleX(0); opacity: 0; }
            100% { transform: scaleX(1); opacity: 1; }
        }
        .pair-card-matched {
            animation: matchGlow 2s infinite alternate ease-in-out;
            border: 2px solid #4ADE80 !important;
        }
        @keyframes matchGlow {
            0% { box-shadow: 0 0 8px rgba(74, 222, 128, 0.35); }
            100% { box-shadow: 0 0 22px rgba(74, 222, 128, 0.85); transform: scale(1.02); }
        }
    </style>
    """, unsafe_allow_html=True)

    # Feedback Banner if two cards just flipped
    if st.session_state.pairs_feedback:
        fb_type, fb_msg_en, fb_msg_ta = st.session_state.pairs_feedback
        if fb_type == "match":
            st.success(f"🎉 {fb_msg_ta if lang == 'ta' else fb_msg_en}")
        else:
            st.warning(f"💡 {fb_msg_ta if lang == 'ta' else fb_msg_en}")

    # --------------------------------------------------------------------------
    # CARD GRID RENDERING
    # --------------------------------------------------------------------------
    # Columns per row: 3 for easy (6 cards = 2x3), 4 for medium/hard (8 cards = 2x4, 12 cards = 3x4)
    cols_per_row = 3 if target_pairs == 3 else 4
    num_cards = len(deck)

    for row_start in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            card_idx = row_start + col_idx
            if card_idx >= num_cards:
                break

            card = deck[card_idx]
            is_matched = card_idx in matched
            is_flipped = card_idx in flipped or is_matched

            card_name = card["name_ta"] if lang == "ta" else card["name_en"]
            btn_key = f"pair_card_{card_idx}_{st.session_state.pairs_moves}_{lang}"

            with cols[col_idx]:
                with st.container(border=True):
                    if is_flipped:
                        # Card is Face-Up
                        img_path = card.get("img", "")
                        if img_path and os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)
                        else:
                            st.markdown(
                                f"<div style='font-size: 60px; text-align: center; padding: 25px 0;'>{card['icon']}</div>",
                                unsafe_allow_html=True
                            )
                        
                        # Label
                        if is_matched:
                            st.markdown(
                                f"<div style='text-align: center; color: #4ADE80; font-weight: 800; font-size: 16px; margin-top: 6px;'>"
                                f"✅ {card_name}</div>",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"<div style='text-align: center; color: #FBBF24; font-weight: 800; font-size: 16px; margin-top: 6px;'>"
                                f"👁️ {card_name}</div>",
                                unsafe_allow_html=True
                            )
                    else:
                        # Card is Face-Down (Accessible, Warm Pattern)
                        st.markdown(
                            f"""
                            <div style="height: 190px; display: flex; flex-direction: column; 
                                        justify-content: center; align-items: center; 
                                        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); 
                                        border: 2px dashed #475569; border-radius: 10px; cursor: pointer;">
                                <div style="font-size: 42px; margin-bottom: 5px;">🎴</div>
                                <div style="font-size: 14px; font-weight: bold; color: #94A3B8;">
                                    {'தட்டவும்' if lang == 'ta' else 'Tap to Flip'}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        flip_label = "🔍 " + ("திறக்க" if lang == "ta" else "Flip Card")
                        if st.button(flip_label, key=btn_key, use_container_width=True):
                            # Handle Flip Logic
                            if len(flipped) == 0:
                                st.session_state.pairs_flipped = [card_idx]
                                st.session_state.pairs_feedback = None
                                st.rerun()
                            elif len(flipped) == 1:
                                if card_idx == flipped[0]:
                                    pass  # Clicked the exact same card
                                else:
                                    first_idx = flipped[0]
                                    first_card = deck[first_idx]
                                    st.session_state.pairs_moves += 1
                                    
                                    # Check match
                                    if first_card["pair_key"] == card["pair_key"]:
                                        st.session_state.pairs_matched.add(first_idx)
                                        st.session_state.pairs_matched.add(card_idx)
                                        st.session_state.pairs_flipped = []
                                        st.session_state.pairs_show_celebration = True
                                        st.session_state.pairs_celebration_idx = random.randint(0, len(CELEBRATION_RHYMES) - 1)
                                        item_name = card["name_ta"] if lang == "ta" else card["name_en"]
                                        st.session_state.pairs_feedback = (
                                            "match",
                                            f"Wonderful! You found the matching pair for {item_name}!",
                                            f"அருமை! {item_name} ஜோடியைச் சரியாகக் கண்டுபிடித்துவிட்டீர்கள்!"
                                        )
                                    else:
                                        st.session_state.pairs_flipped = [first_idx, card_idx]
                                        st.session_state.pairs_feedback = (
                                            "mismatch",
                                            "Not a match. Take a moment to memorize where they are, then tap Continue.",
                                            "ஜோடி பொருந்தவில்லை. சிறிது நினைவில் வைத்துக்கொண்டு அடுத்த அட்டையைத் திறக்கவும்."
                                        )
                                    st.rerun()
                            elif len(flipped) == 2:
                                # Two unmatched cards are shown, clicking a new card resets them
                                st.session_state.pairs_flipped = [card_idx]
                                st.session_state.pairs_feedback = None
                                st.rerun()

    # If 2 cards are currently flipped and don't match, show "Flip Back" button
    if len(flipped) == 2 and not st.session_state.pairs_completed:
        st.markdown("<br>", unsafe_allow_html=True)
        flip_back_label = "🔄 " + ("அட்டைகளை மூடி மீண்டும் முயற்சிக்கவும் (Continue)" if lang == "ta" else "Flip Back & Continue")
        if st.button(flip_back_label, key="pairs_continue_turn_btn", use_container_width=True, type="primary"):
            st.session_state.pairs_flipped = []
            st.session_state.pairs_feedback = None
            st.rerun()

    # --------------------------------------------------------------------------
    # COMPLETION CELEBRATION
    # --------------------------------------------------------------------------
    if len(matched) == len(deck) and len(deck) > 0 and not st.session_state.pairs_completed:
        st.session_state.pairs_completed = True
        rt = round(time.time() - st.session_state.pairs_start_time, 2)
        accuracy = max(50.0, round((target_pairs / max(target_pairs, st.session_state.pairs_moves)) * 100, 1))

        # Record to Database
        if db:
            try:
                db.record_session(
                    patient_id=patient["id"],
                    cognitive_domain="memory",
                    game_name="Memory Matching Pairs",
                    start_level=diff_num,
                    end_level=min(5, diff_num + 1 if accuracy >= 80.0 else diff_num),
                    total_trials=target_pairs,
                    correct_trials=target_pairs,
                    accuracy_pct=accuracy,
                    avg_response_time_sec=round(rt / target_pairs, 2),
                    fatigue_events=0,
                    caregiver_notes=f"Completed {target_pairs} memory pairs in {st.session_state.pairs_moves} moves."
                )
            except Exception:
                pass

        cheer_text = (
            f"அற்புதம்! அனைத்து {target_pairs} ஜோடிகளையும் வெற்றிகரமாகக் கண்டறிந்துவிட்டீர்கள்!"
            if lang == "ta"
            else f"Outstanding work! You successfully matched all {target_pairs} pairs with great memory recall!"
        )
        st.success(f"🎉 **{cheer_text}** (⏱️ {rt}{'வி' if lang == 'ta' else 's'} | {st.session_state.pairs_moves} {'நகர்வுகள்' if lang == 'ta' else 'moves'})")
        render_celebration(rhyme_idx=0, lang=lang)

    # Reset / Play Again
    if st.session_state.pairs_completed:
        st.markdown("<br>", unsafe_allow_html=True)
        again_label = "➡️ " + ("புதிய ஜோடி விளையாட்டு (Play Another Round)" if lang == "ta" else "Play Another Round")
        if st.button(again_label, key="pairs_play_again_btn", use_container_width=True, type="primary"):
            st.session_state.pairs_deck = build_pair_deck(patient["id"], target_pairs, db=db)
            st.session_state.pairs_flipped = []
            st.session_state.pairs_matched = set()
            st.session_state.pairs_moves = 0
            st.session_state.pairs_start_time = time.time()
            st.session_state.pairs_completed = False
            st.session_state.pairs_feedback = None
            st.rerun()
