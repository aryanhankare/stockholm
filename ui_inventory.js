const inventory = [
  { name: "Rice", quantity: 10, sold: 20, days: 7, lead_time: 7, pending_order: 5 },
  { name: "Cooking Oil", quantity: 25, sold: 8, days: 7, lead_time: 3, pending_order: 0 },
  { name: "Sugar", quantity: 0, sold: 15, days: 7, lead_time: 5, pending_order: 10 },
  { name: "Wheat", quantity: 12, sold: 5, days: 7, lead_time: 2, pending_order: 15 },
  { name: "Flour", quantity: 18, sold: 12, days: 7, lead_time: 4, pending_order: 0 },
  { name: "Tea", quantity: 21, sold: 7, days: 7, lead_time: 3, pending_order: 5 }
];

function getDecision(product) {
  const velocity = product.sold / product.days;
  const target = Math.max(25, Math.floor(velocity * 7));
  const available = product.quantity + product.pending_order;

  if (product.quantity <= 0) return { status: "out", label: "Out of stock", action: "Reorder", urgency: "High", reorder: target };
  if (available < target) {
    const urgency = product.quantity <= 10 || product.lead_time >= 7 ? "High" : "Medium";
    return { status: "reorder", label: "Reorder", action: "Reorder", urgency, reorder: target - available };
  }
  return { status: "healthy", label: "Healthy", action: "No action", urgency: "Low", reorder: 0 };
}

function render() {
  const query = document.getElementById("search").value.toLowerCase().trim();
  const filter = document.getElementById("filter").value;
  const body = document.getElementById("inventory-body");

  const rows = inventory.filter(product => {
    const decision = getDecision(product);
    const matchesSearch = product.name.toLowerCase().includes(query);
    const matchesFilter = filter === "all" || decision.status === filter;
    return matchesSearch && matchesFilter;
  });

  body.innerHTML = rows.length ? rows.map(product => {
    const decision = getDecision(product);
    const velocity = (product.sold / product.days).toFixed(2);

    return `
      <tr>
        <td><span class="product-name">${product.name}</span></td>
        <td><span class="stock-value">${product.quantity}</span> units</td>
        <td><span class="velocity">${velocity}/day</span></td>
        <td><span class="lead">${product.lead_time} days</span></td>
        <td>
          <span class="status ${decision.status}">
            <i></i>${decision.label}
          </span>
        </td>
      </tr>
    `;
  }).join("") : '<tr><td colspan="5"><div class="empty">No products match your search.</div></td></tr>';

  renderAttention();
}

function renderAttention() {
  const attention = inventory
    .map(product => ({ product, decision: getDecision(product) }))
    .filter(item => item.decision.status !== "healthy");

  document.getElementById("agent-summary").textContent =
    attention.length
      ? `${attention.length} product${attention.length > 1 ? "s need" : " needs"} your attention.`
      : "Everything looks healthy right now.";

  document.getElementById("attention-list").innerHTML = attention.length
    ? attention.map(({ product, decision }) => `
      <div class="attention-item">
        <div class="attention-item-top">
          <strong>${product.name}</strong>
          <span class="status ${decision.status}"><i></i>${decision.urgency}</span>
        </div>
        <div class="attention-action">${decision.action} ${decision.reorder} units</div>
        <div class="attention-detail">
          ${product.quantity} in stock · ${product.pending_order} pending · ${product.lead_time} day lead time
        </div>
      </div>
    `).join("")
    : '<div class="empty">No action required.</div>';
}

document.getElementById("search").addEventListener("input", render);
document.getElementById("filter").addEventListener("change", render);
document.getElementById("add-product").addEventListener("click", () => {
  alert("Product creation will be connected to the inventory backend next.");
});

render();
