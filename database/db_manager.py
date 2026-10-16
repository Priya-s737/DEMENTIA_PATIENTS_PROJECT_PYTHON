"""
Database Manager for NeuroCare Platform.
SQLite-backed persistent data layer for patient profiles, personalized caregiver memories,
clinical session telemetry, role-based authentication (Admin/Caregiver), and audit logs.
"""

import sqlite3
import os
import hashlib
import secrets
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "neurocare.db")
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hashes a password using SHA-256 with a unique cryptographic salt."""
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return pwd_hash, salt

class DatabaseManager:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database schema if tables do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Users table (Admin & Caregiver accounts)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL, -- 'admin', 'caregiver'
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 2. Caregiver Action & System Audit Logs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT NOT NULL,
                role TEXT NOT NULL,
                action TEXT NOT NULL, -- 'LOGIN', 'ADD_PATIENT', 'UPLOAD_MEMORY', 'LAUNCH_SESSION', 'EXPORT_REPORT'
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 3. Patients table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caregiver_id INTEGER,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                condition TEXT NOT NULL,
                baseline_mmse REAL DEFAULT 22.0,
                language_preference TEXT DEFAULT 'en',
                caregiver_name TEXT NOT NULL,
                caregiver_contact TEXT,
                current_adaptive_level INTEGER DEFAULT 2,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE SET NULL
            )
            """)

            # 4. Caregiver Familiar Memories (Reminiscence Vault with Local Image Paths)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                category TEXT NOT NULL, -- 'family', 'place', 'routine', 'hobby', 'object'
                label_en TEXT NOT NULL,
                label_ta TEXT NOT NULL,
                detail_en TEXT NOT NULL,
                detail_ta TEXT NOT NULL,
                image_path TEXT, -- Local file path in uploads/ directory
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
            """)

            # 5. Game / Cognitive Activity Sessions
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                session_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cognitive_domain TEXT NOT NULL, -- 'memory', 'attention', 'orientation', 'language'
                game_name TEXT NOT NULL,
                start_level INTEGER NOT NULL,
                end_level INTEGER NOT NULL,
                total_trials INTEGER NOT NULL,
                correct_trials INTEGER NOT NULL,
                accuracy_pct REAL NOT NULL,
                avg_response_time_sec REAL NOT NULL,
                fatigue_events INTEGER DEFAULT 0,
                caregiver_notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
            """)

            # 6. Granular Trial-by-Trial Telemetry
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                trial_number INTEGER NOT NULL,
                stimulus TEXT,
                target_response TEXT,
                user_response TEXT,
                is_correct INTEGER NOT NULL,
                response_time_sec REAL NOT NULL,
                difficulty_level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
            """)
            conn.commit()

    # --- Authentication & User Management ---
    def register_user(self, username: str, password: str, full_name: str, role: str = "caregiver",
                      email: str = "", phone: str = "") -> Optional[int]:
        """Registers a new user with hashed password. Returns user ID or None if username exists."""
        pwd_hash, salt = hash_password(password)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO users (username, password_hash, salt, full_name, role, email, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username.strip().lower(), pwd_hash, salt, full_name, role, email, phone))
                conn.commit()
                user_id = cursor.lastrowid
                self.log_audit(user_id, username, role, "REGISTER", f"Registered new {role} account: {full_name}")
                return user_id
            except sqlite3.IntegrityError:
                return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticates user credentials. Returns user dict on success, None on failure."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip().lower(),))
            row = cursor.fetchone()
            if not row:
                return None
            user = dict(row)
            test_hash, _ = hash_password(password, user["salt"])
            if test_hash == user["password_hash"]:
                self.log_audit(user["id"], user["username"], user["role"], "LOGIN", f"Successful login for {user['full_name']}")
                return user
            return None

    def get_all_users(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, role, email, phone, created_at FROM users ORDER BY id ASC")
            return [dict(r) for r in cursor.fetchall()]

    def get_all_caregivers(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, email, phone, created_at FROM users WHERE role = 'caregiver' ORDER BY id ASC")
            return [dict(r) for r in cursor.fetchall()]

    # --- Audit Logging ---
    def log_audit(self, user_id: Optional[int], username: str, role: str, action: str, details: str = ""):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO audit_logs (user_id, username, role, action, details)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, username, role, action, details))
                conn.commit()
        except Exception:
            pass

    def get_audit_logs(self, limit: int = 100) -> pd.DataFrame:
        with self._get_connection() as conn:
            query = "SELECT timestamp, username, role, action, details FROM audit_logs ORDER BY timestamp DESC LIMIT ?"
            return pd.read_sql_query(query, conn, params=(limit,))

    # --- Patient Management ---
    def get_all_patients(self, caregiver_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if caregiver_id:
                cursor.execute("SELECT * FROM patients WHERE caregiver_id = ? ORDER BY id ASC", (caregiver_id,))
            else:
                cursor.execute("SELECT * FROM patients ORDER BY id ASC")
            return [dict(row) for row in cursor.fetchall()]

    def get_patient(self, patient_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def add_patient(self, name: str, age: int, condition: str, baseline_mmse: float,
                    language_preference: str, caregiver_name: str, caregiver_contact: str = "",
                    notes: str = "", caregiver_id: Optional[int] = None) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO patients (caregiver_id, name, age, condition, baseline_mmse, language_preference, caregiver_name, caregiver_contact, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (caregiver_id, name, age, condition, baseline_mmse, language_preference, caregiver_name, caregiver_contact, notes))
            conn.commit()
            p_id = cursor.lastrowid
            self.log_audit(caregiver_id, caregiver_name, "caregiver", "ADD_PATIENT", f"Created patient record: {name}, Age: {age}")
            return p_id

    def update_patient_level(self, patient_id: int, new_level: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE patients SET current_adaptive_level = ? WHERE id = ?", (new_level, patient_id))
            conn.commit()

    # --- Memory Vault (with local image upload) ---
    def get_patient_memories(self, patient_id: int, category: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("""
                SELECT * FROM memories WHERE patient_id = ? AND category = ? AND is_active = 1
                ORDER BY id ASC
                """, (patient_id, category))
            else:
                cursor.execute("""
                SELECT * FROM memories WHERE patient_id = ? AND is_active = 1
                ORDER BY category, id ASC
                """, (patient_id,))
            return [dict(row) for row in cursor.fetchall()]

    def add_memory(self, patient_id: int, category: str, label_en: str, label_ta: str,
                   detail_en: str, detail_ta: str, image_path: str = "") -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO memories (patient_id, category, label_en, label_ta, detail_en, detail_ta, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, category, label_en, label_ta, detail_en, detail_ta, image_path))
            conn.commit()
            mem_id = cursor.lastrowid
            self.log_audit(None, "Caregiver", "caregiver", "UPLOAD_MEMORY", f"Added memory anchor: {label_en} ({category}) for patient ID {patient_id}")
            return mem_id

    def delete_memory(self, memory_id: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()

    # --- Session & Trial Logging ---
    def record_session(self, patient_id: int, cognitive_domain: str, game_name: str,
                       start_level: int, end_level: int, total_trials: int, correct_trials: int,
                       accuracy_pct: float, avg_response_time_sec: float,
                       fatigue_events: int = 0, caregiver_notes: str = "") -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO sessions (
                patient_id, cognitive_domain, game_name, start_level, end_level,
                total_trials, correct_trials, accuracy_pct, avg_response_time_sec,
                fatigue_events, caregiver_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id, cognitive_domain, game_name, start_level, end_level,
                total_trials, correct_trials, accuracy_pct, avg_response_time_sec,
                fatigue_events, caregiver_notes
            ))
            session_id = cursor.lastrowid
            cursor.execute("UPDATE patients SET current_adaptive_level = ? WHERE id = ?", (end_level, patient_id))
            conn.commit()
            self.log_audit(None, "Patient/Caregiver", "patient", "SESSION_COMPLETED", f"{game_name} ({cognitive_domain}) - Acc: {accuracy_pct}%, Level: {end_level}")
            return session_id

    def record_trial(self, session_id: int, patient_id: int, trial_number: int,
                     stimulus: str, target_response: str, user_response: str,
                     is_correct: bool, response_time_sec: float, difficulty_level: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO trials (
                session_id, patient_id, trial_number, stimulus, target_response,
                user_response, is_correct, response_time_sec, difficulty_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, patient_id, trial_number, stimulus, str(target_response),
                str(user_response), 1 if is_correct else 0, response_time_sec, difficulty_level
            ))
            conn.commit()

    # --- Analytics & Reporting ---
    def get_patient_session_history(self, patient_id: int) -> pd.DataFrame:
        with self._get_connection() as conn:
            query = """
            SELECT session_timestamp, cognitive_domain, game_name, start_level, end_level,
                   total_trials, correct_trials, accuracy_pct, avg_response_time_sec, fatigue_events
            FROM sessions
            WHERE patient_id = ?
            ORDER BY session_timestamp ASC
            """
            return pd.read_sql_query(query, conn, params=(patient_id,))

    def get_all_sessions_df(self) -> pd.DataFrame:
        with self._get_connection() as conn:
            query = """
            SELECT s.*, p.name as patient_name, p.condition, p.baseline_mmse, p.caregiver_name
            FROM sessions s
            JOIN patients p ON s.patient_id = p.id
            ORDER BY s.session_timestamp ASC
            """
            return pd.read_sql_query(query, conn)
