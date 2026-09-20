let decisions = [];

async function loadInventory() {
  const body = document.getElementById("inventory-body");

  try {
    body.innerHTML = '<tr><td colspan="5"><div class="empty">Loading inventory...</div></td></tr>';

    const inventoryResponse = await fetch("/api/inventory");

    if (!inventoryResponse.ok) {
      throw new Error("Could not load inventory");
    }

    const inventory = await inventoryResponse.json();

    const agentResponse = await fetch("/api/agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(inventory)
    });

    if (!agentResponse.ok) {
      throw new Error("Could not run Stockholm Agent");
    }

    decisions = await agentResponse.json();

    updateSummary();
    render();
  } catch (error) {
    body.innerHTML = '<tr><td colspan="5"><div class="empty">Could not connect to the inventory backend.</div></td></tr>';
    document.getElementById("agent-summary").textContent = "Backend connection failed.";
    document.getElementById("attention-list").innerHTML =
      '<div class="empty">Start the Flask server and refresh the page.</div>';
    console.error(error);
  }
}

function statusFor(decision) {
  if (decision.action === "OUT_OF_STOCK") {
    return { key: "out", label: "Out of stock" };
  }

  if (decision.action === "REORDER") {
    return { key: "reorder", label: "Reorder" };
  }

  return { key: "healthy", label: "Healthy" };
}

function updateSummary() {
  const lowStock = decisions.filter(d => d.action === "REORDER").length;
  const outOfStock = decisions.filter(d => d.action === "OUT_OF_STOCK").length;
  const reorderValue = decisions.reduce(
    (total, d) => total + d.reorder_quantity,
    0
  );

  document.getElementById("products-count").textContent = decisions.length;
  document.getElementById("low-stock-count").textContent = lowStock;
  document.getElementById("out-stock-count").textContent = outOfStock;
  document.getElementById("reorder-value").textContent = reorderValue;
}

function render() {
  const query = document.getElementById("search").value.toLowerCase().trim();
  const filter = document.getElementById("filter").value;
  const body = document.getElementById("inventory-body");

  const rows = decisions.filter(decision => {
    const status = statusFor(decision);
    const matchesSearch = decision.product.toLowerCase().includes(query);
    const matchesFilter = filter === "all" || status.key === filter;

    return matchesSearch && matchesFilter;
  });

  body.innerHTML = rows.length
    ? rows.map(decision => {
        const status = statusFor(decision);

        return `
          <tr>
            <td><span class="product-name">${decision.product}</span></td>
            <td><span class="stock-value">${decision.quantity}</span> units</td>
            <td><span class="velocity">${decision.sales_velocity.toFixed(2)}/day</span></td>
            <td><span class="lead">${decision.lead_time} days</span></td>
            <td>
              <span class="status ${status.key}">
                <i></i>${status.label}
              </span>
            </td>
          </tr>
        `;
      }).join("")
    : '<tr><td colspan="5"><div class="empty">No products match your search.</div></td></tr>';

  renderAttention();
}

function renderAttention() {
  const attention = decisions.filter(
    decision => decision.action !== "NO_ACTION"
  );

  document.getElementById("agent-summary").textContent =
    attention.length
      ? `${attention.length} product${attention.length > 1 ? "s need" : " needs"} your attention.`
      : "Everything looks healthy right now.";

  document.getElementById("attention-list").innerHTML = attention.length
    ? attention.map(decision => {
        const status = statusFor(decision);

        return `
          <div class="attention-item">
            <div class="attention-item-top">
              <strong>${decision.product}</strong>
              <span class="status ${status.key}"><i></i>${decision.urgency}</span>
            </div>

            <div class="attention-action">
              ${status.label} ${decision.reorder_quantity} units
            </div>

            <div class="attention-detail">
              ${decision.quantity} in stock ·
              ${decision.pending_order} pending ·
              ${decision.lead_time} day lead time
            </div>

            <div class="attention-detail">
              Location: ${decision.location}
            </div>
          </div>
        `;
      }).join("")
    : '<div class="empty">No action required.</div>';
}

document.getElementById("search").addEventListener("input", render);
document.getElementById("filter").addEventListener("change", render);

document.getElementById("add-product").addEventListener("click", () => {
  alert("Product creation will be connected next.");
});

loadInventory();
