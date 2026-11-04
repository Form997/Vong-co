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
