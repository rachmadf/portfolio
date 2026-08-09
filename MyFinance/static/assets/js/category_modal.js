$(document).ready(function () {
    $("#tblCategoryLookup").DataTable({
        responsive: true,
        pageLength: 8,
        lengthChange: false,
        ordering: true,
        searching: true,
        info: true,
        language: {

            search: "Search:",

            emptyTable: "No categories found"
        }
    });
});

// select category
$(document).on("click", ".btnSelectCategory", function () {
    $("#category_id").val($(this).data("id"));
    $("#category_name").val($(this).data("name"));
    bootstrap.Modal
        .getInstance(document.getElementById("categoryModal"))
        .hide();

    // loadAvailableItems();
});


$(document).on("click", ".btnSelectCategory", function () {
    $("#category_id").val($(this).data("id"));
    $("#category_name").val($(this).data("name"));
    bootstrap.Modal
        .getInstance(document.getElementById("categoryModal"))
        .hide();
    loadAvailableItems();

});