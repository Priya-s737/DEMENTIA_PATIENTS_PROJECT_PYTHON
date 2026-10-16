"""
Configuration module for Cognitive Gaming & Memory Assistance Platform.
Clinical Cognitive Assessment & Memory Assistance Platform.
"""

APP_NAME = "NeuroCare - Cognitive Memory & Assistance Platform"
APP_SUBTITLE = "Personalized, Adaptive Cognitive Gaming for Dementia & MCI"
VERSION = "2.0.0-PRO"
AUTHORS = ["Clinical NeuroCare Team"]
INSTITUTION = "Cognitive Rehabilitation & Memory Health Network"

# Cognitive Domains Supported
COGNITIVE_DOMAINS = {
    "memory": {
        "name_en": "Episodic & Working Memory",
        "name_ta": "நினைவாற்றல் பயிற்சி",
        "description_en": "Recalling familiar faces, life timelines, and visual item matrices.",
        "description_ta": "குடும்பத்தினர் முகம், வாழ்க்கை நிகழ்வுகள் மற்றும் படங்களை நினைவில் கொள்ளுதல்.",
        "icon": "🧠",
        "color": "#4A90E2"
    },
    "attention": {
        "name_en": "Attention & Executive Function",
        "name_ta": "கவனக்குவிப்பு & செயல் திறன்",
        "description_en": "Bilingual Stroop test and digital trail-making sequential challenges.",
        "description_ta": "வண்ணம்-சொல் வேறுபாடு அறிதல் மற்றும் வரிசை இணைப்புப் பயிற்சிகள்.",
        "icon": "🎯",
        "color": "#E67E22"
    },
    "orientation": {
        "name_en": "Temporal & Spatial Orientation",
        "name_ta": "காலம் மற்றும் இட உணர்வு",
        "description_en": "Awareness of date, time of day, home environment, and daily activities.",
        "description_ta": "நேரம், நாள், பருவநிலை மற்றும் இருப்பிட விழிப்புணர்வு பயிற்சிகள்.",
        "icon": "🧭",
        "color": "#27AE60"
    },
    "language": {
        "name_en": "Language & Semantic Recognition",
        "name_ta": "மொழி மற்றும் பொருள் அறிதல்",
        "description_en": "Naming daily objects, category fluency, and cross-lingual cues.",
        "description_ta": "பயன்பாட்டு பொருட்கள் பெயர் அறிதல் மற்றும் மொழிப் பயிற்சிகள்.",
        "icon": "🗣️",
        "color": "#9B59B6"
    }
}

# Bilingual Localization Dictionary
TRANSLATIONS = {
    "en": {
        # General & Navigation
        "app_title": "NeuroCare Assistant",
        "select_mode": "Select Portal Mode",
        "patient_mode": "👵 Elderly / Patient Mode",
        "caregiver_mode": "👨‍⚕️ Caregiver & Clinician Portal",
        "research_mode": "📊 Research & Publication Suite",
        "language_select": "Select Language / மொழியைத் தேர்ந்தெடுக்கவும்",
        "welcome_patient": "Welcome back! Let's exercise your mind with pleasant memories today.",
        "encouragement_positive": "Wonderful job! You did fantastic!",
        "encouragement_gentle": "Take your time. You are doing very well.",
        "fatigue_notice": "You seem a bit tired. Let's take a peaceful 1-minute breathing break!",
        "start_game": "▶️ Start Activity",
        "next_question": "➡️ Next Question",
        "submit_answer": "✅ Submit Answer",
        "well_done": "🎉 Excellent Work!",
        "try_again": "Almost there! Let's try once more.",
        "score_label": "Your Score",
        "level_label": "Adaptive Level",
        "time_taken": "Response Time",
        "listen_audio": "🔊 Listen to Prompt",
        "read_aloud": "Read Aloud",
        
        # Domains & Specialized Games
        "domain_memory": "Memory Games",
        "domain_attention": "Attention & Focus",
        "domain_orientation": "Time & Location",
        "domain_language": "Language & Naming",
        "game_sudoku": "🧩 Senior Sudoku Challenge",
        "game_memory_pairs": "🃏 Memory Matching Pairs",
        "game_face_recall": "🖼️ Photo & Memory Recall",
        "game_memory_increment": "🔢 Memory Span Increment",
        "game_stroop": "🎨 Color Stroop Task",
        "game_orientation": "🕒 Reality Orientation",
        "game_language": "🏷️ Object & Category Match",
        "motivational_story_title": "📖 Daily Uplifting Story",
        
        # Caregiver Portal
        "caregiver_header": "Caregiver & Clinical Dashboard",
        "profile_management": "Patient Profiles & Memory Vault",
        "add_memory": "Add New Personal Memory",
        "manage_memories": "Personalized Familiar Anchors",
        "analytics_overview": "Longitudinal Cognitive Trajectories",
        "clinical_summary": "Generate Clinical Summary Report",
        "adaptive_settings": "Adaptive Engine Sensitivity Parameters",
        
        # Research Suite
        "research_header": "Conference Research & Statistical Evaluation Suite",
        "dataset_generator": "Randomized Benchmark RCT Generator (N=30)",
        "run_stats": "Run Statistical Significance Tests (Paired t-test, Cohen's d)",
        "latex_table": "Export LaTeX Conference Table",
        "citation_box": "Recommended Conference Citation"
    },
    "ta": {
        # General & Navigation
        "app_title": "நியூரோகேர் நினைவாற்றல் தளம்",
        "select_mode": "பிரிவைத் தேர்ந்தெடுக்கவும்",
        "patient_mode": "👵 முதியோர் / நோயாளி பிரிவு",
        "caregiver_mode": "👨‍⚕️ பராமரிப்பாளர் & மருத்துவர் பிரிவு",
        "research_mode": "📊 ஆய்வுக் கட்டுரை மற்றும் பகுப்பாய்வு",
        "language_select": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "welcome_patient": "வணக்கம்! இன்று உங்கள் நினைவுகளைப் புதுப்பித்து மகிழ்வோம்.",
        "encouragement_positive": "மிக அற்புதம்! மிகச் சிறப்பாகச் செய்தீர்கள்!",
        "encouragement_gentle": "பொறுமையாகச் செய்யுங்கள். நீங்கள் நன்றாகச் செய்கிறீர்கள்.",
        "fatigue_notice": "நீங்கள் சோர்வாக உணர்கிறீர்கள் போல் உள்ளது. சிறிது நேரம் ஓய்வெடுக்கலாம் வாருங்கள்!",
        "start_game": "▶️ விளையாட்டைத் தொடங்கு",
        "next_question": "➡️ அடுத்த கேள்வி",
        "submit_answer": "✅ பதிலைச் சமர்ப்பிக்கவும்",
        "well_done": "🎉 மிகச் சிறப்பு!",
        "try_again": "பரவாயில்லை! மீண்டும் ஒருமுறை முயற்சிப்போம்.",
        "score_label": "உங்கள் மதிப்பெண்",
        "level_label": "தற்போதைய நிலை",
        "time_taken": "எடுத்துக்கொண்ட நேரம்",
        "listen_audio": "🔊 குரல் வழியே கேள்",
        "read_aloud": "குரலில் வாசி",
        
        # Domains & Specialized Games
        "domain_memory": "நினைவாற்றல் பயிற்சிகள்",
        "domain_attention": "கவனக்குவிப்புப் பயிற்சிகள்",
        "domain_orientation": "காலம் மற்றும் இடம்",
        "domain_language": "மொழி மற்றும் சொற்கள்",
        "game_sudoku": "🧩 முதியோர் சுடோக்கு புதிர்",
        "game_memory_pairs": "🃏 ஜோடி நினைவாற்றல் விளையாட்டு",
        "game_face_recall": "🖼️ நினைவுப் புகைப்படம் அறிதல்",
        "game_memory_increment": "🔢 நினைவுத்திறன் அதிகரிப்பு",
        "game_stroop": "🎨 வண்ணக் கவனக்குவிப்புப் பயிற்சி",
        "game_orientation": "🕒 காலம் & இருப்பிடம் அறிதல்",
        "game_language": "🏷️ பொருள் & மொழி அறிதல்",
        "motivational_story_title": "📖 தினசரி உத்வேகக் கதை",
        
        # Caregiver Portal
        "caregiver_header": "பராமரிப்பாளர் கட்டுப்பாட்டு மையம்",
        "profile_management": "நோயாளி சுயவிவரம் & நினைவுக் களஞ்சியம்",
        "add_memory": "புதிய குடும்ப நினைவைச் சேர்க்க",
        "manage_memories": "சேமிக்கப்பட்ட நினைவுகள்",
        "analytics_overview": "முன்னேற்றப் புள்ளிவிவரங்கள்",
        "clinical_summary": "மருத்துவ அறிக்கை உருவாக்கு",
        "adaptive_settings": "தானியங்கி கடினத்தன்மை அமைப்புகள்",
        
        # Research Suite
        "research_header": "ஆய்வுக் கட்டுரை மற்றும் புள்ளிவிவர மையம்",
        "dataset_generator": "ஆய்வு தரவுத்தளம் (RCT Benchmark, N=30)",
        "run_stats": "புள்ளிவிவரச் சோதனை (Paired t-test, Cohen's d)",
        "latex_table": "LaTeX அட்டவணையாக மாற்றுக",
        "citation_box": "ஆய்வுக் குறிப்பு"
    }
}

# Color palettes for accessibility
THEMES = {
    "Warm Calming (Recommended)": {
        "bg_primary": "#F8FAFC",
        "card_bg": "#FFFFFF",
        "text_primary": "#0F172A",
        "accent": "#2563EB",
        "success": "#16A34A",
        "warning": "#D97706",
        "border": "#E2E8F0"
    },
    "High Contrast (Elderly AAA)": {
        "bg_primary": "#000000",
        "card_bg": "#1E293B",
        "text_primary": "#FFFFFF",
        "accent": "#FACC15",
        "success": "#4ADE80",
        "warning": "#FB923C",
        "border": "#FFFFFF"
    }
}
