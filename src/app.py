import streamlit as st
import importlib
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Bitcoin Community Learning Hub",
    page_icon="🌟",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        margin-bottom: 1rem;
    }
    h1, h2 {
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Main title and description
    st.title("🌟 Bitcoin Community Learning Hub")
    st.markdown("""
    Welcome to the Bitcoin Community Learning Hub! This platform is designed to help you
    understand Bitcoin from the ground up, whether you're a complete beginner or looking
    to deepen your knowledge.
    """)

    # Module selection sidebar
    st.sidebar.title("Navigation")
    module = st.sidebar.radio(
        "Choose your learning level:",
        ["Home", "Beginner", "Intermediate", "Advanced"]
    )

    # Display content based on selection
    if module == "Home":
        display_home()
    else:
        try:
            # Dynamically import and display the selected module
            module_name = module.lower()
            module_path = f"modules.{module_name}"
            module_lib = importlib.import_module(module_path)
            module_lib.show_content()
        except Exception as e:
            st.error(f"Module {module} is under development. Please check back later!")
            st.exception(e)

def display_home():
    st.header("📚 Learning Paths")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌱 Beginner")
        st.write("""
        Perfect for those new to Bitcoin. Learn the fundamentals:
        - What is Bitcoin?
        - How does it work?
        - Basic terminology
        """)
    
    with col2:
        st.subheader("🌿 Intermediate")
        st.write("""
        Deepen your knowledge:
        - Technical aspects
        - Bitcoin economics
        - Security practices
        """)
    
    with col3:
        st.subheader("🌳 Advanced")
        st.write("""
        Master complex topics:
        - Protocol details
        - Advanced concepts
        - Current developments
        """)

    st.markdown("---")
    st.markdown("""
    ### 🎯 How to Use This Platform
    1. Choose your level from the sidebar
    2. Read through the material at your own pace
    3. Progress to the next level when you're ready
    4. Revisit previous sections anytime
    """)

if __name__ == "__main__":
    main()