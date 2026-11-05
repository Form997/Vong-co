/* Reading preferences stay on this device; unavailable storage is harmless. */
(() => {
  'use strict';
  const panel = document.querySelector('.reading-tools');
  if (!panel) return;
  const key = 'hai-dat-reading-v1';
  const labels = ['Mặc định', 'Lớn', 'Rất lớn'];
  let size = 0, focused = false;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && Number.isInteger(saved.size) && saved.size >= 0 && saved.size <= 2) size = saved.size;
    if (saved && typeof saved.focused === 'boolean') focused = saved.focused;
  } catch (_) { /* Keep defaults if storage is blocked or malformed. */ }
  function apply(save = false) {
    document.body.dataset.readingSize = String(size);
    document.body.dataset.readingFocus = String(focused);
    panel.querySelector('output').textContent = labels[size];
    panel.querySelector('[data-reading="smaller"]').disabled = size === 0;
    panel.querySelector('[data-reading="larger"]').disabled = size === 2;
    panel.querySelector('[data-reading="focus"]').setAttribute('aria-pressed', String(focused));
    if (save) {
      try { localStorage.setItem(key, JSON.stringify({size, focused})); } catch (_) { /* Optional persistence. */ }
    }
  }
  panel.hidden = false;
  apply();
  panel.addEventListener('click', event => {
    const button = event.target.closest('button[data-reading]');
    if (!button) return;
    const action = button.dataset.reading;
    if (action === 'top') {
      const heading = document.querySelector('main h1');
      if (heading) { heading.setAttribute('tabindex', '-1'); heading.focus({preventScroll:true}); }
      window.scrollTo({top:0, behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
      return;
    }
    if (action === 'larger') size = Math.min(2, size + 1);
    if (action === 'smaller') size = Math.max(0, size - 1);
    if (action === 'focus') focused = !focused;
    if (action === 'reset') {
      size = 0; focused = false;
      try { localStorage.removeItem(key); } catch (_) { /* Optional storage. */ }
      apply();
    } else apply(true);
  });
})();

/* Section tracking changes only the navigation state, never filters or history. */
(() => {
  'use strict';
  const nav = document.querySelector('.taskbar');
  if (!nav || !document.getElementById('tra-cuu')) return;
  const links = [...nav.querySelectorAll('a[data-task]')];
  const sections = [['home','dau-trang'],['search','tra-cuu'],['ly','bai-ly'],['sources','nguon']]
    .map(([key,id]) => ({key,element:document.getElementById(id)})).filter(s => s.element);
  function activate(key) {
    for (const link of links) {
      if (link.dataset.task === key) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    }
  }
  let queued = false;
  function track() {
    queued = false;
    let current = sections[0].key;
    for (const section of sections) if (section.element.getBoundingClientRect().top <= 150) current = section.key;
    activate(current);
  }
  window.addEventListener('scroll', () => {
    if (!queued) {queued=true; requestAnimationFrame(track);}
  }, {passive:true});
  nav.addEventListener('click', event => {
    const link = event.target.closest('a[data-task]');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    activate(link.dataset.task);
    if (link.dataset.task === 'search') {
      event.preventDefault();
      if (location.hash !== '#tra-cuu') {
        const url = new URL(location.href);
        url.hash = 'tra-cuu';
        history.pushState(null, '', url);
      }
      document.getElementById('tra-cuu').scrollIntoView({block:'start'});
      document.getElementById('search')?.focus({preventScroll:true});
    }
  });
  track();
})();
