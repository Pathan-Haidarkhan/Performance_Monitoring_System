import { apiRequest } from './auth.js';
import { validateForm, loadRoles, loadManagers, toggleManager } from './validation.js';



const updateUserById = "/api/user/updateUser"; 
const gerUserById = "/api/user/getUserById"; 

document.addEventListener("DOMContentLoaded", async () => {

    await loadRoles();

    await loadManagers();

    await loadUser();

});

async function loadUser() {
    
    const firstName = document.getElementById("firstName");
    const lastName = document.getElementById("lastName");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const role = document.getElementById("role");
    const managerId = document.getElementById("managerId");
    const status = document.getElementById("status");
    
    const response = await apiRequest(`${gerUserById}/${userId}`);

    const result = await response.json();

    const user = result.data;

    firstName.value = user.firstName;
    lastName.value = user.lastName;
    email.value = user.email;
    password.value = user.password;
    role.value = user.roleId;
    

    managerId.value = user.managerId ?? "";
    status.value = user.isActive.toString();
    

  
    const managerDiv = document.getElementById("managerDiv");
    const manager = document.getElementById("managerId");

    const selectedOption = role.options[role.selectedIndex].text;

    if (!selectedOption) {
        return;
    }

    if (selectedOption === "employee") {

        managerDiv.classList.remove("d-none");

    } else {

        managerDiv.classList.add("d-none");
        manager.value = "";
    }
}

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



document.getElementById("userForm").addEventListener("submit", updateUser);

async function updateUser(e){

    e.preventDefault();

    if(!validateForm())
        return;

    const dto = {

        firstName:firstName.value.trim(),
        lastName:lastName.value.trim(),
        email:email.value.trim(),
        password: password.value.trim(),
        roleId:Number(role.value),
        managerId:managerId.value
            ? Number(managerId.value)
            : null,
        isActive:status.value==="true"

    };

    try{
            const response = await apiRequest(

            `${updateUserById}/${userId}`,

            {
                method:"PUT",
                body:JSON.stringify(dto)
            }

        );

        const result = await response.json();

        if(result.success){

            alert(result.message);

        window.location.href = "/Admin/userManagement";

        } else {

            alert(result.message);
        }
    }
    catch (error) {
        console.error(error);
        alert("Something went wrong.");
    }

}