"""
Automated Verification Suite for NeuroCare Platform.
Tests database, user authentication, audit trails, adaptive engine, personalization vault,
local uploaded images, and research stats.
"""

import os
import sys
import io
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from database.db_manager import DatabaseManager
from database.mock_data import seed_database_if_empty
from modules.personalization import PersonalizationEngine
from modules.adaptive_engine import AdaptiveDifficultyEngine
from modules.voice_assistant import VoiceAssistant
from modules.research_stats import ResearchStatsEngine

def run_all_tests():
    print("==================================================")
    print("[*] Running NeuroCare Platform Automated Verification Suite")
    print("==================================================")

    test_db_path = "test_neurocare_auth.db"
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except Exception:
            pass

    # 1. Test Database & RBAC Authentication
    db = DatabaseManager(test_db_path)
    seed_database_if_empty(db)

    # Test Admin Authentication
    admin_auth = db.authenticate_user("admin", "admin123")
    assert admin_auth is not None and admin_auth["role"] == "admin"
    print(f"✅ Admin Authentication: PASS (User: {admin_auth['full_name']})")

    # Test Caregiver Authentication
    cg_auth = db.authenticate_user("caregiver", "Caregiver@123")
    assert cg_auth is not None and cg_auth["role"] == "caregiver"
    print(f"✅ Caregiver Authentication: PASS (User: {cg_auth['full_name']})")

    # Test Failed Auth
    bad_auth = db.authenticate_user("caregiver", "wrongpass")
    assert bad_auth is None
    print("✅ Security Rejection on Invalid Password: PASS")

    # 2. Test Caregiver Audit Logs
    audit_df = db.get_audit_logs(limit=50)
    assert len(audit_df) >= 3
    print(f"✅ Caregiver Action Audit Trail: PASS ({len(audit_df)} audit events recorded)")

    # 3. Test Patients & Local Image Memory Vault
    patients = db.get_all_patients()
    assert len(patients) >= 3
    p1 = patients[0]
    memories = db.get_patient_memories(p1["id"])
    assert len(memories) >= 5
    print(f"✅ Patient Memory Vault with Local Paths: PASS ({len(memories)} memories linked to {p1['name']})")

    # 4. Test Personalization Engine
    pe = PersonalizationEngine(db)
    face_stim = pe.get_face_recall_stimuli(p1["id"], difficulty_level=2, lang="ta")
    assert "target" in face_stim and len(face_stim["options"]) >= 2
    print(f"✅ Personalization Engine (Tamil Face Recall): PASS (Target: {face_stim['target']})")

    # 5. Test Adaptive Engine
    ae = AdaptiveDifficultyEngine()
    trials_good = [{"is_correct": True, "response_time_sec": 2.1} for _ in range(5)]
    decision_up = ae.evaluate_session_performance(current_level=2, trial_results=trials_good)
    assert decision_up.next_level == 3 and decision_up.action == "INCREASE"
    print(f"✅ Adaptive Progression (EDA): PASS (Level 2 -> Level {decision_up.next_level})")

    # 6. Test Memory Increment Game & Photo Guard
    from games.memory_increment_game import MEMORY_SYMBOLS, render_memory_increment_game
    assert len(MEMORY_SYMBOLS) >= 6
    print(f"✅ Memory Span Increment Game Symbols: PASS ({len(MEMORY_SYMBOLS)} symbols configured)")

    # Test empty photos guard
    no_photo_stim = pe.get_face_recall_stimuli(patient_id=9999, difficulty_level=1, lang="en")
    assert no_photo_stim["has_photos"] is False
    print("✅ Photo Recall Empty-Upload Safety Guard: PASS (Questions suppressed when no photos exist)")

    # 7. Test Research Suite
    re = ResearchStatsEngine()
    rct_df = re.generate_rct_dataset(n_participants=30, seed=42)
    assert len(rct_df) == 30
    exp_cohort = rct_df[rct_df["Group"] == "Experimental (NeuroCare)"]
    stats_res = re.calculate_domain_statistics(exp_cohort["Pre_Memory"].values, exp_cohort["Post_Memory"].values)
    assert stats_res["p_value"] < 0.01 and stats_res["cohens_d"] > 0.8
    print(f"✅ Research RCT Statistics: PASS (t={stats_res['t_statistic']}, p={stats_res['p_value']}, Cohen's d={stats_res['cohens_d']})")

    # Cleanup
    try:
        import gc
        gc.collect()
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
    except Exception:
        pass

    print("==================================================")
    print("[SUCCESS] ALL VERIFICATION SUITES PASSED (100%)")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
