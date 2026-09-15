import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #FFF9DB;
    color: #222222;
    font-family: 'Segoe UI', sans-serif;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #222;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Search Box */
.stTextInput > div > div > input {
    background-color: white;
    color: black;
    border-radius: 15px;
    border: 2px solid #F4D35E;
    padding: 15px;
    font-size: 18px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button {
    width: 100%;
    background-color: #F4D35E;
    color: black;
    border-radius: 12px;
    border: none;
    padding: 14px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #FFD93D;
    transform: scale(1.02);
}

/* White Cards */
.result-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
    color: #222;
    border: 1px solid #eee;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFF3BF;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px 20px;
    color: black;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    color: #666;
    font-size: 14px;
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background-color: #F4D35E;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("⚙️ Dashboard")

    st.markdown("---")

    show_search = st.checkbox("🔍 Show Search Results", value=True)
    show_scrape = st.checkbox("📚 Show Scraped Content", value=True)
    show_feedback = st.checkbox("🧠 Show Critic Feedback", value=True)

    st.markdown("---")

    st.success("✅ System Ready")

    st.info("""
    Multi-Agent Research System
    
    ✔ Search Agent  
    ✔ Reader Agent  
    ✔ Writer Agent  
    ✔ Critic Agent
    """)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">🧠 AI Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Generate professional AI-powered research reports instantly</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SEARCH BAR
# ---------------------------------------------------

topic = st.text_input(
    label="Research Topic",
    placeholder="🔎 Enter your research topic...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([4,1])

with col1:
    run_button = st.button("🚀 Generate Research")

with col2:
    clear_button = st.button("🗑 Clear")

if clear_button:
    st.rerun()

# ---------------------------------------------------
# SEARCH HISTORY
# ---------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

if run_button:

    if not topic.strip():

        st.warning("⚠ Please enter a research topic.")
        st.stop()

    try:

        # Save history
        st.session_state.history.append(topic)

        # Progress UI
        progress = st.progress(0)
        status = st.empty()

        status.info("🔄 Initializing AI Agents...")

        progress.progress(10)

        # Loading Spinner
        with st.spinner("🤖 AI agents are researching your topic..."):

            state = run_research_pipeline(topic)

        progress.progress(100)

        status.success("✅ Research Completed Successfully!")

        # Celebration
        st.balloons()

        # ---------------------------------------------------
        # TABS
        # ---------------------------------------------------

        tabs = st.tabs([
            "📝 Final Report",
            "🔍 Search Results",
            "📚 Scraped Content",
            "🧠 Critic Feedback"
        ])

        # ---------------------------------------------------
        # FINAL REPORT
        # ---------------------------------------------------

        with tabs[0]:

            st.markdown("## 📝 Final Research Report")

            st.markdown(
                f"""
                <div class="result-card">
                {state['report']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---------------------------------------------------
        # SEARCH RESULTS
        # ---------------------------------------------------

        with tabs[1]:

            if show_search:

                st.markdown(
                    f"""
                    <div class="result-card">
                    {state['search_result']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------
        # SCRAPED CONTENT
        # ---------------------------------------------------

        with tabs[2]:

            if show_scrape:

                st.markdown(
                    f"""
                    <div class="result-card">
                    {state['scraped_content']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------
        # FEEDBACK
        # ---------------------------------------------------

        with tabs[3]:

            if show_feedback:

                st.markdown(
                    f"""
                    <div class="result-card">
                    {state['Feedback']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ---------------------------------------------------
        # DOWNLOAD REPORT
        # ---------------------------------------------------

        full_report = f"""
AI RESEARCH REPORT
Generated: {datetime.now()}

TOPIC:
{topic}

================================================

SEARCH RESULTS:
{state['search_result']}

================================================

SCRAPED CONTENT:
{state['scraped_content']}

================================================

FINAL REPORT:
{state['report']}

================================================

CRITIC FEEDBACK:
{state['Feedback']}
"""

        st.download_button(
            label="📥 Download Full Report",
            data=full_report,
            file_name=f"{topic.replace(' ', '_')}_report.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(f"❌ Error: {str(e)}")

# ---------------------------------------------------
# RECENT SEARCHES
# ---------------------------------------------------

if st.session_state.history:

    st.markdown("## 🕘 Recent Searches")

    for item in reversed(st.session_state.history[-5:]):

        st.markdown(
            f"""
            <div class="result-card">
            🔹 {item}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">
Built with ❤️ using Streamlit + Multi-Agent AI System
</div>
""", unsafe_allow_html=True)
