import { saveTokens, getAccessToken } from './auth.js';

document.getElementById("toggleBtn").addEventListener("click", function(){

    const passwordField = document.getElementById("password");
    const icon = document.getElementById("toggleIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.innerHTML = "🙈";
    } else {
        passwordField.type = "password";
        icon.innerHTML = "👁";
    }
});


document.getElementById("loginBtn").addEventListener("click", login);
async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("error");

    errorDiv.innerText = "";

    if(email == ""){
        errorDiv.innerHTML = "Username Or Email is required";
        return;
    }
    else if(password == ""){
        errorDiv.innerHTML = "Password is required";
        return;
    }

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
            errorDiv.innerText = "Invalid credentials. Please try again.";
            console.log(data.message);
        }

    } catch (error) {
        console.log("Internal Server error.");
    }
}

function redirectByRole(role) {


    switch(role){
        case "ADMIN":
            window.location.href = routes.admin;
            break;

        case "MANAGER":
            window.location.href = routes.manager;
            break;

        case "EMPLOYEE":
            window.location.href = routes.employee;
            break;

        default:
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