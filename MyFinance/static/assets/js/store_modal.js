$(document).ready(function () {
    $("#tblStoreLookup").DataTable({
        responsive: true,
        pageLength: 8,
        lengthChange: false,
        ordering: true,
        searching: true,
        info: true,
        language: {
            search: "Search:",
            emptyTable: "No stores found"
        }
    });
});

// store selection
$(document).on("click", ".btnSelectStore", function () {
    $("#store_id").val($(this).data("id"));
    $("#store_name").val($(this).data("name"));
    bootstrap.Modal
        .getInstance(document.getElementById("storeModal"))
        .hide();
});

// debug:
// $(document).on("click", ".btnSelectStore", function () {

//     console.log("Store button clicked");

//     console.log($(this).data("id"));
//     console.log($(this).data("name"));

//     $("#store_id").val($(this).data("id"));
//     $("#store_name").val($(this).data("name"));

//     console.log($("#store_name").val());

// });

$(document).on("click", ".btnSelectStore", function () {
    $("#store_id").val($(this).data("id"));
    $("#store_name").val($(this).data("name"));
    bootstrap.Modal
        .getInstance(document.getElementById("storeModal"))
        .hide();

    loadAvailableItems();
});