// Lightweight, responsive, infinite carousel
(function() {
  function initCarousel(container) {
    const track = container.querySelector('.simple-carousel');
    if (!track) return;

    let items = Array.from(track.querySelectorAll('.couple-item'));
    if (items.length < 2) return; // Not enough items to be a carousel

    const prevBtn = container.querySelector('.carousel-nav.prev');
    const nextBtn = container.querySelector('.carousel-nav.next');

    const autoplay = container.dataset.autoplay === 'true';
    const interval = parseInt(container.dataset.interval || '3000', 10);
    const mobileBreakpoint = 768;

    let slidesDesktop = parseInt(container.dataset.slidesDesktop || '3', 10);
    let slidesMobile = parseInt(container.dataset.slidesMobile || '3', 10);
    
    let stepPx = 0;
    let timerId = null;
    let isTransitioning = false;
    let isDragging = false;
    let startX = 0;
    let currentTranslate = 0;
    let startTranslate = 0;

    function calcLayout() {
        const isMobile = window.innerWidth < mobileBreakpoint;
        const slidesToShow = isMobile ? slidesMobile : slidesDesktop;

        // On mobile, CSS flex-basis controls the width. On desktop, we set it.
        if (!isMobile) {
            const containerWidth = container.clientWidth;
            const gap = (items.length > 1) ? parseFloat(window.getComputedStyle(items[0]).marginRight) * (slidesToShow - 1) : 0;
            const totalWidth = containerWidth - gap;
            const itemWidth = totalWidth / slidesToShow;
            items.forEach(item => {
                item.style.flex = `0 0 ${itemWidth}px`;
            });
        } else {
            // On mobile, remove inline style to let CSS take over
            items.forEach(item => {
                item.style.flex = '';
            });
        }

        // After styles are applied, get the real width of an item
        if (items.length > 0) {
            stepPx = items[0].offsetWidth;
        }

        const showNav = items.length > slidesToShow;
        if (prevBtn) prevBtn.style.display = showNav ? 'block' : 'none';
        if (nextBtn) nextBtn.style.display = showNav ? 'block' : 'none';
    }

    function updatePosition(animate = true) {
        track.style.transition = animate ? 'transform 500ms ease' : 'none';
        track.style.transform = `translateX(${currentTranslate}px)`;
    }

    function next() {
        if (isTransitioning) return;
        isTransitioning = true;
        stopAutoplay();

        currentTranslate -= stepPx;
        updatePosition();

        track.addEventListener('transitionend', () => {
            const firstItem = track.firstElementChild;
            if (firstItem) {
                track.appendChild(firstItem); // Move first item to the end
            }

            currentTranslate += stepPx;
            updatePosition(false); // Reset position without animation
            isTransitioning = false;
            startAutoplay();
        }, { once: true });
    }

    function prev() {
        if (isTransitioning) return;
        isTransitioning = true;
        stopAutoplay();

        const lastItem = track.lastElementChild;
        if (lastItem) {
            track.insertBefore(lastItem, track.firstElementChild); // Move last to start
        }

        currentTranslate += stepPx;
        updatePosition(false); // Jump to new start position

        requestAnimationFrame(() => {
            currentTranslate -= stepPx;
            updatePosition(true); // Animate back to original position

            track.addEventListener('transitionend', () => {
                isTransitioning = false;
                startAutoplay();
            }, { once: true });
        });
    }

    function getPositionX(event) {
        return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }

    function touchStart(event) {
        isDragging = true;
        startX = getPositionX(event);
        startTranslate = currentTranslate;
        stopAutoplay();
        track.style.transition = 'none';
    }

    function touchMove(event) {
        if (!isDragging) return;
        const currentPosition = getPositionX(event);
        const moveX = currentPosition - startX;
        currentTranslate = startTranslate + moveX;
        updatePosition(false);
    }

    function touchEnd() {
        if (!isDragging) return;
        isDragging = false;
        const movedBy = currentTranslate - startTranslate;

        // Snap to the nearest slide
        const slidesMoved = Math.round(movedBy / stepPx);
        if (slidesMoved < 0) {
            for (let i = 0; i < Math.abs(slidesMoved); i++) next();
        } else if (slidesMoved > 0) {
            for (let i = 0; i < slidesMoved; i++) prev();
        } else {
            // If not moved enough, snap back
            currentTranslate = startTranslate;
            updatePosition();
        }
        startAutoplay();
    }

    function startAutoplay() {
        if (!autoplay || items.length <= (window.innerWidth < mobileBreakpoint ? slidesMobile : slidesDesktop)) return;
        stopAutoplay();
        timerId = setInterval(next, interval);
    }

    function stopAutoplay() {
        clearInterval(timerId);
        timerId = null;
    }

    // --- Event Listeners ---
    if (nextBtn) nextBtn.addEventListener('click', next);
    if (prevBtn) prevBtn.addEventListener('click', prev);

    // Drag support
    track.addEventListener('mousedown', touchStart);
    track.addEventListener('mousemove', touchMove);
    track.addEventListener('mouseup', touchEnd);
    track.addEventListener('mouseleave', () => { if (isDragging) touchEnd(); });
    track.addEventListener('touchstart', touchStart, { passive: true });
    track.addEventListener('touchmove', touchMove, { passive: true });
    track.addEventListener('touchend', touchEnd);
    container.addEventListener('dragstart', (e) => e.preventDefault());

    // Autoplay pause on hover
    container.addEventListener('mouseenter', stopAutoplay);
    container.addEventListener('mouseleave', startAutoplay);

    // Re-calculate on resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            stopAutoplay();
            calcLayout();
            startAutoplay();
        }, 200);
    });

    // Initial setup
    calcLayout();
    startAutoplay();
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.simple-carousel-container').forEach(initCarousel);
  });
})();
