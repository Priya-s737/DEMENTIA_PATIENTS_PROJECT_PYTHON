/**
 * NeuroCare Senior Cognitive Games Suite - Real Game-Feel Edition
 * Transforms cognitive assessments into vibrant, rewarding, engaging brain-training games!
 * Features:
 * - Real-Time Web Audio API Sound Synthesizer (Taps, Flips, Chimes, Fanfares)
 * - Canvas Confetti & Golden Star Burst Cannon
 * - Game HUD with Live Score, Combo Streaks, Reaction Timers & Level Progress
 * - Micro-Animations: Green Glows, Floating +100 PTS, Shakes (NO ALERT BOXES!)
 * - In-Game Dignified Adult Celebration Stage matching celebration.py
 * - All 7 Specialized Games Fully Interactive
 */

// ==============================================================================
// 1. WEB AUDIO API SOUND SYNTHESIZER
// ==============================================================================
const SoundFX = {
  ctx: null,

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  },

  tap() {
    this.init();
    if (!this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(540, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(180, this.ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.06);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.06);
    } catch (e) {}
  },

  flip() {
    this.init();
    if (!this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(280, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(620, this.ctx.currentTime + 0.09);
      gain.gain.setValueAtTime(0.14, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.1);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.1);
    } catch (e) {}
  },

  correct() {
    this.init();
    if (!this.ctx) return;
    try {
      // Ascending major chime C5 (523), E5 (659), G5 (784)
      [523.25, 659.25, 783.99].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.07);
        gain.gain.setValueAtTime(0, this.ctx.currentTime + idx * 0.07);
        gain.gain.linearRampToValueAtTime(0.22, this.ctx.currentTime + idx * 0.07 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + idx * 0.07 + 0.38);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime + idx * 0.07);
        osc.stop(this.ctx.currentTime + idx * 0.07 + 0.4);
      });
    } catch (e) {}
  },

  wrong() {
    this.init();
    if (!this.ctx) return;
    try {
      // Gentle warm low double-thump (never harsh or abrasive)
      [220, 180].forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.1);
        gain.gain.setValueAtTime(0.12, this.ctx.currentTime + idx * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + idx * 0.1 + 0.18);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime + idx * 0.1);
        osc.stop(this.ctx.currentTime + idx * 0.1 + 0.2);
      });
    } catch (e) {}
  },

  fanfare() {
    this.init();
    if (!this.ctx) return;
    try {
      // Radiant C Major 9 harmonic chord matching celebration.py
      const freqs = [261.63, 329.63, 392.00, 493.88, 587.33, 783.99];
      freqs.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + i * 0.09);
        gain.gain.setValueAtTime(0, this.ctx.currentTime + i * 0.09);
        gain.gain.linearRampToValueAtTime(0.24, this.ctx.currentTime + i * 0.09 + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0005, this.ctx.currentTime + i * 0.09 + 1.8);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime + i * 0.09);
        osc.stop(this.ctx.currentTime + i * 0.09 + 1.9);
      });
    } catch (e) {}
  }
};


// ==============================================================================
// 2. CANVAS CONFETTI & GOLDEN STAR CANNON
// ==============================================================================
const ConfettiFX = {
  particles: [],
  animId: null,

  launch(durationMs = 2600) {
    const canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext('2d');
    const colors = ['#E5A823', '#FEF08A', '#10B981', '#3B82F6', '#EC4899', '#8B5CF6'];

    this.particles = [];
    for (let i = 0; i < 95; i++) {
      this.particles.push({
        x: canvas.width * 0.5 + (Math.random() - 0.5) * 220,
        y: canvas.height * 0.65,
        vx: (Math.random() - 0.5) * 18,
        vy: -Math.random() * 19 - 8,
        size: Math.random() * 9 + 6,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        vRot: (Math.random() - 0.5) * 14,
        alpha: 1
      });
    }

    const startTime = Date.now();
    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      this.particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.55; // gravity
        p.rotation += p.vRot;
        p.alpha = Math.max(0, 1 - (Date.now() - startTime) / durationMs);

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.4);
        ctx.restore();
      });

      if (Date.now() - startTime < durationMs) {
        this.animId = requestAnimationFrame(render);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    };
    if (this.animId) cancelAnimationFrame(this.animId);
    this.animId = requestAnimationFrame(render);
  }
};


// Floating Points Helper (e.g. +100 PTS)
function showFloatingPoints(parentEl, text = '+100 XP') {
  if (!parentEl) return;
  const wrap = document.createElement('div');
  wrap.className = 'floating-points-wrap';
  wrap.innerHTML = `<div class="floating-points">${text}</div>`;
  parentEl.prepend(wrap);
  setTimeout(() => wrap.remove(), 1200);
}

// In-Game Dignified Celebration Stage Modal (Zero alert boxes!)
function renderInGameCelebration(container, { motif, title, text, badge, onNext, lang = 'ta' }) {
  SoundFX.fanfare();
  ConfettiFX.launch();

  const nextLabel = (lang === 'ta')
    ? '🌟 அடுத்த நிலைக்குத் தொடரலாம் (Next Challenge) ⏭️'
    : '🌟 Continue to Next Challenge ⏭️';

  const defaultBadge = (lang === 'ta') ? '✨ கூர்மையான கவனம்' : '✨ Sharp Focus';
  const defaultTitle = (lang === 'ta') ? 'சிறப்பான சாதனை!' : 'Splendid Achievement!';
  const defaultText = (lang === 'ta') ? 'அனுபவமும் கூர்மையான கவனமும் என்றும் நிலைத்திருக்கும் சிறந்த பலம்.' : 'Outstanding cognitive focus and sharp attention shine through!';

  const stageHtml = `
    <div class="game-celebration-stage">
      <div class="celebration-emblem">${motif || '🌟'}</div>
      <div class="celebration-badge">${badge || defaultBadge}</div>
      <div class="celebration-title">${title || defaultTitle}</div>
      <div class="celebration-text">“${text || defaultText}”</div>
      <button class="btn-celebration-next btn-game-press" id="btnNextChallenge">
        ${nextLabel}
      </button>
    </div>
  `;
  container.innerHTML = stageHtml;

  const btn = container.querySelector('#btnNextChallenge');
  if (btn && onNext) {
    btn.onclick = () => {
      SoundFX.tap();
      onNext();
    };
  }
}

// Global Telemetry Recorder
async function recordGameTelemetry(gameKey, score, accuracy, responseTimeMs, domain = 'memory') {
  try {
    const patientId = window.activePatientId || 1;
    await fetch('/api/sessions/record', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_id: patientId,
        game_key: gameKey,
        level: 3,
        score: score,
        accuracy: accuracy,
        response_time_ms: responseTimeMs,
        cognitive_domain: domain
      })
    });
  } catch (e) {}
}


// ==============================================================================
// 1. SENIOR 4x4 SUDOKU GAME - 3D VIDEO GAME CONSOLE
// ==============================================================================
class SudokuGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.mode = 'symbols'; // 'symbols' or 'numbers'
    this.difficulty = 'easy'; // 'easy', 'medium', 'hard'

    this.symbolMap = {
      1: { icon: '🍎', name_en: 'Apple', name_ta: 'ஆப்பிள்' },
      2: { icon: '🌸', name_en: 'Lotus', name_ta: 'மலர்' },
      3: { icon: '☀️', name_en: 'Sun', name_ta: 'சூரியன்' },
      4: { icon: '🔔', name_en: 'Bell', name_ta: 'மணி' }
    };

    this.puzzles = [
      {
        id: 'p4_1',
        solution: [
          [1, 2, 3, 4],
          [3, 4, 1, 2],
          [2, 1, 4, 3],
          [4, 3, 2, 1]
        ],
        easy_clues: [
          [1, 2, 3, 0],
          [3, 0, 1, 2],
          [2, 1, 0, 3],
          [0, 3, 2, 1]
        ],
        medium_clues: [
          [1, 0, 3, 0],
          [0, 4, 0, 2],
          [2, 0, 4, 0],
          [0, 3, 0, 1]
        ],
        hard_clues: [
          [0, 2, 0, 4],
          [3, 0, 0, 0],
          [0, 0, 0, 3],
          [4, 0, 2, 0]
        ]
      },
      {
        id: 'p4_2',
        solution: [
          [2, 4, 1, 3],
          [1, 3, 4, 2],
          [4, 2, 3, 1],
          [3, 1, 2, 4]
        ],
        easy_clues: [
          [2, 4, 0, 3],
          [1, 0, 4, 2],
          [4, 2, 3, 0],
          [0, 1, 2, 4]
        ],
        medium_clues: [
          [0, 4, 1, 0],
          [1, 0, 0, 2],
          [4, 0, 0, 1],
          [0, 1, 2, 0]
        ],
        hard_clues: [
          [2, 0, 0, 3],
          [0, 3, 4, 0],
          [0, 2, 3, 0],
          [3, 0, 0, 4]
        ]
      },
      {
        id: 'p4_3',
        solution: [
          [3, 1, 4, 2],
          [4, 2, 3, 1],
          [1, 3, 2, 4],
          [2, 4, 1, 3]
        ],
        easy_clues: [
          [3, 1, 4, 0],
          [0, 2, 3, 1],
          [1, 3, 0, 4],
          [2, 0, 1, 3]
        ],
        medium_clues: [
          [3, 0, 4, 0],
          [0, 2, 0, 1],
          [1, 0, 2, 0],
          [0, 4, 0, 3]
        ],
        hard_clues: [
          [0, 1, 4, 0],
          [4, 0, 0, 1],
          [0, 3, 2, 0],
          [2, 0, 0, 3]
        ]
      }
    ];

    this.currentPuzzleIdx = 0;
    this.board = [];
    this.givenMask = [];
    this.selectedCell = null;
    this.history = [];
    this.conflicts = [];
    this.lives = 3;
    this.score = 300;
    this.startTime = Date.now();
    this.timerInterval = null;
    this.elapsedSeconds = 0;

    this.initPuzzle(0, 'easy');
  }

  initPuzzle(idx = 0, diff = 'easy') {
    this.currentPuzzleIdx = idx;
    this.difficulty = diff;
    const puz = this.puzzles[idx % this.puzzles.length];
    this.solution = puz.solution;

    const cluesKey = `${diff}_clues`;
    const initial = puz[cluesKey] || puz.easy_clues;

    this.board = initial.map(row => [...row]);
    this.givenMask = initial.map(row => row.map(v => v !== 0));
    this.selectedCell = null;
    this.history = [];
    this.conflicts = [];
    this.lives = 3;
    this.startTime = Date.now();
    this.elapsedSeconds = 0;

    if (this.timerInterval) clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds++;
      const el = document.getElementById('sudokuTimerDisplay');
      if (el) {
        const m = Math.floor(this.elapsedSeconds / 60);
        const s = this.elapsedSeconds % 60;
        el.innerText = `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
      }
    }, 1000);

    this.render();
  }

  setDifficulty(diff) {
    SoundFX.tap();
    this.initPuzzle(this.currentPuzzleIdx, diff);
  }

  setMode(mode) {
    SoundFX.tap();
    this.mode = mode;
    this.render();
  }

  selectCell(r, c) {
    SoundFX.tap();
    this.selectedCell = [r, c];
    this.render();
  }

  inputNumber(val) {
    if (!this.selectedCell) return;
    const [r, c] = this.selectedCell;
    if (this.givenMask[r][c]) return;

    // Check if correct against solution
    const expected = this.solution[r][c];
    if (val !== expected) {
      // Wrong move - lose a heart
      SoundFX.wrong();
      this.lives = Math.max(0, this.lives - 1);
      this.conflicts.push(`${r}-${c}`);
      this.render();

      setTimeout(() => {
        this.conflicts = [];
        this.render();
      }, 500);

      if (this.lives === 0) {
        showFloatingPoints(this.container, this.lang === 'ta' ? '🔄 3 வாய்ப்புகள் முடிந்தது! மீண்டும் தொடங்குவோம்.' : '🔄 3 chances used! Restarting with fresh focus...');
        setTimeout(() => {
          this.initPuzzle(this.currentPuzzleIdx, this.difficulty);
        }, 900);
      }
      return;
    }

    // Correct move!
    SoundFX.correct();
    this.history.push([r, c, this.board[r][c]]);
    this.board[r][c] = val;
    this.score += 50;
    showFloatingPoints(this.container, '+50 PTS! ✨');

    this.checkConflicts();
    this.render();
    this.checkWin();
  }

  clearCell() {
    SoundFX.tap();
    if (!this.selectedCell) return;
    const [r, c] = this.selectedCell;
    if (this.givenMask[r][c]) return;

    this.history.push([r, c, this.board[r][c]]);
    this.board[r][c] = 0;
    this.checkConflicts();
    this.render();
  }

  undo() {
    SoundFX.tap();
    if (this.history.length === 0) return;
    const [r, c, prevVal] = this.history.pop();
    this.board[r][c] = prevVal;
    this.checkConflicts();
    this.render();
  }

  giveHint() {
    SoundFX.correct();
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        if (this.board[r][c] === 0 || this.board[r][c] !== this.solution[r][c]) {
          this.board[r][c] = this.solution[r][c];
          this.selectedCell = [r, c];
          this.score = Math.max(0, this.score - 20);
          this.checkConflicts();
          this.render();
          this.checkWin();
          return;
        }
      }
    }
  }

  checkConflicts() {
    this.conflicts = [];
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const val = this.board[r][c];
        if (val === 0) continue;
        for (let oc = 0; oc < 4; oc++) {
          if (oc !== c && this.board[r][oc] === val) this.conflicts.push(`${r}-${c}`);
        }
        for (let or_ = 0; or_ < 4; or_++) {
          if (or_ !== r && this.board[or_][c] === val) this.conflicts.push(`${r}-${c}`);
        }
      }
    }
  }

  checkWin() {
    let fullAndCorrect = true;
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        if (this.board[r][c] !== this.solution[r][c]) fullAndCorrect = false;
      }
    }
    if (fullAndCorrect) {
      if (this.timerInterval) clearInterval(this.timerInterval);
      const rt = Date.now() - this.startTime;
      recordGameTelemetry('sudoku_4x4', 100, 1.0, rt, 'executive');

      renderInGameCelebration(this.container, {
        motif: '🧩',
        badge: this.lang === 'ta' ? '✨ நேர்த்தியான தீர்வு' : '✨ Flawless Logic',
        title: this.lang === 'ta' ? 'சுடோக்கு புதிர் வெற்றி!' : 'Sudoku Console Mastered!',
        text: this.lang === 'ta'
          ? 'நேர்த்தியான முடிவு! நிதானமான சிந்தனையும் தெளிவான பகுப்பாய்வுத் திறனும் உங்கள் தனிச்சிறப்பு. அடுத்த புதிருக்குத் தொடரலாம்!'
          : 'Masterful precision! Calm deliberation and clear logical reasoning completed the 4x4 quadrants.',
        lang: this.lang,
        onNext: () => this.initPuzzle(this.currentPuzzleIdx + 1, this.difficulty)
      });
    }
  }

  render() {
    if (!this.container) return;

    const selR = this.selectedCell ? this.selectedCell[0] : -1;
    const selC = this.selectedCell ? this.selectedCell[1] : -1;
    const selectedVal = (selR !== -1 && selC !== -1) ? this.board[selR][selC] : 0;

    // Remaining counts for keypad
    const counts = { 1: 0, 2: 0, 3: 0, 4: 0 };
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const v = this.board[r][c];
        if (v >= 1 && v <= 4) counts[v]++;
      }
    }

    // Top Console Status Bar (Hearts, Score, Timer)
    const m = Math.floor(this.elapsedSeconds / 60);
    const s = this.elapsedSeconds % 60;
    const timeFormatted = `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;

    let heartsHtml = '';
    for (let h = 0; h < 3; h++) {
      heartsHtml += `<span class="sudoku-heart ${h < this.lives ? '' : 'lost'}">❤️</span>`;
    }

    const consoleTop = `
      <div class="sudoku-game-console">
        <div class="sudoku-top-stats">
          <div class="sudoku-hearts-wrap" title="3 Lives Remaining">
            ${heartsHtml}
          </div>
          <div class="sudoku-score-badge">
            🏆 <span>${this.score} PTS</span>
          </div>
          <div class="sudoku-timer-badge">
            ⏱️ <span id="sudokuTimerDisplay">${timeFormatted}</span>
          </div>
        </div>

        <!-- Difficulty Pills & Mode Switcher -->
        <div class="sudoku-subnav-row">
          <div class="sudoku-diff-pills">
            <button class="btn-diff-pill ${this.difficulty === 'easy' ? 'active' : ''}" onclick="sudokuInstance.setDifficulty('easy')">
              🌱 ${this.lang === 'ta' ? 'எளிது' : 'Easy'}
            </button>
            <button class="btn-diff-pill ${this.difficulty === 'medium' ? 'active' : ''}" onclick="sudokuInstance.setDifficulty('medium')">
              ⚡ ${this.lang === 'ta' ? 'நடுத்தரம்' : 'Medium'}
            </button>
            <button class="btn-diff-pill ${this.difficulty === 'hard' ? 'active' : ''}" onclick="sudokuInstance.setDifficulty('hard')">
              🔥 ${this.lang === 'ta' ? 'கடினம்' : 'Hard'}
            </button>
          </div>

          <button class="sudoku-mode-toggle btn-game-press" onclick="sudokuInstance.setMode('${this.mode === 'symbols' ? 'numbers' : 'symbols'}')">
            ${this.mode === 'symbols' ? '🔢 ' + (this.lang === 'ta' ? 'எண்கள் முறை' : 'Numbers Mode') : '🍎 ' + (this.lang === 'ta' ? 'படக் குறியீடு முறை' : 'Picture Symbols')}
          </button>
        </div>

        <!-- 4 Distinct 2x2 Quadrant Blocks (NOT a flat table!) -->
        <div class="sudoku-quadrants-container">
    `;

    // Render the 4 Quadrant Blocks:
    // Block 0: rows 0..1, cols 0..1
    // Block 1: rows 0..1, cols 2..3
    // Block 2: rows 2..3, cols 0..1
    // Block 3: rows 2..3, cols 2..3
    const quadrants = [
      [[0, 0], [0, 1], [1, 0], [1, 1]],
      [[0, 2], [0, 3], [1, 2], [1, 3]],
      [[2, 0], [2, 1], [3, 0], [3, 1]],
      [[2, 2], [2, 3], [3, 2], [3, 3]]
    ];

    let quadrantsHtml = '';
    quadrants.forEach((quad) => {
      quadrantsHtml += '<div class="sudoku-quadrant-block">';
      quad.forEach(([r, c]) => {
        const val = this.board[r][c];
        const isGiven = this.givenMask[r][c];
        const isSelected = (r === selR && c === selC);
        const hasConflict = this.conflicts.includes(`${r}-${c}`);
        const isCrosshair = (!isSelected && (r === selR || c === selC));
        const isMatch = (selectedVal !== 0 && val === selectedVal && !isSelected);

        let tileClasses = 'sudoku-tile-3d';
        if (isGiven) tileClasses += ' fixed';
        else tileClasses += ' player';

        if (isSelected) tileClasses += ' selected';
        else if (isCrosshair) tileClasses += ' crosshair';

        if (isMatch) tileClasses += ' match-aura';
        if (hasConflict) tileClasses += ' conflict';

        let displayContent = '';
        if (val !== 0) {
          if (this.mode === 'symbols') {
            displayContent = this.symbolMap[val].icon;
          } else {
            displayContent = val;
          }
        }

        quadrantsHtml += `
          <div class="${tileClasses}" onclick="sudokuInstance.selectCell(${r}, ${c})">
            ${displayContent}
          </div>
        `;
      });
      quadrantsHtml += '</div>';
    });

    // Arcade Number / Symbol Gamepad
    let gamepadHtml = '<div class="sudoku-gamepad-grid">';
    for (let n = 1; n <= 4; n++) {
      const remaining = 4 - counts[n];
      const isComplete = (remaining <= 0);
      const icon = this.symbolMap[n].icon;
      const label = (this.mode === 'symbols') ? icon : n;
      const subLabel = isComplete
        ? '✅'
        : `${remaining} ${this.lang === 'ta' ? 'மீதம்' : 'left'}`;

      gamepadHtml += `
        <button class="btn-gamepad-tile btn-game-press" onclick="sudokuInstance.inputNumber(${n})" ${isComplete ? 'style="opacity: 0.55;"' : ''}>
          <span class="tile-main">${label}</span>
          <span class="tile-sub">${subLabel}</span>
        </button>
      `;
    }
    gamepadHtml += '</div>';

    // Action Tools Row
    const toolsHtml = `
      <div class="sudoku-tools-row">
        <button class="btn-sudoku-action btn-game-press" onclick="sudokuInstance.clearCell()">
          🧹 <span>${this.lang === 'ta' ? 'அழி' : 'Erase'}</span>
        </button>
        <button class="btn-sudoku-action btn-game-press" onclick="sudokuInstance.undo()">
          ↩️ <span>${this.lang === 'ta' ? 'முந்தைய படி' : 'Undo'}</span>
        </button>
        <button class="btn-sudoku-action btn-hint-gold btn-game-press" onclick="sudokuInstance.giveHint()">
          💡 <span>${this.lang === 'ta' ? 'மந்திரக் குறிப்பு' : 'Hint'}</span>
        </button>
        <button class="btn-sudoku-action btn-game-press" onclick="sudokuInstance.initPuzzle(sudokuInstance.currentPuzzleIdx + 1, sudokuInstance.difficulty)">
          🔄 <span>${this.lang === 'ta' ? 'புதிய புதிர்' : 'New Puzzle'}</span>
        </button>
      </div>
    `;

    this.container.innerHTML = consoleTop + quadrantsHtml + '</div>' + gamepadHtml + toolsHtml + '</div>';
  }
}

// ==============================================================================
// 2. MEMORY MATCHING PAIRS (3D FLIPS, SOUND & PARTICLES)
// ==============================================================================
class MemoryPairsGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.icons = [
      { id: 'coffee', symbol: '☕', name_ta: 'காபி டம்ளர்', name_en: 'Filter Coffee' },
      { id: 'banyan', symbol: '🌳', name_ta: 'ஆலமரம்', name_en: 'Banyan Tree' },
      { id: 'peacock', symbol: '🦚', name_ta: 'மயில்', name_en: 'Peacock' },
      { id: 'jasmine', symbol: '🌸', name_ta: 'மல்லிகை மலர்', name_en: 'Jasmine' },
      { id: 'flute', symbol: '🪈', name_ta: 'புல்லாங்குழல்', name_en: 'Flute' },
      { id: 'elephant', symbol: '🐘', name_ta: 'யானை', name_en: 'Elephant' }
    ];

    this.cards = [];
    this.flippedIndices = [];
    this.matchedIds = new Set();
    this.moves = 0;
    this.streak = 0;
    this.score = 0;
    this.isLocked = false;
    this.startTime = Date.now();

    this.initGame();
  }

  initGame() {
    this.moves = 0;
    this.streak = 0;
    this.matchedIds.clear();
    this.flippedIndices = [];
    this.isLocked = false;
    this.startTime = Date.now();

    const deck = [];
    this.icons.forEach(item => {
      deck.push({ ...item, uid: Math.random() });
      deck.push({ ...item, uid: Math.random() });
    });

    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }

    this.cards = deck;
    this.render();
  }

  flipCard(idx) {
    if (this.isLocked) return;
    if (this.flippedIndices.includes(idx)) return;
    if (this.matchedIds.has(this.cards[idx].id)) return;

    SoundFX.flip();
    this.flippedIndices.push(idx);
    this.render();

    if (this.flippedIndices.length === 2) {
      this.moves++;
      this.isLocked = true;
      const [idx1, idx2] = this.flippedIndices;
      const card1 = this.cards[idx1];
      const card2 = this.cards[idx2];

      if (card1.id === card2.id) {
        // Matched!
        SoundFX.correct();
        this.matchedIds.add(card1.id);
        this.streak++;
        this.score += (50 * this.streak);

        showFloatingPoints(this.container, `+${50 * this.streak} PTS! ✨`);
        this.flippedIndices = [];
        this.isLocked = false;
        this.render();

        if (this.matchedIds.size === this.icons.length) {
          const rt = Date.now() - this.startTime;
          recordGameTelemetry('memory_pairs', 100, 1.0, rt, 'memory');

          renderInGameCelebration(this.container, {
            motif: '🃏',
            badge: this.lang === 'ta' ? '✨ கூர்மையான நினைவாற்றல்' : '✨ Sharp Memory',
            title: this.lang === 'ta' ? 'அனைத்து ஜோடிகளும் கண்டுபிடிக்கப்பட்டன!' : 'All Pairs Matched!',
            text: this.lang === 'ta'
              ? `அற்புதமான நினைவாற்றல்! வெறும் ${this.moves} நகர்வுகளில் அனைத்து ஜோடிகளையும் வெற்றிகரமாக இணைத்தீர்கள்.`
              : `Flawless concentration! You uncovered and matched all pairs in only ${this.moves} total moves.`,
            lang: this.lang,
            onNext: () => this.initGame()
          });
        }
      } else {
        // Mismatch
        SoundFX.wrong();
        this.streak = 0;
        setTimeout(() => {
          this.flippedIndices = [];
          this.isLocked = false;
          this.render();
        }, 850);
      }
    }
  }

  render() {
    if (!this.container) return;

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score}</strong></div>
        <div class="hud-pill streak-pill">🔥 ${this.streak > 1 ? `${this.streak}x Combo!` : 'Streak Active'}</div>
        <div class="hud-pill">🔄 ${this.lang === 'ta' ? 'நகர்வுகள்:' : 'Moves:'} <strong>${this.moves}</strong></div>
        <div class="hud-pill" style="color: #34D399;">✨ ${this.matchedIds.size} / ${this.icons.length}</div>
      </div>
    `;

    let cardsHtml = '<div class="pairs-table-felt"><div class="pairs-grid">';
    this.cards.forEach((card, idx) => {
      const isFlipped = this.flippedIndices.includes(idx);
      const isMatched = this.matchedIds.has(card.id);

      let cardClasses = 'pair-card';
      if (isFlipped || isMatched) cardClasses += ' flipped';
      if (isMatched) cardClasses += ' matched';

      const cardLabel = (this.lang === 'ta') ? card.name_ta : card.name_en;

      cardsHtml += `
        <div class="${cardClasses}" onclick="memoryPairsInstance.flipCard(${idx})">
          <div class="pair-card-inner">
            <div class="pair-card-front">
              <span class="card-pattern">🪷</span>
            </div>
            <div class="pair-card-back">
              <span class="card-icon">${card.symbol}</span>
              <span class="card-name">${cardLabel}</span>
            </div>
          </div>
        </div>
      `;
    });
    cardsHtml += '</div></div>';

    this.container.innerHTML = hudHtml + cardsHtml;
  }
}


// ==============================================================================
// 3. PERSONALIZED FAMILIAR PHOTO RECALL (NO ALERTS)
// ==============================================================================
class FaceRecallGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.stimulus = null;
    this.score = 100;
    this.streak = 0;
    this.startTime = Date.now();
  }

  async loadStimulus() {
    try {
      this.lang = (typeof currentLang !== 'undefined') ? currentLang : this.lang;
      const patientId = window.activePatientId || 1;
      const res = await fetch(`/api/games/face-recall?patient_id=${patientId}&lang=${this.lang}`);
      this.stimulus = await res.json();
      this.startTime = Date.now();
      this.render();
    } catch (e) {
      console.error('Failed to load face recall:', e);
    }
  }

  handleChoice(btnEl, chosen) {
    if (!this.stimulus) return;
    const isCorrect = (chosen.trim().toLowerCase() === this.stimulus.target.trim().toLowerCase());
    const rt = Date.now() - this.startTime;

    if (isCorrect) {
      SoundFX.correct();
      btnEl.classList.add('anim-correct-glow');
      this.streak++;
      this.score += (100 * this.streak);
      showFloatingPoints(this.container, `+${100 * this.streak} XP! 🌟`);

      recordGameTelemetry('face_recall', 100, 1.0, rt, 'memory');

      setTimeout(() => {
        renderInGameCelebration(this.container, {
          motif: '🖼️',
          badge: this.lang === 'ta' ? '✨ குடும்ப பாசம்' : '✨ Cherished Bond',
          title: this.lang === 'ta' ? 'சரியான நினைவு!' : 'Cherished Memory Recognized!',
          text: this.lang === 'ta'
            ? `அற்புதமான நினைவாற்றல்! இவர் உங்கள் அன்பிற்குரிய ${this.stimulus.target}.`
            : `Heartwarming recognition! This is indeed your loved one: ${this.stimulus.target}.`,
          lang: this.lang,
          onNext: () => this.loadStimulus()
        });
      }, 700);
    } else {
      SoundFX.wrong();
      btnEl.classList.add('anim-wrong-shake');
      this.streak = 0;
      recordGameTelemetry('face_recall', 40, 0.4, rt, 'memory');
      setTimeout(() => btnEl.classList.remove('anim-wrong-shake'), 500);
    }
  }

  render() {
    if (!this.container) return;

    if (!this.stimulus || !this.stimulus.has_photos) {
      this.container.innerHTML = `
        <div class="game-empty-state">
          <div style="font-size: 50px;">📸</div>
          <h3>${this.lang === 'ta' ? 'நினைவுக் களஞ்சியத்தில் படங்கள் இல்லை' : 'No Memories in Patient Vault'}</h3>
          <p>${this.lang === 'ta' ? 'பராமரிப்பாளர் பிரிவில் சென்று குடும்ப புகைப்படங்களை பதிவேற்றவும்.' : 'Please upload personal family photos from the Caregiver Portal to anchor reminiscence questions.'}</p>
          <button class="btn-secondary" onclick="faceRecallInstance.loadStimulus()">🔄 ${this.lang === 'ta' ? 'புதுப்பி' : 'Refresh'}</button>
        </div>
      `;
      return;
    }

    const s = this.stimulus;
    const imgSrc = s.image_path.startsWith('/') ? s.image_path : `/${s.image_path}`;

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score}</strong></div>
        <div class="hud-pill streak-pill">🔥 ${this.streak} Streak</div>
        <div class="hud-pill">🖼️ ${this.lang === 'ta' ? 'குடும்ப நினைவு' : 'Family Vault'}</div>
      </div>
    `;

    const html = `
      <div class="photo-recall-card">
        <div class="photo-recall-header">
          <h3>🖼️ ${this.lang === 'ta' ? 'இவர் யார் என்று உங்களுக்கு நினைவிருக்கிறதா?' : 'Do you recognize this loved one?'}</h3>
          <p class="photo-cue">💡 ${this.lang === 'ta' ? 'உறவு முறை குறிப்பு:' : 'Relation Cue:'} <strong>${s.relation_cue}</strong></p>
        </div>

        <div class="photo-img-wrap">
          <img src="${imgSrc}" alt="Familiar Memory" class="photo-img" onerror="this.src='/uploads/story_images/day_3.jpg'">
        </div>

        <div class="photo-options-grid">
          ${s.options.map(opt => `
            <button class="btn-photo-opt btn-game-press" onclick="faceRecallInstance.handleChoice(this, '${opt.replace(/'/g, "\\'")}')">
              ${opt}
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = hudHtml + html;
  }
}


// ==============================================================================
// 4. MEMORY SPAN INCREMENT (SEQUENTIAL ANIMATIONS & KEYPAD)
// ==============================================================================
// ==============================================================================
// 4. SIMON-SAYS WORKING MEMORY SPAN - 3D MEMORY MATRIX CONSOLE
// ==============================================================================
class MemoryIncrementGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.span = 3;
    this.sequence = [];
    this.userSequence = [];
    this.phase = 'preview'; // 'preview' or 'recall'
    this.allSymbols = [];
    this.score = 200;
    this.streak = 0;
    this.lives = 3;
    this.previewTimer = null;
    this.startTime = Date.now();
  }

  async startNewRound(span = 3) {
    this.lang = (typeof currentLang !== 'undefined') ? currentLang : this.lang;
    this.span = span;
    this.userSequence = [];
    this.phase = 'preview';

    try {
      const res = await fetch(`/api/games/memory-increment?span=${this.span}&lang=${this.lang}`);
      const data = await res.json();
      this.sequence = data.sequence;
      this.allSymbols = data.all_symbols;
      this.render();

      let timeLeft = 3;
      if (this.previewTimer) clearInterval(this.previewTimer);

      this.sequence.forEach((_, idx) => {
        setTimeout(() => {
          SoundFX.tap();
        }, idx * 600);
      });

      this.previewTimer = setInterval(() => {
        timeLeft--;
        const timerEl = document.getElementById('spanTimerCount');
        const barEl = document.getElementById('spanMeterBar');
        if (timerEl) timerEl.innerText = `${timeLeft}s`;
        if (barEl) barEl.style.width = `${(timeLeft / 3) * 100}%`;

        if (timeLeft <= 0) {
          clearInterval(this.previewTimer);
          SoundFX.flip();
          this.phase = 'recall';
          this.startTime = Date.now();
          this.render();
        }
      }, 1000);
    } catch (e) {
      console.error('Failed to load memory increment sequence:', e);
    }
  }

  replay() {
    SoundFX.tap();
    this.score = Math.max(0, this.score - 15);
    this.startNewRound(this.span);
  }

  undo() {
    SoundFX.tap();
    if (this.userSequence.length > 0) {
      this.userSequence.pop();
      this.render();
    }
  }

  handleSymbolTap(symId) {
    if (this.phase !== 'recall') return;
    SoundFX.tap();

    this.userSequence.push(symId);
    this.render();

    const currentIdx = this.userSequence.length - 1;
    if (this.userSequence[currentIdx] !== this.sequence[currentIdx].id) {
      SoundFX.wrong();
      this.lives = Math.max(0, this.lives - 1);
      this.streak = 0;
      const rt = Date.now() - this.startTime;
      recordGameTelemetry('memory_increment', 40, 0.4, rt, 'memory');

      showFloatingPoints(this.container, this.lang === 'ta' ? '⚠️ தவறான வரிசை!' : '⚠️ Pattern Mismatch!');

      if (this.lives === 0) {
        setTimeout(() => {
          showFloatingPoints(this.container, this.lang === 'ta' ? '🔄 புதிய தொடக்கம்!' : '🔄 Refreshing Focus...');
          this.lives = 3;
          this.startNewRound(Math.max(2, this.span - 1));
        }, 900);
      } else {
        setTimeout(() => {
          this.userSequence = [];
          this.render();
        }, 800);
      }
      return;
    }

    if (this.userSequence.length === this.sequence.length) {
      const rt = Date.now() - this.startTime;
      this.streak++;
      const earned = (this.span * 80) + (this.streak * 20);
      this.score += earned;
      showFloatingPoints(this.container, `+${earned} PTS! 🚀`);
      recordGameTelemetry('memory_increment', 100, 1.0, rt, 'memory');

      const nextSpan = Math.min(6, this.span + 1);

      setTimeout(() => {
        renderInGameCelebration(this.container, {
          motif: '🧠',
          badge: this.lang === 'ta' ? `✨ நிலை உயர்வு: Span ${this.span} வென்றீர்கள்!` : `✨ Span ${this.span} Mastered!`,
          title: this.lang === 'ta' ? 'அற்புதமான வரிசை நினைவாற்றல்!' : 'Flawless Sequential Recall!',
          text: this.lang === 'ta'
            ? `அற்புதம்! ${this.span} பொருட்களின் சரியான வரிசையை நினைவில் வைத்தீர்கள். அடுத்த சவாலில் ${nextSpan} பொருட்கள் தோன்றும்!`
            : `Outstanding memory retention! You preserved all ${this.span} sequential elements in working memory. Advancing to Span ${nextSpan}!`,
          lang: this.lang,
          onNext: () => this.startNewRound(nextSpan)
        });
      }, 400);
    }
  }

  render() {
    if (!this.container) return;

    if (this.sequence.length === 0) {
      this.startNewRound(this.span);
      return;
    }

    let heartsHtml = '';
    for (let h = 0; h < 3; h++) {
      heartsHtml += `<span class="sudoku-heart ${h < this.lives ? '' : 'lost'}">❤️</span>`;
    }

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score} PTS</strong></div>
        <div class="hud-pill streak-pill">🔥 ${this.streak > 1 ? `${this.streak}x Combo!` : 'Focus Combo'}</div>
        <div class="hud-pill">🧠 Level: <strong>Span ${this.span}</strong></div>
        <div class="sudoku-hearts-wrap" title="3 Lives Remaining">${heartsHtml}</div>
      </div>
    `;

    if (this.phase === 'preview') {
      const html = `
        <div class="memory-span-console">
          <div class="span-stage-screen">
            <div class="span-stage-banner">
              👀 ${this.lang === 'ta' ? 'வரிசையை உற்று கவனியுங்கள் (Memorize Sequence):' : 'Watch & Memorize the Sequence:'}
              <span id="spanTimerCount" style="color: #38BDF8; font-size: 20px; font-weight: 900; margin-left: 8px;">3s</span>
            </div>

            <div class="span-meter-wrap">
              <div id="spanMeterBar" class="span-meter-bar" style="width: 100%;"></div>
            </div>

            <div class="span-seq-row">
              ${this.sequence.map((item, idx) => `
                <div class="span-seq-item-3d" style="animation-delay: ${idx * 0.18}s;">
                  <span class="step-tag">Step ${idx + 1}</span>
                  <span class="seq-icon">${item.icon}</span>
                  <span class="seq-label">${this.lang === 'ta' ? item.name_ta : item.name_en}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
      this.container.innerHTML = hudHtml + html;
    } else {
      const html = `
        <div class="memory-span-console">
          <div class="span-stage-screen">
            <div class="span-stage-banner">
              🎯 ${this.lang === 'ta' ? 'அதே வரிசையில் கீழ் உள்ள பொத்தான்களைத் தொடவும்:' : 'Tap the items below in the EXACT same sequence:'}
            </div>

            <div class="span-sockets-row">
              ${this.sequence.map((_, idx) => {
                const userSymId = this.userSequence[idx];
                const symObj = userSymId ? this.allSymbols.find(s => s.id === userSymId) : null;
                return `
                  <div class="span-socket-3d ${symObj ? 'filled anim-correct-glow' : 'empty'}">
                    ${symObj ? `<span class="seq-icon">${symObj.icon}</span>` : `<span class="socket-placeholder">#${idx + 1}</span>`}
                  </div>
                `;
              }).join('')}
            </div>

            <!-- Action Tools Row -->
            <div style="display: flex; justify-content: center; gap: 12px; margin-top: 10px;">
              <button class="btn-sudoku-action btn-game-press" onclick="memoryIncrementInstance.undo()">
                ↩️ <span>${this.lang === 'ta' ? 'முந்தைய படி (Undo)' : 'Undo'}</span>
              </button>
              <button class="btn-sudoku-action btn-game-press" onclick="memoryIncrementInstance.replay()">
                🔄 <span>${this.lang === 'ta' ? 'மீண்டும் காட்டு (Replay)' : 'Replay'}</span>
              </button>
            </div>
          </div>

          <!-- Arcade Gamepad Input Matrix -->
          <div class="span-gamepad-grid">
            ${this.allSymbols.map(sym => `
              <button class="btn-span-gem btn-game-press" onclick="memoryIncrementInstance.handleSymbolTap('${sym.id}')">
                <span class="gem-icon">${sym.icon}</span>
                <span class="gem-label">${this.lang === 'ta' ? sym.name_ta : sym.name_en}</span>
              </button>
            `).join('')}
          </div>
        </div>
      `;
      this.container.innerHTML = hudHtml + html;
    }
  }
}


// ==============================================================================
// 5. COLOR STROOP ATTENTION ARENA (ARCADE FOCUS RUSH)
// ==============================================================================
class StroopGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.currentStimulus = null;
    this.score = 250;
    this.streak = 0;
    this.trials = 0;
    this.lives = 3;
    this.startTime = Date.now();
    this.lastReactionTime = null;
    this.trialTimer = null;
    this.remainingMs = 3500;
  }

  async nextTrial() {
    try {
      this.lang = (typeof currentLang !== 'undefined') ? currentLang : this.lang;
      if (this.trialTimer) clearInterval(this.trialTimer);
      const res = await fetch(`/api/games/stroop?lang=${this.lang}`);
      this.currentStimulus = await res.json();
      this.startTime = Date.now();
      this.remainingMs = 3500;
      this.render();

      const fillEl = document.getElementById('stroopTimerBar');
      this.trialTimer = setInterval(() => {
        this.remainingMs -= 70;
        if (fillEl) {
          const pct = Math.max(0, (this.remainingMs / 3500) * 100);
          fillEl.style.width = `${pct}%`;
        }
        if (this.remainingMs <= 0) {
          clearInterval(this.trialTimer);
        }
      }, 70);
    } catch (e) {
      console.error('Failed to load Stroop trial:', e);
    }
  }

  handleChoice(btnEl, chosen) {
    if (!this.currentStimulus) return;
    if (this.trialTimer) clearInterval(this.trialTimer);

    this.trials++;
    const rt = Date.now() - this.startTime;
    this.lastReactionTime = rt;

    const isCorrect = (chosen.trim().toLowerCase() === this.currentStimulus.correct_answer.trim().toLowerCase());

    if (isCorrect) {
      SoundFX.correct();
      btnEl.classList.add('anim-correct-glow');
      this.streak++;

      const isFast = rt < 1600;
      const bonus = isFast ? 50 : 0;
      const pts = 100 + (this.streak * 25) + bonus;
      this.score += pts;

      const fastTag = isFast ? (this.lang === 'ta' ? '⚡ மின்னல் வேகம்!' : '⚡ LIGHTNING SPEED!') : '';
      showFloatingPoints(this.container, `+${pts} PTS! ${fastTag}`);
      recordGameTelemetry('stroop_focus', 100, 1.0, rt, 'attention');

      if (this.trials % 10 === 0) {
        setTimeout(() => {
          renderInGameCelebration(this.container, {
            motif: '🎯',
            badge: this.lang === 'ta' ? '✨ கூர்மையான கவனம்' : '✨ High Focus Master',
            title: this.lang === 'ta' ? '10 சோதனைகள் நிறைவுற்றன!' : '10 Focus Trials Mastered!',
            text: this.lang === 'ta'
              ? `சிறப்பான சாதனை! உங்கள் சராசரி எதிர்வினை நேரம் ${(rt / 1000).toFixed(2)} வினாடிகள். அடுத்த சுற்றுக்குத் தொடரலாம்!`
              : `Flawless attention control! Your reaction speed averaged ${(rt / 1000).toFixed(2)}s. Ready for the next speed tier!`,
            lang: this.lang,
            onNext: () => this.nextTrial()
          });
        }, 400);
      } else {
        setTimeout(() => this.nextTrial(), 450);
      }
    } else {
      SoundFX.wrong();
      btnEl.classList.add('anim-wrong-shake');
      this.lives = Math.max(0, this.lives - 1);
      this.streak = 0;
      recordGameTelemetry('stroop_focus', 0, 0.0, rt, 'attention');

      showFloatingPoints(this.container, this.lang === 'ta' ? '⚠️ மை நிறத்தைத் தேர்வுசெய்யவும்!' : '⚠️ Match Ink Color!');

      if (this.lives === 0) {
        setTimeout(() => {
          showFloatingPoints(this.container, this.lang === 'ta' ? '🔄 கவசங்கள் புதுப்பிக்கப்படுகின்றன...' : '🔄 Resetting Focus Shields...');
          this.lives = 3;
          this.nextTrial();
        }, 900);
      } else {
        setTimeout(() => this.nextTrial(), 650);
      }
    }
  }

  getColorClass(colorName) {
    const c = colorName.toLowerCase();
    if (c.includes('red') || c.includes('சிகப்பு') || c.includes('சிவப்பு')) return 'color-red';
    if (c.includes('blue') || c.includes('நீலம்')) return 'color-blue';
    if (c.includes('green') || c.includes('பச்சை')) return 'color-green';
    if (c.includes('yellow') || c.includes('மஞ்சள்')) return 'color-yellow';
    return 'color-blue';
  }

  getColorEmoji(colorName) {
    const c = colorName.toLowerCase();
    if (c.includes('red') || c.includes('சிகப்பு') || c.includes('சிவப்பு')) return '🔴';
    if (c.includes('blue') || c.includes('நீலம்')) return '🔵';
    if (c.includes('green') || c.includes('பச்சை')) return '🟢';
    if (c.includes('yellow') || c.includes('மஞ்சள்')) return '🟡';
    return '💎';
  }

  render() {
    if (!this.container) return;

    if (!this.currentStimulus) {
      this.nextTrial();
      return;
    }

    const s = this.currentStimulus;

    let shieldsHtml = '';
    for (let h = 0; h < 3; h++) {
      shieldsHtml += `<span class="sudoku-heart ${h < this.lives ? '' : 'lost'}">🛡️</span>`;
    }

    const rtDisplay = this.lastReactionTime ? `${(this.lastReactionTime / 1000).toFixed(2)}s` : '--';

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score} PTS</strong></div>
        <div class="hud-pill streak-pill">🔥 ${this.streak > 1 ? `${this.streak}x Combo!` : 'Focus Streak'}</div>
        <div class="hud-pill">⏱️ <strong>${rtDisplay}</strong></div>
        <div class="hud-pill">🎯 Round <strong>${(this.trials % 10) + 1} / 10</strong></div>
        <div class="sudoku-hearts-wrap" title="3 Shields Remaining">${shieldsHtml}</div>
      </div>
    `;

    const html = `
      <div class="stroop-game-console">
        <!-- Attention Rule Banner -->
        <div class="stroop-rule-banner">
          ⚡ ${this.lang === 'ta' ? 'மை நிறத்தை (INK COLOR) மட்டும் தொடவும்! சொல்லைப் படிக்க வேண்டாம்!' : 'TAP THE INK COLOR ONLY! DO NOT READ THE WORD!'}
        </div>

        <!-- Optical Target Chamber -->
        <div class="stroop-target-chamber">
          <div class="stroop-reticle-ring"></div>
          <div class="stroop-target-word" style="color: ${s.display_color}; text-shadow: 0 0 25px ${s.display_color}aa, 0 0 50px ${s.display_color}55;">
            ${s.word_text}
          </div>

          <div class="stroop-timer-bar-wrap">
            <div id="stroopTimerBar" class="stroop-timer-bar-fill"></div>
          </div>
        </div>

        <!-- Arcade Color Controller Keypad -->
        <div class="stroop-arcade-keypad">
          ${s.options.map(opt => `
            <button class="btn-arcade-color ${this.getColorClass(opt)} btn-game-press" onclick="stroopInstance.handleChoice(this, '${opt}')">
              <span class="color-gem"></span>
              <span>${this.getColorEmoji(opt)} ${opt}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = hudHtml + html;
  }
}


// ==============================================================================
// 6. TEMPORAL & SPATIAL REALITY ORIENTATION (INTERACTIVE ANALOG CLOCK)
// ==============================================================================
class OrientationGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.type = 'temporal';
    this.stimulus = null;
    this.score = 120;
    this.streak = 0;
    this.startTime = Date.now();
  }

  async loadQuestion(type = 'temporal') {
    this.type = type;
    try {
      this.lang = (typeof currentLang !== 'undefined') ? currentLang : this.lang;
      const res = await fetch(`/api/games/orientation?type=${this.type}&lang=${this.lang}`);
      this.stimulus = await res.json();
      this.startTime = Date.now();
      this.render();
    } catch (e) {
      console.error('Failed to load orientation question:', e);
    }
  }

  handleChoice(btnEl, chosen) {
    if (!this.stimulus) return;
    const isCorrect = (chosen.trim().toLowerCase() === this.stimulus.correct.trim().toLowerCase());
    const rt = Date.now() - this.startTime;

    if (isCorrect) {
      SoundFX.correct();
      btnEl.classList.add('anim-correct-glow');
      this.streak++;
      this.score += 60;
      showFloatingPoints(this.container, `+60 PTS! 🕒`);
      recordGameTelemetry('reality_orientation', 100, 1.0, rt, 'orientation');

      setTimeout(() => {
        renderInGameCelebration(this.container, {
          motif: '🧭',
          badge: this.lang === 'ta' ? '✨ காலம் & இடம் தெளிவு' : '✨ Grounded in Reality',
          title: this.lang === 'ta' ? 'மிகச் சரியான விழிப்புணர்வு!' : 'Accurate Reality Orientation!',
          text: this.lang === 'ta'
            ? `அருமை! மிகச்சரியான விடை: ${this.stimulus.correct}. காலம் மற்றும் சுற்றுப்புற விழிப்புணர்வு சீராக உள்ளது.`
            : `Brilliant! Correct anchor: ${this.stimulus.correct}. You remain accurately attuned to daily reality.`,
          lang: this.lang,
          onNext: () => this.loadQuestion(this.type)
        });
      }, 500);
    } else {
      SoundFX.wrong();
      btnEl.classList.add('anim-wrong-shake');
      this.streak = 0;
      recordGameTelemetry('reality_orientation', 40, 0.4, rt, 'orientation');
      setTimeout(() => btnEl.classList.remove('anim-wrong-shake'), 600);
    }
  }

  render() {
    if (!this.container) return;

    if (!this.stimulus) {
      this.loadQuestion('temporal');
      return;
    }

    const s = this.stimulus;

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score}</strong></div>
        <div class="hud-pill">🧭 ${this.type === 'temporal' ? (this.lang === 'ta' ? 'நேரம் & காலம்' : 'Time & Date') : (this.lang === 'ta' ? 'வீட்டு சூழல்' : 'Home Space')}</div>
      </div>
    `;

    const html = `
      <div class="orientation-card">
        <div class="orientation-type-toggle">
          <button class="btn-ori-toggle btn-game-press ${this.type === 'temporal' ? 'active' : ''}" onclick="orientationInstance.loadQuestion('temporal')">
            🕒 ${this.lang === 'ta' ? 'நேரம் & காலம்' : 'Time & Calendar'}
          </button>
          <button class="btn-ori-toggle btn-game-press ${this.type === 'spatial' ? 'active' : ''}" onclick="orientationInstance.loadQuestion('spatial')">
            🏡 ${this.lang === 'ta' ? 'வீட்டு சூழல் & இடம்' : 'Spatial Home Environment'}
          </button>
        </div>

        <div class="orientation-stimulus-box">
          <div class="ori-icon" style="font-size: 58px; margin-bottom: 8px;">${s.icon}</div>
          <h3 class="ori-question">${s.question}</h3>
        </div>

        <div class="orientation-options-grid">
          ${s.options.map(opt => `
            <button class="btn-ori-opt btn-game-press" onclick="orientationInstance.handleChoice(this, '${opt.replace(/'/g, "\\'")}')">
              ${opt}
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = hudHtml + html;
  }
}


// ==============================================================================
// 7. LANGUAGE & SEMANTIC OBJECT NAMING (TACTILE OPTIONS)
// ==============================================================================
class LanguageNamingGame {
  constructor(containerId, lang = null) {
    this.container = document.getElementById(containerId);
    this.lang = lang || (typeof currentLang !== 'undefined' ? currentLang : 'ta');
    this.stimulus = null;
    this.score = 140;
    this.streak = 0;
    this.startTime = Date.now();
  }

  async nextTrial() {
    try {
      this.lang = (typeof currentLang !== 'undefined') ? currentLang : this.lang;
      const res = await fetch(`/api/games/language?lang=${this.lang}`);
      this.stimulus = await res.json();
      this.startTime = Date.now();
      this.render();
    } catch (e) {
      console.error('Failed to load language trial:', e);
    }
  }

  handleChoice(btnEl, chosen) {
    if (!this.stimulus) return;
    const isCorrect = (chosen.trim().toLowerCase() === this.stimulus.target.trim().toLowerCase());
    const rt = Date.now() - this.startTime;

    if (isCorrect) {
      SoundFX.correct();
      btnEl.classList.add('anim-correct-glow');
      this.streak++;
      this.score += 50;
      showFloatingPoints(this.container, `+50 PTS! 🏷️`);
      recordGameTelemetry('language_naming', 100, 1.0, rt, 'language');

      setTimeout(() => {
        renderInGameCelebration(this.container, {
          motif: '🏷️',
          badge: this.lang === 'ta' ? '✨ சொல்வளம் & சொல் அடையாளம்' : '✨ Lexical Fluency',
          title: this.lang === 'ta' ? 'மிகச் சரியான பொருள் அடையாளம்!' : 'Accurate Semantic Naming!',
          text: this.lang === 'ta'
            ? `அருமை! இது ${this.stimulus.target}. சொல்வளமும் மொழித்திறனும் சீராக வெளிப்படுகிறது.`
            : `Splendid! That is indeed ${this.stimulus.target}. Excellent lexical retrieval and semantic matching.`,
          lang: this.lang,
          onNext: () => this.nextTrial()
        });
      }, 500);
    } else {
      SoundFX.wrong();
      btnEl.classList.add('anim-wrong-shake');
      this.streak = 0;
      recordGameTelemetry('language_naming', 30, 0.3, rt, 'language');
      setTimeout(() => btnEl.classList.remove('anim-wrong-shake'), 600);
    }
  }

  render() {
    if (!this.container) return;

    if (!this.stimulus) {
      this.nextTrial();
      return;
    }

    const s = this.stimulus;

    const hudHtml = `
      <div class="game-hud-bar">
        <div class="hud-pill score-pill">🏆 ${this.lang === 'ta' ? 'மதிப்பெண்:' : 'Score:'} <strong>${this.score}</strong></div>
        <div class="hud-pill">🏷️ ${s.category}</div>
      </div>
    `;

    const html = `
      <div class="naming-card">
        <div class="naming-header">
          <h3>🏷️ ${this.lang === 'ta' ? 'இந்தப் பொருளின் சரியான பெயர் என்ன?' : 'What is the correct name of this object?'}</h3>
          <p class="naming-category">📁 ${this.lang === 'ta' ? 'பிரிவு:' : 'Category:'} <strong>${s.category}</strong></p>
        </div>

        <div class="naming-visual-box">
          <span class="naming-icon">${s.icon}</span>
        </div>

        <div class="naming-options-grid">
          ${s.options.map(opt => `
            <button class="btn-naming-opt btn-game-press" onclick="languageNamingInstance.handleChoice(this, '${opt.replace(/'/g, "\\'")}')">
              ${opt}
            </button>
          `).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = hudHtml + html;
  }
}

// Global Window Exports
if (typeof window !== 'undefined') {
  window.SudokuGame = SudokuGame;
  window.MemoryPairsGame = MemoryPairsGame;
  window.FaceRecallGame = FaceRecallGame;
  window.MemoryIncrementGame = MemoryIncrementGame;
  window.StroopGame = StroopGame;
  window.OrientationGame = OrientationGame;
  window.LanguageNamingGame = LanguageNamingGame;
  window.SoundFX = SoundFX;
  window.ConfettiFX = ConfettiFX;
}
