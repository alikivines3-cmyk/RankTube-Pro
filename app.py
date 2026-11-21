import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0a0a0f; color: white; }
h1, h2, h3 { color: white !important; }
.logo-box { display: flex; align-items: center; gap: 15px; background: #1a1a2e; padding: 12px 18px; border-radius: 18px; border: 1px solid #333; }
.logo-circle { width: 60px; height: 60px; background: linear-gradient(135deg, #FF0000, #FF6B00); border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }
.logo-play { color: white; font-size: 28px; margin-left: 4px; }
.logo-arrow { position: absolute; top: -6px; right: -6px; background: white; color: #FF0000; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; }
.hero { background: linear-gradient(135deg, #FF0000, #FF6B00); padding: 25px 15px; border-radius: 20px; text-align: center; }
.box-red { background: linear-gradient(135deg, #FF0000, #FF6B00); border-radius: 16px; padding: 18px 10px; text-align: center; min-height: 140px; }
.box-blue { background: linear-gradient(135deg, #0066FF, #00CCFF); border-radius: 16px; padding: 18px 10px; text-align: center; min-height: 140px; }
.box-green { background: linear-gradient(135deg, #00AA44, #00DD77); border-radius: 16px; padding: 18px 10px; text-align: center; min-height: 140px; }
.box-purple { background: linear-gradient(135deg, #7A00FF, #FF00AA); border-radius: 16px; padding: 18px 10px; text-align: center; min-height: 140px; }
.stButton>button { background: linear-gradient(90deg, #FF0000, #FF6B00); color: white; border: none; border-radius: 25px; padding: 10px 20px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "connected_channel" not in st.session_state:
    st.session_state.connected_channel = ""

try:
    YOUTUBE_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
except:
    YOUTUBE_KEY = ""
    GEMINI_KEY = ""

COUNTRIES = {"Pakistan": "PK", "India": "IN", "USA": "US", "UK": "GB", "UAE": "AE", "Saudi Arabia": "SA", "Bangladesh": "BD", "Canada": "CA"}

@st.cache_data(ttl=600)
def call_gemini_cached(prompt):
    gem_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    gr = requests.post(gem_url, json=payload, timeout=30).json()
    try:
        return gr["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI Error - Try Again"

@st.cache_data(ttl=600)
def get_channel_data_cached(query):
    if query.startswith("@"):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=channel&key={YOUTUBE_KEY}"
        r = requests.get(url, timeout=15).json()
        if "items" in r and len(r["items"]) > 0:
            real_id = r["items"][0]["snippet"]["channelId"]
        else:
            return None
    else:
        real_id = query
    url2 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings&id={real_id}&key={YOUTUBE_KEY}"
    r = requests.get(url2, timeout=15).json()
    if "items" in r and len(r["items"]) > 0:
        return r["items"][0]
    return None

def get_channel_videos(channel_id, max_n=3):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&type=video&maxResults={max_n}&key={YOUTUBE_KEY}"
    r = requests.get(url, timeout=15).json()
    return r.get("items", [])

st.markdown("""
<div class="logo-box">
    <div class="logo-circle"><div class="logo-play">▶</div><div class="logo-arrow">↗</div></div>
    <div><h1 style="margin:0; font-size:32px;">RANK<span style="color:#FF0000;">TUBE</span> PRO 📈</h1><p style="margin:0; color:#ccc;">Fast | AI Powered | Grow Fast</p></div>
</div>
""", unsafe_allow_html=True)
st.write("---")

if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero">
        <div style="font-size:50px;">🚀</div>
        <h1 style="color:white; font-size:36px;">Grow Your YouTube 10X Faster</h1>
        <p style="color:white;">AI Titles | Country Trends | Audit | Competitor</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="box-red"><div style="font-size:36px;">🤖</div><h3>AI TITLES</h3><p>Viral Titles In 10 Sec</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="box-blue"><div style="font-size:36px;">🌍</div><h3>COUNTRY TRENDS</h3><p>Trends By Country</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="box-green"><div style="font-size:36px;">📊</div><h3>AUDIT</h3><p>Score Out Of 100</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="box-purple"><div style="font-size:36px;">⚔️</div><h3>COMPETITOR</h3><p>Beat Competitor</p></div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("STEP 1: SIGN UP WITH GOOGLE")
    email = st.text_input("Enter Your Gmail", placeholder="example@gmail.com")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("Continue With Google"):
            if "@" in email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Enter Valid Gmail")
    with col_g2:
        if st.button("Continue As Guest"):
            st.session_state.logged_in = True
            st.session_state.user_email = "Guest User"
            st.rerun()
    st.stop()

st.success(f"Welcome: {st.session_state.user_email}")
col_logout, col_conn = st.columns([1, 3])
with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.connected_channel = ""
        st.rerun()
with col_conn:
    if st.session_state.connected_channel:
        st.success(f"Connected: {st.session_state.connected_channel}")
    else:
        st.warning("Channel Not Connected")

with st.expander("STEP 2: CONNECT CHANNEL", expanded=(st.session_state.connected_channel == "")):
    conn_input = st.text_input("Enter Channel Name", "@AliMahiVlogs")
    if st.button("Connect Channel"):
        d = get_channel_data_cached(conn_input)
        if d:
            st.session_state.connected_channel = conn_input
            st.success(f"Connected: {d['snippet']['title']}")
            st.rerun()
        else:
            st.error("Not Found")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Dashboard", "Title", "Trends", "RPM", "Competitor", "Thumbnail", "Audit"])

with tab1:
    st.header("Channel Dashboard")
    ch = st.text_input("Channel", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Channel Data"):
        with st.spinner("Loading..."):
            data = get_channel_data_cached(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            col_logo, col_info = st.columns([1, 4])
            with col_logo:
                st.image(snip["thumbnails"]["high"]["url"], width=100)
            with col_info:
                st.subheader(snip["title"])
                st.write(snip.get("description", "")[:200])
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subs", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Videos", stats.get("videoCount", "0"))
            avg_val = int(stats.get("viewCount", "0")) // max(int(stats.get("videoCount", "1")), 1)
            c4.metric("Avg Views", f"{avg_val:,}")
            st.subheader("Latest Videos - Click To Watch")
            vids = get_channel_videos(cid, 3)
            for v in vids:
                vid = v["id"]["videoId"]
                col_t, col_b = st.columns([1, 3])
                with col_t:
                    st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                with col_b:
                    st.write(f"**{v['snippet']['title'][:70]}**")
                    st.link_button("Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
                    if st.button(f"Play Video - {vid[:6]}", key=f"play_{vid}"):
                        st.video(f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Not Found")

with tab2:
    st.header("AI Title Generator")
    topic = st.text_input("Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI"):
        with st.spinner("AI Thinking - 15 Sec Wait - Do Not Click Again"):
            result = call_gemini_cached(f"For {niche} channel topic {topic}: Give 5 viral titles, 30 sec script, 10 hashtags, best time. In English.")
        st.write(result)

with tab3:
    st.header("Trends By Country")
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        selected_country_name = st.selectbox("Select Country", list(COUNTRIES.keys()), index=0)
    with col_c2:
        trend_category = st.selectbox("Category", ["All", "Gaming", "Vlog", "News", "Islamic", "Food", "Tech", "Cricket"])
    selected_code = COUNTRIES[selected_country_name]
    st.write(f"Selected: {selected_country_name}")
    if st.button(f"Get Google Trends - {selected_country_name}"):
        with st.spinner("Fetching..."):
            res = call_gemini_cached(f"Google Trends for {selected_country_name}, category {trend_category}. Top 10 keywords, volume, 1 video idea each, 5 rising. In English.")
        st.write(res)
    if st.button(f"Load YouTube Trending - {selected_country_name}"):
        with st.spinner("Loading..."):
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={selected_code}&maxResults=6&key={YOUTUBE_KEY}"
            r = requests.get(url, timeout=15).json()
        if "items" in r:
            for v in r["items"]:
                vid = v["id"]
                col_t, col_b = st.columns([1, 3])
                with col_t:
                    st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                with col_b:
                    st.write(f"**{v['snippet']['title'][:70]}**")
                    st.write(f"{v['snippet']['channelTitle']} | Views {int(v['statistics'].get('viewCount', '0')):,}")
                    st.link_button("Watch", f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Not Found")

with tab4:
    st.header("RPM Calculator - Fast, No AI Needed")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Niche?", ["Vlog - 1 Dollar", "Gaming - 1.5 Dollar", "Tech - 3 Dollar", "Finance - 5 Dollar", "Islamic - 1.2 Dollar", "Food - 1.8 Dollar"])
    rpm_val = float(niche_rpm.split("-")[1].strip().split(" ")[0])
    earning = (views / 1000) * rpm_val
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly Dollar", f"{earning:.2f} USD")
    c2.metric("Monthly Rupees", f"{earning*280:,.0f} PKR")
    c3.metric("Yearly Dollar", f"{earning*12:.2f} USD")

with tab5:
    st.header("Competitor Analysis")
    comp = st.text_input("Competitor Name", "@DuckyBhai")
    if st.button("Analyze Competitor"):
        with st.spinner("Analyzing..."):
            data = get_channel_data_cached(comp)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            st.image(snip["thumbnails"]["high"]["url"], width=100)
            st.subheader(snip["title"])
            c1, c2, c3 = st.columns(3)
            c1.metric("Subs", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Videos", stats.get("videoCount", "0"))
            if st.button("How To Beat Them?"):
                beat = call_gemini_cached(f"Competitor {snip['title']} has {stats.get('subscriberCount')} subs. How to beat them? 5 strategies.")
                st.write(beat)
        else:
            st.error("Not Found")

with tab6:
    st.header("Thumbnail Ideas")
    th_topic = st.text_input("Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas"):
        with st.spinner("AI Designing..."):
            thumb = call_gemini_cached(f"For topic {th_topic} give 5 viral thumbnail ideas. Text, Color, Face, Background. For Pakistani audience.")
        st.write(thumb)

with tab7:
    st.header("Channel Audit - Fast")
    audit_ch = st.text_input("Channel To Audit", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="audit_ch")
    if st.button("Run Audit"):
        with st.spinner("Auditing..."):
            data = get_channel_data_cached(audit_ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            subs = int(stats.get("subscriberCount", "0"))
            views = int(stats.get("viewCount", "0"))
            vcount = int(stats.get("videoCount", "0"))
            avg_views = views // max(vcount, 1)
            score = 0
            if subs >= 1000:
                score = score + 25
            elif subs >= 100:
                score = score + 15
            else:
                score = score + 10
            if vcount >= 20:
                score = score + 25
            elif vcount >= 5:
                score = score + 10
            if avg_views >= 1000:
                score = score + 25
            elif avg_views >= 100:
                score = score + 15
            else:
                score = score + 5
            if len(snip.get("description", "")) > 100:
                score = score + 10
            else:
                score = score + 3
            if score > 100:
                score = 100
            st.markdown(f"### Score: {score} / 100")
            st.progress(score / 100)
            c1, c2, c3 = st.columns(3)
            c1.metric("Subs", f"{subs:,}")
            c2.metric("Views", f"{views:,}")
            c3.metric("Avg Views", f"{avg_views:,}")
            ai_audit = call_gemini_cached(f"Audit channel {snip['title']}, Subs {subs}, Views {views}, Videos {vcount}, Avg {avg_views}, Score {score}/100. Give 5 fixes in Pakistan.")
            st.write(ai_audit)
        else:
            st.error("Not Found")

st.write("---")
st.write("RANKTUBE PRO | Ali Mahi | Version 8.0 FAST")
