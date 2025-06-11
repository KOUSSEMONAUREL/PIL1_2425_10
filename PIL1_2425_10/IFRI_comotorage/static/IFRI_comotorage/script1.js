let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.furt');
    const dots = document.querySelectorAll('.dot');

    slides.forEach(slide => {
        slide.style.display = 'none';
    });

    slides[index].style.display = 'flex';    

    dots.forEach(dot => dot.classList.remove('active'));

    dots[index].classList.add('active');

    currentSlide = index;
}

document.addEventListener('DOMContentLoaded', () => {
    showSlide(0);
});


function handleMobileSections() {
    const prefooterH3s = document.querySelectorAll('.prefooter h3');
    const furt0 = document.querySelector('.furt0');
    const furt1 = document.getElementById('furt1');
    const furt2 = document.getElementById('furt2');
    const furt3 = document.getElementById('furt3');

    function isMobile() {
        return window.innerWidth < 500;
    }

    function hideAllSections() {
        if (furt1) furt1.style.display = 'none';
        if (furt2) furt2.style.display = 'none';
        if (furt3) furt3.style.display = 'none';
        if (furt0) furt0.style.display = 'none';
    }

    function showSection(sectionId) {
        hideAllSections();
        const section = document.getElementById(sectionId);
        if (section && furt0) {
            furt0.style.display = 'block';
            section.style.display = 'block';
        }
    }

    prefooterH3s.forEach((h3, index) => {
        h3.addEventListener('click', (event) => {
            if (isMobile()) {
                event.preventDefault();
                
                const sectionMap = {
                    0: 'furt1',
                    1: 'furt2',
                    2: 'furt3'
                };

                showSection(sectionMap[index]);
            }
        });
    });

    document.addEventListener('click', (e) => {
        if (isMobile()) {
            if (e.target === furt0) {
                hideAllSections();

            }
        }
    });

    function addCloseButtons() {
        const sections = [furt1, furt2, furt3];
        sections.forEach(section => {
            if (section && !section.querySelector('.close-btn')) {
                const closeBtn = document.createElement('span');
                closeBtn.innerHTML = '×';
                closeBtn.className = 'close-btn';
                closeBtn.style.cssText = 'position: absolute; top: 10px; right: 15px; font-size: 30px; color: #666; cursor: pointer; font-weight: bold; z-index: 1001;';
                closeBtn.addEventListener('click', hideAllSections);
                section.appendChild(closeBtn);
            }
        });
    }

    addCloseButtons();

    window.addEventListener('resize', () => {
        if (!isMobile()) {
            hideAllSections();
        }
    });

    if (isMobile()) {
        hideAllSections();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    handleMobileSections();
});