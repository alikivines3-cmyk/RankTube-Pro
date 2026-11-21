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
.audit-good { background: #0a5c2e; padding: 10px; border-radius: 10px; }
.audit-bad { background: #7a1a1a; padding: 10px; border-radius: 10px; }
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
        <h1 style="margin:0; font-size:38px;">RANK<span style="color:#FF0000;">TUBE</span> <span style="color:#FF0000;">PRO</span> <span style="font-size:20px;">📈</span></h1>
        <p style="margin:0; color:#aaa;">Pakistans No.1 YouTube Growth Tool | AI Powered | Grow Fast</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.write("---")

if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero">
        <h1 style="color:white; font-size:42px;">Grow Your YouTube Channel 10X Faster</h1>
        <p style="color:white; font-size:18px;">AI Titles | Country Wise Trends | Channel Audit | Competitor Spy</p>
        <p style="color:#ffcccc;">Join 5000+ Creators Using RANKTUBE PRO</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="feature-card"><h2>AI Titles</h2><p>Viral Titles In 10 Sec</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><h2>Country Trends</h2><p>Trends By Country</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><h2>Channel Audit</h2><p>Score Out Of 100</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="feature-card"><h2>Competitor Spy</h2><p>Beat Competitor</p></div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("Step 1: Sign Up With Google")
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
        st.success(f"Connected Channel: {st.session_state.connected_channel}")
    else:
        st.warning("Channel Not Connected Yet")

with st.expander("Step 2: Connect Your Channel", expanded=(st.session_state.connected_channel == "")):
    conn_input = st.text_input("Enter Channel Name", "@AliMahiVlogs")
    if st.button("Connect Channel"):
        d = get_channel_data(conn_input)
        if d:
            st.session_state.connected_channel = conn_input
            st.success(f"Connected: {d['snippet']['title']}")
            st.rerun()
        else:
            st.error("Channel Not Found")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Dashboard", "Title + Script", "Trends By Country", "RPM Calculator", "Competitor", "Thumbnail", "Channel Audit"])

with tab1:
    st.header("Channel Dashboard - Full Profile")
    ch = st.text_input("Channel", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Full Channel Data"):
        with st.spinner("Loading Logo, Banner and Videos..."):
            data = get_channel_data(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                banner_url = data["brandingSettings"]["image"]["bannerExternalUrl"]
                st.image(banner_url, use_container_width=True)
            col_logo, col_info = st.columns([1, 4])
            with col_logo:
                st.image(snip["thumbnails"]["high"]["url"], width=130)
            with col_info:
                st.subheader(snip["title"])
                st.write(snip.get("description", "")[:300])
                st.link_button("Visit On YouTube", f"https://www.youtube.com/channel/{cid}")
            st.write("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subscribers", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Total Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Total Videos", stats.get("videoCount", "0"))
            avg_val = int(stats.get("viewCount", "0")) // max(int(stats.get("videoCount", "1")), 1)
            c4.metric("Avg Views", f"{avg_val:,}")
            st.write("---")
            st.subheader("Latest Videos")
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
                            st.link_button("Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Channel Not Found")

with tab2:
    st.header("AI Title + Script Generator")
    topic = st.text_input("Video Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI"):
        with st.spinner("AI Thinking..."):
            result = call_gemini(f"For Pakistani YouTube {niche} channel, topic {topic}: Give 1) 5 viral titles Urdu English mix 2) 30 sec script 3) 10 hashtags 4) Best upload time Pakistan. In English.")
        st.write(result)

with tab3:
    st.header("Trends By Country - Select Country")
    st.write("Select Any Country - That Country Real Trend Will Show")
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
    st.subheader(f"Google Trends In {selected_country_name}")
    if st.button(f"Get Google Trends - {selected_country_name}"):
        with st.spinner(f"Fetching Google Trends For {selected_country_name}..."):
            res = call_gemini(f"Give REAL Google Trends for country {selected_country_name} right now. Category {trend_category}. Give Top 10 most searched keywords on Google in {selected_country_name} today, with search volume High Medium Low, and 1 YouTube video idea for each keyword. Also give 5 Rising keywords. In English.")
        st.write(res)
    st.write("---")
    st.subheader(f"YouTube Trending Videos In {selected_country_name}")
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
                            st.link_button("Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error(f"No Trending Found For {selected_country_name}")
    st.write("---")
    st.subheader("Compare 2 Countries")
    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        cmp1 = st.selectbox("Country 1", list(COUNTRIES.keys()), index=0, key="cmp1")
    with col_cmp2:
        cmp2 = st.selectbox("Country 2", list(COUNTRIES.keys()), index=2, key="cmp2")
    if st.button("Compare Countries Trends"):
        with st.spinner("Comparing..."):
            comp_res = call_gemini(f"Compare Google and YouTube Trends between {cmp1} and {cmp2}. Give Top 5 trending topics in each country, what is common, what is different, and which country has better opportunity for a Pakistani YouTuber. In English.")
        st.write(comp_res)

with tab4:
    st.header("RPM Calculator")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Your Niche?", ["Vlog - 1 Dollar", "Gaming - 1.5 Dollar", "Tech - 3 Dollar", "Finance - 5 Dollar", "Islamic - 1.2 Dollar", "Food - 1.8 Dollar"])
    rpm_text = niche_rpm.split("-")[1].strip().split(" ")[0]
    rpm_val = float(rpm_text)
    earning = (views / 1000) * rpm_val
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly Dollar", f"{earning:.2f} USD")
    c2.metric("Monthly Rupees", f"{earning*280:,.0f} PKR")
    c3.metric("Yearly Dollar", f"{earning*12:.2f} USD")
    if st.button("How To Increase RPM?"):
        with st.spinner("Asking AI..."):
            rpm_res = call_gemini(f"How to increase RPM for Pakistani YouTube? Niche {niche_rpm}, views {views}. Give 5 tips in English.")
        st.write(rpm_res)

with tab5:
    st.header("Competitor Analysis")
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
            st.write(snip.get("description", "")[:250])
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
                beat_res = call_gemini(f"Competitor {snip['title']} has {stats.get('subscriberCount')} subs. How to beat them? Give 5 strategies for Pakistani audience in English.")
                st.write(beat_res)
        else:
            st.error("Competitor Not Found")

with tab6:
    st.header("Thumbnail Ideas - AI")
    th_topic = st.text_input("Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas"):
        with st.spinner("AI Designing..."):
            thumb_res = call_gemini(f"For video topic {th_topic} give 5 viral thumbnail ideas. For each: Text, Color, Face expression, Background. For Pakistani audience, high CTR. In English.")
        st.write(thumb_res)

with tab7:
    st.header("Channel Audit - Full Report Card")
    st.write("AI Will Audit Your Channel And Give Score Out Of 100")
    audit_ch = st.text_input("Channel To Audit", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="audit_ch")
    if st.button("Run Full Channel Audit"):
        with st.spinner("Auditing Channel..."):
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
            st.markdown(f"### Your Channel Score: {score} / 100")
            st.progress(score / 100)
            if score >= 80:
                st.success("EXCELLENT - Your Channel Is Growing Well!")
            elif score >= 50:
                st.warning("GOOD - But Needs Improvement")
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
                st.markdown(f'<div class="audit-bad">NEED - Monetization Subs: {subs} / 1000</div>', unsafe_allow_html=True)
            st.write("")
            if vcount >= 20:
                st.markdown('<div class="audit-good">OK - Total Videos Good</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="audit-bad">NEED - Total Videos Only {vcount} - Need At Least 20</div>', unsafe_allow_html=True)
            st.write("")
            if avg_views >= 500:
                st.markdown('<div class="audit-good">OK - Avg Views Good</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="audit-bad">NEED - Avg Views Only {avg_views} - Need More CTR</div>', unsafe_allow_html=True)
            st.write("")
            st.subheader("AI Audit - What To Fix?")
            ai_audit = call_gemini(f"Audit this YouTube channel: Name {snip['title']}, Subs {subs}, Views {views}, Videos {vcount}, Avg Views {avg_views}, Score {score} out of 100. Give 5 specific things to fix to grow faster in Pakistan, in English.")
            st.write(ai_audit)
        else:
            st.error("Channel Not Found For Audit")

st.write("---")
st.markdown("<p style='text-align:center; color:#888;'>Made With Love - RANKTUBE PRO | Ali Mahi | Version 6.0 - All In One</p>", unsafe_allow_html=True)
