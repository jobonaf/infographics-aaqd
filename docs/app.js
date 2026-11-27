'use strict';

let presentation = null;
let slides = [];
let defaults = { duration: 1050, padding: 0.08, slideDuration: 650 };

async function loadManifest(path = 'presentation.json') {
  const response = await fetch(path, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`Impossibile caricare il manifesto ${path} (${response.status})`);
  const manifest = await response.json();
  if (!manifest || !Array.isArray(manifest.slides)) throw new Error('Manifesto non valido: manca l\'array "slides"');
  const activeSlides = manifest.slides.filter(slide => slide.enabled !== false);
  if (!activeSlides.length) throw new Error('Il manifesto non contiene SVG abilitate');
  for (const slide of activeSlides) {
    if (!slide.title || (!slide.src && !slide.content) || !Array.isArray(slide.frames) || !slide.frames.length) {
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
let slideTransitioning = false;

const sleepFrame = () => new Promise(resolve => requestAnimationFrame(resolve));
const waitTransition = (element, fallback) => new Promise(resolve => {
  let done = false;
  const finish = () => { if (!done) { done = true; resolve(); } };
  element.addEventListener('transitionend', finish, { once: true });
  setTimeout(finish, fallback);
});

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
  if (!Number.isFinite(target) || target === slideIndex || slideTransitioning) return;
  const direction = target > slideIndex ? 1 : -1;
  slideIndex = target;
  await loadSlide(slideIndex, direction);
}

const easeInOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

function parseViewBox(svg) {
  const raw = svg.getAttribute('viewBox');
  if (raw) return raw.trim().split(/[ ,]+/).map(Number);
  return [0, 0, Number(svg.getAttribute('width')) || 1920, Number(svg.getAttribute('height')) || 1080];
}

function viewBoxForRect(rect, base, padding = 0.10) {
  const aspect = base[2] / base[3];
  const width = Math.max(rect.width * (1 + padding * 2), rect.height * (1 + padding * 2) * aspect);
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
      setViewBox(start.map((v, i) => v + (target[i] - v) * k));
      if (t < 1) animationId = requestAnimationFrame(tick); else resolve();
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
  slideSelect.value = String(slideIndex);
  [...frameButtons.children].forEach((button, i) => {
    if (i === frameIndex) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  });
}

async function goToFrame(index, animate = true) {
  if (!frameTargets.length || slideTransitioning) return;
  frameIndex = Math.max(0, Math.min(index, frameTargets.length - 1));
  updateControls();
  const target = frameTargets[frameIndex];
  if (!svgRoot) return;
  if (animate) {
    const frame = slides[slideIndex].frames[frameIndex];
    await animateCamera(target, frame.duration ?? defaults.duration);
  } else setViewBox(target);
}

async function step(delta) {
  if (slideTransitioning) return;
  const target = frameIndex + delta;
  if (target >= 0 && target < frameTargets.length) return goToFrame(target);
  const nextSlide = slideIndex + (delta > 0 ? 1 : -1);
  if (nextSlide < 0 || nextSlide >= slides.length) return;
  slideIndex = nextSlide;
  await loadSlide(slideIndex, delta > 0 ? 1 : -1);
  if (delta < 0) await goToFrame(frameTargets.length - 1, false);
}

function buildFrameTargets() {
  const base = parseViewBox(svgRoot);
  frameFocusRects = [];
  frameTargets = slides[slideIndex].frames.map(frame => {
    if (frame.id === 'overview') { frameFocusRects.push(null); return base; }
    const panel = svgRoot.querySelector(`#${CSS.escape(frame.id)}`);
    if (!panel) throw new Error(`Nel file SVG manca il gruppo #${frame.id}`);
    const b = panel.getBBox();
    frameFocusRects.push({ x: b.x, y: b.y, width: b.width, height: b.height });
    return viewBoxForRect(b, base, frame.padding ?? defaults.padding);
  });
}

function createTextSlide(slide) {
  const content = slide.content || {};
  const article = document.createElement('article');
  article.className = 'text-slide';

  const eyebrow = document.createElement('div');
  eyebrow.className = 'text-slide-eyebrow';
  eyebrow.textContent = content.eyebrow || '';

  const heading = document.createElement('h2');
  heading.textContent = content.heading || slide.title;

  const subtitle = document.createElement('p');
  subtitle.className = 'text-slide-subtitle';
  subtitle.textContent = content.subtitle || '';

  const lines = document.createElement('div');
  lines.className = 'text-slide-lines';
  for (const value of content.lines || []) {
    const line = document.createElement('p');
    line.textContent = value;
    lines.append(line);
  }

  const footer = document.createElement('p');
  footer.className = 'text-slide-footer';
  footer.textContent = content.footer || '';

  article.append(eyebrow, heading, subtitle, lines, footer);
  return article;
}

async function fetchSvg(index) {
  const response = await fetch(slides[index].src, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`Impossibile caricare l'SVG (${response.status})`);
  const parsed = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
  if (parsed.querySelector('parsererror')) throw new Error('Il file ricevuto non è un SVG valido');
  const imported = document.importNode(parsed.documentElement, true);
  imported.removeAttribute('width'); imported.removeAttribute('height');
  imported.setAttribute('width', '100%'); imported.setAttribute('height', '100%');
  imported.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  imported.classList.add('slide-svg');
  return imported;
}

async function createSlideElement(index) {
  const slide = slides[index];
  return (slide.type === 'text' || (!slide.src && slide.content)) ? createTextSlide(slide) : fetchSvg(index);
}

async function swapSlide(imported, direction) {
  const oldSvg = svgRoot;
  const oldOverlay = focusOverlay;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!oldSvg || !direction || reduced) {
    stage.replaceChildren(imported);
    return;
  }

  slideTransitioning = true;
  const duration = Number(defaults.slideDuration) || 650;
  const easing = 'cubic-bezier(.22,.61,.36,1)';
  const startY = direction > 0 ? '100%' : '-100%';
  const endY = direction > 0 ? '-100%' : '100%';

  imported.style.position = 'absolute';
  imported.style.inset = '0';
  imported.style.zIndex = '2';
  oldSvg.style.position = 'absolute';
  oldSvg.style.inset = '0';
  oldSvg.style.zIndex = '1';
  if (oldOverlay) oldOverlay.style.zIndex = '3';
  stage.append(imported);

  const incomingAnimation = imported.animate(
    [{ transform: `translateY(${startY})` }, { transform: 'translateY(0)' }],
    { duration, easing, fill: 'forwards' }
  );
  const outgoingAnimation = oldSvg.animate(
    [{ transform: 'translateY(0)' }, { transform: `translateY(${endY})` }],
    { duration, easing, fill: 'forwards' }
  );
  const overlayAnimation = oldOverlay?.animate(
    [{ transform: 'translateY(0)' }, { transform: `translateY(${endY})` }],
    { duration, easing, fill: 'forwards' }
  );

  await Promise.all([
    incomingAnimation.finished,
    outgoingAnimation.finished,
    overlayAnimation?.finished ?? Promise.resolve(),
  ]);

  oldSvg.remove();
  oldOverlay?.remove();
  imported.getAnimations().forEach(animation => animation.cancel());
  imported.style.position = '';
  imported.style.inset = '';
  imported.style.zIndex = '';
  imported.style.transform = '';
  slideTransitioning = false;
}

async function loadSlide(index, direction = 0) {
  status.textContent = 'Caricamento SVG…';
  const imported = await createSlideElement(index);
  await swapSlide(imported, direction);
  svgRoot = imported.matches('svg') ? imported : null;
  focusOverlay = null;
  if (svgRoot) {
    createFocusOverlay();
    await sleepFrame();
    buildFrameTargets();
  } else {
    frameTargets = [null];
    frameFocusRects = [null];
  }
  frameButtons.replaceChildren();
  slides[index].frames.forEach((frame, i) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = frame.label;
    button.addEventListener('click', () => goToFrame(i));
    frameButtons.append(button);
  });
  frameIndex = 0;
  if (svgRoot) setViewBox(frameTargets[0]);
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
  if (event.target instanceof HTMLButtonElement || event.target instanceof HTMLSelectElement) return;
  if (event.key === 'ArrowRight' || event.key === ' ') { event.preventDefault(); step(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
  if (event.key.toLowerCase() === 'f') document.querySelector('#fullscreen').click();
});

function showError(error) {
  console.error(error); status.textContent = 'Errore';
  const message = document.createElement('div');
  message.className = 'error';
  message.textContent = `${error.message} Avvia la demo tramite un server HTTP locale e verifica i percorsi nel manifesto.`;
  stage.replaceChildren(message);
  slideTransitioning = false;
}

async function start() {
  const params = new URLSearchParams(window.location.search);
  const requested = params.get('presentation');

  if (requested) {
    await loadManifest(requested);
  } else {
    try {
      await loadManifest('presentation.sequence.json');
    } catch {
      await loadManifest('presentation.json');
    }
  }
  buildSlideSelector();
  slideIndex = 0;
  await loadSlide(slideIndex);
}
start().catch(showError);
