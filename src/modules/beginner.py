import streamlit as st

def show_content():
    st.title("Foundations: Money and Bitcoin")

    st.markdown(
        """
        This level builds the money mental models you need to understand why Bitcoin exists.
        The goal is clarity, not hype.
        """
    )

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {
            "page1": 0,
            "page2": 0,
            "page3": 0,
            "page4": 0,
        }
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    pages = {
        1: page_one,
        2: page_two,
        3: page_three,
        4: page_four,
    }

    st.markdown("### Module Navigation")
    page = st.radio(
        "",
        [
            "1. Why Money Exists",
            "2. What Money Must Do",
            "3. Hard vs Easy Money",
            "4. Historical Lessons",
        ],
        horizontal=True,
        label_visibility="collapsed",
        index=st.session_state.current_page - 1,
    )

    st.session_state.current_page = int(page[0])

    progress = sum(st.session_state.quiz_scores.values()) / (
        len(st.session_state.quiz_scores) * 100
    )
    st.markdown("### Your Progress")
    st.progress(progress)

    pages[st.session_state.current_page]()

    st.markdown("---")
    st.markdown("### References")
    st.markdown(
        """
        - The Bitcoin Standard (Ammous)
        - Layered Money (Nik Bhatia)
        - The Price of Tomorrow (Booth)
        """
    )


def page_one():
    st.header("Why Money Exists")

    st.markdown(
        """
        Trade breaks down when people want different things at the same time.
        Money solves this coordination problem by making value portable across time, place, and scale.
        """
    )

    st.subheader("Barter friction simulator")
    col1, col2 = st.columns(2)

    with col1:
        item_to_trade = st.selectbox(
            "What do you have to trade?",
            ["Fish", "Shoes", "Cow", "Salt"],
        )

    with col2:
        item_wanted = st.selectbox(
            "What do you want?",
            ["Fish", "Shoes", "Cow", "Salt"],
        )

    if st.button("Try the trade"):
        if item_to_trade == item_wanted:
            st.warning("You already have what you want.")
        elif item_to_trade == "Cow" and item_wanted == "Salt":
            st.error("Trade failed: the cow cannot be divided into small units.")
            st.info("This is a scale problem: you cannot make fine-grained trades.")
        else:
            st.error("Trade failed: no matching wants in the same moment.")
            st.info("This is the coincidence-of-wants problem.")

    st.markdown(
        """
        **Three money problems in barter**
        - Across scale: large items cannot be divided for small trades.
        - Across space: physical goods are hard to move.
        - Across time: perishable goods cannot store value.
        """
    )

    st.info("Key takeaway: money is the tool that makes value portable across scale, space, and time.")

    st.markdown("### Quick check")
    quiz_1 = st.radio(
        "What is the core problem with barter?",
        [
            "Too many goods to choose from",
            "The coincidence of wants",
            "Money does not exist",
            "Prices are too high",
        ],
        key="quiz1",
    )

    if st.button("Check answer", key="check1"):
        if quiz_1 == "The coincidence of wants":
            st.success("Correct. Direct barter fails because wants rarely line up.")
            st.session_state.quiz_scores["page1"] = 100
        else:
            st.error("Try again. Think about why two people cannot easily trade directly.")
            st.session_state.quiz_scores["page1"] = 0


def page_two():
    st.header("What Money Must Do")

    st.markdown(
        """
        Money has three core functions. If a good performs all three reliably,
        it can become a dominant monetary tool.
        """
    )

    selected_function = st.selectbox(
        "Select a function to explore:",
        ["Medium of Exchange", "Store of Value", "Unit of Account"],
    )

    if selected_function == "Medium of Exchange":
        st.markdown(
            """
            Money lets you trade without needing a direct match:
            Fish -> Money -> Shoes.
            """
        )
    elif selected_function == "Store of Value":
        st.markdown(
            """
            Money preserves purchasing power so value can move through time.
            """
        )
    else:
        st.markdown(
            """
            Money gives prices a common language so you can compare choices.
            """
        )

    st.subheader("Salability across scale, space, and time")
    good = st.selectbox(
        "Select a good to evaluate:",
        ["Gold", "Fish", "House", "Digital File"],
    )

    scores = {
        "Gold": ["High", "Medium", "High"],
        "Fish": ["Low", "Low", "Low"],
        "House": ["Low", "Low", "High"],
        "Digital File": ["High", "High", "High"],
    }

    st.table(
        {
            "Property": ["Across scale", "Across space", "Across time"],
            "Assessment": scores[good],
        }
    )

    st.info(
        "Key takeaway: good money is divisible, portable, and durable at the same time."
    )

    st.markdown("### Quick check")
    quiz_2 = st.multiselect(
        "Which are the three main functions of money?",
        [
            "Medium of Exchange",
            "Store of Value",
            "Unit of Account",
            "Source of Income",
            "Form of Investment",
        ],
        key="quiz2",
    )

    if st.button("Check answer", key="check2"):
        correct_answers = {
            "Medium of Exchange",
            "Store of Value",
            "Unit of Account",
        }
        if set(quiz_2) == correct_answers:
            st.success("Correct. You identified all three functions.")
            st.session_state.quiz_scores["page2"] = 100
        else:
            st.error("Try again and select exactly three functions.")
            st.session_state.quiz_scores["page2"] = 0


def page_three():
    st.header("Hard vs Easy Money")

    st.markdown(
        """
        Money is hard when supply is difficult to increase.
        Money is easy when production can scale quickly.
        """
    )

    st.subheader("Stock-to-flow calculator")
    col1, col2 = st.columns(2)

    with col1:
        stock = st.number_input(
            "Total existing supply (stock)",
            min_value=1,
            value=1000,
        )

    with col2:
        flow = st.number_input(
            "Annual new production (flow)",
            min_value=1,
            value=10,
        )

    if st.button("Calculate stock-to-flow"):
        ratio = stock / flow
        st.metric("Stock-to-flow ratio", f"{ratio:.2f}")

        if ratio > 50:
            st.success("This is hard money: supply growth is slow.")
        elif ratio > 20:
            st.info("This is moderately hard money.")
        else:
            st.warning("This is easy money: supply can expand quickly.")

    st.subheader("Supply shock walkthrough")
    stage = st.select_slider(
        "Explore a typical easy-money cycle:",
        options=[
            "1. Demand rises",
            "2. Price rises",
            "3. Production expands",
            "4. Supply floods",
            "5. Savings dilute",
        ],
    )

    stage_explanations = {
        "1. Demand rises": "People try to store value in the easy money.",
        "2. Price rises": "Higher prices signal profit for producers.",
        "3. Production expands": "Supply increases faster than demand.",
        "4. Supply floods": "More units reduce scarcity and value.",
        "5. Savings dilute": "Purchasing power leaks away from savers.",
    }

    st.info(stage_explanations[stage])

    st.markdown("### Quick check")
    quiz_3 = st.radio(
        "What makes money hard?",
        [
            "It is physically heavy",
            "It is difficult to produce new units",
            "It is hard to spend",
            "It is difficult to store",
        ],
        key="quiz3",
    )

    if st.button("Check answer", key="check3"):
        if quiz_3 == "It is difficult to produce new units":
            st.success("Correct. Hard money is defined by supply resistance.")
            st.session_state.quiz_scores["page3"] = 100
        else:
            st.error("Try again. Think about supply growth.")
            st.session_state.quiz_scores["page3"] = 0


def page_four():
    st.header("Historical Lessons")

    st.markdown(
        """
        History shows a repeating pattern: when technology makes a money easy to produce,
        it loses its monetary premium.
        """
    )

    selected_case = st.selectbox(
        "Choose a historical case study:",
        ["Rai Stones", "Aggry Beads", "Seashells", "Metals"],
    )

    cases = {
        "Rai Stones": {
            "summary": "Large limestone discs on Yap Island.",
            "failure": "Technology made production cheaper and faster.",
            "lesson": "Money must resist production improvements.",
        },
        "Aggry Beads": {
            "summary": "Beads used as money in West Africa.",
            "failure": "Industrial mass production destroyed scarcity.",
            "lesson": "Hard money can turn easy overnight.",
        },
        "Seashells": {
            "summary": "Shells used across regions for trade.",
            "failure": "Improved collection methods increased supply.",
            "lesson": "Technological shocks change monetary winners.",
        },
        "Metals": {
            "summary": "Gold and silver outlasted other commodities.",
            "failure": "Rarely failed due to natural scarcity.",
            "lesson": "Scarcity plus durability beats novelty.",
        },
    }

    st.markdown(f"**Summary**: {cases[selected_case]['summary']}")
    st.markdown(f"**Failure or advantage**: {cases[selected_case]['failure']}")
    st.markdown(f"**Lesson**: {cases[selected_case]['lesson']}")

    st.subheader("Pattern recognition")
    st.markdown(
        """
        1. A scarce good becomes money.
        2. Demand rises and creates a monetary premium.
        3. Technology reduces scarcity.
        4. The monetary premium collapses.
        """
    )

    st.markdown("### Quick check")
    quiz_4 = st.radio(
        "Why do primitive moneys often fail?",
        [
            "They were too heavy to carry",
            "Technology made them too easy to produce",
            "People disliked how they looked",
            "They were too hard to find",
        ],
        key="quiz4",
    )

    if st.button("Check answer", key="check4"):
        if quiz_4 == "Technology made them too easy to produce":
            st.success("Correct. Scarcity evaporates when production becomes easy.")
            st.session_state.quiz_scores["page4"] = 100
        else:
            st.error("Try again. Think about what happens when supply can expand quickly.")
            st.session_state.quiz_scores["page4"] = 0
