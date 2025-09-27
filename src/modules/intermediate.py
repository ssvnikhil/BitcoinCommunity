import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_content():
    st.title("🌿 Unsound Money and Societal Impact")
    
    if 'quiz_scores_intermediate' not in st.session_state:
        st.session_state.quiz_scores_intermediate = {
            'page1': 0,
            'page2': 0,
            'page3': 0,
            'page4': 0
        }

    # Navigation
    pages = {
        1: page_gold_standard_flaw,
        2: page_time_preference,
        3: page_capitalism_business_cycle,
        4: page_sound_money_liberty
    }

    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Select a topic:",
        ["1. Gold Standard & Fiat Money",
         "2. Time Preference & Society",
         "3. Business Cycles",
         "4. Sound Money & Liberty"],
        index=0
    )
    
    current_page = int(page[0])
    
    # Progress tracking
    progress = sum(st.session_state.quiz_scores_intermediate.values()) / (len(st.session_state.quiz_scores_intermediate) * 100)
    st.sidebar.markdown("### Your Progress")
    st.sidebar.progress(progress)
    
    # Display current page
    pages[current_page]()

def page_gold_standard_flaw():
    st.header("💰 The Gold Standard's Fatal Flaw")
    
    # Interactive Timeline
    st.subheader("📅 Timeline of Monetary System Changes")
    
    events = {
        "Pre-1914": "Gold Standard Era - Global unified economy",
        "1914": "WWI Begins - Gold standard suspended",
        "1920s": "Monetary Nationalism emerges",
        "1944": "Bretton Woods System",
        "1971": "End of Gold Standard - Pure Fiat Era begins"
    }
    
    selected_era = st.select_slider(
        "Explore different eras:",
        options=list(events.keys())
    )
    
    st.info(f"**{selected_era}**: {events[selected_era]}")
    
    # Interactive Gold vs Paper Money Simulation
    st.subheader("🏦 Gold Centralization Simulation")
    
    gold_in_vault = st.slider("Percentage of gold stored in central banks:", 0, 100, 50)
    paper_money = st.slider("Paper money issued as percentage of gold reserves:", 100, 300, 100)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Physical Gold", "Paper Claims"],
        y=[100, paper_money],
        name="Money Supply"
    ))
    fig.update_layout(title="Gold Reserves vs Paper Claims")
    st.plotly_chart(fig)
    
    if paper_money > 100:
        st.warning(f"⚠️ Alert: Paper claims exceed physical gold by {paper_money - 100}%!")
        st.markdown("""
        This situation creates:
        1. Risk of bank runs
        2. Debasement of currency
        3. Transfer of purchasing power to issuers
        """)

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What was the fatal flaw in the gold standard system?",
        ["Gold was too heavy to carry",
         "The centralization of gold in banks enabling paper money expansion",
         "Gold was too scarce",
         "Gold was too abundant"]
    )
    
    if st.button("Check Answer", key="check1"):
        if quiz == "The centralization of gold in banks enabling paper money expansion":
            st.success("🎉 Correct! The centralization of gold enabled the expansion of paper claims beyond physical reserves.")
            st.session_state.quiz_scores_intermediate['page1'] = 100
        else:
            st.error("Try again! Think about how the banking system evolved.")
            st.session_state.quiz_scores_intermediate['page1'] = 0

def page_time_preference():
    st.header("⏳ Time Preference and Civilization")
    
    # Interactive Time Preference Calculator
    st.subheader("🎯 Personal Time Preference Calculator")
    
    amount_today = st.number_input("How much would you accept today?", min_value=1, value=100)
    future_days = st.slider("In how many days would you receive the money?", 1, 365, 30)
    
    # Calculate implied time preference
    future_amount = st.number_input("How much would you need to receive in the future to wait?", 
                                  min_value=float(amount_today), value=float(amount_today * 1.1))
    
    annual_rate = ((future_amount/amount_today) ** (365/future_days) - 1) * 100
    
    st.metric("Your Implied Annual Time Preference Rate", f"{annual_rate:.1f}%")
    
    if annual_rate > 20:
        st.warning("You have a relatively high time preference!")
    else:
        st.success("You have a relatively low time preference!")
        
    # Sound vs Unsound Money Effects
    st.subheader("💡 Money Systems Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sound Money Society")
        st.markdown("""
        - ✅ Long-term planning
        - ✅ Capital accumulation
        - ✅ Productive investment
        - ✅ Sustainable growth
        - ✅ Cultural achievements
        """)
        
    with col2:
        st.markdown("### Unsound Money Society")
        st.markdown("""
        - ❌ Short-term thinking
        - ❌ Immediate consumption
        - ❌ Debt accumulation
        - ❌ Economic instability
        - ❌ Cultural decline
        """)
    
    # Interactive Visualization
    st.subheader("📊 Savings Rate Simulation")
    
    years = np.arange(1950, 2025)
    sound_money = 15 + np.random.normal(0, 1, len(years))
    unsound_money = 15 + np.random.normal(0, 1, len(years)) - 0.2 * (years - 1950)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=sound_money, name="Sound Money Economy"))
    fig.add_trace(go.Scatter(x=years, y=unsound_money, name="Unsound Money Economy"))
    fig.update_layout(title="Simulated Savings Rates Over Time",
                     yaxis_title="Savings Rate (%)")
    st.plotly_chart(fig)
    
    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "How does sound money affect time preference?",
        ["It increases time preference",
         "It has no effect on time preference",
         "It lowers time preference",
         "Time preference is unrelated to money"]
    )
    
    if st.button("Check Answer", key="check2"):
        if quiz == "It lowers time preference":
            st.success("🎉 Correct! Sound money encourages long-term thinking and investment.")
            st.session_state.quiz_scores_intermediate['page2'] = 100
        else:
            st.error("Try again! Think about how monetary stability affects planning.")
            st.session_state.quiz_scores_intermediate['page2'] = 0

def page_capitalism_business_cycle():
    st.header("📈 The Business Cycle and Price Signals")
    
    # Price Signal Demonstration
    st.subheader("🎯 Market Price Signal Simulator")
    
    # Simple supply-demand simulator
    supply = st.slider("Supply level:", 0, 100, 50)
    demand = st.slider("Demand level:", 0, 100, 50)
    
    # Calculate market price
    natural_price = 100 * (demand / supply)
    central_bank_intervention = st.checkbox("Apply Central Bank Intervention")
    
    if central_bank_intervention:
        artificial_price = natural_price * 0.7  # Artificial suppression
        st.metric("Market Price", f"${artificial_price:.2f}", 
                 delta=f"-${natural_price - artificial_price:.2f}")
        st.warning("⚠️ Price signals are distorted by intervention!")
    else:
        st.metric("Market Price", f"${natural_price:.2f}")
        st.success("✅ Price signals are accurate!")

    # Business Cycle Visualization
    st.subheader("📊 The Boom-Bust Cycle")
    
    # Generate sample data for a business cycle
    periods = 100
    x = np.linspace(0, 4*np.pi, periods)
    natural_cycle = 100 + 10*np.sin(x)
    boom_bust = 100 + 20*np.sin(x) + x/2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(periods)), y=natural_cycle, 
                            name="Natural Market Fluctuations"))
    fig.add_trace(go.Scatter(x=list(range(periods)), y=boom_bust, 
                            name="Central Bank Induced Cycle"))
    fig.update_layout(title="Economic Cycles Comparison",
                     yaxis_title="Economic Activity")
    st.plotly_chart(fig)
    
    # Interactive Boom-Bust Explanation
    st.subheader("🎮 Boom-Bust Cycle Simulator")
    
    stage = st.select_slider(
        "Explore the stages of the cycle:",
        options=["1. Low Interest Rates", 
                "2. Credit Expansion", 
                "3. Malinvestment", 
                "4. Resource Scarcity",
                "5. Bust"]
    )
    
    cycle_explanations = {
        "1. Low Interest Rates": "Central bank artificially lowers interest rates below market level",
        "2. Credit Expansion": "Banks create new money through loans, increasing money supply",
        "3. Malinvestment": "Businesses invest in projects that appear profitable due to cheap credit",
        "4. Resource Scarcity": "Competition for real resources reveals insufficient savings",
        "5. Bust": "Projects fail as real resource constraints become apparent"
    }
    
    st.info(f"**{stage}**: {cycle_explanations[stage]}")
    
    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What causes the boom-bust cycle?",
        ["Natural market fluctuations",
         "Consumer confidence changes",
         "Central bank interest rate manipulation",
         "Random economic events"]
    )
    
    if st.button("Check Answer", key="check3"):
        if quiz == "Central bank interest rate manipulation":
            st.success("🎉 Correct! The cycle is caused by artificial interest rate manipulation.")
            st.session_state.quiz_scores_intermediate['page3'] = 100
        else:
            st.error("Try again! Think about the role of central banks.")
            st.session_state.quiz_scores_intermediate['page3'] = 0

def page_sound_money_liberty():
    st.header("🗽 Sound Money and Liberty")
    
    # Government Spending Simulator
    st.subheader("🏛️ Government Funding Methods")
    
    spending = st.slider("Government Spending (Billions $)", 100, 1000, 500)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Direct Taxation", f"${spending}B")
        st.info("Transparent but unpopular")
        
    with col2:
        st.metric("Money Printing", f"${spending}B")
        st.warning("Hidden tax through inflation")
        
    with col3:
        st.metric("Debt", f"${spending}B")
        st.error("Burden on future generations")

    # The Bezzle Visualization
    st.subheader("🎭 The Economic Zombie Problem")
    
    # Interactive zombie company simulator
    zombie_percentage = st.slider("Percentage of zombie companies:", 0, 50, 20)
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=["Productive Companies", "Zombie Companies"],
        values=[100-zombie_percentage, zombie_percentage],
        hole=0.3
    ))
    fig.update_layout(title="Economic Resource Allocation")
    st.plotly_chart(fig)
    
    if zombie_percentage > 30:
        st.error("⚠️ High level of zombie companies indicates severe economic distortion!")
    elif zombie_percentage > 15:
        st.warning("⚠️ Moderate level of zombie companies present in the economy")
    else:
        st.success("✅ Healthy level of creative destruction in the economy")

    # War Financing Comparison
    st.subheader("⚔️ War Financing Under Different Monetary Systems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Gold Standard Era")
        st.markdown("""
        - ✅ Limited by treasury reserves
        - ✅ Requires public support
        - ✅ Natural constraints
        - ✅ Quick resolution
        """)
        
    with col2:
        st.markdown("### Fiat Money Era")
        st.markdown("""
        - ❌ Unlimited funding potential
        - ❌ Hidden costs through inflation
        - ❌ Perpetual warfare possible
        - ❌ Extended conflicts
        """)

    # Knowledge Check
    st.subheader("📝 Knowledge Check")
    quiz = st.radio(
        "What is the 'bezzle' in an economy?",
        ["Profitable companies",
         "Companies surviving on cheap credit despite being unproductive",
         "Government agencies",
         "Start-up companies"]
    )
    
    if st.button("Check Answer", key="check4"):
        if quiz == "Companies surviving on cheap credit despite being unproductive":
            st.success("🎉 Correct! The bezzle refers to companies that survive through cheap credit rather than productive value creation.")
            st.session_state.quiz_scores_intermediate['page4'] = 100
        else:
            st.error("Try again! Think about the effects of artificially cheap credit.")
            st.session_state.quiz_scores_intermediate['page4'] = 0