/* ===================================================================
   사진 정리 앱 — 메인 JavaScript
   =================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initViewToggle();
  initFlashAutoClose();
  initLightbox();
  loadStats();
});

/* ── 뷰 토글 (그리드 / 리스트) ─────────────────────────────────────── */
function initViewToggle() {
  const gridBtn = document.getElementById('gridViewBtn');
  const listBtn = document.getElementById('listViewBtn');
  const grids   = document.querySelectorAll('.photo-grid');

  if (!gridBtn || !listBtn) return;

  const saved = localStorage.getItem('viewMode') || 'grid';
  if (saved === 'list') applyListView(grids, gridBtn, listBtn);

  gridBtn.addEventListener('click', () => {
    grids.forEach(g => g.classList.remove('list-view'));
    gridBtn.classList.add('active');
    listBtn.classList.remove('active');
    localStorage.setItem('viewMode', 'grid');
  });

  listBtn.addEventListener('click', () => {
    applyListView(grids, gridBtn, listBtn);
    localStorage.setItem('viewMode', 'list');
  });
}

function applyListView(grids, gridBtn, listBtn) {
  grids.forEach(g => g.classList.add('list-view'));
  listBtn.classList.add('active');
  gridBtn.classList.remove('active');
}

/* ── 플래시 메시지 자동 닫기 ────────────────────────────────────────── */
function initFlashAutoClose() {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });
}

/* ── 통계 API 호출 ─────────────────────────────────────────────────── */
async function loadStats() {
  try {
    const res  = await fetch('/api/stats');
    const data = await res.json();

    const el = document.getElementById('stats');
    if (!el) return;

    el.innerHTML = `
      <div class="stat-item">
        <span class="stat-value">${data.total_photos}</span>
        <span class="stat-label">사진</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">${data.total_albums}</span>
        <span class="stat-label">앨범</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">${data.total_tags}</span>
        <span class="stat-label">태그</span>
      </div>
    `;
  } catch (_) { /* 무시 */ }
}

/* ── 라이트박스 ─────────────────────────────────────────────────────── */
function initLightbox() {
  const img = document.getElementById('mainImage');
  if (!img) return;

  const box = document.createElement('div');
  box.id = 'lightbox';
  box.style.cssText = `
    display:none; position:fixed; inset:0; z-index:1000;
    background:rgba(0,0,0,.92); align-items:center; justify-content:center;
    cursor:zoom-out;
  `;

  const bigImg = document.createElement('img');
  bigImg.style.cssText = `
    max-width:95vw; max-height:95vh; object-fit:contain;
    border-radius:8px; box-shadow:0 0 60px rgba(0,0,0,.8);
  `;

  const closeBtn = document.createElement('button');
  closeBtn.textContent = '×';
  closeBtn.style.cssText = `
    position:absolute; top:1rem; right:1.5rem;
    background:none; border:none; color:#fff;
    font-size:2rem; cursor:pointer; opacity:.8;
  `;

  box.append(closeBtn, bigImg);
  document.body.append(box);

  img.style.cursor = 'zoom-in';
  img.addEventListener('click', () => {
    bigImg.src = img.src;
    box.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  });

  function close() {
    box.style.display = 'none';
    document.body.style.overflow = '';
  }

  closeBtn.addEventListener('click', close);
  box.addEventListener('click', e => { if (e.target === box) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
}

/* ── 키보드 단축키 (상세 페이지 이전/다음) ─────────────────────────── */
(function initKeyboardNav() {
  const prevLink = document.querySelector('.detail-nav-arrows a:first-child');
  const nextLink = document.querySelector('.detail-nav-arrows a:last-child');

  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'ArrowLeft'  && prevLink) prevLink.click();
    if (e.key === 'ArrowRight' && nextLink) nextLink.click();
  });
})();
