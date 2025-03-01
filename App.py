import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import requests
from io import BytesIO
import urllib.parse

# Download necessary NLTK resources
nltk.download('punkt')
st.set_page_config(page_title='Briefly: The world in a nutshell', page_icon="📰")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Roboto:wght@400;700&display=swap') !important;

    html, body {
        font-family: 'Roboto', sans-serif !important;
        font-size: 16px !important;
        background-color: #f4f4f4 !important;
    }
    h1 {
        font-size: 24px !important;
        font-family: 'Merriweather', serif !important;
    }
    h2, h3, h4 {
        font-size: 20px !important;
        font-family: 'Merriweather', serif !important;
    }
    img {
        height: 100px !important;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_news_search_topic(topic, lang):
    try:
        encoded_topic = urllib.parse.quote(topic)
        site = f'https://news.google.com/rss/search?q={encoded_topic}&hl={lang}'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

def run():
    st.title("BRIEFLY: THE WORLD IN A NUTSHELL")

    logo_url = "https://drive.google.com/uc?id=1LhZ97smrzmOk9hvaluEv-vupnuK0RHlX"
    logo_response = requests.get(logo_url)
    logo_image = Image.open(BytesIO(logo_response.content))
    st.image(logo_image, width=150)  # Adjusted logo size

    lang_options = {'English': 'en', 'हिंदी': 'hi'}
    selected_lang = st.selectbox("Select Language", list(lang_options.keys()))

    category = ['Trending🔥 News', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)

    if cat_op == category[1]:
        user_topic = st.text_input("Enter your Topic🔍")
        if st.button("Search") and user_topic.strip():
            news_list = fetch_news_search_topic(topic=user_topic, lang=lang_options[selected_lang])
            if news_list:
                st.subheader(f"✅ News related to {user_topic.capitalize()}")
            else:
                st.error(f"No News found for {user_topic}")
        else:
            st.warning("Please write Topic Name to Search🔍")

run()
