import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import requests
from io import BytesIO

nltk.download('punkt')
st.set_page_config(page_title='Briefly: The world in a nutshell', page_icon="📰")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Roboto:wght@400;700&display=swap');

    html, body {
        font-family: 'Roboto', sans-serif !important;
        font-size: 16px !important;
        background-color: #f4f4f4 !important;
    }
    h1, h2, h3, h4 {
        font-family: 'Merriweather', serif !important;
    }
    .news-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .news-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        width: 30%;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .news-card h6 {
        text-align: justify;
    }
    .news-expander {
        margin-top: auto;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

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

def display_news(list_of_news, news_quantity):
    st.markdown('<div class="news-container">', unsafe_allow_html=True)
    c = 0
    for news in list_of_news:
        if c >= news_quantity:
            break
        
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception:
            continue
        
        st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
        st.markdown(f'**{news.title.text}**')
        with st.expander("Read More", expanded=False):
            st.markdown(f"<h6>{news_data.summary}</h6>", unsafe_allow_html=True)
            st.markdown(f"[Read more at {news.source.text}]({news.link.text})")
            st.success("Published Date: " + news.pubDate.text)
        st.markdown('</div>', unsafe_allow_html=True)
        c += 1
    st.markdown('</div>', unsafe_allow_html=True)

def run():
    st.title("BRIEFLY: THE WORLD IN A NUTSHELL")
    logo_url = "https://drive.google.com/uc?id=1LhZ97smrzmOk9hvaluEv-vupnuK0RHlX"
    logo_response = requests.get(logo_url)
    logo_image = Image.open(BytesIO(logo_response.content))
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo_image, use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

    lang_options = {'English': 'en', 'हिंदी': 'hi'}
    selected_lang = st.selectbox("Select Language", list(lang_options.keys()))

    category = ['Trending🔥 News', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)

    if cat_op == category[0]:
        st.subheader("✅ Trending🔥 News")
        news_list = fetch_news_search_topic("top news", lang_options[selected_lang])
        display_news(news_list, 21)
    elif cat_op == category[1]:
        user_topic = st.text_input("Enter your Topic🔍")
        if st.button("Search") and user_topic:
            news_list = fetch_news_search_topic(user_topic, lang_options[selected_lang])
            if news_list:
                st.subheader(f"✅ News on {user_topic.capitalize()}")
                display_news(news_list, 21)
            else:
                st.error(f"No News found for {user_topic}")

run()
