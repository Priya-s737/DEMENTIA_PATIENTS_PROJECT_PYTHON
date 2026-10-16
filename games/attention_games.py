"""
Attention & Executive Function Games:
1. Bilingual Stroop Interference Challenge (Selective Attention & Cognitive Inhibition)
2. Digital Trail Making Test (TMT-A / TMT-B Executive Switching)
Strictly localized with rich visual icons/emojis on all option buttons.
"""

import streamlit as st
import time
import random
from typing import Dict, Any
from modules.voice_assistant import VoiceAssistant
from modules.difficulty import render_difficulty_selector

COLOR_PALETTE = {
    "RED": {"hex": "#DC2626", "en": "Red", "ta": "சிகப்பு", "icon": "🔴"},
    "BLUE": {"hex": "#2563EB", "en": "Blue", "ta": "நீலம்", "icon": "🔵"},
    "GREEN": {"hex": "#16A34A", "en": "Green", "ta": "பச்சை", "icon": "🟢"},
    "YELLOW": {"hex": "#CA8A04", "en": "Yellow", "ta": "மஞ்சள்", "icon": "🟡"},
    "PURPLE": {"hex": "#9333EA", "en": "Purple", "ta": "ஊதா", "icon": "🟣"}
}

def render_attention_game(patient: Dict[str, Any], lang: str = "en"):
    st.markdown(f"### 🎯 {'கவனக்குவிப்பு & செயல் திறன்' if lang == 'ta' else 'Attention & Executive Function Challenge'}")

    if "att_game_sub" not in st.session_state:
        st.session_state.att_game_sub = "stroop"
    if "att_trials" not in st.session_state:
        st.session_state.att_trials = []
    if "att_current_trial" not in st.session_state:
        st.session_state.att_current_trial = 1
    if "att_trial_start_time" not in st.session_state:
        st.session_state.att_trial_start_time = time.time()
    if "att_feedback" not in st.session_state:
        st.session_state.att_feedback = None

    curr_lvl = patient.get("current_adaptive_level", 2)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎨 " + ("வண்ண-சொல் பயிற்சி" if lang == "ta" else "Color-Word Stroop Task"), use_container_width=True):
            st.session_state.att_game_sub = "stroop"
            st.session_state.att_stimulus = None
            st.session_state.att_feedback = None
            st.rerun()
    with col2:
        if st.button("🔢 " + ("வரிசை இணைப்புப் பயிற்சி" if lang == "ta" else "Trail Making Test"), use_container_width=True):
            st.session_state.att_game_sub = "tmt"
            st.session_state.tmt_state = None
            st.rerun()

    st.divider()

    # --- EASY / MEDIUM / HARD DIFFICULTY SELECTOR ---
    diff_str, diff_num = render_difficulty_selector("attention", lang=lang, default_lvl=curr_lvl)

    # --- SUB-GAME 1: STROOP INTERFERENCE TASK ---
    if st.session_state.att_game_sub == "stroop":
        if (
            "att_stimulus" not in st.session_state 
            or st.session_state.att_stimulus is None 
            or st.session_state.att_stimulus.get("lang") != lang
            or st.session_state.att_stimulus.get("difficulty") != diff_str
        ):
            color_keys = list(COLOR_PALETTE.keys())
            
            # Difficulty-specific Stroop configuration
            if diff_str == "easy":
                num_choices = 2
                is_incongruent = False  # 100% Congruent: word matches ink color
                prompt_text = (
                    "எழுத்தின் நிறத்தைத் தேர்ந்தெடுக்கவும்:"
                    if lang == "ta"
                    else "Identify the color of the text:"
                )
            elif diff_str == "medium":
                num_choices = 3
                is_incongruent = random.random() < 0.5  # 50% Incongruent
                prompt_text = (
                    "எழுத்தின் மை நிறத்தை மட்டும் தேர்வு செய்யவும்:"
                    if lang == "ta"
                    else "Identify the INK COLOR only:"
                )
            else:  # hard
                num_choices = 4
                is_incongruent = True  # 100% Incongruent high Stroop conflict
                prompt_text = (
                    "எழுத்தின் மை நிறத்தை மட்டும் தேர்வு செய்யவும். சொல்லைப் படிக்க வேண்டாம்!"
                    if lang == "ta"
                    else "Identify the INK COLOR only. Do not read the written word!"
                )
            
            word_color_key = random.choice(color_keys)
            if is_incongruent:
                other_color_keys = [k for k in color_keys if k != word_color_key]
                ink_color_key = random.choice(other_color_keys)
            else:
                ink_color_key = word_color_key

            word_text = COLOR_PALETTE[word_color_key]["ta" if lang == "ta" else "en"]
            ink_hex = COLOR_PALETTE[ink_color_key]["hex"]
            target_answer = f"{COLOR_PALETTE[ink_color_key]['icon']} {COLOR_PALETTE[ink_color_key]['ta' if lang == 'ta' else 'en']}"

            distractor_keys = [k for k in color_keys if k != ink_color_key]
            chosen_distractors = random.sample(distractor_keys, num_choices - 1)
            
            all_choice_keys = [ink_color_key] + chosen_distractors
            random.shuffle(all_choice_keys)

            options = []
            for k in all_choice_keys:
                options.append({
                    "key": k,
                    "hex": COLOR_PALETTE[k]["hex"],
                    "icon": COLOR_PALETTE[k]["icon"],
                    "label": COLOR_PALETTE[k]["ta" if lang == "ta" else "en"]
                })

            st.session_state.att_stimulus = {
                "word_text": word_text,
                "ink_hex": ink_hex,
                "target_key": ink_color_key,
                "target_answer": target_answer,
                "options": options,
                "prompt_text": prompt_text,
                "is_incongruent": is_incongruent,
                "difficulty": diff_str,
                "lang": lang
            }
            st.session_state.att_trial_start_time = time.time()
            st.session_state.att_feedback = None

        stim = st.session_state.att_stimulus

        st.components.v1.html(
            VoiceAssistant.get_speech_html(stim["prompt_text"], lang=lang),
            height=60
        )
        st.markdown(f"#### ⚠️ {stim['prompt_text']}")

        st.markdown(
            f"""
            <div style="background-color: #1E293B; border-radius: 16px; padding: 35px; text-align: center; margin: 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                <span style="font-size: 56px; font-weight: 900; color: {stim['ink_hex']}; letter-spacing: 4px;">
                    {stim['word_text']}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        opt_cols = st.columns(len(stim["options"]))
        for idx, (col, opt_data) in enumerate(zip(opt_cols, stim["options"])):
            with col:
                opt_hex = opt_data.get("hex", "#2563EB")
                opt_icon = opt_data.get("icon", "🎨")
                opt_label = opt_data.get("label", "")
                
                # Visual Color Disc Card for illiterate / dementia seniors
                st.markdown(
                    f"""
                    <div style="background: white; border-radius: 16px; padding: 15px 10px; text-align: center; 
                                box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 2px solid #E2E8F0; margin-bottom: 8px;">
                        <div style="background-color: {opt_hex}; width: 80px; height: 80px; border-radius: 50%; 
                                    margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.2); border: 3px solid white;">
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                btn_key = f"stroop_btn_{idx}_{stim['word_text']}_{st.session_state.att_current_trial}_{lang}"
                if st.button(f"{opt_icon} {opt_label}", key=btn_key, use_container_width=True):
                    rt = round(time.time() - st.session_state.att_trial_start_time, 2)
                    is_correct = (opt_data["key"] == stim["target_key"])

                    st.session_state.att_trials.append({
                        "stimulus": f"Stroop({stim['word_text']}|{stim['target_answer']})",
                        "target_response": stim["target_answer"],
                        "user_response": opt_label,
                        "is_correct": is_correct,
                        "response_time_sec": rt,
                        "difficulty_level": diff_num
                    })

                    st.session_state.att_feedback = {
                        "is_correct": is_correct,
                        "correct_answer": stim["target_answer"],
                        "rt": rt
                    }
                    st.rerun()

        if st.session_state.att_feedback:
            fb = st.session_state.att_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'மிக அற்புதம்! மை நிறத்தை சரியாகக் கண்டறிந்தீர்கள்!' if lang == 'ta' else 'Fantastic! Perfect cognitive response!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
            else:
                st.warning(f"💡 {'சரியான மை நிறம்:' if lang == 'ta' else 'The ink color was:'} **{fb['correct_answer']}**.")

            if st.button("➡️ " + ("அடுத்த பயிற்சி" if lang == "ta" else "Next Trial"), key="stroop_next_btn", use_container_width=True):
                st.session_state.att_current_trial += 1
                st.session_state.att_stimulus = None
                st.session_state.att_feedback = None
                st.rerun()

    # --- SUB-GAME 2: DIGITAL TRAIL MAKING TEST (TMT) ---
    elif st.session_state.att_game_sub == "tmt":
        if (
            "tmt_state" not in st.session_state 
            or st.session_state.tmt_state is None 
            or st.session_state.tmt_state.get("lang") != lang
            or st.session_state.tmt_state.get("difficulty") != diff_str
        ):
            if diff_str == "easy":
                seq = ["1️⃣", "2️⃣", "3️⃣"]
            elif diff_str == "medium":
                seq = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            else:
                seq = ["1️⃣", "🅰️", "2️⃣", "🅱️", "3️⃣", "🅲"]

            shuffled_grid = list(seq)
            random.shuffle(shuffled_grid)

            st.session_state.tmt_state = {
                "target_sequence": seq,
                "current_step_index": 0,
                "shuffled_grid": shuffled_grid,
                "completed_steps": [],
                "errors": 0,
                "start_time": time.time(),
                "is_finished": False,
                "difficulty": diff_str,
                "lang": lang
            }

        tmt = st.session_state.tmt_state
        prompt_tmt = (
            f"வரிசையாகக் கிளிக் செய்யவும்: {' ➜ '.join(tmt['target_sequence'])}"
            if lang == "ta"
            else f"Connect the trail in sequence: {' ➜ '.join(tmt['target_sequence'])}"
        )

        st.components.v1.html(VoiceAssistant.get_speech_html(prompt_tmt, lang=lang), height=60)
        st.markdown(f"#### 🔗 {prompt_tmt}")

        if not tmt["is_finished"]:
            expected_item = tmt["target_sequence"][tmt["current_step_index"]]
            st.info(f"👉 {'அடுத்து தொடவேண்டியது:' if lang == 'ta' else 'Next item to press:'} **{expected_item}** | {'பிழைகள்:' if lang == 'ta' else 'Errors:'} {tmt['errors']}")

            grid_cols = st.columns(3)
            for idx, item in enumerate(tmt["shuffled_grid"]):
                c = grid_cols[idx % 3]
                with c:
                    is_already_done = item in tmt["completed_steps"]
                    btn_text = f"✅ {item}" if is_already_done else f"{item}"
                    if st.button(btn_text, key=f"tmt_btn_{item}_{idx}_{lang}", disabled=is_already_done, use_container_width=True):
                        if item == expected_item:
                            tmt["completed_steps"].append(item)
                            tmt["current_step_index"] += 1
                            if tmt["current_step_index"] == len(tmt["target_sequence"]):
                                tmt["is_finished"] = True
                                total_time = round(time.time() - tmt["start_time"], 2)
                                st.session_state.att_trials.append({
                                    "stimulus": f"TMT({''.join(tmt['target_sequence'])})",
                                    "target_response": "COMPLETE",
                                    "user_response": f"Errors:{tmt['errors']}",
                                    "is_correct": (tmt["errors"] <= 1),
                                    "response_time_sec": total_time,
                                    "difficulty_level": diff_num
                                })
                        else:
                            tmt["errors"] += 1
                            st.toast(f"⚠️ {'தவறான தேர்வு! அடுத்து வேண்டியது:' if lang == 'ta' else 'Oops! Next target is:'} {expected_item}")
                        st.rerun()
        else:
            total_time = round(time.time() - tmt["start_time"], 2)
            st.success(f"🎉 {'வாழ்த்துகள்! பாதையை வெற்றிகரமாக முடித்துவிட்டீர்கள்!' if lang == 'ta' else 'Trail Completed Successfully!'} ⏱️ {total_time}{'வி' if lang == 'ta' else 's'} | {'பிழைகள்:' if lang == 'ta' else 'Errors:'} {tmt['errors']}")
            if st.button("🔄 " + ("மீண்டும் பயிற்சி செய்ய" if lang == "ta" else "Start New Trail"), key=f"tmt_restart_{lang}", use_container_width=True):
                st.session_state.tmt_state = None
                st.rerun()
