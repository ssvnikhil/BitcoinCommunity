from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

try:
    import feedparser
except Exception:  # pragma: no cover - optional dependency for local envs
    feedparser = None

import xml.etree.ElementTree as ET

from utils import format_compact

BLOCKCHAIN_API = "https://api.blockchain.info/charts"


def show_content():
    st.title("Signal Desk")

    st.markdown(
        """
        A focused briefing for people who want clarity, not noise. This section frames Bitcoin as money,
        compares it to familiar assets, and highlights on-chain activity.
        """
    )

    st.info(
        "This content is educational and does not constitute investment advice. Bitcoin is volatile and high risk."
    )

    tabs = st.tabs(
        ["Primer", "Comparative Lens", "On-Chain Signals", "Merchant Adoption", "Daily Brief"],
    )

    with tabs[0]:
        render_primer()

    with tabs[1]:
        render_comparison()

    with tabs[2]:
        render_onchain()

    with tabs[3]:
        render_merchants()

    with tabs[4]:
        render_brief()

    st.markdown("---")
    st.markdown("### References")
    st.markdown(
        """
        - Fidelity Digital Assets: Bitcoin First Revisited (Sept 2023)
        - Blockchain.com Charts & Statistics API
        - CoinDesk RSS feed
        """
    )


# ----------------------------
# Primer
# ----------------------------

def render_primer():
    st.header("What Is Bitcoin?")
    st.markdown(
        """
        Bitcoin is a decentralized monetary network and a digital asset native to that network. It enables
        peer-to-peer value transfer without a central intermediary and enforces a fixed supply policy.
        """
    )

    st.subheader("Why Some Investors Consider It an Investment")
    st.markdown(
        """
        Investors who allocate to bitcoin often frame it as an emerging monetary good and store-of-value asset.
        The thesis centers on scarcity, decentralization, and the ability to hold value in a digital world.
        """
    )

    st.subheader("Hard / Sound Money Characteristics")
    st.markdown(
        """
        Good money tends to be durable, divisible, portable, fungible, verifiable, and scarce. Bitcoin combines
        digital portability with enforceable scarcity, which is why many analysts group it with hard money.
        """
    )

    st.markdown("### Signals to Remember")
    st.markdown(
        """
        1. Scarcity is enforceable by consensus, not by trust in an issuer.
        2. The network is open-source and permissionless, so settlement is global.
        3. Monetary premiums tend to concentrate in the best monetary good.
        """
    )


# ----------------------------
# Comparison
# ----------------------------

def render_comparison():
    st.header("Asset Comparison (Qualitative)")
    st.markdown(
        """
        This is a qualitative comparison intended to show tradeoffs, not to rank assets. The properties are
        based on standard money characteristics and practical market behavior.
        """
    )

    comparison = pd.DataFrame(
        [
            {
                "Asset": "USD",
                "Durable": "Medium",
                "Portable": "High (digital)",
                "Divisible": "High",
                "Verifiable": "Medium",
                "Scarce": "Low",
                "Transparency": "Medium",
                "Counterparty Risk": "High",
            },
            {
                "Asset": "Stocks",
                "Durable": "High",
                "Portable": "High (digital)",
                "Divisible": "Medium",
                "Verifiable": "Medium",
                "Scarce": "Medium",
                "Transparency": "Medium",
                "Counterparty Risk": "Medium",
            },
            {
                "Asset": "Real Estate",
                "Durable": "High",
                "Portable": "Low",
                "Divisible": "Low",
                "Verifiable": "Medium",
                "Scarce": "Medium",
                "Transparency": "Low",
                "Counterparty Risk": "Medium",
            },
            {
                "Asset": "Bitcoin",
                "Durable": "High",
                "Portable": "High",
                "Divisible": "High",
                "Verifiable": "High",
                "Scarce": "High",
                "Transparency": "High",
                "Counterparty Risk": "Low (self-custody)",
            },
        ]
    )

    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.markdown("### Interpretation")
    st.markdown(
        """
        - Bitcoin scores highest on portability, verifiability, and scarcity.
        - USD is extremely portable but lacks hard scarcity.
        - Real estate is durable but illiquid and hard to divide.
        - Stocks can be liquid but depend on corporate and regulatory structures.
        """
    )


# ----------------------------
# On-chain data
# ----------------------------

@st.cache_data(ttl=3600)
def fetch_blockchain_chart(chart: str, timespan: str = "1year"):
    url = f"{BLOCKCHAIN_API}/{chart}?timespan={timespan}&format=json"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()

    values = payload.get("values", [])
    df = pd.DataFrame(values)
    if not df.empty:
        df["date"] = pd.to_datetime(df["x"], unit="s")
        df = df.rename(columns={"y": payload.get("name", chart)})
    return payload, df


def render_onchain():
    st.header("On-Chain Signals")

    st.markdown(
        """
        These metrics are pulled from public blockchain data. They are network activity proxies, not
        direct measures of users or adoption.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Active addresses (last 1Y)")
        try:
            meta, df = fetch_blockchain_chart("n-unique-addresses", "1year")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df[df.columns[1]],
                    mode="lines",
                    name="Active addresses",
                )
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                yaxis=dict(tickformat=".2s"),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption(meta.get("description", "Unique addresses used on the network."))
        except Exception:
            st.warning("Unable to load active address data right now.")

    with col2:
        st.subheader("Transactions per day (last 1Y)")
        try:
            meta, df = fetch_blockchain_chart("n-transactions", "1year")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df[df.columns[1]],
                    mode="lines",
                    name="Transactions",
                )
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                yaxis=dict(tickformat=".2s"),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption(meta.get("description", "Confirmed transactions per day."))
        except Exception:
            st.warning("Unable to load transaction data right now.")

    st.subheader("Estimated transaction volume (USD, last 1Y)")
    try:
        meta, df = fetch_blockchain_chart("estimated-transaction-volume-usd", "1year")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df[df.columns[1]],
                mode="lines",
                name="USD volume",
            )
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis=dict(tickformat=".2s"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(meta.get("description", "Estimated transaction volume in USD."))
    except Exception:
        st.warning("Unable to load transaction volume data right now.")

    st.subheader("YoY growth in active addresses (proxy, 5Y)")
    st.caption(
        "This uses unique active addresses as a proxy for user growth. It is not the same as unique users."
    )
    try:
        _, df = fetch_blockchain_chart("n-unique-addresses", "5years")
        df = df.set_index("date").resample("Y").mean()
        df["YoY %"] = df.iloc[:, 0].pct_change() * 100
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df.index.year.astype(str),
                y=df["YoY %"],
                name="YoY %",
            )
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis=dict(tickformat=".2s"),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.warning("Unable to compute YoY growth from active addresses.")

    st.subheader("Compare with USD online transaction volume")
    st.markdown(
        """
        Upload a CSV with `date` and `value` columns (daily or monthly) to compare
        Bitcoin on-chain volume with another payment dataset.
        """
    )
    uploaded = st.file_uploader("Upload comparison CSV", type=["csv"])
    if uploaded:
        try:
            external = pd.read_csv(uploaded)
            external["date"] = pd.to_datetime(external["date"])
            external = external.rename(columns={"value": "External Volume"})

            _, btc = fetch_blockchain_chart("estimated-transaction-volume-usd", "1year")
            btc = btc.rename(columns={btc.columns[1]: "Bitcoin Volume"})

            merged = pd.merge(btc[["date", "Bitcoin Volume"]], external[["date", "External Volume"]], on="date", how="inner")
            if merged.empty:
                st.warning("No matching dates found between the two datasets.")
            else:
                st.line_chart(merged.set_index("date"))
        except Exception:
            st.warning("Failed to parse the CSV. Ensure it has `date` and `value` columns.")

    st.markdown("### Metrics that require premium data sources")
    st.markdown(
        """
        - Wallets holding BTC (non-zero addresses)
        - Holding period distribution (short vs long-term holders)
        - New user growth (first-time active addresses)
        """
    )
    st.info(
        "If you want these metrics, we can plug in Glassnode, Coin Metrics, or Blockworks APIs once keys are available."
    )


# ----------------------------
# Merchant adoption map
# ----------------------------

@st.cache_data(ttl=21600)
def geocode_country(country_name: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "limit": 1,
        "q": country_name,
        "addressdetails": 1,
        "accept-language": "en",
        "extratags": 1,
    }
    headers = {"User-Agent": "BitcoinSignalHub/1.0"}
    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    results = response.json()
    if not results:
        return None
    return results[0]


def _area_id(osm_type: str, osm_id: int):
    if osm_type == "relation":
        return 3600000000 + int(osm_id)
    if osm_type == "way":
        return 2400000000 + int(osm_id)
    return None


def _overpass_query_area(area_id: int, include_legacy: bool):
    legacy_clause = ""
    if include_legacy:
        legacy_clause = """
      node["payment:bitcoin"="yes"](area.searchArea);
      way["payment:bitcoin"="yes"](area.searchArea);
      relation["payment:bitcoin"="yes"](area.searchArea);
        """
    return f"""
    [out:json][timeout:50];
    area({area_id})->.searchArea;
    (
      node["currency:XBT"="yes"](area.searchArea);
      way["currency:XBT"="yes"](area.searchArea);
      relation["currency:XBT"="yes"](area.searchArea);
      node["payment:onchain"="yes"](area.searchArea);
      way["payment:onchain"="yes"](area.searchArea);
      relation["payment:onchain"="yes"](area.searchArea);
      node["payment:lightning"="yes"](area.searchArea);
      way["payment:lightning"="yes"](area.searchArea);
      relation["payment:lightning"="yes"](area.searchArea);
      node["payment:lightning_contactless"="yes"](area.searchArea);
      way["payment:lightning_contactless"="yes"](area.searchArea);
      relation["payment:lightning_contactless"="yes"](area.searchArea);
      {legacy_clause}
    );
    out center tags;
    """


def _overpass_query_bbox(south: float, west: float, north: float, east: float, include_legacy: bool):
    legacy_clause = ""
    if include_legacy:
        legacy_clause = f"""
      node["payment:bitcoin"="yes"]({south},{west},{north},{east});
      way["payment:bitcoin"="yes"]({south},{west},{north},{east});
      relation["payment:bitcoin"="yes"]({south},{west},{north},{east});
        """
    return f"""
    [out:json][timeout:50];
    (
      node["currency:XBT"="yes"]({south},{west},{north},{east});
      way["currency:XBT"="yes"]({south},{west},{north},{east});
      relation["currency:XBT"="yes"]({south},{west},{north},{east});
      node["payment:onchain"="yes"]({south},{west},{north},{east});
      way["payment:onchain"="yes"]({south},{west},{north},{east});
      relation["payment:onchain"="yes"]({south},{west},{north},{east});
      node["payment:lightning"="yes"]({south},{west},{north},{east});
      way["payment:lightning"="yes"]({south},{west},{north},{east});
      relation["payment:lightning"="yes"]({south},{west},{north},{east});
      node["payment:lightning_contactless"="yes"]({south},{west},{north},{east});
      way["payment:lightning_contactless"="yes"]({south},{west},{north},{east});
      relation["payment:lightning_contactless"="yes"]({south},{west},{north},{east});
      {legacy_clause}
    );
    out center tags;
    """


def _call_overpass(query: str):
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://overpass.nchc.org.tw/api/interpreter",
    ]
    payload = None
    last_error = None
    for endpoint in endpoints:
        try:
            response = requests.post(
                endpoint,
                data=query.encode("utf-8"),
                headers={"User-Agent": "BitcoinSignalHub/1.0"},
                timeout=90,
            )
            response.raise_for_status()
            payload = response.json()
            break
        except Exception as exc:
            last_error = exc
            continue
    if payload is None:
        raise RuntimeError(f"Overpass query failed: {last_error}")
    return payload


def _elements_to_rows(elements, fallback_country: str):
    rows = []
    seen = set()
    for el in elements:
        key = (el.get("type"), el.get("id"))
        if key in seen:
            continue
        seen.add(key)

        if el.get("type") == "node":
            lat = el.get("lat")
            lon = el.get("lon")
        else:
            center = el.get("center") or {}
            lat = center.get("lat")
            lon = center.get("lon")

        if lat is None or lon is None:
            continue

        tags = el.get("tags", {})
        rows.append(
            {
                "name": tags.get("name", "Unknown"),
                "lat": lat,
                "lon": lon,
                "city": tags.get("addr:city") or tags.get("city"),
                "state": tags.get("addr:state") or tags.get("addr:province"),
                "country": tags.get("addr:country") or fallback_country,
                "category": tags.get("amenity") or tags.get("shop") or tags.get("tourism"),
                "source": "OpenStreetMap tags",
            }
        )

    return rows


@st.cache_data(ttl=21600)
def fetch_merchants_for_country(country_name: str, include_legacy: bool):
    geo = geocode_country(country_name)
    if not geo:
        raise RuntimeError("Country not found in geocoder.")

    bbox = geo.get("boundingbox")
    if bbox and len(bbox) == 4:
        south, north, west, east = map(float, bbox)
    else:
        south = north = west = east = None

    area_id = _area_id(geo["osm_type"], geo["osm_id"])

    elements = []
    if area_id is not None:
        query = _overpass_query_area(area_id, include_legacy)
        payload = _call_overpass(query)
        elements = payload.get("elements", [])

    if not elements and None not in (south, north, west, east):
        # Large countries often fail in a single area query. Split into a 3x3 grid.
        lat_span = abs(north - south)
        lon_span = abs(east - west)
        grid = 3 if (lat_span * lon_span) > 200 else 2

        lat_step = (north - south) / grid
        lon_step = (east - west) / grid
        for i in range(grid):
            for j in range(grid):
                s = south + i * lat_step
                n = south + (i + 1) * lat_step
                w = west + j * lon_step
                e = west + (j + 1) * lon_step
                query = _overpass_query_bbox(s, w, n, e, include_legacy)
                payload = _call_overpass(query)
                elements.extend(payload.get("elements", []))

    return _elements_to_rows(elements, geo.get("display_name", country_name))


def render_merchants():
    st.header("Merchant Adoption Map")
    st.markdown(
        "Explore Bitcoin-accepting merchants by country. Data is pulled from OpenStreetMap tags "
        "used by BTC Map and refreshed on demand."
    )
    st.caption(
        "We query OSM tags like currency:XBT and payment:onchain/lightning; payment:bitcoin is legacy and optional."
    )

    with st.form("merchant_search"):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            country = st.text_input("Country", value="United States")
        with col2:
            region = st.text_input("State/Province (optional)", value="")
        with col3:
            max_points = st.slider("Max map points", 200, 2000, 800, step=100)
        st.caption(
            "Tip: For large countries like the U.S., add a state/province for faster and more reliable results."
        )
        include_legacy = st.checkbox(
            "Include legacy payment:bitcoin tag",
            value=True,
            help="Legacy tags increase coverage but may include outdated entries.",
        )
        view_mode = st.selectbox(
            "View mode",
            ["Summary (state-level)", "Drilldown (merchant-level)"],
        )
        submitted = st.form_submit_button("Load merchants")

    if not submitted:
        st.caption("Enter a country (and optionally a state/province) then click Load merchants.")
        return

    if not country.strip():
        st.warning("Enter a country name to load merchants.")
        return

    query_name = country.strip()
    if region.strip():
        query_name = f"{region.strip()}, {country.strip()}"

    with st.spinner("Fetching merchant data..."):
        try:
            rows = fetch_merchants_for_country(query_name, include_legacy)
        except Exception as exc:
            st.error(f"Failed to load merchants: {exc}")
            st.info(
                "If the country is large (e.g., United States), try adding a state/province for faster results."
            )
            return

    if not rows:
        st.warning("No merchants found for this area.")
        st.info(
            "Try adding a state/province or enabling legacy tags to improve coverage."
        )
        return

    df = pd.DataFrame(rows)
    if len(df) > max_points:
        df = df.sample(max_points, random_state=42)

    st.caption(f"{format_compact(len(rows))} locations retrieved before sampling.")

    if view_mode == "Summary (state-level)":
        st.subheader(f"State-level adoption: {query_name}")
        state_counts = df["state"].dropna().value_counts()
        if state_counts.empty:
            st.warning("State-level tags are missing. Switch to Drilldown for merchant map.")
        else:
            summary = state_counts.rename_axis("state").reset_index(name="count")
            summary["country"] = country.strip()
            summary = summary.head(50)

            state_points = []
            for _, row in summary.iterrows():
                state_geo = geocode_country(f"{row['state']}, {row['country']}")
                if not state_geo:
                    continue
                try:
                    state_points.append(
                        {
                            "state": row["state"],
                            "count": int(row["count"]),
                            "lat": float(state_geo["lat"]),
                            "lon": float(state_geo["lon"]),
                        }
                    )
                except Exception:
                    continue

            if not state_points:
                st.warning("Unable to geocode state centroids. Use Drilldown mode.")
            else:
                points_df = pd.DataFrame(state_points)
                max_count = points_df["count"].max()
                points_df["radius"] = points_df["count"].apply(
                    lambda c: 20000 + (c / max_count) * 60000
                )

                import pydeck as pdk

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=points_df,
                    get_position="[lon, lat]",
                    get_radius="radius",
                    get_fill_color="[209, 136, 47, 160]",
                    pickable=True,
                )

                view_state = pdk.ViewState(
                    latitude=points_df["lat"].mean(),
                    longitude=points_df["lon"].mean(),
                    zoom=3.2,
                )

                st.pydeck_chart(
                    pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        tooltip={"text": "{state}\\nMerchants: {count}"},
                    )
                )

            st.subheader("Top states by merchant count")
            summary_display = summary.rename(
                columns={"state": "State", "count": "Merchants"}
            )
            summary_display["Merchants"] = summary_display["Merchants"].apply(
                format_compact
            )
            st.dataframe(summary_display, use_container_width=True)

            st.subheader("Drill down")
            selected_state = st.selectbox(
                "Select a state to drill down",
                ["All"] + summary["state"].tolist(),
            )
            if selected_state != "All":
                df = df[df["state"] == selected_state]

    if view_mode == "Drilldown (merchant-level)":
        st.subheader(f"Merchant map: {query_name}")
        st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    st.subheader("Counts by state/region (if tagged)")
    state_counts = df["state"].dropna().value_counts().head(15)
    if state_counts.empty:
        st.caption("No state-level tags found for this country.")
    else:
        state_df = state_counts.rename_axis("State").to_frame("Merchants")
        state_df["Merchants"] = state_df["Merchants"].apply(format_compact)
        st.dataframe(state_df, use_container_width=True)

    st.subheader("Counts by city (if tagged)")
    city_counts = df["city"].dropna().value_counts().head(20)
    if city_counts.empty:
        st.caption("No city-level tags found for this country.")
    else:
        city_df = city_counts.rename_axis("City").to_frame("Merchants")
        city_df["Merchants"] = city_df["Merchants"].apply(format_compact)
        st.dataframe(city_df, use_container_width=True)

    st.subheader("Filter by city or state")
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.selectbox("City", ["All"] + sorted(df["city"].dropna().unique().tolist()))
    with col2:
        state_filter = st.selectbox("State/Region", ["All"] + sorted(df["state"].dropna().unique().tolist()))

    filtered = df.copy()
    if city_filter != "All":
        filtered = filtered[filtered["city"] == city_filter]
    if state_filter != "All":
        filtered = filtered[filtered["state"] == state_filter]

    st.caption(f"{format_compact(len(filtered))} locations match filters.")
    st.dataframe(
        filtered[["name", "category", "city", "state"]].head(200),
        use_container_width=True,
    )


# ----------------------------
# Daily brief
# ----------------------------

def render_brief():
    st.header("Daily Brief")

    st.markdown(
        """
        A quick read based on the latest on-chain activity and headlines.
        """
    )

    metrics = [
        ("n-unique-addresses", "Active addresses"),
        ("n-transactions", "Transactions"),
        ("estimated-transaction-volume-usd", "Txn volume (USD)"),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for idx, (chart, label) in enumerate(metrics):
        with cols[idx]:
            try:
                _, df = fetch_blockchain_chart(chart, "30days")
                df = df.sort_values("date")
                latest = df.iloc[-1, 1]
                previous = df.iloc[-8, 1] if len(df) > 8 else df.iloc[0, 1]
                delta = latest - previous
                st.metric(
                    label,
                    format_compact(latest),
                    delta=f"{format_compact(delta)} vs 7d",
                )
            except Exception:
                st.metric(label, "--")

    st.markdown("### News Brief (Daily)")
    def parse_rss_fallback(url: str):
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        items = root.findall(".//item")
        results = []
        for item in items[:10]:
            title = item.findtext("title") or ""
            link = item.findtext("link") or ""
            published = item.findtext("pubDate") or item.findtext("published") or ""
            results.append({"title": title, "link": link, "published": published})
        return results

    sources = {
        "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    }

    selected = st.multiselect(
        "Select news sources:",
        list(sources.keys()),
        default=["CoinDesk"],
    )

    headlines = []
    for name in selected:
        if feedparser is not None:
            feed = feedparser.parse(sources[name])
            for entry in feed.entries[:10]:
                headlines.append(
                    {
                        "source": name,
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    }
                )
        else:
            try:
                entries = parse_rss_fallback(sources[name])
                for entry in entries:
                    entry["source"] = name
                    headlines.append(entry)
            except Exception:
                continue

    if not headlines:
        st.warning("No headlines available. The feed may be blocked or unavailable.")
        return

    st.markdown("#### Top headlines")
    for item in headlines[:8]:
        title = " ".join((item.get("title") or "").split())
        link = item.get("link") or ""
        if link:
            st.markdown(f"- [{title}]({link})")
        else:
            st.markdown(f"- {title}")

    st.markdown("#### Theme signals")
    keywords = extract_keywords([h["title"] for h in headlines])
    if keywords:
        st.write(", ".join([kw for kw, _ in keywords[:10]]))
    else:
        st.write("No dominant themes yet.")


def extract_keywords(titles):
    stopwords = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "is",
        "are",
        "was",
        "were",
        "be",
        "this",
        "that",
        "it",
        "its",
        "bitcoin",
        "btc",
    }

    tokens = []
    for title in titles:
        words = [w.strip(".,:;()[]\"'!?/") for w in title.lower().split()]
        tokens.extend([w for w in words if w and w not in stopwords and len(w) > 2])

    return Counter(tokens).most_common(20)
