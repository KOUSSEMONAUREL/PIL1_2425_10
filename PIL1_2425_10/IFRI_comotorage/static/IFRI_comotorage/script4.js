document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('span');
    const sidebar = document.getElementById('footer');
    let hideSidebarTimeout;

    if (window.matchMedia("(min-width: 500px)").matches) {
        toggleBtn.addEventListener('mouseenter', () => {
            clearTimeout(hideSidebarTimeout);
            sidebar.style.left = '0';
            toggleBtn.innerHTML = '<i class="fas fa-angle-left"></i>';
            toggleBtn.style.left = '100px';

            hideSidebarTimeout = setTimeout(() => {
                sidebar.style.left = '-120px';
                toggleBtn.innerHTML = '<i class="fas fa-angle-right"></i>';
                toggleBtn.style.left = '0';
            }, 2000);
        });

        sidebar.addEventListener('mouseenter', () => {
            clearTimeout(hideSidebarTimeout);
            sidebar.style.left = '0';
            toggleBtn.innerHTML = '<i class="fas fa-angle-left"></i>';
            toggleBtn.style.left = '100px';
        });

        sidebar.addEventListener('mouseleave', () => {
            hideSidebarTimeout = setTimeout(() => {
                sidebar.style.left = '-120px';
                toggleBtn.innerHTML = '<i class="fas fa-angle-right"></i>';
                toggleBtn.style.left = '0';
            }, 200);
        });
    }

});