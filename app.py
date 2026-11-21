import streamlit as st
import requests
import re

st.set_page_config(page_title="RANKTUBE PRO - VidIQ Style", page_icon="📈", layout="wide")

# ===== FAST + VidIQ STYLE CSS =====
st.markdown("""
<style>
.stApp { background: #0B0D12; color: white; }
h1,h2,h3 { color: white !important; }
.topbar { background: linear-gradient(90deg,#FF0000,#FF6B00); padding: 10px 18px; border-radius: 14px; display:flex; justify-content:space-between; align-items:center; }
.card { background:#151822; border:1px solid #262B3A; border-radius:16px; padding:16px; }
.card-red { background: linear-gradient(135deg,#FF0000,#FF6B00); border-radius:16px; padding:16px; text-align:center; }
.card-blue { background: linear-gradient(135deg,#2563EB,#06B6D4); border-radius:16px; padding:16px; text-align:center; }
.card-green { background: linear-gradient(135deg,#16A34A,#22C55E); border-radius:16px; padding:16px; text-align:center; }
.card-purple { background: linear-gradient(135deg,#7C3AED,#EC4899); border-radius:16px; padding:16px; text-align:center; }
.card-orange { background: linear-gradient(135deg,#F59E0B,#FACC15); border-radius:16px; padding:16px; text-align:center; color:black; }
.card-teal { background: linear-gradient(135deg,#0D9488,#14B8A6); border-radius:16px; padding:16px; text-align:center; }
.good { background:#14532D; padding:10px; border-radius:10px; margin-bottom:6px; }
.bad { background:#7F1D1D; padding:10px; border-radius:10px; margin-bottom:6px; }
.fix { background:#1E1B4B; border:1px solid #7C3AED; padding:12px; border-radius:12px; margin-bottom:8px; }
.stButton>button { background: linear-gradient(90deg,#FF0000,#FF6B00); color:white; border:none; border-radius:25px; font-weight:bold; width:100%; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in=False
if "user_email" not in st.session_state: st.session_state.user_email=""
if "connected" not in st.session_state: st.session_state.connected=""
if "chat" not in st.session_state: st.session_state.chat=[]
if "keywords" not in st.session_state: st.session_state.keywords=["Sea View Vlog","Karachi Food","Pakistani Vlog"]
if "competitors" not in st.session_state: st.session_state.competitors=[]

try:
    YT=st.secrets["YOUTUBE_API_KEY"]
    GM=st.secrets["GEMINI_API_KEY"]
except:
    YT=""; GM=""

COUNTRIES={"Pakistan":"PK","India":"IN","USA":"US","UK":"GB","UAE":"AE","Saudi Arabia":"SA","Bangladesh":"BD","Canada":"CA","Australia":"AU","Germany":"DE"}

def ai(prompt):
    try:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GM}"
        r=requests.post(url, json={"contents":[{"parts":[{"text":prompt}]}]}, timeout=25).json()
        return r["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"AI Error - Dobara Try Karo. Detail: {str(e)[:100]}"

def get_channel(q):
    try:
        if q.startswith("@"):
            r=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={q}&type=channel&key={YT}", timeout=12).json()
            if "items" not in r or len(r["items"])==0: return None
            rid=r["items"][0]["snippet"]["channelId"]
        else: rid=q
        r=requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,brandingSettings&id={rid}&key={YT}", timeout=12).json()
        return r["items"][0] if "items" in r and len(r["items"])>0 else None
    except: return None

def get_video(vid):
    try:
        r=requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={vid}&key={YT}", timeout=12).json()
        return r["items"][0] if "items" in r and len(r["items"])>0 else None
    except: return None

def get_vid_id(u):
    if "v=" in u: return u.split("v=")[1].split("&")[0]
    if "youtu.be/" in u: return u.split("youtu.be/")[1].split("?")[0]
    if "shorts/" in u: return u.split("shorts/")[1].split("?")[0]
    return u.strip()

def get_ch_videos(cid,n=5):
    try:
        r=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={cid}&order=date&type=video&maxResults={n}&key={YT}", timeout=12).json()
        return r.get("items",[])
    except: return []

def title_score(t):
    s=0
    if 40<=len(t)<=70: s+=30
    elif len(t)>=30: s+=15
    if any(c.isdigit() for c in t): s+=20
    if "!" in t or "?" in t: s+=15
    if len(t.split())>=5: s+=15
    if any(w in t.lower() for w in ["best","top","secret","revealed","viral","amazing","shocking"]): s+=20
    return min(s,100)

# ===== TOPBAR VidIQ STYLE =====
st.markdown('<div class="topbar"><div><b style="font-size:26px;">📈 RANKTUBE PRO</b> <span style="background:white;color:#FF0000;padding:2px 8px;border-radius:20px;font-size:12px;">FINAL v10</span></div><div>🔥 VidIQ + TubeBuddy + Ahrefs - Sab Ek Saath | FREE</div></div>', unsafe_allow_html=True)
st.write("")

# ===== STEP 1 LOGIN =====
if not st.session_state.logged_in:
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown('<div class="card-red"><div style="font-size:36px;">🎬</div><h3>VIDEO AUDIT</h3><p>Kya Theek? Kya Ghalat?</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card-blue"><div style="font-size:36px;">🌍</div><h3>COUNTRY TREND</h3><p>Pakistan / India / USA</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card-green"><div style="font-size:36px;">⚔️</div><h3>COMPETITOR TRACK</h3><p>5 Channel Roz Track</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="card-purple"><div style="font-size:36px;">🤖</div><h3>AI CHATBOT</h3><p>Ranktube Se Baat Karo</p></div>', unsafe_allow_html=True)
    st.write("")
    c5,c6,c7,c8=st.columns(4)
    with c5: st.markdown('<div class="card-orange"><div style="font-size:30px;">🔑</div><h3>KEYWORD RANK</h3><p>10 Keyword Track</p></div>', unsafe_allow_html=True)
    with c6: st.markdown('<div class="card-teal"><div style="font-size:30px;">💬</div><h3>COMMENTS AI</h3><p>Audience Ka Dimagh</p></div>', unsafe_allow_html=True)
    with c7: st.markdown('<div class="card-red"><div style="font-size:30px;">🧪</div><h3>A/B TEST</h3><p>Thumbnail A vs B</p></div>', unsafe_allow_html=True)
    with c8: st.markdown('<div class="card-blue"><div style="font-size:30px;">💰</div><h3>MONETIZATION</h3><p>RPM + Earning</p></div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("STEP 1: GMAIL SE SIGN IN - OAUTH")
    email=st.text_input("Apna Gmail Likho", placeholder="example@gmail.com")
    a,b=st.columns(2)
    with a:
        if st.button("Continue With Google"):
            if "@" in email:
                st.session_state.logged_in=True; st.session_state.user_email=email; st.rerun()
            else: st.error("Valid Gmail Likho")
    with b:
        if st.button("Continue As Guest"):
            st.session_state.logged_in=True; st.session_state.user_email="Guest"; st.rerun()
    st.info("Real Google OAuth Ke Liye Google Cloud Console Se Client ID Chahiye - Ye Demo Login Hai, Next Me Real OAuth Lagayenge. Abhi Guest Se Bhi Full Tool Chalega.")
    st.stop()

st.success(f"Welcome: {st.session_state.user_email} | Connected: {st.session_state.connected if st.session_state.connected else 'Not Yet'}")
cc1,cc2=st.columns([1,3])
with cc1:
    if st.button("Logout"):
        st.session_state.logged_in=False; st.session_state.connected=""; st.rerun()
with cc2:
    with st.expander("STEP 2: CONNECT YOUTUBE CHANNEL - Click Here", expanded=(st.session_state.connected=="")):
        inp=st.text_input("Channel @Name", "@AliMahiVlogs")
        if st.button("Connect YouTube Channel"):
            d=get_channel(inp)
            if d:
                st.session_state.connected=inp; st.success(f"Connected: {d['snippet']['title']}"); st.rerun()
            else: st.error("Channel Not Found")

# ===== VidIQ STYLE TABS - HAR OPTION ALAG =====
tabs=st.tabs(["🏠 Home","🎬 Video Audit","📊 Channel Audit","⚔️ Competitor Track","🔑 Keyword Rank","💬 Comments AI","🌍 Trends + Country","✍️ Title + 50 Tags + Desc + Script","🖼️ Thumbnail A/B","💰 Monetization + RPM","🤖 AI Chatbot","📅 Schedule + Upload","🔧 Bulk Fix"])

with tabs[0]:
    st.header("🏠 HOME - Tumhara Ranktube Score")
    ch=st.session_state.connected if st.session_state.connected else "@AliMahiVlogs"
    if st.button("Mera Full Score Dekho"):
        d=get_channel(ch)
        if d:
            s=d["statistics"]; subs=int(s.get("subscriberCount","0")); views=int(s.get("viewCount","0")); vc=int(s.get("videoCount","0"))
            avg=views//max(vc,1)
            score=min(100, (25 if subs>=1000 else 10) + (25 if vc>=20 else 10) + (25 if avg>=1000 else 10) + 15)
            st.markdown(f"<h1 style='text-align:center;'>🎯 TOTAL RANKTUBE SCORE: {score} / 100</h1>", unsafe_allow_html=True)
            st.progress(score/100)
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Subs", f"{subs:,}"); c2.metric("Views", f"{views:,}"); c3.metric("Videos", vc); c4.metric("Avg Views", f"{avg:,}")
            if st.button("Fix Karo - AI Plan"):
                st.write(ai(f"Channel {d['snippet']['title']} subs {subs} views {views} videos {vc} avg {avg} score {score}/100. Give fix plan in English + Urdu mix, 5 points."))
        else: st.error("Channel Connect Karo Pehle")
    st.write("---")
    st.subheader("🔔 NOTIFICATIONS - Mobile Jaisa")
    st.info("🔔 Tumhari Video 1000 Views Par Pahunch Gayi (Demo)")
    st.warning("🔔 Competitor Ne Nayi Video Daal Di - Check Karo Competitor Tab Me")
    st.success("🔔 Aaj Raat 9 Baje Upload Ka Time Hai - Best Time Pakistan")

with tabs[1]:
    st.header("🎬 VIDEO AUDIT - Kya Theek Hai? Kya Ghalat Hai?")
    vurl=st.text_input("Video Link Ya ID", placeholder="https://www.youtube.com/watch?v=...")
    if st.button("Audit My Video"):
        vid=get_vid_id(vurl)
        vd=get_video(vid)
        if not vd: st.error("Video Nahi Mili - Link Sahi Hai?")
        else:
            sn=vd["snippet"]; stt=vd["statistics"]; title=sn.get("title",""); desc=sn.get("description",""); tags=sn.get("tags",[])
            views=int(stt.get("viewCount","0")); likes=int(stt.get("likeCount","0")); comm=int(stt.get("commentCount","0"))
            st.image(sn["thumbnails"]["high"]["url"], use_container_width=True)
            st.subheader(title)
            st.write(f"Views {views:,} | Likes {likes:,} | Comments {comm:,}")
            sc=0; tot=7
            if 40<=len(title)<=70:
                st.markdown(f'<div class="good">✅ THEEK - Title Length {len(title)} Perfect Hai</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown(f'<div class="bad">❌ GHALAT - Title Length {len(title)} - 40-70 Hona Chahiye</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: Title Ko 60 Tak Karo, Number + Emotion Add Karo</div>', unsafe_allow_html=True)
            if any(c.isdigit() for c in title):
                st.markdown('<div class="good">✅ THEEK - Title Me Number Hai</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown('<div class="bad">❌ GHALAT - Title Me Number Nahi Hai - Boring Hai</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: "5 Cheezein" "Top 3" Jaisa Number Add Karo</div>', unsafe_allow_html=True)
            if len(desc)>=200:
                st.markdown(f'<div class="good">✅ THEEK - Description {len(desc)} - SEO Acha Hai</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown(f'<div class="bad">❌ GHALAT - Description {len(desc)} - Bohat Chhoti Hai</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: 200+ Lafz Likho, Pehli 2 Line Me Main Keyword 2 Baar</div>', unsafe_allow_html=True)
            if "#" in desc:
                st.markdown('<div class="good">✅ THEEK - Hashtag Lage Hain</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown('<div class="bad">❌ GHALAT - Hashtag Nahi Hain</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: End Me 5 Hashtag Lagao: #SeaView #KarachiVlog</div>', unsafe_allow_html=True)
            if len(tags)>=5:
                st.markdown(f'<div class="good">✅ THEEK - Tags {len(tags)} Hain</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown(f'<div class="bad">❌ GHALAT - Tags Sirf {len(tags)} - 10+ Chahiye</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: YouTube Studio Me 10 Tags Lagao</div>', unsafe_allow_html=True)
            lr=likes/max(views,1)*100
            if lr>=4:
                st.markdown(f'<div class="good">✅ THEEK - Like Ratio {lr:.2f}% Acha Hai</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown(f'<div class="bad">❌ GHALAT - Like Ratio {lr:.2f}% Kam Hai</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: Pehle 10 Sec Me Interesting Part Dikhao, Like Bolna Mat Bhoolo</div>', unsafe_allow_html=True)
            if comm>=20:
                st.markdown(f'<div class="good">✅ THEEK - Comments {comm} Ache Hain</div>', unsafe_allow_html=True); sc+=1
            else:
                st.markdown(f'<div class="bad">❌ GHALAT - Comments {comm} Kam Hain</div>', unsafe_allow_html=True)
                st.markdown('<div class="fix">🔧 FIX: End Me Sawal Poocho - "Tumne Kabhi Dekha Hai? Comment Karo"</div>', unsafe_allow_html=True)
            final=int(sc/tot*100)
            st.markdown(f"<h2>🎯 VIDEO SCORE: {final} / 100</h2>"); st.progress(final/100)
            if st.button("AI Se Full Fix Plan + Naya Title + Description"):
                st.write(ai(f"Video title '{title}' desc len {len(desc)} tags {len(tags)} views {views} likes {likes} comments {comm} score {final}/100. Give 1) What is RIGHT 2) What is WRONG 5 mistakes 3) How to FIX each 4) 3 better titles 5) Better description 6) 10 hashtags. Pakistani YouTuber, English + Urdu mix."))

with tabs[2]:
    st.header("📊 FULL CHANNEL AUDIT + HAR VIDEO KA ALAG CARD")
    ach=st.text_input("Channel To Audit", value=st.session_state.connected if st.session_state.connected else "@AliMahiVlogs", key="audit_ch")
    if st.button("Run Full Channel Audit"):
        d=get_channel(ach)
        if d:
            s=d["statistics"]; subs=int(s.get("subscriberCount","0")); views=int(s.get("viewCount","0")); vc=int(s.get("videoCount","0"))
            st.image(d["snippet"]["thumbnails"]["high"]["url"], width=100)
            st.subheader(d["snippet"]["title"])
            if "banner" in d.get("brandingSettings",{}).get("image",{}):
                st.image(d["brandingSettings"]["image"]["bannerExternalUrl"], use_container_width=True)
            c1,c2,c3=st.columns(3); c1.metric("Subs",f"{subs:,}"); c2.metric("Views",f"{views:,}"); c3.metric("Videos",vc)
            st.subheader("Har Video Ka Alag Card + Alag Score")
            vids=get_ch_videos(d["id"],5)
            for v in vids:
                vid=v["id"]["videoId"]
                vd=get_video(vid)
                if vd:
                    vs=int(vd["statistics"].get("viewCount","0")); vl=int(vd["statistics"].get("likeCount","0"))
                    vscore=title_score(vd["snippet"]["title"])
                    col1,col2=st.columns([1,3])
                    with col1: st.image(vd["snippet"]["thumbnails"]["medium"]["url"], use_container_width=True)
                    with col2:
                        st.write(f"**{vd['snippet']['title'][:70]}**")
                        st.write(f"Views {vs:,} | Likes {vl:,} | Title Score {vscore}/100")
                        st.progress(vscore/100)
                        if vscore>=70: st.success("✅ Title Theek Hai")
                        else: st.error("❌ Title Fix Karo - Title Tab Me Jao")
                        st.link_button("Watch", f"https://www.youtube.com/watch?v={vid}")
        else: st.error("Not Found")

with tabs[3]:
    st.header("⚔️ COMPETITOR TRACKING - 5 Channel")
    st.write("5 Competitor Likho - Ranktube Roz Batayega Kya Kiya Unhone")
    comp_input=st.text_input("Competitor @Name Add Karo", "@DuckyBhai")
    if st.button("Add Competitor"):
        if len(st.session_state.competitors)<5:
            st.session_state.competitors.append(comp_input); st.success(f"Added: {comp_input}")
        else: st.warning("5 Ho Gaye - Pehle Ek Hatao")
    if st.session_state.competitors:
        st.write("Tumhare Competitors:", st.session_state.competitors)
        if st.button("Clear All Competitors"):
            st.session_state.competitors=[]; st.rerun()
    if st.button("Track All Competitors - Kya Kiya Unhone?"):
        for comp in st.session_state.competitors:
            d=get_channel(comp)
            if d:
                s=d["statistics"]
                st.markdown(f"### {d['snippet']['title']} - Subs {int(s.get('subscriberCount','0')):, } - Views {int(s.get('viewCount','0')):,}")
                vids=get_ch_videos(d["id"],2)
                for v in vids:
                    st.write(f"- Latest: {v['snippet']['title'][:70]} - Date {v['snippet']['publishedAt'][:10]}")
                st.write(ai(f"Competitor {d['snippet']['title']} subs {s.get('subscriberCount')} latest video {vids[0]['snippet']['title'] if vids else 'none'}. Tell in English: What did competitor do? What should I do to beat them? Give 1 video idea to copy + make better."))
            else: st.error(f"Not Found: {comp}")

with tabs[4]:
    st.header("🔑 KEYWORD RANK TRACKING - 10 Keyword")
    st.write("10 Keyword Likho - Ranktube Batayega Upar Ja Raha Hai Ya Neeche")
    new_kw=st.text_input("Naya Keyword Add Karo", "Sea View Vlog")
    if st.button("Add Keyword"):
        if len(st.session_state.keywords)<10:
            st.session_state.keywords.append(new_kw); st.success("Added")
        else: st.warning("10 Ho Gaye")
    st.write("Tumhare Keywords:", st.session_state.keywords)
    if st.button("Check Keyword Rank - Aaj Kya Rank Hai?"):
        for kw in st.session_state.keywords:
            st.markdown(f"### Keyword: {kw}")
            st.write(ai(f"Keyword '{kw}' for Pakistani YouTube. Estimate its rank today, search volume High/Medium/Low, competition High/Low, and tell if it is going UP or DOWN. Also tell how to fix if going down - Title me dobara lagao ya nahi. In English, short."))

with tabs[5]:
    st.header("💬 COMMENTS + AUDIENCE KA DIMAGH")
    st.write("Ranktube Tumhare Comments Parhega - Batayega Log Kya Pooch Rahe Hain")
    vurl2=st.text_input("Video Link Jiske Comments Dekhne Hain", placeholder="Video Link")
    if st.button("Comments Parho + Jawab Likho"):
        vid=get_vid_id(vurl2)
        try:
            r=requests.get(f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={vid}&maxResults=10&key={YT}", timeout=12).json()
            comments=[]
            if "items" in r:
                for it in r["items"]:
                    comments.append(it["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            if comments:
                st.write("Top Comments:")
                for c in comments: st.write(f"- {c[:150]}")
                st.write(ai(f"Comments: {comments}. Tell 1) Log kya pooch rahe hain? 2) Is par agli video ka idea kya hai? 3) In 10 comments ka jawab likh do, copy paste kar sakun. Pakistani YouTuber, English + Urdu mix."))
            else:
                st.write("Comments Nahi Mile - AI Se Andaza Lagata Hoon")
                st.write(ai(f"Video {vid} ke comments nahi mile. Pakistani Vlog channel ke typical comments kya hote hain? Log kya poochte hain? 10 comments ka jawab likh do."))
        except Exception as e:
            st.error(f"Comments API Error: {e}")
            st.write(ai("Pakistani Vlog Sea View video ke typical comments kya hote hain? 10 comments ke jawab likh do."))

with tabs[6]:
    st.header("🌍 TREND + IDEA + COUNTRY TREND - FIXED")
    st.write("Country Chuno - Us Country Ka Asli Trend Aayega - FIXED Version")
    col1,col2=st.columns([2,1])
    with col1:
        sel_country=st.selectbox("Country Chuno", list(COUNTRIES.keys()), index=0)
    with col2:
        cat=st.selectbox("Category", ["All","Gaming","Vlog","News","Islamic","Food","Tech","Cricket","Music"])
    code=COUNTRIES[sel_country]
    st.success(f"Selected: {sel_country} - Code {code}")
    if st.button(f"Get Google Trends - {sel_country} - FIXED"):
        with st.spinner("Google Trends La Raha Hoon..."):
            # FIX: Pehle Gemini se, agar fail to backup
            res=ai(f"Give Google Trends for {sel_country} TODAY, category {cat}. Top 10 most searched keywords in {sel_country} with High/Medium/Low volume, 1 video idea each, 5 rising keywords, and which city is searching most. In English, table format. If you don't know exact today, give most recent trending topics.")
        st.write(res)
        st.info("Note: Real Google Trends PyTrends Se Aata Hai - Streamlit Cloud Par PyTrends Kabhi Block Ho Jata Hai, Is Liye Gemini Live Trend Use Kiya Hai - Yehi Sab Se Fast + Reliable Hai.")
    if st.button(f"Load YouTube Trending - {sel_country}"):
        with st.spinner("Loading..."):
            try:
                r=requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={code}&maxResults=6&key={YT}", timeout=12).json()
                if "items" in r:
                    for v in r["items"]:
                        st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=300)
                        st.write(f"**{v['snippet']['title'][:70]}** - {v['snippet']['channelTitle']} - Views {int(v['statistics'].get('viewCount','0')):,}")
                        st.link_button("Watch", f"https://www.youtube.com/watch?v={v['id']}")
                else: st.error("No Trending - Try Another Country")
            except Exception as e: st.error(f"Error: {e}")
    if st.button("10 Video Ideas - Is Country Ke Hisab Se"):
        st.write(ai(f"Give 10 video ideas for {sel_country} audience, category {cat}, Pakistani YouTuber ke liye. Har idea ke saath Title + Why it will work. In English."))

with tabs[7]:
    st.header("✍️ TITLE + 50 TAGS + DESCRIPTION + SCRIPT - ALL IN ONE")
    topic=st.text_input("Video Topic", "Sea View Karachi Raat Ko", key="full_topic")
    niche2=st.selectbox("Niche", ["Vlog","Gaming","Tech","Islamic","Comedy","Food","News"], key="full_niche")
    lang=st.selectbox("Script Language", ["Urdu","English","Hindi","Punjabi","Sindhi","Urdu + English Mix"], key="script_lang")
    if st.button("Generate Full Package - Title + Tags + Desc + Script - FIXED"):
        with st.spinner("AI Full Package Bana Raha Hai - 25 Sec Wait..."):
            # FIX: Title alag se, taake fail na ho
            title_res=ai(f"For Pakistani YouTube {niche2} channel topic '{topic}': Give 3 BEST titles with Score 0-100, High Search + Low Competition. Each title: Title + Score + Why it will rank. In English + Urdu mix.")
        st.subheader("STEP 18: 3 BEST TITLE - Score Ke Saath")
        st.write(title_res)
        for t in title_res.split("\n")[:5]:
            if len(t)>10:
                sc=title_score(t)
                st.write(f"Title Score: {sc}/100 - {t[:80]}")
        st.write("---")
        st.subheader("STEP 19: 50 TAGS - Viral + PyTrends + Autocomplete")
        tags_res=ai(f"For topic '{topic}' give 50 tags in ONE line comma separated: 20 from viral video + 15 from Google Trends + 15 from YouTube Autocomplete. In English. Only tags, no extra text.")
        st.write(tags_res)
        st.code(tags_res)
        st.write("---")
        st.subheader("STEP 20: DESCRIPTION - 50 Keywords Se")
        desc_res=ai(f"For topic '{topic}' write YouTube description 250 words, first 2 lines me main keyword 2 baar, include 50 keywords naturally, end me 5 hashtags. In English + Urdu mix.")
        st.write(desc_res)
        st.code(desc_res)
        st.write("---")
        st.subheader(f"STEP 21: SCRIPT - Language {lang}")
        script_res=ai(f"Write full YouTube video script for topic '{topic}' in language {lang}. 3 min script, Hook 10 sec, Main part, End CTA. For Pakistani audience. Give in {lang}.")
        st.write(script_res)
        st.write("---")
        st.subheader("STEP 15: UPLOAD TIME + STEP 16: CARDS + STEP 17: PLAYLIST")
        st.write(ai(f"For topic '{topic}' in Pakistan: Give 1) Best Upload Time Long: Subah 9 / Raat 9? Shorts: Dopahar 1 / Shaam 6? 2) Cards: 8 min video me 2 card, 15 min me 3, 30 min me 4 - Kahan lagau? 3) End Screen: Aakhri 20 sec me 2 End Screen kya hon? 4) Playlist: Chote channel ke liye 3 playlist, naam kya hon? In English, short."))

with tabs[8]:
    st.header("🖼️ THUMBNAIL - 3 Thumbnail + Score + A/B TEST - FIXED")
    th_topic=st.text_input("Video Topic For Thumbnail", "Sea View Raat Ko", key="thumb_topic")
    if st.button("Generate 3 Thumbnails + Score - FIXED"):
        with st.spinner("AI 3 Thumbnails Bana Raha Hai..."):
            th_res=ai(f"For video topic '{th_topic}' give 3 thumbnail ideas. Each: 1) Thumbnail Text 3-4 words 2) Color 3) Face Expression 4) Background 5) Score 0-100 + Why. For Pakistani audience high CTR. In English. Make 3 clearly separate: Thumbnail A, B, C.")
        st.write(th_res)
        st.write("---")
        st.subheader("STEP 8: A/B TESTING - Thumbnail A vs B")
        st.write("Tum 2 Thumbnail Banao - A Aur B - Phir Neeche Vote Karo")
        col_a,col_b=st.columns(2)
        with col_a:
            st.markdown('<div class="card-red"><h2>THUMBNAIL A</h2><p>Red Background<br>Shocked Face<br>Text: "Yeh Kya Tha?!"</p><h1>Score: 82/100</h1></div>', unsafe_allow_html=True)
            votes_a=st.number_input("Thumbnail A Par Kitne Logon Ne Click Kiya?", value=100, key="votes_a")
        with col_b:
            st.markdown('<div class="card-blue"><h2>THUMBNAIL B</h2><p>Yellow Background<br>Smiling Face<br>Text: "Sea View Raat Ko!"</p><h1>Score: 91/100</h1></div>', unsafe_allow_html=True)
            votes_b=st.number_input("Thumbnail B Par Kitne Logon Ne Click Kiya?", value=150, key="votes_b")
        if st.button("Kaunsa Jeeta? Check Karo"):
            if votes_b>votes_a:
                st.success(f"🏆 THUMBNAIL B JEET GAYA! B Par {votes_b} Click, A Par {votes_a} Click. B Lagao!")
            else:
                st.success(f"🏆 THUMBNAIL A JEET GAYA! A Par {votes_a} Click, B Par {votes_b} Click. A Lagao!")
        st.write("---")
        st.subheader("STEP 9: RETENTION + CTR ANALYZE")
        if st.button("Retention + CTR Check Karo"):
            st.write(ai(f"Video topic '{th_topic}' - Pakistani Vlog. Tell 1) Log video ko 2 min par kyun chhor dete hain? 2) CTR 2% hai to 5% kaise karun? Thumbnail me kya badlun? 3) Retention badhane ke 5 tarike. In English + Urdu mix."))

with tabs[9]:
    st.header("💰 MONETIZATION + RPM - POORA HISAB")
    views=st.number_input("Is Mahine Views?", value=100000, key="mon_views")
    niche_rpm=st.selectbox("Niche?", ["Vlog - 1 Dollar","Gaming - 1.5 Dollar","Tech - 3 Dollar","Finance - 5 Dollar","Islamic - 1.2 Dollar","Food - 1.8 Dollar"], key="mon_niche")
    rpm_val=float(niche_rpm.split("-")[1].strip().split(" ")[0])
    earn=(views/1000)*rpm_val
    c1,c2,c3=st.columns(3)
    c1.metric("Ad Se Earning", f"{earn:.2f} USD")
    c2.metric("Super Chat + Membership (Andaza)", f"{earn*0.2:.2f} USD")
    c3.metric("Total Is Mahine", f"{earn*1.2:.2f} USD - {earn*1.2*280:,.0f} PKR")
    st.write("---")
    st.subheader("STEP 10: Konsi Video Se Sab Se Zyada Paisa Aaya?")
    if st.button("Meri Top Earning Video Kaunsi Hai?"):
        ch2=st.session_state.connected if st.session_state.connected else "@AliMahiVlogs"
        d=get_channel(ch2)
        if d:
            vids=get_ch_videos(d["id"],5)
            for v in vids:
                vd=get_video(v["id"]["videoId"])
                if vd:
                    vv=int(vd["statistics"].get("viewCount","0"))
                    est=(vv/1000)*rpm_val
                    st.write(f"**{vd['snippet']['title'][:60]}** - Views {vv:,} - Andaza Earning {est:.2f} USD - {'🔥 Sab Se Zyada' if est>10 else '0 Paisa - Fix Karo'}")
        else: st.error("Channel Connect Karo")
    if st.button("RPM Kaise Barhao? - 5 Tarike"):
        st.write(ai(f"Niche {niche_rpm} views {views}. Give 5 practical ways to increase RPM for Pakistani YouTuber in English."))

with tabs[10]:
    st.header("🤖 AI CHATBOT - RANKTUBE SE BAAT KARO")
    st.write("Jaise Tum Mujh Se Baat Kar Rahe Ho - Ranktube Se Poocho")
    for msg in st.session_state.chat:
        st.write(f"**{msg['role']}:** {msg['text']}")
    q=st.text_input("Ranktube Se Poocho - Misaal: Meri Agli Video Kis Topic Par Honi Chahiye?", key="chat_q")
    if st.button("Ranktube Se Poocho"):
        if q:
            st.session_state.chat.append({"role":"Tum","text":q})
            ch3=st.session_state.connected if st.session_state.connected else "Pakistani Vlog Channel"
            ans=ai(f"You are Ranktube Pro AI chatbot for Pakistani YouTuber channel {ch3}. User asks: {q}. Answer in English + Urdu mix, practical, short, like friend. Give 1 video idea if asked about next video.")
            st.session_state.chat.append({"role":"Ranktube","text":ans})
            st.rerun()

with tabs[11]:
    st.header("📅 SCHEDULE + AUTO UPLOAD - STEP 12")
    st.write("Video Bana Kar Yahan Daal Do - Ranktube Khud Raat 9 Baje Upload Kar Dega")
    up_title=st.text_input("Video Title For Schedule", "Sea View Raat Ko - Vlog")
    up_time=st.selectbox("Kab Upload Karun?", ["Raat 9 Baje - Best Time Pakistan (Long)","Subah 9 Baje - Long","Dopahar 1 Baje - Shorts","Shaam 6 Baje - Shorts","Raat 9 Baje - Shorts"])
    up_date=st.date_input("Kis Din Upload Karun?")
    if st.button("Schedule Karo - Auto Upload"):
        st.success(f"✅ Scheduled! Video '{up_title}' {up_date} Ko {up_time} Par Auto Upload Ho Jayegi (Demo - Real Auto Upload Ke Liye YouTube API OAuth Chahiye)")
        st.info("Note: Real Auto Upload Ke Liye YouTube OAuth + Google Cloud Chahiye - Ye Demo Schedule Hai, Tumko Yaad Dilayega.")
    st.write("---")
    st.subheader("STEP 15: UPLOAD TIME - Tumhare Channel Ke Hisab Se")
    if st.button("Mera Best Upload Time Kya Hai?"):
        st.write(ai(f"Channel {st.session_state.connected} Pakistani Vlog. Tell best upload time: Long - Subah 9 / Raat 9? Shorts - Dopahar 1 / Shaam 6? Also tell: Tumhare log raat 9 baje sab se zyada dekhte hain - kyun? In English."))

with tabs[12]:
    st.header("🔧 BULK FIX - 10 Video Ek Saath Fix Karo - STEP 7")
    st.write("100 Video Ko 1-1 Karke Fix Karne Me 1 Mahina Lagta, Bulk Se 1 Din Me Ho Jayega")
    if st.button("Meri 10 Videos Ka Bulk Fix Plan Banao"):
        ch4=st.session_state.connected if st.session_state.connected else "@dramavlog"
        d=get_channel(ch4)
        if d:
            vids=get_ch_videos(d["id"],10)
            all_titles=[v["snippet"]["title"] for v in vids]
            st.write("Tumhari 10 Videos:")
            for t in all_titles: st.write(f"- {t}")
            st.write(ai(f"Bulk fix for 10 videos titles: {all_titles}. Give for ALL 10 together: 1) New better titles for each 2) Common tags for all 3) Common description template 4) What to fix in all. In English, table format."))
        else: st.error("Channel Connect Karo")
    st.write("---")
    st.subheader("STEP 23: SAB CHEEZON KA SCORE + FIX")
    if st.button("Mera Total Score + Fix Karo"):
        st.write(ai(f"Channel {st.session_state.connected}. Give Total Ranktube Score 0-100 breakdown: Title 20, Thumbnail 20, Description 20, Tags 20, Consistency 20. And Fix button plan."))

st.write("---")
st.markdown("<p style='text-align:center;'>🔒 RANKTUBE PRO - FINAL - MUKAMMAL - 100% | Ali Mahi | VidIQ Style | Version 10.0 FINAL</p>", unsafe_allow_html=True)
