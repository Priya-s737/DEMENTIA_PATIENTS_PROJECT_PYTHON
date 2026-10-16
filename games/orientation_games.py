"""
Temporal & Spatial Orientation Cognitive Domain Games:
1. Temporal Reality Orientation (Time of Day, Season, Calendar)
2. Spatial Home Environment & Daily Living Orientation (ADL)
Strictly localized with rich visual icons/emojis on all option buttons.
"""

import streamlit as st
import time
import os
import random
from datetime import datetime
from typing import Dict, Any
from modules.voice_assistant import VoiceAssistant
from modules.visual_assets import resolve_option_visual, resolve_distinct_option_visuals
from modules.difficulty import render_difficulty_selector

ROOM_ICONS = {
    "சமையலறை": "🍳",
    "Kitchen": "🍳",
    "படுக்கையறை": "🛏️",
    "Bedroom": "🛏️",
    "வீட்டுத் தோட்டம்": "🌺",
    "Garden": "🌺",
    "முன் வராண்டா": "🚪",
    "Front Porch": "🚪",
    "பால்கனி": "🏙️",
    "Balcony": "🏙️",
    "சாப்பாட்டு கூடம்": "🍽️",
    "Dining Hall": "🍽️",
    "குளியலறை": "🚿",
    "Bathroom": "🚿",
    "வரவேற்பறை": "🛋️",
    "Living Room": "🛋️",
    "பொருளறை": "📦",
    "Store Room": "📦",
    "Pantry": "🥫"
}

def render_orientation_game(patient: Dict[str, Any], lang: str = "en"):
    st.markdown(f"### 🧭 {'காலம் மற்றும் இட விழிப்புணர்வு' if lang == 'ta' else 'Temporal & Spatial Reality Orientation'}")

    if "ori_game_sub" not in st.session_state:
        st.session_state.ori_game_sub = "temporal"
    if "ori_trials" not in st.session_state:
        st.session_state.ori_trials = []
    if "ori_current_trial" not in st.session_state:
        st.session_state.ori_current_trial = 1
    if "ori_trial_start_time" not in st.session_state:
        st.session_state.ori_trial_start_time = time.time()
    if "ori_feedback" not in st.session_state:
        st.session_state.ori_feedback = None

    curr_lvl = patient.get("current_adaptive_level", 2)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🕒 " + ("நேரம் மற்றும் கால விழிப்புணர்வு" if lang == "ta" else "Time & Calendar Reality"), use_container_width=True):
            st.session_state.ori_game_sub = "temporal"
            st.session_state.ori_stimulus = None
            st.session_state.ori_feedback = None
            st.rerun()
    with col2:
        if st.button("🏡 " + ("வீட்டு சூழல் மற்றும் இருப்பிடம்" if lang == "ta" else "Spatial Home Environment"), use_container_width=True):
            st.session_state.ori_game_sub = "spatial"
            st.session_state.ori_spatial_stim = None
            st.session_state.ori_feedback = None
            st.rerun()

    st.divider()

    # --- EASY / MEDIUM / HARD DIFFICULTY SELECTOR ---
    diff_str, diff_num = render_difficulty_selector("orientation", lang=lang, default_lvl=curr_lvl)

    # --- SUB-GAME 1: TEMPORAL ORIENTATION ---
    if st.session_state.ori_game_sub == "temporal":
        if (
            "ori_stimulus" not in st.session_state 
            or st.session_state.ori_stimulus is None 
            or st.session_state.ori_stimulus.get("lang") != lang
            or st.session_state.ori_stimulus.get("difficulty") != diff_str
        ):
            now = datetime.now()
            current_hour = now.hour

            if 5 <= current_hour < 12:
                time_of_day_en = "🌅 Morning"
                time_of_day_ta = "🌅 காலை நேரம்"
                icon = "🌅"
            elif 12 <= current_hour < 17:
                time_of_day_en = "☀️ Afternoon"
                time_of_day_ta = "☀️ மதிய நேரம்"
                icon = "☀️"
            elif 17 <= current_hour < 20:
                time_of_day_en = "🌇 Evening"
                time_of_day_ta = "🌇 மாலை நேரம்"
                icon = "🌇"
            else:
                time_of_day_en = "🌙 Night"
                time_of_day_ta = "🌙 இரவு நேரம்"
                icon = "🌙"

            current_day_en = now.strftime("%A")
            current_day_ta = {
                "Monday": "திங்கட்கிழமை", "Tuesday": "செவ்வாய்க்கிழமை", "Wednesday": "புதன்கிழமை",
                "Thursday": "வியாழக்கிழமை", "Friday": "வெள்ளிக்கிழமை", "Saturday": "சனிக்கிழமை", "Sunday": "ஞாயிற்றுக்கிழமை"
            }.get(current_day_en, current_day_en)

            q_type = random.choice(["time_of_day", "day_of_week"])

            if q_type == "time_of_day":
                target_ans = time_of_day_ta if lang == "ta" else time_of_day_en
                all_opts = [
                    "🌅 காலை நேரம்" if lang == "ta" else "🌅 Morning",
                    "☀️ மதிய நேரம்" if lang == "ta" else "☀️ Afternoon",
                    "🌇 மாலை நேரம்" if lang == "ta" else "🌇 Evening",
                    "🌙 இரவு நேரம்" if lang == "ta" else "🌙 Night"
                ]
                prompt = (
                    f"இப்போது வானிலை மற்றும் வெளிச்சத்தைப் பார்த்து இது எந்த நேரம் என்று கூறுங்கள்: {icon}"
                    if lang == "ta"
                    else f"Looking outside or checking your daily routine, what time of day is it right now? {icon}"
                )
            else:
                target_ans = f"📅 {current_day_ta}" if lang == "ta" else f"📅 {current_day_en}"
                days_en = [f"📅 {d}" for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
                days_ta = [f"📅 {d}" for d in ["திங்கட்கிழமை", "செவ்வாய்க்கிழமை", "புதன்கிழமை", "வியாழக்கிழமை", "வெள்ளிக்கிழமை", "சனிக்கிழமை", "ஞாயிற்றுக்கிழமை"]]
                all_opts = days_ta if lang == "ta" else days_en
                prompt = (
                    "இன்று வாரத்தின் என்ன கிழமை என்று கூறுங்கள்:"
                    if lang == "ta"
                    else "What day of the week is it today?"
                )

            num_choices = 2 if diff_str == "easy" else (3 if diff_str == "medium" else 4)
            distractors = [o for o in all_opts if o != target_ans]
            chosen_d = random.sample(distractors, num_choices - 1)
            options = [target_ans] + chosen_d
            random.shuffle(options)

            st.session_state.ori_stimulus = {
                "prompt": prompt,
                "target": target_ans,
                "options": options,
                "icon": icon,
                "difficulty": diff_str,
                "lang": lang
            }
            st.session_state.ori_trial_start_time = time.time()
            st.session_state.ori_feedback = None

        stim = st.session_state.ori_stimulus

        st.components.v1.html(VoiceAssistant.get_speech_html(stim["prompt"], lang=lang), height=60)
        st.markdown(f"#### {stim['prompt']}")

        st.markdown("<br>", unsafe_allow_html=True)

        opt_cols = st.columns(len(stim["options"]))
        distinct_visuals = resolve_distinct_option_visuals(stim["options"])
        for idx, (col, opt, (opt_img, opt_icon)) in enumerate(zip(opt_cols, stim["options"], distinct_visuals)):
            with col:
                with st.container(border=True):
                    if opt_img and os.path.exists(opt_img):
                        st.image(opt_img, use_container_width=True)
                    btn_key = f"ori_btn_{idx}_{st.session_state.ori_current_trial}_{lang}"
                    btn_label = opt if any(opt.strip().startswith(c) for c in ["🌅", "☀️", "🌇", "🌙", "📅", opt_icon]) else f"{opt_icon} {opt}"
                    if st.button(btn_label, key=btn_key, use_container_width=True):
                        rt = round(time.time() - st.session_state.ori_trial_start_time, 2)
                        is_correct = (opt == stim["target"])

                        st.session_state.ori_trials.append({
                            "stimulus": "Temporal Orientation",
                            "target_response": stim["target"],
                            "user_response": opt,
                            "is_correct": is_correct,
                            "response_time_sec": rt,
                            "difficulty_level": diff_num
                        })

                        st.session_state.ori_feedback = {
                            "is_correct": is_correct,
                            "correct_answer": stim["target"],
                            "rt": rt
                        }
                        st.rerun()

        if st.session_state.ori_feedback:
            fb = st.session_state.ori_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'மிகச் சரியான விடை!' if lang == 'ta' else 'Accurate reality orientation!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
            else:
                st.warning(f"💡 {'சரியான விடை:' if lang == 'ta' else 'The correct answer is:'} **{fb['correct_answer']}**.")

            if st.button("➡️ " + ("அடுத்த கேள்வி" if lang == "ta" else "Next Question"), key="ori_next_btn", use_container_width=True):
                st.session_state.ori_current_trial += 1
                st.session_state.ori_stimulus = None
                st.session_state.ori_feedback = None
                st.rerun()

    # --- SUB-GAME 2: SPATIAL HOME ENVIRONMENT ---
    elif st.session_state.ori_game_sub == "spatial":
        spatial_tasks_en = [
            {"prompt": "Where in the house do you prepare hot filter coffee or food?", "target": "Kitchen", "options": ["Kitchen", "Bedroom", "Garden", "Living Room"]},
            {"prompt": "Where do you go to sleep and take a peaceful night's rest?", "target": "Bedroom", "options": ["Bedroom", "Dining Hall", "Kitchen", "Front Porch"]},
            {"prompt": "Where do you water the flowering rose plants and smell fresh flowers?", "target": "Garden", "options": ["Garden", "Bathroom", "Living Room", "Kitchen"]},
            {"prompt": "Where do you sit to read the morning newspaper and greet visitors?", "target": "Front Porch", "options": ["Front Porch", "Kitchen", "Bedroom", "Dining Hall"]},
            {"prompt": "Where do you take a refreshing bath and wash hands with soap?", "target": "Bathroom", "options": ["Bathroom", "Kitchen", "Front Porch", "Garden"]},
            {"prompt": "Where does the family sit together to enjoy lunch and dinner?", "target": "Dining Hall", "options": ["Dining Hall", "Bathroom", "Bedroom", "Front Porch"]}
        ]
        spatial_tasks_ta = [
            {"prompt": "வீட்டில் சூடான பில்டர் காபி அல்லது சுவையான உணவு எங்கு சமைப்பீர்கள்?", "target": "சமையலறை", "options": ["சமையலறை", "படுக்கையறை", "வீட்டுத் தோட்டம்", "வரவேற்பறை"]},
            {"prompt": "இரவில் அமைதியாக உறங்க எங்கு செல்வீர்கள்?", "target": "படுக்கையறை", "options": ["படுக்கையறை", "சாப்பாட்டு கூடம்", "சமையலறை", "முன் வராண்டா"]},
            {"prompt": "ரோஜா செடிகளுக்கு தண்ணீர் ஊற்ற எங்கு செல்வீர்கள்?", "target": "வீட்டுத் தோட்டம்", "options": ["வீட்டுத் தோட்டம்", "குளியலறை", "வரவேற்பறை", "சமையலறை"]},
            {"prompt": "காலை செய்திதாள் வாசித்து விருந்தினரை வரவேற்கும் இடம் எது?", "target": "முன் வராண்டா", "options": ["முன் வராண்டா", "சமையலறை", "படுக்கையறை", "சாப்பாட்டு கூடம்"]},
            {"prompt": "குளித்து முகம் கழுவ எங்கு செல்வீர்கள்?", "target": "குளியலறை", "options": ["குளியலறை", "சமையலறை", "முன் வராண்டா", "வீட்டுத் தோட்டம்"]},
            {"prompt": "குடும்பத்தினர் அனைவரும் ஒன்றாக அமர்ந்து உணவு உண்ணும் இடம் எது?", "target": "சாப்பாட்டு கூடம்", "options": ["சாப்பாட்டு கூடம்", "குளியலறை", "படுக்கையறை", "முன் வராண்டா"]}
        ]

        if (
            "ori_spatial_stim" not in st.session_state 
            or st.session_state.ori_spatial_stim is None 
            or st.session_state.ori_spatial_stim.get("lang") != lang
            or st.session_state.ori_spatial_stim.get("difficulty") != diff_str
        ):
            tasks = spatial_tasks_ta if lang == "ta" else spatial_tasks_en
            task = random.choice(tasks)
            raw_target = task["target"]
            target_with_icon = f"{ROOM_ICONS.get(raw_target, '🏠')} {raw_target}"
            
            num_choices = 2 if diff_str == "easy" else (3 if diff_str == "medium" else 4)
            distractor_opts = [o for o in task["options"] if o != raw_target]
            chosen_d = random.sample(distractor_opts, num_choices - 1)
            selected_raw = [raw_target] + chosen_d
            options_with_icons = [f"{ROOM_ICONS.get(o, '🏠')} {o}" for o in selected_raw]
            random.shuffle(options_with_icons)

            st.session_state.ori_spatial_stim = {
                "prompt": task["prompt"],
                "target": target_with_icon,
                "options": options_with_icons,
                "difficulty": diff_str,
                "lang": lang
            }
            st.session_state.ori_trial_start_time = time.time()
            st.session_state.ori_feedback = None

        stim = st.session_state.ori_spatial_stim

        st.components.v1.html(VoiceAssistant.get_speech_html(stim["prompt"], lang=lang), height=60)
        st.markdown(f"#### 🏠 {stim['prompt']}")

        st.markdown("<br>", unsafe_allow_html=True)

        opt_cols = st.columns(len(stim["options"]))
        distinct_visuals = resolve_distinct_option_visuals(stim["options"])
        for idx, (col, opt, (opt_img, opt_icon)) in enumerate(zip(opt_cols, stim["options"], distinct_visuals)):
            with col:
                with st.container(border=True):
                    if opt_img and os.path.exists(opt_img):
                        st.image(opt_img, use_container_width=True)
                    btn_key = f"spatial_btn_{idx}_{st.session_state.ori_current_trial}_{lang}"
                    btn_label = opt if any(opt.strip().startswith(c) for c in ["🍳", "🛏️", "🌺", "🚪", "🚿", "🍽️", "🛋️", opt_icon]) else f"{opt_icon} {opt}"
                    if st.button(btn_label, key=btn_key, use_container_width=True):
                        rt = round(time.time() - st.session_state.ori_trial_start_time, 2)
                        is_correct = (opt == stim["target"])

                        st.session_state.ori_trials.append({
                            "stimulus": "Spatial Orientation",
                            "target_response": stim["target"],
                            "user_response": opt,
                            "is_correct": is_correct,
                            "response_time_sec": rt,
                            "difficulty_level": diff_num
                        })

                        st.session_state.ori_feedback = {
                            "is_correct": is_correct,
                            "correct_answer": stim["target"],
                            "rt": rt
                        }
                        st.rerun()

        if st.session_state.ori_feedback:
            fb = st.session_state.ori_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'அற்புதம்! வீட்டு சூழலை சரியாக உணர்ந்துள்ளீர்கள்!' if lang == 'ta' else 'Spot on! Correct spatial awareness!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
            else:
                st.warning(f"💡 {'சரியான இடம்:' if lang == 'ta' else 'The correct room is:'} **{fb['correct_answer']}**.")

            if st.button("➡️ " + ("அடுத்த பயிற்சி" if lang == "ta" else "Next Location"), key="spatial_next_btn", use_container_width=True):
                st.session_state.ori_current_trial += 1
                st.session_state.ori_spatial_stim = None
                st.session_state.ori_feedback = None
                st.rerun()
