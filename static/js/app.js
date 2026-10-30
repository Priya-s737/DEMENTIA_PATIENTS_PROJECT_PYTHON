/**
 * NeuroCare Clinical Web Portal - Complete Multi-Role Application Orchestrator
 * Google & Vellore VTOP Structured Layout
 * Restores ALL features from original app:
 * - 3 Portals: Senior 1-Tap Mode, Caregiver Portal, Clinical Specialist Admin
 * - 7 Clinical Games: Sudoku, Pairs, Photo Recall, Memory Span, Stroop, Orientation, Object Naming
 * - Caregiver Memory Vault with Local Photo Uploader
 * - Clinical Specialist RCT Statistics (N=30) and LaTeX Generation
 * - Strict Bilingual Localization (Pure Tamil & Pure English)
 */

let currentLang = 'ta';
let currentRole = 'senior';
let currentUser = null;
let activePatient = null;
let activePatientId = 1;

// Global Game & Player Instances
let playerInstance = null;
let sudokuInstance = null;
let memoryPairsInstance = null;
let faceRecallInstance = null;
let memoryIncrementInstance = null;
let stroopInstance = null;
let orientationInstance = null;
let languageNamingInstance = null;

let allEpisodes = [];
let todayEpisode = null;
let activeDayIdx = 3;
let patientList = [];

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', async () => {
  window.activePatientId = activePatientId;

  // Initialize 60 FPS HTML5 Canvas Moving Picture Player
  playerInstance = new MovingPicturePlayer('cinemaCanvas', {
    audioId: 'storyAudioElem',
    playBtnId: 'btnCinemaPlay',
    muteBtnId: 'btnCinemaMute',
    timeId: 'cinemaTimeCode',
    progressId: 'cinemaProgressFill',
    thumbId: 'cinemaScrubberThumb',
    subtitleId: 'cinemaSubtitleBox',
    themeBadgeId: 'cinemaThemeBadge'
  });

  // Initialize all 7 Cognitive Games
  sudokuInstance = new SudokuGame('sudokuGameMount');
  memoryPairsInstance = new MemoryPairsGame('memoryPairsMount');
  faceRecallInstance = new FaceRecallGame('faceRecallMount');
  memoryIncrementInstance = new MemoryIncrementGame('memoryIncrementMount');
  stroopInstance = new StroopGame('stroopGameMount');
  orientationInstance = new OrientationGame('orientationMount');
  languageNamingInstance = new LanguageNamingGame('languageMount');

  // Load backend data
  await loadPatientProfilesList();
  await loadPatientRecord(1);
  await loadStories();

  setupScrubberEvents();
  updateStaticLabels();
});


// ==============================================================================
// 1. AUTHENTICATION & ROLE SWITCHING
// ==============================================================================

function openAuthModal() {
  const modal = document.getElementById('authGateModal');
  if (modal) modal.style.display = 'block';
  loadPatientProfilesList();
}

function closeAuthModal() {
  const modal = document.getElementById('authGateModal');
  if (modal) modal.style.display = 'none';
}

function switchAuthTab(tabId) {
  document.querySelectorAll('.auth-tab-btn').forEach((btn, idx) => {
    const isTarget = btn.getAttribute('onclick').includes(tabId);
    btn.classList.toggle('active', isTarget);
  });
  document.querySelectorAll('.auth-tab-pane').forEach(pane => {
    pane.classList.toggle('active', pane.id === tabId);
  });
}

async function loadPatientProfilesList() {
  try {
    const res = await fetch('/api/auth/patients');
    patientList = await res.json();
    renderPatientLaunchpadCards();
  } catch (e) {
    console.error('Failed to load patient profiles:', e);
  }
}

function renderPatientLaunchpadCards() {
  const mount = document.getElementById('authPatientCardsMount');
  if (!mount || !patientList) return;

  mount.innerHTML = patientList.map((p, idx) => {
    const isSelected = (p.id === activePatientId);
    const desc = (currentLang === 'ta') ? p.desc_ta : p.desc_en;
    const avatar = (p.id === 1) ? '👨‍🏫' : ((p.id === 2) ? '👩‍🏫' : '👨‍⚕️');

    return `
      <div class="patient-launch-card ${isSelected ? 'selected' : ''}" onclick="selectPatientForLaunch(${p.id})">
        <div class="avatar">${avatar}</div>
        <div class="name">${p.name}</div>
        <div class="condition">${p.age} ${currentLang === 'ta' ? 'வயது' : 'yrs'} • ${p.condition}</div>
        <div class="desc">💡 ${desc}</div>
      </div>
    `;
  }).join('');
}

function selectPatientForLaunch(patientId) {
  activePatientId = patientId;
  window.activePatientId = patientId;
  renderPatientLaunchpadCards();
}

async function launchSeniorSession(lang) {
  currentLang = lang;
  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'senior', patient_id: activePatientId })
    });
    const data = await res.json();
    if (data.status === 'success') {
      currentUser = data.user;
      activePatient = data.patient;
      setRoleView('senior', currentUser, activePatient);
      closeAuthModal();

      // Update language toggle button text
      const langBtn = document.getElementById('langToggleBtn');
      if (langBtn) langBtn.innerText = (currentLang === 'ta') ? 'English' : 'தமிழ்';

      // Refresh games and story for new language
      propagateLanguageToAllComponents();
      playEpisode(activeDayIdx);
    }
  } catch (e) {
    console.error('Senior launch failed:', e);
  }
}

async function handleCaregiverLogin(event) {
  event.preventDefault();
  const username = document.getElementById('cgLoginUser').value.trim();
  const password = document.getElementById('cgLoginPass').value.trim();

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'caregiver', username, password })
    });
    const data = await res.json();
    if (data.status === 'success') {
      currentUser = data.user;
      activePatient = data.patient;
      setRoleView('caregiver', currentUser, activePatient);
      closeAuthModal();
      loadCaregiverMemories();
      loadCaregiverAnalytics();
    } else {
      alert(data.message || 'Login failed.');
    }
  } catch (e) {
    alert('Server communication error during caregiver login.');
  }
}

async function handleCaregiverRegister(event) {
  event.preventDefault();
  const fullName = document.getElementById('cgRegName').value.trim();
  const username = document.getElementById('cgRegUser').value.trim();
  const password = document.getElementById('cgRegPass').value.trim();
  const phone = document.getElementById('cgRegPhone').value.trim();

  try {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full_name: fullName, username, password, phone, role: 'caregiver' })
    });
    const data = await res.json();
    if (data.status === 'success') {
      alert(currentLang === 'ta' ? 'கணக்கு வெற்றிகரமாக பதிவு செய்யப்பட்டது! இப்போது உள்நுழையலாம்.' : 'Account registered successfully! Please log in.');
      document.getElementById('cgLoginUser').value = username;
      document.getElementById('cgLoginPass').value = password;
    } else {
      alert(data.message || 'Registration failed.');
    }
  } catch (e) {
    alert('Error registering caregiver account.');
  }
}

async function handleAdminLogin(event) {
  event.preventDefault();
  const username = document.getElementById('adminLoginUser').value.trim();
  const password = document.getElementById('adminLoginPass').value.trim();

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: 'admin', username, password })
    });
    const data = await res.json();
    if (data.status === 'success') {
      currentUser = data.user;
      activePatient = data.patient;
      setRoleView('admin', currentUser, activePatient);
      closeAuthModal();
      loadAdminOverview();
      loadAdminRctStats();
    } else {
      alert(data.message || 'Login failed.');
    }
  } catch (e) {
    alert('Server communication error during admin login.');
  }
}

function handleLogout() {
  currentUser = null;
  openAuthModal();
}

function setRoleView(role, user, patient) {
  currentRole = role;

  const roleBadge = document.getElementById('currentRoleBadge');
  const avatarEl = document.getElementById('activeUserAvatar');
  const nameEl = document.getElementById('activeUserNameDisplay');
  const subEl = document.getElementById('activeUserSubDisplay');

  // Hide all view containers
  document.getElementById('seniorPortalView').style.display = 'none';
  document.getElementById('caregiverPortalView').style.display = 'none';
  document.getElementById('adminPortalView').style.display = 'none';

  // Hide all navigation bars
  document.getElementById('seniorNavBar').style.display = 'none';
  document.getElementById('caregiverNavBar').style.display = 'none';
  document.getElementById('adminNavBar').style.display = 'none';

  if (role === 'senior') {
    if (roleBadge) roleBadge.innerText = (currentLang === 'ta') ? 'முதியோர் பிரிவு' : 'SENIOR MODE';
    if (avatarEl) avatarEl.innerText = '👴';
    if (nameEl) nameEl.innerText = patient ? patient.name : 'Ramasamy Sundaram';
    if (subEl) subEl.innerText = `PID: NC-2026-0${patient ? patient.id : 1} • MMSE: ${patient ? patient.baseline_mmse : 23.5}/30 • Level ${patient ? patient.current_adaptive_level : 5}`;

    document.getElementById('seniorNavBar').style.display = 'flex';
    document.getElementById('seniorPortalView').style.display = 'block';
    switchSeniorTab('senior_story');
  } else if (role === 'caregiver') {
    if (roleBadge) roleBadge.innerText = (currentLang === 'ta') ? 'பராமரிப்பாளர்' : 'CAREGIVER PORTAL';
    if (avatarEl) avatarEl.innerText = '👨‍⚕️';
    if (nameEl) nameEl.innerText = user ? user.full_name : 'Primary Caregiver';
    if (subEl) subEl.innerText = (currentLang === 'ta') ? `பராமரிக்கப்படும் முதியவர்: ${patient ? patient.name : 'Ramasamy Sundaram'}` : `Assigned Elder: ${patient ? patient.name : 'Ramasamy Sundaram'}`;

    const cgElderName = document.getElementById('cgAssignedElderName');
    const cgElderMeta = document.getElementById('cgAssignedElderMeta');
    if (cgElderName && patient) cgElderName.innerText = patient.name;
    if (cgElderMeta && patient) cgElderMeta.innerText = `Age: ${patient.age} | Level: Level ${patient.current_adaptive_level}/5 | ${patient.condition}`;

    document.getElementById('caregiverNavBar').style.display = 'flex';
    document.getElementById('caregiverPortalView').style.display = 'block';
    switchCaregiverTab('cg_vault');
  } else if (role === 'admin') {
    if (roleBadge) roleBadge.innerText = (currentLang === 'ta') ? 'மருத்துவ நிர்வாகி' : 'CLINICAL SPECIALIST (ADMIN)';
    if (avatarEl) avatarEl.innerText = '🛡️';
    if (nameEl) nameEl.innerText = user ? user.full_name : 'Dr. S. Meenakshi';
    if (subEl) subEl.innerText = 'Clinical Administrator • Research Benchmark Lead';

    document.getElementById('adminNavBar').style.display = 'flex';
    document.getElementById('adminPortalView').style.display = 'block';
    switchAdminTab('adm_caregivers');
  }
}

function launchElderFromCaregiver() {
  setRoleView('senior', null, activePatient);
}


// ==============================================================================
// 2. BILINGUAL MOVING PICTURE STORY THEATER
// ==============================================================================

async function loadStories() {
  try {
    const res = await fetch('/api/story/all');
    const data = await res.json();
    allEpisodes = data.episodes;
    todayEpisode = data.today;
    activeDayIdx = todayEpisode.day_idx;

    renderDaySelector();
    playEpisode(todayEpisode.day_idx);
  } catch (err) {
    console.error('Failed to load stories:', err);
  }
}

function renderDaySelector() {
  const container = document.getElementById('daySelectorMount');
  if (!container || !allEpisodes) return;

  const todayIdx = todayEpisode ? todayEpisode.day_idx : 3;

  const html = allEpisodes.map(ep => {
    const isActive = (ep.day_idx === activeDayIdx);
    const isToday = (ep.day_idx === todayIdx);
    const dayLabel = (currentLang === 'ta') ? ep.day_short_ta : ep.day_short_en;
    const todayTag = (currentLang === 'ta') ? 'இன்று' : 'TODAY';

    let cardClasses = 'day-pill-card';
    if (isActive) cardClasses += ' active';
    if (isToday) cardClasses += ' today';

    return `
      <div class="${cardClasses}" onclick="switchDay(${ep.day_idx})">
        <div class="pill-icon">${ep.episode_icon}</div>
        <div class="pill-day-title">${dayLabel}</div>
        ${isToday ? `<div class="pill-tag">⭐ ${todayTag}</div>` : ''}
      </div>
    `;
  }).join('');

  container.innerHTML = html;
}

function switchDay(dayIdx) {
  activeDayIdx = dayIdx;
  renderDaySelector();
  playEpisode(dayIdx);
}

function playEpisode(dayIdx) {
  const ep = allEpisodes.find(e => e.day_idx === dayIdx) || todayEpisode;
  if (!ep || !playerInstance) return;

  // Reflection Card Text
  const title = (currentLang === 'ta') ? ep.title_ta : ep.title_en;
  const quote = (currentLang === 'ta') ? ep.quote_ta : ep.quote_en;
  const story = (currentLang === 'ta') ? ep.story_ta : ep.story_en;

  const titleEl = document.getElementById('storyCardTitle');
  const quoteEl = document.getElementById('storyCardQuote');
  const textEl = document.getElementById('storyCardText');
  const dateEl = document.getElementById('portalTodayDate');

  if (titleEl) titleEl.innerHTML = `<span>${ep.episode_icon}</span> ${title}`;
  if (quoteEl) quoteEl.innerText = quote;
  if (textEl) textEl.innerText = story;

  if (dateEl) {
    const d = new Date();
    const dayName = (currentLang === 'ta') ? ep.day_ta : ep.day_en;
    dateEl.innerText = (currentLang === 'ta')
      ? `${dayName}, ${d.getDate()} அக்டோபர் ${d.getFullYear()}`
      : `${dayName}, October ${d.getDate()}, ${d.getFullYear()}`;
  }

  // Load moving picture & bilingual audio
  playerInstance.loadStory(ep, currentLang);
}


// ==============================================================================
// 3. TAB NAVIGATION (SENIOR, CAREGIVER, ADMIN)
// ==============================================================================

function switchSeniorTab(tabKey) {
  if (typeof SoundFX !== 'undefined') SoundFX.tap();
  document.querySelectorAll('#seniorNavBar .nav-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabKey);
  });
  document.querySelectorAll('#seniorPortalView .portal-section').forEach(sec => {
    sec.style.display = (sec.id === `sec_${tabKey}`) ? 'block' : 'none';
  });

  if (tabKey === 'senior_games') {
    activateGame('sudoku');
  }
}

function switchCaregiverTab(tabKey) {
  if (typeof SoundFX !== 'undefined') SoundFX.tap();
  document.querySelectorAll('#caregiverNavBar .nav-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabKey);
  });
  document.querySelectorAll('#caregiverPortalView .portal-section').forEach(sec => {
    sec.style.display = (sec.id === `sec_${tabKey}`) ? 'block' : 'none';
  });
}

function switchAdminTab(tabKey) {
  if (typeof SoundFX !== 'undefined') SoundFX.tap();
  document.querySelectorAll('#adminNavBar .nav-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabKey);
  });
  document.querySelectorAll('#adminPortalView .portal-section').forEach(sec => {
    sec.style.display = (sec.id === `sec_${tabKey}`) ? 'block' : 'none';
  });
}

// 7 Games Selector in Senior Mode
function activateGame(gameKey) {
  if (typeof SoundFX !== 'undefined') SoundFX.tap();
  document.querySelectorAll('.game-tab-pill').forEach(pill => {
    const isTarget = pill.getAttribute('onclick').includes(gameKey);
    pill.classList.toggle('active', isTarget);
  });

  document.querySelectorAll('.game-panel-wrap').forEach(wrap => {
    wrap.style.display = (wrap.id === `game_mount_${gameKey}`) ? 'block' : 'none';
  });

  if (gameKey === 'sudoku' && sudokuInstance) sudokuInstance.render();
  if (gameKey === 'pairs' && memoryPairsInstance) memoryPairsInstance.render();
  if (gameKey === 'photo_recall' && faceRecallInstance) faceRecallInstance.loadStimulus();
  if (gameKey === 'memory_increment' && memoryIncrementInstance) memoryIncrementInstance.startNewRound(3);
  if (gameKey === 'stroop' && stroopInstance) stroopInstance.nextTrial();
  if (gameKey === 'orientation' && orientationInstance) orientationInstance.loadQuestion('temporal');
  if (gameKey === 'language' && languageNamingInstance) languageNamingInstance.nextTrial();
}


// ==============================================================================
// 4. LANGUAGE SWITCHER (STRICT BILINGUAL PURE TAMIL & PURE ENGLISH)
// ==============================================================================

function toggleLanguage() {
  currentLang = (currentLang === 'ta') ? 'en' : 'ta';
  document.getElementById('langToggleBtn').innerText = (currentLang === 'ta') ? 'English' : 'தமிழ்';

  propagateLanguageToAllComponents();

  renderDaySelector();
  playEpisode(activeDayIdx);
  updateStaticLabels();
  renderPatientLaunchpadCards();

  if (currentRole === 'caregiver') loadCaregiverMemories();
  if (currentRole === 'admin') {
    loadAdminOverview();
    loadAdminRctStats();
  }
}

function propagateLanguageToAllComponents() {
  if (sudokuInstance) sudokuInstance.lang = currentLang;
  if (memoryPairsInstance) memoryPairsInstance.lang = currentLang;
  if (faceRecallInstance) faceRecallInstance.lang = currentLang;
  if (memoryIncrementInstance) memoryIncrementInstance.lang = currentLang;
  if (stroopInstance) stroopInstance.lang = currentLang;
  if (orientationInstance) orientationInstance.lang = currentLang;
  if (languageNamingInstance) languageNamingInstance.lang = currentLang;

  // Re-render active game
  const activeWrap = document.querySelector('.game-panel-wrap[style*="block"], .game-panel-wrap.active');
  if (activeWrap) {
    const id = activeWrap.id;
    if (id.includes('sudoku')) sudokuInstance.render();
    if (id.includes('pairs')) memoryPairsInstance.render();
    if (id.includes('photo_recall')) faceRecallInstance.loadStimulus();
    if (id.includes('memory_increment')) memoryIncrementInstance.render();
    if (id.includes('stroop')) stroopInstance.render();
    if (id.includes('orientation')) orientationInstance.loadQuestion(orientationInstance.type);
    if (id.includes('language')) languageNamingInstance.render();
  }
}

function updateStaticLabels() {
  const isTa = (currentLang === 'ta');
  document.querySelectorAll('[data-en]').forEach(el => {
    el.innerText = isTa ? el.getAttribute('data-ta') : el.getAttribute('data-en');
  });
}


// ==============================================================================
// 5. CAREGIVER PORTAL: MEMORY VAULT & REPORT FUNCTIONS
// ==============================================================================

async function loadCaregiverMemories() {
  const patientId = activePatient ? activePatient.id : 1;
  try {
    const res = await fetch(`/api/caregiver/memories?patient_id=${patientId}`);
    const memories = await res.json();
    renderCaregiverMemoryGallery(memories);
  } catch (e) {
    console.error('Failed to load caregiver memories:', e);
  }
}

function renderCaregiverMemoryGallery(memories) {
  const mount = document.getElementById('caregiverMemoryGalleryMount');
  if (!mount) return;

  if (!memories || memories.length === 0) {
    mount.innerHTML = `<p style="color: var(--text-muted); font-size: 14px;">${currentLang === 'ta' ? 'நினைவுகள் எதுவும் இன்னும் சேர்க்கப்படவில்லை.' : 'No memory photos added yet. Upload a family photo above!'}</p>`;
    return;
  }

  mount.innerHTML = memories.map(m => {
    const title = (currentLang === 'ta') ? m.label_ta : m.label_en;
    const desc = (currentLang === 'ta') ? m.detail_ta : m.detail_en;
    const imgPath = m.image_path ? (m.image_path.startsWith('/') ? m.image_path : `/${m.image_path}`) : '/uploads/story_images/day_3.jpg';

    return `
      <div class="memory-item-card">
        <img src="${imgPath}" alt="${title}" onerror="this.src='/uploads/story_images/day_3.jpg'">
        <div class="memory-item-body">
          <div class="memory-item-title">${title}</div>
          <div class="memory-item-desc">💡 ${desc}</div>
          <div class="memory-item-meta">
            <span style="font-size: 11px; background: #E2E8F0; padding: 2px 6px; border-radius: 4px; font-weight: 700;">${m.category}</span>
            <button onclick="handleDeleteMemory(${m.id})" style="background: none; border: none; color: #EF4444; font-size: 12px; font-weight: 700; cursor: pointer;">
              🗑️ ${currentLang === 'ta' ? 'நீக்கு' : 'Delete'}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

async function handleMemoryUpload(event) {
  event.preventDefault();
  const patientId = activePatient ? activePatient.id : 1;

  const form = document.getElementById('memoryUploadForm');
  const formData = new FormData();
  formData.append('patient_id', patientId);
  formData.append('category', document.getElementById('memCat').value);
  formData.append('label_en', document.getElementById('memLabelEn').value);
  formData.append('label_ta', document.getElementById('memLabelTa').value);
  formData.append('detail_en', document.getElementById('memDetailEn').value);
  formData.append('detail_ta', document.getElementById('memDetailTa').value);

  const fileInput = document.getElementById('memFile');
  if (fileInput.files.length > 0) {
    formData.append('file', fileInput.files[0]);
  }

  try {
    const res = await fetch('/api/caregiver/memories', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    if (data.status === 'success') {
      alert(currentLang === 'ta' ? 'புகைப்படம் வெற்றிகரமாகச் சேமிக்கப்பட்டது!' : 'Memory photo saved successfully!');
      form.reset();
      loadCaregiverMemories();
    } else {
      alert(data.message || 'Upload error');
    }
  } catch (e) {
    alert('Failed to upload memory photo.');
  }
}

async function handleDeleteMemory(memId) {
  if (!confirm(currentLang === 'ta' ? 'இந்த நினைவை நீக்க விரும்புகிறீர்களா?' : 'Are you sure you want to delete this memory?')) return;
  try {
    const res = await fetch(`/api/caregiver/memories/${memId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.status === 'success') {
      loadCaregiverMemories();
    }
  } catch (e) {
    console.error('Delete memory failed:', e);
  }
}

async function loadCaregiverAnalytics() {
  const patientId = activePatient ? activePatient.id : 1;
  try {
    const res = await fetch(`/api/analytics?patient_id=${patientId}`);
    const data = await res.json();
    const tbody = document.querySelector('#cgSessionHistoryTable tbody');
    if (!tbody || !data.recent_sessions) return;

    tbody.innerHTML = data.recent_sessions.map(s => `
      <tr>
        <td>#${s.id || s.session_id || '28'}</td>
        <td><strong>${s.cognitive_domain || 'Memory'}</strong></td>
        <td><span style="color: #10B981; font-weight: 800;">${s.accuracy_pct || (s.accuracy ? Math.round(s.accuracy * 100) : 85)}%</span></td>
        <td>${s.avg_response_time_sec || (s.response_time_ms ? (s.response_time_ms/1000).toFixed(2) : 2.1)}s</td>
        <td>${s.session_timestamp || '2026-10-22'}</td>
      </tr>
    `).join('');
  } catch (e) {
    console.error('Failed to load caregiver analytics:', e);
  }
}

function previewGameInCaregiver(gameKey) {
  const mount = document.getElementById('caregiverPreviewMount');
  if (!mount) return;
  mount.innerHTML = `<div id="cg_submount_${gameKey}" class="neat-card"></div>`;

  if (gameKey === 'sudoku') {
    new SudokuGame(`cg_submount_${gameKey}`).render();
  } else if (gameKey === 'pairs') {
    new MemoryPairsGame(`cg_submount_${gameKey}`).render();
  } else if (gameKey === 'photo_recall') {
    const f = new FaceRecallGame(`cg_submount_${gameKey}`);
    f.loadStimulus();
  } else if (gameKey === 'memory_increment') {
    const m = new MemoryIncrementGame(`cg_submount_${gameKey}`);
    m.startNewRound(3);
  } else if (gameKey === 'stroop') {
    const s = new StroopGame(`cg_submount_${gameKey}`);
    s.nextTrial();
  } else if (gameKey === 'orientation') {
    const o = new OrientationGame(`cg_submount_${gameKey}`);
    o.loadQuestion('temporal');
  } else if (gameKey === 'language') {
    const l = new LanguageNamingGame(`cg_submount_${gameKey}`);
    l.nextTrial();
  }
}

function downloadClinicalReport() {
  const content = document.getElementById('clinicalReportTextView').innerText;
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Clinical_Assessment_Report_PID_${activePatient ? activePatient.id : 1}.md`;
  a.click();
  URL.revokeObjectURL(url);
}


// ==============================================================================
// 6. CLINICAL SPECIALIST & RCT RESEARCH BENCHMARK
// ==============================================================================

async function loadAdminOverview() {
  try {
    const res = await fetch('/api/clinical/overview');
    const data = await res.json();

    if (data.kpi) {
      document.getElementById('kpiCaregiversCount').innerText = data.kpi.caregivers_count;
      document.getElementById('kpiPatientsCount').innerText = data.kpi.patients_count;
      document.getElementById('kpiSessionsCount').innerText = data.kpi.sessions_count;
      document.getElementById('kpiAuditCount').innerText = data.kpi.audit_events_count;
    }

    // Caregivers Roster Table
    const cgTbody = document.querySelector('#admCaregiverRosterTable tbody');
    if (cgTbody && data.caregivers) {
      cgTbody.innerHTML = data.caregivers.map(cg => `
        <tr>
          <td>#${cg.id}</td>
          <td><code>${cg.username}</code></td>
          <td><strong>${cg.full_name}</strong></td>
          <td>${cg.phone}</td>
          <td><span style="background: #EFF6FF; color: #2563EB; font-weight: 800; padding: 2px 8px; border-radius: 6px;">${cg.assigned_patients} Elders</span></td>
          <td>${cg.created_at}</td>
        </tr>
      `).join('');
    }

    // Live Audit Logs Table
    const auditTbody = document.querySelector('#admAuditLogsTable tbody');
    if (auditTbody && data.audit_logs) {
      auditTbody.innerHTML = data.audit_logs.map(log => `
        <tr>
          <td style="font-size: 12.5px; color: var(--text-muted);">${log.timestamp || log.created_at || 'Just now'}</td>
          <td><strong>${log.username}</strong> (${log.role || 'caregiver'})</td>
          <td><span style="font-size: 11px; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 6px; border-radius: 4px; font-weight: 700;">${log.action_type || log.action}</span></td>
          <td style="font-size: 13.5px;">${log.details || log.message}</td>
        </tr>
      `).join('');
    }

    // Patient Cohort Table
    const pTbody = document.querySelector('#admPatientCohortTable tbody');
    if (pTbody && data.patients) {
      pTbody.innerHTML = data.patients.map(p => `
        <tr>
          <td>#NC-${p.id}</td>
          <td><strong>${p.name}</strong></td>
          <td>${p.age} yrs</td>
          <td><span style="color: #2563EB; font-weight: 700;">${p.condition}</span></td>
          <td><strong>${p.baseline_mmse} / 30</strong></td>
          <td><span style="background: #ECFDF5; color: #047857; font-weight: 800; padding: 2px 8px; border-radius: 6px;">Level ${p.current_adaptive_level}</span></td>
          <td>${p.caregiver_name || 'Caregiver'}</td>
        </tr>
      `).join('');
    }
  } catch (e) {
    console.error('Failed to load clinical overview:', e);
  }
}

async function loadAdminRctStats() {
  try {
    const res = await fetch('/api/clinical/rct-stats');
    const data = await res.json();

    const tbody = document.querySelector('#admRctStatsTable tbody');
    if (tbody && data.table_rows) {
      tbody.innerHTML = data.table_rows.map(row => `
        <tr>
          <td><strong>${row.domain}</strong></td>
          <td>${row.pre_test}</td>
          <td>${row.post_test}</td>
          <td><span style="color: #10B981; font-weight: 800;">${row.mean_gain}</span></td>
          <td><code>t = ${row.t_stat}</code></td>
          <td><strong style="color: #047857;">${row.p_value}</strong></td>
          <td><span style="background: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px; font-weight: 800;">d = ${row.cohens_d}</span></td>
        </tr>
      `).join('');
    }

    const latexEl = document.getElementById('admLatexCodeView');
    if (latexEl && data.latex_code) {
      latexEl.innerText = data.latex_code;
    }
  } catch (e) {
    console.error('Failed to load RCT statistics:', e);
  }
}


// ==============================================================================
// 7. UTILITY & ACCESSIBILITY
// ==============================================================================

let isLargeFont = false;
function toggleFontSize() {
  isLargeFont = !isLargeFont;
  document.body.classList.toggle('large-font', isLargeFont);
}

function setupScrubberEvents() {
  const track = document.getElementById('cinemaScrubberTrack');
  if (!track) return;

  track.addEventListener('click', (e) => {
    const rect = track.getBoundingClientRect();
    const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    if (playerInstance) {
      playerInstance.seek(ratio);
    }
  });
}

async function loadPatientRecord(patientId) {
  try {
    const res = await fetch(`/api/patient?id=${patientId}`);
    activePatient = await res.json();
    activePatientId = activePatient.id;
    window.activePatientId = activePatient.id;

    const seniorMmse = document.getElementById('seniorMmseVal');
    const seniorLevel = document.getElementById('seniorLevelVal');
    if (seniorMmse && activePatient) seniorMmse.innerText = `${activePatient.baseline_mmse} / 30`;
    if (seniorLevel && activePatient) seniorLevel.innerText = `Level ${activePatient.current_adaptive_level} / 5`;
  } catch (e) {
    console.error('Failed to load patient record:', e);
  }
}
