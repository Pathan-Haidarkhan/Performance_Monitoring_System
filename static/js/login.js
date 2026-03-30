import { saveTokens, getAccessToken } from './auth.js';


function togglePassword() {

    const passwordField = document.getElementById("password");
    const icon = document.getElementById("toggleIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.innerHTML = "🙈";
    } else {
        passwordField.type = "password";
        icon.innerHTML = "👁";
    }
}


document.getElementById("loginBtn").addEventListener("click", login);
async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("error");

    errorDiv.innerText = "";

    try {

        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            saveTokens(data.data.access_token, data.data.refresh_token);

            localStorage.setItem("userId", data.data.user_id);
            localStorage.setItem("role", data.data.role);
            localStorage.setItem("username", data.data.username)

            redirectByRole(data.data.role)



        } else {
            errorDiv.innerText = data.data.message || "Invalid credentials";
        }

    } catch (error) {
        errorDiv.innerText = "Server error. Please try again.";
    }
}

function redirectByRole(role) {

    if (role === "admin"){
        window.location.href = routes.admin;
    }
    else if (role === "manager"){
        window.location.href = routes.manager;
    }
    else if (role === "employee"){
        window.location.href = routes.employee;
    }
    else{
        logout();
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const token = getAccessToken();
    const role = localStorage.getItem("role");

    if (token && role) {
        redirectByRole(role);
    }

});