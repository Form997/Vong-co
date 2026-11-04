"""Shared, progressively enhanced task navigation for every published page."""
import posixpath
from html import escape

ICONS = (
    '<path d="m3 10 9-7 9 7v10H3z"/><path d="M9 20v-7h6v7"/>',
    '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
    '<path d="M9 18V5l12-2v13M9 9l12-2"/><ellipse cx="6" cy="18" rx="3" ry="2"/><ellipse cx="18" cy="16" rx="3" ry="2"/>',
    '<path d="M12 5C9 3 5 3 2 4v15c3-1 7-1 10 1 3-2 7-2 10-1V4c-3-1-7-1-10 1v15"/>',
)


def navigation_for(relative):
    home = relative == 'web/v3/index.html'
    base = '' if home else posixpath.relpath('web/v3/', posixpath.dirname(relative) or '.') + '/'
    active = 'ly' if relative.startswith('ly/') else ('search' if relative.startswith(('bai/', 'nhom/')) else 'home')
    items = [('home', 'dau-trang', 'Trang chủ'), ('search', 'tra-cuu', 'Tra cứu'),
             ('ly', 'bai-ly', 'Bài lý'), ('sources', 'nguon', 'Nguồn')]
    links = []
    for (key, anchor, label), icon in zip(items, ICONS):
        current = ' aria-current="page"' if key == active else ''
        links.append(f'<a href="{escape(base + "#" + anchor, quote=True)}" data-task="{key}"{current}>'
                     f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg><span>{label}</span></a>')
    return '<nav class="taskbar" aria-label="Thanh tác vụ thư viện">'+''.join(links)+'</nav>'
