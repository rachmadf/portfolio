/* ==========================================================
   MyFinance - expense.js
   Revised with additional validation
========================================================== */
"use strict";

let currentEditingRow = null;
let historyModal = null;
let availableItemTable;
let currentPlan = [];


// ========================================================
// FOR EXPENSE PLAN FEATURE
// ========================================================
// Initialize DataTable
$(document).ready(function () {
    availableItemTable = $("#tblAvailableItems").DataTable({
        responsive: true,
        paging: true,
        pageLength: 10,
        searching: false,
        ordering: true,
        info: false,
        autoWidth: false,
        // columnDefs: [

        //         {
        //             targets: 1,
        //             width: "50px"
        //         }

        //     ],
        columns: [
            {
                data: null,
                render: function (data, type, row) {
                    return `
                        <div class="py-1">
                            <div class="fw-semibold text-dark">
                                ${row.item_name}
                            </div>
                            <small class="text-muted">
                                ${formatCurrency(row.unit_price)}
                            </small>
                        </div>
                    `;
                }
            },

            {
                data: null,
                className: "text-center",
                orderable: false,
                searchable: false,
                // width: "50px",
                render: function (data, type, row) {
                    return `
                        <button
                            type="button" 
                            class="btn btn-primary btnAddItem"
                            data-item="${row.item_name}"
                            data-category-id="${row.category_id}"
                            data-store-id="${row.store_id}"
                            data-price="${row.unit_price}"
                            title="Add to Current Plan">

                            <i class="bi bi-plus"></i>

                        </button>
                    `;

                }
            }

        ]

    });

    loadAvailableItems();

});

// ---------------------------------------------
// Currency Formatter
// ---------------------------------------------
function formatCurrency(value) {

    return "Rp " + Number(value).toLocaleString("id-ID");

}

// ---------------------------------------------
// load available item from route
// ---------------------------------------------
function loadAvailableItems() {

    const category_id = $("#category_id").val();
    const store_id = $("#store_id").val();
    const keyword = $("#txtSearchItem").val();

    const params = {};

    if(category_id)
        params.category_id = category_id;

    if(store_id)
        params.store_id = store_id;

    if(keyword)
        params.keyword = keyword;

    $.ajax({
        url: AVAILABLE_ITEMS_URL,
        method: "GET",
        data: params,
        success: function(response){

            renderAvailableItems(response);

            $("#availableItemCount")
                .text(response.length + " Items");
        }
    });
}

// ---------------------------------------------
// show available item into card
// ---------------------------------------------
function renderAvailableItems(items){
    const list = $("#availableItemList");
    list.empty();
    if(items.length === 0){
        list.html(`
            <div class="text-center p-4 text-muted">
                <i class="bi bi-inbox fs-2"></i>
                <div>No items found</div>
            </div>
        `);
        return;

    }

    items.forEach(function(item){
        list.append(`
            <div
                class="list-group-item">
                <div class="d-flex justify-content-between">
                    <div class="flex-grow-1">
                        <div class="fw-semibold">
                            ${item.item_name}
                        </div>
                        <small class="text-success fw-semibold">
                            ${formatCurrency(item.unit_price)}
                        </small>

                        <br>
                        <small class="text-muted">
                            Last purchase :
                            ${item.last_purchase_date}
                        </small>

                        <div class="ms-3 text-end">
                            <a
                                href="#"
                                class="link-success fw-semibold text-decoration-none btnAddItem"
                                data-item-name="${item.item_name}"
                                data-category-id="${item.category_id}"
                                data-category-name="${item.category_name}"

                                data-store-id="${item.store_id}"
                                data-store-name="${item.store_name}"

                                data-unit-price="${item.unit_price}"

                            >
                                 Add <i class="bi bi-arrow-right-short"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `);

    });

}

let searchTimer;
$("#txtSearchItem").on("keyup", function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () {
        loadAvailableItems();

    }, 300);

});


// reset button
$("#btnResetFilter").on("click", function () {
    $("#category_id").val("");
    $("#category_name").val("");
    $("#store_id").val("");
    $("#store_name").val("");
    $("#txtSearchItem").val("");
    loadAvailableItems();
});

// ---------------------------------------------
// Button Add Item to Current Plan Listener
// ---------------------------------------------
$(document).on("click", ".btnAddItem", function (e) {
    e.preventDefault();
    const item = {
        item_name: $(this).data("item-name"),
        category_id: $(this).data("category-id"),
        category_name: $(this).data("category-name"),
        store_id: $(this).data("store-id"),
        store_name: $(this).data("store-name"),
        unit_price: parseFloat($(this).data("unit-price")),
        quantity: 1
    };

    console.log(item);
    addItemToCurrentPlan(item);

});

// ---------------------------------------------
// Add Item to Current Plan
//---------------------------------------------
function addItemToCurrentPlan(item){

    const existing = currentPlan.find(planItem =>

        planItem.item_name === item.item_name &&
        planItem.store_id === item.store_id &&
        planItem.category_id === item.category_id

    );

    if(existing){

        existing.quantity++;

    }
    else{

        currentPlan.push(item);

    }

    renderCurrentPlan();

}

function renderCurrentPlan(){

    // console.table(currentPlan);
    console.log($("#currentPlanList").length);
    const list = $("#currentPlanList");

    list.empty();

    currentPlan.forEach(function(item){

        list.append(`

            <div class="list-group-item">

                <div class="d-flex justify-content-between align-items-start">

                    <div class="flex-grow-1">

                        <div class="fw-semibold">

                            ${item.item_name}

                        </div>


                        <div class="d-flex align-items-center gap-1 mt-2">

                            <button
                                type="button"
                                class="btn btn-outline-secondary btn-sm qty-btn btnDecreaseQty"
                                data-item-name="${item.item_name}"
                                data-category-id="${item.category_id}"
                                data-store-id="${item.store_id}">

                                <i class="bi bi-dash"></i>

                            </button>

                            <span class="qty-value">

                                ${item.quantity}

                            </span>

                            <button
                                type="button"
                                class="btn btn-outline-primary btn-sm qty-btn btnIncreaseQty"
                                data-item-name="${item.item_name}"
                                data-category-id="${item.category_id}"
                                data-store-id="${item.store_id}">

                                <i class="bi bi-plus"></i>

                            </button>

                        </div>

                        <br>

                        <small class="text-success fw-semibold">

                            ${formatCurrency(item.unit_price)}

                        </small>

                    </div>

                    <div class="text-end">

                        <small class="text-muted">

                            ${formatCurrency(item.quantity * item.unit_price)}

                        </small>

                    </div>

                </div>

            </div>

            `);

    });

    updateEstimatedTotal();


}

// --------------------------------------------------
// button increase quantity in current plan card
// --------------------------------------------------

$(document).on("click", ".btnIncreaseQty", function () {

    const existing = currentPlan.find(item =>

        item.item_name === $(this).data("item-name") &&
        item.category_id === $(this).data("category-id") &&
        item.store_id === $(this).data("store-id")

    );

    if(existing){

        existing.quantity++;

        renderCurrentPlan();

    }

});

// --------------------------------------------------
// button decrease quantity in current plan card
// --------------------------------------------------

$(document).on("click", ".btnDecreaseQty", function () {

    const existing = currentPlan.find(item =>

        item.item_name === $(this).data("item-name") &&
        item.category_id === $(this).data("category-id") &&
        item.store_id === $(this).data("store-id")

    );

    if(!existing)
        return;

    existing.quantity--;

    if(existing.quantity <= 0){

        currentPlan = currentPlan.filter(item =>

            !(

                item.item_name === existing.item_name &&
                item.category_id === existing.category_id &&
                item.store_id === existing.store_id

            )

        );

    }

    renderCurrentPlan();

});

// ----------------------------------------------
// 
// ----------------------------------------------

function updateEstimatedTotal(){

    let total = 0;

    currentPlan.forEach(function(item){

        total += item.quantity * item.unit_price;

    });

    $("#estimatedTotal").text(
        formatCurrency(total)
    );

}


// ===================================================
// FOR EXPENSE REPORT FEATURE
// ===================================================
const expenseTableBody = document.getElementById("expenseItems");
const btnAddItem = document.getElementById("btnAddItem");
const btnSave = document.getElementById("btnSave");
const btnReset = document.getElementById("btnReset");
const discountInput = document.getElementById("discount");
const totalItemsElement = document.getElementById("totalItems");
const grandTotalElement = document.getElementById("grandTotal");
const hiddenExpenseDetails = document.getElementById("expense_details");

function formatCurrency(v){
    return Number(v || 0).toLocaleString("id-ID", {
        minimumFractionDigits:2,
        maximumFractionDigits:2
    });
}

function categoryOptions(){
    let html = '<option value="">Select Category</option>';
    categories.forEach(c=>{
        html += `<option value="${c.id}">${c.name}</option>`;
    });
    return html;
}

function addRow_inTheEnd(){
    expenseTableBody.insertAdjacentHTML("afterbegin", `
    <tr>
        <td><select class="form-select category">${categoryOptions()}</select></td>
        <td><input type="text" class="form-control item-name"></td>
        <td><input type="number" class="form-control qty text-end" value="1" min="1"></td>
        <td><input type="number" class="form-control unit-price text-end" value="0" min="0" step="100"></td>
        <td><input type="text" class="form-control subtotal text-end" value="0.00" readonly></td>
        <td class="text-center">
            <button type="button" class="btn btn-sm btn-outline-danger remove-row">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    </tr>`);

    bindRow(expenseTableBody.firstElementChild);
    updateSummary();
}

function addRow(){

    expenseTableBody.insertAdjacentHTML("afterbegin", `
    <tr>
        <td>
            <select class="form-select category">
                ${categoryOptions()}
            </select>
        </td>

        <td>
            <div class="d-flex align-items-center gap-2">

                <input
                    type="text"
                    class="form-control item-name">

                <button
                    type="button"
                    class="btn btn-link btn-md history-item p-0">

                    <i class="bi bi-bag-plus-fill"></i>

                </button>

            </div>
        </td>

        <td>
            <input type="number"
                   class="form-control qty text-end"
                   value="1"
                   min="1">
        </td>

        <td>
            <input type="number"
                   class="form-control unit-price text-end"
                   value="0"
                   min="0"
                   step="100.0">
        </td>

        <td>
            <input type="text"
                   class="form-control subtotal text-end"
                   value="0.00"
                   readonly>
        </td>

        <td class="text-center">
            <button type="button"
                    class="btn btn-sm btn-outline-danger remove-row">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    </tr>`);

    bindRow(expenseTableBody.firstElementChild);

    updateSummary();
}

function bindRow(row){
    row.querySelector(".qty").addEventListener("input",()=>calculateRow(row));
    row.querySelector(".unit-price").addEventListener("input",()=>calculateRow(row));
    row.querySelector(".remove-row").addEventListener("click",()=>{
        if(expenseTableBody.rows.length===1){
            alert("At least one item is required.");
            return;
        }
        row.remove();
        updateSummary();
    });

    row.querySelector(".history-item")
    .addEventListener("click", () => {

        openHistoryModal(row);


    });

    calculateRow(row);

}

function calculateRow(row){
    const qty = Number(row.querySelector(".qty").value || 0);
    const price = Number(row.querySelector(".unit-price").value || 0);
    row.querySelector(".subtotal").value = formatCurrency(qty * price);
    updateSummary();
}

function serializeItems(){
    const data=[];
    let subtotal=0;

    [...expenseTableBody.rows].forEach(row=>{
        const qty = Number(row.querySelector(".qty").value || 0);
        const unitPrice = Number(row.querySelector(".unit-price").value || 0);
        const lineSubtotal = qty * unitPrice;

        subtotal += lineSubtotal;

        data.push({
            category_id: row.querySelector(".category").value,
            item_name: row.querySelector(".item-name").value.trim(),
            quantity: qty,
            unit_price: unitPrice,
            subtotal: lineSubtotal
        });
    });

    hiddenExpenseDetails.value = JSON.stringify(data);
    return subtotal;
}

function updateSummary(){
    const subtotal = serializeItems();

    const discount = Math.max(
        0,
        Number(discountInput.value || 0)
    );

    discountInput.value = discount;

    const grand = Math.max(0, subtotal - discount);

    totalItemsElement.value = expenseTableBody.rows.length;
    grandTotalElement.value = formatCurrency(grand);
}

function validateForm(){

    if(document.getElementById("expense_date").value===""){
        alert("Transaction date is required.");
        return false;
    }

    if(document.getElementById("store_id").value===""){
        alert("Please select a store.");
        return false;
    }

    if(document.getElementById("payment_method_id").value===""){
        alert("Please select a payment method.");
        return false;
    }

    for(const row of expenseTableBody.rows){

        const category = row.querySelector(".category").value;
        const itemName = row.querySelector(".item-name").value.trim();
        const quantity = Number(row.querySelector(".qty").value || 0);
        const unitPrice = Number(row.querySelector(".unit-price").value || 0);

        if(!category){
            alert("Please select a category.");
            row.querySelector(".category").focus();
            return false;
        }

        if(itemName===""){
            alert("Item name is required.");
            row.querySelector(".item-name").focus();
            return false;
        }

        if(quantity<=0){
            alert("Quantity must be greater than zero.");
            row.querySelector(".qty").focus();
            return false;
        }

        if(unitPrice<0){
            alert("Unit price cannot be negative.");
            row.querySelector(".unit-price").focus();
            return false;
        }
    }

    return true;
}

document.addEventListener("DOMContentLoaded",()=>{

    historyModal = new bootstrap.Modal(
        document.getElementById("itemHistoryModal")
    );

    addRow();

    btnAddItem.addEventListener("click", addRow);

    discountInput.addEventListener("input", updateSummary);

    btnReset.addEventListener("click",()=>{
        setTimeout(()=>{
            expenseTableBody.innerHTML="";
            discountInput.value=0;
            addRow();
        },10);
    });

    btnSave.addEventListener("click",()=>{
        new bootstrap.Modal(
            document.getElementById("saveExpenseModal")
        ).show();
    });

    document.getElementById("confirmSave").addEventListener("click",()=>{

        if(!validateForm()){
            btnSave.disabled = false;
            return;
        }

        serializeItems();

        const modal = bootstrap.Modal.getInstance(
            document.getElementById("saveExpenseModal")
        );

        if(modal){
            modal.hide();
        }

        btnSave.disabled = true;
        btnSave.innerHTML = '<i class="bi bi-hourglass-split"></i> Saving...';

        document.getElementById("expenseForm").submit();

    });

    document.getElementById("expenseForm").addEventListener("submit", serializeItems);

});

// ===========================================================
// Open Modal to Add Existing Item into new expense item entry
// ===========================================================
async function openHistoryModal(row){

    currentEditingRow = row;

    const categorySelect = row.querySelector(".category");

    const categoryId = categorySelect.value;

    if(categoryId === ""){

        alert("Please select a category first.");

        categorySelect.focus();

        return;

    }

    document.getElementById("historyCategoryName").value =
        categorySelect.options[
            categorySelect.selectedIndex
        ].text;

    const items = await loadItemHistory(categoryId);

    populateHistoryTable(items);

    // console.log(items);

    historyModal.show();

    document
    .getElementById("historyTableBody")
    .addEventListener("click", function(e){

        const button = e.target.closest(".select-history");

        if(!button){
            return;
        }

        const itemName = button.dataset.item;
        const lastPrice = Number(button.dataset.price);

        currentEditingRow.querySelector(".item-name").value = itemName;
        currentEditingRow.querySelector(".unit-price").value = lastPrice;

        calculateRow(currentEditingRow);

        historyModal.hide();

    });

}

async function loadItemHistory(categoryId){

    try{

        const response = await fetch(
            `/expense/api/items/${categoryId}`
        );

        if(!response.ok){
            throw new Error("Unable to retrieve item history.");
        }

        const result = await response.json();

        return result.data;

    }
    catch(error){

        console.error(error);

        alert(error.message);

        return [];
    }

}

function populateHistoryTable(items){

    const tbody = document.getElementById("historyTableBody");

    console.log(document.getElementById("historyTableBody"));

    tbody.innerHTML = "";

    if(items.length === 0){

        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted">
                    No previous items found.
                </td>
            </tr>
        `;

        return;
    }

    items.forEach(item=>{

        tbody.insertAdjacentHTML("beforeend",`

            <tr>

                <td>${item.item_name}</td>

                <td class="text-end">
                    ${formatCurrency(item.last_price)}
                </td>

                <td class="text-center">
                    ${item.usage_count}
                </td>

                <td class="text-center">

                    <button
                        type="button"
                        class="btn btn-sm btn-success select-history"
                        data-item="${item.item_name}"
                        data-price="${item.last_price}">

                        <i class="bi bi-plus-circle"></i> Add

                    </button>

                </td>

            </tr>

        `);

    });

}