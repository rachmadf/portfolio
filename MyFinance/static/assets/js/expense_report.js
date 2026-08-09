/**
 * ==========================================================
 * Expense Monthly Report
 * ==========================================================
 */
console.log("expense_report.js loaded");
document.addEventListener("DOMContentLoaded", function () {

    //--------------------------------------------------------
    // Get category summary from Flask
    //--------------------------------------------------------
    if (typeof categorySummary === "undefined") {
        return;
    }

    const labels = categorySummary.map(item => item.category);

    const totals = categorySummary.map(item => Number(item.total));

    //--------------------------------------------------------
    // Currency formatter
    //--------------------------------------------------------
    const currencyFormatter = new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0
        }
    );

    //--------------------------------------------------------
    // Color palette
    //--------------------------------------------------------
    const colors = [
        "#0d6efd",
        "#198754",
        "#ffc107",
        "#dc3545",
        "#6f42c1",
        "#20c997",
        "#fd7e14",
        "#6610f2",
        "#0dcaf0",
        "#adb5bd"
    ];

    //--------------------------------------------------------
    // Horizontal Bar Chart
    //--------------------------------------------------------
    const barCanvas = document.getElementById("expenseBarChart");

    if (barCanvas) {

        new Chart(barCanvas, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{
                    label: "Expense",
                    data: totals,
                    backgroundColor: colors,
                    borderRadius: 6
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis: "y",

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return currencyFormatter.format(
                                    context.raw
                                );
                            }
                        }
                    }
                },

                scales: {

                    x: {

                        beginAtZero: true,

                        ticks: {

                            callback: function (value) {

                                return currencyFormatter.format(value);
                            }
                        }
                    },

                    y: {

                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    //--------------------------------------------------------
    // Doughnut Chart
    //--------------------------------------------------------
    const doughnutCanvas = document.getElementById("expenseDoughnutChart");

    if (doughnutCanvas) {

        new Chart(doughnutCanvas, {

            type: "doughnut",

            data: {

                labels: labels,

                datasets: [{
                    data: totals,
                    backgroundColor: colors,
                    borderWidth: 1
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "65%",

                plugins: {

                    legend: {

                        position: "bottom"
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return (
                                    context.label +
                                    ": " +
                                    currencyFormatter.format(context.raw)
                                );
                            }
                        }
                    }
                }
            }
        });
    }


    //--------------------------------------------------------
    // Daily Expense Trend
    //--------------------------------------------------------
    if (typeof dailyTrend !== "undefined") {

        const dailyCanvas = document.getElementById("dailyExpenseTrendChart");

        if (dailyCanvas) {

            const dailyLabels = dailyTrend.map(item => item.date);
            const dailyTotals = dailyTrend.map(item => Number(item.total));

            new Chart(dailyCanvas, {

                type: "line",

                data: {

                    labels: dailyLabels,

                    datasets: [{

                        label: "Daily Expense",

                        data: dailyTotals,

                        borderColor: "#0d6efd",

                        backgroundColor: "rgba(13,110,253,0.15)",

                        fill: true,

                        tension: 0.3,

                        pointRadius: 4,

                        pointHoverRadius: 6

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    interaction: {

                        intersect: false,

                        mode: "index"

                    },

                    plugins: {

                        legend: {

                            display: false

                        },

                        tooltip: {

                            callbacks: {

                                label(context) {

                                    return currencyFormatter.format(
                                        context.raw
                                    );

                                }

                            }

                        }

                    },

                    scales: {

                        y: {

                            beginAtZero: true,

                            ticks: {

                                callback(value) {

                                    return currencyFormatter.format(value);

                                }

                            }

                        }

                    }

                }

            });

        }

    }

    //--------------------------------------------------------
    // DataTable
    //--------------------------------------------------------

    const table =
        document.getElementById("expenseTransactionTable");

    if (table) {

        $(function () {

            $("#expenseTransactionTable").DataTable({

                pageLength: 10,

                lengthMenu: [
                    [10, 25, 50, 100],
                    [10, 25, 50, 100]
                ],

                order: [[0, "desc"]],

                responsive: true

            });

        });

    }

// end of code
});