// Get references to DOM elements we'll use throughout the script
var lineItemsBody = document.querySelector('#line-items tbody');
var addItemBtn = document.getElementById('add-item');
var generateBtn = document.getElementById('generate-btn');
var invoiceForm = document.getElementById('invoice-form');
var invoiceOutput = document.getElementById('invoice-output');
var editBtn = document.getElementById('edit-btn');
var printBtn = document.getElementById('print-btn');

// Loop through all table rows, calculate each line total, and update the summary
function calculateTotals() {
    var rows = lineItemsBody.querySelectorAll('tr');
    var subtotal = 0;

    for (var i = 0; i < rows.length; i++) {
        var quantity = parseFloat(rows[i].querySelector('.item-quantity').value) || 0;
        var price = parseFloat(rows[i].querySelector('.item-price').value) || 0;
        var lineTotal = quantity * price;
        rows[i].querySelector('.item-total').textContent = lineTotal.toFixed(2);
        subtotal += lineTotal;
    }

    var tax = subtotal * 0.10;
    var total = subtotal + tax;

    document.getElementById('subtotal').textContent = subtotal.toFixed(2);
    document.getElementById('tax').textContent = tax.toFixed(2);
    document.getElementById('total').textContent = total.toFixed(2);
}

// Build a new table row with the same structure as the starter row
function createRow() {
    var row = document.createElement('tr');
    row.innerHTML =
        '<td><input type="text" class="item-description" placeholder="Item description"></td>' +
        '<td><input type="number" class="item-quantity" min="0" value="0"></td>' +
        '<td><input type="number" class="item-price" min="0" step="0.01" value="0"></td>' +
        '<td class="item-total">0.00</td>' +
        '<td><button class="remove-row" type="button">Remove</button></td>';
    return row;
}

// Remove a row when its Remove button is clicked (keep at least one row)
function handleRemoveRow(event) {
    if (event.target.classList.contains('remove-row')) {
        var rows = lineItemsBody.querySelectorAll('tr');
        if (rows.length > 1) {
            event.target.closest('tr').remove();
            calculateTotals();
        }
    }
}

// Recalculate whenever a quantity or price input changes
lineItemsBody.addEventListener('input', function(event) {
    if (event.target.classList.contains('item-quantity') ||
        event.target.classList.contains('item-price')) {
        calculateTotals();
    }
});

// Wire up the Add Item button to insert a new row
addItemBtn.addEventListener('click', function() {
    var newRow = createRow();
    lineItemsBody.appendChild(newRow);
});

// Delegate click events on the table body to handle Remove buttons
lineItemsBody.addEventListener('click', handleRemoveRow);