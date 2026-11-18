import base64
from contextlib import contextmanager
from html import escape
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import sqlite3
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from collections.abc import Generator
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from io import BytesIO

import qrcode

ROOT = Path(__file__).resolve().parent


def load_local_environment() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        value = value.strip().strip("\"'")
        if key.strip():
            os.environ.setdefault(key.strip(), value)


load_local_environment()

HOST = os.environ.get("BAKERY_HOST", "0.0.0.0")
PORT = int(os.environ.get("BAKERY_PORT", "8001"))
DATABASE = ROOT / "bakery_payments.sqlite3"
PUBLIC_STATIC_PATHS = {
    "/",
    "/index.html",
    "/script.js",
    "/style.css",
}
PAYMENT_MODE = os.environ.get("PAYMENT_MODE", "demo").lower()
if PAYMENT_MODE not in {"demo", "esewa"}:
    raise ValueError("PAYMENT_MODE must be either 'demo' or 'esewa'.")
ESEWA_ENV = os.environ.get("ESEWA_ENV", "sandbox").lower()
if ESEWA_ENV not in {"sandbox", "production"}:
    raise ValueError("ESEWA_ENV must be either 'sandbox' or 'production'.")
ESEWA_PRODUCT_CODE = os.environ.get(
    "ESEWA_PRODUCT_CODE", "EPAYTEST" if ESEWA_ENV == "sandbox" else ""
)
ESEWA_SECRET_KEY = os.environ.get(
    "ESEWA_SECRET_KEY", "8gBm/:&EnhH.1/q" if ESEWA_ENV == "sandbox" else ""
)
ESEWA_CHECKOUT_URL = (
    "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    if ESEWA_ENV == "sandbox"
    else "https://epay.esewa.com.np/api/epay/main/v2/form"
)
ESEWA_STATUS_URL = (
    "https://rc.esewa.com.np/api/epay/transaction/status/"
    if ESEWA_ENV == "sandbox"
    else "https://esewa.com.np/api/epay/transaction/status/"
)


def discover_lan_ip() -> str:
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        connection.connect(("192.0.2.1", 80))
        return connection.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        connection.close()


LAN_BASE_URL = os.environ.get(
    "BAKERY_LAN_BASE_URL", f"http://{discover_lan_ip()}:{PORT}"
).rstrip("/")
PUBLIC_BASE_URL = os.environ.get("ESEWA_PUBLIC_BASE_URL", LAN_BASE_URL).rstrip("/")
LOG = logging.getLogger("bakery")

# Prices are server-owned so the browser cannot change the amount being charged.
MENU_PRICES = {
    "dal-bhat": 250,
    "chicken-dal-bhat": 400,
    "veg-thali": 220,
    "chicken-thali": 350,
    "thakali-thali": 450,
    "mutton-thali": 550,
    "dhido": 350,
    "gundruk": 120,
    "sel-roti": 40,
    "yomari": 80,
    "veg-momo": 100,
    "chicken-momo": 140,
    "buff-momo": 150,
    "jhol-momo": 180,
    "kothe-momo": 170,
    "chowmein": 120,
    "chicken-chowmein": 170,
    "thukpa": 150,
    "chicken-thukpa": 200,
    "samosa": 30,
    "bara": 80,
    "chatamari": 150,
    "choila": 250,
    "aloo-tama": 150,
    "puri-tarkari": 100,
    "chana-chat": 80,
    "pani-puri": 80,
    "chatpate": 60,
    "litti-chokha": 180,
    "maithili-thali": 999,
    "veg-burger": 120,
    "chicken-burger": 180,
    "pizza": 250,
    "chicken-pizza": 350,
    "french-fries": 100,
    "chicken-fried-rice": 180,
    "veg-fried-rice": 130,
    "chicken-roll": 150,
    "donut": 70,
    "cake-slice": 120,
    "milk-tea": 30,
    "black-tea": 20,
    "coffee": 80,
    "cold-coffee": 150,
    "lassi": 100,
    "lemon-soda": 80,
    "coke": 60,
    "sprite": 60,
    "ice-cream": 100,
    "rasbari": 40,
}
CURRENCY_QUANTUM = Decimal("0.01")


def money(value: Decimal | int | str) -> str:
    return format(Decimal(value).quantize(CURRENCY_QUANTUM, rounding=ROUND_HALF_UP), ".2f")


@contextmanager
def database_connection() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    with database_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                transaction_uuid TEXT PRIMARY KEY,
                bill_id TEXT NOT NULL UNIQUE,
                customer_name TEXT NOT NULL,
                items_json TEXT NOT NULL,
                subtotal TEXT NOT NULL,
                discount TEXT NOT NULL,
                total_amount TEXT NOT NULL,
                status TEXT NOT NULL,
                reference_id TEXT,
                payment_token_hash TEXT NOT NULL,
                qr_scanned_at TEXT,
                payment_mode TEXT NOT NULL DEFAULT 'ESEWA',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {
            column["name"]
            for column in connection.execute("PRAGMA table_info(orders)").fetchall()
        }
        if "bill_id" not in columns:
            connection.execute("ALTER TABLE orders ADD COLUMN bill_id TEXT NOT NULL DEFAULT ''")
            legacy_orders = connection.execute(
                "SELECT transaction_uuid FROM orders WHERE bill_id = ''"
            ).fetchall()
            for order in legacy_orders:
                connection.execute(
                    "UPDATE orders SET bill_id = ? WHERE transaction_uuid = ?",
                    (f"BILL-{order['transaction_uuid']}", order["transaction_uuid"]),
                )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_bill_id ON orders(bill_id)"
        )
        if "payment_token_hash" not in columns:
            connection.execute(
                "ALTER TABLE orders ADD COLUMN payment_token_hash TEXT NOT NULL DEFAULT ''"
            )
        if "qr_scanned_at" not in columns:
            connection.execute("ALTER TABLE orders ADD COLUMN qr_scanned_at TEXT")
        if "payment_mode" not in columns:
            connection.execute(
                "ALTER TABLE orders ADD COLUMN payment_mode TEXT NOT NULL DEFAULT 'ESEWA'"
            )


def calculate_order(payload: dict) -> tuple[list[dict], Decimal, Decimal, Decimal, str]:
    customer_name = str(payload.get("customerName", "")).strip() or "Guest"
    if len(customer_name) > 80:
        raise ValueError("Customer name must be 80 characters or fewer.")
    submitted_items = payload.get("items")
    if not isinstance(submitted_items, list) or not submitted_items:
        raise ValueError("Add at least one item before continuing.")

    items = []
    subtotal = Decimal("0")
    seen = set()
    for item in submitted_items:
        if not isinstance(item, dict):
            raise ValueError("Invalid item in the order.")
        item_id = item.get("id")
        quantity = item.get("quantity")
        if (
            not isinstance(item_id, str)
            or item_id not in MENU_PRICES
            or not isinstance(quantity, int)
            or isinstance(quantity, bool)
        ):
            raise ValueError("An order item or quantity is invalid.")
        if quantity < 1 or quantity > 99 or item_id in seen:
            raise ValueError("Item quantities must be between 1 and 99.")
        seen.add(item_id)
        unit_price = Decimal(MENU_PRICES[item_id])
        subtotal += unit_price * quantity
        items.append(
            {
                "id": item_id,
                "quantity": quantity,
                "unit_price": money(unit_price),
            }
        )

    discount = (subtotal * Decimal("0.20")) if subtotal > 10000 else Decimal("0")
    total = subtotal - discount
    return items, subtotal, discount, total, customer_name


def sign_fields(fields: dict, secret: str) -> str:
    message = ",".join(
        f"{field}={fields[field]}" for field in fields["signed_field_names"].split(",")
    )
    digest = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def decode_esewa_response(encoded_data: str) -> dict:
    normalized = encoded_data.replace(" ", "+")
    normalized += "=" * (-len(normalized) % 4)
    try:
        response = json.loads(base64.b64decode(normalized, validate=True).decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("eSewa returned an invalid payment response.") from exc

    if not isinstance(response, dict):
        raise ValueError("eSewa returned an invalid payment response.")
    required = ("signed_field_names", "signature")
    if any(not isinstance(response.get(key), str) for key in required):
        raise ValueError("eSewa payment response is missing its signature.")
    signed_names = response["signed_field_names"].split(",")
    mandatory_names = {
        "status",
        "total_amount",
        "transaction_uuid",
        "product_code",
        "signed_field_names",
    }
    if (
        not mandatory_names.issubset(signed_names)
        or len(set(signed_names)) != len(signed_names)
        or any(name not in response for name in signed_names)
    ):
        raise ValueError("eSewa payment response has invalid signed fields.")
    expected = sign_fields(
        {"signed_field_names": response["signed_field_names"], **response},
        ESEWA_SECRET_KEY,
    )
    if not hmac.compare_digest(expected, response["signature"]):
        raise ValueError("eSewa payment response signature did not match.")
    return response


def verify_with_esewa(transaction_uuid: str, total_amount: str) -> dict:
    query = urllib.parse.urlencode(
        {
            "product_code": ESEWA_PRODUCT_CODE,
            "total_amount": total_amount,
            "transaction_uuid": transaction_uuid,
        }
    )
    request = urllib.request.Request(
        f"{ESEWA_STATUS_URL}?{query}",
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.loads(response.read(1024 * 1024).decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError("Could not confirm the payment with eSewa. Please retry verification.") from exc

    if not isinstance(result, dict):
        raise RuntimeError("eSewa returned an invalid transaction status.")
    return result


def order_response(row: sqlite3.Row) -> dict:
    payment_mode = row["payment_mode"]
    if payment_mode == "CASH":
        payment_status = "PAYMENT SUCCESSFUL" if row["status"] == "COMPLETE" else "PAYMENT DUE"
    elif row["status"] == "COMPLETE" and payment_mode == "DEMO":
        payment_status = "PAYMENT SUCCESSFUL (DEMO)"
    elif row["status"] == "COMPLETE":
        payment_status = "PAYMENT SUCCESSFUL"
    else:
        payment_status = row["status"]
    return {
        "transaction_uuid": row["transaction_uuid"],
        "bill_id": row["bill_id"],
        "customer_name": row["customer_name"],
        "items": json.loads(row["items_json"]),
        "subtotal": row["subtotal"],
        "discount": row["discount"],
        "total_amount": row["total_amount"],
        "status": row["status"],
        "payment_status": payment_status,
        "reference_id": row["reference_id"],
        "qr_scanned": row["qr_scanned_at"] is not None,
        "payment_mode": payment_mode,
        "created_at": row["created_at"],
    }


def checkout_fields(transaction_uuid: str, total_amount: str) -> dict:
    fields = {
        "amount": total_amount,
        "tax_amount": "0",
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": ESEWA_PRODUCT_CODE,
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "success_url": f"{PUBLIC_BASE_URL}/payment/esewa/success",
        "failure_url": f"{PUBLIC_BASE_URL}/payment/esewa/failure",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }
    fields["signature"] = sign_fields(fields, ESEWA_SECRET_KEY)
    return fields


def build_demo_checkout_html(row: sqlite3.Row, token: str) -> bytes:
    transaction_uuid = escape(row["transaction_uuid"], quote=True)
    payment_token = escape(token, quote=True)
    page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#321b16"><title>Online payment demo | Namaste Bakery</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;background:#fff8f1;color:#321b16;margin:0;padding:24px}}
main{{max-width:440px;margin:8vh auto;background:white;border:1px solid #ead9ca;border-radius:18px;padding:26px;box-shadow:0 12px 36px #321b1612}}
h1{{font-size:25px;margin:0 0 4px}}.muted,.note{{color:#76695f}}
.badge{{display:inline-block;border-radius:999px;background:#fff0d9;color:#8b4a12;padding:5px 10px;font-size:12px;font-weight:700}}
.total{{display:flex;justify-content:space-between;border-top:1px solid #ead9ca;padding-top:16px;font-size:20px;font-weight:700}}
button{{width:100%;border:0;border-radius:10px;padding:15px;background:#321b16;color:white;font-size:17px;font-weight:700;margin-top:20px}}
button:disabled{{opacity:.65}}.note{{font-size:13px;margin:14px 0 0}}.success{{color:#287342;font-weight:700}}
</style>
<main>
<span class="badge">SIMULATION · NO MONEY WILL BE TRANSFERRED</span>
<h1>Namaste Bakery</h1>
<p class="muted">Demo checkout for {escape(row["customer_name"])}</p>
<div class="total"><span>Total</span><span>Rs. {escape(row["total_amount"])}</span></div>
<button id="confirm-demo" type="button">Confirm demo payment</button>
<p class="note" id="checkout-status" role="status">Tap to send your confirmation to the bakery server. The cashier bill is prepared only after this server confirms this order. Demo only: no money is transferred.</p>
</main>
<script>
const confirmButton = document.getElementById("confirm-demo");
const statusMessage = document.getElementById("checkout-status");
confirmButton.addEventListener("click", async () => {{
  confirmButton.disabled = true;
  statusMessage.textContent = "Confirming demo checkout…";
  try {{
    const response = await fetch("/api/payments/demo/confirm", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{
        transaction_uuid: "{transaction_uuid}",
        payment_token: "{payment_token}"
      }})
    }});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not confirm demo checkout.");
    const order = result.order;
    if (
      !order
      || order.transaction_uuid !== "{transaction_uuid}"
      || order.status !== "COMPLETE"
      || order.payment_mode !== "DEMO"
      || typeof order.bill_id !== "string"
      || !order.bill_id
    ) {{
      throw new Error("The bakery server did not verify this demo confirmation.");
    }}
    confirmButton.hidden = true;
    statusMessage.className = "note success";
    statusMessage.textContent =
      `Demo confirmation verified by the bakery server. Bill ${{order.bill_id}} is ready at the cashier. No money was transferred.`;
  }} catch (error) {{
    statusMessage.textContent = error.message || "Could not confirm demo checkout.";
    confirmButton.disabled = false;
  }}
}});
</script>
</html>"""
    return page.encode("utf-8")


def build_customer_checkout_html(row: sqlite3.Row) -> bytes:
    fields = checkout_fields(row["transaction_uuid"], row["total_amount"])
    inputs = "\n".join(
        f'<input type="hidden" name="{escape(name, quote=True)}" value="{escape(value, quote=True)}">'
        for name, value in fields.items()
    )
    items = json.loads(row["items_json"])
    item_lines = "\n".join(
        f"<li>{escape(item['id'])} × {item['quantity']}</li>" for item in items
    )
    page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#321b16"><title>Pay Namaste Bakery with eSewa</title>
<style>
body{{font:16px/1.5 system-ui,sans-serif;background:#fff8f1;color:#321b16;margin:0;padding:24px}}
main{{max-width:440px;margin:8vh auto;background:white;border:1px solid #ead9ca;border-radius:18px;padding:26px;box-shadow:0 12px 36px #321b1612}}
h1{{font-size:25px;margin:0 0 4px}}.muted,.note{{color:#76695f}}ul{{padding-left:21px;color:#55443c}}
.total{{display:flex;justify-content:space-between;border-top:1px solid #ead9ca;padding-top:16px;font-size:20px;font-weight:700}}
button{{width:100%;border:0;border-radius:10px;padding:15px;background:#321b16;color:white;font-size:17px;font-weight:700;margin-top:20px}}
.note{{font-size:13px;margin:14px 0 0}}
</style>
<main><h1>Namaste Bakery</h1>
<p class="muted">Secure eSewa payment · Order for {escape(row["customer_name"])}</p>
<ul>{item_lines}</ul>
<div class="total"><span>Total</span><span>Rs. {escape(row["total_amount"])}</span></div>
<form id="esewa-checkout" method="post" action="{escape(ESEWA_CHECKOUT_URL, quote=True)}">{inputs}
<button type="submit">Continue to eSewa</button></form>
<p class="note" id="checkout-status" role="status">Opening secure eSewa checkout…</p>
<p class="note">Authorize the payment in eSewa. After confirmation, this page will show success and the cashier's bill will be ready to print.</p></main>
<script>
const checkoutForm = document.getElementById("esewa-checkout");
try {{
  if (typeof checkoutForm.requestSubmit === "function") {{
    checkoutForm.requestSubmit();
  }} else {{
    checkoutForm.submit();
  }}
}} catch (error) {{
  document.getElementById("checkout-status").textContent =
    "Automatic redirect was blocked. Tap Continue to eSewa to proceed.";
}}
</script>
</html>"""
    return page.encode("utf-8")


def generate_qr_png(data: str) -> bytes:
    buffer = BytesIO()
    qrcode.make(data).save(buffer, "PNG")
    return buffer.getvalue()


class BakeryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid request size.") from exc
        if length < 1 or length > 65536:
            raise ValueError("Request must contain valid JSON smaller than 64 KB.")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must be valid JSON.") from exc
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return payload

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/payments/esewa/initiate":
            self.initiate_esewa_payment()
            return
        if path == "/api/payments/demo/confirm":
            self.confirm_demo_payment()
            return
        if path == "/api/orders/cash":
            self.create_cash_order()
            return
        if path == "/api/payments/esewa/cancel":
            self.cancel_esewa_payment()
            return
        if path == "/api/payments/esewa/verify":
            self.send_json(405, {"error": "eSewa returns payment status through its signed callback."})
            return
        self.send_json(404, {"error": "Not found."})

    def cancel_esewa_payment(self):
        try:
            payload = self.read_json()
            transaction_uuid = payload.get("transaction_uuid", "")
            token = payload.get("payment_token", "")
            if not isinstance(transaction_uuid, str) or not isinstance(token, str):
                raise ValueError("Invalid payment reference.")
            with database_connection() as connection:
                connection.execute("BEGIN IMMEDIATE")
                row = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()
                if row is None or not self.valid_order_token(row, token):
                    raise ValueError("Payment order not found.")
                if row["status"] != "PENDING":
                    self.send_json(409, {"error": "This payment is no longer pending."})
                    return
                if row["qr_scanned_at"] is not None:
                    self.send_json(
                        409,
                        {"error": "The customer has opened checkout. Wait for eSewa's result before ending this order."},
                    )
                    return
                updated = connection.execute(
                    "UPDATE orders SET status = 'CANCELLED' "
                    "WHERE transaction_uuid = ? AND status = 'PENDING'",
                    (transaction_uuid,),
                ).rowcount
                if updated != 1:
                    self.send_json(409, {"error": "Payment status changed; check its latest status."})
                    return
            self.send_json(200, {"status": "CANCELLED"})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except sqlite3.Error:
            LOG.exception("Could not cancel eSewa payment")
            self.send_json(503, {"error": "Could not cancel this payment."})

    def confirm_demo_payment(self):
        try:
            payload = self.read_json()
            transaction_uuid = payload.get("transaction_uuid", "")
            token = payload.get("payment_token", "")
            if (
                not isinstance(transaction_uuid, str)
                or not re.fullmatch(r"NB-[0-9a-f]{24}", transaction_uuid)
                or not isinstance(token, str)
            ):
                raise ValueError("Invalid demo payment reference.")

            with database_connection() as connection:
                connection.execute("BEGIN IMMEDIATE")
                row = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()
                if (
                    row is None
                    or row["payment_mode"] != "DEMO"
                    or not self.valid_order_token(row, token)
                ):
                    self.send_json(404, {"error": "Demo checkout not found."})
                    return
                if row["status"] != "PENDING" or row["qr_scanned_at"] is None:
                    self.send_json(409, {"error": "This demo checkout is not awaiting confirmation."})
                    return

                updated = connection.execute(
                    "UPDATE orders SET status = 'COMPLETE', reference_id = 'DEMO' "
                    "WHERE transaction_uuid = ? AND payment_mode = 'DEMO' "
                    "AND status = 'PENDING' AND qr_scanned_at IS NOT NULL",
                    (transaction_uuid,),
                ).rowcount
                if updated != 1:
                    self.send_json(409, {"error": "This demo checkout is no longer pending."})
                    return
                completed_order = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()

            if completed_order is None:
                raise RuntimeError("The demo order disappeared during confirmation.")
            self.send_json(200, {"order": order_response(completed_order)})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except (RuntimeError, sqlite3.Error):
            LOG.exception("Could not confirm demo payment")
            self.send_json(503, {"error": "Could not confirm this demo checkout."})

    def initiate_esewa_payment(self):
        try:
            if PAYMENT_MODE == "esewa":
                if not ESEWA_PRODUCT_CODE or not ESEWA_SECRET_KEY:
                    raise RuntimeError("Set ESEWA_PRODUCT_CODE and ESEWA_SECRET_KEY before accepting payments.")
                base_url = urllib.parse.urlsplit(PUBLIC_BASE_URL)
                if (
                    base_url.scheme not in {"http", "https"}
                    or not base_url.netloc
                    or base_url.path
                    or base_url.query
                    or base_url.fragment
                    or base_url.username
                    or base_url.password
                ):
                    raise RuntimeError("ESEWA_PUBLIC_BASE_URL must be an absolute HTTP or HTTPS origin.")
                if ESEWA_ENV == "production" and not PUBLIC_BASE_URL.startswith("https://"):
                    raise RuntimeError("Live eSewa payments require ESEWA_PUBLIC_BASE_URL to use HTTPS.")
            payload = self.read_json()
            items, subtotal, discount, total, customer_name = calculate_order(payload)
            transaction_uuid = f"NB-{secrets.token_hex(12)}"
            bill_id = f"BILL-{secrets.token_hex(6).upper()}"
            payment_token = secrets.token_urlsafe(32)
            amount_text = money(total)
            with database_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO orders
                    (transaction_uuid, bill_id, customer_name, items_json, subtotal, discount,
                     total_amount, status, payment_token_hash, payment_mode)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
                    """,
                    (
                        transaction_uuid,
                        bill_id,
                        customer_name,
                        json.dumps(items, separators=(",", ":")),
                        money(subtotal),
                        money(discount),
                        amount_text,
                        hashlib.sha256(payment_token.encode("utf-8")).hexdigest(),
                        PAYMENT_MODE.upper(),
                    ),
                )

            token_query = urllib.parse.urlencode(
                {"transaction_uuid": transaction_uuid, "token": payment_token}
            )
            self.send_json(
                200,
                {
                    "transaction_uuid": transaction_uuid,
                    "payment_token": payment_token,
                    "payment_mode": PAYMENT_MODE,
                    "payment_url": f"{LAN_BASE_URL}/pay/esewa?{token_query}",
                    "qr_url": (
                        f"/api/orders/{transaction_uuid}/qr?"
                        f"{urllib.parse.urlencode({'token': payment_token})}"
                    ),
                },
            )
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except (RuntimeError, sqlite3.Error) as exc:
            LOG.exception("Could not initiate eSewa payment")
            self.send_json(503, {"error": str(exc)})

    def create_cash_order(self):
        try:
            payload = self.read_json()
            items, subtotal, discount, total, customer_name = calculate_order(payload)
            transaction_uuid = f"NB-{secrets.token_hex(12)}"
            bill_id = f"BILL-{secrets.token_hex(6).upper()}"
            with database_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO orders
                    (transaction_uuid, bill_id, customer_name, items_json, subtotal, discount,
                     total_amount, status, payment_token_hash, payment_mode)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'COMPLETE', '', 'CASH')
                    """,
                    (
                        transaction_uuid,
                        bill_id,
                        customer_name,
                        json.dumps(items, separators=(",", ":")),
                        money(subtotal),
                        money(discount),
                        money(total),
                    ),
                )
                row = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()
            if row is None:
                raise RuntimeError("The cash order could not be loaded after saving.")
            self.send_json(201, {"order": order_response(row)})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except (RuntimeError, sqlite3.Error) as exc:
            LOG.exception("Could not save cash order")
            self.send_json(503, {"error": "Could not save this order. Please retry."})

    def verify_esewa_payment(self, encoded_data: str) -> dict:
        try:
            if not isinstance(encoded_data, str) or len(encoded_data) > 16384:
                raise ValueError("The eSewa response is missing or invalid.")
            response = decode_esewa_response(encoded_data)
            transaction_uuid = response.get("transaction_uuid")
            if not isinstance(transaction_uuid, str):
                raise ValueError("The eSewa response is missing its transaction reference.")

            with database_connection() as connection:
                row = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()
            if row is None:
                raise ValueError("This eSewa transaction does not belong to a bakery order.")
            if row["payment_mode"] != "ESEWA":
                raise ValueError("This is a demo payment and cannot be verified by eSewa.")
            if row["status"] == "CANCELLED":
                raise ValueError("This bakery payment order was cancelled.")
            if response.get("product_code") != ESEWA_PRODUCT_CODE:
                raise ValueError("eSewa returned a different merchant product code.")
            try:
                response_amount = money(Decimal(str(response.get("total_amount", ""))))
            except InvalidOperation as exc:
                raise ValueError("eSewa returned an invalid payment amount.") from exc
            if response_amount != row["total_amount"]:
                raise ValueError("The eSewa payment amount does not match this order.")

            status = verify_with_esewa(transaction_uuid, row["total_amount"])
            try:
                status_amount = money(Decimal(str(status.get("total_amount", "0"))))
            except InvalidOperation as exc:
                raise ValueError("eSewa returned an invalid transaction amount.") from exc
            if (
                status.get("status") != "COMPLETE"
                or status.get("transaction_uuid") != transaction_uuid
                or status.get("product_code") != ESEWA_PRODUCT_CODE
                or status_amount != row["total_amount"]
            ):
                raise ValueError("eSewa has not confirmed the full payment for this order.")

            with database_connection() as connection:
                updated = connection.execute(
                    "UPDATE orders SET status = 'COMPLETE', reference_id = ?, qr_scanned_at = "
                    "COALESCE(qr_scanned_at, CURRENT_TIMESTAMP) "
                    "WHERE transaction_uuid = ? AND status = 'PENDING'",
                    (str(status.get("ref_id") or ""), transaction_uuid),
                ).rowcount
                paid_row = connection.execute(
                    "SELECT * FROM orders WHERE transaction_uuid = ?",
                    (transaction_uuid,),
                ).fetchone()
            if paid_row is None:
                raise RuntimeError("The payment order disappeared during verification.")
            if updated == 0 and paid_row["status"] != "COMPLETE":
                raise ValueError("This bakery payment order is no longer pending.")
            return order_response(paid_row)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        except (RuntimeError, sqlite3.Error) as exc:
            LOG.exception("Could not verify eSewa payment")
            raise RuntimeError(str(exc)) from exc

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/pay/esewa":
            self.show_customer_checkout(query)
            return
        if parsed.path == "/payment/esewa/success":
            self.send_customer_return((query.get("data") or [""])[0])
            return
        if parsed.path == "/payment/esewa/failure":
            self.send_customer_failure()
            return
        if parsed.path.startswith("/api/orders/"):
            parts = parsed.path.removeprefix("/api/orders/").strip("/").split("/")
            if len(parts) == 2 and parts[1] == "qr":
                self.get_order_qr(parts[0], query)
                return
            if len(parts) == 1:
                self.get_paid_order(parts[0], query)
                return
            self.send_json(404, {"error": "Not found."})
            return
        if parsed.path not in PUBLIC_STATIC_PATHS:
            self.send_error(404, "File not found.")
            return
        super().do_GET()

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path not in PUBLIC_STATIC_PATHS:
            self.send_error(404, "File not found.")
            return
        super().do_HEAD()

    @staticmethod
    def valid_order_token(row: sqlite3.Row, token: str) -> bool:
        if not token:
            return False
        supplied_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return hmac.compare_digest(supplied_hash, row["payment_token_hash"])

    def show_customer_checkout(self, query: dict):
        transaction_uuid = (query.get("transaction_uuid") or [""])[0]
        token = (query.get("token") or [""])[0]
        with database_connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM orders WHERE transaction_uuid = ?",
                (transaction_uuid,),
            ).fetchone()
            if row is not None and row["status"] == "PENDING" and self.valid_order_token(row, token):
                updated = connection.execute(
                    "UPDATE orders SET qr_scanned_at = COALESCE(qr_scanned_at, CURRENT_TIMESTAMP) "
                    "WHERE transaction_uuid = ? AND status = 'PENDING'",
                    (transaction_uuid,),
                ).rowcount
                if updated != 1:
                    row = None
        if row is not None and row["payment_mode"] == "DEMO" and row["status"] == "COMPLETE":
            body = (
                b"<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
                b"<meta name=\"viewport\" content=\"width=device-width\">"
                b"<title>Online payment demo complete | Namaste Bakery</title>"
                b"<style>body{font:16px/1.5 system-ui,sans-serif;max-width:36rem;"
                b"margin:15vh auto;padding:1rem;color:#321b16}</style>"
                b"<h1>Online payment demo confirmed</h1>"
                b"<p>This is only a payment-flow demonstration. No payment provider was contacted and no money was transferred.</p>"
                b"<p>The cashier has been notified and can print the demo bill.</p></html>"
            )
            status = 200
        elif row is not None and row["status"] == "PENDING" and self.valid_order_token(row, token):
            body = (
                build_demo_checkout_html(row, token)
                if row["payment_mode"] == "DEMO"
                else build_customer_checkout_html(row)
            )
            status = 200
        else:
            body = (
                b"<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
                b"<meta name=\"viewport\" content=\"width=device-width\">"
                b"<title>Payment link unavailable</title>"
                b"<h1>This payment link is invalid or has expired.</h1></html>"
            )
            status = 404
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def get_order_qr(self, transaction_uuid: str, query: dict):
        token = (query.get("token") or [""])[0]
        with database_connection() as connection:
            row = connection.execute(
                "SELECT * FROM orders WHERE transaction_uuid = ?",
                (transaction_uuid,),
            ).fetchone()
        if (
            row is None
            or row["status"] != "PENDING"
            or not self.valid_order_token(row, token)
        ):
            self.send_json(404, {"error": "Payment link not found or expired."})
            return
        payment_url = f"{LAN_BASE_URL}/pay/esewa?{urllib.parse.urlencode({'transaction_uuid': transaction_uuid, 'token': token})}"
        image = generate_qr_png(payment_url)
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(image)))
        self.end_headers()
        self.wfile.write(image)

    def get_paid_order(self, transaction_uuid: str, query: dict):
        if not re.fullmatch(r"NB-[0-9a-f]{24}", transaction_uuid):
            self.send_json(400, {"error": "Invalid transaction reference."})
            return
        token = (query.get("token") or [""])[0]
        with database_connection() as connection:
            row = connection.execute(
                "SELECT * FROM orders WHERE transaction_uuid = ?",
                (transaction_uuid,),
            ).fetchone()
        if row is None:
            self.send_json(404, {"error": "Order not found."})
            return
        if not hmac.compare_digest(
            hashlib.sha256(token.encode("utf-8")).hexdigest(), row["payment_token_hash"]
        ):
            self.send_json(404, {"error": "Order not found."})
            return
        self.send_json(200, {"order": order_response(row)})

    def send_customer_return(self, encoded_data: str):
        try:
            self.verify_esewa_payment(encoded_data)
            message = (
                "Payment verified successfully! Your cashier has been notified, "
                "and the bill is ready to print. Please return to the cashier."
            )
            status_code = 200
        except ValueError as exc:
            message = f"Payment is not verified: {escape(str(exc))}. Please contact the cashier."
            status_code = 400
        except RuntimeError as exc:
            message = f"Payment verification is temporarily unavailable: {escape(str(exc))}. Please contact the cashier."
            status_code = 503
        body = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>eSewa payment result | Namaste Bakery</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:36rem;margin:15vh auto;padding:1rem;color:#321b16}}</style>
<h1>Namaste Bakery payment</h1><p>{message}</p></html>""".encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_customer_failure(self):
        body = (
            b"<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
            b"<meta name=\"viewport\" content=\"width=device-width\">"
            b"<title>Payment not completed | Namaste Bakery</title>"
            b"<h1>Payment not completed</h1><p>eSewa did not complete this payment. "
            b"Please return to the cashier; no paid bill was created.</p></html>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    initialize_database()
    server = ThreadingHTTPServer((HOST, PORT), BakeryHandler)
    print(f"Namaste Bakery running: http://localhost:{PORT}")
    print(f"Phone access (same Wi-Fi): {LAN_BASE_URL}")
    print(f"eSewa environment: {ESEWA_ENV} ({ESEWA_PRODUCT_CODE or 'merchant code not configured'})")
    if ESEWA_ENV != "sandbox" and not PUBLIC_BASE_URL.startswith("https://"):
        print("Warning: production eSewa callbacks should use ESEWA_PUBLIC_BASE_URL with HTTPS.")
    threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBakery server stopped.")
    finally:
        server.server_close()
