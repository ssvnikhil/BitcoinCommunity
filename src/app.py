import streamlit as st
import importlib

# Set page config
st.set_page_config(
    page_title="Bitcoin Signal Hub",
    page_icon="₿",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Space+Grotesk:wght@400;600;700&display=swap');

    :root {
        --bg: #f7f1e7;
        --ink: #1b1713;
        --muted: #6a5e52;
        --accent: #d1882f;
        --accent-2: #2f6f6d;
        --card: #fff7ea;
        --stroke: #eadfce;
    }

    .stApp {
        background: radial-gradient(1200px circle at 10% 5%, #fff2dc 0%, transparent 60%),
                    radial-gradient(1000px circle at 90% 10%, #e7f2ef 0%, transparent 55%),
                    linear-gradient(180deg, var(--bg) 0%, #f4efe7 100%);
        color: var(--ink);
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--ink);
    }

    h1 {
        font-family: 'DM Serif Display', serif;
        letter-spacing: 0.5px;
    }

    .hero {
        background: linear-gradient(135deg, #fff5e8 0%, #f6efe4 100%);
        border: 1px solid var(--stroke);
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(33, 23, 12, 0.08);
    }

    .hero-kicker {
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
        color: var(--muted);
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-size: 2.6rem;
        margin-bottom: 0.8rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--muted);
        margin-bottom: 0;
    }

    .card {
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 16px;
        padding: 1.4rem;
        height: 100%;
    }

    .card h3 {
        margin-top: 0;
    }

    .pill {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(209, 136, 47, 0.15);
        color: var(--ink);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton button {
        width: 100%;
        border-radius: 999px;
        border: 1px solid var(--stroke);
        background: #1b1713;
        color: #fef9f3;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);
        background: #2d2620;
    }

    .section-title {
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }

    .section-note {
        color: var(--muted);
        font-size: 0.95rem;
    }

    /* Top navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid var(--stroke);
        padding: 0.35rem;
        border-radius: 999px;
        box-shadow: 0 6px 18px rgba(33, 23, 12, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.45rem 1.2rem;
        border-radius: 999px;
        font-weight: 600;
        color: var(--muted);
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        background: #1b1713 !important;
        color: #fef9f3 !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    if "learning_level" not in st.session_state:
        st.session_state.learning_level = "Beginner"

    st.markdown("""
        <div class="hero">
            <div class="hero-kicker">Signal-First Intelligence</div>
            <div class="hero-title">Bitcoin Signal Hub</div>
            <div class="hero-subtitle">
                A product-analytics view of Bitcoin: on-chain activity, market structure, and daily signal synthesis.
                Built for people who want answers fast without the noise.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top navigation (tabs)
    st.markdown("###")
    home_tab, signal_tab, learning_tab, alerts_tab = st.tabs(
        ["Home", "Signal Desk", "Learning", "Alerts (Coming Soon)"]
    )

    with home_tab:
        display_home()

    with signal_tab:
        try:
            module_lib = importlib.import_module("modules.signal_desk")
            module_lib.show_content()
        except Exception as e:
            st.error("Signal Desk is under development. Please check back later!")
            st.exception(e)

    with learning_tab:
        st.markdown("### Learning Navigation")
        st.session_state.learning_level = st.radio(
            "",
            ["Beginner", "Intermediate", "Advanced"],
            horizontal=True,
            label_visibility="collapsed",
            index=["Beginner", "Intermediate", "Advanced"].index(
                st.session_state.learning_level
            ),
        )
        display_learning_home(key_prefix="learning_tab")
        try:
            module_map = {
                "Beginner": "beginner",
                "Intermediate": "intermediate",
                "Advanced": "advanced",
            }
            module_name = module_map[st.session_state.learning_level]
            module_path = f"modules.{module_name}"
            module_lib = importlib.import_module(module_path)
            module_lib.show_content()
        except Exception as e:
            st.error("Learning module is under development. Please check back later!")
            st.exception(e)

    with alerts_tab:
        st.subheader("Alerts: Coming Soon")
        st.markdown(
            "Price alerts are temporarily disabled while we finalize Supabase and email delivery setup."
        )
        st.info(
            "The feature will return once infrastructure is configured. For now, use Signal Desk for insights."
        )

def display_home():
    st.markdown("### Welcome to the Bitcoin Signal Hub")
    st.markdown(
        '<div class="section-note">This community helps you find signal in a noisy market — from on-chain analytics to clear learning paths.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="card">
            <span class="pill">What to Expect</span>
            <h3>Signal-First Insight</h3>
            <p>Daily briefings, on-chain activity, and real market structure — designed to answer the questions you would otherwise search for.</p>
            <p><strong>Outcome</strong>: You know what matters today and why.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    display_learning_home(key_prefix="home")

def display_learning_home(key_prefix: str):
    st.markdown("### Learning Platform")
    st.markdown(
        '<div class="section-note">Structured paths for beginners, intermediate learners, and advanced readers.</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <span class="pill">Foundations</span>
            <h3>Beginner</h3>
            <p>Build the money mental models. Understand why Bitcoin exists and what it fixes.</p>
            <p><strong>Outcome</strong>: You can explain Bitcoin in one clear paragraph.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Beginner", key=f"{key_prefix}_start_beginner"):
            st.session_state.learning_level = "Beginner"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <span class="pill">Systems</span>
            <h3>Intermediate</h3>
            <p>See how unsound money shapes society, incentives, and business cycles.</p>
            <p><strong>Outcome</strong>: You can diagnose monetary incentives in the real world.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Intermediate", key=f"{key_prefix}_start_intermediate"):
            st.session_state.learning_level = "Intermediate"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card">
            <span class="pill">Protocol</span>
            <h3>Advanced</h3>
            <p>Learn how Bitcoin achieves scarcity, security, and governance without trust.</p>
            <p><strong>Outcome</strong>: You can assess protocol tradeoffs with confidence.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Advanced", key=f"{key_prefix}_start_advanced"):
            st.session_state.learning_level = "Advanced"
            st.rerun()

    st.markdown("---")
    st.markdown("### How This Hub Works")
    st.markdown("""
    1. Start with the signal you need today.
    2. Read the core idea, then test your understanding.
    3. Capture the takeaway and move to the next topic.
    """)

    st.markdown("### What You Get")
    st.markdown("""
    - Clear definitions and mental models
    - Incentive-based explanations instead of slogans
    - Short, focused checks for comprehension
    - References at the end of each level
    """)

if __name__ == "__main__":
    main()
