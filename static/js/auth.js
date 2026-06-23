

export function getAccessToken() {
    return localStorage.getItem("access_token");
}


export function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

export function saveTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
}

function clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");
}

export function logout() {
    clearTokens();
    window.location.href = "/login";
}

export async function apiRequest(url, options = {}) {

    let accessToken = getAccessToken();

    options.headers = {
        ...options.headers,
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json"
    };

    let response = await fetch(url, options);


    if (response.status === 401) {

        const refreshed = await refreshAccessToken();

        if (refreshed) {
            options.headers["Authorization"] = "Bearer " + getAccessToken();
            return fetch(url, options);
        } else {
            logout();
            return;
        }
    }
    return response;
}


async function refreshAccessToken() {

    const refreshToken = getRefreshToken();

    if (!refreshToken) return false;

    try {
        const response = await fetch("/api/auth/refresh", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });

        if (!response.ok) {
            return false;
        }
        const data = await response.json();

        localStorage.setItem("access_token", data.access_token);

        return true;

    } catch (error) {
        return false;
    }
}