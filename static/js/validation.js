import { apiRequest } from './auth.js';



const getRoles = "/api/user/getRoles";
const getManager = "/api/user/getManager"

export function validateForm() {

    let valid = true;

    document.querySelectorAll(".form-control, .form-select").forEach(field => {

        field.classList.remove("is-invalid");

        const feedback = field.parentElement.querySelector(".invalid-feedback");

        if (feedback) {
            feedback.textContent = "";
        }

    });

    valid &= validateRequired("firstName", "First name is required.");
    valid &= validateRequired("lastName", "Last name is required.");
    valid &= validateEmail();
    valid &= validatePassword();
    valid &= validateRole();
    valid &= validateManager();

    return Boolean(valid);

}

export  function validateRequired(id, message) {

    const input = document.getElementById(id);

    if (input.value.trim() === "") {

        showError(input, message);

        return false;
    }

    return true;

}

export function validateEmail() {

    const email = document.getElementById("email");

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email.value.trim() === "") {

        showError(email, "Email is required.");

        return false;

    }

    if (!regex.test(email.value.trim())) {

        showError(email, "Enter a valid email.");

        return false;

    }

    return true;

}

export function validatePassword() {

    const password = document.getElementById("password");

    if (password.value.trim() === "") {

        showError(password, "Password is required.");

        return false;

    }
    if (password.value.length < 6) {

        showError(password, "Password must be at least 6 characters.");

        return false;

    }

    return true;

}

export function validateRole() {

    const role = document.getElementById("role");
    if (role.value === "") {

        showError(role, "Please select a role.");

        return false;

    }

    return true;
}

export function validateManager() {

    const managerDiv = document.getElementById("managerDiv");
    const manager = document.getElementById("managerId");

   
    if (managerDiv.classList.contains("d-none")) {
        manager.classList.remove("is-invalid");
        return true;
    }

    if (manager.value === "") {
        showError(manager, "Please select a manager.");
        return false;
    }

    manager.classList.remove("is-invalid");
    return true;
}

export function showError(input, message) {

    input.classList.add("is-invalid");

    const feedback = input.parentElement.querySelector(".invalid-feedback");

    if (feedback) {

        feedback.textContent = message;

    }

}

export function toggleManager(){
    
    const selectedrole = document.getElementById("role");
    const managerDiv = document.getElementById("managerDiv");
    const managerId = document.getElementById("managerId");
    
    selectedrole.addEventListener("change", function(){
    
        const selected = this.options[this.selectedIndex].text;
        if(selected === "employee"){
            managerDiv.classList.remove("d-none");
        }else{
            managerDiv.classList.add("d-none");
            managerId.value = "";
        }

    });

};


export async function loadRoles() {

    const response = await apiRequest(`${getRoles}`);
    const result = await response.json();

    //  const role = document.getElementById("role");
    role.innerHTML = '<option value="">Select Role</option>';

    result.data.forEach(item => {

        role.innerHTML += `
            <option value="${item.id}">
                ${item.name}
            </option>
        `;

    });

}

export async function loadManagers() {

    const response =  await apiRequest(`${getManager}`);
    const result = await response.json();

    const manager = document.getElementById("managerId");

    manager.innerHTML = '<option value="">Select Manager</option>';

    result.data.forEach(item => {

        manager.innerHTML += `
            <option value="${item.id}">
                ${item.name}
            </option>
        `;

    });

}
