import { apiRequest } from './auth.js';
import { validateForm, toggleManager, loadRoles, loadManagers} from './validation.js';


const createUser = "/api/user/createUser";


// const managerDiv = document.getElementById("managerDiv");
// const managerId = document.getElementById("managerId");


document.addEventListener("DOMContentLoaded", async () => {

    await loadRoles();
    await loadManagers();

});


 toggleManager();


const password = document.getElementById("password");
const toggle = document.getElementById("togglePassword");
toggle.addEventListener("click", function () {

    if (password.type === "password") {

        password.type = "text";
        this.innerHTML = '<i class="bi bi-eye-slash"></i>';

    } else {

        password.type = "password";
        this.innerHTML = '<i class="bi bi-eye"></i>';

    }

});


document.getElementById("userForm").addEventListener("submit", async function (e) {

     e.preventDefault();

    if (!validateForm()) {
        return;
    }
    const payload = {
        firstName: document.getElementById("firstName").value.trim(),
        lastName: document.getElementById("lastName").value.trim(),
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value,
        roleId: Number(document.getElementById("role").value),
        managerId: document.getElementById("managerId").value
            ? Number(document.getElementById("managerId").value)
            : null,
        isActive: document.getElementById("status").value === "true"
    };

    try {

        const response = await apiRequest(createUser, {
            method: "POST",
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.success) {

            alert(result.message);
            window.location.href = "/Admin/userManagement";

        } else {

            alert(result.message);
        }

    } catch (error) {
        console.error(error);
        alert("Something went wrong.");
    }


});

