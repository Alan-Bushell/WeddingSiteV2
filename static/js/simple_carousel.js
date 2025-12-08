// Lightweight, responsive carousel for .simple-carousel-container
// Features: prev/next buttons, responsive slides-per-view, optional autoplay, pause on hover, infinite loop, touch support

(function() {
  function initCarousel(container) {
    const track = container.querySelector('.simple-carousel');
    if (!track) return;

    const originalItems = Array.from(track.querySelectorAll('.couple-item'));
    if (originalItems.length === 0) return;

    const prevBtn = container.querySelector('.carousel-nav.prev');
    const nextBtn = container.querySelector('.carousel-nav.next');

    const autoplay = (container.dataset.autoplay || 'false') === 'true';
    const interval = parseInt(container.dataset.interval || '4000', 10);
    const mobileBreakpoint = 768;

    let slidesDesktop = parseInt(container.dataset.slidesDesktop || '1', 10);
    let slidesMobile = parseInt(container.dataset.slidesMobile || '1', 10);

    let items = [];
    let slidesToShow = 1;
    let slideWidth = 0; // px width per slide
    let stepPx = 0; // px to move per slide including gap
    let currentIndex = 0; // index of the first visible slide
    let timerId = null;
    let isTransitioning = false;
    let isDragging = false;
    let startX = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;

    // Clone items for infinite loop
    const clonesToCreate = Math.max(slidesDesktop, slidesMobile, 1);
    const clonesEnd = originalItems.slice(0, clonesToCreate).map(item => item.cloneNode(true));
    const clonesStart = originalItems.slice(-clonesToCreate).map(item => item.cloneNode(true));
    
    track.append(...clonesEnd);
    track.prepend(...clonesStart);
    items = Array.from(track.querySelectorAll('.couple-item'));
    currentIndex = clonesToCreate;

    // Apply essential styles to enable transform-based sliding
    container.style.position = 'relative';
    container.style.overflow = 'hidden';
    track.style.display = 'flex';
    track.style.willChange = 'transform';
    track.style.transition = 'transform 500ms ease';

    function calcLayout() {
      const isMobile = window.innerWidth < mobileBreakpoint;
      slidesToShow = isMobile ? slidesMobile : slidesDesktop;
      slidesToShow = Math.max(1, Math.min(slidesToShow, originalItems.length));

      const containerWidth = container.clientWidth;
      if (isMobile) {
        const maxThirty = Math.floor(containerWidth * 0.30);
        slideWidth = Math.max(110, maxThirty);
      } else {
        const desktopScale = 0.385; // match CSS intended width proportion
        slideWidth = Math.max(1, Math.round((containerWidth / slidesToShow) * desktopScale));
      }
      items.forEach((el) => {
        el.style.flex = `0 0 ${slideWidth}px`;
        el.style.maxWidth = `${slideWidth}px`;
      });

      const cs = window.getComputedStyle(track);
      const gapVal = (cs.gap || cs.columnGap || '0px');
      const gapPx = parseFloat(gapVal) || 0;
      stepPx = slideWidth + gapPx;

      updatePosition(false);

      const showNav = originalItems.length > slidesToShow;
      if (prevBtn) prevBtn.style.display = showNav ? 'block' : 'none';
      if (nextBtn) nextBtn.style.display = showNav ? 'block' : 'none';
    }

    function updatePosition(animate = true) {
      if (!animate) track.style.transition = 'none';
      currentTranslate = -(currentIndex * stepPx);
      track.style.transform = `translateX(${currentTranslate}px)`;
      if (!animate) {
        requestAnimationFrame(() => {
          track.style.transition = 'transform 500ms ease';
        });
      }
    }

    function goTo(index, animate = true) {
      if (isTransitioning) return;
      isTransitioning = true;
      currentIndex = index;
      updatePosition(animate);
    }

    function next() { goTo(currentIndex + 1); }
    function prev() { goTo(currentIndex - 1); }

    function handleTransitionEnd() {
      isTransitioning = false;
      if (currentIndex >= originalItems.length + clonesToCreate) {
        currentIndex = clonesToCreate;
        updatePosition(false);
      } else if (currentIndex < clonesToCreate) {
        currentIndex = originalItems.length + clonesToCreate - 1;
        updatePosition(false);
      }
    }

    function touchStart(index) {
      return function(event) {
        isDragging = true;
        startX = getPositionX(event);
        prevTranslate = currentTranslate;
        stopAutoplay();
        track.style.transition = 'none';
      }
    }

    function touchMove(event) {
      if (isDragging) {
        const currentPosition = getPositionX(event);
        const moveX = currentPosition - startX;
        currentTranslate = prevTranslate + moveX;
        track.style.transform = `translateX(${currentTranslate}px)`;
      }
    }

    function touchEnd() {
      isDragging = false;
      const movedBy = currentTranslate - prevTranslate;
      if (movedBy < -50) next();
      else if (movedBy > 50) prev();
      else goTo(currentIndex); // Snap back

      startAutoplay();
      track.style.transition = 'transform 500ms ease';
    }

    function getPositionX(event) {
      return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }

    function startAutoplay() {
      if (!autoplay || originalItems.length <= slidesToShow) return;
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
    track.addEventListener('transitionend', handleTransitionEnd);

    // Touch events
    track.addEventListener('touchstart', touchStart(0));
    track.addEventListener('touchmove', touchMove);
    track.addEventListener('touchend', touchEnd);

    // Mouse drag events (for desktop)
    track.addEventListener('mousedown', touchStart(0));
    track.addEventListener('mousemove', touchMove);
    track.addEventListener('mouseup', touchEnd);
    track.addEventListener('mouseleave', () => { if(isDragging) touchEnd(); });
    track.addEventListener('dragstart', (e) => e.preventDefault());


    // Pause autoplay on hover/focus
    container.addEventListener('mouseenter', stopAutoplay);
    container.addEventListener('mouseleave', startAutoplay);
    container.addEventListener('focusin', stopAutoplay);
    container.addEventListener('focusout', startAutoplay);

    // Recompute on resize
    let resizeT;
    window.addEventListener('resize', () => {
      clearTimeout(resizeT);
      resizeT = setTimeout(() => {
        stopAutoplay();
        calcLayout();
        startAutoplay();
      }, 200);
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
