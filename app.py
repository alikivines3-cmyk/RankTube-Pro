import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")

st.markdown("""
<style>
.main { background-color: #0a0a0f; }
.stApp { background-color: #0a0a0f; color: white; }
h1, h2, h3 { color: white !important; }
.logo-box { display: flex; align-items: center; gap: 18px; background: linear-gradient(90deg, #1a1a2e, #0f0f0f); padding: 15px 20px; border-radius: 20px; border: 1px solid #333; }
.logo-circle { width: 75px; height: 75px; background: linear-gradient(135deg, #FF0000, #FF6B00); border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 25px rgba(255,0,0,0.6); flex-shrink: 0; }
.logo-play { color: white; font-size: 34px; margin-left: 6px; }
.logo-arrow { position: absolute; top: -8px; right: -8px; background: white; color: #FF0000; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; border: 2px solid #FF0000; }
.hero { background: linear-gradient(135deg, #FF0000 0%, #FF6B00 40%, #7a00ff 100%); padding: 40px 20px; border-radius: 25px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(255,0,0,0.3); }
.hero h1 { font-size: 48px !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.4); }
.box-red { background: linear-gradient(135deg, #FF0000, #FF6B00); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 180px; box-shadow: 0 8px 25px rgba(255,0,0,0.3); }
.box-blue { background: linear-gradient(135deg, #0066FF, #00CCFF); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 180px; box-shadow: 0 8px 25px rgba(0,102,255,0.3); }
.box-green { background: linear-gradient(135deg, #00AA44, #00DD77); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 180px; box-shadow: 0 8px 25px rgba(0,170,68,0.3); }
.box-purple { background: linear-gradient(135deg, #7A00FF, #FF00AA); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 180px; box-shadow: 0 8px 25px rgba(122,0,255,0.3); }
.box-orange { background: linear-gradient(135deg, #FF8800, #FFCC00); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 160px; }
.box-pink { background: linear-gradient(135deg, #FF0066, #FF66AA); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 160px; }
.box-teal { background: linear-gradient(135deg, #00AAAA, #00FFCC); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 160px; }
.box-dark { background: linear-gradient(135deg, #222244, #444488); border-radius: 20px; padding: 25px 15px; text-align: center; min-height: 160px; }
.big-title { font-size: 36px !important; font-weight: 800; margin-bottom: 5px; }
.big-icon { font-size: 48px; }
.small-desc { font-size: 15px; color: rgba(255,255,255,0.9); }
div[data-testid="stMetric"] { border-radius: 18px !important; padding: 18px !important; border: none !important; }
.stButton>button { background: linear-gradient(90deg, #FF0000, #FF6B00); color: white; border: none; border-radius: 30px; padding: 12px 25px; font-weight: bold; width: 100%; font-size: 16px; box-shadow: 0 5px 15px rgba(255,0,0,0.3); }
.stButton>button:hover { background: linear-gradient(90deg, #CC0000, #FF0000); color: white; transform: scale(1.02); }
.section-red { background: linear-gradient(135deg, #2a0000, #1a0000); border-left: 6px solid #FF0000; padding: 20px; border-radius: 15px; }
.section-blue { background: linear-gradient(135deg, #001a33, #000a1a); border-left: 6px solid #0066FF; padding: 20px; border-radius: 15px; }
.section-green { background: linear-gradient(135deg, #002a11, #001a0a); border-left: 6px solid #00AA44; padding: 20px; border-radius: 15px; }
.section-purple { background: linear-gradient(135deg, #1a0033, #0f001a); border-left: 6px solid #7A00FF; padding: 20px; border-radius: 15px; }
.section-orange { background: linear-gradient(135deg, #331a00, #1a0f00); border-left: 6px solid #FF8800; padding: 20px; border-radius: 15px; }
.country-box { background: linear-gradient(135deg, #1a1a2e, #2a1a4e); border: 2px solid #7A00FF; border-radius: 20px; padding: 20px; }
.audit-good { background: linear-gradient(90deg, #00AA44, #00DD77); padding: 12px; border-radius: 12px; font-weight: bold; }
.audit-bad { background: linear-gradient(90deg, #FF0000, #FF4444); padding: 12px; border-radius: 12px; font-weight: bold; }
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

COUNTRIES = {
    "Pakistan": "PK",
    "India": "IN",
    "USA": "US",
    "UK": "GB",
    "UAE": "AE",
    "Saudi Arabia": "SA",
    "Bangladesh": "BD",
    "Turkey": "TR",
    "Canada": "CA",
    "Australia": "AU",
    "Germany": "DE",
    "France": "FR",
    "Indonesia": "ID",
    "Malaysia": "MY"
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
    <div>
        <h1 style="margin:0; font-size:40px;">RANK<span style="color:#FF0000;">TUBE</span> <span style="color:#FF8800;">PRO</span> <span style="font-size:22px;">📈</span></h1>
        <p style="margin:0; color:#ccc; font-size:16px;">Pakistans No.1 YouTube Growth Tool | AI Powered | Grow Fast ↗</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.write("---")

if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero">
        <div style="font-size:70px;">🚀</div>
        <h1 style="color:white;">Grow Your YouTube Channel 10X Faster</h1>
        <p style="color:white; font-size:20px; font-weight:bold;">AI Titles | Country Wise Trends | Channel Audit | Competitor Spy | RPM Calculator</p>
        <p style="color:#ffe6cc; font-size:16px;">⭐⭐⭐⭐⭐ Join 5000+ Pakistani Creators | 100% Free To Start</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-size:32px;'>✨ WHY CHOOSE RANKTUBE PRO? ✨</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="box-red"><div class="big-icon">🤖</div><div class="big-title">AI TITLES</div><div class="small-desc">Viral Titles In 10 Sec<br>High CTR | Urdu + English</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="box-blue"><div class="big-icon">🌍</div><div class="big-title">COUNTRY TRENDS</div><div class="small-desc">Trends By Country<br>Pakistan | USA | India | UK</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="box-green"><div class="big-icon">📊</div><div class="big-title">CHANNEL AUDIT</div><div class="small-desc">Score Out Of 100<br>What To Fix? Full Report</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="box-purple"><div class="big-icon">⚔️</div><div class="big-title">COMPETITOR SPY</div><div class="small-desc">Beat Your Competitor<br>See Their Secret Strategy</div></div>', unsafe_allow_html=True)
    st.write("")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown('<div class="box-orange"><div class="big-icon">💰</div><div class="big-title">RPM CALCULATOR</div><div class="small-desc">Kitne Paise Banein Ge?</div></div>', unsafe_allow_html=True)
    with c6:
        st.markdown('<div class="box-pink"><div class="big-icon">🖼️</div><div class="big-title">THUMBNAIL AI</div><div class="small-desc">Viral Thumbnail Ideas</div></div>', unsafe_allow_html=True)
    with c7:
        st.markdown('<div class="box-teal"><div class="big-icon">🔥</div><div class="big-title">TRENDING VIDEOS</div><div class="small-desc">Watch Trending Videos</div></div>', unsafe_allow_html=True)
    with c8:
        st.markdown('<div class="box-dark"><div class="big-icon">🔗</div><div class="big-title">CHANNEL CONNECT</div><div class="small-desc">Connect In 1 Click</div></div>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h2 style='text-align:center; font-size:30px;'>🔐 STEP 1: SIGN UP WITH GOOGLE 🔐</h2>", unsafe_allow_html=True)
    st.write("Sign Up Karo, Phir Channel Connect Karo, Phir Full Tool Khul Jayega")
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

st.markdown(f"<div class='section-green'><h2 style='margin:0;'>👋 Welcome Back! {st.session_state.user_email} ✅ Logged In</h2></div>", unsafe_allow_html=True)
st.write("")
col_logout, col_conn = st.columns([1, 3])
with col_logout:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.connected_channel = ""
        st.rerun()
with col_conn:
    if st.session_state.connected_channel:
        st.success(f"Connected Channel: {st.session_state.connected_channel}")
    else:
        st.warning("Channel Not Connected Yet - Connect Below")

with st.expander("STEP 2: CONNECT YOUR CHANNEL - CLICK HERE", expanded=(st.session_state.connected_channel == "")):
    conn_input = st.text_input("Enter Channel Name", "@AliMahiVlogs")
    if st.button("Connect Channel"):
        d = get_channel_data(conn_input)
        if d:
            st.session_state.connected_channel = conn_input
            st.success(f"Connected: {d['snippet']['title']}")
            st.rerun()
        else:
            st.error("Channel Not Found")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Dashboard", "✍️ Title + Script", "🌍 Trends By Country", "💰 RPM Calculator", "⚔️ Competitor", "🖼️ Thumbnail", "✅ Channel Audit"])

with tab1:
    st.markdown("<div class='section-red'><h2 style='margin:0; font-size:32px;'>📊 CHANNEL DASHBOARD - FULL PROFILE 📊</h2><p style='margin:0;'>Your Channel Logo, Banner, Stats And Latest Videos</p></div>", unsafe_allow_html=True)
    st.write("")
    ch = st.text_input("Channel", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Full Channel Data"):
        with st.spinner("Loading..."):
            data = get_channel_data(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            col_logo, col_info = st.columns([1, 4])
            with col_logo:
                st.image(snip["thumbnails"]["high"]["url"], width=130)
            with col_info:
                st.markdown(f"<h2 style='font-size:32px;'>{snip['title']} ✅</h2>", unsafe_allow_html=True)
                st.write(snip.get("description", "")[:300])
                st.link_button("Visit On YouTube", f"https://www.youtube.com/channel/{cid}")
            st.write("---")
            st.markdown("<h3>📈 YOUR STATS</h3>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown('<div class="box-red" style="min-height:120px;"><div class="big-icon">👥</div><div>SUBSCRIBERS</div></div>', unsafe_allow_html=True)
                st.metric("Subscribers", f"{int(stats.get('subscriberCount', '0')):,}")
            with c2:
                st.markdown('<div class="box-blue" style="min-height:120px;"><div class="big-icon">👁️</div><div>TOTAL VIEWS</div></div>', unsafe_allow_html=True)
                st.metric("Total Views", f"{int(stats.get('viewCount', '0')):,}")
            with c3:
                st.markdown('<div class="box-green" style="min-height:120px;"><div class="big-icon">🎬</div><div>TOTAL VIDEOS</div></div>', unsafe_allow_html=True)
                st.metric("Total Videos", stats.get("videoCount", "0"))
            with c4:
                avg_val = int(stats.get("viewCount", "0")) // max(int(stats.get("videoCount", "1")), 1)
                st.markdown('<div class="box-purple" style="min-height:120px;"><div class="big-icon">📊</div><div>AVG VIEWS</div></div>', unsafe_allow_html=True)
                st.metric("Avg Views", f"{avg_val:,}")
            st.write("---")
            st.markdown("<h3>🎬 LATEST VIDEOS - WATCH HERE</h3>", unsafe_allow_html=True)
            vids = get_channel_videos(cid, 6)
            for i in range(0, len(vids), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(vids):
                        v = vids[i + j]
                        vid = v["id"]["videoId"]
                        with col:
                            st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                            st.write(v["snippet"]["title"][:60])
                            st.video(f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Channel Not Found")

with tab2:
    st.markdown("<div class='section-blue'><h2 style='margin:0; font-size:32px;'>✍️ AI TITLE + SCRIPT GENERATOR ✍️</h2><p style='margin:0;'>Viral Titles, Script, Hashtags In 10 Seconds</p></div>", unsafe_allow_html=True)
    st.write("")
    topic = st.text_input("Video Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI"):
        with st.spinner("AI Thinking..."):
            result = call_gemini(f"For Pakistani YouTube {niche} channel, topic {topic}: Give 1) 5 viral titles Urdu English mix 2) 30 sec script 3) 10 hashtags 4) Best upload time Pakistan. In English.")
        st.markdown("<h3>🤖 AI RESULT</h3>", unsafe_allow_html=True)
        st.write(result)

with tab3:
    st.markdown("<div class='section-purple'><h2 style='margin:0; font-size:32px;'>🌍 TRENDS BY COUNTRY 🌍</h2><p style='margin:0;'>Select Any Country - That Country Real Trend Will Show</p></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="country-box">', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        selected_country_name = st.selectbox("Select Country For Trends", list(COUNTRIES.keys()), index=0)
    with col_c2:
        trend_category = st.selectbox("Category", ["All", "Gaming", "Vlog", "News", "Islamic", "Food", "Tech", "Cricket", "Music"])
    selected_code = COUNTRIES[selected_country_name]
    st.write(f"Selected: {selected_country_name} - Code: {selected_code}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    st.markdown(f"<h3>📈 GOOGLE TRENDS IN {selected_country_name.upper()}</h3>", unsafe_allow_html=True)
    if st.button(f"Get Google Trends - {selected_country_name}"):
        with st.spinner(f"Fetching Google Trends For {selected_country_name}..."):
            res = call_gemini(f"Give REAL Google Trends for country {selected_country_name} right now. Category {trend_category}. Give Top 10 most searched keywords on Google in {selected_country_name} today, with search volume High Medium Low, and 1 YouTube video idea for each keyword. Also give 5 Rising keywords. In English.")
        st.write(res)
    st.write("---")
    st.markdown(f"<h3>🎬 YOUTUBE TRENDING VIDEOS IN {selected_country_name.upper()}</h3>", unsafe_allow_html=True)
    if st.button(f"Load YouTube Trending - {selected_country_name}"):
        with st.spinner(f"Loading YouTube Trending For {selected_country_name}..."):
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={selected_code}&maxResults=9&key={YOUTUBE_KEY}"
            r = requests.get(url).json()
        if "items" in r and len(r["items"]) > 0:
            st.success(f"Showing Top Trending Videos In {selected_country_name}")
            for i in range(0, len(r["items"]), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(r["items"]):
                        v = r["items"][i + j]
                        vid = v["id"]
                        with col:
                            st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                            st.write(f"TRENDING {i+j+1} IN {selected_country_name}")
                            st.write(v["snippet"]["title"][:60])
                            st.write(f"{v['snippet']['channelTitle']} | Views {int(v['statistics'].get('viewCount', '0')):,}")
                            st.video(f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error(f"No Trending Found For {selected_country_name}")
    st.write("---")
    st.markdown("<h3>⚖️ COMPARE 2 COUNTRIES</h3>", unsafe_allow_html=True)
    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        cmp1 = st.selectbox("Country 1", list(COUNTRIES.keys()), index=0, key="cmp1")
    with col_cmp2:
        cmp2 = st.selectbox("Country 2", list(COUNTRIES.keys()), index=2, key="cmp2")
    if st.button("Compare Countries Trends"):
        with st.spinner("Comparing..."):
            comp_res = call_gemini(f"Compare Google and YouTube Trends between {cmp1} and {cmp2}. Give Top 5 trending topics in each country, what is common, what is different. In English.")
        st.write(comp_res)

with tab4:
    st.markdown("<div class='section-green'><h2 style='margin:0; font-size:32px;'>💰 RPM / EARNINGS CALCULATOR 💰</h2><p style='margin:0;'>Kitne Paise Banein Ge? Calculate Karo</p></div>", unsafe_allow_html=True)
    st.write("")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Your Niche?", ["Vlog - 1 Dollar", "Gaming - 1.5 Dollar", "Tech - 3 Dollar", "Finance - 5 Dollar", "Islamic - 1.2 Dollar", "Food - 1.8 Dollar"])
    rpm_text = niche_rpm.split("-")[1].strip().split(" ")[0]
    rpm_val = float(rpm_text)
    earning = (views / 1000) * rpm_val
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="box-green"><div class="big-icon">💵</div><div>MONTHLY DOLLAR</div></div>', unsafe_allow_html=True)
        st.metric("Monthly Dollar", f"{earning:.2f} USD")
    with c2:
        st.markdown('<div class="box-orange"><div class="big-icon">💴</div><div>MONTHLY RUPEES</div></div>', unsafe_allow_html=True)
        st.metric("Monthly Rupees", f"{earning*280:,.0f} PKR")
    with c3:
        st.markdown('<div class="box-purple"><div class="big-icon">🏦</div><div>YEARLY DOLLAR</div></div>', unsafe_allow_html=True)
        st.metric("Yearly Dollar", f"{earning*12:.2f} USD")
    if st.button("How To Increase RPM?"):
        with st.spinner("Asking AI..."):
            rpm_res = call_gemini(f"How to increase RPM for Pakistani YouTube? Niche {niche_rpm}, views {views}. Give 5 tips in English.")
        st.write(rpm_res)

with tab5:
    st.markdown("<div class='section-orange'><h2 style='margin:0; font-size:32px;'>⚔️ COMPETITOR ANALYSIS ⚔️</h2><p style='margin:0;'>See Competitor Secret - Beat Them</p></div>", unsafe_allow_html=True)
    st.write("")
    comp = st.text_input("Competitor Name", "@DuckyBhai")
    if st.button("Analyze Competitor"):
        with st.spinner("Analyzing..."):
            data = get_channel_data(comp)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid2 = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            st.image(snip["thumbnails"]["high"]["url"], width=120)
            st.subheader(snip["title"])
            c1, c2, c3 = st.columns(3)
            c1.metric("Their Subs", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Their Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Their Videos", stats.get("videoCount", "0"))
            st.subheader("Their Latest Videos")
            vids2 = get_channel_videos(cid2, 3)
            for v in vids2:
                st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=300)
                st.write(v["snippet"]["title"][:70])
                st.video(f"https://www.youtube.com/watch?v={v['id']['videoId']}")
            if st.button("Ask AI - How To Beat Them?"):
                beat_res = call_gemini(f"Competitor {snip['title']} has {stats.get('subscriberCount')} subs. How to beat them? Give 5 strategies.")
                st.write(beat_res)
        else:
            st.error("Competitor Not Found")

with tab6:
    st.markdown("<div class='section-purple'><h2 style='margin:0; font-size:32px;'>🖼️ THUMBNAIL IDEAS - AI 🖼️</h2><p style='margin:0;'>Viral Thumbnail Ideas - High CTR</p></div>", unsafe_allow_html=True)
    st.write("")
    th_topic = st.text_input("Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas"):
        with st.spinner("AI Designing..."):
            thumb_res = call_gemini(f"For video topic {th_topic} give 5 viral thumbnail ideas. For each: Text, Color, Face expression, Background. For Pakistani audience.")
        st.write(thumb_res)

with tab7:
    st.markdown("<div class='section-blue'><h2 style='margin:0; font-size:32px;'>✅ CHANNEL AUDIT - FULL REPORT CARD ✅</h2><p style='margin:0;'>Your Score Out Of 100 - What To Fix?</p></div>", unsafe_allow_html=True)
    st.write("")
    audit_ch = st.text_input("Channel To Audit", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="audit_ch")
    if st.button("Run Full Channel Audit"):
        with st.spinner("Auditing..."):
            data = get_channel_data(audit_ch)
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
            elif subs >= 10:
                score = score + 10
            if vcount >= 50:
                score = score + 25
            elif vcount >= 20:
                score = score + 18
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
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                score = score + 15
            else:
                score = score + 5
            if score > 100:
                score = 100
            st.markdown(f"<h2 style='font-size:38px; text-align:center;'>🎯 YOUR SCORE: {score} / 100 🎯</h2>", unsafe_allow_html=True)
            st.progress(score / 100)
            if score >= 80:
                st.success("EXCELLENT - Growing Well!")
            elif score >= 50:
                st.warning("GOOD - Needs Improvement")
            else:
                st.error("NEEDS WORK - Follow Audit Below")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subs", f"{subs:,}")
            c2.metric("Views", f"{views:,}")
            c3.metric("Videos", vcount)
            c4.metric("Avg Views", f"{avg_views:,}")
            st.write("---")
            st.subheader("Audit Checklist")
            if subs >= 1000:
                st.markdown('<div class="audit-good">OK - Monetization Subs Complete</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="audit-bad">NEED - Subs: {subs} / 1000</div>', unsafe_allow_html=True)
            st.write("")
            if vcount >= 20:
                st.markdown('<div class="audit-good">OK - Videos Good</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="audit-bad">NEED - Videos Only {vcount} - Need 20</div>', unsafe_allow_html=True)
            st.write("")
            if avg_views >= 500:
                st.markdown('<div class="audit-good">OK - Avg Views Good</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="audit-bad">NEED - Avg Views Only {avg_views}</div>', unsafe_allow_html=True)
            st.write("")
            ai_audit = call_gemini(f"Audit channel {snip['title']}, Subs {subs}, Views {views}, Videos {vcount}, Avg {avg_views}, Score {score}/100. Give 5 things to fix in Pakistan.")
            st.write(ai_audit)
        else:
            st.error("Channel Not Found")

st.write("---")
st.markdown("<p style='text-align:center; color:#888; font-size:16px;'>Made With Love - RANKTUBE PRO | Ali Mahi | Version 7.0 MODERN - Eye Catching</p>", unsafe_allow_html=True)
