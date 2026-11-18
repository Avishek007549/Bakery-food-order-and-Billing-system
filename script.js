const menu = [
  // 1–10: Nepali meals and traditional food
  {
    id: "dal-bhat",
    name: "Dal Bhat Tarkari",
    price: 300,
    emoji: "🍛",
    description: "Traditional Nepali rice, lentils and vegetables.",
    background: "#f1e2d3"
  },
  {
    id: "chicken-dal-bhat",
    name: "Chicken Dal Bhat",
    price: 450,
    emoji: "🍗",
    description: "Nepali rice meal served with chicken curry.",
    background: "#f3dfb9"
  },
  {
    id: "veg-thali",
    name: "Veg Thali",
    price: 300,
    emoji: "🥗",
    description: "Rice, lentils, seasonal vegetables and pickle.",
    background: "#e8e6d3"
  },
  {
    id: "chicken-thali",
    name: "Chicken Thali",
    price: 350,
    emoji: "🍗",
    description: "A filling meal with chicken curry and rice.",
    background: "#f5e1cf"
  },
  {
    id: "thakali-thali",
    name: "Thakali Khana Set",
    price: 450,
    emoji: "🍱",
    description: "A classic Thakali-style meal with accompaniments.",
    background: "#f2e7cd"
  },
  {
    id: "mutton-thali",
    name: "Mutton Thali",
    price: 550,
    emoji: "🍖",
    description: "Rice, mutton curry and traditional sides.",
    background: "#f3dfb9"
  },
  {
    id: "dhido",
    name: "Dhido Set",
    price: 350,
    emoji: "🥣",
    description: "Traditional dhido with curry and vegetables.",
    background: "#e8e6d3"
  },
  {
    id: "gundruk",
    name: "Gundruk Soup",
    price: 120,
    emoji: "🥣",
    description: "Traditional fermented leafy-green soup.",
    background: "#dce9d5"
  },
  {
    id: "sel-roti",
    name: "Sel Roti",
    price: 40,
    emoji: "🍩",
    description: "Traditional homemade Nepali rice bread.",
    background: "#f5e1cf"
  },
  {
    id: "yomari",
    name: "Yomari",
    price: 80,
    emoji: "🥟",
    description: "Newari rice-flour dumpling with sweet filling.",
    background: "#f2e7cd"
  },

  // 11–20: Momo and popular snacks
  {
    id: "veg-momo",
    name: "Veg Momo",
    price: 100,
    emoji: "🥟",
    description: "Steamed vegetable dumplings with achar.",
    background: "#e8e6d3"
  },
  {
    id: "chicken-momo",
    name: "Chicken Momo",
    price: 140,
    emoji: "🥟",
    description: "Juicy chicken dumplings with spicy tomato achar.",
    background: "#f1e2d3"
  },
  {
    id: "buff-momo",
    name: "Buff Momo",
    price: 150,
    emoji: "🥟",
    description: "Popular buffalo-meat dumplings with dipping sauce.",
    background: "#f3dfb9"
  },
  {
    id: "jhol-momo",
    name: "Jhol Momo",
    price: 180,
    emoji: "🍲",
    description: "Momo served in flavorful sesame-tomato broth.",
    background: "#f5e1cf"
  },
  {
    id: "kothe-momo",
    name: "Kothe Momo",
    price: 170,
    emoji: "🥟",
    description: "Pan-fried dumplings with a crispy base.",
    background: "#f2e7cd"
  },
  {
    id: "chowmein",
    name: "Veg Chowmein",
    price: 120,
    emoji: "🍜",
    description: "Stir-fried noodles with fresh vegetables.",
    background: "#e8e6d3"
  },
  {
    id: "chicken-chowmein",
    name: "Chicken Chowmein",
    price: 170,
    emoji: "🍜",
    description: "Noodles tossed with chicken and vegetables.",
    background: "#f3dfb9"
  },
  {
    id: "thukpa",
    name: "Veg Thukpa",
    price: 150,
    emoji: "🍜",
    description: "Warm Himalayan noodle soup with vegetables.",
    background: "#dce9d5"
  },
  {
    id: "chicken-thukpa",
    name: "Chicken Thukpa",
    price: 200,
    emoji: "🍜",
    description: "Comforting noodle soup with chicken.",
    background: "#f1e2d3"
  },
  {
    id: "samosa",
    name: "Samosa",
    price: 30,
    emoji: "🥟",
    description: "Crispy pastry filled with spiced potatoes.",
    background: "#f5e1cf"
  },

  // 21–30: Newari, Madhesi and Indian-influenced favorites
  {
    id: "bara",
    name: "Newari Bara",
    price: 80,
    emoji: "🥞",
    description: "Traditional savory lentil pancake.",
    background: "#f2e7cd"
  },
  {
    id: "chatamari",
    name: "Chatamari",
    price: 150,
    emoji: "🫓",
    description: "Newari rice-flour crepe with savory toppings.",
    background: "#e8e6d3"
  },
  {
    id: "choila",
    name: "Buff Choila",
    price: 250,
    emoji: "🍖",
    description: "Spiced Newari-style grilled buffalo meat.",
    background: "#f3dfb9"
  },
  {
    id: "aloo-tama",
    name: "Aloo Tama",
    price: 150,
    emoji: "🥘",
    description: "Traditional curry with potato and bamboo shoots.",
    background: "#dce9d5"
  },
  {
    id: "puri-tarkari",
    name: "Puri Tarkari",
    price: 100,
    emoji: "🥘",
    description: "Fried bread served with vegetable curry.",
    background: "#f5e1cf"
  },
  {
    id: "chana-chat",
    name: "Chana Chat",
    price: 80,
    emoji: "🥗",
    description: "Tangy chickpeas mixed with spices and herbs.",
    background: "#f2e7cd"
  },
  {
    id: "pani-puri",
    name: "Pani Puri",
    price: 80,
    emoji: "🥙",
    description: "Crispy puris with spicy tangy water.",
    background: "#e8e6d3"
  },
  {
    id: "chatpate",
    name: "Chatpate",
    price: 60,
    emoji: "🥗",
    description: "Spicy puffed-rice snack with crunchy toppings.",
    background: "#f3dfb9"
  },
  {
    id: "litti-chokha",
    name: "Litti Chokha",
    price: 180,
    emoji: "🍽️",
    description: "Madhesi and Bihari-style litti with chokha.",
    background: "#f1e2d3"
  },
  {
    id: "maithili-thali",
    name: "Maithili Thali",
    price: 999,
    emoji: "🍱",
    description: "Special regional feast with selected traditional sides.",
    background: "#f5e1cf"
  },

  // 31–40: Fast food and bakery favorites
  {
    id: "veg-burger",
    name: "Veg Burger",
    price: 120,
    emoji: "🍔",
    description: "Vegetable patty with fresh salad and sauce.",
    background: "#f3dfb9"
  },
  {
    id: "chicken-burger",
    name: "Chicken Burger",
    price: 180,
    emoji: "🍔",
    description: "Chicken burger with lettuce and house sauce.",
    background: "#f1e2d3"
  },
  {
    id: "pizza",
    name: "Veg Pizza",
    price: 250,
    emoji: "🍕",
    description: "Cheesy pizza topped with colorful vegetables.",
    background: "#f5e1cf"
  },
  {
    id: "chicken-pizza",
    name: "Chicken Pizza",
    price: 350,
    emoji: "🍕",
    description: "Pizza with chicken, cheese and savory toppings.",
    background: "#f3dfb9"
  },
  {
    id: "french-fries",
    name: "French Fries",
    price: 100,
    emoji: "🍟",
    description: "Golden fries served with tomato ketchup.",
    background: "#f2e7cd"
  },
  {
    id: "chicken-fried-rice",
    name: "Chicken Fried Rice",
    price: 180,
    emoji: "🍚",
    description: "Fried rice with chicken, egg and vegetables.",
    background: "#e8e6d3"
  },
  {
    id: "veg-fried-rice",
    name: "Veg Fried Rice",
    price: 130,
    emoji: "🍚",
    description: "Wok-fried rice with fresh vegetables.",
    background: "#dce9d5"
  },
  {
    id: "chicken-roll",
    name: "Chicken Roll",
    price: 150,
    emoji: "🌯",
    description: "Chicken and vegetables wrapped in flatbread.",
    background: "#f1e2d3"
  },
  {
    id: "donut",
    name: "Donut",
    price: 70,
    emoji: "🍩",
    description: "Soft bakery donut with a sweet finish.",
    background: "#f5e1cf"
  },
  {
    id: "cake-slice",
    name: "Cake Slice",
    price: 120,
    emoji: "🍰",
    description: "A soft, sweet slice of bakery cake.",
    background: "#f2e7cd"
  },

  // 41–50: Breakfast, drinks and desserts
  {
    id: "milk-tea",
    name: "Milk Tea",
    price: 30,
    emoji: "",
    description: "Classic Nepali chiya brewed with milk and spices.",
    background: "#f2e7cd"
  },
  {
    id: "black-tea",
    name: "Black Tea",
    price: 20,
    emoji: "🍵",
    description: "Freshly brewed black tea.",
    background: "#dce9d5"
  },
  {
    id: "coffee",
    name: "Coffee",
    price: 80,
    emoji: "☕",
    description: "Hot, aromatic coffee for your daily break.",
    background: "#f1e2d3"
  },
  {
    id: "cold-coffee",
    name: "Cold Coffee",
    price: 150,
    emoji: "☕",
    description: "Chilled creamy coffee served over ice.",
    background: "#f3dfb9"
  },
  {
    id: "lassi",
    name: "Lassi",
    price: 100,
    emoji: "🥛",
    description: "Refreshing yogurt-based traditional drink.",
    background: "#f2e7cd"
  },
  {
    id: "lemon-soda",
    name: "Lemon Soda",
    price: 80,
    emoji: "🍋",
    description: "Refreshing lemon drink with sparkling soda.",
    background: "#dce9d5"
  },
  {
    id: "coke",
    name: "Coca-Cola",
    price: 60,
    emoji: "🥤",
    description: "Chilled cola soft drink.",
    background: "#f5e1cf"
  },
  {
    id: "sprite",
    name: "Sprite",
    price: 60,
    emoji: "🥤",
    description: "Lemon-lime flavored soft drink.",
    background: "#58e00e"
  },
  {
    id: "ice-cream",
    name: "Ice Cream",
    price: 100,
    emoji: "🍨",
    description: "A cool and creamy dessert.",
    background: "#d61b63"
  },
  {
    id: "rasbari",
    name: "Rasbari",
    price: 80,
    emoji: "🍮",
    description: "Traditional sweet dumpling soaked in syrup.",
    background: "#d61b63"
  }
];

const menuGrid = document.getElementById("menuGrid");
const menuCount = document.getElementById("menuCount");
const cartItems = document.getElementById("cartItems");
const cartCount = document.getElementById("cartCount");
const clearCartBtn = document.getElementById("clearCartBtn");
const subtotalEl = document.getElementById("subtotal");
const discountRow = document.getElementById("discountRow");
const discountEl = document.getElementById("discount");
const totalEl = document.getElementById("total");
const formMessage = document.getElementById("formMessage");
const customerNameInput = document.getElementById("customerName");
const confirmationSection = document.getElementById("confirmationSection");
const confirmationEyebrow = confirmationSection.querySelector(".eyebrow");
const confirmationTitle = confirmationSection.querySelector("h2");
const confirmationMessage = confirmationSection.querySelector(".confirmation-heading p");
const receiptEl = document.getElementById("receipt");
const yearEl = document.getElementById("year");
const paymentCheckoutPanel = document.getElementById("paymentCheckoutPanel");
const paymentInstruction = document.getElementById("paymentInstruction");
const paymentProviderLabel = document.getElementById("paymentProviderLabel");
const paymentQrHeading = paymentCheckoutPanel.querySelector(".payment-qr-header span");
const onlinePaymentOptionLabel = document.querySelector('.payment-option input[value="eSewa"] + span');
const customerQrBox = document.getElementById("customerQrBox");
const customerQrImage = document.getElementById("customerQrImage");
const onlinePaymentLink = document.getElementById("onlinePaymentLink");
const cancelPaymentBtn = document.getElementById("cancelPaymentBtn");
const acceptOrderBtn = document.getElementById("acceptOrderBtn");
const acceptOrderLabel = document.getElementById("acceptOrderLabel");
const secureNote = document.querySelector(".secure-note");
const isDirectFileMode = window.location.protocol === "file:";
let checkoutInProgress = false;
let currentPaymentOrder = null;
let orderCompleted = false;
let paymentPollTimer = 0;

customerQrImage.addEventListener("load", () => {
  paymentCheckoutPanel.scrollIntoView({ behavior: "smooth", block: "center" });
});

customerQrImage.addEventListener("error", () => {
  customerQrBox.hidden = true;
  paymentInstruction.textContent =
    "Could not load the payment QR. Check the server connection, then cancel this payment and generate a new QR.";
});

function getSelectedPaymentMethod() {
  const selected = document.querySelector('input[name="paymentMethod"]:checked');
  return selected ? selected.value : "Cash";
}

function isOrderLocked() {
  return Boolean(currentPaymentOrder || orderCompleted);
}

const state = {
  cart: []
};

const formatCurrency = (amount) => `Rs. ${Number(amount).toFixed(2)}`;
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;"
})[character]);

function getFoodArtwork(item) {
  const itemName = item.name.toLowerCase();

  if (itemName.includes("momo")) {
    return `
      <svg class="custom-illustration illustration-momo" viewBox="0 0 120 90" aria-hidden="true">
        <path class="dumpling-shell" d="M29 26c8-12 22-19 40-19 20 0 34 8 41 22 8 17 3 39-16 51-15 10-35 11-52 5C27 73 13 58 14 41c0-7 5-13 15-15z"/>
        <path class="dumpling-fill" d="M36 30c15-8 33-9 47-1 8 5 14 15 13 26-1 11-10 18-22 22-18 7-42 4-53-14-6-8-3-24 15-33z"/>
        <path class="dumpling-sauce" d="M41 27c7-2 14-3 18-2 7 1 10 6 12 12-6 0-11 1-17 3-7 3-17 4-25 1 1-11 5-13 12-14z"/>
        <path d="M42 62c6 5 19 8 28 5" fill="none" stroke="#f0b56d" stroke-width="3" stroke-linecap="round"/>
        <path d="M23 20c-7-4-13-2-17 4" fill="none" stroke="#d68d4d" stroke-width="3" stroke-linecap="round"/>
        <path d="M82 16c9-4 16-4 22 1" fill="none" stroke="#d68d4d" stroke-width="3" stroke-linecap="round"/>
      </svg>
    `;
  }

  if (itemName.includes("samosa")) {
    return `
      <svg class="custom-illustration illustration-samosa" viewBox="0 0 120 90" aria-hidden="true">
        <path class="pastry" d="M28 65l25-34 16 18 20-26 12 14 10 35-35 16-27 0-21-23z"/>
        <path class="filling" d="M42 52l13-16 13 13 19-24 11 11-12 20-12 13-20 5-12-22z"/>
        <path d="M30 70l17 5 25-1 17 9 12-9" fill="none" stroke="#cec3b3" stroke-width="3" stroke-linecap="round"/>
      </svg>
    `;
  }

  return `<span aria-hidden="true">${item.emoji}</span>`;
}

function getItemById(itemId) {
  return menu.find((item) => item.id === itemId);
}

function getCartTotalQuantity() {
  return state.cart.reduce((sum, item) => sum + item.quantity, 0);
}

function buildBill() {
  const subtotal = state.cart.reduce((sum, item) => {
    const menuItem = getItemById(item.id);
    return sum + menuItem.price * item.quantity;
  }, 0);

  const discount = subtotal > 10000 ? subtotal * 0.2 : 0;
  const total = subtotal - discount;

  return { subtotal, discount, total };
}

function renderMenu() {
  const orderLocked = isOrderLocked();
  menuGrid.innerHTML = menu.map((item) => `
    <article class="menu-card" aria-label="${item.name}">
      <div class="food-art" style="background:${item.background};">
        ${getFoodArtwork(item)}
      </div>
      <div class="food-details">
        <h3>${item.name}</h3>
        <p>${item.description}</p>
        <div class="food-bottom">
          <span class="food-price">${formatCurrency(item.price)}</span>
          <button class="add-button" type="button" data-id="${item.id}" ${orderLocked ? "disabled" : ""}>Add</button>
        </div>
      </div>
    </article>
  `).join("");

  menuCount.textContent = `${menu.length} delicious choices`;
}

function renderCart() {
  const orderLocked = isOrderLocked();
  if (state.cart.length === 0) {
    cartItems.innerHTML = `
      <div class="empty-cart">
        <span>🛍️</span>
        <strong>Your cart is waiting!</strong>
        <p>Add something delicious from our menu.</p>
      </div>
    `;
    cartCount.textContent = "0";
    subtotalEl.textContent = formatCurrency(0);
    discountEl.textContent = `- ${formatCurrency(0)}`;
    totalEl.textContent = formatCurrency(0);
    discountRow.hidden = true;
    return;
  }

  const items = state.cart.map((entry) => {
    const menuItem = getItemById(entry.id);
    return `
      <div class="cart-line">
        <div>
          <span class="cart-line-name">${menuItem.name}</span>
          <span class="cart-line-price">${formatCurrency(menuItem.price)} each</span>
        </div>
        <div class="cart-line-right">
          <strong>${formatCurrency(menuItem.price * entry.quantity)}</strong>
          <div class="quantity-control" aria-label="Quantity controls for ${menuItem.name}">
            <button type="button" data-action="decrease" data-id="${menuItem.id}" ${orderLocked ? "disabled" : ""}>−</button>
            <span>${entry.quantity}</span>
            <button type="button" data-action="increase" data-id="${menuItem.id}" ${orderLocked ? "disabled" : ""}>+</button>
          </div>
          <button type="button" class="remove-button" data-action="remove" data-id="${menuItem.id}" ${orderLocked ? "disabled" : ""}>Remove</button>
        </div>
      </div>
    `;
  }).join("");

  cartItems.innerHTML = items;
  cartCount.textContent = String(getCartTotalQuantity());

  const { subtotal, discount, total } = buildBill();
  subtotalEl.textContent = formatCurrency(subtotal);
  discountRow.hidden = discount === 0;
  discountEl.textContent = `- ${formatCurrency(discount)}`;
  totalEl.textContent = formatCurrency(total);
}

function addToCart(itemId) {
  if (isOrderLocked()) return;
  const existingItem = state.cart.find((item) => item.id === itemId);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    state.cart.push({ id: itemId, quantity: 1 });
  }

  formMessage.textContent = "";
  renderCart();
}

function changeQuantity(itemId, action) {
  if (isOrderLocked()) return;
  const existingItem = state.cart.find((item) => item.id === itemId);
  if (!existingItem) return;

  if (action === "increase") {
    existingItem.quantity += 1;
  }

  if (action === "decrease") {
    existingItem.quantity -= 1;
  }

  if (existingItem.quantity <= 0) {
    state.cart = state.cart.filter((item) => item.id !== itemId);
  }

  renderCart();
}

function removeItem(itemId) {
  if (isOrderLocked()) return;
  state.cart = state.cart.filter((item) => item.id !== itemId);
  renderCart();
}

function clearCart() {
  if (isOrderLocked()) return;
  state.cart = [];
  formMessage.textContent = "";
  confirmationSection.hidden = true;
  renderCart();
}

function updatePaymentMethodUI() {
  const paymentMethod = getSelectedPaymentMethod();
  const isQrPayment = paymentMethod === "eSewa";
  paymentCheckoutPanel.hidden = !isQrPayment;
  if (isDirectFileMode) {
    paymentQrHeading.textContent = "PHONE CONFIRMATION NEEDS SERVER";
    paymentProviderLabel.textContent = "SERVER REQUIRED";
    onlinePaymentOptionLabel.textContent = "💳 Phone QR (server required)";
  } else {
    paymentQrHeading.textContent = "ONE-TIME QR · SHOW TO CUSTOMER";
    paymentProviderLabel.textContent = "QR payment";
    onlinePaymentOptionLabel.textContent = "💳 Online payment (QR)";
  }
  acceptOrderLabel.textContent = isQrPayment
    ? isDirectFileMode ? "Run server for phone QR" : "Generate QR"
    : "Accept Order";
  if (!currentPaymentOrder) {
    paymentInstruction.textContent = isDirectFileMode
      ? "A customer phone cannot send confirmation to a cashier page opened as a local file. Run start.bat, open its localhost address on the cashier computer, and use the printed Phone access address on the customer's phone."
      : "Generate a one-time QR to scan or open the checkout link. Demo mode simulates payment and does not transfer money.";
  }
}

function saveDirectOpenOrder(paymentMode, transactionUuid = null) {
  const { subtotal, discount, total } = buildBill();
  const order = {
    transaction_uuid: transactionUuid || `LOCAL-${Date.now()}-${Math.random().toString(16).slice(2, 10)}`,
    bill_id: `BILL-${Date.now().toString(36).toUpperCase()}`,
    customer_name: customerNameInput.value.trim() || "Guest",
    items: state.cart.map(({ id, quantity }) => ({
      id,
      quantity,
      unit_price: String(getItemById(id).price)
    })),
    subtotal: String(subtotal),
    discount: String(discount),
    total_amount: String(total),
    status: "COMPLETE",
    payment_status: paymentMode === "DEMO"
      ? "PAYMENT SUCCESSFUL (DEMO)"
      : "PAYMENT SUCCESSFUL",
    reference_id: paymentMode === "DEMO" ? "DEMO" : "CASH",
    payment_mode: paymentMode,
    created_at: new Date().toLocaleString()
  };

  try {
    const storedOrders = JSON.parse(localStorage.getItem("bakeryOrders") || "[]");
    if (!Array.isArray(storedOrders)) {
      throw new Error("Saved order data is not a list.");
    }
    storedOrders.push(order);
    localStorage.setItem("bakeryOrders", JSON.stringify(storedOrders));
  } catch (error) {
    console.error("Could not save direct-open order:", error);
    throw new Error("Could not save this order in browser storage. Try serving the bakery with start.bat.");
  }

  return order;
}

function showCompletedOrder(order) {
  orderCompleted = true;
  renderReceipt(order);
  customerNameInput.disabled = true;
  document.querySelectorAll('input[name="paymentMethod"]').forEach((input) => {
    input.disabled = true;
  });
  clearCartBtn.disabled = true;
  acceptOrderBtn.disabled = true;
  renderMenu();
  renderCart();
  confirmationSection.hidden = false;
  confirmationSection.scrollIntoView({ behavior: "smooth", block: "start" });
  setTimeout(() => window.print(), 500);
}

function renderReceipt(order = null) {
  const paymentMode = order?.payment_mode || "CASH";
  const isDemoPayment = paymentMode === "DEMO";
  const isCashPayment = paymentMode === "CASH";
  const paymentMethod = isDemoPayment ? "QR payment demo" : isCashPayment ? "Cash" : "eSewa";
  const customerName = order?.customer_name || customerNameInput.value.trim() || "Guest";
  const subtotal = order ? Number(order.subtotal) : buildBill().subtotal;
  const discount = order ? Number(order.discount) : buildBill().discount;
  const total = order ? Number(order.total_amount) : buildBill().total;
  const receiptItems = order
    ? order.items
    : state.cart.map((item) => {
      const menuItem = getItemById(item.id);
      return { id: item.id, quantity: item.quantity, unit_price: menuItem.price };
    });
  const paymentStatus = order?.payment_status
    || (isCashPayment ? "PAYMENT DUE" : "PAYMENT SUCCESSFUL");

  confirmationEyebrow.textContent = isDemoPayment
    ? "DEMO PAYMENT"
    : isCashPayment ? "ORDER SAVED" : "PAYMENT VERIFIED";
  confirmationTitle.textContent = isDemoPayment
    ? "Demo complete — bill is ready"
    : isCashPayment ? "Cash payment received — bill is ready" : "Payment successful — bill is ready";
  confirmationMessage.textContent = isDemoPayment
    ? "Payment successful in demo mode. No money was transferred. The demo bill is ready to print."
    : isCashPayment
      ? "Cash payment recorded as received. The bill is ready to print."
      : `Payment successful. ${order?.reference_id ? `Reference ${order.reference_id}. ` : ""}Bill is ready to print.`;
  confirmationSection.querySelector(".confirmed-icon").classList.toggle("pending", false);
  const safeCustomerName = escapeHtml(customerName);

  const rows = receiptItems.map((item) => {
    const menuItem = getItemById(item.id);
    if (!menuItem) return "";
    return `
      <tr>
        <td>${escapeHtml(menuItem.name)}</td>
        <td>${item.quantity}</td>
        <td>${formatCurrency(Number(item.unit_price) * item.quantity)}</td>
      </tr>
    `;
  }).join("");

  receiptEl.innerHTML = `
    <div class="receipt-brand">
      <div class="receipt-logo">🥐</div>
      <div>
        <strong>Namaste Bakery</strong>
        <small>Freshly made, happily served</small>
      </div>
    </div>

    <div class="receipt-header">
      <h3>Namaste Bakery</h3>
      <p>Freshly made, happily served</p>
      <p>${new Date().toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" })}</p>
    </div>

    <div class="receipt-meta">
      <div><strong>Customer:</strong> ${safeCustomerName}</div>
      <div><strong>Bill ID:</strong> ${escapeHtml(order?.bill_id || "Not saved")}</div>
      <div><strong>Payment type:</strong> ${escapeHtml(paymentMethod)}</div>
      <div><strong>Order status:</strong> ORDER SUCCESSFUL</div>
      <div><strong>Payment status:</strong> ${escapeHtml(isDemoPayment ? "PAYMENT SUCCESSFUL (DEMO — NO MONEY TRANSFERRED)" : paymentStatus)}</div>
      ${order?.created_at ? `<div><strong>Saved:</strong> ${escapeHtml(order.created_at)}</div>` : ""}
    </div>

    <table>
      <thead>
        <tr>
          <th>Item</th>
          <th>Qty</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>

    <div class="receipt-total">
      <div><span>Subtotal</span><span>${formatCurrency(subtotal)}</span></div>
      <div><span>Discount</span><span>${formatCurrency(discount)}</span></div>
      <div class="grand-total"><span>Total</span><span>${formatCurrency(total)}</span></div>
    </div>

    <div class="receipt-thanks">Thank you for visiting Namaste Bakery! ✨</div>
  `;
}

async function acceptOrder() {
  if (orderCompleted) return;
  if (state.cart.length === 0) {
    formMessage.textContent = "Please add an item before placing the order.";
    return;
  }

  formMessage.textContent = "";
  if (checkoutInProgress) return;

  if (getSelectedPaymentMethod() === "eSewa") {
    if (isDirectFileMode) {
      paymentInstruction.textContent =
        "Phone-confirmed checkout needs the bakery server. Run start.bat, then open the server's localhost address on the cashier computer and its Phone access address on the customer's phone.";
      formMessage.textContent = "This local-file page cannot receive or verify customer phone confirmation.";
      return;
    }
    checkoutInProgress = true;
    acceptOrderBtn.disabled = true;
    paymentInstruction.textContent = "Creating an online payment request...";
    try {
      const response = await fetch("/api/payments/esewa/initiate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerName: customerNameInput.value.trim(),
          items: state.cart.map(({ id, quantity }) => ({ id, quantity }))
        })
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || "Could not start online checkout.");
      }
      if (
        typeof result.transaction_uuid !== "string"
        || !/^NB-[0-9a-f]{24}$/.test(result.transaction_uuid)
        || typeof result.payment_token !== "string"
        || typeof result.qr_url !== "string"
        || !result.qr_url.startsWith("/api/orders/")
        || typeof result.payment_url !== "string"
        || !["demo", "esewa"].includes(result.payment_mode)
      ) {
        throw new Error("The server returned an invalid online payment request.");
      }
      const paymentUrl = new URL(result.payment_url, window.location.href);
      if (!["http:", "https:"].includes(paymentUrl.protocol) || paymentUrl.username || paymentUrl.password) {
        throw new Error("The server returned an invalid online checkout link.");
      }

      currentPaymentOrder = {
        transactionUuid: result.transaction_uuid,
        paymentToken: result.payment_token,
        paymentMode: result.payment_mode
      };
      paymentProviderLabel.textContent = result.payment_mode === "demo" ? "PAYMENT DEMO" : "eSewa";
      customerQrImage.src = result.qr_url;
      customerQrBox.hidden = false;
      onlinePaymentLink.href = paymentUrl.href;
      onlinePaymentLink.textContent = result.payment_mode === "demo"
        ? "Open demo link"
        : "Open online checkout";
      onlinePaymentLink.hidden = false;
      cancelPaymentBtn.hidden = false;
      acceptOrderLabel.textContent = "Waiting for payment";
      customerNameInput.disabled = true;
      document.querySelectorAll('input[name="paymentMethod"]').forEach((input) => {
        input.disabled = true;
      });
      clearCartBtn.disabled = true;
      renderMenu();
      renderCart();
      checkoutInProgress = false;
      acceptOrderBtn.disabled = true;
      paymentInstruction.textContent = result.payment_mode === "demo"
        ? "SIMULATION ONLY: Scan and open the QR link on the same Wi-Fi, then confirm the demo checkout on the phone. This does not contact a payment provider or transfer money."
        : "On the same Wi-Fi, scan this QR and open its link to continue to eSewa. Scanning without opening the link is not detected. The bill prints only after eSewa verifies payment.";
      pollForPayment();
    } catch (error) {
      console.error("Could not create online payment QR:", error);
      paymentInstruction.textContent = error.message || "Could not create the online payment QR.";
      checkoutInProgress = false;
      acceptOrderBtn.disabled = false;
    }
    return;
  }

  checkoutInProgress = true;
  acceptOrderBtn.disabled = true;
  formMessage.textContent = "Saving order...";
  try {
    let result;
    if (isDirectFileMode) {
      result = { order: saveDirectOpenOrder("CASH") };
    } else {
      const response = await fetch("/api/orders/cash", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerName: customerNameInput.value.trim(),
          items: state.cart.map(({ id, quantity }) => ({ id, quantity }))
        })
      });
      result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || "Could not save the cash order.");
      }
    }
    if (!result.order?.bill_id) {
      throw new Error(result.error || "Could not save the cash order.");
    }
    formMessage.textContent = "";
    showCompletedOrder(result.order);
  } catch (error) {
    console.error("Could not save cash order:", error);
    formMessage.textContent = error.message || "Could not save the order.";
  } finally {
    checkoutInProgress = false;
    acceptOrderBtn.disabled = orderCompleted;
  }
}

function stopPaymentPolling() {
  if (paymentPollTimer) {
    clearTimeout(paymentPollTimer);
    paymentPollTimer = 0;
  }
}

function unlockOrderControls() {
  customerNameInput.disabled = orderCompleted;
  document.querySelectorAll('input[name="paymentMethod"]').forEach((input) => {
    input.disabled = orderCompleted;
  });
  clearCartBtn.disabled = orderCompleted;
  acceptOrderBtn.disabled = orderCompleted;
  cancelPaymentBtn.hidden = true;
  cancelPaymentBtn.disabled = false;
  customerQrBox.hidden = true;
  customerQrImage.removeAttribute("src");
  onlinePaymentLink.hidden = true;
  onlinePaymentLink.removeAttribute("href");
  paymentProviderLabel.textContent = "QR payment";
  acceptOrderLabel.textContent = getSelectedPaymentMethod() === "eSewa"
    ? "Generate QR"
    : "Accept Order";
  renderMenu();
  renderCart();
  updatePaymentMethodUI();
}

async function pollForPayment() {
  if (!currentPaymentOrder) return;
  try {
    const { transactionUuid, paymentToken } = currentPaymentOrder;
    const response = await fetch(
      `/api/orders/${encodeURIComponent(transactionUuid)}?token=${encodeURIComponent(paymentToken)}`,
      { cache: "no-store" }
    );
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "Could not check payment status.");
    }

    if (result.order.status === "COMPLETE") {
      stopPaymentPolling();
      currentPaymentOrder = null;
      orderCompleted = true;
      unlockOrderControls();
      paymentInstruction.textContent = result.order.payment_mode === "DEMO"
        ? "Online payment demo confirmed — no money transferred. Preparing the demo bill and opening print..."
        : "Payment verified successfully! Preparing the bill and opening the print dialog...";
      showCompletedOrder(result.order);
      return;
    }

    if (result.order.status !== "PENDING") {
      throw new Error(`This payment order is ${result.order.status.toLowerCase()}.`);
    }

    paymentInstruction.textContent = result.order.qr_scanned
      ? currentPaymentOrder.paymentMode === "demo"
        ? "Customer opened the demo checkout. Waiting for them to confirm the simulation on their phone; no money will be transferred."
        : "The customer opened the QR checkout link. Waiting for the payment provider to confirm the payment..."
      : currentPaymentOrder.paymentMode === "demo"
        ? "Waiting for the customer to scan and open the QR link on the same Wi-Fi. The customer must confirm the simulation; no money will be transferred."
        : "Waiting for the customer to scan and open the QR link on the same Wi-Fi...";
    cancelPaymentBtn.disabled = result.order.qr_scanned;
  } catch (error) {
    console.error("Could not poll online payment status:", error);
    paymentInstruction.textContent = error.message || "Could not check payment status.";
  }

  if (currentPaymentOrder) {
    paymentPollTimer = setTimeout(pollForPayment, 2000);
  }
}

async function cancelPayment() {
  if (!currentPaymentOrder) return;
  cancelPaymentBtn.disabled = true;
  paymentInstruction.textContent = "Cancelling this payment link...";
  try {
    const response = await fetch("/api/payments/esewa/cancel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        transaction_uuid: currentPaymentOrder.transactionUuid,
        payment_token: currentPaymentOrder.paymentToken
      })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "Could not cancel payment.");
    }
    stopPaymentPolling();
    currentPaymentOrder = null;
    cancelPaymentBtn.disabled = false;
    unlockOrderControls();
    paymentInstruction.textContent = "Payment link cancelled. You can change the order or create a new QR.";
  } catch (error) {
    console.error("Could not cancel online payment:", error);
    paymentInstruction.textContent = error.message || "Could not cancel payment.";
    cancelPaymentBtn.disabled = false;
  }
}

function resetOrder() {
  if (currentPaymentOrder) {
    paymentInstruction.textContent = "Cancel the active payment before starting a new order.";
    return;
  }
  state.cart = [];
  orderCompleted = false;
  customerNameInput.value = "";
  confirmationSection.hidden = true;
  formMessage.textContent = "";
  confirmationEyebrow.textContent = "ORDER RECEIVED";
  confirmationTitle.textContent = "Thank you for choosing us!";
  confirmationMessage.textContent = "Your order has been confirmed in this session.";
  unlockOrderControls();
}

async function handlePaymentReturn() {
  const params = new URLSearchParams(window.location.search);
  if (params.has("data") || params.has("payment")) {
    history.replaceState(null, "", window.location.pathname);
  }
}

document.addEventListener("change", (event) => {
  if (event.target.matches('input[name="paymentMethod"]')) {
    updatePaymentMethodUI();
  }
});

document.addEventListener("input", (event) => {
  if (event.target.id === "customerName") formMessage.textContent = "";
});

document.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;

  if (button.classList.contains("add-button")) {
    addToCart(button.dataset.id);
    return;
  }

  if (button.dataset.action === "increase") {
    changeQuantity(button.dataset.id, "increase");
    return;
  }

  if (button.dataset.action === "decrease") {
    changeQuantity(button.dataset.id, "decrease");
    return;
  }

  if (button.dataset.action === "remove") {
    removeItem(button.dataset.id);
    return;
  }

  if (button.id === "clearCartBtn") {
    clearCart();
    return;
  }

  if (button.id === "acceptOrderBtn") {
    acceptOrder();
    return;
  }

  if (button.id === "cancelPaymentBtn") {
    cancelPayment();
    return;
  }

  if (button.id === "newOrderBtn") {
    resetOrder();
    return;
  }

  if (button.id === "printBtn") {
    window.print();
  }
});

renderMenu();
renderCart();
updatePaymentMethodUI();
if (isDirectFileMode) {
  secureNote.textContent =
    "Cash orders work directly from this file. Customer-confirmed QR checkout requires starting the bakery server with start.bat.";
}
yearEl.textContent = new Date().getFullYear();
handlePaymentReturn();
