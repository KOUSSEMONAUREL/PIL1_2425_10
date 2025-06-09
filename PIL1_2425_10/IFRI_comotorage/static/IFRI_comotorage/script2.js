let data = JSON.parse(localStorage.getItem("Account")) || [];
let account;
const remember = localStorage.getItem("Remember");

// Switch between forms (login or signup)
function showCard(form) {
  document.querySelectorAll("section").forEach((element) => {
    element.style.display = element.className === form ? "" : "none";
  });
}

// Display login form if no account is found
if (remember) {
  account = data.find(item => item.username === remember);
  if (account) showCard("welcome-form");
} else {
  showCard("login-form");
}

// Sign Up Logic
const regForm = {
  username: document.getElementById("username"),
  email: document.getElementById("email"),
  password: document.getElementById("reg_password"),
  passwordConfirm: document.getElementById("conreg_password"),
  submitButton: document.getElementById("signup_submit"),
};

// Active ou désactive le bouton de soumission en fonction de la validité des champs
function toggleSubmitButton() {
  const username = regForm.username.value;
  const email = regForm.email.value;
  const password = regForm.password.value;
  const passwordConfirm = regForm.passwordConfirm.value;

  const isValid =
    username && email && password && password === passwordConfirm;

  regForm.submitButton.disabled = !isValid;
}

// Validation des champs lors de la saisie
function validateSignup() {
  const username = regForm.username.value;
  const email = regForm.email.value;
  const password = regForm.password.value;
  const passwordConfirm = regForm.passwordConfirm.value;

  if (!username || !email || !password || password !== passwordConfirm) {
    alert("Please fill out the form correctly.");
    return;
  }

  // Vérification si le nom d'utilisateur ou l'email existe déjà
  if (data.some(item => item.username === username || item.email === email)) {
    alert("Username or email already taken.");
    return;
  }

  // Sauvegarde du nouvel utilisateur
  data.push({ username, email, password });
  localStorage.setItem("Account", JSON.stringify(data));
  showCard("login-form");
}

// Événements pour valider les champs à chaque saisie
regForm.username.addEventListener("input", toggleSubmitButton);
regForm.email.addEventListener("input", toggleSubmitButton);
regForm.password.addEventListener("input", toggleSubmitButton);
regForm.passwordConfirm.addEventListener("input", toggleSubmitButton);

// Sign up event listener
regForm.submitButton.addEventListener("click", validateSignup);

// Login Logic
const logForm = {
  usernameOrEmail: document.getElementById("username_email"),
  password: document.getElementById("password"),
  remember: document.getElementById("remember_check"),
  submitButton: document.getElementById("login_submit"),
};

// Handle login
function login() {
  const value = logForm.usernameOrEmail.value;
  const user = data.find(item => item.username === value || item.email === value);

  if (user && user.password === logForm.password.value) {
    if (logForm.remember.checked) {
      localStorage.setItem("Remember", user.username);
    }
    account = user;
    showCard("welcome-form");
  } else {
    alert("Invalid credentials.");
  }
}

// Login event listener
logForm.submitButton.addEventListener("click", login);

// Welcome Page Logic
function toWelcome() {
  document.getElementById("name_output").textContent = account.username;
  showCard("welcome-form");
}

// Logout Logic
document.getElementById("logout_btn").addEventListener("click", () => {
  localStorage.removeItem("Remember");
  showCard("login-form");
});

// Change Theme Logic
const changeThemeButton = document.getElementById("change_theme");

function setTheme(theme) {
  document.body.classList.toggle("dark-mode", theme === "dark");
  changeThemeButton.innerHTML = theme === "dark" ? '<i class="ri-moon-fill"></i>' : '<i class="ri-sun-fill"></i>';
  localStorage.setItem("theme", theme);
}

changeThemeButton.addEventListener("click", () => {
  const currentTheme = document.body.classList.contains("dark-mode") ? "light" : "dark";
  setTheme(currentTheme);
});

// Initialize Theme
const savedTheme = localStorage.getItem("theme") || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
setTheme(savedTheme);