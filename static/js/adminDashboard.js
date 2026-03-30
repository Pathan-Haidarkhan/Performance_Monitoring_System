import{ apiRequest } from './auth.js';

const CompanyPerformance = "/api/dashboard/companyPerformance";
const TopPerformers = "/api/dashboard/topPerformers";
const PerformanceTrend = "/api/dashboard/performanceTrend";
const CompanyRanking = "/api/dashboard/companyRanking";
const RankingDistribution = "/api/dashboard/ratingDistribution";



document.addEventListener("DOMContentLoaded", function(){

    const today = new Date();

    document.getElementById("filterMonth").value = today.getMonth() + 1;
    document.getElementById("filterYear").value = today.getFullYear();

    populateYearDropdown();
    loadDashboard();

});

async function loadDashboard() {

const month = document.getElementById("filterMonth").value;
const year = document.getElementById("filterYear").value;

loadCompanySummary(month, year);
loadTopPerformers(month, year);
loadTrend();

}

async function loadCompanySummary(month, year){

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

async function loadTopPerformers(month, year){

const response = await apiRequest(
`{TopPerformers}?month=${month}&year=${year}`
);

const result = await response.json();
const data = result.data;

const table = document.getElementById("topPerformersTable");

table.innerHTML = "";

data.forEach((emp,index)=>{
    table.innerHTML += `
        <tr>
        <td>${index+1}</td>
        <td>${emp.name}</td>
        <td>${emp.totalScore}</td>
        <td>${emp.rating}</td>
        </tr>
        `;
    });

}

async function loadTrend(){

const response = await apiRequest(
`${PerformanceTrend}?months=6`
);

const result = await response.json();
const data = result.data;

showTrendChart(data);

}

async function loadCompanyRanking(month, year){

    const response = await apiRequest(
    `${CompanyRanking}?month=${month}&year=${year}`
    );

    const result = await response.json();
    const data = result.data;

    const table = document.getElementById("rankingTable");

    let html = "";

    data.forEach(row => {

        html += `
        <tr>
            <td>${row.rank}</td>
            <td>${row.employee}</td>
            <td>${row.score}</td>
            <td>
                <span class="rating-badge rating-${row.rating}">
                ${row.rating}
                </span>
            </td>
        </tr>
        `;

    });
    table.innerHTML = html;
}

async function loadRankingDistribution(month, year){
     const response = await apiRequest(
    `${RankingDistribution}?month=${month}&year=${year}`
    );

    const result = await response.json();
    const data = result.data;

    createRatingChart(data.labels, data.values)
}

let trendChartInstance = null;

function createTrendChart(labels, values) {

    const ctx = document.getElementById("performanceChart").getContext("2d");
    const gradient = ctx.createLinearGradient(0,0,0,300);
    gradient.addColorStop(0,"rgba(11,60,93,0.4)");
    gradient.addColorStop(1,"rgba(11,60,93,0)");

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


function animateCounter(elementId, targetValue, suffix="") {

    const element = document.getElementById(elementId);
    let start = 0;

    const duration = 800;
    const increment = targetValue / (duration / 16);

    function updateCounter() {
        start += increment;

        if(start >= targetValue){
            element.innerText = Math.round(targetValue) + suffix;
            return;
        }

        element.innerText = Math.round(start) + suffix;
        requestAnimationFrame(updateCounter);
    }

    updateCounter();
}

function showTrendChart(data){

    document.getElementById("trendLoader").style.display = "none";
    document.getElementById("performanceChart").style.display = "block";

    createTrendChart(data.labels, data.values);

}

function populateYearDropdown(){

    const startYear = 2022;
    const currentYear = new Date().getFullYear();
    const yearSelect = document.getElementById("filterYear");

    for(let year = currentYear; year >= startYear; year--){

        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;

        yearSelect.appendChild(option);
    }

    yearSelect.value = currentYear;
}