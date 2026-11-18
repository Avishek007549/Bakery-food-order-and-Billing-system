# Namaste Bakery

## Run on Windows

1. Install Python 3 if it is not already installed.
2. Double-click `start.bat`, or run it from a terminal.
3. The launcher creates a project-local `.venv` on first run and starts the bakery at <http://localhost:8001>.
4. Stop the server with `Ctrl+C` in its terminal.

The launcher installs the QR-code package into `.venv` automatically.

## Run from VS Code

Run **Tasks: Run Task** from the Command Palette and choose **Run Namaste Bakery**. This runs the same launcher and environment setup as `start.bat`.

## Open `index.html` directly

You can open `index.html` from File Explorer without starting the server. In this mode, cash orders are saved in the current browser's local storage, on this device only. Cash should be marked paid only after the cashier has actually collected it. Phone-confirmed QR checkout is unavailable when the HTML file is opened directly: the browser cannot receive a confirmation from another device. Select the QR option to see instructions, then run `start.bat` for a customer-scanned checkout.

For a phone to open a checkout page and report a demo confirmation to the cashier, shared order records, or eSewa checkout, start the app with `start.bat` instead. Keep the phone and cashier computer on the same Wi-Fi network, open `http://localhost:8001` on the cashier computer, add items, and choose **Generate QR**. The phone must use the printed **Phone access (same Wi-Fi)** URL. Do not use `localhost` as the phone-facing address.

### Phone-scanned demo checkout

1. Run `start.bat` and open the **Phone access (same Wi-Fi)** address printed in its terminal on the cashier computer.
2. Add items, leave **Online payment (QR)** selected, and choose **Generate QR**.
3. Scan the QR with the customer's phone while both devices are on the same Wi-Fi, then open the link.
4. The customer reviews the total and taps **Confirm demo payment**. The server checks the order-specific token and that checkout was opened from its QR; only then does the cashier screen update and open the demo bill for printing. The customer checkout also displays the bill ID returned by the server.

This verifies a customer confirmation for a simulated demo only. It does not verify or charge a wallet or bank account. Real payments must use a supported payment provider and its server-side verification.

## QR payment flow

The default `PAYMENT_MODE=demo` runs a simulated online payment flow. Each order creates a one-time QR code and an online checkout link. The customer scans and opens the link, reviews the amount, and explicitly confirms the demo checkout; the cashier then sees the demo order complete and can print the bill. The demo is clearly labeled and does not contact a payment provider or transfer real money.

To test eSewa's sandbox checkout instead, set `PAYMENT_MODE=esewa`. Each order creates a one-time QR code and an online checkout link for the same payment session. The customer must complete checkout in eSewa; the cashier prints the bill only after the server verifies eSewa's signed response and confirms the transaction status. Sandbox payments do not transfer real money.

When running through `start.bat`, every eSewa, demo QR, and cash order is saved in `bakery_payments.sqlite3` with its items, totals, payment type/status, creation time, and unique bill ID. Accepting a cash order records it as paid (the cashier should only accept after collecting cash); QR demos are marked as successful demo payments and are not real transfers. Keep a backup of this database if you need to retain order history.

### eSewa setup and phone access

Copy `.env.example` to `.env` in the project folder if you need to change the defaults, then start the app with `start.bat`. To use eSewa, set `PAYMENT_MODE=esewa`; use merchant-issued credentials for live payments.

For phone access, allow incoming connections to port 8001 through Windows Firewall and ensure Wi-Fi client isolation is disabled. The server prints a **Phone access (same Wi-Fi)** URL at startup. If automatic LAN-address discovery selects the wrong network adapter, set `BAKERY_LAN_BASE_URL` in `.env` to the cashier computer's reachable address, for example `http://192.168.1.20:8001`. Do not use `localhost` for the phone-facing URL.

### Live payments

Replace the sandbox settings in `.env` with the production product code and secret issued for your eSewa merchant account. Set `PAYMENT_MODE=esewa`, `ESEWA_ENV=production`, and `ESEWA_PUBLIC_BASE_URL` to the app's public HTTPS origin. The eSewa return URLs must reach this server; a local-only app is not suitable for live remote use. Never put the merchant secret in `script.js` or publish `.env`.

The QR opens the bakery's order-specific page, which submits a signed request to eSewa's hosted checkout. Payment confirmation comes from eSewa's signed response plus the server-to-server transaction status request; scanning the QR alone cannot confirm a payment.

eSewa's flow and signature/status verification are based on its [official ePay documentation](https://developer.esewa.com.np/pages/Epay).
