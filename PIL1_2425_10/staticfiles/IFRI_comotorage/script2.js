// Removing localStorage dependencies since they won't work in Django context
const butsignup = document.getElementById('to_signup');
const butsignin = document.getElementById('to_login');

butsignup.addEventListener('click', () => showCard("signup-form"));
butsignin.addEventListener('click', () => showCard("login-form"));

function showCard(form) {
  document.querySelectorAll("section").forEach((element) => {
    element.style.display = element.classList.contains(form) ? "block" : "none";
  });
}

// Initially show login form
showCard("login-form");

// Change Theme Logic
const changeThemeButton = document.getElementById("change_theme");

function setTheme(theme) {
  document.body.classList.toggle("dark-mode", theme === "dark");
  changeThemeButton.innerHTML = theme === "dark" ? '<i class="ri-moon-fill"></i>' : '<i class="ri-sun-fill"></i>';
  // Store theme preference if needed (you might want to use Django sessions instead)
}

changeThemeButton.addEventListener("click", () => {
  const currentTheme = document.body.classList.contains("dark-mode") ? "light" : "dark";
  setTheme(currentTheme);
});

// Set initial theme based on system preference
const savedTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
setTheme(savedTheme);

// Handle logout with Django CSRF
const logoutBtn = document.getElementById('logout_btn');

if (logoutBtn) {
    logoutBtn.addEventListener('click', function(event) {
        event.preventDefault(); 

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        const csrftoken = getCookie('csrftoken');

        fetch('/auth/logout/', { 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/Login/'; 
            } else {
                console.error('Logout failed:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
        });
    });
}

// Welcome page logic (if user is authenticated)
if (document.querySelector('.welcome-form')) {
    // Show welcome form if user is authenticated
    const welcomeSection = document.querySelector('.welcome-form');
    if (welcomeSection && document.body.dataset.authenticated === 'true') {
        showCard("welcome-form");
    }
}

// Handle form navigation buttons
const changePasswordBtn = document.getElementById('change_password_btn');
const deleteAccountBtn = document.getElementById('delete_account_btn');
const changeCancelBtn = document.getElementById('change_cancel');
const deleteCancelBtn = document.getElementById('delete_cancel');

if (changePasswordBtn) {
    changePasswordBtn.addEventListener('click', () => showCard("change-password-form"));
}

if (deleteAccountBtn) {
    deleteAccountBtn.addEventListener('click', () => showCard("delete-account-form"));
}

if (changeCancelBtn) {
    changeCancelBtn.addEventListener('click', () => showCard("welcome-form"));
}

if (deleteCancelBtn) {
    deleteCancelBtn.addEventListener('click', () => showCard("welcome-form"));
}