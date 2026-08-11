/**
 * nav_inject.js — Unified Navigation Engine for all 213 Lesson Pages
 */
(function () {
  'use strict';

  const SK_DONE = 'ipmh_done_v2';
  const SK_TH = 'ipmh_th_v2';
  const SK_LR = 'ipmh_lr_v2';
  const SK_SB_OPEN = 'ipmh_sb_open_v2';

  let completed = new Set(JSON.parse(localStorage.getItem(SK_DONE) || '[]'));
  let theme = localStorage.getItem(SK_TH) || 'dark';

  // Calculate current file's relative path from root directory
  function getCurrentRelPath() {
    const rawPath = decodeURIComponent(window.location.pathname).replace(/\\/g, '/');
    for (const catName of Object.keys(NAV_TREE)) {
      const idx = rawPath.indexOf(catName + '/');
      if (idx >= 0) {
        return rawPath.substring(idx);
      }
    }
    return rawPath;
  }

  const currentRelPath = getCurrentRelPath();

  // Find current lesson object
  const currentLesson = NAV_LESSONS.find(l => currentRelPath.endsWith(l.path) || currentRelPath.includes(l.path)) || NAV_LESSONS[0];

  // Category lessons list for Prev/Next
  const categoryLessons = NAV_LESSONS.filter(l => l.category === currentLesson.category);
  const currentIndex = categoryLessons.findIndex(l => l.path === currentLesson.path);

  const prevLesson = currentIndex > 0 ? categoryLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < categoryLessons.length - 1 ? categoryLessons[currentIndex + 1] : null;

  // Save last read
  localStorage.setItem(SK_LR, currentLesson.path);

  // Helper to compute relative URL between paths
  function getRelativeUrl(fromPath, toPath) {
    const fromParts = fromPath.split('/');
    const toParts = toPath.split('/');
    fromParts.pop(); // Remove filename

    let common = 0;
    while (common < fromParts.length && common < toParts.length && fromParts[common] === toParts[common]) {
      common++;
    }

    const ups = '../'.repeat(fromParts.length - common);
    const remainder = toParts.slice(common).join('/');
    return ups + remainder;
  }

  // Path to home page (index.html)
  const homeUrl = '../'.repeat(currentRelPath.split('/').length - 1) + 'index.html';

  // Inject Styles
  function injectStyles() {
    const style = document.createElement('style');
    style.id = 'unified-nav-styles';
    style.textContent = `
      /* Hide original broken ByteByteGo sidebars */
      .ant-layout-sider, aside.ant-layout-sider, .style_sider__ucgEf, .style_codingPatternsSider___CRHA {
        display: none !important;
      }
      
      /* Ensure main content takes full width */
      .ant-layout-has-sider > .ant-layout, .ant-layout-content {
        margin-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
      }

      body {
        padding-top: 48px !important;
      }

      /* Floating Topbar */
      #nav-topbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 48px;
        z-index: 999990;
        background: #0f172a;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 14px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13px;
        color: #f1f5f9;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        gap: 10px;
      }

      .topbar-left {
        display: flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
        overflow: hidden;
      }

      .topbar-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
      }

      .tb-btn-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.05);
        color: #f1f5f9;
        cursor: pointer;
        text-decoration: none;
        font-size: 14px;
        transition: all 0.15s;
      }

      .tb-btn-icon:hover {
        background: #6366f1;
        border-color: #6366f1;
        color: #fff;
      }

      .tb-badge {
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        color: #fff;
        white-space: nowrap;
      }

      .tb-title {
        color: #94a3b8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 500;
      }

      .tb-nav-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.05);
        color: #f1f5f9;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.15s;
        white-space: nowrap;
      }

      .tb-nav-btn:hover:not(.disabled) {
        background: #6366f1;
        border-color: #6366f1;
        color: #fff;
      }

      .tb-nav-btn.disabled {
        opacity: 0.3;
        cursor: not-allowed;
        pointer-events: none;
      }

      .tb-counter {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #64748b;
        white-space: nowrap;
      }

      .tb-check-lbl {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.05);
        font-size: 12px;
        font-weight: 500;
        transition: all 0.15s;
        white-space: nowrap;
      }

      .tb-check-lbl:hover {
        background: rgba(16, 185, 129, 0.2);
        border-color: #10b981;
      }

      .tb-check-lbl input {
        accent-color: #10b981;
        cursor: pointer;
      }

      /* Unified Custom Sidebar Drawer */
      #custom-nav-sidebar {
        position: fixed;
        top: 48px;
        left: 0;
        bottom: 0;
        width: 320px;
        z-index: 999980;
        background: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        transform: translateX(-100%);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
      }

      #custom-nav-sidebar.open {
        transform: translateX(0);
      }

      .sidebar-search-box {
        padding: 10px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        background: #111827;
      }

      .sb-search-input {
        width: 100%;
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: #1e293b;
        color: #f1f5f9;
        font-size: 12px;
        outline: none;
      }

      .sb-search-input:focus {
        border-color: #6366f1;
      }

      .sidebar-tree-content {
        flex-grow: 1;
        overflow-y: auto;
        padding: 8px;
        scrollbar-width: thin;
        scrollbar-color: rgba(255,255,255,0.1) transparent;
      }

      /* Accordion Course Section */
      .sb-cat-section {
        margin-bottom: 6px;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(17, 24, 39, 0.6);
      }

      .sb-cat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 10px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 12px;
        color: #f1f5f9;
        cursor: pointer;
        user-select: none;
        transition: background 0.15s;
      }

      .sb-cat-header:hover {
        background: rgba(255, 255, 255, 0.06);
      }

      .sb-cat-body {
        display: none;
        padding: 4px;
        background: #090d16;
      }

      .sb-cat-section.open .sb-cat-body {
        display: block;
      }

      .sb-subgroup-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6366f1;
        padding: 6px 10px 4px 10px;
        margin-top: 4px;
        border-top: 1px dashed rgba(255,255,255,0.06);
      }

      .sb-subgroup-title:first-child {
        border-top: none;
        margin-top: 0;
      }

      /* Lesson item link */
      .sb-item-link {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 5px 8px;
        border-radius: 6px;
        font-size: 12px;
        color: #94a3b8;
        text-decoration: none;
        margin-bottom: 1px;
        transition: all 0.15s;
        line-height: 1.3;
      }

      .sb-item-link:hover {
        background: rgba(99, 102, 241, 0.15);
        color: #f1f5f9;
      }

      .sb-item-link.active {
        background: #6366f1 !important;
        color: #ffffff !important;
        font-weight: 600;
      }

      .sb-item-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex-grow: 1;
      }

      /* Toast Notification */
      #nav-toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #1e293b;
        color: #f1f5f9;
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 4px solid #6366f1;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        z-index: 1000000;
        transform: translateY(80px);
        opacity: 0;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
      }

      #nav-toast.show {
        transform: translateY(0);
        opacity: 1;
      }
    `;
    document.head.appendChild(style);
  }

  // Inject Top Bar
  function injectTopBar() {
    const meta = NAV_META[currentLesson.category] || { name: currentLesson.category, color: '#6366f1' };
    const isDone = completed.has(currentLesson.path);

    const topbar = document.createElement('div');
    topbar.id = 'nav-topbar';
    topbar.innerHTML = `
      <div class="topbar-left">
        <button id="tb-toggle-sb" class="tb-btn-icon" title="Toggle Navigation Sidebar (☰)">☰</button>
        <a href="${homeUrl}" class="tb-btn-icon" title="Back to Hub Dashboard">🏠</a>
        <span class="tb-badge" style="background: ${meta.color}">${meta.name}</span>
        <span class="tb-title">${currentLesson.title}</span>
      </div>
      <div class="topbar-right">
        ${prevLesson ? `<a href="${getRelativeUrl(currentRelPath, prevLesson.path)}" class="tb-nav-btn" title="Previous (←)">← Prev</a>` : `<span class="tb-nav-btn disabled">← Prev</span>`}
        <span class="tb-counter">${currentIndex + 1} / ${categoryLessons.length}</span>
        ${nextLesson ? `<a href="${getRelativeUrl(currentRelPath, nextLesson.path)}" class="tb-nav-btn" title="Next (→)">Next →</a>` : `<span class="tb-nav-btn disabled">Next →</span>`}
        <label class="tb-check-lbl" title="Mark as Completed">
          <input type="checkbox" id="tb-chk-done" ${isDone ? 'checked' : ''}>
          <span id="tb-chk-text">${isDone ? '✅ Done' : '☑️ Complete'}</span>
        </label>
      </div>
    `;

    document.body.insertBefore(topbar, document.body.firstChild);

    // Completion Checkbox
    const chk = document.getElementById('tb-chk-done');
    const chkText = document.getElementById('tb-chk-text');
    chk.addEventListener('change', function () {
      if (chk.checked) {
        completed.add(currentLesson.path);
        chkText.textContent = '✅ Done';
        showToast('Marked as completed! 🎉');
      } else {
        completed.delete(currentLesson.path);
        chkText.textContent = '☑️ Complete';
        showToast('Unmarked');
      }
      localStorage.setItem(SK_DONE, JSON.stringify([...completed]));
      renderSidebarItems();
    });

    // Sidebar Toggle
    const sbToggleBtn = document.getElementById('tb-toggle-sb');
    sbToggleBtn.addEventListener('click', toggleSidebar);
  }

  // Inject Sidebar Drawer
  function injectSidebar() {
    const sidebar = document.createElement('aside');
    sidebar.id = 'custom-nav-sidebar';
    sidebar.innerHTML = `
      <div class="sidebar-search-box">
        <input type="text" id="sb-search-input" class="sb-search-input" placeholder="Search 213 lessons ( / )..." />
      </div>
      <div id="sidebar-tree-content" class="sidebar-tree-content"></div>
    `;
    document.body.appendChild(sidebar);

    renderSidebarItems();

    // Search Input in Sidebar
    const searchInput = document.getElementById('sb-search-input');
    searchInput.addEventListener('input', function (e) {
      filterSidebarItems(e.target.value);
    });
  }

  // Render Sidebar Category Accordions and Links
  function renderSidebarItems() {
    const container = document.getElementById('sidebar-tree-content');
    if (!container) return;
    container.innerHTML = '';

    Object.entries(NAV_TREE).forEach(([catName, subgroups]) => {
      const meta = NAV_META[catName] || { name: catName, icon: '📄', color: '#6366f1' };
      const catLessons = NAV_LESSONS.filter(l => l.category === catName);
      const catDoneCount = catLessons.filter(l => completed.has(l.path)).length;
      const isCurrentCategory = currentLesson.category === catName;

      const sec = document.createElement('div');
      sec.className = `sb-cat-section ${isCurrentCategory ? 'open' : ''}`;

      let bodyHtml = '';
      Object.entries(subgroups).forEach(([sgName, lessons]) => {
        if (sgName !== 'General') {
          bodyHtml += `<div class="sb-subgroup-title">${sgName}</div>`;
        }
        lessons.forEach(l => {
          const isCurrent = l.path === currentLesson.path;
          const isLessonDone = completed.has(l.path);
          const linkUrl = getRelativeUrl(currentRelPath, l.path);

          bodyHtml += `
            <a href="${linkUrl}" class="sb-item-link ${isCurrent ? 'active' : ''}" data-path="${l.path}">
              <span>${isLessonDone ? '✅' : '📄'}</span>
              <span class="sb-item-title">${l.title}</span>
            </a>
          `;
        });
      });

      sec.innerHTML = `
        <div class="sb-cat-header">
          <span>${meta.icon} ${meta.name}</span>
          <span style="font-size:11px; opacity:0.8">${catDoneCount}/${catLessons.length}</span>
        </div>
        <div class="sb-cat-body">${bodyHtml}</div>
      `;

      sec.querySelector('.sb-cat-header').addEventListener('click', function () {
        sec.classList.toggle('open');
      });

      container.appendChild(sec);
    });

    // Auto scroll active item into view
    setTimeout(() => {
      const activeLink = container.querySelector('.sb-item-link.active');
      if (activeLink) {
        activeLink.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }
    }, 100);
  }

  // Filter sidebar links on search
  function filterSidebarItems(query) {
    const q = query.toLowerCase().trim();
    const sections = document.querySelectorAll('.sb-cat-section');

    sections.forEach(sec => {
      let matchCount = 0;
      const links = sec.querySelectorAll('.sb-item-link');

      links.forEach(link => {
        const text = link.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          link.style.display = 'flex';
          matchCount++;
        } else {
          link.style.display = 'none';
        }
      });

      if (q) {
        if (matchCount > 0) {
          sec.style.display = 'block';
          sec.classList.add('open');
        } else {
          sec.style.display = 'none';
        }
      } else {
        sec.style.display = 'block';
        if (sec.querySelector('.sb-item-link.active')) {
          sec.classList.add('open');
        }
      }
    });
  }

  // Toggle Sidebar Drawer
  function toggleSidebar() {
    const sb = document.getElementById('custom-nav-sidebar');
    if (!sb) return;
    const isOpen = sb.classList.toggle('open');
    localStorage.setItem(SK_SB_OPEN, isOpen ? 'true' : 'false');
  }

  // Toast Helper
  function showToast(msg) {
    let toast = document.getElementById('nav-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'nav-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2400);
  }

  // Keyboard Shortcuts
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowLeft' && prevLesson) {
        window.location.href = getRelativeUrl(currentRelPath, prevLesson.path);
      }
      if (e.key === 'ArrowRight' && nextLesson) {
        window.location.href = getRelativeUrl(currentRelPath, nextLesson.path);
      }
      if (e.key === '/') {
        e.preventDefault();
        const sb = document.getElementById('custom-nav-sidebar');
        if (sb && !sb.classList.contains('open')) {
          sb.classList.add('open');
        }
        const sInput = document.getElementById('sb-search-input');
        if (sInput) sInput.focus();
      }
      if (e.key === 'Escape') {
        const sb = document.getElementById('custom-nav-sidebar');
        if (sb && sb.classList.contains('open')) {
          sb.classList.remove('open');
        }
      }
    });
  }

  // Init
  function init() {
    injectStyles();
    injectTopBar();
    injectSidebar();
    setupKeyboardShortcuts();

    // Auto-open sidebar if user previously kept it open
    if (localStorage.getItem(SK_SB_OPEN) === 'true') {
      const sb = document.getElementById('custom-nav-sidebar');
      if (sb) sb.classList.add('open');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
