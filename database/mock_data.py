"""
Mock Data Generator & Initial Seeder for NeuroCare Platform.
Populates:
- Admin & Caregiver accounts
- Audit trails tracking caregiver activity
- Patient profiles with local uploaded image paths
- 28-day longitudinal cognitive training records
"""

from datetime import datetime, timedelta
import random
import os
from database.db_manager import DatabaseManager

def seed_database_if_empty(db: DatabaseManager):
    """Checks if the database is empty; if so, populates comprehensive mock clinical data."""
    users = db.get_all_users()
    if len(users) > 0:
        return  # Already seeded

    # 1. Seed System Users (Admin & Caregivers)
    admin_id = db.register_user(
        username="admin",
        password="admin123",
        full_name="Dr. S. Meenakshi (Clinical Admin)",
        role="admin",
        email="admin@neurocare.health",
        phone="+91 94440 11223"
    )

    c1_id = db.register_user(
        username="caregiver",
        password="Caregiver@123",
        full_name="Primary Caregiver",
        role="caregiver",
        email="caregiver@care.neurocare.health",
        phone="+91 98401 23456"
    )

    c2_id = db.register_user(
        username="caregiver2",
        password="Caregiver@123",
        full_name="Clinical Caregiver",
        role="caregiver",
        email="caregiver2@care.neurocare.health",
        phone="+91 94440 98765"
    )

    # 2. Seed Sample Patients linked to Caregivers
    p1_id = db.add_patient(
        name="Ramasamy Sundaram",
        age=74,
        condition="Mild Cognitive Impairment (MCI)",
        baseline_mmse=23.5,
        language_preference="ta",
        caregiver_name="Primary Caregiver",
        caregiver_contact="+91 98401 23456",
        notes="Retired Mathematics teacher. Enjoys Carnatic music and temple architecture.",
        caregiver_id=c1_id
    )

    p2_id = db.add_patient(
        name="Kalyani Narayanan",
        age=68,
        condition="Mild Dementia (Early Stage)",
        baseline_mmse=19.0,
        language_preference="en",
        caregiver_name="Clinical Caregiver",
        caregiver_contact="+91 94440 98765",
        notes="Former school principal. Responsive to familiar household photos, gardening memories.",
        caregiver_id=c2_id
    )

    p3_id = db.add_patient(
        name="Dr. K. S. Ramanathan",
        age=79,
        condition="Age-Associated Memory Impairment",
        baseline_mmse=25.0,
        language_preference="en",
        caregiver_name="Primary Caregiver",
        caregiver_contact="+91 98401 23456",
        notes="High cognitive reserve. Prefers fast-paced executive function challenges.",
        caregiver_id=c1_id
    )

    # 3. Seed Personalized Memories with Local Image File Paths in uploads/
    memories_p1 = [
        ("family", "Daughter - Ananya", "மகள் - அனன்யா",
         "Daughter who visits every Sunday with filter coffee.",
         "ஒவ்வொரு ஞாயிறும் பில்டர் காபியுடன் வந்து நலம் விசாரிக்கும் அன்பு மகள்.",
         "uploads/sample_daughter.jpg"),
        
        ("family", "Grandson - Arvind", "பேரன் - அரவிந்த்",
         "Grandson studying engineering who plays chess with him.",
         "பொறியியல் படிக்கும் மற்றும் அவருடன் சதுரங்கம் விளையாடும் பாசமிகு பேரன்.",
         "uploads/sample_grandson.jpg"),

        ("family", "Wife - Rukmini", "மனைவி - ருக்மணி",
         "Beloved wife of 48 years, known for her delicious rasam.",
         "48 ஆண்டுகால அன்பான மனைவி, சுவையான ரசம் வைப்பதில் வல்லவர்.",
         "uploads/sample_wife.jpg"),

        ("place", "Madurai Meenakshi Temple", "மதுரை மீனாட்சி அம்மன் கோவில்",
         "Childhood hometown temple where he used to walk every evening.",
         "அவர் சிறுவயதில் மாலைதோறும் சென்று வழிபட்ட சொந்த ஊர் கோவில்.",
         "uploads/sample_temple.jpg"),

        ("routine", "Morning Filter Coffee", "காலை பில்டர் காபி குடித்தல்",
         "First thing at 6:30 AM in traditional brass tumbler.",
         "காலை 6:30 மணிக்கு பாரம்பரிய பித்தளை டம்ளரில் அருந்தும் வழக்கம்.",
         "uploads/sample_coffee.jpg"),

        ("hobby", "Playing Carnatic Flute", "புல்லாங்குழல் வாசித்தல்",
         "Playing peaceful ragas like Kalyani and Mohanam on weekend evenings.",
         "வார இறுதி நாட்களில் கல்யாணி மற்றும் மோகன ராகங்களை வாசித்தல்.",
         "uploads/sample_flute.jpg"),

        ("object", "Reading Glasses (Spectacles)", "மூக்குக் கண்ணாடி",
         "Spectacles used every morning to read the news.",
         "காலை செய்திதாள் வாசிக்கப் பயன்படுத்தும் மூக்குக் கண்ணாடி.",
         "uploads/sample_spectacles.jpg")
    ]

    for cat, l_en, l_ta, d_en, d_ta, img_p in memories_p1:
        db.add_memory(p1_id, cat, l_en, l_ta, d_en, d_ta, img_p)

    # 4. Seed Audit Logs for Caregiver Process & Oversight
    db.log_audit(admin_id, "admin", "admin", "SYSTEM_INIT", "System initialized and clinical database seeded")
    db.log_audit(c1_id, "caregiver", "caregiver", "LOGIN", "Caregiver logged in from Web Portal")
    db.log_audit(c1_id, "caregiver", "caregiver", "ADD_PATIENT", "Registered patient Ramasamy Sundaram (MCI)")
    db.log_audit(c1_id, "caregiver", "caregiver", "UPLOAD_MEMORY", "Uploaded family photos: Daughter, Grandson, Wife")
    db.log_audit(c1_id, "caregiver", "caregiver", "LAUNCH_SESSION", "Launched Cognitive Training Session for Patient Ramasamy")
    db.log_audit(c2_id, "caregiver2", "caregiver", "LOGIN", "Caregiver logged in")
    db.log_audit(c2_id, "caregiver2", "caregiver", "ADD_PATIENT", "Registered patient Kalyani Narayanan (Early Dementia)")

    # 5. Seed 4-Week Longitudinal Sessions for Patient 1
    base_time = datetime.now() - timedelta(days=28)
    domains = ["memory", "attention", "orientation", "language"]
    game_names = {
        "memory": "Familiar Face & Life Timeline Recall",
        "attention": "Bilingual Stroop & Trail Making Test",
        "orientation": "Temporal & Spatial Daily Navigator",
        "language": "Semantic Object Naming & Category Fluency"
    }

    random.seed(42)
    curr_level = 1
    for day in range(28):
        session_time = base_time + timedelta(days=day, hours=random.randint(9, 11), minutes=random.randint(10, 50))
        domain = domains[day % 4]
        game_name = game_names[domain]
        
        progress_factor = day / 28.0
        acc = min(96.0, 62.0 + (progress_factor * 26.0) + random.uniform(-6.0, 6.0))
        rt = max(1.8, 5.2 - (progress_factor * 2.4) + random.uniform(-0.4, 0.4))
        
        start_lvl = curr_level
        if acc >= 80.0 and rt <= 3.5:
            curr_level = min(5, curr_level + 1)
        elif acc < 60.0 or rt > 5.0:
            curr_level = max(1, curr_level - 1)
        end_lvl = curr_level

        total_trials = 8
        correct_trials = int(round((acc / 100.0) * total_trials))
        fatigue = 1 if (random.random() < 0.12 and day < 10) else 0

        sess_id = db.record_session(
            patient_id=p1_id,
            cognitive_domain=domain,
            game_name=game_name,
            start_level=start_lvl,
            end_level=end_lvl,
            total_trials=total_trials,
            correct_trials=correct_trials,
            accuracy_pct=round(acc, 1),
            avg_response_time_sec=round(rt, 2),
            fatigue_events=fatigue,
            caregiver_notes=f"Week {day//7 + 1} session logged by Primary Caregiver."
        )
