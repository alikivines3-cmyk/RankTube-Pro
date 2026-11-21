import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")

# ===== PROFESSIONAL CSS + LOGO =====
st.markdown("""
<style>
.main { background-color: #0f0f0f; }
.stApp { background-color: #0f0f0f; color: white; }
h1, h2, h3 { color: white !important; }
.logo-box { display: flex; align-items: center; gap: 15px; }
.logo-circle { width: 70px; height: 70px; background: linear-gradient(135deg, #FF0000, #FF4444); border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; box-shadow: 0 0 20px rgba(255,0,0,0.5); }
.logo-play { color: white; font-size: 32px; margin-left: 5px; }
.logo-arrow { position: absolute; top: -8px; right: -8px; background: white; color: #FF0000; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; border: 2px solid #FF0000; }
div[data-testid="stMetric"] { background: linear-gradient(135deg, #1e1e1e, #2a2a2a); border: 1px solid #333; border-radius: 12px; padding: 15px; }
div[data-testid="stMetric"] label { color: #aaa !important; }
div[data-testid="stMetric"] div { color: white !important; }
.stButton>button { background: linear-gradient(90deg, #FF0000, #FF4444); color: white; border: none; border-radius: 25px; padding: 10px 25px; font-weight: bold; width: 100%; }
.stButton>button:hover { background: linear-gradient(90deg, #CC0000, #FF0000); color: white; }
.banner-img { border-radius: 15px; width: 100%; }
.channel-logo { border-radius: 50%; border: 3px solid #FF0000; }
</style>
""", unsafe_allow_html=True)

# ===== NEW PROFESSIONAL HEADER WITH YT LOGO + UP ARROW =====
st.markdown("""
<div class="logo-box">
    <div class="logo-circle">
        <div class="logo-play">▶</div>
        <div class="logo-arrow">↗</div>
    </div>
    <div>
        <h1 style="margin:0; font-size:38px;">RANK<span style="color:#FF0000;">TUBE</span> <span style="color:#FF0000;">PRO</span> <span style="font-size:20px;">📈</span></h1>
        <p style="margin:0; color:#aaa;">Pakistan's No.1 YouTube Growth Tool | AI Powered | Real Data | Grow Fast ↗</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("---")

try:
    YOUTUBE_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    st.success("✅ Connected - Real YouTube + AI Data Ready")
except:
    st.error("❌ Keys Not Found")
    YOUTUBE_KEY = ""
    GEMINI_KEY = ""

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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "✍️ Title + Script", "🔥 Trending Videos", "💰 RPM Calculator", "⚔️ Competitor", "🖼️ Thumbnail"])

with tab1:
    st.header("📊 Channel Dashboard - Full Profile")
    ch = st.text_input("Enter Channel @Name", "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Full Channel Data", key="dash_btn"):
        with st.spinner("Loading Channel Logo, Banner & Videos..."):
            data = get_channel_data(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid = data["id"]
            # ===== BANNER =====
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                banner_url = data["brandingSettings"]["image"]["bannerExternalUrl"]
                st.image(banner_url, use_container_width=True)
            elif "thumbnails" in snip:
                st.image(snip["thumbnails"]["high"]["url"], width=200)
            # ===== LOGO + INFO =====
            col_logo, col_info = st.columns([1, 4])
            with col_logo:
                st.image(snip["thumbnails"]["high"]["url"], width=130)
            with col_info:
                st.subheader(f"✅ {snip['title']}  ✔️ Verified Channel")
                st.write(f"📅 Created: {snip.get('publishedAt','')[:10]} | 🌍 Country: {snip.get('country','Pakistan')}")
                st.write(snip.get("description", "")[:300])
                st.link_button("🔴 Visit Channel On YouTube", f"https://www.youtube.com/channel/{cid}")
            st.write("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subscribers", f"{int(stats.get('subscriberCount','0')):,}")
            c2.metric("Total Views", f"{int(stats.get('viewCount','0')):,}")
            c3.metric("Total Videos", stats.get("videoCount", "0"))
            avg = int(stats.get("viewCount","0")) // max(int(stats.get("videoCount","1")),1)
            c4.metric("Avg Views / Video", f"{avg:,}")
            subs = int(stats.get("subscriberCount", "0"))
            if subs < 1000:
                st.progress(subs / 1000)
                st.warning(f"Need {1000-subs} More Subs For Monetization - {subs/10:.1f}% Complete")
            else:
                st.success("🎉 Monetization Subs Complete!")
            # ===== RECENT VIDEOS =====
            st.write("---")
            st.subheader("🎬 Latest Videos - Watch Here")
            vids = get_channel_videos(cid, 6)
            if vids:
                for i in range(0, len(vids), 3):
                    cols = st.columns(3)
                    for j, col in enumerate(cols):
                        if i+j < len(vids):
                            v = vids[i+j]
                            vid = v["id"]["videoId"]
                            with col:
                                st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                                st.write(f"**{v['snippet']['title'][:60]}...**")
                                st.write(f"📅 {v['snippet']['publishedAt'][:10]}")
                                st.video(f"https://www.youtube.com/watch?v={vid}")
                                st.link_button("▶️ Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
            else:
                st.info("No Recent Videos Found - Channel May Have No Public Videos")
        else:
            st.error("Channel Not Found")

with tab2:
    st.header("✍️ AI Title + Script Generator")
    topic = st.text_input("Video Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI ✨"):
        with st.spinner("AI Is Thinking..."):
            result = call_gemini(f"For Pakistani YouTube {niche} channel, topic '{topic}': Give 1) 5 viral high CTR titles in Urdu+English mix 2) 1 short 30 sec video script 3) 10 hashtags 4) Best upload time in Pakistan. Give in English.")
        st.write(result)
        st.code(result)

with tab3:
    st.header("🔥 Trending Videos In Pakistan - Watch Here")
    if st.button("Load Trending Videos 🔥"):
        with st.spinner("Loading Trending Videos..."):
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=PK&maxResults=12&key={YOUTUBE_KEY}"
            r = requests.get(url).json()
        if "items" in r:
            for i in range(0, len(r["items"]), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i+j < len(r["items"]):
                        v = r["items"][i+j]
                        vid = v["id"]
                        with col:
                            st.image(v["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                            st.write(f"🔥 **TRENDING #{i+j+1}**")
                            st.write(f"**{v['snippet']['title'][:70]}...**")
                            st.write(f"📺 {v['snippet']['channelTitle']} | 👁️ {int(v['statistics'].get('viewCount','0')):,} Views")
                            st.video(f"https://www.youtube.com/watch?v={vid}")
                            st.link_button("▶️ Watch On YouTube", f"https://www.youtube.com/watch?v={vid}")
        else:
            st.error("Trending Not Found")
    if st.button("Get AI Trending Topics"):
        st.write(call_gemini("Give Top 10 trending topics on YouTube in Pakistan this week. Give 1 video idea for each. In English."))

with tab4:
    st.header("💰 RPM / Earnings Calculator")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Your Niche?", ["Vlog - $1", "Gaming - $1.5", "Tech - $3", "Finance - $5", "Islamic - $1.2", "Food - $1.8"])
    rpm_val = float(niche_rpm.split("$")[1])
    earning = (views / 1000) * rpm_val
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly $", f"${earning:.2f}")
    c2.metric("Monthly Rs", f"Rs {earning*280:,.0f}")
    c3.metric("Yearly $", f"${earning*12:.2f}")
    if st.button("How To Increase RPM? Ask AI"):
        st.write(call_gemini(f"How to increase RPM for Pakistani YouTube? Niche {niche_rpm}, views {views}. Give 5 tips in English."))

with tab5:
    st.header("⚔️ Competitor Analysis - Full Profile")
    comp = st.text_input("Enter Competitor @Name", "@DuckyBhai")
    if st.button("Analyze Competitor"):
        with st.spinner("Analyzing..."):
            data = get_channel_data(comp)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            cid2 = data["id"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            col_i, col_d = st.columns([1, 3])
            with col_i:
                st.image(snip["thumbnails"]["high"]["url"], width=120)
            with col_d:
                st.subheader(snip['title'])
                st.write(snip.get("description", "")[:250])
            c1, c2, c3 = st.columns(3)
            c1.metric("Their Subs", f"{int(stats.get('subscriberCount','0')):,}")
            c2.metric("Their Views", f"{int(stats.get('viewCount','0')):,}")
            c3.metric("Their Videos", stats.get("videoCount", "0"))
            st.subheader("🎬 Their Latest Videos")
            vids2 = get_channel_videos(cid2, 3)
            for v in vids2:
                vid = v["id"]["videoId"]
                st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=300)
                st.write(f"**{v['snippet']['title'][:70]}**")
                st.video(f"https://www.youtube.com/watch?v={vid}")
            if st.button("Ask AI - How To Beat Them?"):
                st.write(call_gemini(f"Competitor {snip['title']} has {stats.get('subscriberCount')} subs. How to beat them? Give 5 strategies for Pakistani audience in English."))
        else:
            st.error("Competitor Not Found")

with tab6:
    st.header("🖼️ Thumbnail Ideas - AI")
    th_topic = st.text_input("Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas 🎨"):
        st.write(call_gemini(f"For video topic '{th_topic}' give 5 viral thumbnail ideas. For each: 1) Thumbnail text (3-4 words) 2) Color 3) Face expression 4) Background. For Pakistani audience, high CTR. In English."))

st.write("---")
st.markdown("<p style='text-align:center; color:#888;'>Made With ❤️ - RANKTUBE PRO | Ali Mahi | Version 4.0 PRO - Grow Fast ↗</p>", unsafe_allow_html=True)
