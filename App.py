import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import requests
from io import BytesIO

# Download necessary NLTK resources
nltk.download('punkt')
st.set_page_config(page_title='Briefly: The world in a nutshell', page_icon="📰")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Roboto:wght@400;700&display=swap') !important;
    /* Add your custom styling here */
    </style>
""", unsafe_allow_html=True)

# Dictionary of Indian languages and their Google News language codes
languages = {
    'Assamese': 'as', 'Bengali': 'bn', 'Gujarati': 'gu', 'Hindi': 'hi', 'Kannada': 'kn',
    'Malayalam': 'ml', 'Marathi': 'mr', 'Odia': 'or', 'Punjabi': 'pa', 'Tamil': 'ta',
    'Telugu': 'te', 'Urdu': 'ur', 'English': 'en', 'Konkani': 'kok', 'Maithili': 'mai',
    'Nepali': 'ne', 'Bodo': 'brx', 'Dogri': 'doi', 'Kashmiri': 'ks', 'Manipuri': 'mni',
    'Santali': 'sat', 'Sindhi': 'sd'
}

def fetch_news_search_topic(topic, lang_code):
    try:
        site = f'https://news.google.com/rss/search?q={topic}&hl={lang_code}&gl=IN'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

def fetch_top_news(lang_code):
    try:
        site = f'https://news.google.com/news/rss?hl={lang_code}&gl=IN'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching top news: {e}")
        return []

def fetch_category_news(topic, lang_code):
    try:
        site = f'https://news.google.com/news/rss/headlines/section/topic/{topic}?hl={lang_code}&gl=IN'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching category news: {e}")
        return []

# Function to display news articles
def display_news(list_of_news, news_quantity):
    cols = st.columns(3)
    c = 0
    for news in list_of_news:
        if c % 3 == 0 and c != 0:
            cols = st.columns(3)
        with cols[c % 3]:
            st.markdown(f'**{news.title.text}**')
            news_data = Article(news.link.text)
            try:
                news_data.download()
                news_data.parse()
                news_data.nlp()
            except Exception as e:
                st.error(f"Error processing article: {e}")
                continue
            with st.expander("Read More"):
                st.markdown(f"<h6 style='text-align: justify;'>{news_data.summary}</h6>", unsafe_allow_html=True)
                st.markdown(f"[Read more at {news.source.text}]({news.link.text})")
                st.success("Published Date: " + news.pubDate.text)
        c += 1
        if c >= news_quantity:
            break

# Main app function
def run():
    st.title("BRIEFLY: THE WORLD IN A NUTSHELL")
    # shared_link = "https://drive.google.com/file/d/1K1fzEgjXHO2gOMUAPvJ6HEvHyvKaLFFC/view?usp=sharing"
    shared_link = "https://drive.google.com/file/d/1LhZ97smrzmOk9hvaluEv-vupnuK0RHlX/view?usp=sharing"
    file_id = shared_link.split('/d/')[1].split('/')[0]
    download_url = f"https://drive.google.com/uc?id={file_id}"

    response = requests.get(download_url)
    response.raise_for_status()  # Check for request errors

    image = Image.open(BytesIO(response.content))
    st.image(image, use_column_width=False)

    category = ['Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)

    if cat_op == category[0]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = 21
        news_list = fetch_top_news(lang_code)
        display_news(news_list, no_of_news)
    elif cat_op == category[1]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = 21
            news_list = fetch_category_news(chosen_topic, lang_code)
            if news_list:
                st.subheader(f"✅ Here are some {chosen_topic} News for you")
                display_news(news_list, no_of_news)
            else:
                st.error(f"No News found for {chosen_topic}")

    elif cat_op == category[2]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = 21
        if st.button("Search") and user_topic:
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(user_topic_pr, lang_code)
            if news_list:
                st.subheader(f"✅ Here are some News related to {user_topic.capitalize()} for you")
                display_news(news_list, no_of_news)
            else:
                st.error(f"No News found for {user_topic}")
        else:
            st.warning("Please write Topic Name to Search🔍")

run()
