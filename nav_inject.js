/**
 * nav_inject.js — Injected into every lesson HTML to enable:
 *   1. Sidebar menu item clicks → navigate to correct local file
 *   2. Top navigation bar (Home, Prev/Next, Complete, Theme)
 *   3. Progress tracking via localStorage
 *   4. Keyboard shortcuts (← → arrows, Esc)
 */
(function () {
  'use strict';

  // ---- Constants ----
  const SK_DONE = 'ipmh_done_v2';
  const SK_TH = 'ipmh_th_v2';
  const SK_LR = 'ipmh_lr_v2';

  // ---- Determine current file path relative to root ----
  // Works for both file:// and http:// protocols
  function getCurrentRelPath() {
    const path = decodeURIComponent(window.location.pathname);
    // Extract "DirName/filename.html" from the full path
    for (const cat of Object.keys(CATEGORY_ORDER)) {
      const idx = path.indexOf(cat + '/');
      if (idx >= 0) {
        return path.substring(idx);
      }
    }
    return path;
  }

  const currentRelPath = getCurrentRelPath();

  // Find which category we're in
  let currentCategory = null;
  let currentIndex = -1;
  let categoryFiles = [];

  for (const [cat, files] of Object.entries(CATEGORY_ORDER)) {
    const idx = files.findIndex(f => currentRelPath.endsWith(f) || currentRelPath.includes(f));
    if (idx >= 0) {
      currentCategory = cat;
      currentIndex = idx;
      categoryFiles = files;
      break;
    }
  }

  // ---- localStorage helpers ----
  let completed = new Set(JSON.parse(localStorage.getItem(SK_DONE) || '[]'));
  let theme = localStorage.getItem(SK_TH) || 'dark';

  function saveCompleted() {
    localStorage.setItem(SK_DONE, JSON.stringify([...completed]));
  }

  // Use relative path as the lesson ID for completion tracking
  function getLessonId(relPath) {
    return relPath;
  }

  const currentLessonId = getLessonId(currentRelPath);

  // Save last-read
  localStorage.setItem(SK_LR, currentLessonId);

  // ---- 1. Fix Sidebar Navigation ----
  function fixSidebar() {
    // Find all menu items with data-menu-id
    const allMenuItems = document.querySelectorAll('[data-menu-id]');

    allMenuItems.forEach(item => {
      // Extract the course path from data-menu-id
      const menuId = item.getAttribute('data-menu-id');
      if (!menuId) return;

      // Extract /courses/... path
      const match = menuId.match(/\/courses\/[^\s"'>]+/);
      if (!match) return;

      const coursePath = match[0];
      const targetFile = NAV_MAP[coursePath];
      if (!targetFile) return;

      // Calculate relative URL from current file to target file
      const targetUrl = getRelativeUrl(currentRelPath, targetFile);

      // Make the item clickable
      item.style.cursor = 'pointer';

      // Remove any existing click handlers by cloning
      const newItem = item.cloneNode(true);
      item.parentNode.replaceChild(newItem, item);

      newItem.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        window.location.href = targetUrl;
      });
    });
  }

  // Calculate relative path from current file to target file
  function getRelativeUrl(fromPath, toPath) {
    const fromParts = fromPath.split('/');
    const toParts = toPath.split('/');

    // Remove filename from "from" path to get directory
    fromParts.pop();

    // Find common prefix length
    let common = 0;
    while (common < fromParts.length && common < toParts.length && fromParts[common] === toParts[common]) {
      common++;
    }

    // Build relative path
    const upCount = fromParts.length - common;
    const ups = '../'.repeat(upCount);
    const remainder = toParts.slice(common).join('/');

    return ups + remainder;
  }

  // ---- 2. Inject Top Navigation Bar ----
  function injectTopBar() {
    const isCompleted = completed.has(currentLessonId);
    const prevFile = currentIndex > 0 ? categoryFiles[currentIndex - 1] : null;
    const nextFile = currentIndex < categoryFiles.length - 1 ? categoryFiles[currentIndex + 1] : null;

    // Extract lesson title from the page
    const h1 = document.querySelector('article h1, main h1, .style_learnContent__K5K7M h1, h1');
    const lessonTitle = h1 ? h1.textContent.trim() : 'Lesson';

    const bar = document.createElement('div');
    bar.id = 'nav-inject-bar';
    bar.innerHTML = `
      <div class="nib-left">
        <a href="${'../'.repeat(currentRelPath.split('/').length - 1)}index.html" class="nib-home" title="Back to Hub">🏠</a>
        <span class="nib-sep">│</span>
        <span class="nib-course">${currentCategory || 'Course'}</span>
        <span class="nib-sep">›</span>
        <span class="nib-title">${lessonTitle}</span>
      </div>
      <div class="nib-right">
        ${prevFile ? `<a href="${getRelativeUrl(currentRelPath, prevFile)}" class="nib-btn" title="Previous Lesson (←)">← Prev</a>` : `<span class="nib-btn disabled">← Prev</span>`}
        <span class="nib-progress">${currentIndex + 1} / ${categoryFiles.length}</span>
        ${nextFile ? `<a href="${getRelativeUrl(currentRelPath, nextFile)}" class="nib-btn" title="Next Lesson (→)">Next →</a>` : `<span class="nib-btn disabled">Next →</span>`}
        <span class="nib-sep">│</span>
        <label class="nib-check" title="Mark as completed">
          <input type="checkbox" id="nib-done-chk" ${isCompleted ? 'checked' : ''}>
          <span>${isCompleted ? '✅ Done' : '☑️ Complete'}</span>
        </label>
        <button id="nib-theme-btn" class="nib-btn" title="Toggle Theme">${theme === 'dark' ? '☀️' : '🌙'}</button>
      </div>
    `;

    // Inject styles
    const style = document.createElement('style');
    style.textContent = `
      #nav-inject-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        height: 44px;
        background: #111827;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13px;
        color: #e2e8f0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        gap: 8px;
        flex-wrap: nowrap;
      }
      #nav-inject-bar .nib-left {
        display: flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
        overflow: hidden;
      }
      #nav-inject-bar .nib-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
      }
      #nav-inject-bar .nib-home {
        font-size: 18px;
        text-decoration: none;
        display: flex;
        align-items: center;
        padding: 4px 8px;
        border-radius: 6px;
        transition: background 0.15s;
      }
      #nav-inject-bar .nib-home:hover { background: rgba(255,255,255,0.08); }
      #nav-inject-bar .nib-sep { color: #475569; }
      #nav-inject-bar .nib-course {
        color: #6366f1;
        font-weight: 600;
        white-space: nowrap;
      }
      #nav-inject-bar .nib-title {
        color: #94a3b8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      #nav-inject-bar .nib-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        color: #e2e8f0;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.15s;
        white-space: nowrap;
      }
      #nav-inject-bar .nib-btn:hover:not(.disabled) {
        background: #6366f1;
        color: #fff;
        border-color: #6366f1;
      }
      #nav-inject-bar .nib-btn.disabled {
        opacity: 0.3;
        cursor: not-allowed;
        pointer-events: none;
      }
      #nav-inject-bar .nib-progress {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: #64748b;
        white-space: nowrap;
      }
      #nav-inject-bar .nib-check {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        cursor: pointer;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        transition: all 0.15s;
        white-space: nowrap;
        font-size: 12px;
      }
      #nav-inject-bar .nib-check:hover { background: rgba(16,185,129,0.15); }
      #nav-inject-bar .nib-check input { accent-color: #10b981; cursor: pointer; }

      /* Push page content down to avoid overlap with fixed bar */
      body { padding-top: 48px !important; }

      /* Toast */
      #nib-toast {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: #1e293b;
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 4px solid #6366f1;
        padding: 10px 18px;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        z-index: 100000;
        transform: translateY(80px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
      #nib-toast.show { transform: translateY(0); opacity: 1; }
    `;

    document.head.appendChild(style);

    // Insert bar at the very top of body
    document.body.insertBefore(bar, document.body.firstChild);

    // Add toast element
    const toast = document.createElement('div');
    toast.id = 'nib-toast';
    document.body.appendChild(toast);

    // ---- Event handlers ----
    // Completion checkbox
    const chk = document.getElementById('nib-done-chk');
    if (chk) {
      chk.addEventListener('change', function () {
        if (chk.checked) {
          completed.add(currentLessonId);
          chk.parentElement.querySelector('span').textContent = '✅ Done';
          showToast('Marked as completed! 🎉');
        } else {
          completed.delete(currentLessonId);
          chk.parentElement.querySelector('span').textContent = '☑️ Complete';
          showToast('Unmarked');
        }
        saveCompleted();
      });
    }

    // Theme toggle
    const themeBtn = document.getElementById('nib-theme-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        theme = theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem(SK_TH, theme);
        themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
        // Can't fully re-theme ByteByteGo pages, but sync with hub
      });
    }
  }

  function showToast(msg) {
    const t = document.getElementById('nib-toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2400);
  }

  // ---- 3. Keyboard Shortcuts ----
  function setupKeyboard() {
    document.addEventListener('keydown', function (e) {
      // Don't intercept if user is typing in an input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowLeft' && currentIndex > 0) {
        window.location.href = getRelativeUrl(currentRelPath, categoryFiles[currentIndex - 1]);
      }
      if (e.key === 'ArrowRight' && currentIndex < categoryFiles.length - 1) {
        window.location.href = getRelativeUrl(currentRelPath, categoryFiles[currentIndex + 1]);
      }
    });
  }

  // ---- Init on DOM ready ----
  function init() {
    fixSidebar();
    injectTopBar();
    setupKeyboard();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
