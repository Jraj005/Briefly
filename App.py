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

    html, body {
        font-family: 'Roboto', sans-serif !important;
        font-size: 16px !important;
        background-color: #f4f4f4 !important;
        width:70% !important;
    }
    h1 {
        font-size: 24px !important;  /* Title font size */
        font-family: 'Merriweather', serif !important;
    }
    h2, h3, h4 {
        font-size: 20px !important;  /* Subtitle font size */
        font-family: 'Merriweather', serif !important;
    }
    h5, h6 {
        font-size: 18px !important;  /* Section header font size */
        font-family: 'Merriweather', serif !important;
    }
    p {
        font-size: 20px !important;  /* Paragraph font size */
        font-family: 'Merriweather', serif !important;
    }
    .css-1r6slb0{
        box-shadow:3px 3px 2px 0px rgba(255,255,255,.65) !important;
        padding: 15px 20px !important;
            color:white !important;
        border-radius:15px !important;
        margin:10px 2px !important;
            background-color:#252829 !important;
    }
    .css-1r6slb0:hover{
        transform:scale(1.07) !important;
        z-index:2 !important;
    }
    .css-144ybaj{
            background-color: white !important;
            color:black !important;
            border-radius:12px !important;
            font-size:18px !important;
            }
    .css-19lmkc0{
            text-align:center !important;}
    .css-1kyxreq{
            justify-content:center !important;
            }
    .css-1y4p8pa{
        max-width:60rem !important;
        margin:0px 10px !important;
    }
    .css-ocqkz7{
            gap:1.2 rem !important;
    }
    .css-1v0mbdj{
        width:14rem !important;
    }
    .css-10trblm{
        text-align:center !important;
    }
    #newsslice-news-made-simple{
        font-size:40px !important;
    }
    .st-4brx5n{
        display: flex;
        justify-content: center;
    }
    img{
        height: 40vh;
    }
    .css-1r6slb0{
        width: calc(25%) !important;
        flex: 1 1 calc(33.3333% - 1.5rem) !important;
    }
    .css-1epmw04{
        border:none !important;
    }
    .st-bh{
        border:none;
    }
    .st-dv{
        color:black;
    }
    .st-da{
        border:none;
    }
    .st-do{
        background-color:white;
        color:black;
        border-radius:20px;
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
        news_list = sp_page.find_all('item')
        return news_list
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
        news_list = sp_page.find_all('item')
        return news_list
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
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching category news: {e}")
        return []

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        return image
    except Exception:
        return Image.open('./Meta/no_image.jpg')

def display_news(list_of_news, news_quantity):
    cols = st.columns(3)  # Create three columns for desktop view
    c = 0

    for news in list_of_news:
        if c % 3 == 0 and c != 0:  # For every third news item, create new columns
            cols = st.columns(3)

    with cols[c % 3]:  # Distribute cards evenly across columns
    card_container = st.container()
    
    with card_container:
        st.markdown(f"<b>{news.title.text}</b>", unsafe_allow_html=True)

        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(f"Error processing article: {e}")
            continue

        st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)  # Pushes expander to bottom

        with st.expander("Read More"):
            st.markdown(f"<p style='text-align: justify;'>{news_data.summary}</p>", unsafe_allow_html=True)
            st.markdown(f"[Read more at {news.source.text}]({news.link.text})")
            st.success("Published Date: " + news.pubDate.text)



        c += 1
        if c >= news_quantity:
            break

def run():

    st.title("BRIEFLY: THE WORLD IN A NUTSHELL")

    # Updated Logo URL
    logo_url = "https://drive.google.com/uc?id=1LhZ97smrzmOk9hvaluEv-vupnuK0RHlX"
    logo_response = requests.get(logo_url)
    logo_image = Image.open(BytesIO(logo_response.content))
    st.markdown(
    "<div style='text-align: center;'>"
    "<img src='https://drive.google.com/uc?id=1LhZ97smrzmOk9hvaluEv-vupnuK0RHlX' width='200'>"
    "</div>", 
    unsafe_allow_html=True
)
    # Language Selection
    lang_options = {
        'English': 'en',
        'हिंदी': 'hi',
        'বাংলা': 'bn',
        'ગુજરાતી': 'gu',
        'ಕನ್ನಡ': 'kn',
        'മലയാളം': 'ml',
        'मराठी': 'mr',
        'தமிழ்': 'ta',
        'తెలుగు': 'te',
        'उर्दू': 'ur'
    }
    selected_lang = st.selectbox("Select Language", list(lang_options.keys()))

    category = ['Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)

    if cat_op == category[0]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = 21
        news_list = fetch_top_news(lang_options[selected_lang])
        display_news(news_list, no_of_news)
    elif cat_op == category[1]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = 21
            news_list = fetch_category_news(chosen_topic, lang_options[selected_lang])
            if news_list:
                st.subheader("✅ Here are some {} News for you".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(chosen_topic))

    elif cat_op == category[2]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = 21

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr, lang=lang_options[selected_lang])
            if news_list:
                st.subheader("✅ Here are some News related to {} for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")

run()
