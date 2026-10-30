/**
 * Moving Picture Video Player Engine
 * HTML5 Canvas 60 FPS Ken Burns Motion, Physics Overlays, Synchronized Voice & Subtitles
 */

class MovingPicturePlayer {
  constructor(canvasId, options = {}) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.audio = document.getElementById(options.audioId || 'storyAudioElem');

    this.playBtn = document.getElementById(options.playBtnId || 'btnCinemaPlay');
    this.muteBtn = document.getElementById(options.muteBtnId || 'btnCinemaMute');
    this.timeDisplay = document.getElementById(options.timeId || 'cinemaTimeCode');
    this.progressBar = document.getElementById(options.progressId || 'cinemaProgressFill');
    this.scrubberThumb = document.getElementById(options.thumbId || 'cinemaScrubberThumb');
    this.subtitleEl = document.getElementById(options.subtitleId || 'cinemaSubtitleBox');
    this.themeBadgeEl = document.getElementById(options.themeBadgeId || 'cinemaThemeBadge');

    this.currentDay = 3; // Default: Thursday
    this.isPlaying = true;
    this.isMuted = false;
    this.currentTime = 0;
    this.totalDuration = 45;
    this.animTime = 0;
    this.animFrameId = null;

    this.bgImg = new Image();
    this.bgLoaded = false;
    this.captions = [];
    this.storyData = null;

    // Physics Particles
    this.particles = [];
    this.steamParticles = [];
    this.raindrops = [];
    this.musicNotes = [];
    this.initParticles();

    if (this.canvas) {
      this.canvas.width = 854;
      this.canvas.height = 480;
    }
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < 35; i++) {
      this.particles.push({
        x: Math.random() * 854,
        y: Math.random() * 480,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 0.8 - 0.5,
        size: Math.random() * 4 + 1.5,
        alpha: Math.random() * 0.7 + 0.2,
        phase: Math.random() * Math.PI * 2
      });
    }

    this.steamParticles = [];
    for (let s = 0; s < 22; s++) {
      this.steamParticles.push({
        x: 550 + (Math.random() - 0.5) * 24,
        y: 350 + Math.random() * 40,
        vy: -1.2 - Math.random() * 0.8,
        vx: 0,
        radius: 6 + Math.random() * 7,
        alpha: 0.6,
        age: Math.random() * 100
      });
    }

    this.raindrops = [];
    for (let r = 0; r < 75; r++) {
      this.raindrops.push({
        x: Math.random() * 854,
        y: Math.random() * 480,
        speed: 13 + Math.random() * 7,
        len: 12 + Math.random() * 10
      });
    }

    const symbols = ['♪', '♫', '♬', '♩'];
    this.musicNotes = [];
    for (let m = 0; m < 9; m++) {
      this.musicNotes.push({
        x: 430 + (Math.random() - 0.5) * 60,
        y: 280 + Math.random() * 120,
        sym: symbols[m % symbols.length],
        vy: -1.1 - Math.random() * 0.8,
        phase: Math.random() * Math.PI * 2,
        alpha: 0.85,
        size: 22 + Math.random() * 10
      });
    }
  }

  loadStory(storyData, lang = 'ta') {
    this.storyData = storyData;
    this.currentDay = storyData.day_idx;
    this.currentLang = lang;
    this.captions = (lang === 'ta') ? storyData.captions_ta : storyData.captions_en;

    // Load High-Res Artwork
    this.bgLoaded = false;
    this.bgImg = new Image();
    this.bgImg.crossOrigin = 'anonymous';
    this.bgImg.src = storyData.image_url || `/uploads/story_images/day_${this.currentDay}.jpg`;
    this.bgImg.onload = () => {
      this.bgLoaded = true;
    };

    // Update Theme Badge
    if (this.themeBadgeEl) {
      const dayName = (lang === 'ta') ? storyData.day_ta : storyData.day_en;
      const themeTag = (lang === 'ta') ? storyData.theme_tag_ta : storyData.theme_tag_en;
      this.themeBadgeEl.innerHTML = `<span>${storyData.episode_icon}</span> <span>${dayName} • ${themeTag}</span>`;
    }

    // Load Audio Source with dynamic language parameter (en or ta)
    if (this.audio) {
      const audioUrl = `/api/story/audio?day=${this.currentDay}&lang=${lang}`;
      this.audio.src = audioUrl;
      this.audio.load();
      this.audio.currentTime = 0;
      this.currentTime = 0;

      this.audio.onloadedmetadata = () => {
        if (this.audio.duration && this.audio.duration > 5) {
          this.totalDuration = this.audio.duration;
        }
      };

      this.audio.onended = () => {
        this.onVideoEnd();
      };

      // Autoplay
      const promise = this.audio.play();
      if (promise !== undefined) {
        promise.then(() => {
          this.isPlaying = true;
          if (this.playBtn) this.playBtn.innerText = '❚❚';
        }).catch(() => {
          this.isPlaying = true; // Video animation still plays smoothly!
        });
      }
    }

    if (!this.animFrameId) {
      this.startLoop();
    }
  }

  startLoop() {
    const loop = () => {
      this.update();
      this.draw();
      this.animFrameId = requestAnimationFrame(loop);
    };
    this.animFrameId = requestAnimationFrame(loop);
  }

  update() {
    this.animTime += 0.02;

    if (this.isPlaying) {
      if (this.audio && !this.audio.paused) {
        this.currentTime = this.audio.currentTime;
      } else {
        this.currentTime += 0.02;
        if (this.currentTime >= this.totalDuration) {
          this.onVideoEnd();
        }
      }
    }

    // Update UI elements
    const progressRatio = Math.min(1, this.currentTime / this.totalDuration);
    if (this.progressBar) {
      this.progressBar.style.width = (progressRatio * 100) + '%';
    }
    if (this.scrubberThumb) {
      this.scrubberThumb.style.left = (progressRatio * 100) + '%';
    }

    if (this.timeDisplay) {
      const curM = Math.floor(this.currentTime / 60);
      const curS = Math.floor(this.currentTime % 60);
      const totM = Math.floor(this.totalDuration / 60);
      const totS = Math.floor(this.totalDuration % 60);
      const fmtCur = (curM < 10 ? '0' : '') + curM + ':' + (curS < 10 ? '0' : '') + curS;
      const fmtTot = (totM < 10 ? '0' : '') + totM + ':' + (totS < 10 ? '0' : '') + totS;
      this.timeDisplay.innerText = `${fmtCur} / ${fmtTot}`;
    }

    // Subtitle progress
    if (this.subtitleEl && this.captions && this.captions.length > 0) {
      const step = this.totalDuration / this.captions.length;
      const capIdx = Math.min(this.captions.length - 1, Math.floor(this.currentTime / step));
      if (this.subtitleEl.innerText !== this.captions[capIdx]) {
        this.subtitleEl.innerText = this.captions[capIdx];
      }
    }
  }

  draw() {
    if (!this.ctx) return;
    const ctx = this.ctx;
    ctx.clearRect(0, 0, 854, 480);

    const progressRatio = Math.min(1, this.currentTime / this.totalDuration);

    // 1. Ken Burns Moving Picture Camera Motion
    if (this.bgLoaded && this.bgImg.width > 0) {
      const zoom = 1.0 + (progressRatio * 0.20);
      const maxPanX = this.bgImg.width * (zoom - 1);
      const panX = Math.sin(progressRatio * Math.PI) * (maxPanX * 0.5);
      const maxPanY = this.bgImg.height * (zoom - 1);
      const panY = progressRatio * (maxPanY * 0.35);

      const srcW = this.bgImg.width / zoom;
      const srcH = this.bgImg.height / zoom;
      const srcX = Math.max(0, Math.min(this.bgImg.width - srcW, ((this.bgImg.width - srcW) / 2) + panX));
      const srcY = Math.max(0, Math.min(this.bgImg.height - srcH, ((this.bgImg.height - srcH) / 2) + panY));

      ctx.drawImage(this.bgImg, srcX, srcY, srcW, srcH, 0, 0, 854, 480);

      // Vignette
      const vig = ctx.createRadialGradient(427, 240, 180, 427, 240, 480);
      vig.addColorStop(0, 'rgba(0, 0, 0, 0)');
      vig.addColorStop(0.7, 'rgba(0, 0, 0, 0.2)');
      vig.addColorStop(1, 'rgba(0, 0, 0, 0.65)');
      ctx.fillStyle = vig;
      ctx.fillRect(0, 0, 854, 480);
    } else {
      // Fallback ambient
      const grad = ctx.createLinearGradient(0, 0, 0, 480);
      grad.addColorStop(0, '#0F172A');
      grad.addColorStop(0.5, '#1E293B');
      grad.addColorStop(1, '#78350F');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 854, 480);
    }

    // 2. Dynamic Physical Overlays matching each day
    switch (this.currentDay) {
      case 0: // Monday Coffee
        this.drawSteam(550, 360);
        this.drawLightBeams();
        this.drawBirds();
        break;
      case 1: // Tuesday Vintage Music
        this.drawMusicNotes();
        this.drawBokeh();
        break;
      case 2: // Wednesday Courtyard Rain
        this.drawRain();
        this.drawPetals();
        break;
      case 3: // Thursday Banyan Lamp
        this.drawDancingFlame(595, 290);
        this.drawFireflies();
        break;
      case 4: // Friday Serene River
        this.drawRiverGlints();
        this.drawPetals();
        break;
      case 5: // Saturday Temple Bells
      case 6: // Sunday Hearth
        this.drawStars();
        this.drawBokeh();
        break;
      default:
        this.drawBokeh();
    }
  }

  // --- Particle Overlays ---
  drawDancingFlame(x, y) {
    const ctx = this.ctx;
    ctx.save();
    const halo = ctx.createRadialGradient(x, y - 20, 8, x, y - 20, 140);
    const pulse = (Math.sin(this.animTime * 8) + 1) * 0.15;
    halo.addColorStop(0, `rgba(254, 240, 138, ${0.8 + pulse})`);
    halo.addColorStop(0.35, `rgba(245, 158, 11, ${0.45 + pulse * 0.5})`);
    halo.addColorStop(0.7, 'rgba(217, 119, 6, 0.15)');
    halo.addColorStop(1, 'transparent');
    ctx.fillStyle = halo;
    ctx.beginPath();
    ctx.arc(x, y - 20, 140, 0, Math.PI * 2);
    ctx.fill();

    const flick = Math.sin(this.animTime * 16) * 3 + Math.cos(this.animTime * 24) * 2;
    const flameH = 38 + flick;

    ctx.fillStyle = '#EF4444';
    ctx.beginPath();
    ctx.moveTo(x - 12, y);
    ctx.quadraticCurveTo(x - 16, y - flameH * 0.6, x + flick * 0.6, y - flameH);
    ctx.quadraticCurveTo(x + 16, y - flameH * 0.6, x + 12, y);
    ctx.fill();

    ctx.fillStyle = '#F59E0B';
    ctx.beginPath();
    ctx.moveTo(x - 8, y);
    ctx.quadraticCurveTo(x - 10, y - flameH * 0.5, x + flick * 0.4, y - flameH * 0.85);
    ctx.quadraticCurveTo(x + 10, y - flameH * 0.5, x + 8, y);
    ctx.fill();

    ctx.fillStyle = '#FEF08A';
    ctx.beginPath();
    ctx.moveTo(x - 4, y);
    ctx.quadraticCurveTo(x - 5, y - flameH * 0.35, x + flick * 0.2, y - flameH * 0.6);
    ctx.quadraticCurveTo(x + 5, y - flameH * 0.35, x + 4, y);
    ctx.fill();
    ctx.restore();
  }

  drawSteam(x, y) {
    const ctx = this.ctx;
    ctx.save();
    for (let s = 0; s < this.steamParticles.length; s++) {
      const p = this.steamParticles[s];
      p.y += p.vy;
      p.x += Math.sin(this.animTime * 2.5 + p.age) * 0.7;
      p.alpha -= 0.008;
      p.radius += 0.12;

      ctx.fillStyle = `rgba(255, 255, 255, ${Math.max(0, p.alpha * 0.45)})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();

      if (p.alpha <= 0 || p.y < y - 180) {
        p.x = x + (Math.random() - 0.5) * 22;
        p.y = y;
        p.alpha = 0.6;
        p.radius = 6 + Math.random() * 5;
      }
    }
    ctx.restore();
  }

  drawLightBeams() {
    const ctx = this.ctx;
    ctx.save();
    const beam = ctx.createLinearGradient(0, 0, 854, 480);
    const p = (Math.sin(this.animTime * 1.5) + 1) * 0.06;
    beam.addColorStop(0, `rgba(254, 240, 138, ${0.12 + p})`);
    beam.addColorStop(0.5, `rgba(245, 158, 11, ${0.05 + p})`);
    beam.addColorStop(1, 'transparent');
    ctx.fillStyle = beam;
    ctx.fillRect(0, 0, 854, 480);
    ctx.restore();
  }

  drawMusicNotes() {
    const ctx = this.ctx;
    for (let m = 0; m < this.musicNotes.length; m++) {
      const n = this.musicNotes[m];
      n.y += n.vy;
      n.x += Math.sin(this.animTime * 2.5 + n.phase) * 1.0;
      if (n.y < 60) {
        n.y = 310;
        n.x = 430 + (Math.random() - 0.5) * 60;
      }
      ctx.fillStyle = `rgba(254, 240, 138, ${n.alpha})`;
      ctx.font = `bold ${n.size}px serif`;
      ctx.fillText(n.sym, n.x, n.y);
    }
  }

  drawRain() {
    const ctx = this.ctx;
    ctx.strokeStyle = 'rgba(224, 242, 254, 0.55)';
    ctx.lineWidth = 1.5;
    for (let i = 0; i < this.raindrops.length; i++) {
      const d = this.raindrops[i];
      ctx.beginPath();
      ctx.moveTo(d.x, d.y);
      ctx.lineTo(d.x - 2, d.y + d.len);
      ctx.stroke();
      d.y += d.speed;
      d.x -= 0.6;
      if (d.y > 480) {
        d.y = -20;
        d.x = Math.random() * 854;
      }
    }
  }

  drawRiverGlints() {
    const ctx = this.ctx;
    ctx.save();
    for (let g = 0; g < 18; g++) {
      const gx = (g * 48 + this.animTime * 35) % 854;
      const gy = 320 + Math.sin(this.animTime * 3 + g) * 60;
      const sp = (Math.sin(this.animTime * 6 + g) + 1) * 0.45;
      ctx.fillStyle = `rgba(254, 240, 138, ${sp})`;
      ctx.beginPath();
      ctx.arc(gx, gy, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  drawBirds() {
    const ctx = this.ctx;
    ctx.strokeStyle = '#FEF08A';
    ctx.lineWidth = 2.2;
    const baseBirdX = ((this.animTime * 55) % 950) - 80;
    const wingFlap = Math.sin(this.animTime * 9) * 8;
    for (let b = 0; b < 4; b++) {
      const bx = baseBirdX - (b * 45);
      const by = 90 + (b * 22) + Math.sin(this.animTime + b) * 10;
      ctx.beginPath();
      ctx.moveTo(bx - 12, by + wingFlap);
      ctx.quadraticCurveTo(bx - 6, by - 6, bx, by);
      ctx.quadraticCurveTo(bx + 6, by - 6, bx + 12, by + wingFlap);
      ctx.stroke();
    }
  }

  drawFireflies() {
    const ctx = this.ctx;
    for (let f = 0; f < 12; f++) {
      const fx = 320 + Math.sin(this.animTime * 1.2 + f) * 180;
      const fy = 220 + Math.cos(this.animTime * 1.8 + f * 2) * 90;
      const alpha = (Math.sin(this.animTime * 4 + f) + 1) * 0.45;
      ctx.fillStyle = `rgba(254, 240, 138, ${alpha})`;
      ctx.beginPath();
      ctx.arc(fx, fy, 4, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  drawPetals() {
    const ctx = this.ctx;
    for (let p = 0; p < 14; p++) {
      const px = (p * 65 + (this.animTime * 30)) % 854;
      const py = (p * 45 + (this.animTime * 25)) % 460;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
      ctx.beginPath();
      ctx.ellipse(px, py, 6, 3, this.animTime + p, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  drawBokeh() {
    const ctx = this.ctx;
    for (let b = 0; b < this.particles.length; b++) {
      const pt = this.particles[b];
      pt.y += pt.vy;
      pt.x += pt.vx;
      if (pt.y < -10) pt.y = 490;
      if (pt.x < -10) pt.x = 864;
      if (pt.x > 864) pt.x = -10;

      const pulse = (Math.sin(this.animTime * 2 + pt.phase) + 1) * 0.5;
      ctx.fillStyle = `rgba(254, 240, 138, ${pt.alpha * pulse})`;
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  drawStars() {
    const ctx = this.ctx;
    for (let s = 0; s < 25; s++) {
      const sx = (s * 87 + 45) % 854;
      const sy = (s * 43 + 20) % 210;
      const alpha = (Math.sin(this.animTime * 3 + s) + 1) * 0.45;
      ctx.fillStyle = `rgba(254, 240, 138, ${alpha})`;
      ctx.beginPath();
      ctx.arc(sx, sy, 1.8, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  togglePlay() {
    if (this.isPlaying) {
      this.isPlaying = false;
      if (this.audio) this.audio.pause();
      if (this.playBtn) this.playBtn.innerText = '▶';
    } else {
      this.isPlaying = true;
      if (this.audio) this.audio.play().catch(() => {});
      if (this.playBtn) this.playBtn.innerText = '❚❚';
    }
  }

  toggleMute() {
    if (this.audio) {
      this.isMuted = !this.isMuted;
      this.audio.muted = this.isMuted;
      if (this.muteBtn) this.muteBtn.innerText = this.isMuted ? '🔇' : '🔊';
    }
  }

  seek(ratio) {
    this.currentTime = ratio * this.totalDuration;
    if (this.audio) {
      this.audio.currentTime = this.currentTime;
    }
  }

  onVideoEnd() {
    this.isPlaying = false;
    if (this.playBtn) this.playBtn.innerText = '▶';
    const endModal = document.getElementById('cinemaEndModal');
    if (endModal) endModal.style.display = 'flex';
  }

  replay() {
    const endModal = document.getElementById('cinemaEndModal');
    if (endModal) endModal.style.display = 'none';
    this.currentTime = 0;
    if (this.audio) {
      this.audio.currentTime = 0;
      this.audio.play().catch(() => {});
    }
    this.isPlaying = true;
    if (this.playBtn) this.playBtn.innerText = '❚❚';
  }
}
