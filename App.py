import calendar, html, time
from urllib.parse import quote_plus
import feedparser
import streamlit as st

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
