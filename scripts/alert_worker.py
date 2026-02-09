import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

import requests
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USER)

PRICE_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"


def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase credentials are not configured.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def now_utc():
    return datetime.now(timezone.utc)


def fetch_btc_price():
    response = requests.get(PRICE_API, timeout=20)
    response.raise_for_status()
    data = response.json()
    return float(data["bitcoin"]["usd"])


def should_trigger(alert, price, now):
    if not alert["enabled"]:
        return False

    threshold = alert["price_threshold"]
    if alert["direction"] == "above" and price < threshold:
        return False
    if alert["direction"] == "below" and price > threshold:
        return False

    last_sent = alert.get("last_sent_at")
    if last_sent:
        last_dt = datetime.fromisoformat(last_sent.replace("Z", "+00:00"))
        delta = (now - last_dt).total_seconds() / 60
        if delta < alert["cooldown_minutes"]:
            return False
    return True


def send_email(to_email, subject, body):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials are not configured.")

    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)


def main():
    client = get_supabase()
    price = fetch_btc_price()
    now = now_utc()

    result = client.table("alerts").select("*").eq("asset", "BTC").execute()
    alerts = result.data or []

    for alert in alerts:
        if not should_trigger(alert, price, now):
            continue

        subject = f"BTC price alert: ${price:,.0f}"
        body = (
            f"BTC is now ${price:,.0f}.\n"
            f"Alert: BTC {alert['direction']} ${alert['price_threshold']:,.0f}.\n\n"
            f"{alert.get('custom_message') or ''}"
        ).strip()

        send_email(alert["email"], subject, body)
        client.table("alerts").update({"last_sent_at": now.isoformat()}).eq("id", alert["id"]).execute()


if __name__ == "__main__":
    main()
