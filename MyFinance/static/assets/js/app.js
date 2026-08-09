document.addEventListener("DOMContentLoaded", function () {

    console.log("MyFinance Loaded");

});

document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.classList.remove("show");
            alert.classList.add("fade");

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 1500);

    });

});