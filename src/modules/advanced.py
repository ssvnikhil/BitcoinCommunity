import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_content():
    st.title("🌳 Bitcoin: Digital Hard Money")
    
    if 'quiz_scores_advanced' not in st.session_state:
        st.session_state.quiz_scores_advanced = {
            'page1': 0,
            'page2': 0,
            'page3': 0,
            'page4': 0
        }

    # Navigation
    pages = {
        1: page_digital_scarcity,
        2: page_monetary_policy,
        3: page_sovereignty,
        4: page_scaling
    }

    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Select a topic:",
        ["1. Digital Scarcity",
         "2. Monetary Policy",
         "3. Sovereignty & Immutability",
         "4. Scaling & Blockchain"],
        index=0
    )
    
    current_page = int(page[0])
    
    # Progress tracking
    progress = sum(st.session_state.quiz_scores_advanced.values()) / (len(st.session_state.quiz_scores_advanced) * 100)
    st.sidebar.markdown("### Your Progress")
    st.sidebar.progress(progress)
    
    # Display current page
    pages[current_page]()

def page_digital_scarcity():
    st.header("💎 Bitcoin: The First Digital Solution to Scarcity")
    
    # Digital Cash Problem Visualization
    st.subheader("🔄 The Double Spending Problem")
    
    # Interactive demonstration of double spending
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Traditional Digital Files")
        st.markdown("""
        1. Create digital token
        2. Copy file ✅
        3. Send copy 1 ✅
        4. Send copy 2 ✅
        5. **Result**: Double spending possible!
        """)
        
    with col2:
        st.markdown("### Bitcoin Solution")
        st.markdown("""
        1. Create transaction
        2. Broadcast to network
        3. Miners verify & confirm
        4. Second spend attempt ❌
        5. **Result**: Double spending prevented!
        """)

    # Proof of Work Simulation
    st.subheader("⛏️ Proof of Work Simulator")
    
    target_difficulty = st.slider("Mining Difficulty (number of leading zeros):", 1, 5, 3)
    nonce = st.number_input("Try a nonce value:", 0, 1000000, 0)
    
    import hashlib
    
    data = f"Bitcoin block {nonce}"
    hash_result = hashlib.sha256(data.encode()).hexdigest()
    
    st.code(f"Hash: {hash_result}")
    if hash_result.startswith('0' * target_difficulty):
        st.success("🎉 Valid hash found! Block would be added to the chain.")
    else:
        st.error("❌ Invalid hash. Try another nonce value.")

    # Mining Security Visualization
    st.subheader("🔒 Network Security vs. Hash Power")
    
    hash_power = st.slider("Total Network Hash Power (EH/s):", 1, 500, 350)
    
    security_level = hash_power / 5  # Simplified security metric
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = security_level,
        title = {'text': "Network Security Level"},
        gauge = {'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 33], 'color': "red"},
                    {'range': [33, 66], 'color': "yellow"},
                    {'range': [66, 100], 'color': "green"}]}))
    
    st.plotly_chart(fig)

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What makes Bitcoin the first successful digital cash system?",
        ["It's faster than traditional banking",
         "It solves the double-spending problem without intermediaries",
         "It's backed by government",
         "It's easier to use than cash"]
    )
    
    if st.button("Check Answer", key="check1"):
        if quiz == "It solves the double-spending problem without intermediaries":
            st.success("🎉 Correct! Bitcoin is revolutionary because it prevents double-spending without requiring trust in a third party.")
            st.session_state.quiz_scores_advanced['page1'] = 100
        else:
            st.error("Try again! Think about the core innovation of Bitcoin.")
            st.session_state.quiz_scores_advanced['page1'] = 0

def page_monetary_policy():
    st.header("📊 Bitcoin's Monetary Policy")
    
    # Supply Schedule Visualization
    st.subheader("🔮 Bitcoin Supply Schedule")
    
    years = np.arange(2009, 2141)
    max_supply = 21_000_000
    
    def bitcoin_supply(year):
        halving_events = (year - 2009) // 4
        initial_reward = 50
        current_reward = initial_reward / (2 ** halving_events)
        blocks_per_year = 52560
        return min(max_supply, sum(blocks_per_year * initial_reward / (2 ** h) 
                                 for h in range(halving_events + 1)))
    
    supply = [bitcoin_supply(year) for year in years]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=supply, name="Bitcoin Supply"))
    fig.update_layout(title="Bitcoin Supply Over Time",
                     yaxis_title="Total Bitcoins",
                     xaxis_title="Year")
    st.plotly_chart(fig)
    
    # Halving Countdown Simulator
    current_reward = 6.25
    next_halving = "2024"
    
    st.subheader("⚡ Next Halving Event")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Block Reward", f"{current_reward} BTC")
    with col2:
        st.metric("Next Block Reward", f"{current_reward/2} BTC")
    with col3:
        st.metric("Estimated Date", next_halving)

    # Stock-to-Flow Comparison
    st.subheader("📈 Stock-to-Flow Ratio Comparison")
    
    assets = {
        "Bitcoin (2025)": 120,
        "Gold": 62,
        "Silver": 22,
        "Platinum": 15,
        "Oil": 0.4
    }
    
    fig = go.Figure([go.Bar(x=list(assets.keys()), y=list(assets.values()))])
    fig.update_layout(title="Stock-to-Flow Ratios",
                     yaxis_title="Stock-to-Flow Ratio")
    st.plotly_chart(fig)

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What makes Bitcoin's supply schedule unique?",
        ["It can be changed by developers",
         "It increases based on demand",
         "It has an absolute maximum supply of 21 million",
         "It's controlled by miners"]
    )
    
    if st.button("Check Answer", key="check2"):
        if quiz == "It has an absolute maximum supply of 21 million":
            st.success("🎉 Correct! Bitcoin is the first example of absolute scarcity in monetary history.")
            st.session_state.quiz_scores_advanced['page2'] = 100
        else:
            st.error("Try again! Think about Bitcoin's unique supply characteristics.")
            st.session_state.quiz_scores_advanced['page2'] = 0

def page_sovereignty():
    st.header("🛡️ Sovereignty and Immutability")
    
    # Sovereignty Demonstration
    st.subheader("🔑 Private Key Sovereignty")
    
    st.markdown("""
    ### Not your keys, not your coins!
    
    Simulate different storage methods:
    """)
    
    storage_method = st.selectbox(
        "Choose a storage method:",
        ["Exchange Wallet", "Software Wallet", "Hardware Wallet", "Paper Wallet"]
    )
    
    control_levels = {
        "Exchange Wallet": ("Low", "Exchange controls keys", "❌"),
        "Software Wallet": ("Medium", "You control keys but connected to internet", "⚠️"),
        "Hardware Wallet": ("High", "You control keys with offline security", "✅"),
        "Paper Wallet": ("High", "You control keys with physical backup", "✅")
    }
    
    level, description, icon = control_levels[storage_method]
    st.info(f"{icon} Sovereignty Level: {level}\n\n{description}")

    # Hard Fork Simulator
    st.subheader("🔱 Hard Fork Demonstration")
    
    st.markdown("### Network Consensus Rules")
    
    proposed_change = st.selectbox(
        "Select a proposed protocol change:",
        ["Increase Block Size", "Change Total Supply", "Modify Block Time", "Add New Feature"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original Chain")
        st.markdown("""
        - ✅ Maintains existing rules
        - ✅ Keeps network effect
        - ✅ Preserves decentralization
        """)
        
    with col2:
        st.markdown("### Fork Chain")
        st.markdown("""
        - ❌ New untested rules
        - ❌ Smaller network
        - ❌ Less security
        """)

    # Immutability Visualization
    st.subheader("🏛️ Protocol Change Difficulty")
    
    stakeholders = ["Miners", "Node Operators", "Developers", "Users", "Businesses"]
    agreement = st.multiselect("Select stakeholders who agree to change:", stakeholders)
    
    consensus_level = len(agreement) / len(stakeholders) * 100
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = consensus_level,
        title = {'text': "Consensus Level"},
        gauge = {'axis': {'range': [0, 100]},
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}))
    
    st.plotly_chart(fig)
    
    if consensus_level < 95:
        st.error("❌ Insufficient consensus - Change rejected!")
    else:
        st.success("✅ Strong consensus achieved!")

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What makes Bitcoin immutable?",
        ["Government regulations",
         "Developer decisions",
         "Distributed consensus and economic incentives",
         "Mining hardware"]
    )
    
    if st.button("Check Answer", key="check3"):
        if quiz == "Distributed consensus and economic incentives":
            st.success("🎉 Correct! Bitcoin's immutability comes from its distributed nature and aligned economic incentives.")
            st.session_state.quiz_scores_advanced['page3'] = 100
        else:
            st.error("Try again! Think about what makes Bitcoin resistant to changes.")
            st.session_state.quiz_scores_advanced['page3'] = 0

def page_scaling():
    st.header("⚡ Scaling and Blockchain Technology")
    
    # Scaling Tradeoffs Visualization
    st.subheader("📊 Scaling Trilemma")
    
    st.markdown("""
    ### The Blockchain Trilemma
    Choose which properties to optimize:
    """)
    
    decentralization = st.slider("Decentralization", 0, 100, 80)
    security = st.slider("Security", 0, 100, 80)
    scalability = 300 - decentralization - security  # Demonstrating the tradeoff
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[decentralization, security, max(0, scalability)],
        theta=['Decentralization', 'Security', 'Scalability'],
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )
    
    st.plotly_chart(fig)
    
    if scalability < 0:
        st.warning("⚠️ These settings are impossible - adjust the tradeoffs!")

    # Layer 2 Scaling Solutions
    st.subheader("⚡ Layer 2 Solutions")
    
    solution = st.selectbox(
        "Explore scaling solutions:",
        ["Lightning Network", "Sidechains", "Payment Channels"]
    )
    
    solutions_info = {
        "Lightning Network": {
            "Speed": "⚡ Instant",
            "Cost": "💰 Very Low",
            "Scale": "📈 Millions TPS",
            "Security": "🔒 High"
        },
        "Sidechains": {
            "Speed": "⚡ Fast",
            "Cost": "💰 Low",
            "Scale": "📈 High",
            "Security": "🔒 Medium"
        },
        "Payment Channels": {
            "Speed": "⚡ Instant",
            "Cost": "💰 Very Low",
            "Scale": "📈 High",
            "Security": "🔒 High"
        }
    }
    
    for metric, value in solutions_info[solution].items():
        st.markdown(f"**{metric}**: {value}")

    # Blockchain Efficiency Comparison
    st.subheader("⚖️ Database Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Traditional Database")
        st.markdown("""
        - ✅ High throughput
        - ✅ Low cost
        - ✅ Easy to modify
        - ❌ Requires trust
        """)
        
    with col2:
        st.markdown("### Blockchain")
        st.markdown("""
        - ❌ Limited throughput
        - ❌ High cost
        - ❌ Hard to modify
        - ✅ Trustless
        """)

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "Why is blockchain technology NOT suitable for most applications?",
        ["It's too new",
         "It's too complex",
         "Its inefficiency is only justified for trustless money",
         "It's too expensive to develop"]
    )
    
    if st.button("Check Answer", key="check4"):
        if quiz == "Its inefficiency is only justified for trustless money":
            st.success("🎉 Correct! Blockchain's inefficiency is only worth it when eliminating trust is essential, as in Bitcoin.")
            st.session_state.quiz_scores_advanced['page4'] = 100
        else:
            st.error("Try again! Think about the tradeoffs of blockchain technology.")
            st.session_state.quiz_scores_advanced['page4'] = 0