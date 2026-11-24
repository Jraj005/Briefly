import calendar, html, time
from urllib.parse import quote_plus
import feedparser
import streamlit as st
st.markdown("""
<style>
a.news-card, a.news-card:hover, a.news-card:visited {
    text-decoration: none !important;
    color: inherit !important;
}
.news-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: .6rem;
    background: #1A1F2B;
    border: 1px solid #2A3142;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin: .5rem 0;
    min-height: 170px;
    transition: transform .2s ease, border-color .2s ease, box-shadow .3s ease;
}
.news-card:hover {
    transform: translateY(-3px);
    border-color: #1E90FF;
    box-shadow: 0 8px 20px rgba(0,0,0,.5);
}
.news-source {
    font-size: .72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #1E90FF;
}
.news-title {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.45;
    color: #FFFFFF;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.pub-date {
    font-size: .8rem;
    color: #9AA4B5;
}
@media (max-width: 700px) {
    .news-card { min-height: 0; padding: 1rem 1.1rem; }
    .news-title { font-size: 1rem; }
}
</style>
""", unsafe_allow_html=True)
LANGS = {
    'English': ('en-IN', 'IN', 'IN:en'), 'हिंदी': ('hi', 'IN', 'IN:hi'),
    'বাংলা': ('bn', 'IN', 'IN:bn'),      'ગુજરાતી': ('gu', 'IN', 'IN:gu'),
    'ಕನ್ನಡ': ('kn', 'IN', 'IN:kn'),       'മലയാളം': ('ml', 'IN', 'IN:ml'),
    'मराठी': ('mr', 'IN', 'IN:mr'),      'தமிழ்': ('ta', 'IN', 'IN:ta'),
    'తెలుగు': ('te', 'IN', 'IN:te'),      'اردو': ('ur', 'IN', 'IN:ur'),
}
BASE = "https://news.google.com/rss"

def build_url(lang, query=None, topic=None):
    hl, gl, ceid = LANGS[lang]
    params = f"hl={hl}&gl={gl}&ceid={ceid}"
    if query:
        return f"{BASE}/search?q={quote_plus(query)}&{params}"
    if topic:
        return f"{BASE}/headlines/section/topic/{topic}?{params}"
    return f"{BASE}?{params}"

@st.cache_data(ttl=600, show_spinner="Fetching headlines…")
def fetch_feed(url):
    feed = feedparser.parse(url, agent="Mozilla/5.0")
    return [{
        "title": e.title.rsplit(" - ", 1)[0],
        "source": e.get("source", {}).get("title", ""),
        "link": e.link,
        "ts": calendar.timegm(e.published_parsed) if e.get("published_parsed") else None,
    } for e in feed.entries]

def time_ago(ts):
    if not ts:
        return ""
    s = int(time.time() - ts)
    if s < 3600:  return f"{max(s // 60, 1)}m ago"
    if s < 86400: return f"{s // 3600}h ago"
    return f"{s // 86400}d ago"

def render(items, limit=18):
    items = items[:limit]
    if not items:
        st.info("No stories found.")
        return
    for i in range(0, len(items), 3):
        for col, it in zip(st.columns(3), items[i:i + 3]):
            col.markdown(f"""
            <a href="{html.escape(it['link'])}" target="_blank" class="news-card">
              <div class="news-source">{html.escape(it['source'])}</div>
              <div class="news-title">{html.escape(it['title'])}</div>
              <div class="pub-date"><i class="lucide-clock"></i>{time_ago(it['ts'])}</div>
            </a>""", unsafe_allow_html=True)

# --- UI ---
with st.sidebar:
    lang = st.selectbox("Language", list(LANGS))

top, cats, search = st.tabs(["🔥 Top Stories", "🗂 Categories", "🔍 Search"])

with top:
    render(fetch_feed(build_url(lang)))

with cats:
    topic = st.pills("Category", ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY",
                                  "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"])
    if topic:
        render(fetch_feed(build_url(lang, topic=topic)))

with search:
    q = st.text_input("Search news", placeholder="e.g. ISRO, Sensex, IPL")
    when = st.segmented_control("Time range", ["Any", "1h", "1d", "7d"], default="Any")
    if q.strip():
        query = q if when == "Any" else f"{q} when:{when}"
        render(fetch_feed(build_url(lang, query=query)))
