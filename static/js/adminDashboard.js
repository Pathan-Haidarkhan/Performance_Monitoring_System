import { apiRequest } from './auth.js';

const CompanyPerformance = "/api/dashboard/companyPerformance";
const TopPerformers = "/api/dashboard/topPerformers";
const PerformanceTrend = "/api/dashboard/performanceTrend";
const CompanyRanking = "/api/dashboard/companyRanking";
const RankingDistribution = "/api/dashboard/ratingDistribution";



document.getElementById("filterbtn").addEventListener("click", loadDashboard);

let rankingTable;
let month;
let year;

$(document).ready(function () {

    const today = new Date();

    document.getElementById("filterMonth").value = today.getMonth() + 1;
    document.getElementById("filterYear").value = today.getFullYear();

    populateYearDropdown();
    loadDashboard();


    month = document.getElementById("filterMonth").value;
    year = document.getElementById("filterYear").value;

    rankingTable = $('#rankingTable').DataTable({
   
        
        serverSide: true,
        searching: true,  
        ordering: true,
        pageLength: 10,
        order:[[2,'desc']],
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        language: {
            lengthMenu: "_MENU_&nbsp;&nbsp;entries per page",
            emptyTable: "No ranking data available",
            processing: "Loading..."
        },
        columnDefs: [
            { targets: 0, orderable: false }
        ],

        ajax: async function (data, callback) {

            const page = (data.start / data.length) + 1;
            const pageSize = data.length
            const search = data.search.value;

            const sortColumn = data.columns[data.order[0].column].data;
            const sortDirection = data.order[0].dir;

           

            const response = await apiRequest(
                `${CompanyRanking}?month=${month}&year=${year}&page=${page}&pagesize=${pageSize}&search=${search}&sortcolumn=${sortColumn}&sortdirection=${sortDirection}`
            );

            const result = await response.json();

            callback({
                draw: data.draw,
                recordsTotal: result.data.totalRecords,
                recordsFiltered: result.data.totalRecords,
                data: result.data.items
            });
        },

        columns: [
            { data: "rank", className: "text-center" },
            { data: "employee", className: "text-center", orderSequence: ['asc', 'desc'] },
            { data: "score", className: "text-center", orderSequence: ['asc', 'desc'] },
            {
                data: "rating", className: "text-center", orderSequence: ['asc', 'desc'],
                render: function (data) {
                    return `<span class="rating-badge rating-${data}">
                                ${data}
                            </span>`;
                }
            }
        ]
    });
});

async function loadDashboard() {

    month = document.getElementById("filterMonth").value;
    year = document.getElementById("filterYear").value;

    loadCompanySummary(month, year);
    loadTopPerformers(month, year);
   
    loadRankingDistribution(month, year);
    loadTrend();

    if (rankingTable) {
        rankingTable.ajax.reload();
    }
}

async function loadCompanySummary(month, year) {

    const response = await apiRequest(
        `${CompanyPerformance}?month=${month}&year=${year}`
    );

    const result = await response.json();
    const data = result.data;

    animateCounter("totalEmployees", data.totalEmployees);
    animateCounter("averageScore", data.averageScore, "%");
    animateCounter("highestScore", data.highestScore);
    animateCounter("lowestScore", data.lowestScore);

}

async function loadTopPerformers(month, year) {

    const response = await apiRequest(
        `${TopPerformers}?month=${month}&year=${year}`
    );

    const result = await response.json();
    const data = result.data || [];

    const table = document.getElementById("topPerformersTable");

    const tableContainer = document.getElementById("topPerformersTableContainer");
    const emptyState = document.getElementById("topPerformersEmpty");


    table.innerHTML = "";


    if (data.length === 0) {

        tableContainer.classList.add("d-none");
        emptyState.classList.remove("d-none");

        return;
    }


    tableContainer.classList.remove("d-none");
    emptyState.classList.add("d-none");

    let rows = "";

    data.forEach((emp, index) => {

        let medal = index + 1;

        if (index === 0) {
            medal = "🥇";
        }
        else if (index === 1) {
            medal = "🥈";
        }
        else if (index === 2) {
            medal = "🥉";
        }

        rows += `
            <tr>
                <td>${medal}</td>
                <td>${emp.name}</td>
                <td>${emp.totalScore}</td>
                <td>
                    <span class="rating-badge rating-${emp.rating}">
                        ${emp.rating}
                    </span>
                </td>
            </tr>
        `;
    });

    table.innerHTML = rows;
}

async function loadTrend() {

    const response = await apiRequest(
        `${PerformanceTrend}?months=6`
    );

    const result = await response.json();
    const data = result.data;

    showTrendChart(data);

}

async function loadCompanyRanking(month, year,page = 1) {

    let currentPage = page;
    const pageSize = 10;

    rankingTable.ajax.reload();

}

async function loadRankingDistribution(month, year) {
    const response = await apiRequest(
        `${RankingDistribution}?month=${month}&year=${year}`
    );

    const result = await response.json();
    const data = result.data;
    const labels = data.labels;
    const values = data.values;

    const chartContainer =
        document.getElementById("ratingChartContainer");

    const emptyState =
        document.getElementById("ratingChartEmpty");

    if (labels.length === 0 || values.length === 0) {

        chartContainer.classList.add("d-none");
        emptyState.classList.remove("d-none");

        return;
    }

    chartContainer.classList.remove("d-none");
    emptyState.classList.add("d-none");

    createRatingChart(data.labels, data.values)

    labels.forEach((label, index) => {

        const count = values[index];

        switch (label.toUpperCase()) {

            case "EXCELLENT":
                document.getElementById("excellentCount").textContent = count;
                break;

            case "GOOD":
                document.getElementById("goodCount").textContent = count;
                break;

            case "AVERAGE":
                document.getElementById("averageCount").textContent = count;
                break;

            case "POOR":
                document.getElementById("poorCount").textContent = count;
                break;
        }
    });
}

let trendChartInstance = null;

function createTrendChart(labels, values) {

    const ctx = document.getElementById("performanceChart").getContext("2d");
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, "rgba(11,60,93,0.4)");
    gradient.addColorStop(1, "rgba(11,60,93,0)");

    if (trendChartInstance) {
        trendChartInstance.destroy();
    }

    trendChartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Average Performance Score",
                data: values,
                borderColor: "#0B3C5D",
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.3,
                fill: true,
                pointRadius: 4
            }]
        },
        options: {

            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                }
            },

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}

function createRatingChart(labels, values) {

    const ctx = document.getElementById("ratingChart");
    const existingChart = Chart.getChart("ratingChart");

    if (existingChart) {
        existingChart.destroy();
    }
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}


function animateCounter(elementId, targetValue, suffix = "") {

    const element = document.getElementById(elementId);
    let start = 0;

    const duration = 800;
    const increment = targetValue / (duration / 16);

    function updateCounter() {
        start += increment;

        if (start >= targetValue) {
            element.innerText = Math.round(targetValue) + suffix;
            return;
        }

        element.innerText = Math.round(start) + suffix;
        requestAnimationFrame(updateCounter);
    }

    updateCounter();
}

function showTrendChart(data) {

    document.getElementById("trendLoader").style.display = "none";
    document.getElementById("performanceChart").style.display = "block";

    const badge = document.getElementById("trendGrowthBadge");
    const growth = data.growthPercentage;
    badge.textContent = `${growth}%`;

    badge.classList.remove(
        "bg-success",
        "bg-danger",
        "bg-secondary"
    );

    if (growth > 0) {
        badge.classList.add("bg-success");
        badge.textContent = `+${growth}%`;
    }
    else if (growth < 0) {
        badge.classList.add("bg-danger");
        badge.textContent = `${growth}%`;
    }
    else {
        badge.classList.add("bg-secondary");
        badge.textContent = "0%";
    }


    createTrendChart(data.labels, data.values);

}

function populateYearDropdown() {

    const startYear = 2022;
    const currentYear = new Date().getFullYear();
    const yearSelect = document.getElementById("filterYear");

    for (let year = currentYear; year >= startYear; year--) {

        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;

        yearSelect.appendChild(option);
    }

    yearSelect.value = currentYear;
}