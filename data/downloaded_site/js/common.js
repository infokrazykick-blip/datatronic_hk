/* Common JS for Datatronic
   - Provides shared functions used across pages
   - Expects i18next (if used) and Flickity to be loaded before calling page-specific init
*/

// Toggle mobile nav (used by hamburger onclick)
window.toggleMenu = function() {
  const navLinks = document.getElementById('navLinks');
  if (navLinks) navLinks.classList.toggle('active');
};

// Toggle contact sidebar (used by minimize button)
window.toggleSidebar = function() {
  const sidebar = document.getElementById('contactSidebar');
  const minimize = document.querySelector('.mystickyelements-minimize') || document.getElementById('contactSidebarToggle');
  if (!sidebar) return;
  sidebar.classList.toggle('collapsed');
  const collapsed = sidebar.classList.contains('collapsed');
  if (minimize) {
    const label = collapsed ? '➜' : '←';
    minimize.innerHTML = label;
    minimize.setAttribute('aria-pressed', collapsed ? 'true' : 'false');
    if (minimize.id === 'contactSidebarToggle') minimize.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
  }
  sidebar.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
  try { localStorage.setItem('sidebarCollapsed', collapsed ? '1' : '0'); } catch(e){}
};

// Initialize sidebar accessibility and persisted state
function _initSidebar() {
  const sidebar = document.getElementById('contactSidebar');
  const minimize = document.querySelector('.mystickyelements-minimize') || document.getElementById('contactSidebarToggle');
  if (!sidebar || !minimize) return;
  const toggleBtn = minimize;
  toggleBtn.setAttribute('role', 'button');
  toggleBtn.setAttribute('tabindex', '0');
  toggleBtn.setAttribute('aria-pressed', 'false');
  sidebar.setAttribute('aria-expanded', 'true');
  toggleBtn.addEventListener('keydown', function(e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); window.toggleSidebar(); } });
  toggleBtn.addEventListener('click', function() { window.toggleSidebar(); });
  try {
    const stored = localStorage.getItem('sidebarCollapsed');
    if (stored === '0') {
      sidebar.classList.remove('collapsed');
      toggleBtn.setAttribute('aria-pressed', 'false');
      sidebar.setAttribute('aria-expanded', 'true');
    } else {
      sidebar.classList.add('collapsed');
      toggleBtn.setAttribute('aria-pressed', 'true');
      sidebar.setAttribute('aria-expanded', 'false');
    }
  } catch(e){}
}

// Flyout behavior for social icons
function _initFlyoutsAndMobile() {
  document.querySelectorAll('[data-flyout]').forEach(function(el){
    const li = el.closest('.mystickyelements-social-icon-li');
    const flyout = li ? li.querySelector('.mystickyelements-flyout') : null;
    if(!flyout) return;
    el.addEventListener('mouseenter', function(){ if(window.innerWidth>420) flyout.classList.add('open'); });
    el.addEventListener('mouseleave', function(){ if(window.innerWidth>420) flyout.classList.remove('open'); });
    el.addEventListener('click', function(e){
      const sidebar = document.getElementById('contactSidebar');
      if (sidebar && sidebar.classList.contains('collapsed')) {
        e.preventDefault(); e.stopPropagation();
        sidebar.classList.remove('collapsed');
        const minimize = document.querySelector('.mystickyelements-minimize');
        if (minimize) minimize.innerHTML = '←';
        sidebar.setAttribute('aria-expanded','true');
        try { localStorage.setItem('sidebarCollapsed','0'); } catch(e){}
        return;
      }
      e.stopPropagation();
      flyout.classList.toggle('open');
      el.setAttribute('aria-expanded', flyout.classList.contains('open') ? 'true' : 'false');
    });
  });

  document.querySelectorAll('.mystickyelements-social-icon').forEach(function(el){
    el.addEventListener('click', function(e){
      const sidebar = document.getElementById('contactSidebar');
      const li = el.closest('.mystickyelements-social-icon-li');
      const phoneLink = li ? li.querySelector('a[href^="tel:"]') : null;
      if (sidebar && sidebar.classList.contains('collapsed')) {
        e.preventDefault(); e.stopPropagation();
        sidebar.classList.remove('collapsed');
        const minimize = document.querySelector('.mystickyelements-minimize'); if (minimize) minimize.innerHTML = '←';
        sidebar.setAttribute('aria-expanded','true');
        try { localStorage.setItem('sidebarCollapsed','0'); } catch(e){}
        return;
      }
      // allow default behavior for links
    });
  });

  // close flyouts when clicking outside or pressing Escape
  document.addEventListener('click', function(e){
    document.querySelectorAll('.mystickyelements-flyout.open').forEach(function(f){
      if(!f.contains(e.target)){
        f.classList.remove('open');
        var icon = f.closest('.mystickyelements-social-icon-li').querySelector('[data-flyout]');
        if(icon) icon.setAttribute('aria-expanded','false');
      }
    });
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') document.querySelectorAll('.mystickyelements-flyout.open').forEach(function(f){ f.classList.remove('open'); var icon = f.closest('.mystickyelements-social-icon-li').querySelector('[data-flyout]'); if(icon) icon.setAttribute('aria-expanded','false'); }); });

  // mobile toggle button
  if (!document.getElementById('contactSidebarMobileToggle')) {
    const mobileToggle = document.createElement('button');
    mobileToggle.id = 'contactSidebarMobileToggle';
    mobileToggle.setAttribute('aria-label', 'Open contact sidebar');
    mobileToggle.innerHTML = '<i class="fa fa-phone"></i>';
    document.body.appendChild(mobileToggle);
    mobileToggle.addEventListener('click', function(){ const sidebar = document.getElementById('contactSidebar'); if (sidebar) sidebar.classList.toggle('mobile-open'); });

    document.addEventListener('click', function(e){ const sidebar = document.getElementById('contactSidebar'); const mobileToggle = document.getElementById('contactSidebarMobileToggle'); if(!sidebar || !mobileToggle) return; if(sidebar.classList.contains('mobile-open')){ if(!sidebar.contains(e.target) && !mobileToggle.contains(e.target)){ sidebar.classList.remove('mobile-open'); } } });
  }
}

// Awards lightbox
function _initAwardsLightbox(){
  const modal = document.getElementById('lightboxModal');
  if(!modal) return;
  const modalImg = document.getElementById('lightboxImage');
  const modalCaption = document.getElementById('lightboxCaption');
  const closeBtn = modal.querySelector('.lightbox-close');
  document.querySelectorAll('.image-lightbox').forEach(function(el){ el.addEventListener('click', function(e){ e.preventDefault(); const href = el.getAttribute('href') || el.dataset.src; const title = el.getAttribute('title') || ''; modalImg.src = href; modalImg.alt = title; modalCaption.textContent = title; modal.classList.add('open'); modal.setAttribute('aria-hidden','false'); closeBtn && closeBtn.focus(); }); });
  function closeModal(){ modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); if(modalImg) { modalImg.src = ''; }; if(modalCaption) modalCaption.textContent = ''; }
  closeBtn && closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e){ if(e.target === modal) closeModal(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeModal(); });
}

// Initialize Flickity sliders if Flickity present
function _initFlickity(){
  if(typeof Flickity === 'undefined') return;
  document.querySelectorAll('.slider[data-flickity-options]').forEach(function(el){
    var optsStr = el.getAttribute('data-flickity-options') || '{}';
    var opts = {};
    try { opts = JSON.parse(optsStr); } catch(e){ console.warn('Flickity options parse error', e); }
    var flk = new Flickity(el, opts);
    flk.on('ready', function(){ el.querySelectorAll('.flickity-prev-next-button').forEach(function(btn){ if(!btn.getAttribute('aria-label')) btn.setAttribute('aria-label', btn.classList.contains('previous') ? 'Previous' : 'Next'); }); });
    setTimeout(function(){ try{ flk.reloadCells(); flk.resize(); flk.reposition(); }catch(e){} }, 250);
  });
}

// Back-to-top logic
function _initBackToTop(){
  const topLink = document.getElementById('top-link');
  if (topLink) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) { topLink.style.display = 'block'; } else { topLink.style.display = 'none'; }
    });
    topLink.addEventListener('click', function(e){ e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
}

// Navbar hide/show on scroll and add .nav-solid when scrolled
function _initNavbarScroll(){
  let lastScrollTop = 0;
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > lastScrollTop && scrollTop > 50) { navbar.classList.add('hidden'); } else { navbar.classList.remove('hidden'); }
    if (scrollTop > 80) { navbar.classList.add('nav-solid'); } else { navbar.classList.remove('nav-solid'); }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }, false);
}

// i18n helpers (changeLanguage & updateContent) — pages should keep their own i18next.init blocks
window.changeLanguage = function(lng) { if (typeof i18next !== 'undefined') { i18next.changeLanguage(lng, window.updateContent); } const btn = document.querySelector('.dropdown button'); if (btn) btn.textContent = lng.toUpperCase(); };
window.updateContent = function(){ if (typeof i18next === 'undefined') return; document.querySelectorAll('[data-i18n]').forEach(el => { const key = el.getAttribute('data-i18n'); el.textContent = i18next.t(key); });
};

// Auto-init common behaviors when DOM is ready
document.addEventListener('DOMContentLoaded', function(){
  _initSidebar();
  _initFlyoutsAndMobile();
  _initAwardsLightbox();
  _initFlickity();
  _initBackToTop();
  _initNavbarScroll();
});