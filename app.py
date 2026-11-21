import streamlit as st
import requests
import re

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
.good-box { background: linear-gradient(90deg, #00AA44, #00DD77); padding: 12px; border-radius: 12px; font-weight: bold; margin-bottom: 8px; }
.bad-box { background: linear-gradient(90deg, #FF0000, #FF4444); padding: 12px; border-radius: 12px; font-weight: bold; margin-bottom: 8px; }
.warn-box { background: linear-gradient(90deg, #FF8800, #FFCC00); padding: 12px; border-radius: 12px; font-weight: bold; color: black; margin-bottom: 8px; }
.fix-box { background: #1a1a2e; border: 1px solid #7A00FF; padding: 15px; border-radius: 15px; margin-bottom: 10px; }
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

def call_gemini(prompt):
    gem_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    gr = requests.post(gem_url, json=payload, timeout=30).json()
    try:
        return gr["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI Error - Try Again"

def get_channel_data(query):
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

def get_video_id_from_url(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    if "shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]
    return url.strip()

def get_video_data(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={YOUTUBE_KEY}"
    r = requests.get(url, timeout=15).json()
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
    <div><h1 style="margin:0; font-size:32px;">RANK<span style="color:#FF0000;">TUBE</span> PRO 📈</h1><p style="margin:0; color:#ccc;">Video Audit | Fix Your Video | Grow Fast</p></div>
</div>
""", unsafe_allow_html=True)
st.write("---")

if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero">
        <div style="font-size:50px;">🚀</div>
        <h1 style="color:white; font-size:36px;">Grow Your YouTube 10X Faster</h1>
        <p style="color:white;">Video Audit | AI Titles | Country Trends | Channel Audit</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="box-red"><div style="font-size:36px;">🎬</div><h3>VIDEO AUDIT</h3><p>Kya Theek Hai? Kya Ghalat?</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="box-blue"><div style="font-size:36px;">🌍</div><h3>COUNTRY TRENDS</h3><p>Trends By Country</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="box-green"><div style="font-size:36px;">📊</div><h3>CHANNEL AUDIT</h3><p>Score Out Of 100</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="box-purple"><div style="font-size:36px;">🤖</div><h3>AI TITLES</h3><p>Viral Titles In 10 Sec</p></div>', unsafe_allow_html=True)
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
        d = get_channel_data(conn_input)
        if d:
            st.session_state.connected_channel = conn_input
            st.success(f"Connected: {d['snippet']['title']}")
            st.rerun()
        else:
            st.error("Not Found")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🎬 Video Audit", "Dashboard", "Title", "Trends", "RPM", "Competitor", "Thumbnail", "Channel Audit"])

with tab1:
    st.markdown("<h1 style='font-size:36px;'>🎬 VIDEO AUDIT - Kya Theek Hai? Kya Ghalat Hai? 🔍</h1>", unsafe_allow_html=True)
    st.write("Apni Video Ka Link Dalo - App Batayega Kya Theek Hai, Kya Ghalat Hai, Aur Kaise Fix Karo")
    video_url = st.text_input("Video Ka Link Ya ID Dalo", placeholder="https://www.youtube.com/watch?v=... ya Sirf Video ID")
    st.write("Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if st.button("Audit My Video - Check Karo Kya Ghalat Hai"):
        if not video_url:
            st.error("Pehle Video Link Dalo")
        else:
            vid = get_video_id_from_url(video_url)
            with st.spinner("Video Check Ho Rahi Hai - 15 Sec Wait..."):
                vdata = get_video_data(vid)
            if not vdata:
                st.error("Video Nahi Mili - Link Sahi Hai? Video Public Hai?")
            else:
                snip = vdata["snippet"]
                stats = vdata["statistics"]
                content = vdata["contentDetails"]
                title = snip.get("title", "")
                desc = snip.get("description", "")
                tags = snip.get("tags", [])
                views = int(stats.get("viewCount", "0"))
                likes = int(stats.get("likeCount", "0"))
                comments = int(stats.get("commentCount", "0"))
                duration = content.get("duration", "")
                thumb = snip["thumbnails"]["high"]["url"]
                st.image(thumb, use_container_width=True)
                st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
                st.write(f"Channel: {snip.get('channelTitle', '')} | Date: {snip.get('publishedAt', '')[:10]} | Duration: {duration}")
                st.video(f"https://www.youtube.com/watch?v={vid}")
                st.write("---")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Views", f"{views:,}")
                c2.metric("Likes", f"{likes:,}")
                like_ratio = (likes / max(views, 1) * 100)
                c3.metric("Like Ratio", f"{like_ratio:.2f}%")
                c4.metric("Comments", f"{comments:,}")
                st.write("---")
                st.markdown("<h2>📋 VIDEO CHECKLIST - Kya Theek Hai, Kya Ghalat Hai?</h2>", unsafe_allow_html=True)
                score = 0
                total = 0
                # 1 Title Length
                total = total + 1
                if len(title) >= 40 and len(title) <= 70:
                    st.markdown(f'<div class="good-box">✅ THEEK HAI - Title Length: {len(title)} Characters - Perfect Hai (40-70 Best Hai)</div>', unsafe_allow_html=True)
                    score = score + 1
                elif len(title) < 40:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Title Bohat Chhota Hai: {len(title)} Characters - 40 Se 70 Hona Chahiye</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="fix-box">🔧 FIX KARO: Title Ko Lamba Karo. Isme Emotion + Number + Curiosity Add Karo. Misaal: "Maine Sea View Me Ye Dekh Liya" Ki Jagah "Sea View Me Mujhe Ye Mila - Tum Yaqeen Nahi Karoge! | Day 5"</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Title Bohat Lamba Hai: {len(title)} Characters - Mobile Me Kat Jayega</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="fix-box">🔧 FIX KARO: Title Ko 60 Characters Tak Chhota Karo. Faltu Lafz Hatao, Sirf Main Baat Rakho.</div>', unsafe_allow_html=True)
                # 2 Title Has Number / Emotion
                total = total + 1
                if any(ch.isdigit() for ch in title) or "!" in title or "?" in title:
                    st.markdown('<div class="good-box">✅ THEEK HAI - Title Me Number / Emotion Hai - CTR Acha Hoga</div>', unsafe_allow_html=True)
                    score = score + 1
                else:
                    st.markdown('<div class="bad-box">❌ GHALAT HAI - Title Me Number / Emotion Nahi Hai - Boring Lag Raha Hai</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Title Me Number Ya Emotion Add Karo. Misaal: "5 Cheezein", "Sab Se Bara", "Mujhe Dar Lag Gaya", "Yaqeen Nahi Karoge"</div>', unsafe_allow_html=True)
                # 3 Description
                total = total + 1
                if len(desc) >= 200:
                    st.markdown(f'<div class="good-box">✅ THEEK HAI - Description Lambi Hai: {len(desc)} Characters - SEO Ke Liye Achi Hai</div>', unsafe_allow_html=True)
                    score = score + 1
                elif len(desc) >= 50:
                    st.markdown(f'<div class="warn-box">⚠️ THORA GHALAT - Description Chhoti Hai: {len(desc)} Characters - 200+ Honi Chahiye</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Description Me Video Ki Poori Kahani Likho, 3-4 Line Me. Pehli 2 Line Me Main Keyword Likho.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Description Bilkul Khali Hai: {len(desc)} Characters - YouTube Isko Rank Nahi Karega</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Abhi Description Likho - 200 Lafz Ki. Video Kya Hai, Kyun Dekhni Chahiye, Aur End Me Hashtag Lagao.</div>', unsafe_allow_html=True)
                # 4 Hashtags
                total = total + 1
                if "#" in desc or "#" in title:
                    st.markdown('<div class="good-box">✅ THEEK HAI - Hashtag Lage Hue Hain - Search Me Aayega</div>', unsafe_allow_html=True)
                    score = score + 1
                else:
                    st.markdown('<div class="bad-box">❌ GHALAT HAI - Hashtag Nahi Lage - Search Me Nahi Aayega</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Description Ke End Me 5 Hashtag Lagao. Misaal: #SeaView #KarachiVlog #PakistaniVlogger #AliMahi</div>', unsafe_allow_html=True)
                # 5 Tags
                total = total + 1
                if len(tags) >= 5:
                    st.markdown(f'<div class="good-box">✅ THEEK HAI - Tags Lage Hue Hain: {len(tags)} Tags - Good</div>', unsafe_allow_html=True)
                    score = score + 1
                else:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Tags Kam Hain: {len(tags)} Tags - Kam Se Kam 10 Hone Chahiye</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: YouTube Studio Me Jao - Tags Me Ye Lagao: Sea View, Karachi, Vlog, Pakistani Vlogger, Tumhara Topic, 10 Tags Lagao.</div>', unsafe_allow_html=True)
                # 6 Like Ratio
                total = total + 1
                if like_ratio >= 4:
                    st.markdown(f'<div class="good-box">✅ THEEK HAI - Like Ratio Acha Hai: {like_ratio:.2f}% - Logon Ko Pasand Aaya</div>', unsafe_allow_html=True)
                    score = score + 1
                elif like_ratio >= 2:
                    st.markdown(f'<div class="warn-box">⚠️ THORA GHALAT - Like Ratio Thora Kam Hai: {like_ratio:.2f}% - 4%+ Hona Chahiye</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Video Ke Shuru Me Aur End Me Bolo "Like Kar Do". Log Bhool Jate Hain, Yaad Dilao.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Like Ratio Bohat Kam Hai: {like_ratio:.2f}% - Log Dekh Rahe Hain, Like Nahi Kar Rahe</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Video Ka Pehla 10 Second Boring Hai. Pehle 10 Second Me Sab Se Interesting Part Dikhao, Phir Intro Karo.</div>', unsafe_allow_html=True)
                # 7 Comments
                total = total + 1
                if comments >= 20:
                    st.markdown(f'<div class="good-box">✅ THEEK HAI - Comments Ache Hain: {comments} - Engagement Acha Hai</div>', unsafe_allow_html=True)
                    score = score + 1
                else:
                    st.markdown(f'<div class="bad-box">❌ GHALAT HAI - Comments Bohat Kam Hain: {comments} - Log Baat Nahi Kar Rahe</div>', unsafe_allow_html=True)
                    st.markdown('<div class="fix-box">🔧 FIX KARO: Video Ke End Me Sawal Poocho. Misaal: "Tumne Kabhi Sea View Dekha Hai? Comment Me Batao". Log Jawab Denge.</div>', unsafe_allow_html=True)
                # Final Score
                st.write("---")
                final_score = int(score / total * 100)
                st.markdown(f"<h1 style='text-align:center; font-size:42px;'>🎯 VIDEO SCORE: {final_score} / 100 🎯</h1>", unsafe_allow_html=True)
                st.progress(final_score / 100)
                if final_score >= 80:
                    st.success("🔥 VIDEO BILKUL THEEK HAI - Isko Promote Karo, Ye Chalegi!")
                elif final_score >= 50:
                    st.warning("⚠️ VIDEO THEEK HAI, LEKIN KUCH GHALTIYAN HAIN - Upar Wale Fix Karo, Views Badh Jayenge")
                else:
                    st.error("❌ VIDEO ME BOHAT GHALTIYAN HAIN - Upar Wale Fix Karo, Warna Ye Video Nahi Chalegi")
                st.write("---")
                st.markdown("<h2>🤖 AI SE FULL FIX - Kya Karna Hai?</h2>", unsafe_allow_html=True)
                if st.button("AI Se Full Fix Plan Banao"):
                    with st.spinner("AI Fix Plan Bana Raha Hai..."):
                        ai_fix = call_gemini(f"Video Audit: Title '{title}', Description length {len(desc)}, Tags {len(tags)}, Views {views}, Likes {likes}, Like Ratio {like_ratio:.2f}%, Comments {comments}, Score {final_score}/100. Give in English + Urdu mix: 1) What is RIGHT in this video 2) What is WRONG - list 5 mistakes 3) How to FIX each mistake step by step 4) Give 3 better titles for this video 5) Give better description 6) Give 10 hashtags. Be specific and practical for Pakistani YouTuber.")
                    st.write(ai_fix)
                    st.code(ai_fix)
    st.write("---")
    st.subheader("Apne Channel Ki Latest Videos Ka Audit Karo - Ek Click Me")
    if st.button("Meri Latest Videos Ka Audit Karo"):
        if st.session_state.connected_channel:
            ch_data = get_channel_data(st.session_state.connected_channel)
            if ch_data:
                vids = get_channel_videos(ch_data["id"], 3)
                for v in vids:
                    st.write(f"**{v['snippet']['title'][:70]}** - Upar Wale Box Me Iska Link Paste Kar Ke Audit Karo")
                    st.write(f"Link: https://www.youtube.com/watch?v={v['id']['videoId']}")
        else:
            st.warning("Pehle Channel Connect Karo")

with tab2:
    st.header("Channel Dashboard")
    ch = st.text_input("Channel", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Channel Data"):
        data = get_channel_data(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            if "banner" in data.get("brandingSettings", {}).get("image", {}):
                st.image(data["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            st.image(snip["thumbnails"]["high"]["url"], width=100)
            st.subheader(snip["title"])
            c1, c2, c3 = st.columns(3)
            c1.metric("Subs", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Videos", stats.get("videoCount", "0"))
        else:
            st.error("Not Found")

with tab3:
    st.header("AI Title Generator")
    topic = st.text_input("Topic", "Sea View Karachi")
    niche = st.selectbox("Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate With AI"):
        with st.spinner("AI Thinking..."):
            st.write(call_gemini(f"For {niche} channel topic {topic}: Give 5 viral titles, 30 sec script, 10 hashtags, best time. In English."))

with tab4:
    st.header("Trends By Country")
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        selected_country_name = st.selectbox("Select Country", list(COUNTRIES.keys()), index=0)
    with col_c2:
        trend_category = st.selectbox("Category", ["All", "Gaming", "Vlog", "News", "Islamic", "Food", "Tech", "Cricket"])
    selected_code = COUNTRIES[selected_country_name]
    if st.button(f"Get Google Trends - {selected_country_name}"):
        with st.spinner("Fetching..."):
            st.write(call_gemini(f"Google Trends for {selected_country_name}, category {trend_category}. Top 10 keywords, volume, 1 video idea each, 5 rising. In English."))
    if st.button(f"Load YouTube Trending - {selected_country_name}"):
        with st.spinner("Loading..."):
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={selected_code}&maxResults=6&key={YOUTUBE_KEY}"
            r = requests.get(url, timeout=15).json()
        if "items" in r:
            for v in r["items"]:
                st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=300)
                st.write(v["snippet"]["title"][:70])
                st.link_button("Watch", f"https://www.youtube.com/watch?v={v['id']}")

with tab5:
    st.header("RPM Calculator")
    views = st.number_input("Views Per Month?", value=100000)
    niche_rpm = st.selectbox("Niche?", ["Vlog - 1 Dollar", "Gaming - 1.5 Dollar", "Tech - 3 Dollar", "Finance - 5 Dollar", "Islamic - 1.2 Dollar", "Food - 1.8 Dollar"])
    rpm_val = float(niche_rpm.split("-")[1].strip().split(" ")[0])
    earning = (views / 1000) * rpm_val
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly Dollar", f"{earning:.2f} USD")
    c2.metric("Monthly Rupees", f"{earning*280:,.0f} PKR")
    c3.metric("Yearly Dollar", f"{earning*12:.2f} USD")

with tab6:
    st.header("Competitor Analysis")
    comp = st.text_input("Competitor Name", "@DuckyBhai")
    if st.button("Analyze Competitor"):
        data = get_channel_data(comp)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            st.image(snip["thumbnails"]["high"]["url"], width=100)
            st.subheader(snip["title"])
            c1, c2, c3 = st.columns(3)
            c1.metric("Subs", f"{int(stats.get('subscriberCount', '0')):,}")
            c2.metric("Views", f"{int(stats.get('viewCount', '0')):,}")
            c3.metric("Videos", stats.get("videoCount", "0"))

with tab7:
    st.header("Thumbnail Ideas")
    th_topic = st.text_input("Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas"):
        st.write(call_gemini(f"For topic {th_topic} give 5 viral thumbnail ideas. Text, Color, Face, Background."))

with tab8:
    st.header("Channel Audit")
    audit_ch = st.text_input("Channel To Audit", value=st.session_state.connected_channel if st.session_state.connected_channel else "@AliMahiVlogs", key="audit_ch")
    if st.button("Run Channel Audit"):
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
            st.write(call_gemini(f"Audit channel {snip['title']}, Subs {subs}, Views {views}, Videos {vcount}, Avg {avg_views}, Score {score}/100. Give 5 fixes."))

st.write("---")
st.write("RANKTUBE PRO | Ali Mahi | Version 9.0 - Video Audit")
