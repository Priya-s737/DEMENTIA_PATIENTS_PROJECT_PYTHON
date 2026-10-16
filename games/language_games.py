"""
Language & Semantic Recognition Cognitive Domain Games:
1. Daily Object Naming & Multi-lingual Visual Cues
2. Category Fluency & Semantic Association (Fruits, Musical Instruments, Vehicles, Utensils)
Strictly localized with rich visual icons/emojis on all option buttons.
"""

import streamlit as st
import time
import os
import random
from typing import Dict, Any
from modules.voice_assistant import VoiceAssistant
from modules.visual_assets import resolve_option_visual, resolve_distinct_option_visuals
from modules.difficulty import render_difficulty_selector

OBJECT_ITEMS = [
    {
        "en": "Reading Glasses",
        "ta": "மூக்குக் கண்ணாடி",
        "icon": "👓",
        "category_en": "Personal Accessory",
        "category_ta": "பயன்பாட்டுப் பொருள்",
        "image_file": "spectacles.jpg"
    },
    {
        "en": "Coffee Tumbler",
        "ta": "பித்தளை காபி டம்ளர்",
        "icon": "☕",
        "category_en": "Kitchen Utensil",
        "category_ta": "சமையலறைப் பாத்திரம்",
        "image_file": "coffee.jpg"
    },
    {
        "en": "Flute",
        "ta": "புல்லாங்குழல்",
        "icon": "🪈",
        "category_en": "Musical Instrument",
        "category_ta": "இசைக் கருவி",
        "image_file": "flute.jpg"
    },
    {
        "en": "Umbrella",
        "ta": "குடை",
        "icon": "☂️",
        "category_en": "Daily Utility",
        "category_ta": "பயன்பாட்டுப் பொருள்",
        "image_file": "umbrella.jpg"
    },
    {
        "en": "Wall Clock",
        "ta": "சுவர்க் கடிகாரம்",
        "icon": "🕰️",
        "category_en": "Timepiece",
        "category_ta": "நேரம் காட்டும் சாதனம்",
        "image_file": "clock.jpg"
    },
    {
        "en": "Toothbrush",
        "ta": "பல் துலக்கும் பிரஷ்",
        "icon": "🪥",
        "category_en": "Daily Utility",
        "category_ta": "தினசரி பயன்பாடு",
        "image_file": "toothbrush.jpg"
    },
    {
        "en": "Book",
        "ta": "புத்தகம்",
        "icon": "📖",
        "category_en": "Reading",
        "category_ta": "வாசிப்புப் பொருள்",
        "image_file": "book.jpg"
    },
    {
        "en": "Keyring",
        "ta": "சாவிக்கொத்து",
        "icon": "🔑",
        "category_en": "Security",
        "category_ta": "பாதுகாப்புப் பொருள்",
        "image_file": "keyring.jpg"
    }
]

CATEGORY_ITEMS_ICONS = {
    "Flute": "🪈", "புல்லாங்குழல்": "🪈",
    "Umbrella": "☂️", "குடை": "☂️",
    "Wristwatch": "⌚", "கைக்கடிகாரம்": "⌚",
    "Spectacles": "👓", "மூக்குக்கண்ணாடி": "👓",
    "Book": "📖", "புத்தகம்": "📖",
    "Frying Pan": "🍳", "வாணலி": "🍳",
    "Garden Tool": "🪴", "தோட்டக்கருவி": "🪴",
    "Keyring": "🔑", "சாவிக்கொத்து": "🔑",
    "Idli & Sambar": "🍲", "இட்லி & சாம்பார்": "🍲",
    "Sandwich": "🥪", "சாண்ட்விச்": "🥪",
    "Pizza": "🍕", "பீட்சா": "🍕",
    "Salad": "🥗", "சூப்": "🥣",
    "Train": "🚆", "ரயில்": "🚆",
    "Mango": "🥭", "மாம்பழம்": "🥭",
    "Rose Flower": "🌹", "ரோஜா மலர்": "🌹",
    "Wooden Chair": "🪑", "மர நாற்காலி": "🪑",
    "Cooking Pot": "🍲", "சமையல் பாத்திரம்": "🍲",
    "Apple": "🍎", "ஆப்பிள்": "🍎",
    "Toothbrush": "🪥", "பல் துலக்கும் பிரஷ்": "🪥",
    "Paint Brush": "🖌️", "ஓவிய தூரிகை": "🖌️",
    "Wall Clock": "🕰️", "கடிகாரம்": "🕰️"
}

def render_language_game(patient: Dict[str, Any], lang: str = "en"):
    st.markdown(f"### 🗣️ {'மொழி மற்றும் பொருள் அறிதல்' if lang == 'ta' else 'Language & Semantic Naming Challenge'}")

    if "lang_game_sub" not in st.session_state:
        st.session_state.lang_game_sub = "naming"
    if "lang_trials" not in st.session_state:
        st.session_state.lang_trials = []
    if "lang_current_trial" not in st.session_state:
        st.session_state.lang_current_trial = 1
    if "lang_trial_start_time" not in st.session_state:
        st.session_state.lang_trial_start_time = time.time()
    if "lang_feedback" not in st.session_state:
        st.session_state.lang_feedback = None

    curr_lvl = patient.get("current_adaptive_level", 2)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🏷️ " + ("பொருள் பெயர் அறிதல்" if lang == "ta" else "Object Naming Task"), use_container_width=True):
            st.session_state.lang_game_sub = "naming"
            st.session_state.lang_stimulus = None
            st.session_state.lang_feedback = None
            st.rerun()
    with col2:
        if st.button("🧩 " + ("வகைப்பாடு அடையாளம் காணுதல்" if lang == "ta" else "Category Semantic Match"), use_container_width=True):
            st.session_state.lang_game_sub = "category"
            st.session_state.lang_cat_stim = None
            st.session_state.lang_feedback = None
            st.rerun()

    st.divider()

    # --- EASY / MEDIUM / HARD DIFFICULTY SELECTOR ---
    diff_str, diff_num = render_difficulty_selector("language", lang=lang, default_lvl=curr_lvl)

    # --- SUB-GAME 1: OBJECT NAMING ---
    if st.session_state.lang_game_sub == "naming":
        if (
            "lang_stimulus" not in st.session_state 
            or st.session_state.lang_stimulus is None 
            or st.session_state.lang_stimulus.get("lang") != lang
            or st.session_state.lang_stimulus.get("difficulty") != diff_str
        ):
            target = random.choice(OBJECT_ITEMS)
            raw_target_name = target["ta"] if lang == "ta" else target["en"]
            target_name = raw_target_name
            cue = target.get("cue_ta", target.get("category_ta", "")) if lang == "ta" else target.get("cue_en", target.get("category_en", ""))

            all_names = [o["ta"] if lang == "ta" else o["en"] for o in OBJECT_ITEMS]
            num_choices = 2 if diff_str == "easy" else (3 if diff_str == "medium" else 4)
            distractors = [n for n in all_names if n != target_name]
            chosen_d = random.sample(distractors, num_choices - 1)
            options = [target_name] + chosen_d
            random.shuffle(options)

            prompt = (
                "படத்தைப் பார்த்து இந்தப் பொருளின் பெயரைத் தேர்ந்தெடுக்கவும்:"
                if lang == "ta"
                else "Look at the picture and identify the object:"
            )

            img_file = target.get("image_file", "spectacles.jpg")
            local_q_img = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "visual_cards", img_file)

            st.session_state.lang_stimulus = {
                "prompt": prompt,
                "target": target_name,
                "options": options,
                "image_file": local_q_img,
                "cue": cue,
                "difficulty": diff_str,
                "lang": lang
            }
            st.session_state.lang_trial_start_time = time.time()
            st.session_state.lang_feedback = None

        stim = st.session_state.lang_stimulus

        st.components.v1.html(VoiceAssistant.get_speech_html(stim["prompt"], lang=lang), height=60)
        st.markdown(f"#### {stim['prompt']}")

        # Resolve reliable local photo for the question object
        q_img, _ = resolve_option_visual(stim["target"])
        if not q_img or not os.path.exists(q_img):
            q_img = stim.get("image_url", "")

        col_l, col_center, col_r = st.columns([1, 2, 1])
        with col_center:
            st.markdown(
                f"""
                <div style="background: #1E293B; border-radius: 16px; padding: 10px; border: 3px solid #3B82F6; box-shadow: 0 8px 24px rgba(0,0,0,0.3); text-align: center; margin-bottom: 12px;">
                    <span style="font-size: 15px; font-weight: bold; color: #93C5FD;">
                        🔍 {'அடையாளம் காண வேண்டிய பொருள்' if lang == 'ta' else 'Object to Identify'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if q_img:
                st.image(q_img, use_container_width=True)

        if diff_str == "easy" and stim.get("cue"):
            st.info(f"💡 {'குறிப்பு:' if lang == 'ta' else 'Helpful Clue:'} **{stim['cue']}**")

        st.markdown("<br>", unsafe_allow_html=True)

        opt_cols = st.columns(len(stim["options"]))
        distinct_visuals = resolve_distinct_option_visuals(stim["options"])
        for idx, (col, opt, (opt_img, opt_icon)) in enumerate(zip(opt_cols, stim["options"], distinct_visuals)):
            with col:
                with st.container(border=True):
                    if opt_img and os.path.exists(opt_img):
                        st.image(opt_img, use_container_width=True)
                    btn_key = f"obj_name_{idx}_{st.session_state.lang_current_trial}_{lang}"
                    btn_label = f"{opt_icon} {opt}"
                    if st.button(btn_label, key=btn_key, use_container_width=True):
                        rt = round(time.time() - st.session_state.lang_trial_start_time, 2)
                        is_correct = (opt == stim["target"])

                        st.session_state.lang_trials.append({
                            "stimulus": stim["target"],
                            "target_response": stim["target"],
                            "user_response": opt,
                            "is_correct": is_correct,
                            "response_time_sec": rt,
                            "difficulty_level": diff_num
                        })

                        st.session_state.lang_feedback = {
                            "is_correct": is_correct,
                            "correct_answer": stim["target"],
                            "rt": rt
                        }
                        st.rerun()

        if st.session_state.lang_feedback:
            fb = st.session_state.lang_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'மிக அற்புதம்! சரியான பொருள் பெயர்!' if lang == 'ta' else 'Excellent! Accurate semantic naming!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
            else:
                st.warning(f"💡 {'சரியான பொருள்:' if lang == 'ta' else 'The correct object is:'} **{fb['correct_answer']}**.")

            if st.button("➡️ " + ("அடுத்த பொருள்" if lang == "ta" else "Next Object"), key="lang_next_btn", use_container_width=True):
                st.session_state.lang_current_trial += 1
                st.session_state.lang_stimulus = None
                st.session_state.lang_feedback = None
                st.rerun()

    # --- SUB-GAME 2: CATEGORY FLUENCY ---
    elif st.session_state.lang_game_sub == "category":
        category_tasks_en = [
            {"prompt": "Which of these items is a 'Musical Instrument'?", "target": "Flute", "options": ["Flute", "Umbrella", "Wristwatch", "Spectacles"]},
            {"prompt": "Which of these is used for 'Reading and Studying'?", "target": "Book", "options": ["Book", "Frying Pan", "Garden Tool", "Keyring"]},
            {"prompt": "Which of these is a traditional South Indian 'Breakfast Dish'?", "target": "Idli & Sambar", "options": ["Idli & Sambar", "Sandwich", "Pizza", "Salad"]},
            {"prompt": "Which of these is a 'Public Transport Vehicle' for long travel?", "target": "Train", "options": ["Train", "Apple", "Book", "Spectacles"]},
            {"prompt": "Which of these is a delicious sweet 'Tropical Fruit'?", "target": "Mango", "options": ["Mango", "Flute", "Keyring", "Wall Clock"]},
            {"prompt": "Which of these is a fragrant beautiful 'Flower'?", "target": "Rose Flower", "options": ["Rose Flower", "Umbrella", "Toothbrush", "Train"]},
            {"prompt": "Which of these is a piece of 'Household Furniture' to sit on?", "target": "Wooden Chair", "options": ["Wooden Chair", "Idli & Sambar", "Book", "Spectacles"]}
        ]
        category_tasks_ta = [
            {"prompt": "இவற்றுள் எது 'இசைக் கருவி' ஆகும்?", "target": "புல்லாங்குழல்", "options": ["புல்லாங்குழல்", "குடை", "கைக்கடிகாரம்", "மூக்குக்கண்ணாடி"]},
            {"prompt": "இவற்றுள் எது 'படிப்பிற்கும் வாசிப்பிற்கும்' பயன்படும்?", "target": "புத்தகம்", "options": ["புத்தகம்", "வாணலி", "தோட்டக்கருவி", "சாவிக்கொத்து"]},
            {"prompt": "இவற்றுள் எது பாரம்பரிய 'காலை உணவு' ஆகும்?", "target": "இட்லி & சாம்பார்", "options": ["இட்லி & சாம்பார்", "சாண்ட்விச்", "பீட்சா", "சூப்"]},
            {"prompt": "இவற்றுள் எது நெடுந்தூரப் பயணத்திற்கு உதவும் 'வாகனம்'?", "target": "ரயில்", "options": ["ரயில்", "ஆப்பிள்", "புத்தகம்", "மூக்குக்கண்ணாடி"]},
            {"prompt": "இவற்றுள் எது இனிப்பான சுவையான 'பழம்'?", "target": "மாம்பழம்", "options": ["மாம்பழம்", "புல்லாங்குழல்", "சாவிக்கொத்து", "கடிகாரம்"]},
            {"prompt": "இவற்றுள் எது நறுமணம் மிக்க அழகிய 'மலர்'?", "target": "ரோஜா மலர்", "options": ["ரோஜா மலர்", "குடை", "பல் துலக்கும் பிரஷ்", "ரயில்"]},
            {"prompt": "இவற்றுள் எது நாம் அமர்வதற்குப் பயன்படும் 'மர சாமான்கள்'?", "target": "மர நாற்காலி", "options": ["மர நாற்காலி", "இட்லி & சாம்பார்", "புத்தகம்", "மூக்குக்கண்ணாடி"]}
        ]

        if (
            "lang_cat_stim" not in st.session_state 
            or st.session_state.lang_cat_stim is None 
            or st.session_state.lang_cat_stim.get("lang") != lang
            or st.session_state.lang_cat_stim.get("difficulty") != diff_str
        ):
            tasks = category_tasks_ta if lang == "ta" else category_tasks_en
            task = random.choice(tasks)
            raw_target = task["target"]
            target_with_icon = f"{CATEGORY_ITEMS_ICONS.get(raw_target, '✨')} {raw_target}"
            
            num_choices = 2 if diff_str == "easy" else (3 if diff_str == "medium" else 4)
            distractor_opts = [o for o in task["options"] if o != raw_target]
            chosen_d = random.sample(distractor_opts, num_choices - 1)
            selected_raw = [raw_target] + chosen_d
            options_with_icons = [f"{CATEGORY_ITEMS_ICONS.get(o, '✨')} {o}" for o in selected_raw]
            random.shuffle(options_with_icons)

            st.session_state.lang_cat_stim = {
                "prompt": task["prompt"],
                "target": target_with_icon,
                "options": options_with_icons,
                "difficulty": diff_str,
                "lang": lang
            }
            st.session_state.lang_trial_start_time = time.time()
            st.session_state.lang_feedback = None

        stim = st.session_state.lang_cat_stim

        st.components.v1.html(VoiceAssistant.get_speech_html(stim["prompt"], lang=lang), height=60)
        st.markdown(f"#### 🔍 {stim['prompt']}")

        st.markdown("<br>", unsafe_allow_html=True)

        opt_cols = st.columns(len(stim["options"]))
        distinct_visuals = resolve_distinct_option_visuals(stim["options"])
        for idx, (col, opt, (opt_img, opt_icon)) in enumerate(zip(opt_cols, stim["options"], distinct_visuals)):
            with col:
                with st.container(border=True):
                    if opt_img and os.path.exists(opt_img):
                        st.image(opt_img, use_container_width=True)
                    btn_key = f"cat_btn_{idx}_{st.session_state.lang_current_trial}_{lang}"
                    btn_label = f"{opt_icon} {opt}"
                    if st.button(btn_label, key=btn_key, use_container_width=True):
                        rt = round(time.time() - st.session_state.lang_trial_start_time, 2)
                        is_correct = (opt == stim["target"])

                        st.session_state.lang_trials.append({
                            "stimulus": "Category Fluency",
                            "target_response": stim["target"],
                            "user_response": opt,
                            "is_correct": is_correct,
                            "response_time_sec": rt,
                            "difficulty_level": diff_num
                        })

                        st.session_state.lang_feedback = {
                            "is_correct": is_correct,
                            "correct_answer": stim["target"],
                            "rt": rt
                        }
                        st.rerun()

        if st.session_state.lang_feedback:
            fb = st.session_state.lang_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'சரியான தேர்வு!' if lang == 'ta' else 'Spot-on category categorization!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
            else:
                st.warning(f"💡 {'சரியான விடை:' if lang == 'ta' else 'The matching item is:'} **{fb['correct_answer']}**.")

            if st.button("➡️ " + ("அடுத்த வகைப்பாடு" if lang == "ta" else "Next Category"), key="cat_next_btn", use_container_width=True):
                st.session_state.lang_current_trial += 1
                st.session_state.lang_cat_stim = None
                st.session_state.lang_feedback = None
                st.rerun()
