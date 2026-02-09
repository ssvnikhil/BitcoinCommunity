import os

import streamlit as st

from alerts import create_alert, delete_alert, list_alerts, update_alert


def show_content():
    st.title("Price Alerts")

    st.info(
        "Create BTC price alerts. Notifications are sent via Gmail SMTP from a scheduled worker."
    )

    supabase_ready = True
    if not os.environ.get("SUPABASE_URL"):
        st.warning("SUPABASE_URL is not set. Alerts will not be saved.")
        supabase_ready = False
    if not os.environ.get("SUPABASE_SERVICE_KEY"):
        st.warning("SUPABASE_SERVICE_KEY is not set. Alerts will not be saved.")
        supabase_ready = False
    if not supabase_ready:
        st.caption(
            "If you don't want local secrets, skip alert creation locally. "
            "Configure Supabase in your deployed environment only."
        )

    st.subheader("Create an alert")
    with st.form("create_alert_form"):
        email = st.text_input("Email address")
        direction = st.selectbox("Trigger when BTC price is", ["above", "below"])
        threshold = st.number_input("BTC price threshold (USD)", min_value=1.0, step=10.0)
        cooldown = st.number_input("Cooldown (minutes)", min_value=30, value=60, step=30)
        custom_note = st.text_area("Custom message (optional)")
        enabled = st.checkbox("Enable alert", value=True)
        submitted = st.form_submit_button("Create alert", disabled=not supabase_ready)

    if submitted:
        if not email:
            st.error("Email is required.")
        else:
            payload = {
                "email": email,
                "asset": "BTC",
                "direction": direction,
                "price_threshold": threshold,
                "cooldown_minutes": int(cooldown),
                "custom_message": custom_note,
                "enabled": enabled,
            }
            try:
                create_alert(payload)
                st.success("Alert created.")
            except Exception as exc:
                st.error(f"Failed to create alert: {exc}")

    st.subheader("Your alerts")
    if supabase_ready:
        try:
            response = list_alerts()
            rows = response.data or []
        except Exception as exc:
            st.warning(f"Unable to load alerts: {exc}")
            rows = []
    else:
        rows = []

    if not rows:
        st.write("No alerts yet.")
        return

    for row in rows:
        with st.expander(f"{row['email']} | {row['direction']} ${row['price_threshold']:,.0f}"):
            st.write(f"Status: {'Enabled' if row['enabled'] else 'Disabled'}")
            st.write(f"Cooldown: {row['cooldown_minutes']} minutes")
            st.write(f"Custom message: {row.get('custom_message') or '—'}")
            st.write(f"Last sent: {row.get('last_sent_at') or '—'}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Toggle", key=f"toggle_{row['id']}"):
                    try:
                        update_alert(row["id"], {"enabled": not row["enabled"]})
                        st.success("Updated.")
                    except Exception as exc:
                        st.error(f"Update failed: {exc}")
            with col2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    try:
                        delete_alert(row["id"])
                        st.success("Deleted.")
                    except Exception as exc:
                        st.error(f"Delete failed: {exc}")
