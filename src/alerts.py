import os
from datetime import datetime, timezone

try:
    from supabase import create_client
except Exception:  # pragma: no cover - optional dependency for local envs
    create_client = None


SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def get_supabase():
    if create_client is None:
        raise RuntimeError(
            "supabase package is not installed. Run `pip install -r requirements.txt`."
        )
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase credentials are not configured.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def now_utc():
    return datetime.now(timezone.utc)


def create_alert(payload: dict):
    client = get_supabase()
    return client.table("alerts").insert(payload).execute()


def list_alerts():
    client = get_supabase()
    return client.table("alerts").select("*").order("created_at", desc=True).execute()


def update_alert(alert_id: str, payload: dict):
    client = get_supabase()
    return client.table("alerts").update(payload).eq("id", alert_id).execute()


def delete_alert(alert_id: str):
    client = get_supabase()
    return client.table("alerts").delete().eq("id", alert_id).execute()
