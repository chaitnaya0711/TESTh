(() => {
    // High-End Intersection Observer for scroll reveal animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -100px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                // Optional: unobserve after showing once for permanent state
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Wait for entry loading animations to finish before registering scroll observer
    setTimeout(() => {
        document.querySelectorAll('.reveal-up').forEach(element => {
            const delay = element.getAttribute('data-reveal-delay');
            if (delay) {
                element.style.setProperty('--reveal-delay', `${delay}ms`);
            }
            observer.observe(element);
        });
    }, 3500);
})();
