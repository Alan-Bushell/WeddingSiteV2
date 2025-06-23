// static/js/hero_carousel.js

document.addEventListener('DOMContentLoaded', function() {
    const carouselInterval = 4000; // Time in ms before changing slide (4 seconds)
    const animationDuration = 1500; // Needs to match CSS transition duration (1.5 seconds)
    const mobileBreakpoint = 768; // Matches your CSS media query breakpoint

    // Helper to apply the correct animation class
   function applySlideClass(element, direction, type) {
            // type: 'in' or 'out'
            // direction: 'up', 'down', 'left', 'right'
            // Ensure no <span> tags or curly braces { } around ${type} or ${direction}
            element.classList.add(`slide-${type}-${direction}`);
        }

    // Helper to remove all animation classes for cleanup
    function removeSlideClasses(element) {
        element.classList.remove('slide-in-up', 'slide-in-down', 'slide-in-left', 'slide-in-right',
                                 'slide-out-up', 'slide-out-down', 'slide-out-left', 'slide-out-right');
    }

    // Main function to start and manage a single carousel
    function startCarousel(carouselElement) {
        const inner = carouselElement.querySelector('.carousel-inner');
        const items = inner.querySelectorAll('.carousel-item');
        let currentIndex = 0;
        let currentIntervalId = null;

        // Get desired directions from data attributes on the carousel container
        const desktopDirection = carouselElement.dataset.carouselDirectionDesktop;
        const mobileDirection = carouselElement.dataset.carouselDirectionMobile;

        // Function to update carousel state based on current device type
        // This function will be called on initial load and whenever the window is resized
        function updateCarouselState() {
            const isMobile = window.innerWidth <= mobileBreakpoint;
            const activeDirection = isMobile ? mobileDirection : desktopDirection;

            // Ensure only one active item is visible/ready to animate
            // Clean up any lingering animation classes from previous state/resize
            items.forEach((item, index) => {
                if (index === currentIndex) {
                    item.classList.add('active');
                    item.style.opacity = '1';
                    removeSlideClasses(item);
                } else {
                    item.classList.remove('active');
                    item.style.opacity = '0';
                    removeSlideClasses(item);
                }
            });

            // Clear any existing carousel interval to prevent multiple intervals running
            if (currentIntervalId) {
                clearInterval(currentIntervalId);
            }

            // Start a new interval for the carousel animation
            currentIntervalId = setInterval(() => {
                const currentItem = items[currentIndex];
                let nextIndex = (currentIndex + 1) % items.length;
                const nextItem = items[nextIndex];

                // 1. Prepare current item to slide out and fade out
                currentItem.classList.remove('active'); // Deactivate current item
                applySlideClass(currentItem, activeDirection, 'out'); // Add slide-out class
                currentItem.style.opacity = '0'; // Ensure it starts fading

                // 2. Prepare next item to slide in (position it off-screen)
                removeSlideClasses(nextItem); // Remove any old classes
                applySlideClass(nextItem, activeDirection, 'in'); // Add slide-in class
                nextItem.style.opacity = '0'; // Ensure it's initially invisible

                // 3. A very small delay before making the next item active.
                // This allows the browser to register the 'slide-in' class before 'active' is added,
                // which then causes the transition from the off-screen position to the 'active' position.
                setTimeout(() => {
                    nextItem.classList.add('active'); // Make next item active
                    removeSlideClasses(nextItem); // This removes the 'slide-in-X' class, triggering the transition back to its default (0,0) transform
                    nextItem.style.opacity = '1'; // Fade it in
                }, 50); // Small delay, adjust if needed for smoother animation start

                // 4. After the animation duration, clean up the old item's classes
                // This is important so it's ready for its next turn to become the 'nextItem'
                setTimeout(() => {
                    removeSlideClasses(currentItem);
                }, animationDuration);

                // Move to the next index
                currentIndex = nextIndex;

            }, carouselInterval);
        }

        // Initial setup call for the carousel
        updateCarouselState();

        // Re-initialize carousel state on window resize
        // We use a debounce to prevent the function from firing too many times during a resize operation,
        // which can be performance intensive.
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                updateCarouselState();
            }, 250); // Debounce delay in ms
        });
    }

    // Find all carousel elements and initialize them
    const leftCarousel = document.querySelector('.hero-carousel-left');
    const rightCarousel = document.querySelector('.hero-carousel-right');

    if (leftCarousel) {
        startCarousel(leftCarousel);
    }
    if (rightCarousel) {
        startCarousel(rightCarousel);
    }
});