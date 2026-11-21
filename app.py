import streamlit as st
import requests

st.set_page_config(page_title="RANKTUBE PRO", page_icon="📈", layout="wide")
st.title("📈 RANKTUBE PRO - ASLI DATA WALA")
st.write("Ab Ye Naqli Nahi, Asli YouTube Data Dikhaega")

try:
    YOUTUBE_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    st.success("✅ Dono Keys Lag Gayi - Ab Asli Data Aayega")
except:
    st.error("❌ Keys Nahi Mili - Secrets Me Keys Daalo")
    YOUTUBE_KEY = ""
    GEMINI_KEY = ""

channel_id = st.text_input("🔍 Apne Channel Ka ID Ya Naam Likho", placeholder="Misaal: @AliMahiVlogs ya UCxxxx")

if st.button("Asli Data Lao"):
    if not YOUTUBE_KEY:
        st.warning("Pehle YouTube Key Secrets Me Daalo")
    elif not channel_id:
        st.warning("Pehle Channel ID Likho")
    else:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={YOUTUBE_KEY}"
        if channel_id.startswith("@"):
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_id}&type=channel&key={YOUTUBE_KEY}"
            r = requests.get(url).json()
            if "items" in r and len(r["items"]) > 0:
                real_id = r["items"][0]["snippet"]["channelId"]
                url2 = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={real_id}&key={YOUTUBE_KEY}"
                r = requests.get(url2).json()
            else:
                st.error("Channel Nahi Mila - Naam Sahi Likho")
                st.stop()
        else:
            r = requests.get(url).json()
        if "items" in r and len(r["items"]) > 0:
            data = r["items"][0]
            stats = data["statistics"]
            snip = data["snippet"]
            st.subheader(f"Channel: {snip['title']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Subs", stats.get("subscriberCount", "0"))
            c2.metric("Total Views", stats.get("viewCount", "0"))
            c3.metric("Total Videos", stats.get("videoCount", "0"))
            st.write(snip.get("description", "")[:300])
            st.success("Ye Asli Data Hai - YouTube Se Aaya Hai!")
        else:
            st.error("Channel Nahi Mila. Channel ID Sahi Likho.")

st.write("---")
topic = st.text_input("🔍 Topic Likho - AI Se Title Banwao", "Sea View")
if st.button("AI Se Title Banwao"):
    if not GEMINI_KEY:
        st.warning("Pehle Gemini Key Secrets Me Daalo")
    else:
        gem_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": f"Pakistani YouTube ke liye {topic} par 5 viral title banao, Urdu + English mix me, high CTR wale"}]}]}
        gr = requests.post(gem_url, json=payload).json()
        try:
            text = gr["candidates"][0]["content"]["parts"][0]["text"]
            st.success("AI Ne Ye Title Banaye:")
            st.write(text)
        except:
            st.error("Gemini Me Masla Hai")
            st.write(gr)

st.write("---")
st.write("Made With ❤️ - RANKTUBE PRO")
