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
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Roboto:wght@400;700&display=swap');

    html, body {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        background-color: #f4f4f4;
    }
    h1 {
        font-size: 24px;  /* Title font size */
        font-family: 'Merriweather', serif;
    }
    h2, h3, h4 {
        font-size: 20px;  /* Subtitle font size */
        font-family: 'Merriweather', serif;
    }
    h5, h6 {
        font-size: 18px;  /* Section header font size */
        font-family: 'Merriweather', serif;
    }
    p {
        font-size: 20px;  /* Paragraph font size */
        font-family: 'Merriweather', serif;
    }
    .st-emotion-cache-1r6slb0{
        box-shadow:3px 3px 2px 0px rgba(255,255,255,.65);
        padding: 15px 20px;
            color:white;
        border-radius:15px;
        margin:10px 2px;
            # background-color:#0D0E1F;
            background-color:#252829;
    }
    .st-emotion-cache-1r6slb0:hover{
        transform:scale(1.07);
        z-index:2;
    }
    .st-emotion-cache-144ybaj{
            background-color: white;
            color:black;
            border-radius:12px;
            font-size:18px;
            }
            .st-emotion-cache-19lmkc0{
            text-align:center;}
    .st-emotion-cache-1kyxreq{
            justify-content:center;
            }
    .st-emotion-cache-1y4p8pa{
        max-width:75rem;
        margin:0px 10px;
    }
    .st-emotion-cache-ocqkz7{
            gap:1.2 rem;
    }
    .st-emotion-cache-1v0mbdj{
            width:14rem;
    }
    .st-emotion-cache-10trblm{
        text-align:center;
    }
    #newsslice-news-made-simple{
        font-size:40px;
    }
    .st-emotion-cache-1r6slb0{
        width: calc(25%);
        flex: 1 1 calc(33.3333% - 1.5rem);
    }
    .st-emotion-cache-z22cl0{
        border:none;
            }
    </style>
""", unsafe_allow_html=True)
def fetch_news_search_topic(topic):
    try:
        site = 'https://news.google.com/rss/search?q={}'.format(topic)
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

def fetch_top_news():
    try:
        site = 'https://news.google.com/news/rss'
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        st.error(f"Error fetching top news: {e}")
        return []

def fetch_category_news(topic):
    try:
        site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
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

        with cols[c % 3]:  # Display news in the respective column
            st.markdown(f'**{news.title.text}**')
            news_data = Article(news.link.text)
            try:
                news_data.download()
                news_data.parse()
                news_data.nlp()
            except Exception as e:
                st.error(f"Error processing article: {e}")
                continue  # Skip to the next article if there’s an error

            with st.expander("Read More"):
                st.markdown(f"<h6 style='text-align: justify;'>{news_data.summary}</h6>", unsafe_allow_html=True)
                st.markdown(f"[Read more at {news.source.text}]({news.link.text})")
                st.success("Published Date: " + news.pubDate.text)

        c += 1
        if c >= news_quantity:
            break

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
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[1]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = 21
            news_list = fetch_category_news(chosen_topic)
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
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are some News related to {} for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")

run()
