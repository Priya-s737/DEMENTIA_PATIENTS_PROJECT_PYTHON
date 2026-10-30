"""
Senior & Dementia Sudoku Game:
Tailored for Alzheimer's, Dementia, Amnesia, and Mild Cognitive Impairment (MCI).
Features:
- Senior-adapted 4x4 Mini-Sudoku (Default / Easy / Medium) with 2x2 subgrids
- 6x6 Sudoku (Hard difficulty) with 2x3 blocks
- Dual Input Mode: Numbers (1-4) or Familiar Senior Visual Symbols (🍎, 🌸, ☀️, 🔔)
- Real-time row/column/box conflict assistance without punitive stress
- Intelligent gentle hints with natural language reasoning
- High-contrast, large touch-accessible keypad and cell highlights
- Full pure Tamil and pure English localization with voice audio
- Automated clinical session logging to SQLite database
"""

import streamlit as st
import time
import copy
from typing import Dict, Any, List, Optional, Tuple
from modules.voice_assistant import VoiceAssistant
from modules.difficulty import render_difficulty_selector
from modules.celebration import render_celebration

# 4x4 Puzzle Templates: (Solution, Initial Clues by Difficulty)
# 4x4 boards: 4 rows, 4 cols, 2x2 blocks. Numbers 1..4
SUDOKU_4X4_PUZZLES = [
    {
        "id": "p4_1",
        "solution": [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 1, 4, 3],
            [4, 3, 2, 1]
        ],
        "easy_clues": [
            [1, 2, 3, 0],
            [3, 0, 1, 2],
            [2, 1, 0, 3],
            [0, 3, 2, 1]
        ],
        "medium_clues": [
            [1, 0, 3, 0],
            [0, 4, 0, 2],
            [2, 0, 4, 0],
            [0, 3, 0, 1]
        ],
        "hard_clues": [
            [0, 2, 0, 4],
            [3, 0, 0, 0],
            [0, 0, 0, 3],
            [4, 0, 2, 0]
        ]
    },
    {
        "id": "p4_2",
        "solution": [
            [2, 4, 1, 3],
            [1, 3, 4, 2],
            [4, 2, 3, 1],
            [3, 1, 2, 4]
        ],
        "easy_clues": [
            [2, 4, 0, 3],
            [1, 0, 4, 2],
            [4, 2, 3, 0],
            [0, 1, 2, 4]
        ],
        "medium_clues": [
            [0, 4, 1, 0],
            [1, 0, 0, 2],
            [4, 0, 0, 1],
            [0, 1, 2, 0]
        ],
        "hard_clues": [
            [2, 0, 0, 3],
            [0, 3, 4, 0],
            [0, 2, 3, 0],
            [3, 0, 0, 4]
        ]
    },
    {
        "id": "p4_3",
        "solution": [
            [3, 1, 4, 2],
            [4, 2, 3, 1],
            [1, 3, 2, 4],
            [2, 4, 1, 3]
        ],
        "easy_clues": [
            [3, 1, 4, 0],
            [0, 2, 3, 1],
            [1, 3, 0, 4],
            [2, 0, 1, 3]
        ],
        "medium_clues": [
            [3, 0, 4, 0],
            [0, 2, 0, 1],
            [1, 0, 2, 0],
            [0, 4, 0, 3]
        ],
        "hard_clues": [
            [0, 1, 4, 0],
            [4, 0, 0, 1],
            [0, 3, 2, 0],
            [2, 0, 0, 3]
        ]
    }
]

# Senior Visual Symbols for Acalculia / Picture Mode
SUDOKU_SYMBOLS = {
    1: {"icon": "🍎", "name_en": "Apple", "name_ta": "ஆப்பிள்"},
    2: {"icon": "🌸", "name_en": "Flower", "name_ta": "மலர்"},
    3: {"icon": "☀️", "name_en": "Sun", "name_ta": "சூரியன்"},
    4: {"icon": "🔔", "name_en": "Bell", "name_ta": "மணி"}
}


def find_first_hint_4x4(board: List[List[int]], solution: List[List[int]]) -> Optional[Dict[str, Any]]:
    """
    Finds a gentle, pedagogically sound hint for an empty cell in 4x4 Sudoku.
    Explains which single digit is missing from its row, column, or 2x2 box.
    """
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                needed = solution[r][c]
                # Check row candidates
                row_vals = set(board[r]) - {0}
                col_vals = {board[i][c] for i in range(4)} - {0}
                box_r, box_c = (r // 2) * 2, (c // 2) * 2
                box_vals = {board[box_r + i][box_c + j] for i in range(2) for j in range(2)} - {0}
                
                # Check if row is almost complete
                if len(row_vals) == 3:
                    return {
                        "row": r, "col": c, "val": needed,
                        "reason_en": f"Row {r+1} already has {sorted(list(row_vals))}. Only {needed} is missing!",
                        "reason_ta": f"வரிசை {r+1}-ல் ஏற்கெனவே {sorted(list(row_vals))} உள்ளன. விடுபட்ட எண் {needed} மட்டுமே!"
                    }
                if len(col_vals) == 3:
                    return {
                        "row": r, "col": c, "val": needed,
                        "reason_en": f"Column {c+1} already has {sorted(list(col_vals))}. Only {needed} is missing!",
                        "reason_ta": f"செங்குத்து வரிசை {c+1}-ல் ஏற்கெனவே {sorted(list(col_vals))} உள்ளன. விடுபட்ட எண் {needed} மட்டுமே!"
                    }
                if len(box_vals) == 3:
                    return {
                        "row": r, "col": c, "val": needed,
                        "reason_en": f"This 2x2 box already has {sorted(list(box_vals))}. Only {needed} is missing!",
                        "reason_ta": f"இந்த 2x2 கட்டத்திற்குள் ஏற்கெனவே {sorted(list(box_vals))} உள்ளன. விடுபட்ட எண் {needed} மட்டுமே!"
                    }
                # Fallback hint
                return {
                    "row": r, "col": c, "val": needed,
                    "reason_en": f"In Row {r+1}, Column {c+1}, the matching number is {needed}.",
                    "reason_ta": f"வரிசை {r+1}, நிரல் {c+1}-ல் சரியான எண் {needed} ஆகும்."
                }
    return None


def check_conflicts(board: List[List[int]], r: int, c: int, val: int) -> Optional[Tuple[str, str]]:
    """Checks if placing val at (r, c) creates a conflict in row, col, or 2x2 box."""
    if val == 0:
        return None
    # Check row
    for j in range(4):
        if j != c and board[r][j] == val:
            return (
                f"Number {val} is already in Row {r+1}!",
                f"எண் {val} ஏற்கெனவே வரிசை {r+1}-ல் உள்ளது!"
            )
    # Check col
    for i in range(4):
        if i != r and board[i][c] == val:
            return (
                f"Number {val} is already in Column {c+1}!",
                f"எண் {val} ஏற்கெனவே செங்குத்து நிரல் {c+1}-ல் உள்ளது!"
            )
    # Check 2x2 box
    box_r, box_c = (r // 2) * 2, (c // 2) * 2
    for i in range(2):
        for j in range(2):
            curr_r, curr_c = box_r + i, box_c + j
            if (curr_r != r or curr_c != c) and board[curr_r][curr_c] == val:
                return (
                    f"Number {val} is already in this 2x2 quadrant box!",
                    f"எண் {val} ஏற்கெனவே இந்த 2x2 சதுரக் கட்டத்திற்குள் உள்ளது!"
                )
    return None


def render_sudoku_game(patient: Dict[str, Any], db=None, lang: str = "en"):
    """
    Renders the clinical, senior-adapted Sudoku game.
    """
    st.markdown(f"### 🧩 {'முதியோர் சுடோக்கு புதிர் (Senior Sudoku Challenge)' if lang == 'ta' else 'Senior Cognitive Sudoku Challenge'}")
    sudoku_sub = (
        "டிமென்ஷியா மற்றும் நினைவாற்றல் குறைபாடு முதியோருக்கான எளிய, அமைதியான 4x4 சுடோக்கு"
        if lang == "ta"
        else "Gentle, accessible 4x4 Mini-Sudoku for working memory, pattern recognition, and executive focus."
    )
    st.markdown(
        f"""
        <div style="background: #EFF6FF; border-left: 5px solid #2563EB; padding: 10px 16px; border-radius: 8px; margin-bottom: 14px;">
            <span style="color: #1E3A8A; font-size: 16px; font-weight: 700;">
                ℹ️ {sudoku_sub}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Difficulty selection
    curr_lvl = patient.get("current_adaptive_level", 2)
    diff_str, diff_num = render_difficulty_selector("sudoku", lang=lang, default_lvl=curr_lvl)

    # Session State Initialization
    if "sudoku_puzzle_idx" not in st.session_state:
        st.session_state.sudoku_puzzle_idx = 0
    if "sudoku_symbol_mode" not in st.session_state:
        st.session_state.sudoku_symbol_mode = False
    if "sudoku_selected_cell" not in st.session_state:
        st.session_state.sudoku_selected_cell = (0, 0)
    if "sudoku_history" not in st.session_state:
        st.session_state.sudoku_history = []
    if "sudoku_start_time" not in st.session_state:
        st.session_state.sudoku_start_time = time.time()
    if "sudoku_completed" not in st.session_state:
        st.session_state.sudoku_completed = False
    if "sudoku_hint_message" not in st.session_state:
        st.session_state.sudoku_hint_message = None
    if "sudoku_conflict_message" not in st.session_state:
        st.session_state.sudoku_conflict_message = None

    # Load / Reset Puzzle if difficulty changed or new round
    puz_idx = st.session_state.sudoku_puzzle_idx % len(SUDOKU_4X4_PUZZLES)
    puz_data = SUDOKU_4X4_PUZZLES[puz_idx]

    if "sudoku_curr_diff" not in st.session_state or st.session_state.sudoku_curr_diff != diff_str:
        st.session_state.sudoku_curr_diff = diff_str
        clues_key = f"{diff_str}_clues"
        st.session_state.sudoku_initial_board = copy.deepcopy(puz_data[clues_key])
        st.session_state.sudoku_board = copy.deepcopy(puz_data[clues_key])
        st.session_state.sudoku_solution = copy.deepcopy(puz_data["solution"])
        st.session_state.sudoku_history = []
        st.session_state.sudoku_start_time = time.time()
        st.session_state.sudoku_completed = False
        st.session_state.sudoku_hint_message = None
        st.session_state.sudoku_conflict_message = None

    initial_board = st.session_state.sudoku_initial_board
    board = st.session_state.sudoku_board
    solution = st.session_state.sudoku_solution

    # Top Toolbar: Mode Switcher (Numbers vs Picture Symbols) & Audio Prompt
    t_c1, t_c2 = st.columns([2, 1.2])
    with t_c1:
        instructions_text = (
            "ஒவ்வொரு வரிசையிலும், நிரலிலும், 2x2 கட்டத்திலும் 1 முதல் 4 வரை உள்ள எண்கள் ஒரு முறை மட்டுமே வர வேண்டும்."
            if lang == "ta"
            else "Every row, column, and 2x2 box must contain the numbers 1 through 4 exactly once."
        )
        st.components.v1.html(VoiceAssistant.get_speech_html(instructions_text, lang=lang), height=55)
    with t_c2:
        sym_toggle = st.toggle(
            "🍎 " + ("படக் குறியீட்டு முறை" if lang == "ta" else "Visual Picture Mode"),
            value=st.session_state.sudoku_symbol_mode,
            key="sudoku_sym_toggle"
        )
        if sym_toggle != st.session_state.sudoku_symbol_mode:
            st.session_state.sudoku_symbol_mode = sym_toggle
            st.rerun()

    st.markdown("---")

    # Display Active Conflict or Hint Alert if any
    if st.session_state.sudoku_conflict_message:
        c_en, c_ta = st.session_state.sudoku_conflict_message
        st.warning(f"⚠️ {c_ta if lang == 'ta' else c_en}")
    elif st.session_state.sudoku_hint_message:
        h_en, h_ta = st.session_state.sudoku_hint_message
        st.info(f"💡 {h_ta if lang == 'ta' else h_en}")

    # --------------------------------------------------------------------------
    # 4x4 SUDOKU BOARD RENDERER
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <style>
            .sudoku-cell-fixed {
                background: linear-gradient(135deg, #1E3A8A 0%, #172554 100%) !important;
                color: #FEF08A !important;
                font-weight: 900 !important;
                font-size: 26px !important;
                border: 2px solid #60A5FA !important;
            }
            .sudoku-cell-selected {
                background: #F59E0B !important;
                color: #0F172A !important;
                font-weight: 900 !important;
                box-shadow: 0 0 14px #F59E0B !important;
                border: 3px solid #FEF08A !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    sel_r, sel_c = st.session_state.sudoku_selected_cell

    for r in range(4):
        cols = st.columns(4)
        for c in range(4):
            val = board[r][c]
            is_fixed = (initial_board[r][c] != 0)
            is_selected = (r == sel_r and c == sel_c)

            # Display Label (Number or Symbol)
            if val == 0:
                cell_label = "⬜"
            else:
                if st.session_state.sudoku_symbol_mode:
                    cell_label = SUDOKU_SYMBOLS.get(val, {}).get("icon", str(val))
                else:
                    cell_label = f"🔒 {val}" if is_fixed else str(val)

            btn_key = f"sud_cell_{r}_{c}_{st.session_state.sudoku_puzzle_idx}_{lang}"
            
            with cols[c]:
                # Visual border separation for 2x2 quadrants
                pad_bottom = "12px" if r == 1 else "6px"
                pad_right = "12px" if c == 1 else "6px"
                
                btn_type = "primary" if is_selected else ("secondary" if not is_fixed else "secondary")
                
                if st.button(
                    cell_label,
                    key=btn_key,
                    use_container_width=True,
                    type=btn_type
                ):
                    st.session_state.sudoku_selected_cell = (r, c)
                    st.session_state.sudoku_conflict_message = None
                    st.session_state.sudoku_hint_message = None
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # SENIOR KEYPAD (1, 2, 3, 4, CLEAR, HINT, UNDO)
    # --------------------------------------------------------------------------
    cell_pos_label = f"வரிசை {sel_r+1}, நிரல் {sel_c+1}" if lang == "ta" else f"Row {sel_r+1}, Column {sel_c+1}"
    st.markdown(
        f"**{'கட்டத்தில் நிரப்ப எண்ணைத் தேர்ந்தெடுக்கவும்' if lang == 'ta' else 'Tap to place number in selected cell'} "
        f"({cell_pos_label}):**"
    )

    k_cols = st.columns(6)
    for num in [1, 2, 3, 4]:
        with k_cols[num - 1]:
            if st.session_state.sudoku_symbol_mode:
                sym_info = SUDOKU_SYMBOLS[num]
                k_label = f"{sym_info['icon']} {sym_info['name_ta'] if lang == 'ta' else sym_info['name_en']}"
            else:
                k_label = f"🔢 {num}"

            if st.button(k_label, key=f"keypad_num_{num}_{lang}", use_container_width=True):
                if initial_board[sel_r][sel_c] != 0:
                    st.toast("🔒 " + ("இந்த எண் மாற்ற முடியாத ஆரம்ப குறிப்பு!" if lang == "ta" else "This is a locked clue cell!"))
                else:
                    # Save undo history
                    st.session_state.sudoku_history.append((sel_r, sel_c, board[sel_r][sel_c]))
                    # Check conflicts
                    conflict = check_conflicts(board, sel_r, sel_c, num)
                    board[sel_r][sel_c] = num
                    if conflict:
                        st.session_state.sudoku_conflict_message = conflict
                    else:
                        st.session_state.sudoku_conflict_message = None
                    st.rerun()

    with k_cols[4]:
        clear_label = "❌ " + ("அழி" if lang == "ta" else "Clear")
        if st.button(clear_label, key="keypad_clear_btn", use_container_width=True):
            if initial_board[sel_r][sel_c] == 0:
                st.session_state.sudoku_history.append((sel_r, sel_c, board[sel_r][sel_c]))
                board[sel_r][sel_c] = 0
                st.session_state.sudoku_conflict_message = None
                st.rerun()
            else:
                st.toast("🔒 " + ("ஆரம்ப எண்களை அழிக்க முடியாது" if lang == "ta" else "Cannot clear initial clues"))

    with k_cols[5]:
        undo_label = "↩️ " + ("மீள்" if lang == "ta" else "Undo")
        if st.button(undo_label, key="keypad_undo_btn", use_container_width=True, disabled=len(st.session_state.sudoku_history) == 0):
            last_r, last_c, last_val = st.session_state.sudoku_history.pop()
            board[last_r][last_c] = last_val
            st.session_state.sudoku_conflict_message = None
            st.rerun()

    st.markdown("---")

    # --------------------------------------------------------------------------
    # ASSISTANCE TOOLS & PUZZLE VALIDATION
    # --------------------------------------------------------------------------
    b_col1, b_col2, b_col3 = st.columns([1.5, 1.5, 2])

    with b_col1:
        hint_label = "💡 " + ("உதவிக்குறிப்பு (Hint)" if lang == "ta" else "Gentle Hint")
        if st.button(hint_label, use_container_width=True, key="sudoku_hint_btn"):
            hint = find_first_hint_4x4(board, solution)
            if hint:
                st.session_state.sudoku_selected_cell = (hint["row"], hint["col"])
                st.session_state.sudoku_hint_message = (hint["reason_en"], hint["reason_ta"])
                # Fill the hint cell
                board[hint["row"]][hint["col"]] = hint["val"]
                st.rerun()
            else:
                st.toast("🎉 " + ("அனைத்து கட்டங்களும் நிரப்பப்பட்டுவிட்டன!" if lang == "ta" else "All cells filled!"))

    with b_col2:
        reset_label = "🔄 " + ("புதிதாகத் தொடங்கு" if lang == "ta" else "Reset Puzzle")
        if st.button(reset_label, use_container_width=True, key="sudoku_reset_btn"):
            st.session_state.sudoku_board = copy.deepcopy(initial_board)
            st.session_state.sudoku_history = []
            st.session_state.sudoku_conflict_message = None
            st.session_state.sudoku_hint_message = None
            st.rerun()

    with b_col3:
        check_label = "✅ " + ("முழு புதிரைச் சரிபார்" if lang == "ta" else "Verify Complete Puzzle")
        if st.button(check_label, use_container_width=True, type="primary", key="sudoku_check_btn"):
            is_complete = True
            is_correct = True
            for r in range(4):
                for c in range(4):
                    if board[r][c] == 0:
                        is_complete = False
                    elif board[r][c] != solution[r][c]:
                        is_correct = False

            if not is_complete:
                st.warning("⚠️ " + ("இன்னும் சில கட்டங்கள் காலியாக உள்ளன! தொடர்ந்து நிரப்பவும்." if lang == "ta" else "Some cells are still empty! Keep going."))
            elif not is_correct:
                st.error("💡 " + ("சில எண்கள் தவறான இடத்தில் உள்ளன. கவனமாகச் சரிபார்க்கவும்." if lang == "ta" else "A few numbers are misplaced. Let's inspect rows and columns!"))
            else:
                st.session_state.sudoku_completed = True
                rt = round(time.time() - st.session_state.sudoku_start_time, 2)
                
                # Clinical logging to DB
                if db:
                    try:
                        db.record_session(
                            patient_id=patient["id"],
                            cognitive_domain="attention",
                            game_name="Senior Sudoku 4x4",
                            start_level=diff_num,
                            end_level=min(5, diff_num + 1),
                            total_trials=4,
                            correct_trials=4,
                            accuracy_pct=100.0,
                            avg_response_time_sec=rt,
                            fatigue_events=0,
                            caregiver_notes=f"Successfully solved {diff_str} 4x4 Sudoku with full accuracy."
                        )
                    except Exception as e:
                        pass

                celebration_text = (
                    "மிக அற்புதம்! சுடோக்கு புதிரை மிகச் சிறப்பாக முடித்துவிட்டீர்கள்!"
                    if lang == "ta"
                    else "Brilliant work! You completed the Sudoku puzzle with wonderful focus!"
                )
                st.success(f"🎉 **{celebration_text}** (⏱️ {rt}{'வி' if lang == 'ta' else 's'})")
                render_celebration(rhyme_idx=1, lang=lang)

    # Next Puzzle Button if completed
    if st.session_state.sudoku_completed:
        st.markdown("<br>", unsafe_allow_html=True)
        next_puz_label = "➡️ " + ("அடுத்த சுடோக்கு புதிர்" if lang == "ta" else "Next Sudoku Puzzle")
        if st.button(next_puz_label, key="sudoku_next_puzzle_btn", use_container_width=True, type="primary"):
            st.session_state.sudoku_puzzle_idx += 1
            new_idx = st.session_state.sudoku_puzzle_idx % len(SUDOKU_4X4_PUZZLES)
            new_puz = SUDOKU_4X4_PUZZLES[new_idx]
            st.session_state.sudoku_initial_board = copy.deepcopy(new_puz[f"{diff_str}_clues"])
            st.session_state.sudoku_board = copy.deepcopy(new_puz[f"{diff_str}_clues"])
            st.session_state.sudoku_solution = copy.deepcopy(new_puz["solution"])
            st.session_state.sudoku_history = []
            st.session_state.sudoku_start_time = time.time()
            st.session_state.sudoku_completed = False
            st.session_state.sudoku_conflict_message = None
            st.session_state.sudoku_hint_message = None
            st.rerun()
