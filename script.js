
// Get references to DOM elements we'll use throughout the script
var lineItemsBody = document.querySelector('#line-items tbody');
var addItemBtn = document.getElementById('add-item');
var generateBtn = document.getElementById('generate-btn');
var invoiceForm = document.getElementById('invoice-form');
var invoiceOutput = document.getElementById('invoice-output');
var editBtn = document.getElementById('edit-btn');
var printBtn = document.getElementById('print-btn');

// DOM variables for the draft feature buttons (Secret Mission)
var saveDraftBtn = document.getElementById('save-draft');
var loadDraftBtn = document.getElementById('load-draft');
var clearDraftBtn = document.getElementById('clear-draft');

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

// Build a new table row with the same structure as the starter row (FULLY DETAILED)
function createRow() {
    var row = document.createElement('tr');
    row.innerHTML =
        '' +
        '' +
        '' +
        '0.00' +
        'Remove';
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

function generateInvoice() {
    // Populate company, invoice, and client details in the output view
    document.getElementById('output-company-name').textContent =
        document.getElementById('company-name').value || 'Company Name';
    document.getElementById('output-company-address').textContent =
        document.getElementById('company-address').value || '';
    document.getElementById('output-company-email').textContent =
        document.getElementById('company-email').value || '';
    document.getElementById('output-invoice-number').textContent =
        document.getElementById('invoice-number').value || 'INV-001';
    document.getElementById('output-invoice-date').textContent =
        document.getElementById('invoice-date').value || new Date().toLocaleDateString();
    document.getElementById('output-client-name').textContent =
        document.getElementById('client-name').value || 'Client Name';
    document.getElementById('output-client-address').textContent =
        document.getElementById('client-address').value || '';
    document.getElementById('output-client-email').textContent =
        document.getElementById('client-email').value || '';

    // Build output table rows from line items
    var outputItems = document.getElementById('output-items');
    outputItems.innerHTML = '';
    var rows = lineItemsBody.querySelectorAll('tr');
    for (var i = 0; i < rows.length; i++) {
        var description = rows[i].querySelector('.item-description').value;
        var quantity = rows[i].querySelector('.item-quantity').value;
        var price = rows[i].querySelector('.item-price').value;
        var lineTotal = rows[i].querySelector('.item-total').textContent;
        if (description || parseFloat(quantity) > 0) {
            var outputRow = document.createElement('tr');
            outputRow.innerHTML =
                '' + description + '' +
                '' + quantity + '' +
                '' + parseFloat(price).toFixed(2) + '' +
                '' + lineTotal + '';
            outputItems.appendChild(outputRow);
        }
    }

    // Copy totals and switch to the output view
    document.getElementById('output-subtotal').textContent =
        document.getElementById('subtotal').textContent;
    document.getElementById('output-tax').textContent =
        document.getElementById('tax').textContent;
    document.getElementById('output-total').textContent =
        document.getElementById('total').textContent;
    invoiceForm.classList.add('hidden');
    invoiceOutput.classList.remove('hidden');
}

generateBtn.addEventListener('click', generateInvoice);

editBtn.addEventListener('click', function() {
    invoiceOutput.classList.add('hidden');
    invoiceForm.classList.remove('hidden');
});

printBtn.addEventListener('click', function() {
    window.print();
});

// ==========================================
// SECRET MISSION: LOCALSTORAGE DRAFT FUNCTIONS
// ==========================================

function saveDraft() {
    var data = {
        companyName: document.getElementById('company-name').value,
        companyAddress: document.getElementById('company-address').value,
        companyEmail: document.getElementById('company-email').value,
        invoiceNumber: document.getElementById('invoice-number').value,
        invoiceDate: document.getElementById('invoice-date').value,
        clientName: document.getElementById('client-name').value,
        clientAddress: document.getElementById('client-address').value,
        clientEmail: document.getElementById('client-email').value,
        items: []
    };

    var rows = lineItemsBody.querySelectorAll('tr');
    for (var i = 0; i < rows.length; i++) {
        data.items.push({
            description: rows[i].querySelector('.item-description').value,
            quantity: rows[i].querySelector('.item-quantity').value,
            price: rows[i].querySelector('.item-price').value
        });
    }

    localStorage.setItem('invoiceDraft', JSON.stringify(data));
    alert('Draft saved!');
}

function loadDraft() {
    var saved = localStorage.getItem('invoiceDraft');
    if (!saved) {
        alert('No saved draft found.');
        return;
    }

    try {
        var data = JSON.parse(saved);
        document.getElementById('company-name').value = data.companyName || '';
        document.getElementById('company-address').value = data.companyAddress || '';
        document.getElementById('company-email').value = data.companyEmail || '';
        document.getElementById('invoice-number').value = data.invoiceNumber || '';
        document.getElementById('invoice-date').value = data.invoiceDate || '';
        document.getElementById('client-name').value = data.clientName || '';
        document.getElementById('client-address').value = data.clientAddress || '';
        document.getElementById('client-email').value = data.clientEmail || '';

        // Clear existing rows and rebuild from saved data
        lineItemsBody.innerHTML = '';
        for (var i = 0; i < data.items.length; i++) {
            var row = createRow();
            row.querySelector('.item-description').value = data.items[i].description || '';
            row.querySelector('.item-quantity').value = data.items[i].quantity || 0;
            row.querySelector('.item-price').value = data.items[i].price || 0;
            lineItemsBody.appendChild(row);
        }

        calculateTotals();
        alert('Draft loaded!');
    } catch (error) {
        alert('Error loading draft. The saved data may be corrupted.');
        localStorage.removeItem('invoiceDraft');
    }
}

function clearDraft() {
    localStorage.removeItem('invoiceDraft');
    alert('Draft cleared!');
}

// Wire up the draft buttons
saveDraftBtn.addEventListener('click', saveDraft);
loadDraftBtn.addEventListener('click', loadDraft);
clearDraftBtn.addEventListener('click', clearDraft);