'use strict';

// Le SVG rimangono vettoriali: la telecamera viene simulata modificando il viewBox.
// La presentazione e la sequenza delle inquadrature sono definite in presentation.json.
let presentation = null;
let slides = [];
let defaults = { duration: 1050, padding: 0.08 };

async function loadManifest(path = 'presentation.json') {
  const response = await fetch(path, { cache: 'no-cache' });
  if (!response.ok) {
    throw new Error(`Impossibile caricare il manifesto ${path} (${response.status})`);
  }

  const manifest = await response.json();
  if (!manifest || !Array.isArray(manifest.slides)) {
    throw new Error('Manifesto non valido: manca l\'array "slides"');
  }

  const activeSlides = manifest.slides.filter(slide => slide.enabled !== false);
  if (activeSlides.length === 0) {
    throw new Error('Il manifesto non contiene SVG abilitate');
  }

  for (const slide of activeSlides) {
    if (!slide.title || !slide.src || !Array.isArray(slide.frames) || slide.frames.length === 0) {
      throw new Error(`Configurazione incompleta per la slide "${slide.id || 'senza id'}"`);
    }
  }

  presentation = manifest;
  slides = activeSlides;
  defaults = { ...defaults, ...(manifest.defaults || {}) };
  document.title = manifest.title || document.title;
}

const stage = document.querySelector('#stage');
const status = document.querySelector('#status');
const frameTitle = document.querySelector('#frame-title');
const counter = document.querySelector('#counter');
const frameButtons = document.querySelector('#frame-buttons');
const previousButton = document.querySelector('#previous');
const nextButton = document.querySelector('#next');
const topActions = document.querySelector('.top-actions');
const slideSelect = document.createElement('select');
slideSelect.id = 'slide-select';
slideSelect.setAttribute('aria-label', 'Vai alla slide');
slideSelect.title = 'Vai alla slide';
let svgRoot;
let slideIndex = 0;
let frameIndex = 0;
let currentViewBox;
let animationId = 0;
let frameTargets = [];
let frameFocusRects = [];
let focusOverlay = null;

const sleepFrame = () => new Promise(resolve => requestAnimationFrame(resolve));

function buildSlideSelector() {
  slideSelect.replaceChildren();
  slides.forEach((slide, index) => {
    const option = document.createElement('option');
    option.value = String(index);
    option.textContent = `${index + 1}. ${slide.title}`;
    slideSelect.append(option);
  });
  slideSelect.value = String(slideIndex);
  topActions?.prepend(slideSelect);
}
async function goToSlide(index) {
  const target = Math.max(0, Math.min(Number(index), slides.length - 1));
  if (!Number.isFinite(target) || target === slideIndex) return;
  slideIndex = target;
  await loadSlide(slideIndex);
}
const easeInOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

function parseViewBox(svg) {
  const raw = svg.getAttribute('viewBox');
  if (raw) return raw.trim().split(/[ ,]+/).map(Number);
  return [0, 0, Number(svg.getAttribute('width')) || 1920, Number(svg.getAttribute('height')) || 1080];
}

function viewBoxForRect(rect, base, padding = 0.10) {
  const aspect = base[2] / base[3];
  const widthFromRect = rect.width * (1 + padding * 2);
  const heightFromRect = rect.height * (1 + padding * 2);
  // Mantiene il rapporto 16:9 della slide e include l'intero pannello.
  const width = Math.max(widthFromRect, heightFromRect * aspect);
  const height = width / aspect;
  const cx = rect.x + rect.width / 2;
  const cy = rect.y + rect.height / 2;
  return [cx - width / 2, cy - height / 2, width, height];
}

function setViewBox(box) {
  svgRoot.setAttribute('viewBox', box.map(v => Number(v.toFixed(3))).join(' '));
  currentViewBox = box.slice();
  updateFocusOverlay();
}

function createFocusOverlay() {
  focusOverlay = document.createElement('div');
  focusOverlay.className = 'focus-overlay';
  focusOverlay.setAttribute('aria-hidden', 'true');
  for (const side of ['top', 'right', 'bottom', 'left']) {
    const part = document.createElement('div');
    part.className = `focus-blur focus-blur-${side}`;
    focusOverlay.append(part);
  }
  stage.append(focusOverlay);
}

function updateFocusOverlay() {
  if (!focusOverlay || !currentViewBox) return;
  const rect = frameFocusRects[frameIndex];
  focusOverlay.classList.toggle('is-active', Boolean(rect));
  if (!rect) return;

  const [vx, vy, vw, vh] = currentViewBox;
  const x1 = Math.max(0, Math.min(100, (rect.x - vx) / vw * 100));
  const y1 = Math.max(0, Math.min(100, (rect.y - vy) / vh * 100));
  const x2 = Math.max(0, Math.min(100, (rect.x + rect.width - vx) / vw * 100));
  const y2 = Math.max(0, Math.min(100, (rect.y + rect.height - vy) / vh * 100));
  const [top, right, bottom, left] = focusOverlay.children;
  top.style.cssText = `left:0;top:0;width:100%;height:${y1}%`;
  bottom.style.cssText = `left:0;top:${y2}%;width:100%;height:${100-y2}%`;
  left.style.cssText = `left:0;top:${y1}%;width:${x1}%;height:${y2-y1}%`;
  right.style.cssText = `left:${x2}%;top:${y1}%;width:${100-x2}%;height:${y2-y1}%`;
}

function animateCamera(target, duration = 1050) {
  cancelAnimationFrame(animationId);
  const start = currentViewBox.slice();
  const started = performance.now();
  return new Promise(resolve => {
    const tick = now => {
      const t = Math.min(1, (now - started) / duration);
      const k = easeInOut(t);
      const box = start.map((v, i) => v + (target[i] - v) * k);
      setViewBox(box);
      if (t < 1) animationId = requestAnimationFrame(tick);
      else resolve();
    };
    animationId = requestAnimationFrame(tick);
  });
}

function updateControls() {
  const slide = slides[slideIndex];
  frameTitle.textContent = slide.frames[frameIndex].label;
  counter.textContent = `${frameIndex + 1} / ${slide.frames.length}`;
  previousButton.disabled = slideIndex === 0 && frameIndex === 0;
  nextButton.disabled = slideIndex === slides.length - 1 && frameIndex === slide.frames.length - 1;
  document.querySelector('h1').textContent = slide.title;
  [...frameButtons.children].forEach((button, i) => {
    if (i === frameIndex) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  });
}

async function goToFrame(index, animate = true) {
  if (!frameTargets.length) return;
  frameIndex = Math.max(0, Math.min(index, frameTargets.length - 1));
  updateControls();
  const target = frameTargets[frameIndex];
  if (animate) {
    const frame = slides[slideIndex].frames[frameIndex];
    await animateCamera(target, frame.duration ?? defaults.duration);
  }
  else setViewBox(target);
}

async function step(delta) {
  const target = frameIndex + delta;
  if (target >= 0 && target < frameTargets.length) return goToFrame(target);
  const nextSlide = slideIndex + (delta > 0 ? 1 : -1);
  if (nextSlide < 0 || nextSlide >= slides.length) return;
  slideIndex = nextSlide;
  await loadSlide(slideIndex);
  if (delta < 0) await goToFrame(frameTargets.length - 1);
}

function buildFrameTargets() {
  const base = parseViewBox(svgRoot);
  const frames = slides[slideIndex].frames;
  frameFocusRects = [];
  frameTargets = frames.map(frame => {
    if (frame.id === 'overview') {
      frameFocusRects.push(null);
      return base;
    }
    const panel = svgRoot.querySelector(`#${CSS.escape(frame.id)}`);
    if (!panel) throw new Error(`Nel file SVG manca il gruppo #${frame.id}`);
    const b = panel.getBBox();
    frameFocusRects.push({ x: b.x, y: b.y, width: b.width, height: b.height });
    return viewBoxForRect(b, base, frame.padding ?? defaults.padding);
  });
}

async function loadSlide(index) {
  status.textContent = 'Caricamento SVG…';
  const response = await fetch(slides[index].src, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`Impossibile caricare l'SVG (${response.status})`);
  const source = await response.text();
  const parsed = new DOMParser().parseFromString(source, 'image/svg+xml');
  if (parsed.querySelector('parsererror')) throw new Error('Il file ricevuto non è un SVG valido');
  const imported = document.importNode(parsed.documentElement, true);
  imported.removeAttribute('width');
  imported.removeAttribute('height');
  imported.setAttribute('width', '100%');
  imported.setAttribute('height', '100%');
  imported.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  stage.replaceChildren(imported);
  svgRoot = imported;
  createFocusOverlay();
  // Attende il layout: getBBox() deve essere eseguito dopo l'inserimento nel DOM.
  await sleepFrame();
  buildFrameTargets();
  frameButtons.replaceChildren();
  slides[index].frames.forEach((frame, i) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = frame.label;
    button.addEventListener('click', () => goToFrame(i));
    frameButtons.append(button);
  });
  frameIndex = 0;
  setViewBox(frameTargets[0]);
  updateControls();
  status.textContent = 'SVG vettoriale · pronto';
}

previousButton.addEventListener('click', () => step(-1));
nextButton.addEventListener('click', () => step(1));
slideSelect.addEventListener('change', () => goToSlide(slideSelect.value).catch(showError));
document.querySelector('#fullscreen').addEventListener('click', async () => {
  if (!document.fullscreenElement) await document.querySelector('.app').requestFullscreen?.();
  else await document.exitFullscreen?.();
});
document.addEventListener('keydown', event => {
  if (event.target instanceof HTMLButtonElement) return;
  if (event.key === 'ArrowRight' || event.key === ' ') { event.preventDefault(); step(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
  if (event.key.toLowerCase() === 'f') document.querySelector('#fullscreen').click();
});

function showError(error) {
  console.error(error);
  status.textContent = 'Errore';
  const message = document.createElement('div');
  message.className = 'error';
  message.textContent = `${error.message} Avvia la demo tramite un server HTTP locale e verifica i percorsi nel manifesto.`;
  stage.replaceChildren(message);
}

async function start() {
  const params = new URLSearchParams(window.location.search);
  const manifestPath = params.get('presentation') || 'presentation.json';
  await loadManifest(manifestPath);
  buildSlideSelector();
  slideIndex = 0;
  await loadSlide(slideIndex);
}

start().catch(showError);
