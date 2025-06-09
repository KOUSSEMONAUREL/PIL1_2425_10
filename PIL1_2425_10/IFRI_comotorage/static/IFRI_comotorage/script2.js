let data = JSON.parse(localStorage.getItem("Account")) || [];
const remember = localStorage.getItem("Remember");
let account;
const toSignUpButton = document.getElementById("to_signup");
toSignUpButton.addEventListener("click", () => {
  showCard("signup-form");
  clearSignUp();
});
const toLogInButton = document.getElementById("to_login");
toLogInButton.addEventListener("click", () => {
  showCard("login-form");
  clearSignUp();
});

// Helper function to show or hide cards
function showCard(form) {
  document.querySelectorAll("section").forEach((element) => {
    element.style.display = element.className === form ? "" : "none";
  });
}

// Show Welcome if account exists
if (remember) {
  account = data.find(item => item.username === remember);
  if (account) toWelcome();
} else {
  showCard("login-form");
}

// Show Error
function showError(box, display, error) {
  box.parentElement.classList.add("invalid");
  display.innerHTML = error;
  display.parentElement.style.display = "block";
}

function hideError(box, display) {
  box.parentElement.classList.remove("invalid");
  display.innerHTML = "";
  display.parentElement.style.display = "none";
}

// Check if value exists in data
function checkIfExists(field, value) {
  return data.some(item => item[field] === value);
}

// Sign Up ---------------------------------------------------------------->
const regForm = {
  username: document.getElementById("username"),
  email: document.getElementById("email"),
  password: document.getElementById("reg_password"),
  passwordConfirm: document.getElementById("conreg_password"),
  check: document.getElementById("reg_check"),
  submitButton: document.getElementById("signup_submit"),
};

let validation = {
  username: false,
  email: false,
  password: false,
  passwordConfirm: false,
};

// Validate form fields
function validateUsername() {
  const usernameRegex = /^[A-Za-z0-9_.]{0,25}$/;
  const username = regForm.username.value;
  if (!username.match(usernameRegex)) {
    showError(regForm.username, document.getElementById("username_error"), "Username can only use letters, numbers, underscores, and periods.");
    validation.username = false;
  } else if (checkIfExists("username", username)) {
    showError(regForm.username, document.getElementById("username_error"), "This username is already taken.");
    validation.username = false;
  } else {
    hideError(regForm.username, document.getElementById("username_error"));
    validation.username = true;
  }
}

function validateEmail() {
  const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  const email = regForm.email.value;
  if (!email.match(emailRegex)) {
    showError(regForm.email, document.getElementById("email_error"), "Invalid email.");
    validation.email = false;
  } else if (checkIfExists("email", email)) {
    showError(regForm.email, document.getElementById("email_error"), "This email is already taken.");
    validation.email = false;
  } else {
    hideError(regForm.email, document.getElementById("email_error"));
    validation.email = true;
  }
}

function validatePassword() {
  const password = regForm.password.value;
  if (!password) {
    showError(regForm.password, document.getElementById("reg_password_error"), "Password can't be empty.");
    validation.password = false;
  } else {
    hideError(regForm.password, document.getElementById("reg_password_error"));
    validation.password = true;
  }
}

function validatePasswordConfirm() {
  const confirmPassword = regForm.passwordConfirm.value;
  if (confirmPassword !== regForm.password.value) {
    showError(regForm.passwordConfirm, document.getElementById("conreg_password_error"), "Passwords do not match.");
    validation.passwordConfirm = false;
  } else {
    hideError(regForm.passwordConfirm, document.getElementById("conreg_password_error"));
    validation.passwordConfirm = true;
  }
}

// Check Sign Up
regForm.submitButton.addEventListener("click", () => {
  validateUsername();
  validateEmail();
  validatePassword();
  validatePasswordConfirm();

  if (Object.values(validation).every(val => val === true)) {
    data.push({
      username: regForm.username.value,
      email: regForm.email.value,
      password: regForm.password.value,
    });
    localStorage.setItem("Account", JSON.stringify(data));
    showCard("login-form");
    clearSignUp();
  }
});

// Save Data and Clear Fields
function clearSignUp() {
  regForm.username.value = "";
  regForm.email.value = "";
  regForm.password.value = "";
  regForm.passwordConfirm.value = "";
  regForm.check.checked = false;
  Object.keys(validation).forEach(field => validation[field] = false);
}

// Login ------------------------------------------------------------------>
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
    toWelcome();
    clearLogin();
  } else {
    showError(logForm.usernameOrEmail, document.getElementById("username_email_error"), "Invalid credentials.");
  }
}

logForm.submitButton.addEventListener("click", login);

// Clear Login Fields
function clearLogin() {
  logForm.usernameOrEmail.value = "";
  logForm.password.value = "";
  logForm.remember.checked = false;
}

// Welcome Page ------------------------------------------------------------>
function toWelcome() {
  document.getElementById("name_output").textContent = account.username;
  showCard("welcome-form");
}

// Logout
document.getElementById("logout_btn").addEventListener("click", () => {
  localStorage.removeItem("Remember");
  showCard("login-form");
});

// Change Theme ------------------------------------------------------------>
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