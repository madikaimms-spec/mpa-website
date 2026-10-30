  // Old one-page links (/#gallery etc.) go to the new pages
  const OLD = { about: '/about', initiatives: '/initiatives', bearers: '/office-bearers', events: '/events', gallery: '/gallery', contact: '/contact', support: '/contact' };
  if ((location.pathname === '/' || location.pathname === '/index.html') && OLD[location.hash.slice(1)]) location.replace(OLD[location.hash.slice(1)]);

  document.getElementById('y').textContent = new Date().getFullYear();
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('nav');
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? 'Close' : 'Menu';
  });
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
    nav.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = 'Menu';
  }));

  // Gallery lightbox (gallery page only)
  (() => {
  const lb = document.getElementById('lb');
  if (!lb) return;
  const items = [...document.querySelectorAll('.gallery-grid button')];
  const lbImg = document.getElementById('lb-img');
  let cur = 0, opener = null;
  function show(i) {
    cur = (i + items.length) % items.length;
    const img = items[cur].querySelector('img');
    lbImg.src = img.src; lbImg.alt = img.alt;
  }
  function openLb(i) { opener = items[i]; show(i); lb.classList.add('open'); document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); }
  function closeLb() { lb.classList.remove('open'); document.body.style.overflow = ''; if (opener) opener.focus(); }
  items.forEach((b, i) => b.addEventListener('click', () => openLb(i)));
  lb.querySelector('.lb-close').addEventListener('click', closeLb);
  lb.querySelector('.lb-prev').addEventListener('click', () => show(cur - 1));
  lb.querySelector('.lb-next').addEventListener('click', () => show(cur + 1));
  lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });

  })();

  // Office bearers: public, read-only list from the member portal
  (async () => {
    const API = 'https://mms.madikaipravasi.org/api/public/office-bearers';
    const presentEl = document.getElementById('bearers-present');
    if (!presentEl) return;
    const pastEl = document.getElementById('bearers-past');
    const tabs = [document.getElementById('tab-present'), document.getElementById('tab-past')];
    const panels = [presentEl, pastEl];
    function select(i, focus) {
      tabs.forEach((t, j) => { t.setAttribute('aria-selected', String(i === j)); t.tabIndex = i === j ? 0 : -1; panels[j].hidden = i !== j; });
      if (focus) tabs[i].focus();
    }
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); select((i + 1) % 2, true); }
      });
    });

    const GROUPS = [['office', 'Office bearers'], ['deputy', 'Deputy office bearers'], ['patron', 'Patrons']];
    const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
    const initials = (name) => name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase();
    const fallback = (name) => { const f = el('span', 'pic none', initials(name)); f.setAttribute('aria-hidden', 'true'); return f; };
    function card(b, past) {
      const c = el('article', past ? 'bearer past' : 'bearer');
      if (b.photo_url) {
        const img = el('img', 'pic');
        img.src = b.photo_url; img.alt = b.name; img.loading = 'lazy'; img.width = 104; img.height = 104;
        img.addEventListener('error', () => img.replaceWith(fallback(b.name)));
        c.append(img);
      } else c.append(fallback(b.name));
      c.append(el('span', 'role', b.position_label), el('span', 'name', b.name));
      if (b.years) c.append(el('span', 'term', b.years));
      return c;
    }
    function render(target, list, past, emptyText) {
      target.textContent = '';
      if (!list.length) { target.append(el('p', 'bearers-note', emptyText)); return; }
      for (const [key, title] of GROUPS) {
        const rows = list.filter((b) => b.group === key);
        if (!rows.length) continue;
        const group = el('div', 'bearer-group');
        group.append(el('h3', null, past ? 'Past ' + title.toLowerCase() : title));
        const grid = el('div', 'bearer-grid');
        rows.forEach((b) => grid.append(card(b, past)));
        group.append(grid);
        target.append(group);
      }
    }
    try {
      const res = await fetch(API, { headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(String(res.status));
      const data = await res.json();
      const present = Array.isArray(data.present) ? data.present : [];
      const past = Array.isArray(data.past) ? data.past : [];
      render(presentEl, present, false, 'Office bearers will be listed here soon.');
      render(pastEl, past, true, 'Past office bearers will be listed here soon.');
      tabs[1].textContent = past.length ? `Past (${past.length})` : 'Past';
    } catch (e) {
      presentEl.textContent = '';
      presentEl.append(el('p', 'bearers-note', 'Office bearers could not be loaded right now. Please check back later.'));
    }
  })();
