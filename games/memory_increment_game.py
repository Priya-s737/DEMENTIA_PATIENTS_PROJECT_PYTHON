"""
Memory Increment Game: Working Memory Span & Sequential Recall.
A scientifically validated cognitive training exercise for dementia, MCI, and memory increment.
Presents a progressively increasing sequence of visual items (Span N = 2, 3, 4, 5...) that the senior memorizes and recalls in order.
100% Pure Tamil and Pure English localization with speech audio.
"""

import streamlit as st
import time
import random
from typing import Dict, Any, List
from modules.voice_assistant import VoiceAssistant
from modules.difficulty import render_difficulty_selector
from modules.celebration import render_celebration

MEMORY_SYMBOLS = [
    {"id": "apple", "icon": "🍎", "name_en": "Apple", "name_ta": "ஆப்பிள்"},
    {"id": "banana", "icon": "🍌", "name_en": "Banana", "name_ta": "வாழைப்பழம்"},
    {"id": "grapes", "icon": "🍇", "name_en": "Grapes", "name_ta": "திராட்சை"},
    {"id": "mango", "icon": "🥭", "name_en": "Mango", "name_ta": "மாம்பழம்"},
    {"id": "flower", "icon": "🌺", "name_en": "Flower", "name_ta": "மலர்"},
    {"id": "star", "icon": "⭐", "name_en": "Star", "name_ta": "நட்சத்திரம்"},
    {"id": "bell", "icon": "🔔", "name_en": "Temple Bell", "name_ta": "மணி"},
    {"id": "sun", "icon": "☀️", "name_en": "Sun", "name_ta": "சூரியன்"}
]

def render_memory_increment_game(patient: Dict[str, Any], lang: str = "en"):
    st.markdown(f"### 🔢 {'நினைவுத்திறன் அதிகரிப்புப் பயிற்சி (Memory Span Increment)' if lang == 'ta' else 'Memory Span Increment Challenge'}")
    mem_inc_sub = (
        "வரிசையாகத் தோன்றும் படங்களை நினைவில் வைத்து, அதே வரிசையில் தட்டவும்"
        if lang == "ta"
        else "Memorize the sequence of items and tap them back in the exact same order."
    )
    st.markdown(
        f"""
        <div style="background: #EFF6FF; border-left: 5px solid #2563EB; padding: 10px 16px; border-radius: 8px; margin-bottom: 14px;">
            <span style="color: #1E3A8A; font-size: 16px; font-weight: 700;">
                ℹ️ {mem_inc_sub}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- EASY / MEDIUM / HARD DIFFICULTY SELECTOR ---
    diff_str, diff_num = render_difficulty_selector("memory_increment", lang=lang, default_lvl=patient.get("current_adaptive_level", 2))

    # Base span length by difficulty tier: Easy: 2, Medium: 3, Hard: 4
    base_span_by_diff = {"easy": 2, "medium": 3, "hard": 4}

    # Initialize Session State
    if "mem_span_diff_tracked" not in st.session_state or st.session_state.mem_span_diff_tracked != diff_str:
        st.session_state.mem_span_diff_tracked = diff_str
        st.session_state.mem_span_level = base_span_by_diff.get(diff_str, 2)
        st.session_state.mem_span_target_seq = []
        st.session_state.mem_span_user_seq = []
        st.session_state.mem_span_phase = "memorize"

    if "mem_span_level" not in st.session_state:
        st.session_state.mem_span_level = base_span_by_diff.get(diff_str, 2)
    if "mem_span_target_seq" not in st.session_state:
        st.session_state.mem_span_target_seq = []
    if "mem_span_user_seq" not in st.session_state:
        st.session_state.mem_span_user_seq = []
    if "mem_span_phase" not in st.session_state:
        st.session_state.mem_span_phase = "memorize"
    if "mem_span_score" not in st.session_state:
        st.session_state.mem_span_score = 0
    if "mem_span_start_time" not in st.session_state:
        st.session_state.mem_span_start_time = time.time()

    # Generate new sequence if empty
    if not st.session_state.mem_span_target_seq:
        span_len = st.session_state.mem_span_level
        chosen = random.sample(MEMORY_SYMBOLS, span_len)
        st.session_state.mem_span_target_seq = chosen
        st.session_state.mem_span_user_seq = []
        st.session_state.mem_span_phase = "memorize"
        st.session_state.mem_span_start_time = time.time()

    target_seq = st.session_state.mem_span_target_seq
    current_span = len(target_seq)

    # Top Metric Bar
    m1, m2, m3 = st.columns(3)
    m1.metric(
        label="நினைவு நிலை (Span Length)" if lang == "ta" else "Current Memory Span",
        value=f"{current_span} {'படங்கள்' if lang == 'ta' else 'Items'}"
    )
    m2.metric(
        label="வெற்றி மதிப்பெண்" if lang == "ta" else "Total Score",
        value=f"{st.session_state.mem_span_score} {'புள்ளிகள்' if lang == 'ta' else 'Points'}"
    )
    diff_badge_text = {"easy": "🟢 Easy (Span 2)", "medium": "🟡 Medium (Span 3)", "hard": "🔴 Hard (Span 4)"}
    diff_badge_ta = {"easy": "🟢 எளிது (2 படங்கள்)", "medium": "🟡 நடுத்தரம் (3 படங்கள்)", "hard": "🔴 கடினம் (4 படங்கள்)"}
    m3.metric(
        label="தேர்ந்தெடுத்த நிலை" if lang == "ta" else "Selected Difficulty",
        value=diff_badge_ta.get(diff_str, "🟡 நடுத்தரம்") if lang == "ta" else diff_badge_text.get(diff_str, "🟡 Medium")
    )

    st.divider()

    # PHASE 1: MEMORIZATION PHASE
    if st.session_state.mem_span_phase == "memorize":
        prompt_text = (
            f"கீழே உள்ள {current_span} படங்களை வரிசைப்படி கவனமாகப் பார்த்து நினைவில் வையுங்கள்:"
            if lang == "ta"
            else f"Carefully memorize this sequence of {current_span} items in order:"
        )
        st.components.v1.html(VoiceAssistant.get_speech_html(prompt_text, lang=lang), height=55)
        st.markdown(f"#### 👁️ {prompt_text}")

        seq_cols = st.columns(current_span)
        for idx, item in enumerate(target_seq):
            with seq_cols[idx]:
                item_name = item["name_ta"] if lang == "ta" else item["name_en"]
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
                                color: white; padding: 25px 10px; border-radius: 16px; 
                                text-align: center; margin: 10px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                        <div style="font-size: 20px; font-weight: bold; background: rgba(255,255,255,0.2); 
                                    width: 36px; height: 36px; line-height: 36px; border-radius: 50%; margin: 0 auto 8px auto;">
                            {idx + 1}
                        </div>
                        <div style="font-size: 55px; margin: 5px 0;">{item['icon']}</div>
                        <div style="font-size: 16px; font-weight: 600;">{item_name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧠 " + ("நினைவில் வைத்துவிட்டேன்! (தொடங்கவும்)" if lang == "ta" else "I Memorized It! (Start Recall)"), key="span_memorized_btn", use_container_width=True):
            st.session_state.mem_span_phase = "recall"
            st.session_state.mem_span_user_seq = []
            st.session_state.mem_span_start_time = time.time()
            st.rerun()

    # PHASE 2: RECALL & TAPPING PHASE
    elif st.session_state.mem_span_phase == "recall":
        prompt_recall = (
            f"நீங்கள் பார்த்த படங்களை அதே வரிசையில் தட்டவும் ({len(st.session_state.mem_span_user_seq)} / {current_span}):"
            if lang == "ta"
            else f"Tap the items in the EXACT sequence you saw ({len(st.session_state.mem_span_user_seq)} / {current_span}):"
        )
        st.markdown(f"#### ✍️ {prompt_recall}")

        if st.session_state.mem_span_user_seq:
            st.markdown("**" + ("நீங்கள் தேர்வு செய்த வரிசை:" if lang == "ta" else "Your Selected Sequence:") + "**")
            tapped_cols = st.columns(max(current_span, len(st.session_state.mem_span_user_seq)))
            for idx, item in enumerate(st.session_state.mem_span_user_seq):
                with tapped_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="background-color: #E2E8F0; padding: 12px; border-radius: 10px; text-align: center;">
                            <span style="font-size: 32px;">{item['icon']}</span>
                            <div style="font-size: 12px; font-weight: bold; color: #1E293B;">{idx + 1}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("💡 " + ("கீழே உள்ள பொத்தான்களில் சரியான படங்களை வரிசையாகத் தட்டவும்." if lang == "ta" else "Tap the buttons below in the correct sequence."))

        st.markdown("---")

        st.markdown(f"**{'படத்தைத் தேர்ந்தெடுக்கவும்:' if lang == 'ta' else 'Choose item:'}**")
        keypad_cols = st.columns(4)
        for idx, sym in enumerate(MEMORY_SYMBOLS):
            with keypad_cols[idx % 4]:
                sym_label = f"{sym['icon']} {sym['name_ta'] if lang == 'ta' else sym['name_en']}"
                if st.button(sym_label, key=f"keypad_sym_{sym['id']}_{len(st.session_state.mem_span_user_seq)}_{lang}", use_container_width=True):
                    st.session_state.mem_span_user_seq.append(sym)

                    if len(st.session_state.mem_span_user_seq) == current_span:
                        st.session_state.mem_span_phase = "feedback"
                    st.rerun()

        if st.session_state.mem_span_user_seq:
            if st.button("🔄 " + ("மீண்டும் தேர்ந்தெடுக்க" if lang == "ta" else "Clear / Retap Choices"), key="clear_span_choices"):
                st.session_state.mem_span_user_seq = []
                st.rerun()

    # PHASE 3: FEEDBACK & AUTO-INCREMENT
    elif st.session_state.mem_span_phase == "feedback":
        rt = round(time.time() - st.session_state.mem_span_start_time, 2)
        user_seq_ids = [item["id"] for item in st.session_state.mem_span_user_seq]
        target_seq_ids = [item["id"] for item in target_seq]

        is_correct = (user_seq_ids == target_seq_ids)

        if is_correct:
            st.session_state.mem_span_score += (current_span * 10)
            st.success(
                f"🎉 **{'அற்புதம்! முழு வரிசையையும் மிகச் சரியாக நினைவில் வைத்துள்ளீர்கள்!' if lang == 'ta' else 'Outstanding! Perfect sequential recall!'}** (⏱️ {rt}{'வி' if lang == 'ta' else 's'})"
            )
            render_celebration(rhyme_idx=2, lang=lang)
            
            if current_span < 6:
                st.info(f"🚀 **{'நினைவுத்திறன் அதிகரிப்பு' if lang == 'ta' else 'Memory Span Increment'}:** {'அடுத்த சுற்றில்' if lang == 'ta' else 'Increasing next challenge to'} **{current_span + 1} {'படங்கள்' if lang == 'ta' else 'items'}**!")
                next_span_target = current_span + 1
            else:
                next_span_target = current_span
        else:
            st.warning(
                f"💡 **{'சிறிது தவறிவிட்டது! பரவாயில்லை, தொடர்ந்து பயிற்சி செய்வோம்.' if lang == 'ta' else 'Almost there! Keep practicing.'}**"
            )
            st.markdown(
                f"**{'சரியான வரிசை:' if lang == 'ta' else 'The correct sequence was:'}** " + " ➔ ".join([f"{item['icon']} {item['name_ta'] if lang == 'ta' else item['name_en']}" for item in target_seq])
            )
            next_span_target = max(2, current_span - 1 if current_span > 2 else 2)

        if st.button("➡️ " + ("அடுத்த நினைவாற்றல் பயிற்சி" if lang == "ta" else "Next Memory Challenge"), key="next_span_round_btn", use_container_width=True):
            st.session_state.mem_span_level = next_span_target
            st.session_state.mem_span_target_seq = []
            st.session_state.mem_span_user_seq = []
            st.session_state.mem_span_phase = "memorize"
            st.rerun()
