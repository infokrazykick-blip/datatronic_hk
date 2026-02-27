/* Common JS for Datatronic
   - Provides shared functions used across pages
   - Expects i18next (if used) and Flickity to be loaded before calling page-specific init
*/

// Toggle mobile nav (used by hamburger onclick)
window.toggleMenu = function() {
  const navLinks = document.getElementById('navLinks');
  if (navLinks) navLinks.classList.toggle('active');
};

// Toggle applications dropdown on mobile
window.toggleAppDropdown = function(event) {
  if (window.innerWidth <= 768) {
    event.preventDefault();
    const dropdown = event.target.closest('.nav-dropdown');
    if (dropdown) {
      dropdown.classList.toggle('active');
    }
  }
};

// Initialize applications dropdown
function _initNavDropdown() {
  const triggers = document.querySelectorAll('.nav-dropdown-trigger');
  triggers.forEach(trigger => {
    trigger.addEventListener('click', window.toggleAppDropdown);
  });
  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('active'));
    }
  });
}

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
    flk.on('ready', function(){ 
      el.querySelectorAll('.flickity-prev-next-button').forEach(function(btn){ 
        if(!btn.getAttribute('aria-label')) btn.setAttribute('aria-label', btn.classList.contains('previous') ? 'Previous' : 'Next'); 
      }); 
    });
    // Enhanced resize and reload with better timing
    setTimeout(function(){ 
      try{ 
        flk.reloadCells(); 
        flk.resize(); 
        flk.reposition(); 
        // Ensure autoplay is active after initialization
        if(opts.autoPlay && !flk.isAutoPlaying) {
          flk.playPlayer();
        }
      }catch(e){ console.warn('Flickity reload error:', e); } 
    }, 300);
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
window.changeLanguage = function(lng) {
  if (typeof i18next !== 'undefined') {
    // normalize requested code, but prefer whichever resource key exists on the page
    let req = (lng || '').toString().toLowerCase();
    // candidate list for common variants
    const variants = {
      'ja': ['ja', 'jp'],
      'jp': ['ja', 'jp'],
      'cn': ['cn', 'zh', 'zh-cn'],
      'zh': ['cn', 'zh', 'zh-cn']
    };
    let chosen = req;
    const resources = (i18next && i18next.options && i18next.options.resources) ? i18next.options.resources : {};
    if (variants[req]) {
      // pick first variant that actually exists in resources
      chosen = variants[req].find(v => Object.prototype.hasOwnProperty.call(resources, v)) || variants[req][0];
    } else {
      // if exact exists use it, otherwise fallback to provided
      if (!Object.prototype.hasOwnProperty.call(resources, req)) {
        // nothing to do, keep req
      }
    }
    i18next.changeLanguage(chosen, window.updateContent);
    // Save language choice to localStorage
    try { localStorage.setItem('preferredLanguage', chosen); } catch(e){}
  }
  const btn = document.querySelector('.dropdown button');
  if (btn) {
    const code = (lng || '').toString().toUpperCase();
    if (code === 'JP' || code === 'JA') btn.textContent = 'JP';
    else if (code === 'ZH' || code === 'CN') btn.textContent = 'CN';
    else btn.textContent = code || 'EN';
  }
};

// Get saved language preference from localStorage
window.getSavedLanguage = function() {
  try {
    return localStorage.getItem('preferredLanguage') || 'en';
  } catch(e) {
    return 'en';
  }
};

// Update language button display to reflect current language
window.updateLanguageButtonDisplay = function() {
  const btn = document.querySelector('.dropdown button');
  if (btn && typeof i18next !== 'undefined') {
    const currentLng = i18next.language || 'en';
    if (currentLng === 'ja' || currentLng === 'jp') {
      btn.textContent = 'JP';
    } else if (currentLng === 'cn' || currentLng === 'zh' || currentLng === 'zh-cn') {
      btn.textContent = 'CN';
    } else {
      btn.textContent = 'EN';
    }
  }
};

window.updateContent = function() {
  if (typeof i18next === 'undefined') return;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = i18next.t(key);
  });
  // Also update language button display
  window.updateLanguageButtonDisplay();
};

// Scroll Reveal Animations handler
function _initScrollReveal() {
  if (!('IntersectionObserver' in window)) {
    // Fallback for older browsers: show everything
    document.querySelectorAll('.section-title, .section-desc, .is-divider').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  const observerOptions = { 
    threshold: 0.05, // Trigger earlier
    rootMargin: '0px 0px -50px 0px' // Offset to trigger slightly before coming into view
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-active');
        // Unobserve once shown for performance
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Select typical elements to reveal
  const revealTargets = document.querySelectorAll(
    '.section-title, .section-desc, .is-divider, .about-box, .business-sector-item, .product-item, .reveal-item, .reveal-item-img, .reveal-image, .product-category'
  );

  revealTargets.forEach(el => {
    // Only add reveal-hidden if it's not already visible (to avoid flicker)
    const rect = el.getBoundingClientRect();
    const isVisible = (rect.top < window.innerHeight && rect.bottom >= 0);
    
    if (isVisible) {
      el.classList.add('reveal-active');
    } else {
      el.classList.add('reveal-hidden');
      observer.observe(el);
    }
  });
}

// If a .products-grid contains only one meaningful product card, remove other placeholder cards
function _pruneSingleProductCards() {
  try {
    document.querySelectorAll('.products-grid').forEach(function(grid){
      const cards = Array.from(grid.children || []);
      if (cards.length <= 1) return; // nothing to do

      const meaningful = cards.filter(function(card){
        const text = (card.textContent || '').replace(/\s+/g,' ').trim();
        const textLen = text.length;
        const imgs = card.querySelectorAll('img');
        const hasImg = Array.from(imgs).some(function(img){
          const src = (img.getAttribute('src') || '').trim();
          return src && !src.startsWith('data:');
        });
        // treat as meaningful if there is an image (not a data: placeholder) or reasonable amount of text
        return hasImg || textLen > 8;
      });

      if (meaningful.length === 1) {
        const keep = meaningful[0];
        cards.forEach(function(card){ if (card !== keep) card.remove(); });
        // make grid single-column for better layout
        try { grid.style.gridTemplateColumns = '1fr'; } catch(e){}
        grid.classList.add('single-product-grid');
      }
    });
  } catch(e) { console.warn('pruneSingleProductCards error', e); }
}

// Auto-init common behaviors when DOM is ready
document.addEventListener('DOMContentLoaded', function(){
  _initSidebar();
  _initNavDropdown();
  _initFlyoutsAndMobile();
  _initAwardsLightbox();
  _initFlickity();
  _initBackToTop();
  _initNavbarScroll();
  _initScrollReveal();
  // Remove placeholder product cards when only one real product exists
  _pruneSingleProductCards();
  // Update language button display on page load
  setTimeout(window.updateLanguageButtonDisplay, 100);
});
