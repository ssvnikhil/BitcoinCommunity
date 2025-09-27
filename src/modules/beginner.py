import streamlit as st
import time

def show_content():
    st.title("🌱 Understanding Money and Bitcoin Basics")
    
    st.markdown("""
    Welcome to the Beginner's module! Here you'll learn the fundamental concepts of money 
    and how Bitcoin relates to these core principles.
    """)

    # Session state initialization
    if 'quiz_scores' not in st.session_state:
        st.session_state.quiz_scores = {
            'page1': 0,
            'page2': 0,
            'page3': 0,
            'page4': 0
        }
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    # Navigation
    pages = {
        1: page_one,
        2: page_two,
        3: page_three,
        4: page_four
    }

    # Page selection in sidebar
    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Select a topic:",
        ["1. The Challenge of Exchange",
         "2. Functions of Money",
         "3. Hard vs Easy Money",
         "4. Historical Money Lessons"],
        index=st.session_state.current_page - 1
    )
    
    # Update current page
    st.session_state.current_page = int(page[0])
    
    # Display progress
    progress = sum(st.session_state.quiz_scores.values()) / (len(st.session_state.quiz_scores) * 100)
    st.sidebar.markdown("### Your Progress")
    st.sidebar.progress(progress)
    
    # Display current page
    pages[st.session_state.current_page]()

def page_one():
    st.header("📚 The Challenge of Exchange and Birth of Money")
    
    # Interactive Barter Simulation
    st.subheader("🔄 Interactive Barter Simulation")
    col1, col2 = st.columns(2)
    
    with col1:
        item_to_trade = st.selectbox(
            "What do you have to trade?",
            ["Fish", "Shoes", "Cow", "Salt"]
        )
    
    with col2:
        item_wanted = st.selectbox(
            "What do you want?",
            ["Fish", "Shoes", "Cow", "Salt"]
        )
    
    if st.button("Try to Trade"):
        if item_to_trade == item_wanted:
            st.warning("You already have what you want!")
        elif (item_to_trade == "Cow" and item_wanted == "Salt"):
            st.error("❌ Trade Failed: Cannot divide cow into small enough units for salt!")
            st.info("This demonstrates the challenge of 'Salability Across Scales'")
        else:
            st.error("❌ Trade Failed: Couldn't find someone who wants your item AND has what you want!")
            st.info("This demonstrates the 'Coincidence of Wants' problem")

    # Main Content
    st.markdown("""
    ### The Problem of Barter
    
    In a barter system, trade faces three main challenges:
    
    1. **Across Scales** 📏
       - Example: Trading a cow (high value) for salt (low value)
       - Problem: Can't divide the cow into small enough pieces
    
    2. **Across Space** 🌍
       - Example: Trading with people in different locations
       - Problem: Difficult to transport goods for trade
    
    3. **Across Time** ⏳
       - Example: Trading perishable goods like fish
       - Problem: Can't store value in perishable items
    """)

    # Interactive Quiz
    st.markdown("### 🎯 Knowledge Check")
    quiz_1 = st.radio(
        "What is the main problem with barter trade?",
        ["Too many goods to choose from",
         "The coincidence of wants",
         "Money doesn't exist",
         "Prices are too high"],
        key="quiz1"
    )
    
    if st.button("Check Answer", key="check1"):
        if quiz_1 == "The coincidence of wants":
            st.success("🎉 Correct! The coincidence of wants is the fundamental problem that makes barter impractical.")
            st.session_state.quiz_scores['page1'] = 100
        else:
            st.error("Try again! Think about what makes it difficult for two people to trade directly.")
            st.session_state.quiz_scores['page1'] = 0

def page_two():
    st.header("💰 The Three Functions of Money")
    
    # Interactive Function Selection
    selected_function = st.selectbox(
        "Select a function of money to learn more:",
        ["Medium of Exchange", "Store of Value", "Unit of Account"]
    )
    
    if selected_function == "Medium of Exchange":
        st.markdown("""
        ### 🔄 Medium of Exchange
        
        Money serves as an intermediate step in trade:
        ```
        Without Money: Fish → Shoes (direct barter)
        With Money: Fish → Money → Shoes (indirect exchange)
        ```
        """)
        
    elif selected_function == "Store of Value":
        st.markdown("""
        ### 🏦 Store of Value
        
        Money allows you to:
        - Save today's value for future use
        - Transport wealth across time
        - Plan for future expenses
        """)
        
    elif selected_function == "Unit of Account":
        st.markdown("""
        ### 📊 Unit of Account
        
        Money helps you:
        - Compare prices easily
        - Calculate profits and losses
        - Make economic decisions
        """)

    # Interactive Salability Demonstration
    st.subheader("🎯 Understanding Salability")
    
    good = st.selectbox(
        "Select a good to analyze its salability:",
        ["Gold", "Fish", "House", "Digital Files"]
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Across Scales")
        if good == "Gold":
            st.success("✅ Can be divided")
        elif good == "House":
            st.error("❌ Cannot be divided")
        elif good == "Fish":
            st.warning("⚠️ Limited division")
        else:
            st.success("✅ Perfectly divisible")

    with col2:
        st.markdown("### Across Space")
        if good == "Gold":
            st.success("✅ Portable")
        elif good == "House":
            st.error("❌ Not portable")
        elif good == "Fish":
            st.warning("⚠️ Somewhat portable")
        else:
            st.success("✅ Instantly portable")

    with col3:
        st.markdown("### Across Time")
        if good == "Gold":
            st.success("✅ Durable")
        elif good == "House":
            st.success("✅ Durable")
        elif good == "Fish":
            st.error("❌ Perishable")
        else:
            st.success("✅ Durable")

    # Quiz
    st.markdown("### 📝 Knowledge Check")
    quiz_2 = st.multiselect(
        "Which are the three main functions of money?",
        ["Medium of Exchange", "Store of Value", "Unit of Account", 
         "Source of Income", "Form of Investment"],
        key="quiz2"
    )
    
    if st.button("Check Answer", key="check2"):
        correct_answers = {"Medium of Exchange", "Store of Value", "Unit of Account"}
        if set(quiz_2) == correct_answers:
            st.success("🎉 Correct! You've identified all three main functions of money!")
            st.session_state.quiz_scores['page2'] = 100
        else:
            st.error("Try again! Select exactly three correct functions.")
            st.session_state.quiz_scores['page2'] = 0

def page_three():
    st.header("🏗️ Hard Money vs Easy Money")
    
    # Interactive Stock-to-Flow Calculator
    st.subheader("📊 Stock-to-Flow Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stock = st.number_input("Enter total existing supply (stock):", min_value=1, value=1000)
    
    with col2:
        flow = st.number_input("Enter annual new production (flow):", min_value=1, value=10)
    
    if st.button("Calculate Stock-to-Flow Ratio"):
        ratio = stock / flow
        st.metric("Stock-to-Flow Ratio", f"{ratio:.2f}")
        
        if ratio > 50:
            st.success("This would be considered hard money! 💪")
        elif ratio > 20:
            st.info("This is moderately hard money! 👍")
        else:
            st.warning("This would be considered easy money! ⚠️")

    st.markdown("""
    ### Understanding Monetary Hardness
    
    Money's hardness is determined by how difficult it is to increase its supply:
    
    - **Hard Money**: Difficult to produce more units
    - **Easy Money**: Simple to increase supply
    
    The Stock-to-Flow ratio helps measure this:
    ```
    Stock-to-Flow = Existing Supply / Annual New Production
    ```
    """)

    # Interactive Example
    st.subheader("💡 The Easy Money Trap Simulation")
    
    if st.button("Run Simulation"):
        progress_bar = st.progress(0)
        
        stages = {
            0: "1. People start using an easy money to store wealth",
            20: "2. Increased demand drives up the price",
            40: "3. Higher prices make production more profitable",
            60: "4. Producers create more supply",
            80: "5. Increased supply reduces value",
            100: "Result: Savers lose their wealth 📉"
        }
        
        for i in range(101):
            time.sleep(0.05)
            progress_bar.progress(i)
            if i in stages:
                st.write(stages[i])

    # Quiz
    st.markdown("### 🎯 Knowledge Check")
    quiz_3 = st.radio(
        "What makes money 'hard' money?",
        ["It's physically hard to carry",
         "It's difficult to produce new units",
         "It's hard to spend",
         "It's difficult to store"],
        key="quiz3"
    )
    
    if st.button("Check Answer", key="check3"):
        if quiz_3 == "It's difficult to produce new units":
            st.success("🎉 Correct! Hard money is defined by the difficulty of increasing its supply.")
            st.session_state.quiz_scores['page3'] = 100
        else:
            st.error("Try again! Think about what makes it hard to increase the money supply.")
            st.session_state.quiz_scores['page3'] = 0

def page_four():
    st.header("📜 Historical Lessons from Primitive Moneys")
    
    # Interactive Timeline
    st.subheader("🕰️ Interactive Money Timeline")
    
    selected_case = st.selectbox(
        "Choose a historical case study:",
        ["Rai Stones", "Aggry Beads", "Seashells", "Metals"]
    )
    
    if selected_case == "Rai Stones":
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Yap_Stone_Money.jpg/640px-Yap_Stone_Money.jpg", 
                caption="Rai Stones of Yap Island")
        st.markdown("""
        ### The Fall of Rai Stones
        
        - **Location**: Yap Island
        - **Time Period**: Until 1870s
        - **Failure Cause**: Technology made production too easy
        - **Key Lesson**: Money must remain hard to produce
        """)
        
    elif selected_case == "Aggry Beads":
        st.markdown("""
        ### The Tragedy of Aggry Beads
        
        - **Location**: West Africa
        - **Time Period**: Colonial era
        - **Failure Cause**: European mass production
        - **Key Lesson**: Technology can turn hard money into easy money
        """)
        
    elif selected_case == "Seashells":
        st.markdown("""
        ### The Obsolescence of Seashells
        
        - **Location**: Global
        - **Time Period**: Various
        - **Failure Cause**: Industrial collection methods
        - **Key Lesson**: Technological advancement can destroy monetary premium
        """)
        
    elif selected_case == "Metals":
        st.markdown("""
        ### The Rise of Metals
        
        - **Location**: Global
        - **Time Period**: Modern era
        - **Success Factor**: High stock-to-flow ratio
        - **Key Lesson**: Natural scarcity leads to better money
        """)

    # Interactive Lesson
    st.subheader("🎮 Historical Money Simulator")
    
    money_type = st.selectbox(
        "Choose a type of money to test:",
        ["Seashells", "Gold", "Paper Money", "Bitcoin"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Properties")
        if money_type == "Seashells":
            st.write("- Easy to find with technology")
            st.write("- Not divisible")
            st.write("- Limited durability")
        elif money_type == "Gold":
            st.write("- Hard to mine")
            st.write("- Divisible")
            st.write("- Very durable")
        elif money_type == "Paper Money":
            st.write("- Easy to print")
            st.write("- Divisible")
            st.write("- Moderate durability")
        else:
            st.write("- Fixed supply")
            st.write("- Highly divisible")
            st.write("- Digital durability")
    
    with col2:
        st.markdown("### Outcome as Money")
        if money_type == "Seashells":
            st.error("❌ Failed: Too easy to produce")
        elif money_type == "Gold":
            st.success("✅ Succeeded historically")
        elif money_type == "Paper Money":
            st.warning("⚠️ Mixed results: Depends on issuer")
        else:
            st.success("✅ Modern hard money solution")

    # Quiz
    st.markdown("### 📝 Knowledge Check")
    quiz_4 = st.radio(
        "What was the main reason for the failure of primitive moneys?",
        ["They were too heavy to carry",
         "Technology made them too easy to produce",
         "People didn't like how they looked",
         "They were too hard to find"],
        key="quiz4"
    )
    
    if st.button("Check Answer", key="check4"):
        if quiz_4 == "Technology made them too easy to produce":
            st.success("🎉 Correct! Technological advancement often made primitive moneys too easy to produce, destroying their monetary value.")
            st.session_state.quiz_scores['page4'] = 100
        else:
            st.error("Try again! Think about how technology affected the production of these money types.")
            st.session_state.quiz_scores['page4'] = 0