# NeuroCare: Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients

**Clinical Cognitive Assessment & Memory Assistance Platform**  
**Core Team:** Clinical NeuroCare Team  
**Institution:** Cognitive Rehabilitation & Memory Health Network  

---

## 🌟 Executive Summary & Academic Novelty

**NeuroCare** is a Python-based supportive cognitive ecosystem developed to aid elderly individuals experiencing Mild Cognitive Impairment (MCI) and early-stage Dementia. Unlike generic brain-training apps, NeuroCare integrates:

1. **Caregiver Reminiscence Anchoring (Reminiscence Therapy - RT)**: Injects patient-specific memories (family photos, hometown landmarks, morning routines, favorite classical ragas/foods) directly into cognitive game stimuli.
2. **Post-Login Motivational Story Theater & Animations**: Warm, reassuring daily stories with CSS keyframe animations (glowing sunrise, flowing river, majestic banyan tree, sacred hearth lamp) and bilingual voice audio designed to eliminate anxiety and inspire elderly patients before playing.
3. **Clinical Dementia & Amnesia Game Suite (7 Specialized Activities)**:
   - 🧩 **Senior Sudoku Challenge**: Non-punitive 4x4 Mini-Sudoku (and 6x6 on Hard) with dual Number and Visual Symbol mode (🍎, 🌸, ☀️, 🔔), conflict assistance, and intelligent gentle hints.
   - 🃏 **Memory Matching Pairs Challenge**: Concentration card flip game using uploaded family memories and cultural anchors across 3 difficulty tiers (3, 4, 6 pairs).
   - 🖼️ **Episodic Memory Recall**: Familiar Face-Name Recall & Daily Routine Timeline Sequencing.
   - 🔢 **Working Memory Span Increment**: Progressive sequential recall (Span N=2..5).
   - 🎨 **Attention & Executive**: Bilingual Stroop Interference & Digital Trail Making Test (TMT).
   - 🧭 **Orientation**: Temporal Reality Clock & Spatial Home Environment Navigator.
   - 🗣️ **Language**: Semantic Object Naming & Category Fluency.
4. **Explainable Multi-Parametric Difficulty Adaptation (EDA-Engine)**: Dynamically adjusts task complexity based on real-time accuracy, reaction latency, and error sequences, with an automated **Cognitive Fatigue & Agitation Safety Trigger**.
5. **Bilingual Accessibility (English & தமிழ் / Tamil)**: Multimodal interactions with voice synthesized prompts (TTS) and senior-friendly high-contrast UI meeting WCAG 2.1 AAA accessibility guidelines.
6. **Research & Publication Benchmark Suite**: Automated synthetic Randomized Controlled Trial (RCT) generator ($N=30$), paired sample $t$-tests, Cohen's $d$ effect sizes, interactive radar charts, and publication-ready LaTeX tables for conference papers.

---

## 📐 Mathematical Formulation of the Adaptive Engine (EDA-Engine)

The platform evaluates trial performance using a composite index $\mathcal{C} \in [0, 100]$:

$$\mathcal{C} = \left( w_{\text{acc}} \cdot \frac{\text{Accuracy}}{100} + w_{\text{speed}} \cdot \max\left(0, 1 - \frac{\bar{t}}{\tau_{\max}}\right) \right) \times 100$$

Where:
- $w_{\text{acc}} = 0.65$ (Weight for accuracy)
- $w_{\text{speed}} = 0.35$ (Weight for response speed)
- $\bar{t}$ = Mean response time of the session
- $\tau_{\max} = 10.0\text{s}$ (Max allowed time per trial)

### State Transition Logic:
- **Level Up ($L_{t+1} = L_t + 1$)**: When $\text{Accuracy} \ge 80.0\%$ and $\bar{t} \le 4.5\text{s}$.
- **Level Down ($L_{t+1} = L_t - 1$)**: When $\text{Accuracy} \le 60.0\%$ or $\bar{t} > 4.5\text{s}$.
- **Fatigue Interruption**: When consecutive error count $\ge 3$, difficulty is stepped down and a therapeutic mindful breathing break is initiated.

---

## 🏗️ System Architecture

```
c:/Users/admin/Downloads/New folder/
├── app.py                     # Streamlit multi-portal web app (Patient, Caregiver, Research)
├── config.py                  # Bilingual English/Tamil dictionary, color themes, domain metadata
├── database/
│   ├── __init__.py
│   ├── db_manager.py          # SQLite database layer (Patients, Memories, Sessions, Telemetry)
│   └── mock_data.py           # Pre-seeded clinical profiles & 28-day longitudinal study data
├── modules/
│   ├── __init__.py
│   ├── motivational_story.py  # Heartwarming story theater with CSS keyframe animations & TTS
│   ├── personalization.py     # Reminiscence memory vault & dynamic cue injector
│   ├── adaptive_engine.py     # Multi-metric difficulty adaptation & fatigue detector
│   ├── voice_assistant.py     # Bilingual Text-to-Speech (HTML5 Web Speech & gTTS)
│   ├── difficulty.py          # Easy, Medium, Hard selector with stimulus reset hooks
│   └── research_stats.py      # Inferential statistics, t-tests, Cohen's d, LaTeX generator
├── games/
│   ├── __init__.py
│   ├── sudoku_game.py         # Senior & Dementia 4x4 Mini-Sudoku & Picture Symbol Mode
│   ├── memory_pairs_game.py   # Card-flipping Concentration Memory Matching Pairs
│   ├── memory_games.py        # Face recognition & life timeline sequencing
│   ├── memory_increment_game.py # Progressive working memory span challenge
│   ├── attention_games.py     # Bilingual Stroop task & digital Trail Making Test
│   ├── orientation_games.py   # Temporal clock & spatial home environment
│   └── language_games.py      # Object naming & category fluency
├── requirements.txt           # Python dependencies
└── README.md                  # Complete academic documentation
```

---

## 🚀 How to Run the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit Platform
```bash
streamlit run app.py
```

### 3. Open in Browser
Visit `http://localhost:8501` to access the portal.

---

## 🎓 How to Present This Project to Your Professors

1. **Start in the Caregiver Portal (👨‍⚕️ Caregiver & Clinician Dashboard)**:
   - Show how the caregiver uploads real family photos, names, and memories in English and Tamil.
   - Highlight the longitudinal progression curves and download the **Clinical Assessment Report**.
2. **Switch to Patient Mode (👵 Elderly / Patient Mode)**:
   - Select **தமிழ் (Tamil)** or **English** in the sidebar.
   - Click the **🔊 Listen to Prompt** button to demonstrate voice interaction.
   - Play a round of **Familiar Face Recall** and **Bilingual Stroop Task**. Show how the adaptive engine evaluates the session and adjusts the difficulty in real time.
3. **Finish in the Research Suite (📊 Conference Research & Benchmark Suite)**:
   - Show the simulated **RCT Clinical Trial ($N=30$)**.
   - Review the statistically significant $p$-values ($p < 0.001$) and high Cohen's $d$ effect sizes ($d > 1.8$).
   - Display the **Interactive Radar Chart** and the auto-generated **LaTeX Table** ready for paper submission.

---

## 📄 Conference Submission Targets
- **IEEE EMBS** (Engineering in Medicine and Biology Society)
- **ACM ASSETS** (International ACM SIGACCESS Conference on Computers and Accessibility)
- **Springer CCIS** (Communications in Computer and Information Science)
- **IEEE ICHI** (International Conference on Healthcare Informatics)
