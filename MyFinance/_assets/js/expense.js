/* ==========================================================
   MyFinance - expense.js
   Revised with additional validation
========================================================== */
"use strict";

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

function addRow(){
    expenseTableBody.insertAdjacentHTML("beforeend", `
    <tr>
        <td><select class="form-select category">${categoryOptions()}</select></td>
        <td><input type="text" class="form-control item-name"></td>
        <td><input type="number" class="form-control qty text-end" value="1" min="1"></td>
        <td><input type="number" class="form-control unit-price text-end" value="0" min="0" step="0.01"></td>
        <td><input type="text" class="form-control subtotal text-end" value="0.00" readonly></td>
        <td class="text-center">
            <button type="button" class="btn btn-sm btn-outline-danger remove-row">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    </tr>`);

    bindRow(expenseTableBody.lastElementChild);
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

function validateForm() {

    const expenseDate = document.getElementById("expense_date");
    const store = document.getElementById("store_id");
    const payment = document.getElementById("payment_method_id");

    console.log({
        expenseDate,
        store,
        payment
    });

    if (!expenseDate) {
        alert("expense_date not found");
        return false;
    }

    if (!store) {
        alert("store_id not found");
        return false;
    }

    if (!payment) {
        alert("payment_method_id not found");
        return false;
    }

    console.log("expense_date value =", expenseDate.value);
    console.log("store value =", store.value);
    console.log("payment value =", payment.value);

    return false;
}

document.addEventListener("DOMContentLoaded",()=>{

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