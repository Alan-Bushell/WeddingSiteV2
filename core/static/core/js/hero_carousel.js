// static/js/hero_carousel.js

document.addEventListener('DOMContentLoaded', function() {
    const carouselInterval = 4000; // Time in ms before changing slide (4 seconds)
    const animationDuration = 1500; // Needs to match CSS transition duration (1.5 seconds)
    const mobileBreakpoint = 768; // Matches your CSS media query breakpoint
    const imagesPerView = 3; // Number of images visible at once in the carousel window

    // Main function to start and manage a single carousel
    function startCarousel(carouselElement) {
        const inner = carouselElement.querySelector('.carousel-inner');
        const items = Array.from(inner.querySelectorAll('.carousel-item')); // Get original images

        // Crucial for seamless looping: Clone images and append them
        // We clone enough images to ensure a smooth transition back to the start
        // Cloning all original items twice generally provides enough buffer for smooth looping.
        for (let i = 0; i < items.length * 2; i++) {
            const clone = items[i % items.length].cloneNode(true);
            inner.appendChild(clone);
        }
        const allItems = Array.from(inner.querySelectorAll('.carousel-item')); // All images now, including clones

        let currentIndex = 0; // Tracks the current scroll position based on image index
        let currentIntervalId = null;

        // Function to update carousel state based on current device type and window size
        function updateCarouselState() {
            const isMobile = window.innerWidth <= mobileBreakpoint;

            // Clear any existing carousel interval before setting up a new one
            if (currentIntervalId) {
                clearInterval(currentIntervalId);
            }

            let itemDimension; // This will be the height per image for desktop, width per image for mobile
            let containerScrollDimension; // This will be the total height of .carousel-inner for desktop, total width for mobile

            if (!isMobile) { // Desktop (vertical scroll)
                const carouselHeight = carouselElement.clientHeight; // Height of the visible .hero-carousel window
                itemDimension = carouselHeight / imagesPerView; // Calculated height for each image slot

                allItems.forEach(item => {
                    item.style.width = '100%';
                    item.style.height = `${itemDimension}px`;
                    item.style.display = 'block'; // Ensure images stack vertically
                    item.style.whiteSpace = 'normal'; // Reset from mobile style for images
                });

                containerScrollDimension = itemDimension * allItems.length;
                inner.style.height = `${containerScrollDimension}px`; // Set total height of inner container
                inner.style.width = '100%';
                inner.style.whiteSpace = 'normal'; // Reset from mobile style for inner container
            } else { // Mobile (horizontal scroll)
                const carouselWidth = carouselElement.clientWidth; // Width of the visible .hero-carousel window
                itemDimension = carouselWidth / imagesPerView; // Calculated width for each image slot

                allItems.forEach(item => {
                    item.style.height = '100%';
                    item.style.width = `${itemDimension}px`;
                    item.style.display = 'inline-block'; // Ensure images stack horizontally
                    item.style.verticalAlign = 'top'; // Align correctly for inline-block
                });

                containerScrollDimension = itemDimension * allItems.length;
                inner.style.width = `${containerScrollDimension}px`; // Set total width of inner container
                inner.style.height = '100%';
                inner.style.whiteSpace = 'nowrap'; // Prevent wrapping for horizontal scroll
            }

            // Reset transform based on current index and new dimensions
            const translateProperty = isMobile ? 'translateX' : 'translateY';
            inner.style.transition = 'none'; // Temporarily disable transition for immediate repositioning
            inner.style.transform = `${translateProperty}(-${currentIndex * itemDimension}px)`;
            // Re-enable transition after a tiny delay for subsequent animations
            setTimeout(() => {
                inner.style.transition = `transform ${animationDuration / 1000}s ease-in-out`;
            }, 50);

            // Start the new carousel interval
            currentIntervalId = setInterval(() => {
                const step = 1; // Scroll by one image slot at a time
                currentIndex += step;

                const translateValue = currentIndex * itemDimension;

                inner.style.transition = `transform ${animationDuration / 1000}s ease-in-out`;
                inner.style.transform = `${translateProperty}(-${translateValue}px)`;

                // Logic for seamless looping (jump back when scrolled past original items)
                // We jump back to the start of the cloned section
                if (currentIndex >= items.length) {
                    // After the current animation completes, instantly jump back to the start of the cloned section
                    setTimeout(() => {
                        inner.style.transition = 'none'; // Temporarily disable transition for the jump
                        currentIndex = 0; // Reset index to the start of original items (which corresponds to the first clone of the original first item)
                        inner.style.transform = `${translateProperty}(-${currentIndex * itemDimension}px)`;
                        // Re-enable transition after a very short delay
                        setTimeout(() => {
                            inner.style.transition = `transform ${animationDuration / 1000}s ease-in-out`;
                        }, 50);
                    }, animationDuration); // Wait for the current scroll animation to finish
                }

            }, carouselInterval);
        }

        // Initial setup call for the carousel on page load
        updateCarouselState();

        // Re-initialize carousel state on window resize with a debounce to prevent excessive calls
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                updateCarouselState();
            }, 250); // Debounce delay
        });
    }

    // Find both carousel elements and initialize them
    const leftCarousel = document.querySelector('.hero-carousel-left');
    const rightCarousel = document.querySelector('.hero-carousel-right');

    if (leftCarousel) {
        startCarousel(leftCarousel);
    }
    if (rightCarousel) {
        startCarousel(rightCarousel);
    }
});