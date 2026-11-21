import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")

st.title("📈 RANKTUBE PRO")
st.write("Pakistan's No.1 YouTube Growth Tool - For Creators")

try:
    YOUTUBE_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    st.success("✅ Both Keys Connected - Real Data Ready")
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
        return "AI Error - Try Again After Some Time"

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
    url2 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={real_id}&key={YOUTUBE_KEY}"
    r = requests.get(url2).json()
    if "items" in r and len(r["items"]) > 0:
        return r["items"][0]
    return None

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "✍️ Title + Script", "🔥 Trending", "💰 RPM Calculator", "⚔️ Competitor", "🖼️ Thumbnail"])

with tab1:
    st.header("📊 Your Channel Dashboard")
    ch = st.text_input("Enter Your Channel @Name", "@AliMahiVlogs", key="dash_ch")
    if st.button("Get Real Data", key="dash_btn"):
        data = get_channel_data(ch)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            st.subheader(f"Channel: {snip['title']}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Subscribers", stats.get("subscriberCount", "0"))
            c2.metric("Total Views", stats.get("viewCount", "0"))
            c3.metric("Total Videos", stats.get("videoCount", "0"))
            subs = int(stats.get("subscriberCount", "0"))
            if subs < 1000:
                st.warning(f"You Need {1000-subs} More Subs For Monetization")
            else:
                st.success("Subs Complete For Monetization!")
            st.write(snip.get("description", "")[:500])
        else:
            st.error("Channel Not Found")

with tab2:
    st.header("✍️ AI Title + Script Generator")
    topic = st.text_input("Enter Topic", "Sea View Karachi")
    niche = st.selectbox("Select Niche", ["Vlog", "Gaming", "Tech", "Islamic", "Comedy", "Food", "News"])
    if st.button("Generate Title + Script With AI"):
        result = call_gemini(f"For Pakistani YouTube {niche} channel, topic '{topic}': Give 1) 5 viral high CTR titles in Urdu + English mix 2) 1 short 30 sec video script 3) 10 hashtags 4) Best upload time in Pakistan. Give in English + Urdu mix.")
        st.write(result)

with tab3:
    st.header("🔥 What Is Trending In Pakistan?")
    if st.button("Get Trending Topics"):
        result = call_gemini("Give Top 10 trending topics on YouTube in Pakistan this week - Vlog, Gaming, News, Islamic, Food. Give 1 video idea for each topic. Give in English.")
        st.write(result)
    st.write("---")
    st.subheader("Real Trending Videos On YouTube")
    if st.button("Show Real Trending Videos"):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=PK&maxResults=10&key={YOUTUBE_KEY}"
        r = requests.get(url).json()
        if "items" in r:
            for v in r["items"]:
                st.write(f"**{v['snippet']['title']}** - Views: {v['statistics'].get('viewCount','0')} - Channel: {v['snippet']['channelTitle']}")
        else:
            st.error("Trending Not Found - Check Key")

with tab4:
    st.header("💰 RPM / Earnings Calculator")
    views = st.number_input("How Many Views Per Month?", value=100000)
    niche_rpm = st.selectbox("What Is Your Niche?", ["Vlog - $1", "Gaming - $1.5", "Tech - $3", "Finance - $5", "Islamic - $1.2", "Food - $1.8"])
    rpm_val = float(niche_rpm.split("$")[1])
    earning = (views / 1000) * rpm_val
    st.metric("Monthly Earning (Estimate)", f"${earning:.2f} - Rs {earning*280:.0f}")
    st.write("This Is Estimate - Real RPM Shows In YouTube Studio")
    if st.button("How To Increase RPM? Ask AI"):
        st.write(call_gemini(f"How to increase RPM for Pakistani YouTube channel? Niche {niche_rpm}, views {views}. Give 5 practical tips."))

with tab5:
    st.header("⚔️ Check Competitor")
    comp = st.text_input("Enter Competitor @Name", "@DuckyBhai")
    if st.button("Get Competitor Data"):
        data = get_channel_data(comp)
        if data:
            stats = data["statistics"]
            snip = data["snippet"]
            c1, c2, c3 = st.columns(3)
            c1.metric("Their Subs", stats.get("subscriberCount", "0"))
            c2.metric("Their Views", stats.get("viewCount", "0"))
            c3.metric("Their Videos", stats.get("videoCount", "0"))
            st.write(f"Their Channel: {snip['title']}")
            st.write(f"Their Description: {snip.get('description','')[:300]}")
            if st.button("Ask AI - How To Beat Them?"):
                st.write(call_gemini(f"Competitor channel {snip['title']} has {stats.get('subscriberCount')} subs. My channel is small, how can I beat them? Give 5 strategies for Pakistani audience."))
        else:
            st.error("Competitor Not Found")

with tab6:
    st.header("🖼️ Thumbnail Ideas - AI")
    th_topic = st.text_input("Enter Video Topic", "What I Saw At Sea View?")
    if st.button("Generate Thumbnail Ideas"):
        st.write(call_gemini(f"For video topic '{th_topic}' give 5 viral thumbnail ideas. For each idea give: 1) Thumbnail text (3-4 words) 2) Which color to use 3) Face expression 4) Background. For Pakistani audience, high CTR."))

st.write("---")
st.write("Made With Love - RANKTUBE PRO | Ali Mahi")
