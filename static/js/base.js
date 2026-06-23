import {getAccessToken ,logout} from './auth.js';


document.addEventListener("DOMContentLoaded", async function () {
    const accessToken = getAccessToken();
    if (!accessToken) {
        window.location.href = "/login";
        return;
    }
});

document.getElementById("logoutBtn").addEventListener("click", logout);

document.querySelectorAll(".sidebar a").forEach(link => {
    if (link.href === window.location.href) {
          link.style.backgroundColor = "#9AA5B1";
          link.style.color = "#0B3C5D";
    }
});

const role = localStorage.getItem("role");
const username = localStorage.getItem("username");

document.getElementById("profileName").innerText = localStorage.getItem("username");
document.getElementById("profileRole").innerText = localStorage.getItem("role");

document.getElementById("usernameDisplay").innerText =
    "Welcome, " + username;

const sidebar = document.getElementById("sidebarMenu");
let menuItems = [];
if (role === "ADMIN") {
    menuItems = [
        { name: "Dashboard", link: "/Admin/dashboard", icon: "bi-speedometer2" },
        { name: "User Management", link: "/Admin/userManagement", icon: "bi-people" },
        { name: "Departments", link: "/admin/departments", icon: "bi-building" },
        { name: "Projects", link: "/admin/projects", icon: "bi-kanban" },
        { name: "Reports", link: "/admin/reports", icon: "bi-bar-chart" }
    ];
}

if (role === "MANAGER") {
    menuItems = [
        { name: "Dashboard", link: "/Manager/dashboard", icon: "bi-speedometer2" },
        { name: "Team", link: "/manager/team", icon: "bi-people" },
        { name: "Reports", link: "/manager/reports", icon: "bi-bar-chart" }
    ];
}

if (role === "EMPLOYEE") {
    menuItems = [
        { name: "Dashboard", link: "/Employee/dashboard", icon: "bi-speedometer2" },
        { name: "My Tasks", link: "/employee/tasks", icon: "bi-list-check" },
        { name: "Profile", link: "/employee/profile", icon: "bi-person" }
    ];
}

sidebar.innerHTML = menuItems.map(item => `
    <a href="${item.link}" class="menu-link">
        <i class="bi ${item.icon}"></i>
        <span class="menu-text">${item.name}</span>
    </a>
`).join("");

setActiveMenu();

function setActiveMenu() {
    const links = document.querySelectorAll(".menu-link");
    const currentPath = window.location.pathname;

    links.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
}

