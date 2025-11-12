import streamlit as st
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import nltk

# Download NLTK resource
nltk.download('punkt')

# --- Page Config ---
st.set_page_config(
    page_title="Briefly: The World in a Nutshell",
    page_icon="📰",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Merriweather:wght@400;700&display=swap');
    @import url('https://unpkg.com/lucide-static@latest/font/lucide.css');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }

    h1, h2, h3 {
        font-family: 'Merriweather', serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }

    /* News card */
    .news-card {
        background: #4e5769;
        border-radius: 14px;
        padding: 1.8em 2em;
        margin: 1em 0;
        transition: transform 0.2s ease, box-shadow 0.3s ease;
        box-shadow: -9px 6px 8px 3px rgb(0 0 0 / 63%);
        cursor: pointer;
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 200px;
        max-height: 200px;
        overflow: hidden;
    }

    .news-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.6);
        background: #4d5962;
    }

    .news-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF;
        line-height: 1.5;
        margin-bottom: auto;
        padding-bottom: 0.5em;
        overflow-wrap: break-word;
        flex-grow: 1;
    }

    .news-summary {
        font-size: 0.95rem;
        color: #C7C7C7;
        line-height: 1.5;
        margin-bottom: 10px;
    }

    .pub-date {
        font-size: 0.85rem;
        color: #D1D1D1;
        margin-top: auto;
        padding-top: 0.5em;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    i {
        color: #1E90FF;
        font-size: 1.1rem;
        vertical-align: middle;
    }

    /* Widgets */
    .stSelectbox label, .stTextInput label {
        font-weight: 500;
        color: #FFFFFF !important;
    }

    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #0078FF;
        transform: scale(1.03);
    }

    @media (max-width: 1000px) {
        .news-card {
            min-height: 180px;
            max-height: 180px;
            padding: 1.5em;
        }
        .news-title {
            font-size: 1rem;
        }
    }

    @media (max-width: 700px) {
        .news-card {
            min-height: 160px;
            max-height: 160px;
            padding: 1.2em;
        }
        .news-title {
            font-size: 0.95rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


# --- Fetch Functions ---
def fetch_news_search_topic(topic, lang):
    try:
        site = f'https://news.google.com/rss/search?q={topic}&hl={lang}'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        return sp_page.find_all('item')
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []


def fetch_top_news(lang):
    try:
        site = f'https://news.google.com/news/rss?hl={lang}&gl=IN'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        return sp_page.find_all('item')
    except Exception as e:
        st.error(f"Error fetching top news: {e}")
        return []


def fetch_category_news(topic, lang):
    try:
        site = f'https://news.google.com/news/rss/headlines/section/topic/{topic}?hl={lang}'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        return sp_page.find_all('item')
    except Exception as e:
        st.error(f"Error fetching category news: {e}")
        return []


# --- Display News ---
def display_news(news_list, limit=18):
    cols = st.columns(3)
    count = 0

    for news in news_list:
        if count % 3 == 0 and count != 0:
            cols = st.columns(3)

        with cols[count % 3]:
            try:
                article = Article(news.link.text)
                article.download()
                article.parse()
                article.nlp()

                card_html = f"""
                <a href="{news.link.text}" target="_blank" class="news-card">
                    <div class="news-title">{news.title.text}</div>
                    <div class="pub-date"><i class="lucide-calendar"></i>{news.pubDate.text}</div>
                </a>
                """
                st.markdown(card_html, unsafe_allow_html=True)

            except Exception as e:
                st.warning(f"Could not load article: {e}")

        count += 1
        if count >= limit:
            break


# --- Main Application ---
def run():
    st.markdown("""
        <h1 style='display:flex; flex-direction:column; font-size: 6em; align-items:center; gap:0.5rem;'>
            <i class='lucide-earth'></i> Briefly<span><h5> The World in a Nutshell</h5></span>
        </h1>
    """, unsafe_allow_html=True)

    lang_options = {
        'English': 'en', 'हिंदी': 'hi', 'বাংলা': 'bn', 'ગુજરાતી': 'gu',
        'ಕನ್ನಡ': 'kn', 'മലയാളം': 'ml', 'मराठी': 'mr', 'தமிழ்': 'ta',
        'తెలుగు': 'te', 'उर्दू': 'ur'
    }
    selected_lang = st.selectbox("Select Language", list(lang_options.keys()))

    category = ['Top Stories', 'Explore by Category', 'Discover by Keyword']
    choice = st.selectbox("Select Section", category)

    if choice == category[0]:
        st.subheader("Top Stories", divider="gray")
        display_news(fetch_top_news(lang_options[selected_lang]))

    elif choice == category[1]:
        topics = ['Choose Category', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY',
                  'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        selected_topic = st.selectbox("Select a Category", topics)
        if selected_topic != 'Choose Category':
            st.subheader(f"{selected_topic.title()} News", divider="gray")
            display_news(fetch_category_news(
                selected_topic, lang_options[selected_lang]))
        else:
            st.info("Please select a category above.")

    elif choice == category[2]:
        user_topic = st.text_input("Enter a keyword to search")
        if st.button("Search") and user_topic.strip():
            topic_query = user_topic.replace(' ', '+')
            st.subheader(
                f"News related to '{user_topic.capitalize()}'", divider="gray")
            display_news(fetch_news_search_topic(
                topic_query, lang_options[selected_lang]))
        else:
            st.info("Type a keyword to search for news.")


run()
