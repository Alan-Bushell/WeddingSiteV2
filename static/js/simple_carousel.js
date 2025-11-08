// Lightweight, responsive carousel for .simple-carousel-container
// Features: prev/next buttons, responsive slides-per-view, optional autoplay, pause on hover

(function() {
  function initCarousel(container) {
    const track = container.querySelector('.simple-carousel');
    if (!track) return;

    const items = Array.from(track.querySelectorAll('.couple-item'));
    if (items.length === 0) return;

    const prevBtn = container.querySelector('.carousel-nav.prev');
    const nextBtn = container.querySelector('.carousel-nav.next');

    const autoplay = (container.dataset.autoplay || 'false') === 'true';
    const interval = parseInt(container.dataset.interval || '4000', 10);
    const mobileBreakpoint = 768;

    let slidesDesktop = parseInt(container.dataset.slidesDesktop || '1', 10);
    let slidesMobile = parseInt(container.dataset.slidesMobile || '1', 10);

  let slidesToShow = 1;
  let slideWidth = 0; // px width per slide
  let stepPx = 0; // px to move per slide including gap
    let currentIndex = 0; // index of the first visible slide
    let maxIndex = 0; // last valid starting index
    let timerId = null;

    // Apply essential styles to enable transform-based sliding
    container.style.position = 'relative';
    container.style.overflow = 'hidden';
  track.style.display = 'flex';
    track.style.willChange = 'transform';
    track.style.transition = 'transform 500ms ease';

    function calcLayout() {
      const isMobile = window.innerWidth < mobileBreakpoint;
      slidesToShow = isMobile ? slidesMobile : slidesDesktop;
      slidesToShow = Math.max(1, Math.min(slidesToShow, items.length));

      // compute width per slide and apply to items
      const containerWidth = container.clientWidth;
      // Mobile: prefer smaller tiles max 30% width each; Desktop: equal division
      if (isMobile) {
        const maxThirty = Math.floor(containerWidth * 0.30);
        // Ensure a reasonable minimum size
        slideWidth = Math.max(110, maxThirty);
      } else {
        slideWidth = Math.max(1, Math.round(containerWidth / slidesToShow));
      }
      items.forEach((el) => {
        el.style.flex = `0 0 ${slideWidth}px`;
        el.style.maxWidth = `${slideWidth}px`;
      });

      // Include CSS gap in the translate step to keep slides aligned
      const cs = window.getComputedStyle(track);
      const gapVal = (cs.gap || cs.columnGap || '0px');
      const gapPx = parseFloat(gapVal) || 0;
      stepPx = slideWidth + gapPx;

      maxIndex = Math.max(0, items.length - slidesToShow);
      // Clamp currentIndex in case resize changed bounds
      if (currentIndex > maxIndex) currentIndex = 0;
      updatePosition(false);

      // Hide/show nav based on slide count
      const showNav = items.length > slidesToShow;
      if (prevBtn) prevBtn.style.display = showNav ? 'block' : 'none';
      if (nextBtn) nextBtn.style.display = showNav ? 'block' : 'none';
    }

    function updatePosition(animate = true) {
      if (!animate) track.style.transition = 'none';
  const x = -(currentIndex * stepPx);
      track.style.transform = `translateX(${x}px)`;
      if (!animate) {
        // re-enable transition shortly after layout jump
        requestAnimationFrame(() => {
          track.style.transition = 'transform 500ms ease';
        });
      }
    }

    function goTo(index) {
      if (items.length === 0) return;
      // wrap around for continuous feel
      if (index > maxIndex) index = 0;
      if (index < 0) index = maxIndex;
      currentIndex = index;
      updatePosition(true);
    }

    function next() { goTo(currentIndex + 1); }
    function prev() { goTo(currentIndex - 1); }

    function startAutoplay() {
      if (!autoplay || items.length <= slidesToShow) return;
      stopAutoplay();
      timerId = setInterval(next, interval);
    }
    function stopAutoplay() {
      if (timerId) {
        clearInterval(timerId);
        timerId = null;
      }
    }

    // Event listeners
    if (nextBtn) nextBtn.addEventListener('click', next);
    if (prevBtn) prevBtn.addEventListener('click', prev);

    // Pause autoplay on hover/focus
    container.addEventListener('mouseenter', stopAutoplay);
    container.addEventListener('mouseleave', startAutoplay);
    container.addEventListener('focusin', stopAutoplay);
    container.addEventListener('focusout', startAutoplay);

    // Recompute on resize
    let resizeT;
    window.addEventListener('resize', () => {
      clearTimeout(resizeT);
      resizeT = setTimeout(calcLayout, 200);
    });

    // Initialize
    calcLayout();
    startAutoplay();
  }

  document.addEventListener('DOMContentLoaded', function() {
    const containers = document.querySelectorAll('.simple-carousel-container');
    containers.forEach(initCarousel);
  });
})();
