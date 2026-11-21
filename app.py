import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")

st.markdown("""
<style>
.main { background-color: #0f0f0f; }
.stApp { background-color: #0f0f0f; color: white; }
h1, h2, h3 { color: white !important; }
.logo-box { display: flex; align-items: center; gap: 15px; }
.logo-circle { width: 70px; height: 70px; background: linear-gradient(135deg, #FF0000, #FF4444); border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 20px rgba(255,0,0,0.5); }
.logo-play { color: white; font-size: 32px; margin-left: 5px; }
.logo-arrow { position: absolute; top: -8px; right: -8px; background: white; color: #FF0000; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; border: 2px solid #FF0000; }
.hero { background: linear-gradient(135deg, #FF0000, #7a0000); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; }
.feature-card { background: #1a1a1a; border: 1px solid #333; border-radius: 15px; padding: 20px; text-align: center; }
div[data-testid="stMetric"] { background: linear-gradient(135deg, #1e1e1e, #2a2a2a); border: 1px solid #333; border-radius: 12px; padding: 15px; }
div[data-testid="stMetric"] label { color: #aaa !important; }
div[data-testid="stMetric"] div { color: white !important; }
.stButton>button { background: linear-gradient(90deg, #FF0000, #FF4444); color: white; border: none; border-radius: 25px; padding: 10px 25px; font-weight: bold; width: 100%; }
.country-box { background: #1a1a1a; border: 2px solid #FF0000; border-radius: 15px; padding: 15px; }
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

# ===== COUNTRY LIST - YOUTUBE CODE KE SAATH =====
COUNTRIES = {
    "🇵🇰 Pakistan": "PK",
    "🇮🇳 India": "IN",
    "🇺🇸 USA": "US",
    "🇬🇧 UK": "GB",
    "🇦🇪 UAE": "AE",
    "🇸🇦 Saudi Arabia": "SA",
    "🇧🇩 Bangladesh": "BD",
    "🇹🇷 Turkey": "TR",
    "🇨🇦 Canada": "CA",
    "🇦🇺 Australia": "AU",
    "🇩🇪 Germany": "DE",
    "🇫🇷 France": "FR",
    "🇮🇩 Indonesia": "ID",
    "🇲🇾 Malaysia": "MY",
    "🌍 Worldwide": "US"
}

def call_gemini(prompt):
    gem_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    gr = requests.post(gem_url, json=payload).json()
    try:
        return gr["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI Error - Try Again"

def get_channel_data(query):
    if query.startswith("@"):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=channel&key={YOUTUBE_KEY}"
        r = requests.get(url).json()
        if "items" in r and len(r["items"]) > 0:
            real_id = r["items"][0]["snippet"]["channelId"]
        else:
            return None
    else:
        real_id = query
    url2 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings&id={real_id}&key={YOUTUBE_KEY}"
    r = requests.get(url2).json()
    if "items" in r and len(r["items"]) > 0:
        return r["items"][0]
    return None

def get_channel_videos(channel_id, max_n=6):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&type=video&maxResults={max_n}&key={YOUTUBE_KEY}"
    r = requests.get(url).json()
    return r.get("items", [])

st.markdown("""
<div class="logo-box">
    <div class="logo-circle"><div class="logo-play">▶</div><div class="logo-arrow">↗</div></div>
    <div><h1 style="margin:0; font-size:38px;">RANK<span style="color:#FF0000;">TUBE</span> <span style="color:#FF0000;">PRO</span> <span style="font-size:20px;">📈</span></h1>
    <p style="margin:0; color:#aaa;">Pakistan's No.1 YouTube Growth Tool | AI Powered | Grow Fast ↗</p></div>
</div>
""", unsafe_allow_html=True)
st.write("---")

if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero">
        <h1 style="color:white; font-size:42px;">🚀 Grow Your YouTube Channel 10X Faster</h1>
        <p style="color:white; font-size:18px;">AI Titles | Country Wise Trends | Channel Audit | Competitor Spy</p>
        <p style="color:#ffcccc;">Join 5,000+ Creators Using RANKTUBE PRO</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="feature-card"><h2>🤖 AI Titles</h2><p>Viral Titles In 10 Sec</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><h2>🌍 Country Trends</h2><p>Trends By Country</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feature-card"><h2>📊 Channel Audit</h2><p>Score Out Of 100</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="feature-card"><h2>⚔️ Competitor Spy</h2><p>Beat Competitor</p></div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("🔐 Step 1: Sign Up With Google")
    email = st.text_input("Enter Your Gmail", placeholder="example@gmail.com")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("🔵 Continue With Google"):
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

st.success(f"👋 Welcome: {st.session_state.user_email}")
col_logout, col_conn = st.columns([1, 3])
with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.connected_channel = ""
        st.rerun()
with col_conn:
    if st.session_state.connected_channel:
        st.success(f"🔗 Connected: {st.session_state.connected_channel}")
    else:
        st.warning("⚠️ Channel Not Connected")

with st.expander("🔗 Step 2: Connect Your Channel", expanded=(st.session_state.connected_channel=="")):
    conn_input = st.text_input("Enter Channel @Name", "@AliMahiVlogs")
    if st.button("🔗 Connect Channel"):
        d = get_channel_data(conn_input)
        if d:
            st.session_state.connected_channel = conn_input
            st.success(f"✅ Connected: {d['snippet']['title']}")
            st.rerun()
        else:
            st.error("Not Found")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Dashboard", "✍️ Title + Script", "🌍 Trends By Country", "💰 RPM Calculator", "⚔️ Competitor", "🖼️ Thumbnail", "✅ Channel Audit"])

with tab1:
    st.header("📊 Channel Dashboard")
    ch = st.text_input("Channel", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Full Channel Data"):
        with st.spinner("Loading..."):
            data = get_channel_data(ch)
        if data:
            stats = data["statistics"]; snip = data["snippet"]; cid = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            col_logo, col_info = st.columns([1, 4])
            with col_logo: st.image(snip["thumbnails"]["high"]["url"], width=130)
            with col_info:
                st.subheader(f"✅ {snip['title']}")
                st.write(snip.get("description", "")[:300])
                st.link_button("🔴 Visit On YouTube", f"https://www.youtube.com/channel/{cid}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subscribers", f"{int(stats.get('subscriberCount','0')):,}")
            c2.metric("Total Views", f"{int(stats.get('viewCount','0')):,}")
            c3.metric("Total Videos", stats.get("videoCount", "0"))
            avg = int(stats.get("viewCount","0")) // max(int(stats.get("videoCount","1")),1)
            c4.metric("Avg Views", f"{avg:,}")
            st.subheader("🎬 Latest Videos")
            vids = get_channel_videos(cid, 6)
            for i in range(0, len(vids), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i+j < len(vids):
                        v = vids[i+j]; vid = v["id"]["videoId"]
                        with col:
                            st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                            st.write(f"**{v['snippet']['title'][:60]}...**")
                            st.video(f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Not Found")

with tab2:
    st.header("✍️ AI Title + Script Generator")
    topic = st.text_input("Video Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI ✨"):
        with st.spinner("AI Thinking..."):
            st.write(call_gemini(f"For Pakistani YouTube {niche} channel, topic '{topic}': Give 1) 5 viral titles Urdu+English mix 2) 30 sec script 3) 10 hashtags 4) Best upload time Pakistan. In English."))

with tab3:
    st.header("🌍 Trends By Country - Select Country")
    st.write("Ab Tum Jis Country Ka Trend Dekhna Chahte Ho, Wo Select Karo - Us Country Ka Asli Trend Aayega")
    # ===== COUNTRY SELECTOR - YE NAYA HAI =====
    st.markdown('<div class="country-box">', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        selected_country_name = st.selectbox("🌍 Select Country For Trends", list(COUNTRIES.keys()), index=0)
    with col_c2:
        trend_category = st.selectbox("Category", ["All", "Gaming", "Vlog", "News", "Islamic", "Food", "Tech", "Cricket", "Music"])
    selected_code = COUNTRIES[selected_country_name]
    st.write(f"Selected: **{selected_country_name}** - Code: **{selected_code}**")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader(f"📈 Google Trends In {selected_country_name}")
    st.write(f"Google Par {selected_country_name} Me Log Kya Search Kar Rahe Hain?")
    if st.button(f"Get Google Trends - {selected_country_name} 🔍"):
        with st.spinner(f"Fetching Google Trends For {selected_country_name}..."):
            res = call_gemini(f"Give REAL Google Trends for country {selected_country_name} right now. Category {trend_category}. Give Top 10 most searched keywords on Google in {selected_country_name} today, with search volume High/Medium/Low, and 1 YouTube video idea for each keyword. Also give 5 Rising keywords that are suddenly growing. Also give what people are searching in {selected_country_name} language. In English, clear table format.")
        st.write(res)
    st.write("---")
    st.subheader(f"🎬 YouTube Trending Videos In {selected_country_name} - Watch Here")
    st.write(f"YouTube Par {selected_country_name} Me Kya Trending Hai? Asli Videos")
    if st.button(f"Load YouTube Trending - {selected_country_name} 🔥"):
        with st.spinner(f"Loading YouTube Trending For {selected_country_name}..."):
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={selected_code}&maxResults=9&key={YOUTUBE_KEY}"
            r = requests.get(url).json()
        if "items" in r and len(r["items"]) > 0:
            st.success(f"✅ Showing Top Trending Videos In {selected_country_name}")
            for i in range(0, len(r["items"]), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i+j < len(r["items"]):
                        v = r["items"][i+j]; vid = v["id"]
                        with col:
                            st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                            st.write(f"🔥 TRENDING #{i+j+1} IN {selected_country_name}")
                            st.write(f"**{v['snippet']['title'][:60]}...**")
                            st.write(f"📺 {v['snippet']['channelTitle']} | 👁️ {int(v['statistics'].get('viewCount','0')):,} Views")
                            st.video(f"https://www.youtube.com/watch?v={vid}")
                            st.link_button("▶️ Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error(f"No Trending Found For {selected_country_name} - Try Another Country")
    st.write("---")
    st.subheader("⚖️ Compare 2 Countries")
    st.write("2 Countries Ka Trend Compare Karo - Kahan Kya Chal Raha Hai?")
    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        cmp1 = st.selectbox("Country 1", list(COUNTRIES.keys()), index=0, key="cmp1")
    with col_cmp2:
        cmp2 = st.selectbox("Country 2", list(COUNTRIES.keys()), index=2, key="cmp2")
    if st.button("Compare Countries Trends"):
        st.write(call_gemini(f"Compare Google + YouTube Trends between {cmp1} and {cmp2}. Give Top 5 trending topics in each country, what is common, what is different, and which country has better opportunity for a Pakistani YouTuber. In English."))

with tab4:
    st.header("💰 RPM Calculator")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Your Niche?", ["Vlog - $1", "Gaming - $1.5", "Tech - $3", "Finance - $5", "Islamic - $1.2", "Food - $1.8"])
    rpm_val = float(niche_rpm.split("$")[1]); earning = (views/1000)*rpm_val
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly $", f"${earning:.2f}"); c2.metric("Monthly Rs", f"Rs {earning*280:,.0f}"); c3.metric("
