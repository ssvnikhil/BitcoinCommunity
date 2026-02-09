import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show_content():
    st.title("Unsound Money and Societal Impact")

    if "quiz_scores_intermediate" not in st.session_state:
        st.session_state.quiz_scores_intermediate = {
            "page1": 0,
            "page2": 0,
            "page3": 0,
            "page4": 0,
        }

    pages = {
        1: page_gold_standard_flaw,
        2: page_time_preference,
        3: page_business_cycle,
        4: page_sound_money_liberty,
    }

    st.markdown("### Module Navigation")
    page = st.radio(
        "",
        [
            "1. Gold Standard to Fiat",
            "2. Time Preference",
            "3. Business Cycles",
            "4. Sound Money and Liberty",
        ],
        horizontal=True,
        label_visibility="collapsed",
        index=0,
    )

    current_page = int(page[0])

    progress = sum(st.session_state.quiz_scores_intermediate.values()) / (
        len(st.session_state.quiz_scores_intermediate) * 100
    )
    st.markdown("### Your Progress")
    st.progress(progress)

    pages[current_page]()

    st.markdown("---")
    st.markdown("### References")
    st.markdown(
        """
        - Man, Economy, and State (Rothbard)
        - Human Action (Mises)
        - The Fiat Standard (Ammous)
        """
    )


def page_gold_standard_flaw():
    st.header("From Gold Standard to Fiat")

    st.markdown(
        """
        The gold standard failed because custody and control centralized.
        Once gold sat in vaults, paper claims expanded beyond reserves.
        """
    )

    st.subheader("Timeline of monetary shifts")
    events = {
        "Pre-1914": "Classical gold standard with global settlement",
        "1914": "War finance suspends redemption",
        "1944": "Bretton Woods anchors currencies to the dollar",
        "1971": "Gold convertibility ends; full fiat era begins",
    }

    selected_era = st.select_slider(
        "Explore an era:",
        options=list(events.keys()),
    )
    st.info(f"{selected_era}: {events[selected_era]}")

    st.subheader("Centralization risk simulator")
    gold_in_vault = st.slider("Gold held by banks (%)", 0, 100, 70)
    paper_claims = st.slider("Paper claims vs gold (%)", 100, 300, 150)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Physical gold", "Paper claims"],
            y=[100, paper_claims],
            name="Supply",
        )
    )
    fig.update_layout(title="Claims vs reserves (illustrative)")
    st.plotly_chart(fig)

    if paper_claims > 100:
        st.warning(
            f"Paper claims exceed reserves by {paper_claims - 100}%. This is the seed of bank runs."
        )

    st.markdown("### Quick check")
    quiz = st.radio(
        "What was the fatal flaw in the gold standard?",
        [
            "Gold was too heavy",
            "Gold centralized in banks enabling paper expansion",
            "Gold was too scarce",
            "Gold was too abundant",
        ],
    )

    if st.button("Check answer", key="check1"):
        if quiz == "Gold centralized in banks enabling paper expansion":
            st.success("Correct. Centralization allowed paper claims to outrun reserves.")
            st.session_state.quiz_scores_intermediate["page1"] = 100
        else:
            st.error("Try again. Think about custody and leverage.")
            st.session_state.quiz_scores_intermediate["page1"] = 0


def page_time_preference():
    st.header("Time Preference and Civilization")

    st.markdown(
        """
        When money holds value, people plan longer horizons.
        When money loses value, the future is discounted.
        """
    )

    st.subheader("Personal time preference estimator")
    amount_today = st.number_input("How much would you accept today?", min_value=1, value=100)
    future_days = st.slider("In how many days would you receive the money?", 1, 365, 30)
    future_amount = st.number_input(
        "How much would you need in the future to wait?",
        min_value=float(amount_today),
        value=float(amount_today * 1.1),
    )

    annual_rate = ((future_amount / amount_today) ** (365 / future_days) - 1) * 100
    st.metric("Implied annual time preference", f"{annual_rate:.1f}%")

    if annual_rate > 20:
        st.warning("High time preference suggests strong desire for immediacy.")
    else:
        st.success("Lower time preference supports long-term planning.")

    st.subheader("Societal effects")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Sound money**
            - Long-term planning
            - Capital accumulation
            - Productive investment
            - Lower time preference
            """
        )

    with col2:
        st.markdown(
            """
            **Unsound money**
            - Short-term thinking
            - Consumption pressure
            - Debt expansion
            - Higher time preference
            """
        )

    st.markdown("### Quick check")
    quiz = st.radio(
        "How does sound money affect time preference?",
        [
            "It increases time preference",
            "It has no effect",
            "It lowers time preference",
            "Time preference is unrelated to money",
        ],
    )

    if st.button("Check answer", key="check2"):
        if quiz == "It lowers time preference":
            st.success("Correct. Stable money encourages long-term decisions.")
            st.session_state.quiz_scores_intermediate["page2"] = 100
        else:
            st.error("Try again. Think about how stability changes planning horizons.")
            st.session_state.quiz_scores_intermediate["page2"] = 0


def page_business_cycle():
    st.header("Business Cycles and Price Signals")

    st.markdown(
        """
        Interest rates are price signals. When they are distorted, investment decisions follow a false map.
        """
    )

    st.subheader("Price signal simulator")
    supply = st.slider("Supply level", 1, 100, 50)
    demand = st.slider("Demand level", 1, 100, 50)

    natural_price = 100 * (demand / supply)
    intervention = st.checkbox("Apply central bank intervention")

    if intervention:
        artificial_price = natural_price * 0.7
        st.metric("Market price", f"${artificial_price:.2f}", delta=f"-${natural_price - artificial_price:.2f}")
        st.warning("Price signals are distorted by intervention.")
    else:
        st.metric("Market price", f"${natural_price:.2f}")
        st.success("Price signals are clear.")

    st.subheader("Boom-bust overview (illustrative)")
    periods = 80
    x = np.linspace(0, 4 * np.pi, periods)
    natural_cycle = 100 + 8 * np.sin(x)
    boom_bust = 100 + 18 * np.sin(x) + x / 2

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(range(periods)), y=natural_cycle, name="Natural fluctuations")
    )
    fig.add_trace(
        go.Scatter(x=list(range(periods)), y=boom_bust, name="Credit-driven cycle")
    )
    fig.update_layout(title="Economic cycles (illustrative)", yaxis_title="Economic activity")
    st.plotly_chart(fig)

    st.subheader("Cycle stages")
    stage = st.select_slider(
        "Explore the stages:",
        options=[
            "1. Low rates",
            "2. Credit expansion",
            "3. Malinvestment",
            "4. Resource strain",
            "5. Bust",
        ],
    )

    cycle_explanations = {
        "1. Low rates": "Rates are pushed below market clearing levels.",
        "2. Credit expansion": "New money enters through debt issuance.",
        "3. Malinvestment": "Projects appear profitable on false signals.",
        "4. Resource strain": "Real savings are insufficient to complete projects.",
        "5. Bust": "Projects fail and corrections unfold.",
    }

    st.info(cycle_explanations[stage])

    st.markdown("### Quick check")
    quiz = st.radio(
        "What causes the boom-bust cycle?",
        [
            "Natural market fluctuations",
            "Consumer confidence changes",
            "Interest rate manipulation",
            "Random economic events",
        ],
    )

    if st.button("Check answer", key="check3"):
        if quiz == "Interest rate manipulation":
            st.success("Correct. Artificial credit conditions distort real signals.")
            st.session_state.quiz_scores_intermediate["page3"] = 100
        else:
            st.error("Try again. Think about the source of the distortion.")
            st.session_state.quiz_scores_intermediate["page3"] = 0


def page_sound_money_liberty():
    st.header("Sound Money and Liberty")

    st.markdown(
        """
        The way a society funds itself shapes incentives, accountability, and the scope of state action.
        """
    )

    st.subheader("Government funding methods")
    spending = st.slider("Government spending (billions)", 100, 1000, 500)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Direct taxation", f"${spending}B")
        st.info("Transparent, politically costly")

    with col2:
        st.metric("Money creation", f"${spending}B")
        st.warning("Hidden tax via dilution")

    with col3:
        st.metric("Debt", f"${spending}B")
        st.error("Burden shifted to the future")

    st.subheader("The economic zombie problem")
    zombie_percentage = st.slider("Zombie companies (%)", 0, 50, 20)

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=["Productive", "Zombie"],
            values=[100 - zombie_percentage, zombie_percentage],
            hole=0.3,
        )
    )
    fig.update_layout(title="Capital allocation")
    st.plotly_chart(fig)

    if zombie_percentage > 30:
        st.error("High zombie levels suggest deep misallocation.")
    elif zombie_percentage > 15:
        st.warning("Moderate zombie levels indicate distortion.")
    else:
        st.success("Low zombie levels support creative destruction.")

    st.subheader("War financing comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Gold standard era**
            - Limited by reserves
            - Requires public support
            - Natural constraints
            """
        )

    with col2:
        st.markdown(
            """
            **Fiat era**
            - Expandable funding
            - Hidden costs via inflation
            - Longer conflicts possible
            """
        )

    st.markdown("### Quick check")
    quiz = st.radio(
        "What is the 'bezzle' in an economy?",
        [
            "Profitable companies",
            "Companies surviving on cheap credit",
            "Government agencies",
            "Start-up companies",
        ],
    )

    if st.button("Check answer", key="check4"):
        if quiz == "Companies surviving on cheap credit":
            st.success("Correct. The bezzle is sustained by distorted incentives.")
            st.session_state.quiz_scores_intermediate["page4"] = 100
        else:
            st.error("Try again. Think about misallocated credit.")
            st.session_state.quiz_scores_intermediate["page4"] = 0
