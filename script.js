// ------------------ API URLs ------------------
const API_BASE = "http://127.0.0.1:5000";
const WELL_OUTPUT_URL = `${API_BASE}/api/predict_well_output`;
const EQUIPMENT_ANOMALIES_URL = `${API_BASE}/api/predict_equipment_anomalies`;
// ⚠️ The dedicated route for core metrics data (wells, refineries, etc.)
const CORE_METRICS_URL = `${API_BASE}/api/core_metrics`; 

const LOGISTICS_OPTIMIZATION_URL = `${API_BASE}/api/analytics/logistics_optimization`;
// ------------------ Fetch Data + Render Charts ------------------

/**
 * Utility function to determine color based on database status.
 * This ensures the color coding is driven by the MySQL trigger's output.
 * @param {string} status - 'CRITICAL' or 'HEALTHY'
 * @returns {string} - Hex color code
 */
function getColor(status) {
    // Red for CRITICAL (set by the trigger, typically 3 days or less)
    return status === 'CRITICAL' ? '#e74c3c' : '#3498db'; 
}

// 1️⃣ Predicted Well Output (Uses well_name and predicted_output from ML model)
async function renderWellOutput() {
    try {
        const res = await fetch(WELL_OUTPUT_URL);
        const data = await res.json();

        const labels = data.map(item => item.well_name || "Well");
        const values = data.map(item => item.predicted_output || item.total_output || 0);

        new Chart(document.getElementById("wellOutputChart"), {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Predicted Output (barrels)",
                    data: values,
                    borderColor: "#007bff",
                    borderWidth: 2,
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: "top" }
                }
            }
        });
    } catch (err) {
        console.error("Error loading Well Output:", err);
    }
}

// 2️⃣ Equipment Anomalies (Uses equipment_name and anomaly_score from ML model)
async function renderEquipmentAnomalies() {
    try {
        const res = await fetch(EQUIPMENT_ANOMALIES_URL);
        const data = await res.json();

        const labels = data.map(item => item.equipment_name || `Equipment ${item.equipment_id}`);
        // Anomaly score of -1 or 1 is returned by IsolationForest. We simplify it to 1 for Anomaly.
        const values = data.map(item => (item.anomaly_score === -1 ? 1 : 0)); 

        new Chart(document.getElementById("equipmentAnomalyChart"), {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Anomaly Status",
                    data: values,
                    backgroundColor: values.map(score => (score === 1 ? "#e74c3c" : "#1abc9c")), // Red for Anomaly, Green for Normal
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: "top" }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.1, // Max to clearly show 1 (Anomaly) or 0 (Normal)
                        ticks: {
                            stepSize: 1,
                            // Display 'Anomaly' for 1 and 'Normal' for 0
                            callback: function(value, index, ticks) {
                                return value === 1 ? 'Anomaly' : (value === 0 ? 'Normal' : '');
                            }
                        }
                    }
                }
            }
        });
    } catch (err) {
        console.error("Error loading Equipment Anomalies:", err);
    }
}

// 3️⃣ Refinery Efficiency (Uses refinery_name and the calculated efficiency)
async function renderRefineryEfficiency() {
    try {
        const canvasElement = document.getElementById("refineryEfficiencyChart");
        if (!canvasElement) {
            console.error("Refinery Chart Error: Canvas element with ID 'refineryEfficiencyChart' not found in HTML.");
            return;
        }
        
        const res = await fetch(CORE_METRICS_URL); 
        const data = await res.json();
        
        // This line assumes the Flask key is 'refinery_performance'. Check Flask if still broken.
        const refineryData = data.refinery_performance || []; 
        
        if (refineryData.length === 0) {
             console.warn("Refinery Chart Warning: refinery_performance data array is empty. Check Flask API output.");
             return;
        }
        
        const labels = refineryData.map(item => item.refinery_name);
        
        // ✅ CRITICAL FIX: Ensure value is parsed as a number.
        // It uses parseFloat to handle strings and falls back to 0 if the result is invalid (NaN).
        const values = refineryData.map(item => parseFloat(item.efficiency_percent) || 0); 

        new Chart(canvasElement, {
            type: "pie",
            data: {
                labels,
                datasets: [{
                    label: "Efficiency %",
                    data: values,
                    backgroundColor: ["#007bff", "#1abc9c", "#f87171", "#fbbf24", "#3b82f6", "#f43f5e", "#8b5cf6"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "right" }
                }
            }
        });
    } catch (err) {
        console.error("Error loading Refinery Efficiency:", err);
    }
}

// 4️⃣ Logistics Optimization (FINAL TRIGGER INTEGRATION)
async function renderLogisticsOptimization() {
    try {
        const res = await fetch(LOGISTICS_OPTIMIZATION_URL);
        const data = await res.json();
        
        const recommendations = data.recommendations || [];
        
        // Sort by days_of_stock_remaining (lowest is most critical)
        recommendations.sort((a, b) => a.days_of_stock_remaining - b.days_of_stock_remaining);
        
        const labels = recommendations.map(item => `${item.outlet_name} (${item.refinery_name})`);
        const values = recommendations.map(item => item.days_of_stock_remaining);

        new Chart(document.getElementById("logisticsOptimizationChart"), {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Days of Stock Remaining (Criticality)",
                    data: values,
                    // CORE LOGIC: Color driven by the 'stock_status' field set by the MySQL TRIGGER.
                    backgroundColor: recommendations.map(r => getColor(r.stock_status)), 
                    borderColor: "#fff",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, position: "top" }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Days'
                        }
                    }
                }
            }
        });
    } catch (err) {
        console.error("Error loading Logistics Optimization:", err);
    }
}


// 5️⃣ Retail Sales & Stock Summary (NEW: Supports Outcome 7)
async function renderRetailSalesSummary() {
    try {
        const res = await fetch(CORE_METRICS_URL);
        const data = await res.json();
        
        const retailData = data.retail_sales || [];
        
        // Data fields from core_queries: total_sales, total_stock, refinery_name
        const labels = retailData.map(item => item.refinery_name || `Refinery ${item.refinery_id}`);
        const sales = retailData.map(item => item.total_sales);
        const stock = retailData.map(item => item.total_stock);

        new Chart(document.getElementById("retailSalesSummaryChart"), {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Total Sales (Daily)",
                    data: sales,
                    backgroundColor: '#2ecc71',
                },
                {
                    label: "Total Current Stock",
                    data: stock,
                    backgroundColor: '#3498db',
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" }
                },
                scales: {
                    x: {
                        stacked: false,
                    },
                    y: {
                        beginAtZero: true,
                        stacked: false
                    }
                }
            }
        });
    } catch (err) {
        console.error("Error loading Retail Sales Summary:", err);
    }
}


// ------------------ Init ------------------
document.addEventListener("DOMContentLoaded", () => {
    renderWellOutput();
    renderEquipmentAnomalies();
    renderRefineryEfficiency();
    renderLogisticsOptimization();
    renderRetailSalesSummary(); 
});
