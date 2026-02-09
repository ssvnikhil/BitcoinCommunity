import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def show_content():
    st.title("Bitcoin: Digital Hard Money")

    if "quiz_scores_advanced" not in st.session_state:
        st.session_state.quiz_scores_advanced = {
            "page1": 0,
            "page2": 0,
            "page3": 0,
            "page4": 0,
        }

    pages = {
        1: page_digital_scarcity,
        2: page_monetary_policy,
        3: page_sovereignty,
        4: page_scaling,
    }

    st.markdown("### Module Navigation")
    page = st.radio(
        "",
        [
            "1. Digital Scarcity",
            "2. Monetary Policy",
            "3. Sovereignty and Immutability",
            "4. Scaling and Tradeoffs",
        ],
        horizontal=True,
        label_visibility="collapsed",
        index=0,
    )

    current_page = int(page[0])

    progress = sum(st.session_state.quiz_scores_advanced.values()) / (
        len(st.session_state.quiz_scores_advanced) * 100
    )
    st.markdown("### Your Progress")
    st.progress(progress)

    pages[current_page]()

    st.markdown("---")
    st.markdown("### References")
    st.markdown(
        """
        - Bitcoin: A Peer-to-Peer Electronic Cash System (Satoshi)
        - Mastering Bitcoin (Antonopoulos)
        - Grokking Bitcoin (Song)
        """
    )


def page_digital_scarcity():
    st.header("Digital Scarcity")

    st.markdown(
        """
        Digital files can be copied for free. Bitcoin solved this by creating a ledger that
        makes double spending economically expensive and publicly verifiable.
        """
    )

    st.subheader("Double-spending comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Ordinary digital files**
            1. Create file
            2. Copy file
            3. Send copy 1
            4. Send copy 2
            Result: double spend possible
            """
        )

    with col2:
        st.markdown(
            """
            **Bitcoin**
            1. Create transaction
            2. Broadcast to network
            3. Miners verify and confirm
            4. Second spend attempt rejected
            Result: double spend prevented
            """
        )

    st.subheader("Proof-of-work simulator")
    target_difficulty = st.slider("Mining difficulty (leading zeros)", 1, 5, 3)
    nonce = st.number_input("Try a nonce value", 0, 1_000_000, 0)

    import hashlib

    data = f"Bitcoin block {nonce}"
    hash_result = hashlib.sha256(data.encode()).hexdigest()

    st.code(f"Hash: {hash_result}")
    if hash_result.startswith("0" * target_difficulty):
        st.success("Valid hash found. Block would be accepted.")
    else:
        st.error("Invalid hash. Try another nonce value.")

    st.subheader("Security vs hash power (illustrative)")
    hash_power = st.slider("Network hash power (EH/s)", 1, 500, 300)
    security_level = min(100, hash_power / 5)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=security_level,
            title={"text": "Network security level"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 33], "color": "#e15759"},
                    {"range": [33, 66], "color": "#f28e2b"},
                    {"range": [66, 100], "color": "#59a14f"},
                ],
            },
        )
    )
    st.plotly_chart(fig)

    st.markdown("### Quick check")
    quiz = st.radio(
        "What makes Bitcoin the first successful digital cash system?",
        [
            "It is faster than banking",
            "It solves double spending without intermediaries",
            "It is backed by government",
            "It is easier to use than cash",
        ],
    )

    if st.button("Check answer", key="check1"):
        if quiz == "It solves double spending without intermediaries":
            st.success("Correct. The core innovation is decentralized consensus.")
            st.session_state.quiz_scores_advanced["page1"] = 100
        else:
            st.error("Try again. Focus on the double-spend problem.")
            st.session_state.quiz_scores_advanced["page1"] = 0


def page_monetary_policy():
    st.header("Bitcoin Monetary Policy")

    st.markdown(
        """
        Bitcoin's supply schedule is predetermined and enforced by consensus.
        The block reward halves roughly every four years.
        """
    )

    st.subheader("Supply schedule (approximate)")
    years = np.arange(2009, 2141)
    max_supply = 21_000_000

    def bitcoin_supply(year):
        halving_events = max(0, (year - 2009) // 4)
        initial_reward = 50
        blocks_per_year = 52_560
        return min(
            max_supply,
            sum(
                blocks_per_year * initial_reward / (2**h)
                for h in range(halving_events + 1)
            ),
        )

    supply = [bitcoin_supply(year) for year in years]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=supply, name="Bitcoin supply"))
    fig.update_layout(
        title="Bitcoin supply over time (approximate)",
        yaxis_title="Total bitcoins",
        xaxis_title="Year",
    )
    st.plotly_chart(fig)

    st.subheader("Halving estimator")
    current_year = datetime.utcnow().year
    halvings = max(0, (current_year - 2009) // 4)
    current_reward = 50 / (2**halvings)

    st.markdown(
        """
        This is a simple year-based estimator. Real halving dates are based on block height.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated current block reward", f"{current_reward:.4f} BTC")
    with col2:
        st.metric("Next reward (approx)", f"{current_reward / 2:.4f} BTC")

    st.subheader("Stock-to-flow comparison (illustrative)")
    assets = {
        "Bitcoin": 90,
        "Gold": 60,
        "Silver": 20,
        "Oil": 1,
    }

    fig = go.Figure([go.Bar(x=list(assets.keys()), y=list(assets.values()))])
    fig.update_layout(
        title="Relative stock-to-flow (illustrative)",
        yaxis_title="Relative ratio",
    )
    st.plotly_chart(fig)

    st.markdown("### Quick check")
    quiz = st.radio(
        "What makes Bitcoin's supply schedule unique?",
        [
            "It can be changed by developers",
            "It increases based on demand",
            "It has an absolute maximum supply of 21 million",
            "It is controlled by miners",
        ],
    )

    if st.button("Check answer", key="check2"):
        if quiz == "It has an absolute maximum supply of 21 million":
            st.success("Correct. Bitcoin enforces absolute scarcity.")
            st.session_state.quiz_scores_advanced["page2"] = 100
        else:
            st.error("Try again. Focus on the hard cap.")
            st.session_state.quiz_scores_advanced["page2"] = 0


def page_sovereignty():
    st.header("Sovereignty and Immutability")

    st.markdown(
        """
        Bitcoin gives users direct control of value through private keys.
        It also makes protocol changes extremely difficult without broad consensus.
        """
    )

    st.subheader("Key custody comparison")
    storage_method = st.selectbox(
        "Choose a storage method:",
        ["Exchange Wallet", "Software Wallet", "Hardware Wallet", "Paper Wallet"],
    )

    control_levels = {
        "Exchange Wallet": ("Low", "Exchange controls keys"),
        "Software Wallet": ("Medium", "You control keys, but online"),
        "Hardware Wallet": ("High", "You control keys with offline security"),
        "Paper Wallet": ("High", "You control keys with physical backup"),
    }

    level, description = control_levels[storage_method]
    st.info(f"Sovereignty level: {level}. {description}.")

    st.subheader("Protocol change consensus")
    stakeholders = ["Miners", "Node operators", "Developers", "Users", "Businesses"]
    agreement = st.multiselect("Stakeholders who agree:", stakeholders)

    consensus_level = len(agreement) / len(stakeholders) * 100

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=consensus_level,
            title={"text": "Consensus level"},
            gauge={
                "axis": {"range": [0, 100]},
                "threshold": {
                    "line": {"color": "#e15759", "width": 4},
                    "thickness": 0.75,
                    "value": 95,
                },
            },
        )
    )
    st.plotly_chart(fig)

    if consensus_level < 95:
        st.error("Insufficient consensus. Change rejected.")
    else:
        st.success("Strong consensus achieved.")

    st.markdown("### Quick check")
    quiz = st.radio(
        "What makes Bitcoin immutable?",
        [
            "Government regulations",
            "Developer decisions",
            "Distributed consensus and incentives",
            "Mining hardware",
        ],
    )

    if st.button("Check answer", key="check3"):
        if quiz == "Distributed consensus and incentives":
            st.success("Correct. Immutability emerges from incentives and consensus.")
            st.session_state.quiz_scores_advanced["page3"] = 100
        else:
            st.error("Try again. Focus on consensus and incentives.")
            st.session_state.quiz_scores_advanced["page3"] = 0


def page_scaling():
    st.header("Scaling and Tradeoffs")

    st.markdown(
        """
        Bitcoin prioritizes decentralization and security. Scaling requires tradeoffs
        that must preserve those properties.
        """
    )

    st.subheader("Scaling trilemma")
    decentralization = st.slider("Decentralization", 0, 100, 80)
    security = st.slider("Security", 0, 100, 80)
    scalability = 300 - decentralization - security

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=[decentralization, security, max(0, scalability)],
            theta=["Decentralization", "Security", "Scalability"],
            fill="toself",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
    )
    st.plotly_chart(fig)

    if scalability < 0:
        st.warning("These settings are impossible. Adjust the tradeoffs.")

    st.subheader("Layer 2 solutions")
    solution = st.selectbox(
        "Explore a scaling approach:",
        ["Lightning Network", "Sidechains", "Payment Channels"],
    )

    solutions_info = {
        "Lightning Network": {
            "Speed": "Instant",
            "Cost": "Very low",
            "Scale": "High",
            "Security": "High",
        },
        "Sidechains": {
            "Speed": "Fast",
            "Cost": "Low",
            "Scale": "High",
            "Security": "Medium",
        },
        "Payment Channels": {
            "Speed": "Instant",
            "Cost": "Very low",
            "Scale": "High",
            "Security": "High",
        },
    }

    for metric, value in solutions_info[solution].items():
        st.markdown(f"**{metric}**: {value}")

    st.subheader("Database comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Traditional database**
            - High throughput
            - Low cost
            - Easy to modify
            - Requires trust
            """
        )

    with col2:
        st.markdown(
            """
            **Blockchain**
            - Limited throughput
            - Higher cost
            - Hard to modify
            - Trustless
            """
        )

    st.markdown("### Quick check")
    quiz = st.radio(
        "Why is blockchain not suitable for most applications?",
        [
            "It is too new",
            "It is too complex",
            "Its inefficiency is only justified for trustless money",
            "It is too expensive to develop",
        ],
    )

    if st.button("Check answer", key="check4"):
        if quiz == "Its inefficiency is only justified for trustless money":
            st.success("Correct. The costs make sense only when trust elimination is vital.")
            st.session_state.quiz_scores_advanced["page4"] = 100
        else:
            st.error("Try again. Focus on the tradeoff.")
            st.session_state.quiz_scores_advanced["page4"] = 0
