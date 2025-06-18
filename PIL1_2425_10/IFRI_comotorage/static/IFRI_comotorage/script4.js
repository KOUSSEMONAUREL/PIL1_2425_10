document.addEventListener('DOMContentLoaded', function() {

    const toggleBtn = document.getElementById('span');
    const sidebar = document.getElementById('footer');
    let hideSidebarTimeout;

    if (window.matchMedia("(min-width: 500px)").matches) {
        const showSidebar = () => {
            clearTimeout(hideSidebarTimeout);
            sidebar.style.left = '0';
            toggleBtn.innerHTML = '<i class="fas fa-angle-left"></i>';
            toggleBtn.style.left = '120px';
        };

        const hideSidebar = () => {
            hideSidebarTimeout = setTimeout(() => {
                sidebar.style.left = '-120px';
                toggleBtn.innerHTML = '<i class="fas fa-angle-right"></i>';
                toggleBtn.style.left = '0';
            }, 300);
        };

        toggleBtn.addEventListener('mouseenter', showSidebar);
        toggleBtn.addEventListener('mouseleave', hideSidebar);

        sidebar.addEventListener('mouseenter', showSidebar);
        sidebar.addEventListener('mouseleave', hideSidebar);

        toggleBtn.addEventListener('click', () => {
            if (sidebar.style.left === '0px') {
                hideSidebar();
            } else {
                showSidebar();
            }
        });
    }

    // Gestion de l'affichage conditionnel des erreurs
    function showErrorsOnlyWhenNeeded() {
        const inputs = document.querySelectorAll('.input');
        
        inputs.forEach(input => {
            const inputBox = input.closest('.input-box');
            const parentContainer = inputBox?.closest('.username-email-input, .username-input, .email-input, .password-input');
            const errorSpan = parentContainer?.querySelector('.error-span');
            
            if (errorSpan) {
                // Masquer l'erreur par défaut
                errorSpan.style.display = 'none';
                
                // Enlever les styles d'erreur par défaut
                input.classList.remove('error');
                input.style.borderColor = '';
                input.style.boxShadow = '';
                
                // Afficher l'erreur seulement s'il y a du contenu d'erreur
                const errorText = errorSpan.querySelector('.error-text');
                if (errorText && errorText.textContent.trim() !== '') {
                    errorSpan.style.display = 'flex';
                    input.style.borderColor = '#dc3545';
                    input.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
                }
            }
        });
    }
    
    // Appeler la fonction au chargement
    showErrorsOnlyWhenNeeded();
    
    // Nettoyer les erreurs lors de la saisie
    const inputs = document.querySelectorAll('.input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const inputBox = this.closest('.input-box');
            const parentContainer = inputBox?.closest('.username-email-input, .username-input, .email-input, .password-input');
            const errorSpan = parentContainer?.querySelector('.error-span');
            
            if (errorSpan && this.value.trim() !== '') {
                // Masquer l'erreur lors de la saisie
                errorSpan.style.display = 'none';
                this.style.borderColor = '';
                this.style.boxShadow = '';
                
                // Ajouter le style focus
                this.addEventListener('focus', function() {
                    this.style.borderColor = '#007bff';
                    this.style.boxShadow = '0 0 0 0.2rem rgba(0, 123, 255, 0.25)';
                });
            }
        });
    });
    
    // Masquer automatiquement les messages Django après 5 secondes
    const messages = document.querySelectorAll('.messages .alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Amélioration de la navigation entre login et signup
    const toSignupBtn = document.getElementById('to_signup');
    const toLoginBtn = document.getElementById('to_login');
    const loginForm = document.querySelector('.login-form');
    const signupForm = document.querySelector('.signup-form');
    
    if (toSignupBtn) {
        toSignupBtn.addEventListener('click', function() {
            loginForm.style.display = 'none';
            signupForm.style.display = 'block';
            
            // Nettoyer les erreurs lors du changement de formulaire
            clearFormErrors();
        });
    }
    
    if (toLoginBtn) {
        toLoginBtn.addEventListener('click', function() {
            signupForm.style.display = 'none';
            loginForm.style.display = 'block';
            
            // Nettoyer les erreurs lors du changement de formulaire
            clearFormErrors();
        });
    }
    
    function clearFormErrors() {
        const errorSpans = document.querySelectorAll('.error-span');
        const inputs = document.querySelectorAll('.input');
        
        errorSpans.forEach(span => {
            span.style.display = 'none';
        });
        
        inputs.forEach(input => {
            input.style.borderColor = '';
            input.style.boxShadow = '';
            input.value = '';
        });
    }
    
    // Validation en temps réel pour le formulaire d'inscription
    const signupInputs = {
        username: document.querySelector('#id_username'),
        email: document.querySelector('#id_email'),
        password1: document.querySelector('#id_password1'),
        password2: document.querySelector('#id_password2')
    };
    
    // Validation du nom d'utilisateur
    if (signupInputs.username) {
        signupInputs.username.addEventListener('blur', function() {
            if (this.value.length < 3) {
                showFieldError(this, 'Le nom d\'utilisateur doit contenir au moins 3 caractères.');
            }
        });
    }
    
    // Validation de l'email
    if (signupInputs.email) {
        signupInputs.email.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.value)) {
                showFieldError(this, 'Veuillez entrer une adresse e-mail valide.');
            }
        });
    }
    
    // Validation de la confirmation du mot de passe
    if (signupInputs.password2) {
        signupInputs.password2.addEventListener('blur', function() {
            const password1 = signupInputs.password1?.value;
            if (this.value !== password1) {
                showFieldError(this, 'Les mots de passe ne correspondent pas.');
            }
        });
    }
    
    function showFieldError(input, message) {
        const inputBox = input.closest('.input-box');
        const parentContainer = inputBox?.closest('.username-input, .email-input, .password-input');
        const errorSpan = parentContainer?.querySelector('.error-span');
        const errorText = errorSpan?.querySelector('.error-text');
        
        if (errorSpan && errorText) {
            errorText.textContent = message;
            errorSpan.style.display = 'flex';
            input.style.borderColor = '#dc3545';
            input.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
        }
    }
});