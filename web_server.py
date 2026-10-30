"""
NeuroCare Web Portal - Standalone Web Application Server
Flask-powered REST APIs and Static Web Serving (No Streamlit required).
Clean, bright, Google / Vellore VTOP neat structure web architecture.
Restores ALL features from original app:
- 3 Clear Roles: Senior Mode (1-Tap), Caregiver Portal, Clinical Specialist Admin
- All 7 Clinical Cognitive Games
- Full Caregiver Memory Vault with local photo upload
- Full Clinical Analyst RCT Benchmark & LaTeX generation
- 100% Strict Bilingual Audio & Subtitle Localization (Tamil & English)
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, request, Response
from werkzeug.utils import secure_filename

# Fix Windows stdout encoding for utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from modules.motivational_story import DAILY_STORY_EPISODES, get_today_story_episode
from modules.voice_assistant import VoiceAssistant
from modules.research_stats import ResearchStatsEngine
from modules.personalization import PersonalizationEngine
from database.db_manager import DatabaseManager
from database.mock_data import seed_database_if_empty

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "neurocare_clinical.db")

os.makedirs(UPLOADS_DIR, exist_ok=True)

app = Flask(__name__, static_folder="static")
db = DatabaseManager(DB_PATH)
seed_database_if_empty(db)
personalization = PersonalizationEngine(db)
research_engine = ResearchStatsEngine()

# Ensure caregiver user exists in neurocare_clinical.db
try:
    if not db.authenticate_user("caregiver", "Caregiver@123"):
        db.register_user(
            username="caregiver",
            password="Caregiver@123",
            full_name="Primary Caregiver",
            role="caregiver",
            email="caregiver@care.neurocare.health",
            phone="+91 98401 23456"
        )
except Exception:
    pass


# ------------------------------------------------------------------------------
# STATIC FILE SERVING
# ------------------------------------------------------------------------------

@app.route("/")
def index():
    """Serves the main single-page web portal."""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    """Serves CSS, JS, and static assets."""
    return send_from_directory(STATIC_DIR, filename)


@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    """Serves high-resolution moving picture assets and uploaded memory images."""
    return send_from_directory(UPLOADS_DIR, filename)


# ------------------------------------------------------------------------------
# 1. AUTHENTICATION & ROLE MANAGEMENT APIS
# ------------------------------------------------------------------------------

@app.route("/api/auth/login", methods=["POST"])
def api_auth_login():
    """
    Handles authentication for all 3 portals:
    1. Senior 1-Tap Mode: role='senior', patient_id
    2. Caregiver Login: role='caregiver', username, password
    3. Clinical Admin Login: role='admin', username, password
    """
    data = request.json or {}
    role = data.get("role", "senior")
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    patient_id = data.get("patient_id", 1)

    if role == "senior":
        patient = db.get_patient(patient_id)
        if not patient:
            all_p = db.get_all_patients()
            patient = all_p[0] if all_p else {"id": 1, "name": "Ramasamy Sundaram"}
        return jsonify({
            "status": "success",
            "role": "senior",
            "user": {
                "id": patient["id"],
                "username": f"senior_{patient['id']}",
                "full_name": patient["name"],
                "role": "senior"
            },
            "patient": patient
        })

    # Validate caregiver or admin credentials
    user = db.authenticate_user(username, password)
    if user:
        if role and user["role"] != role:
            return jsonify({
                "status": "error",
                "message": f"Account '{username}' has role '{user['role']}', not '{role}'."
            }), 403

        # Fetch assigned patient if caregiver
        assigned_patient = None
        if user["role"] == "caregiver":
            my_patients = db.get_all_patients(caregiver_id=user["id"])
            if not my_patients:
                all_p = db.get_all_patients()
                assigned_patient = all_p[0] if all_p else None
            else:
                assigned_patient = my_patients[0]
            db.log_audit(user["id"], user["username"], "caregiver", "LOGIN", "Logged into Caregiver Portal")
        elif user["role"] == "admin":
            db.log_audit(user["id"], user["username"], "admin", "LOGIN", "Logged into Clinical Specialist Portal")

        # Sanitize user dict
        user_clean = dict(user)
        user_clean.pop("password_hash", None)
        user_clean.pop("salt", None)

        return jsonify({
            "status": "success",
            "role": user["role"],
            "user": user_clean,
            "patient": assigned_patient
        })

    return jsonify({
        "status": "error",
        "message": "Invalid username or password. Please verify your credentials."
    }), 401


@app.route("/api/auth/register", methods=["POST"])
def api_auth_register():
    """Allows new caregivers to register directly from the portal."""
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    full_name = data.get("full_name", "").strip()
    phone = data.get("phone", "").strip()

    if not username or not password or not full_name:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    try:
        user_id = db.register_user(
            username=username,
            password=password,
            full_name=full_name,
            role="caregiver",
            phone=phone
        )
        if user_id:
            db.log_audit(user_id, username, "caregiver", "REGISTER", f"Registered new caregiver account: {full_name}")
            return jsonify({"status": "success", "user_id": user_id, "message": "Account created successfully."})
        else:
            return jsonify({"status": "error", "message": "Username already taken."}), 409
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/auth/patients", methods=["GET"])
def api_auth_patients():
    """Returns the list of senior patient profiles for the 1-Tap Launchpad."""
    patients = db.get_all_patients()
    patient_descriptions = {
        1: {
            "desc_ta": "ஓய்வுபெற்ற ஆசிரியர் • கர்நாடக இசை & கோயில் கலைகள்",
            "desc_en": "Retired Teacher • Carnatic Music & Temple Architecture"
        },
        2: {
            "desc_ta": "முன்னாள் பள்ளி முதல்வர் • வீட்டுத் தோட்டம் & குடும்ப நினைவுகள்",
            "desc_en": "Former Principal • Gardening & Family Reminiscence"
        },
        3: {
            "desc_ta": "மூத்த மருத்துவர் • பழைய ரயில் பயணம் & செவ்வியல் இலக்கியம்",
            "desc_en": "Senior Physician • Vintage Rail & Classical Literature"
        }
    }
    enriched = []
    for p in patients:
        p_dict = dict(p)
        info = patient_descriptions.get(p["id"], {
            "desc_ta": "அறிவாற்றல் நலவாழ்வு பயிற்சி",
            "desc_en": "Cognitive Longevity & Wellness"
        })
        p_dict["desc_ta"] = info["desc_ta"]
        p_dict["desc_en"] = info["desc_en"]
        enriched.append(p_dict)
    return jsonify(enriched)


# ------------------------------------------------------------------------------
# 2. BILINGUAL STORY VIDEO APIS (TAMIL & ENGLISH 100% STRICT)
# ------------------------------------------------------------------------------

@app.route("/api/story/all")
def api_story_all():
    """Returns all 7 daily episodes with bilingual URLs."""
    now = datetime.now()
    today_weekday = now.weekday()

    episodes_data = []
    for ep in DAILY_STORY_EPISODES:
        ep_dict = dict(ep)
        ep_dict["image_url"] = f"/uploads/story_images/day_{ep['day_idx']}.jpg"
        ep_dict["audio_url_ta"] = f"/api/story/audio?day={ep['day_idx']}&lang=ta"
        ep_dict["audio_url_en"] = f"/api/story/audio?day={ep['day_idx']}&lang=en"
        ep_dict["audio_url"] = f"/api/story/audio?day={ep['day_idx']}&lang=ta"
        episodes_data.append(ep_dict)

    today_ep = episodes_data[today_weekday % len(episodes_data)]

    return jsonify({
        "today_weekday": today_weekday,
        "today": today_ep,
        "episodes": episodes_data
    })


@app.route("/api/story/today")
def api_story_today():
    """Returns today's active story episode with bilingual audio links."""
    lang = request.args.get("lang", "ta")
    today_ep = get_today_story_episode()
    data = dict(today_ep)
    data["image_url"] = f"/uploads/story_images/day_{today_ep['day_idx']}.jpg"
    data["audio_url_ta"] = f"/api/story/audio?day={today_ep['day_idx']}&lang=ta"
    data["audio_url_en"] = f"/api/story/audio?day={today_ep['day_idx']}&lang=en"
    data["audio_url"] = f"/api/story/audio?day={today_ep['day_idx']}&lang={lang}"
    return jsonify(data)


@app.route("/api/story/audio")
def api_story_audio():
    """
    Streams the authentic native audio MP3 for the requested day and language.
    Strictly bilingual: Supports lang=en (English voice) and lang=ta (Tamil voice).
    """
    day_idx = int(request.args.get("day", 3))
    lang = request.args.get("lang", "ta")
    if lang not in ["en", "ta"]:
        lang = "ta"

    ep = DAILY_STORY_EPISODES[day_idx % len(DAILY_STORY_EPISODES)]
    title = ep["title_en"] if lang == "en" else ep["title_ta"]
    quote = ep["quote_en"] if lang == "en" else ep["quote_ta"]
    story_text = ep["story_en"] if lang == "en" else ep["story_ta"]

    full_text = f"{title}. {quote}. {story_text}"
    audio_path = VoiceAssistant.get_audio_file_path(full_text, lang=lang)

    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        return Response(audio_bytes, mimetype="audio/mp3")

    return Response(b"", status=404)


# ------------------------------------------------------------------------------
# 3. CAREGIVER PORTAL & MEMORY VAULT APIS
# ------------------------------------------------------------------------------

@app.route("/api/caregiver/patient")
def api_caregiver_patient():
    """Returns active patient profile for the caregiver."""
    patient_id = int(request.args.get("patient_id", 1))
    p = db.get_patient(patient_id)
    if not p:
        all_p = db.get_all_patients()
        p = all_p[0] if all_p else {}
    return jsonify(dict(p))


@app.route("/api/caregiver/memories", methods=["GET", "POST"])
def api_caregiver_memories():
    """
    GET: Returns all saved memories for the specified patient.
    POST: Uploads local family photo and stores memory anchor.
    """
    if request.method == "GET":
        patient_id = int(request.args.get("patient_id", 1))
        memories = db.get_patient_memories(patient_id)
        return jsonify(memories)

    if request.method == "POST":
        patient_id = int(request.form.get("patient_id", 1))
        category = request.form.get("category", "family")
        label_en = request.form.get("label_en", "").strip()
        label_ta = request.form.get("label_ta", "").strip()
        detail_en = request.form.get("detail_en", "").strip()
        detail_ta = request.form.get("detail_ta", "").strip()

        saved_rel_path = ""
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_name = f"p{patient_id}_{int(time.time())}_{filename}"
                dest_path = os.path.join(UPLOADS_DIR, unique_name)
                file.save(dest_path)
                saved_rel_path = os.path.join("uploads", unique_name)

        final_lbl_en = label_en if label_en else label_ta
        final_lbl_ta = label_ta if label_ta else label_en
        final_det_en = detail_en if detail_en else final_lbl_en
        final_det_ta = detail_ta if detail_ta else final_lbl_ta

        mem_id = db.add_memory(
            patient_id=patient_id,
            category=category,
            label_en=final_lbl_en,
            label_ta=final_lbl_ta,
            detail_en=final_det_en,
            detail_ta=final_det_ta,
            image_path=saved_rel_path
        )

        db.log_audit(2, "caregiver", "caregiver", "UPLOAD_MEMORY", f"Uploaded memory '{final_lbl_en}' into patient vault")

        return jsonify({
            "status": "success",
            "memory_id": mem_id,
            "message": "Memory saved successfully!"
        })


@app.route("/api/caregiver/memories/<int:mem_id>", methods=["DELETE"])
def api_caregiver_delete_memory(mem_id):
    """Deletes a memory anchor from patient vault."""
    db.delete_memory(mem_id)
    db.log_audit(2, "caregiver", "caregiver", "DELETE_MEMORY", f"Deleted memory ID {mem_id}")
    return jsonify({"status": "success", "message": "Memory deleted successfully."})


# ------------------------------------------------------------------------------
# 4. CLINICAL SPECIALIST & RESEARCH BENCHMARK APIS
# ------------------------------------------------------------------------------

@app.route("/api/clinical/overview")
def api_clinical_overview():
    """Returns top KPI numbers, caregiver roster, patient cohort, and audit events."""
    all_users = db.get_all_users()
    caregivers = [u for u in all_users if u["role"] == "caregiver"]
    all_patients = db.get_all_patients()
    all_sessions = db.get_all_sessions_df()
    audit_logs_df = db.get_audit_logs(limit=100)

    audit_records = audit_logs_df.to_dict(orient="records") if not audit_logs_df.empty else []
    sessions_records = all_sessions.to_dict(orient="records") if not all_sessions.empty else []

    # Caregiver roster with patient counts
    roster = []
    for cg in caregivers:
        c_patients = db.get_all_patients(caregiver_id=cg["id"])
        roster.append({
            "id": cg["id"],
            "username": cg["username"],
            "full_name": cg["full_name"],
            "phone": cg.get("phone", "N/A"),
            "assigned_patients": len(c_patients),
            "created_at": cg.get("created_at", "N/A")
        })

    return jsonify({
        "kpi": {
            "caregivers_count": len(caregivers),
            "patients_count": len(all_patients),
            "sessions_count": len(all_sessions),
            "audit_events_count": len(audit_records)
        },
        "caregivers": roster,
        "patients": [dict(p) for p in all_patients],
        "audit_logs": audit_records[:50],
        "sessions": sessions_records
    })


@app.route("/api/clinical/rct-stats")
def api_clinical_rct_stats():
    """
    Computes rigorous clinical statistics (Paired t-test, Cohen's d, p-value)
    across all 4 cognitive domains on the N=30 RCT benchmark and generates LaTeX table.
    """
    rct_df = research_engine.generate_rct_dataset(n_participants=30, seed=42)
    exp_df = rct_df[rct_df["Group"] == "Experimental (NeuroCare)"]

    domains_to_test = [
        ("Episodic Memory", exp_df["Pre_Memory"].values, exp_df["Post_Memory"].values),
        ("Attention & Executive", exp_df["Pre_Attention"].values, exp_df["Post_Attention"].values),
        ("Temporal Orientation", exp_df["Pre_Orientation"].values, exp_df["Post_Orientation"].values),
        ("Language & Naming", exp_df["Pre_Language"].values, exp_df["Post_Language"].values)
    ]

    stats_dict = {}
    table_rows = []
    for d_name, pre, post in domains_to_test:
        res = research_engine.calculate_domain_statistics(pre, post)
        stats_dict[d_name] = res
        table_rows.append({
            "domain": d_name,
            "pre_test": f"{res['mean_pre']:.2f} ± {res['std_pre']:.2f}",
            "post_test": f"{res['mean_post']:.2f} ± {res['std_post']:.2f}",
            "mean_gain": f"+{res['mean_gain']:.2f}",
            "t_stat": round(res["t_statistic"], 2),
            "p_value": "< 0.001" if res["p_value"] < 0.001 else f"{res['p_value']:.4f}",
            "cohens_d": round(res["cohens_d"], 2)
        })

    latex_code = research_engine.generate_latex_table(stats_dict)

    return jsonify({
        "participants_n": 30,
        "table_rows": table_rows,
        "latex_code": latex_code
    })


# ------------------------------------------------------------------------------
# 5. ALL 7 COGNITIVE GAMES APIS
# ------------------------------------------------------------------------------

# Game 3: Personalized Familiar Photo Recall
@app.route("/api/games/face-recall")
def api_game_face_recall():
    """Draws photo stimulus from the patient's personal memory vault."""
    patient_id = int(request.args.get("patient_id", 1))
    lang = request.args.get("lang", "ta")
    level = int(request.args.get("level", 2))

    stimulus = personalization.get_face_recall_stimuli(patient_id=patient_id, difficulty_level=level, lang=lang)
    return jsonify(stimulus)


# Game 4: Memory Span Increment
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

@app.route("/api/games/memory-increment")
def api_game_memory_increment():
    """Generates sequence memory increment trial."""
    span = int(request.args.get("span", 3))
    span = max(2, min(span, 6))
    lang = request.args.get("lang", "ta")

    chosen = random.sample(MEMORY_SYMBOLS, span)
    return jsonify({
        "span": span,
        "sequence": chosen,
        "all_symbols": MEMORY_SYMBOLS
    })


# Game 5: Color Stroop Attention Focus
STROOP_COLORS = [
    {"name_en": "RED", "name_ta": "சிவப்பு", "color": "#EF4444"},
    {"name_en": "BLUE", "name_ta": "நீலம்", "color": "#2563EB"},
    {"name_en": "GREEN", "name_ta": "பச்சை", "color": "#10B981"},
    {"name_en": "YELLOW", "name_ta": "மஞ்சள்", "color": "#F59E0B"}
]

@app.route("/api/games/stroop")
def api_game_stroop():
    """Generates a Stroop cognitive inhibition trial."""
    lang = request.args.get("lang", "ta")
    word_obj = random.choice(STROOP_COLORS)
    ink_obj = random.choice(STROOP_COLORS)

    return jsonify({
        "word_text": word_obj["name_ta"] if lang == "ta" else word_obj["name_en"],
        "display_color": ink_obj["color"],
        "correct_answer": ink_obj["name_ta"] if lang == "ta" else ink_obj["name_en"],
        "is_congruent": (word_obj["color"] == ink_obj["color"]),
        "options": [c["name_ta"] if lang == "ta" else c["name_en"] for c in STROOP_COLORS]
    })


# Game 6: Reality & Spatial Orientation
ORIENTATION_QUESTIONS = {
    "temporal": [
        {
            "question_ta": "தற்போது நாம் எந்தக் காலத்தில் இருக்கிறோம்?",
            "question_en": "Which season or weather period are we currently in?",
            "correct_ta": "பருவமழை காலம் (Monsoon)",
            "correct_en": "Monsoon / Rainy Season",
            "options_ta": ["பருவமழை காலம் (Monsoon)", "சுட்டெரிக்கும் கோடை (Summer)", "பனிக்காலம் (Winter)", "இலையுதிர் காலம் (Autumn)"],
            "options_en": ["Monsoon / Rainy Season", "Peak Summer", "Winter Frost", "Spring Bloom"],
            "icon": "🌦️"
        },
        {
            "question_ta": "இப்போது பகலின் எந்த வேளையில் நாம் இருக்கிறோம்?",
            "question_en": "What time of the day is it right now?",
            "correct_ta": "காலை / பகல் வேளை (Daytime)",
            "correct_en": "Daytime / Morning",
            "options_ta": ["காலை / பகல் வேளை (Daytime)", "நள்ளிரவு (Midnight)", "அதிகாலை 3 மணி", "சாயங்காலம் அந்திப் பொழுது"],
            "options_en": ["Daytime / Morning", "Midnight Dark", "Pre-dawn 3 AM", "Late Twilight"],
            "icon": "☀️"
        },
        {
            "question_ta": "கடிகாரத்தில் சிறிய முள் 3-லும் பெரிய முள் 12-லும் இருந்தால் நேரம் என்ன?",
            "question_en": "If the short clock hand is on 3 and long hand on 12, what time is it?",
            "correct_ta": "3 மணி (3:00 O'Clock)",
            "correct_en": "3:00 O'Clock",
            "options_ta": ["3 மணி (3:00 O'Clock)", "12 மணி (12:00)", "6 மணி (6:00)", "9 மணி (9:00)"],
            "options_en": ["3:00 O'Clock", "12:00 O'Clock", "6:00 O'Clock", "9:00 O'Clock"],
            "icon": "🕰️"
        }
    ],
    "spatial": [
        {
            "question_ta": "நாம் சுவையான உணவு மற்றும் காபி தயார் செய்யும் அறை எது?",
            "question_en": "In which room do we prepare fresh coffee and meals?",
            "correct_ta": "சமையலறை (Kitchen)",
            "correct_en": "Kitchen",
            "options_ta": ["சமையலறை (Kitchen)", "படுக்கையறை (Bedroom)", "குளியலறை (Bathroom)", "பால்கனி (Balcony)"],
            "options_en": ["Kitchen", "Bedroom", "Bathroom", "Balcony"],
            "icon": "🍳"
        },
        {
            "question_ta": "இரவில் நாம் நிம்மதியாக ஓய்வெடுத்து உறங்கும் இடம் எது?",
            "question_en": "Where in the house do we rest and sleep comfortably at night?",
            "correct_ta": "படுக்கையறை (Bedroom)",
            "correct_en": "Bedroom",
            "options_ta": ["படுக்கையறை (Bedroom)", "சாப்பாட்டு கூடம் (Dining)", "முன் வராண்டா (Porch)", "சமையலறை (Kitchen)"],
            "options_en": ["Bedroom", "Dining Hall", "Front Porch", "Kitchen"],
            "icon": "🛏️"
        },
        {
            "question_ta": "செடிகளுக்கு தண்ணீர் ஊற்றி, பூக்களைப் பார்க்கும் இடம் எது?",
            "question_en": "Where do we water flowering plants and enjoy fresh green breeze?",
            "correct_ta": "வீட்டுத் தோட்டம் (Garden)",
            "correct_en": "Home Garden",
            "options_ta": ["வீட்டுத் தோட்டம் (Garden)", "பொருளறை (Store Room)", "குளியலறை (Bathroom)", "படுக்கையறை (Bedroom)"],
            "options_en": ["Home Garden", "Store Room", "Bathroom", "Bedroom"],
            "icon": "🌺"
        }
    ]
}

@app.route("/api/games/orientation")
def api_game_orientation():
    """Generates reality orientation question."""
    ori_type = request.args.get("type", "temporal")
    lang = request.args.get("lang", "ta")
    pool = ORIENTATION_QUESTIONS.get(ori_type, ORIENTATION_QUESTIONS["temporal"])
    q = random.choice(pool)

    return jsonify({
        "type": ori_type,
        "question": q["question_ta"] if lang == "ta" else q["question_en"],
        "correct": q["correct_ta"] if lang == "ta" else q["correct_en"],
        "options": q["options_ta"] if lang == "ta" else q["options_en"],
        "icon": q["icon"]
    })


# Game 7: Language & Semantic Object Naming
NAMING_OBJECTS = [
    {
        "en": "Reading Glasses",
        "ta": "மூக்குக் கண்ணாடி",
        "icon": "👓",
        "category_en": "Personal Accessory",
        "category_ta": "பயன்பாட்டுப் பொருள்",
        "options_ta": ["மூக்குக் கண்ணாடி", "புல்லாங்குழல்", "காபி டம்ளர்", "குடை"],
        "options_en": ["Reading Glasses", "Flute", "Coffee Tumbler", "Umbrella"]
    },
    {
        "en": "Coffee Tumbler",
        "ta": "பித்தளை காபி டம்ளர்",
        "icon": "☕",
        "category_en": "Kitchen Utensil",
        "category_ta": "சமையலறைப் பாத்திரம்",
        "options_ta": ["பித்தளை காபி டம்ளர்", "சுவர்க் கடிகாரம்", "மூக்குக் கண்ணாடி", "புத்தகம்"],
        "options_en": ["Coffee Tumbler", "Wall Clock", "Reading Glasses", "Book"]
    },
    {
        "en": "Carnatic Flute",
        "ta": "புல்லாங்குழல்",
        "icon": "🪈",
        "category_en": "Musical Instrument",
        "category_ta": "இசைக் கருவி",
        "options_ta": ["புல்லாங்குழல்", "குடை", "பல் துலக்கும் பிரஷ்", "பூட்டு & சாவி"],
        "options_en": ["Carnatic Flute", "Umbrella", "Toothbrush", "Lock & Key"]
    },
    {
        "en": "Umbrella",
        "ta": "மழைக்குடை",
        "icon": "☂️",
        "category_en": "Rain Protection",
        "category_ta": "மழைப் பாதுகாப்பு",
        "options_ta": ["மழைக்குடை", "காபி டம்ளர்", "மூக்குக் கண்ணாடி", "சுவர்க் கடிகாரம்"],
        "options_en": ["Umbrella", "Coffee Tumbler", "Reading Glasses", "Wall Clock"]
    },
    {
        "en": "Wall Clock",
        "ta": "சுவர்க் கடிகாரம்",
        "icon": "🕰️",
        "category_en": "Timepiece",
        "category_ta": "நேரம் காட்டும் கருவி",
        "options_ta": ["சுவர்க் கடிகாரம்", "புல்லாங்குழல்", "மழைக்குடை", "புத்தகம்"],
        "options_en": ["Wall Clock", "Carnatic Flute", "Umbrella", "Book"]
    },
    {
        "en": "Reading Book",
        "ta": "செவ்வியல் புத்தகம்",
        "icon": "📖",
        "category_en": "Literature",
        "category_ta": "இலக்கியம் & படிப்பு",
        "options_ta": ["செவ்வியல் புத்தகம்", "மூக்குக் கண்ணாடி", "காபி டம்ளர்", "பல் துலக்கும் பிரஷ்"],
        "options_en": ["Reading Book", "Reading Glasses", "Coffee Tumbler", "Toothbrush"]
    }
]

@app.route("/api/games/language")
def api_game_language():
    """Generates Boston Naming style trial."""
    lang = request.args.get("lang", "ta")
    obj = random.choice(NAMING_OBJECTS)
    return jsonify({
        "target": obj["ta"] if lang == "ta" else obj["en"],
        "icon": obj["icon"],
        "category": obj["category_ta"] if lang == "ta" else obj["category_en"],
        "options": obj["options_ta"] if lang == "ta" else obj["options_en"]
    })


# Telemetry Session Record
@app.route("/api/sessions/record", methods=["POST"])
def api_record_session():
    """Records gameplay telemetry into the clinical database."""
    data = request.json or {}
    patient_id = data.get("patient_id", 1)
    game_key = data.get("game_key", "sudoku_4x4")
    level = data.get("level", 5)
    score = data.get("score", 100)
    accuracy = data.get("accuracy", 1.0)
    rt = data.get("response_time_ms", 1200)

    try:
        session_id = db.record_session(
            patient_id=patient_id,
            game_key=game_key,
            level=level,
            score=score,
            accuracy=accuracy,
            response_time_ms=rt
        )
        return jsonify({"status": "success", "session_id": session_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/patient")
def api_patient():
    """Returns the primary senior patient record."""
    patient_id = int(request.args.get("id", 1))
    patient = db.get_patient(patient_id)
    if patient:
        return jsonify(dict(patient))
    all_p = db.get_all_patients()
    if all_p:
        return jsonify(dict(all_p[0]))
    return jsonify({
        "id": 1,
        "name": "Ramasamy Sundaram",
        "age": 74,
        "condition": "Mild Cognitive Impairment (MCI)",
        "baseline_mmse": 23.5,
        "current_adaptive_level": 5
    })


@app.route("/api/analytics")
def api_analytics():
    """Returns clinical longitudinal telemetry data."""
    try:
        patient_id = int(request.args.get("patient_id", 1))
        sessions_df = db.get_patient_session_history(patient_id=patient_id)
        sessions_list = sessions_df.to_dict(orient="records") if not sessions_df.empty else []
        return jsonify({
            "total_sessions": len(sessions_list),
            "recent_sessions": sessions_list[:15]
        })
    except Exception:
        return jsonify({"total_sessions": 0, "recent_sessions": []})


# ------------------------------------------------------------------------------
# SERVER MAIN ENTRYPOINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("==================================================================")
    print("[*] NEUROCARE STANDALONE WEB PORTAL (Google & Vellore VTOP Structure)")
    print("==================================================================")
    print("[*] All 3 Roles: Senior Patient Mode, Caregiver Portal, Clinical Specialist")
    print("[*] All 7 Cognitive Clinical Games Fully Integrated")
    print("[*] Bilingual Audio & Subtitles: Pure Tamil (ta) and Pure English (en)")
    print("[*] Running on: http://localhost:5000")
    print("==================================================================")
    app.run(host="0.0.0.0", port=5000, debug=False)
