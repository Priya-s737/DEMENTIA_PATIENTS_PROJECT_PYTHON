"""
Memory Cognitive Domain Games:
1. Familiar Photo & Memory Recall (Reminiscence Therapy with ALL Caregiver-Uploaded Photos & Visual Option Cards)
2. Daily Routine & Life Event Timeline Sequencing
Strictly localized for 100% Pure Tamil and 100% Pure English modes without mixed language.
"""

import streamlit as st
import time
import os
from typing import Dict, Any, List
from modules.personalization import PersonalizationEngine
from modules.voice_assistant import VoiceAssistant
from modules.visual_assets import resolve_option_visual, resolve_distinct_option_visuals
from modules.difficulty import render_difficulty_selector
from modules.celebration import render_celebration

FAMILY_ITEM_VISUALS = {
    # Relatives & People
    "மீனாட்சி": {"icon": "👩‍⚕️", "img": "uploads/visual_cards/doctor.jpg"},
    "Meenakshi": {"icon": "👩‍⚕️", "img": "uploads/visual_cards/doctor.jpg"},
    "சுந்தரம்": {"icon": "👨‍🦳", "img": "uploads/visual_cards/father.jpg"},
    "Sundaram": {"icon": "👨‍🦳", "img": "uploads/visual_cards/father.jpg"},
    "ராம்": {"icon": "👨‍🦱", "img": "uploads/visual_cards/husband.jpg"},
    "Ram": {"icon": "👨‍🦱", "img": "uploads/visual_cards/husband.jpg"},
    "பிரியா": {"icon": "👧", "img": "uploads/visual_cards/daughter.jpg"},
    "Priya": {"icon": "👧", "img": "uploads/visual_cards/daughter.jpg"},
    "கார்த்திக்": {"icon": "👦", "img": "uploads/visual_cards/son.jpg"},
    "Karthik": {"icon": "👦", "img": "uploads/visual_cards/son.jpg"},
    "அனு": {"icon": "👩", "img": "uploads/visual_cards/granddaughter.jpg"},
    "Anu": {"icon": "👩", "img": "uploads/visual_cards/granddaughter.jpg"},
    "மருத்துவர்": {"icon": "👨‍⚕️", "img": "uploads/visual_cards/doctor.jpg"},
    "Doctor": {"icon": "👨‍⚕️", "img": "uploads/visual_cards/doctor.jpg"},
    "செவிலியர்": {"icon": "👩‍⚕️", "img": "uploads/visual_cards/nurse.jpg"},
    "Nurse": {"icon": "👩‍⚕️", "img": "uploads/visual_cards/nurse.jpg"},
    
    # Items, Possessions & Locations
    "மூக்குக் கண்ணாடி": {"icon": "👓", "img": "uploads/visual_cards/spectacles.jpg"},
    "Reading Glasses": {"icon": "👓", "img": "uploads/visual_cards/spectacles.jpg"},
    "தங்கக் கடிகாரம்": {"icon": "⌚", "img": "uploads/visual_cards/wristwatch.jpg"},
    "Gold Watch": {"icon": "⌚", "img": "uploads/visual_cards/wristwatch.jpg"},
    "பித்தளை விளக்கு": {"icon": "🪔", "img": "uploads/visual_cards/brass_lamp.jpg"},
    "Brass Lamp": {"icon": "🪔", "img": "uploads/visual_cards/brass_lamp.jpg"},
    "முன் வராண்டா": {"icon": "🏡", "img": "uploads/visual_cards/front_porch.jpg"},
    "Front Porch": {"icon": "🏡", "img": "uploads/visual_cards/front_porch.jpg"},
    "பூஜை அறை": {"icon": "🪔", "img": "uploads/visual_cards/prayer_room.jpg"},
    "Prayer Room": {"icon": "🪔", "img": "uploads/visual_cards/prayer_room.jpg"},
    "காலை நடை": {"icon": "🚶‍♂️", "img": "uploads/visual_cards/morning_walk.jpg"},
    "Morning Walk": {"icon": "🚶‍♂️", "img": "uploads/visual_cards/morning_walk.jpg"},
    "செய்தித்தாள் வாசிப்பு": {"icon": "📰", "img": "uploads/visual_cards/newspaper.jpg"},
    "Reading Newspaper": {"icon": "📰", "img": "uploads/visual_cards/newspaper.jpg"}
}

def render_memory_game(patient: Dict[str, Any], personalization: PersonalizationEngine, lang: str = "en"):
    st.markdown(f"### 🧠 {'நினைவாற்றல் பயிற்சி' if lang == 'ta' else 'Episodic & Working Memory Challenge'}")
    
    if "mem_game_sub" not in st.session_state:
        st.session_state.mem_game_sub = "face_recall"
    if "mem_trials" not in st.session_state:
        st.session_state.mem_trials = []
    if "mem_seen_ids" not in st.session_state:
        st.session_state.mem_seen_ids = []
    if "mem_current_trial" not in st.session_state:
        st.session_state.mem_current_trial = 1
    if "mem_trial_start_time" not in st.session_state:
        st.session_state.mem_trial_start_time = time.time()
    if "mem_feedback" not in st.session_state:
        st.session_state.mem_feedback = None

    curr_lvl = patient.get("current_adaptive_level", 2)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🖼️ " + ("நினைவுப் புகைப்படம் அறிதல்" if lang == "ta" else "Photo & Memory Recall"), use_container_width=True):
            st.session_state.mem_game_sub = "face_recall"
            st.session_state.mem_stimulus = None
            st.session_state.mem_feedback = None
            st.rerun()
    with col2:
        if st.button("⏳ " + ("நிகழ்வு கால வரிசை" if lang == "ta" else "Life Timeline Sequencing"), use_container_width=True):
            st.session_state.mem_game_sub = "timeline"
            st.session_state.mem_stimulus = None
            st.session_state.mem_feedback = None
            st.rerun()

    st.divider()

    # --- EASY / MEDIUM / HARD DIFFICULTY SELECTOR ---
    diff_str, diff_num = render_difficulty_selector("memory", lang=lang, default_lvl=curr_lvl)

    # --- SUB-GAME 1: FAMILIAR PHOTO RECALL ---
    if st.session_state.mem_game_sub == "face_recall":
        if (
            "mem_stimulus" not in st.session_state 
            or st.session_state.mem_stimulus is None 
            or st.session_state.mem_stimulus.get("lang") != lang
            or st.session_state.mem_stimulus.get("difficulty") != diff_str
        ):
            st.session_state.mem_stimulus = personalization.get_face_recall_stimuli(
                patient_id=patient["id"],
                difficulty_level=diff_str,
                lang=lang,
                exclude_ids=st.session_state.mem_seen_ids
            )
            st.session_state.mem_stimulus["lang"] = lang
            st.session_state.mem_stimulus["difficulty"] = diff_str
            if st.session_state.mem_stimulus.get("memory_id"):
                st.session_state.mem_seen_ids.append(st.session_state.mem_stimulus["memory_id"])
            
            st.session_state.mem_trial_start_time = time.time()
            st.session_state.mem_feedback = None

        stim = st.session_state.mem_stimulus

        # If no photos were uploaded by caregiver, DO NOT show questions or option choices
        if not stim.get("has_photos", False):
            st.warning(
                "⚠️ **" + (
                    "புகைப்படங்கள் எதுவும் இன்னும் பதிவேற்றப்படவில்லை!**" if lang == "ta" else "No Personal Photos Uploaded Yet!**"
                )
            )
            st.info(
                "💡 " + (
                    "இந்தப் பயிற்சியை விளையாட, பராமரிப்பாளர் பிரிவில் (Caregiver Portal) உங்கள் குடும்பத்தினர், உறவினர்கள் அல்லது விருப்பமான இடங்களின் புகைப்படங்களைப் பதிவேற்றவும்."
                    if lang == "ta"
                    else "To play this reminiscence memory game, please go to the Caregiver Portal and upload personal family photos and memorable places."
                )
            )
            return

        st.components.v1.html(
            VoiceAssistant.get_speech_html(stim["prompt"], lang=lang),
            height=60
        )

        st.markdown(f"#### 🖼️ {stim['prompt']}")
        
        # Display main stimulus photo prominently
        img_path = stim.get("image_path", "")
        valid_path = None
        if img_path:
            norm_p = os.path.normpath(img_path)
            if os.path.exists(norm_p):
                valid_path = norm_p
            elif os.path.exists(os.path.join(os.getcwd(), norm_p)):
                valid_path = os.path.join(os.getcwd(), norm_p)

        # Fallback if valid_path not found
        if not valid_path and stim.get("target"):
            fallback_img, _ = resolve_option_visual(stim["target"])
            if fallback_img and os.path.exists(fallback_img):
                valid_path = fallback_img

        # Large prominent centered question photo frame
        if valid_path:
            col_l, col_center, col_r = st.columns([1, 2, 1])
            with col_center:
                st.markdown(
                    f"""
                    <div style="background: #1E293B; border-radius: 16px; padding: 10px; border: 3px solid #3B82F6; box-shadow: 0 8px 24px rgba(0,0,0,0.3); text-align: center; margin-bottom: 12px;">
                        <span style="font-size: 15px; font-weight: bold; color: #93C5FD;">
                            📸 {'கேள்விப் புகைப்படம்' if lang == 'ta' else 'Target Question Photo'}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.image(valid_path, use_container_width=True, caption="பதிவேற்றப்பட்ட குடும்ப நினைவு" if lang == "ta" else "Caregiver-Uploaded Family Memory")

        if diff_str == "easy" and stim.get("relation_cue"):
            st.info(f"💡 {'குறிப்பு:' if lang == 'ta' else 'Helpful Clue:'} **{stim['relation_cue']}**")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Render visual cards for every option strictly ensuring NO image repetition
        patient_mems = personalization.db.get_patient_memories(patient["id"])
        num_opts = len(stim["options"])
        opt_cols = st.columns(num_opts)
        distinct_visuals = resolve_distinct_option_visuals(stim["options"], patient_mems)

        for idx, (col, opt, (opt_img, opt_icon)) in enumerate(zip(opt_cols, stim["options"], distinct_visuals)):
            with col:
                with st.container(border=True):
                    # Senior visual card: prominent image
                    if opt_img and os.path.exists(opt_img):
                        st.image(opt_img, use_container_width=True)
                    
                    btn_key = f"mem_opt_{idx}_{stim['target']}_{st.session_state.mem_current_trial}_{lang}"
                    btn_label = opt if any(opt.strip().startswith(c) for c in [opt_icon, "👩‍🦳", "👨‍🦳", "👧", "👦", "👵", "👴", "🐕", "🏛️", "🛕", "🌳", "🖌️", "🪥", "☕", "🪈", "👓", "☂️", "🕰️", "📖", "🔑", "⌚", "🍳", "🪴", "🪔", "🍲", "🥪", "🍕", "🥗", "🥣", "🚆", "🥭", "🌹", "🪑", "🍎"]) else f"{opt_icon} {opt}"
                    if st.button(btn_label, key=btn_key, use_container_width=True):
                        rt = round(time.time() - st.session_state.mem_trial_start_time, 2)
                        is_correct = (opt == stim["target"])
                        
                        st.session_state.mem_trials.append({
                            "stimulus": stim["target"],
                            "target_response": stim["target"],
                            "user_response": opt,
                            "is_correct": is_correct,
                            "response_time_sec": rt,
                            "difficulty_level": diff_num
                        })
                        
                        st.session_state.mem_feedback = {
                            "is_correct": is_correct,
                            "correct_answer": stim["target"],
                            "rt": rt
                        }
                        st.rerun()

        if st.session_state.mem_feedback:
            fb = st.session_state.mem_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'மிக சிறப்பு! சரியான பதில்!' if lang == 'ta' else 'Brilliant! That is correct!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
                def on_next_trial():
                    st.session_state.mem_current_trial += 1
                    st.session_state.mem_stimulus = None
                    st.session_state.mem_feedback = None
                    st.rerun()
                render_celebration(lang=lang, on_continue=on_next_trial)
            else:
                st.warning(f"💡 {'சரியான விடை:' if lang == 'ta' else 'The correct answer was:'} **{fb['correct_answer']}**.")
                if st.button("➡️ " + ("அடுத்த கேள்வி" if lang == "ta" else "Next Question"), key="mem_next_btn", use_container_width=True, type="primary"):
                    st.session_state.mem_current_trial += 1
                    st.session_state.mem_stimulus = None
                    st.session_state.mem_feedback = None
                    st.rerun()

    # --- SUB-GAME 2: TIMELINE SEQUENCING ---
    elif st.session_state.mem_game_sub == "timeline":
        if (
            "mem_stimulus" not in st.session_state 
            or st.session_state.mem_stimulus is None 
            or st.session_state.mem_stimulus.get("lang") != lang
            or st.session_state.mem_stimulus.get("difficulty") != diff_str
        ):
            st.session_state.mem_stimulus = personalization.get_timeline_sequencing_stimuli(
                patient_id=patient["id"],
                difficulty_level=diff_str,
                lang=lang
            )
            st.session_state.mem_stimulus["lang"] = lang
            st.session_state.mem_stimulus["difficulty"] = diff_str
            st.session_state.mem_trial_start_time = time.time()
            st.session_state.mem_feedback = None

        stim = st.session_state.mem_stimulus

        st.components.v1.html(
            VoiceAssistant.get_speech_html(stim["prompt"], lang=lang),
            height=60
        )
        st.markdown(f"#### ⏳ {stim['prompt']}")

        correct_seq = stim["correct_sequence"]
        scrambled = stim["scrambled_steps"]

        st.info("💡 " + ("கீழே உள்ள படக் குறிப்புகளுக்கு 1, 2, 3 என வரிசை எண்களை இடவும்:" if lang == "ta" else "Assign chronological numbers (1, 2, 3...) to order these routine events:"))

        user_order = {}
        for idx, step in enumerate(scrambled):
            col_step, col_pos = st.columns([3, 1])
            with col_step:
                step_img, step_icon = resolve_option_visual(step)
                with st.container(border=True):
                    sub_c1, sub_c2 = st.columns([1, 2.5])
                    with sub_c1:
                        if step_img and os.path.exists(step_img):
                            st.image(step_img, use_container_width=True)
                    with sub_c2:
                        st.markdown(f"### {step_icon} **{step}**")
            with col_pos:
                pos = st.selectbox(
                    f"Position for step {idx+1}",
                    options=list(range(1, len(scrambled) + 1)),
                    index=idx,
                    key=f"timeline_pos_{idx}_{st.session_state.mem_current_trial}_{lang}",
                    label_visibility="collapsed"
                )
                user_order[step] = pos

        if st.button("✅ " + ("வரிசையைச் சரிபார்க்கவும்" if lang == "ta" else "Submit Timeline Sequence"), use_container_width=True):
            rt = round(time.time() - st.session_state.mem_trial_start_time, 2)
            sorted_by_user = sorted(scrambled, key=lambda s: user_order[s])
            is_correct = (sorted_by_user == correct_seq)

            st.session_state.mem_trials.append({
                "stimulus": "Timeline Sequencing",
                "target_response": " -> ".join(correct_seq),
                "user_response": " -> ".join(sorted_by_user),
                "is_correct": is_correct,
                "response_time_sec": rt,
                "difficulty_level": diff_num
            })

            st.session_state.mem_feedback = {
                "is_correct": is_correct,
                "correct_seq": correct_seq,
                "rt": rt
            }
            st.rerun()

        if st.session_state.mem_feedback:
            fb = st.session_state.mem_feedback
            if fb["is_correct"]:
                st.success(f"🎉 {'அற்புதம்! சரியான கால வரிசையில் அடுக்கிவிட்டீர்கள்!' if lang == 'ta' else 'Perfect! You sequenced your routine accurately!'} (⏱️ {fb['rt']}{'வி' if lang == 'ta' else 's'})")
                def on_next_timeline():
                    st.session_state.mem_current_trial += 1
                    st.session_state.mem_stimulus = None
                    st.session_state.mem_feedback = None
                    st.rerun()
                render_celebration(rhyme_idx=3, lang=lang, on_continue=on_next_timeline)
            else:
                st.warning(f"💡 {'சரியான வரிசை:' if lang == 'ta' else 'The ideal chronological order is:'}")
                for i, s in enumerate(fb["correct_seq"], 1):
                    st.write(f"{i}. {s}")

                if st.button("➡️ " + ("அடுத்த பயிற்சி" if lang == "ta" else "Next Routine"), key="timeline_next_btn", use_container_width=True):
                    st.session_state.mem_current_trial += 1
                    st.session_state.mem_stimulus = None
                    st.session_state.mem_feedback = None
                    st.rerun()
