import os
import re
import json
import sqlite3
import streamlit as st
from search import search_library
from reading_support import (
    estimate_reading_difficulty,
    extract_keywords,
    get_reading_recommendation,
    simplify_text_ai,
    generate_glossary_ai
)

# Set page configuration with a premium title and icon
st.set_page_config(
    page_title="Helix Reader | Accessible AI Digital Library",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define script/database paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "library.db")

# ---------------------------------------------------------
# Dynamic CSS Injection (Visual Excellence & Accessibility)
# ---------------------------------------------------------
font_import = "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');"

# Accessibility settings in the sidebar
st.sidebar.title("🧬 Helix Reader Settings")
st.sidebar.markdown("---")

st.sidebar.subheader("👤 User Reading Profile")
user_reading_level = st.sidebar.selectbox(
    "Your Reading Level:",
    ["Elementary", "Middle School", "High School", "Academic"],
    index=2  # High School by default
)

st.sidebar.subheader("♿ Accessibility Adjustments")
accessibility_mode = st.sidebar.selectbox(
    "Choose Accessibility Mode:",
    ["Basic (Default)", "Support Mode", "Easy Reading (High Contrast)"],
    index=0
)

# Define CSS parameters based on accessibility mode selection
if accessibility_mode == "Basic (Default)":
    font_size = "1.05rem"
    heading_size = "2.0rem"
    line_height = "1.6"
    theme_css = """
        .viewer-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            color: #0f172a;
            padding: 2rem;
            border-radius: 1rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .excerpt-box {
            font-style: italic;
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1.25rem;
            border-radius: 0.5rem;
            color: #78350f;
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02);
        }
    """
elif accessibility_mode == "Support Mode":
    font_size = "1.3rem"
    heading_size = "2.3rem"
    line_height = "1.95"
    theme_css = """
        .viewer-container {
            background: #f8fafc;
            color: #0f172a;
            padding: 2.25rem;
            border-radius: 1.25rem;
            border: 2.5px solid #2563eb; /* Prominent blue boundary */
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.08);
        }
        .excerpt-box {
            font-style: italic;
            background-color: #fffbeb;
            border-left: 6px solid #d97706;
            padding: 1.5rem;
            border-radius: 0.75rem;
            font-weight: 500;
            color: #92400e;
        }
    """
else:  # "Easy Reading (High Contrast)" Mode
    font_size = "1.75rem"
    heading_size = "2.8rem"
    line_height = "2.4"
    theme_css = """
        .viewer-container {
            background-color: #000000 !important;
            color: #ffff00 !important;
            padding: 2.5rem !important;
            border-radius: 1.5rem !important;
            border: 6px double #ffff00 !important;
        }
        .excerpt-box {
            background-color: #111111 !important;
            color: #ffff00 !important;
            border-left: 10px solid #ffff00 !important;
            padding: 2rem !important;
            border-radius: 0.75rem !important;
            font-weight: bold !important;
        }
        h1, h2, h3, h4, p, li, span, div, strong, small {
            color: #ffff00 !important;
            font-weight: bold !important;
        }
    """

# Inject global styles
st.markdown(f"""
<style>
    {font_import}
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .title-gradient {{
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.2rem;
    }}
    
    .sub-gradient {{
        color: #475569;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }}
    
    .book-card {{
        padding: 1.25rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .book-card:hover {{
        border-color: #3b82f6;
        transform: translateY(-3px);
        box-shadow: 0 8px 16px -1px rgba(0, 0, 0, 0.08);
    }}
    
    .badge {{
        display: inline-block;
        padding: 0.3rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 8px;
        margin-right: 0.5rem;
    }}
    .badge-topic {{
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }}
    .badge-level {{
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }}
    .badge-keyword {{
        background-color: #f5f3ff;
        color: #6d28d9;
        border: 1px solid #ddd6fe;
        font-size: 0.7rem;
    }}
    
    .rec-box {{
        background-color: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }}
    
    .dict-word-box {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }}
    
    .accessibility-text {{
        font-size: {font_size} !important;
        line-height: {line_height} !important;
    }}
    .accessibility-header {{
        font-size: {heading_size} !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    {theme_css}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State for User Favorites & Custom Dictionary Bookmarks
# ---------------------------------------------------------
if "study_list" not in st.session_state:
    st.session_state.study_list = {}

# ---------------------------------------------------------
# Database Utility Functions
# ---------------------------------------------------------
def log_user_action(resource_id, action_type):
    """
    Inserts a user action event into the SQLite database user_actions table.
    """
    if not os.path.exists(DB_PATH):
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("""
            INSERT INTO user_actions (resource_id, action_type)
            VALUES (?, ?);
        """, (resource_id, action_type))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

def get_user_activity_history():
    """
    Fetches the 5 most recent logged activities.
    """
    if not os.path.exists(DB_PATH):
        return []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.action_type, u.created_at, r.title
            FROM user_actions u
            JOIN resources r ON u.resource_id = r.resource_id
            ORDER BY u.created_at DESC
            LIMIT 5;
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

def get_reading_progress():
    """
    Calculates reading progress metrics from the database (completed books vs. total resources).
    """
    if not os.path.exists(DB_PATH):
        return 0, 40
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT resource_id) FROM user_actions WHERE action_type = 'COMPLETED';")
        completed = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM resources;")
        total = cursor.fetchone()[0]
        conn.close()
        return completed, total
    except Exception:
        return 0, 40

def get_db_stats():
    if not os.path.exists(DB_PATH):
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM resources;")
        total_books = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT topic) FROM resources;")
        total_topics = cursor.fetchone()[0]
        cursor.execute("SELECT DISTINCT topic FROM resources;")
        topics_list = [row[0] for row in cursor.fetchall()]
        conn.close()
        return total_books, total_topics, topics_list
    except Exception:
        return None

# ---------------------------------------------------------
# Sidebar Panel Integrations
# ---------------------------------------------------------
# Progress Tracker
completed, total_count = get_reading_progress()
progress_pct = min(1.0, completed / max(1, total_count))
st.sidebar.subheader("🏆 Your Reading Progress")
st.sidebar.progress(progress_pct)
st.sidebar.write(f"You have completed **{completed}** out of **{total_count}** books in the catalog ({int(progress_pct*100)}%).")

st.sidebar.markdown("---")

# User Study list (Vocabulary Word Builder)
st.sidebar.subheader("🎒 Saved Vocabulary list")
if st.session_state.study_list:
    for word, definition in list(st.session_state.study_list.items()):
        with st.sidebar.expander(f"🔑 {word.title()}"):
            st.write(definition)
            if st.button(f"Remove: {word}", key=f"rm_{word}"):
                del st.session_state.study_list[word]
                st.rerun()
else:
    st.sidebar.info("Add difficult words from any book's dictionary into your study list!")

st.sidebar.markdown("---")

# Recent logged database activity history
st.sidebar.subheader("📜 Activity Log (SQLite)")
history = get_user_activity_history()
if history:
    for action_type, timestamp, title in history:
        emoji = "❤️" if action_type == "FAVORITE" else "✅" if action_type == "COMPLETED" else "📖"
        time_clean = timestamp.split(" ")[1] if " " in timestamp else timestamp
        st.sidebar.markdown(f"*{time_clean}* - {emoji} **{action_type}**:\n*{title}*")
else:
    st.sidebar.info("No activities logged yet. Select a resource below to log actions!")

st.sidebar.markdown("---")

# Library Metrics
st.sidebar.subheader("📊 Library Metrics")
stats = get_db_stats()
if stats:
    total_books, total_topics, topics_list = stats
    st.sidebar.write(f"**Available Books:** {total_books}")
    st.sidebar.write(f"**Categories Covered:** {total_topics}")
    st.sidebar.write(f"**Topics:** {', '.join(topics_list)}")

# ---------------------------------------------------------
# Main UI Tabs
# ---------------------------------------------------------
st.markdown('<div class="title-gradient">Helix Reader</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-gradient">An Accessible Digital Library powered by SQLite, NLP, & Reading Support Systems.</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 Curated Catalog Search", "🧪 Analyze Custom Text"])

# --- TAB 1: CATALOG SEARCH & READING ---
with tab1:
    if "selected_resource" not in st.session_state:
        st.session_state.selected_resource = None
    if "current_para_idx" not in st.session_state:
        st.session_state.current_para_idx = 0

    search_query = st.text_input(
        label="Search library archive (searches titles, authors, topics, keywords)...",
        placeholder="Try: Adam Smith, quantum, history, philosophy, evolution",
        key="search_input"
    )

    if search_query:
        search_response = search_library(DB_PATH, search_query)
        
        if search_response["status"] == "fallback":
            st.warning(f"⚠️ {search_response['message']}")
        elif search_response["status"] == "error":
            st.error(search_response["message"])
        else:
            results = search_response["results"]
            st.success(f"Matched {len(results)} resources in the catalog!")

            col_list, col_view = st.columns([1.2, 1.8])

            with col_list:
                st.write("### 🔍 Search Results")
                for item in results:
                    is_selected = st.session_state.selected_resource and st.session_state.selected_resource["resource_id"] == item["resource_id"]
                    
                    card_html = f"""
                    <div class="book-card" style="{'border-color: #3b82f6; background-color: #eff6ff;' if is_selected else ''}">
                        <strong style="color: #1e3a8a; font-size: 1.05rem;">{item['title']}</strong><br/>
                        <span style="font-size:0.85rem; color:#64748b; font-weight: 500;">By {item['author']}</span>
                        <div style="margin-top: 0.5rem;">
                            <span class="badge badge-topic">{item['topic']}</span>
                            <span class="badge badge-level">{item['reading_level']}</span>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    if st.button(f"Open: {item['title']}", key=f"btn_{item['resource_id']}"):
                        st.session_state.selected_resource = item
                        st.session_state.current_para_idx = 0
                        if "ai_simplified_view" in st.session_state:
                            del st.session_state["ai_simplified_view"]
                        if "ai_glossary_view" in st.session_state:
                            del st.session_state["ai_glossary_view"]
                        if "user_quiz_answered" in st.session_state:
                            del st.session_state["user_quiz_answered"]
                        
                        log_user_action(item["resource_id"], "STARTED_READING")
                        st.rerun()

            with col_view:
                st.write("### 📖 Active Reader Viewport")
                selected = st.session_state.selected_resource
                
                if selected:
                    # Apply accessibility styling boundary
                    st.markdown('<div class="viewer-container">', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="accessibility-header">{selected["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="accessibility-text"><strong>Author:</strong> {selected["author"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="accessibility-text"><strong>Topic:</strong> {selected["topic"]} | <strong>Level:</strong> {selected["reading_level"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("<hr/>", unsafe_allow_html=True)

                    excerpt = selected["excerpt"]
                    
                    # NLP Engine Metrics
                    nlp_difficulty = estimate_reading_difficulty(excerpt)
                    extracted_kw = extract_keywords(excerpt, top_n=5)
                    recs_dict = get_reading_recommendation(nlp_difficulty, user_reading_level=user_reading_level)

                    # Interactive Reading Log Controls
                    st.markdown('<div class="accessibility-text"><strong>Interactive Reading Actions (Log to DB):</strong></div>', unsafe_allow_html=True)
                    btn_c1, btn_c2, btn_c3 = st.columns(3)
                    if btn_c1.button("❤️ Add Favorite", key="act_favorite"):
                        log_user_action(selected["resource_id"], "FAVORITE")
                        st.success("Added to favorites!")
                        st.rerun()
                    if btn_c2.button("✅ Mark Read", key="act_complete"):
                        log_user_action(selected["resource_id"], "COMPLETED")
                        st.success("Marked as Completed!")
                        st.rerun()
                    if btn_c3.button("🔄 Sync Log", key="act_sync"):
                        st.rerun()

                    st.markdown("<br/>", unsafe_allow_html=True)

                    # Reading Section: Checks segment view settings
                    st.markdown('<div class="accessibility-header" style="font-size: 1.35rem;">📖 Text Content</div>', unsafe_allow_html=True)
                    text_segments = [s.strip() for s in re.split(r'(?<=[.!?])\s+', excerpt) if s.strip()]
                    
                    # Display segments
                    if "Easy" in accessibility_mode or "Support" in accessibility_mode:
                        curr_idx = st.session_state.current_para_idx
                        if curr_idx >= len(text_segments):
                            curr_idx = 0
                            st.session_state.current_para_idx = 0
                            
                        st.markdown(f'<div class="excerpt-box accessibility-text">"{text_segments[curr_idx]}"</div>', unsafe_allow_html=True)
                        
                        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                        if curr_idx > 0:
                            if nav_col1.button("⬅️ Previous", key="btn_prev_segment"):
                                st.session_state.current_para_idx -= 1
                                st.rerun()
                        if curr_idx < len(text_segments) - 1:
                            if nav_col3.button("Next ➡️", key="btn_next_segment"):
                                st.session_state.current_para_idx += 1
                                st.rerun()
                        nav_col2.write(f"<center>Chunk {curr_idx + 1} of {len(text_segments)}</center>", unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="excerpt-box accessibility-text">"{excerpt}"</div>', unsafe_allow_html=True)

                    st.markdown("<hr/>", unsafe_allow_html=True)

                    # Keyword Tags Display
                    st.markdown('<div class="accessibility-text"><strong>Extracted Keywords:</strong></div>', unsafe_allow_html=True)
                    kw_html = " ".join([f'<span class="badge badge-keyword">{kw}</span>' for kw in extracted_kw])
                    st.markdown(kw_html, unsafe_allow_html=True)
                    st.write("")

                    # --- Interactive SQLite Dictionary definitions column integration ---
                    st.markdown('<div class="accessibility-header" style="font-size: 1.35rem;">📖 Excerpt Dictionary & Vocabulary Lookup</div>', unsafe_allow_html=True)
                    st.write("Understand complex words from this resource with definitions queried directly from the SQLite database:")
                    
                    # Parse dictionary from DB row
                    dict_data = {}
                    if selected.get("dictionary"):
                        try:
                            dict_data = json.loads(selected["dictionary"])
                        except Exception:
                            dict_data = {}
                            
                    if dict_data:
                        # Allow searching within this book's dictionary
                        dict_search = st.text_input("Filter dictionary words:", key="dict_word_search")
                        for word, definition in dict_data.items():
                            if dict_search and dict_search.lower() not in word.lower():
                                continue
                            
                            # Render dictionary word card with study list adding trigger
                            col_w1, col_w2 = st.columns([3, 1])
                            with col_w1:
                                st.markdown(f"<div class='dict-word-box'><strong>🔑 {word.title()}</strong>: {definition}</div>", unsafe_allow_html=True)
                            with col_w2:
                                if st.button(f"🎒 Bookmark Word", key=f"add_vocab_{word}"):
                                    st.session_state.study_list[word] = definition
                                    st.success(f"Added '{word}' to Study List!")
                                    st.rerun()
                    else:
                        st.write("No dictionary definition bookmarks loaded for this basic resource.")

                    st.markdown("<hr/>", unsafe_allow_html=True)

                    # NLP Metrics and Actionable Recommendations
                    st.markdown('<div class="accessibility-header" style="font-size: 1.3rem;">🧠 NLP Reading Support & Recommendations</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="accessibility-text"><strong>Calculated Readability Grade:</strong> {nlp_difficulty["level"]} (Flesch Score: {nlp_difficulty["score"]})</div>', unsafe_allow_html=True)
                    
                    rec_lines = "".join([f"<li>✅ {r}</li>" for r in recs_dict["recommendations"]])
                    st.markdown(f'<div class="rec-box"><ul style="margin: 0; padding-left: 1.2rem;">{rec_lines}</ul></div>', unsafe_allow_html=True)

                    st.markdown("<hr/>", unsafe_allow_html=True)

                    # Interactive AI Tools Simulation Trigger
                    st.markdown('<div class="accessibility-header" style="font-size: 1.25rem;">🛠️ AI Assistance Tools</div>', unsafe_allow_html=True)
                    ai_col1, ai_col2 = st.columns(2)
                    
                    if ai_col1.button("✨ Simplify Excerpt (AI API Layout)", key="btn_simplify"):
                        st.session_state.ai_simplified_view = simplify_text_ai(excerpt, target_level=user_reading_level)
                    if ai_col2.button("🔑 Generate Glossary (AI API Layout)", key="btn_glossary"):
                        st.session_state.ai_glossary_view = generate_glossary_ai(excerpt)

                    # Display outputs
                    if "ai_simplified_view" in st.session_state:
                        st.info(f"**AI Simplified Version ({user_reading_level} Level):**\n\n> {st.session_state.ai_simplified_view}")
                    if "ai_glossary_view" in st.session_state:
                        st.warning("**AI Glossary terms:**\n\n" + 
                                   "\n".join([f"- **{g['word']}**: {g['definition']}" for g in st.session_state.ai_glossary_view]))

                    # Dynamic Comprehension Quiz Check
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    st.markdown('<div class="accessibility-header" style="font-size: 1.25rem;">📝 Quick Comprehension Check</div>', unsafe_allow_html=True)
                    st.write("Test your understanding of the excerpt above:")
                    
                    main_keyword = extracted_kw[0] if extracted_kw else "the subject"
                    quiz_question = f"What is the primary focus of this excerpt regarding '{main_keyword}'?"
                    st.write(f"**Question:** {quiz_question}")
                    
                    options = [
                        f"It explores the fundamental mechanics and historical contexts of {main_keyword}.",
                        f"It argues that {main_keyword} has no relevance to modern science or history.",
                        f"It lists the financial implications of ignoring {main_keyword} research."
                    ]
                    user_ans = st.radio("Choose the correct answer:", options, key="quiz_options")
                    if st.button("Submit Answer", key="btn_quiz_submit"):
                        if user_ans == options[0]:
                            st.success("🎉 Correct! The text examines the core mechanics and context.")
                        else:
                            st.error("❌ Incorrect. Read the passage and try again!")

                    # Summary & Source
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    st.markdown('<div class="accessibility-header" style="font-size: 1.3rem;">📋 Book Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="accessibility-text">{selected["summary"]}</div>', unsafe_allow_html=True)
                    if selected.get("source_url"):
                        st.markdown(f"🔗 [Explore Source Link]({selected['source_url']})")
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Close viewer-container

                    st.write("<br/>", unsafe_allow_html=True)
                    if st.button("Close Resource Reader", key="btn_close_reader"):
                        st.session_state.selected_resource = None
                        st.session_state.current_para_idx = 0
                        if "ai_simplified_view" in st.session_state:
                            del st.session_state["ai_simplified_view"]
                        if "ai_glossary_view" in st.session_state:
                            del st.session_state["ai_glossary_view"]
                        st.rerun()
                else:
                    st.info("Select a book from the left to read its excerpt and activate reading support features.")
    else:
        st.info("💡 Type in the search bar above to begin searching the library archive.")

# --- TAB 2: ANALYZE CUSTOM TEXT ---
with tab2:
    st.write("### 🧪 Real-time Text Analyzer")
    st.write("Paste any paragraph of text below to estimate its reading difficulty, extract keywords, and apply accessibility settings.")
    
    custom_text = st.text_area(
        label="Paste your text here:",
        height=150,
        placeholder="Paste excerpt text here..."
    )
    
    if custom_text.strip():
        custom_difficulty = estimate_reading_difficulty(custom_text)
        custom_keywords = extract_keywords(custom_text, top_n=6)
        custom_recs = get_reading_recommendation(custom_difficulty, user_reading_level=user_reading_level)
        
        col_c1, col_c2 = st.columns([1.5, 1.5])
        
        with col_c1:
            st.write("#### 📊 Readability Score & Level")
            st.metric("Estimated Grade Level", custom_difficulty["level"])
            st.metric("Flesch Reading Ease Index", f"{custom_difficulty['score']} / 100")
            st.write(f"*Analysis: {custom_difficulty['desc']}*")
            st.write(f"- Avg. Sentence Length: {custom_difficulty['average_sentence_length']} words")
            st.write(f"- Avg. Syllables / Word: {custom_difficulty['average_syllables_per_word']}")
            
        with col_c2:
            st.write("#### 🏷️ Extracted Key Terms")
            kw_tags_html = " ".join([f'<span class="badge badge-keyword" style="font-size: 0.85rem; padding: 0.4rem 0.8rem; margin-bottom:0.5rem;">{kw}</span>' for kw in custom_keywords])
            st.markdown(kw_tags_html, unsafe_allow_html=True)
            
            st.write("#### 📢 Actionable Reading Directive")
            custom_rec_lines = "".join([f"<li>✅ {r}</li>" for r in custom_recs["recommendations"]])
            st.markdown(f'<div class="rec-box"><ul style="margin: 0; padding-left: 1.2rem;">{custom_rec_lines}</ul></div>', unsafe_allow_html=True)
            
        # Accessible Display box
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.write("#### 👓 Accessible Display Rendering")
        
        st.markdown('<div class="viewer-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="accessibility-header">Custom Pasted Content</div>', unsafe_allow_html=True)
        
        custom_segments = [s.strip() for s in re.split(r'(?<=[.!?])\s+', custom_text) if s.strip()]
        
        if "Easy" in accessibility_mode or "Support" in accessibility_mode:
            st.write(f"*Segment-by-segment pager enabled ({len(custom_segments)} chunks)*")
            if "custom_para_idx" not in st.session_state:
                st.session_state.custom_para_idx = 0
            
            c_idx = st.session_state.custom_para_idx
            if c_idx >= len(custom_segments):
                c_idx = 0
                st.session_state.custom_para_idx = 0
                
            st.markdown(f'<div class="excerpt-box accessibility-text">"{custom_segments[c_idx]}"</div>', unsafe_allow_html=True)
            
            c_nav1, c_nav2, c_nav3 = st.columns([1, 2, 1])
            if c_idx > 0:
                if c_nav1.button("⬅️ Previous Chunk", key="btn_custom_prev"):
                    st.session_state.custom_para_idx -= 1
                    st.rerun()
            if c_idx < len(custom_segments) - 1:
                if c_nav3.button("Next Chunk ➡️", key="btn_custom_next"):
                    st.session_state.custom_para_idx += 1
                    st.rerun()
            c_nav2.write(f"<center>Chunk {c_idx + 1} of {len(custom_segments)}</center>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="excerpt-box accessibility-text">"{custom_text}"</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
