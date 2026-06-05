// Mobile nav
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target))
      navLinks.classList.remove('open');
  });
}

// Animate bars on scroll
function animateBars(selector) {
  const bars = document.querySelectorAll(selector);
  if (!bars.length) return;
  const widths = Array.from(bars).map(b => (b.dataset.width || '0') + '%');
  bars.forEach(b => b.style.width = '0');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const idx = Array.from(bars).indexOf(entry.target);
        setTimeout(() => { entry.target.style.width = widths[idx]; }, idx * 30);
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  bars.forEach(b => obs.observe(b));
}
animateBars('.similarity-bar');
animateBars('.diff-bar');

// Animate cards
const cards = document.querySelectorAll('.step-card, .distro-card, .alt-item, .rec-distro, .guide-step');
if (cards.length && 'IntersectionObserver' in window) {
  cards.forEach(el => { el.style.opacity='0'; el.style.transform='translateY(14px)'; el.style.transition='opacity 0.4s ease, transform 0.4s ease'; });
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setTimeout(() => { entry.target.style.opacity='1'; entry.target.style.transform='translateY(0)'; }, 50);
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  cards.forEach(el => obs.observe(el));
}

console.log('%c[LinuxMigrator] Ready', 'color:#22c55e;font-weight:bold;font-family:monospace');
