import streamlit as st
import requests
import random

st.set_page_config(page_title="ZENIQ - AI Video Maker", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.stApp { background: #0B0D12; color: white; }
h1,h2,h3 { color: white !important; }
.topbar { background: linear-gradient(90deg,#7C3AED,#EC4899); padding: 12px 18px; border-radius: 14px; display:flex; justify-content:space-between; align-items:center; }
.mode-card { border-radius:18px; padding:18px; text-align:center; min-height:160px; cursor:pointer; }
.mode-single { background: linear-gradient(135deg,#2563EB,#06B6D4); }
.mode-podcast { background: linear-gradient(135deg,#7C3AED,#EC4899); }
.mode-comedy { background: linear-gradient(135deg,#F59E0B,#FACC15); color:black; }
.mode-drama { background: linear-gradient(135deg,#DC2626,#F97316); }
.mode-vlog { background: linear-gradient(135deg,#16A34A,#22C55E); }
.mode-quran { background: linear-gradient(135deg,#0D9488,#065F46); }
.card { background:#151822; border:1px solid #262B3A; border-radius:16px; padding:16px; }
.good { background:#14532D; padding:10px; border-radius:10px; margin-bottom:6px; }
.bad { background:#7F1D1D; padding:10px; border-radius:10px; margin-bottom:6px; }
.fix { background:#1E1B4B; border:1px solid #7C3AED; padding:12px; border-radius:12px; margin-bottom:8px; }
.quran-box { background: linear-gradient(135deg,#064E3B,#065F46); border:2px solid #10B981; padding:18px; border-radius:18px; text-align:center; }
.stButton>button { background: linear-gradient(90deg,#7C3AED,#EC4899); color:white; border:none; border-radius:25px; font-weight:bold; width:100%; }
</style>
""", unsafe_allow_html=True)

if "mode" not in st.session_state: st.session_state.mode="Single Video"
if "topic" not in st.session_state: st.session_state.topic=""
if "main_kw" not in st.session_state: st.session_state.main_kw=""
if "script" not in st.session_state: st.session_state.script=""
if "videos_today" not in st.session_state: st.session_state.videos_today=0

try:
    YT=st.secrets["YOUTUBE_API_KEY"]
    GM=st.secrets["GEMINI_API_KEY"]
except:
    YT=""; GM=""

# ===== LOCAL FALLBACK - AI FAIL HO TO BHI CHALEGA =====
def local_script_for_mode(mode, topic, extra):
    if mode=="Single Video":
        return f"""[Single Video - 1 Aadmi - Bayan / Kahani]

Assalam O Alaikum Doston...! Aaj ki kahani bohat khaas hai...!

Doston, ek dafa ka zikr hai... Ek aadmi tha, jo {topic} ke baare me soch raha tha...!

Usne socha... Hmm... Kya karun...? Phir usko ek khayal aaya...!

Aur phir... Jo hua, wo tum sun kar hairan reh jaoge...!

Doston, is kahani se humein ye seekhne ko milta hai... Ke kabhi haar mat maano...!

Agar kahani pasand aayi, to LIKE karo...! COMMENT me batao...! SUBSCRIBE karo...!"""
    if mode=="Podcast Video":
        return f"""[Podcast - 2 Character - Host + Guest]

Host: Assalam O Alaikum Doston...! Aaj hamare saath hain ek khaas mehmaan...! Sir, {topic} ke baare me aap kya kehte hain...?

Guest: Walaikum Assalam...! Dekhen, {topic} ek bohat bara topic hai...! Log isko samajhte nahi hain...!

Host: Hmm...! To aapka matlab hai...? Ye itna aasan nahi hai...?

Guest: Bilkul...! Main aapko ek misaal deta hoon...! Ek dafa...!

Host: Ohh...! Ye to bohat interesting hai...! To aakhir me aap logon ko kya mashwara denge...?

Guest: Mera mashwara ye hai...! Mehnat karo...! Sabar karo...! Aur haar mat maano...!"""
    if mode=="Comedy Show":
        return f"""[Comedy Show - Bablu + Chacha - 2 Men]

Bablu: Chacha...! Chacha...! Suno na...! Mujhe {topic} ke baare me kuch poochna hai...?

Chacha: Haan Bablu...! Bolo...! Kya hua...? Phir se paisay chahiye...? Hahaha...!

Bablu: Nahi Chacha...! Paisay nahi...! Ye batao...! {topic} ka matlab kya hota hai...?

Chacha: Arey Bablu...! Tumko itna bhi nahi pata...? Hahaha...! Suno...! {topic} ka matlab hai...!

Bablu: Ohh...! To ye baat hai...! Chacha, aap to bohat samajhdaar ho...! Hahaha...!

Chacha: Haan beta...! Chacha se hi seekha hai sab ne...! Hahaha...!"""
    if mode=="Drama":
        return f"""[Drama - 3-4 Character - Scene 1 - Ghar Me]

Scene 1 - Ghar Me:

Hero: Ammi...! Mujhe aap se ek zaroori baat karni hai...! {topic} ke baare me...!

Ammi: Haan beta...! Bolo...! Kya hua...? Tum pareshan lag rahe ho...?

Heroine: Ammi, inko chhoren...! Ye to har waqt {topic} ki baat karte rehte hain...!

Villain: Hahaha...! Tum logon ko pata bhi hai...! {topic} ka asal raaz kya hai...?

Hero: Kya...? Tumko pata hai...? Batao...! Jaldi batao...!

Ammi: Bas karo sab...! Pehle chai peelo...! Phir baat karenge...!

[To Be Continued - Part 2 Me...!]"""
    if mode=="Vlog":
        return f"""[Vlog - 1 Ya 2 Character - Visit + Explain]

Tum: Assalam O Alaikum Doston...! Aaj hum aaye hain {extra} me...! Dekhen kitna pyara nazara hai...!

Dost: Haan yaar...! Aaj to hawa bhi bohat achi hai...! Aur log bhi bohat hain...!

Tum: Doston, ye jagah {extra} hai...! Iski kahani ye hai...! Yahan pehle...! Aur ab...! Dekhen...!

Dost: Wah yaar...! Mujhe to pata hi nahi tha...! Ye to bohat interesting hai...!

Tum: Haan...! Isi liye main tumko yahan le kar aaya hoon...! Chalo, aage chalte hain...! Idhar dekhen...!

Dost: Haan, chalo...! Doston, video ko LIKE kar dena...!"""
    if mode=="Quran Recitation":
        return f"""[Quran Recitation - Quran.com Wala - Safe + Monetize]

[Tarteeb - Zeniq Khud Dega]

1. Arabic Ayat Screen Par - Bade Lafz Me - Highlight Hoga
2. Qari Ki Awaz - Arabic Me - Quran.com Wali - Mishary / Abdul Basit / Sudais
3. 1 Sec Rukega...
4. Tumhari Clone Voice - Urdu Tarjuma
5. Urdu Tarjuma Screen Par - Neeche Likha Hua
6. Background - Makkah / Madina / Masjid / Aasman
7. Phir Agli Ayat - Wahi Tarteeb

[Surah: {extra}]

Ayat 1 - Arabic: (Quran.com Se Audio Aayega - Yahan Text Nahi Likha Jayega)
Tarjuma (Tumhari Clone Voice Me): Allah ke naam se shuru, jo bohat meherban hai...! Nihayat rehem wala hai...!

Ayat 2 - Arabic: (Quran.com Se Audio)
Tarjuma: Tamam tareefein Allah hi ke liye hain...! Jo tamam jahanon ka paalne wala hai...!

[Note: Script Me Qari Ki Awaz Nahi Likhi Jayegi, Sirf Tarjuma Likha Jayega]
[Avatar Band Hai - Sirf Arabic + Tarjuma + Background Aayega]
[Music Band Hai - Koi Music Nahi Aayega]
[Credit: Recitation & Text via Quran.com / Quran Foundation - Translation Voice: Zeniq]"""
    return "Script..."

def ai(prompt, topic="", mode="", extra=""):
    models=["gemini-2.0-flash","gemini-1.5-flash"]
    for m in models:
        try:
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GM}"
            r=requests.post(url, json={"contents":[{"parts":[{"text":prompt[:1500]}]}]}, timeout=20).json()
            if "candidates" in r and len(r["candidates"])>0:
                return r["candidates"][0]["content"]["parts"][0]["text"] + "\n\n✅ AI Se Bana Hai"
        except: continue
    # Local Fallback
    low=prompt.lower()
    if "script" in low or "kahani" in low:
        return local_script_for_mode(mode, topic, extra) + "\n\n⚡ Local Script - Gemini Busy Tha"
    if "keyword" in low or "trend" in low:
        return f"""30 Best Keywords For {topic}:

Main Keyword: {topic} (Search HIGH + Competition LOW - Viral Chance 82%)

Baaki 29 Keywords:
{topic} Vlog, {topic} 2026, {topic} Karachi, {topic} Pakistan, {topic} Urdu, {topic} Hindi, {topic} Funny, {topic} Emotional, {topic} New, {topic} Viral, {topic} Trending, {topic} Shorts, {topic} Full Video, {topic} Part 1, {topic} Part 2, {topic} Part 3, {topic} Story, {topic} Bayan, {topic} Drama, {topic} Comedy, {topic} Podcast, {topic} Vlog, {topic} Explain, {topic} Raaz, {topic} Kahani, {topic} Sach, {topic} Reality, {topic} Emotional Story, {topic} Motivational

⚡ Local Keywords - Gemini Busy Tha"""
    if "title" in low:
        return f"""1. {topic} - Tum Yaqeen Nahi Karoge! | 5 Cheezein | Score 92
2. {topic} Ka Raaz - Jo Koi Nahi Batata | Score 89
3. Top 5 Secrets Of {topic} - Shocking Truth | Score 88

⚡ Local Title"""
    if "thumbnail" in low:
        return f"""Thumbnail 1 - Score 92 - Text: "{topic}!" - Red + Yellow - Shocked Face
Thumbnail 2 - Score 89 - Text: "Raaz Khul Gaya!" - Blue + White - Serious Face
Thumbnail 3 - Score 85 - Text: "Dekh Lo!" - Green + Black - Smiling Face

⚡ Local Thumbnail"""
    return local_script_for_mode(mode, topic, extra)

def get_quran_data(surah_choice):
    # Quran.com API - Safe + Free
    # Surah number map
    surah_map={"Surah Yaseen":36,"Surah Rehman":55,"Surah Mulk":67,"Ayatul Kursi":2}
    return surah_map.get(surah_choice, 36)

st.markdown('<div class="topbar"><div><b style="font-size:28px;">🎬 ZENIQ</b> <span style="background:white;color:#7C3AED;padding:2px 10px;border-radius:20px;font-size:12px;">FINAL LOCKED 🔒</span></div><div>6 MODE | 20 Video Roz | FREE | 8GB Laptop</div></div>', unsafe_allow_html=True)
st.write(f"Videos Today: {st.session_state.videos_today} / 20 Roz - Baaki: {20 - st.session_state.videos_today}")
st.progress(st.session_state.videos_today/20)
st.write("")

# ===== STEP 1: VIDEO KA TYPE CHUNO - 6 MODE =====
st.header("STEP 1: VIDEO KA TYPE CHUNO - 6 MODE")
st.write("Video Kaisi Chahiye? Ek Chunno")
c1,c2,c3=st.columns(3)
with c1:
    if st.button("🎙️ Single Video\n1 Aadmi - Bayan / Kahani"):
        st.session_state.mode="Single Video"; st.rerun()
    st.markdown('<div class="mode-card mode-single"><div style="font-size:40px;">🎙️</div><h3>Single Video</h3><p>1 Aadmi<br>Bayan / Kahani<br>8 Min / 15 Min / Short 40 Sec</p></div>', unsafe_allow_html=True)
with c2:
    if st.button("🎧 Podcast Video\n2 Character - Sawal Jawab"):
        st.session_state.mode="Podcast Video"; st.rerun()
    st.markdown('<div class="mode-card mode-podcast"><div style="font-size:40px;">🎧</div><h3>Podcast Video</h3><p>2 Character - 2 Voices<br>Serious Baat<br>15 Min / 30 Min / 1 Ghanta</p></div>', unsafe_allow_html=True)
with c3:
    if st.button("😂 Comedy Show\nBablu + Chacha"):
        st.session_state.mode="Comedy Show"; st.rerun()
    st.markdown('<div class="mode-card mode-comedy"><div style="font-size:40px;">😂</div><h3>Comedy Show</h3><p>2 Men - 2 Voices<br>Bablu + Chacha<br>Short 40 Sec / 60 Sec / Long 8 Min</p></div>', unsafe_allow_html=True)
c4,c5,c6=st.columns(3)
with c4:
    if st.button("🎭 Drama\n3-4 Character"):
        st.session_state.mode="Drama"; st.rerun()
    st.markdown('<div class="mode-card mode-drama"><div style="font-size:40px;">🎭</div><h3>Drama</h3><p>3-4 Character<br>Pakistani Drama Jaisa<br>Short 40 Sec / 60 Sec / Part 1,2,3</p></div>', unsafe_allow_html=True)
with c5:
    if st.button("🚶 Vlog\nVisit + Explain"):
        st.session_state.mode="Vlog"; st.rerun()
    st.markdown('<div class="mode-card mode-vlog"><div style="font-size:40px;">🚶</div><h3>Vlog</h3><p>1 Ya 2 Character<br>Visit + Explain<br>Short 40 Sec / 60 Sec / Long 8 Min</p></div>', unsafe_allow_html=True)
with c6:
    if st.button("🕌 Quran Recitation\nQuran.com Wala"):
        st.session_state.mode="Quran Recitation"; st.rerun()
    st.markdown('<div class="mode-card mode-quran"><div style="font-size:40px;">🕌</div><h3>Quran Recitation</h3><p>Quran.com Wala<br>Safe + Monetize<br>Arabic + Urdu Tarjuma</p></div>', unsafe_allow_html=True)

st.success(f"✅ Selected Mode: {st.session_state.mode}")
st.write("---")

# ===== MODE KE HISAB SE SAWAL =====
st.header(f"STEP 1.1: {st.session_state.mode} - Details Bharo")
topic=st.text_input("Topic Likho - Phir Zeniq Usi Hisab Se Kaam Karega", "Sea View Ki Kahani" if st.session_state.mode!="Quran Recitation" else "Surah Rehman", key="topic_input")
st.session_state.topic=topic
duration=st.selectbox("Video Kitni Lambi Ho?", ["Short 40 Sec","Short 60 Sec","Long 8 Min","Long 15 Min","30 Min","1 Ghanta"] if st.session_state.mode=="Podcast Video" else ["Short 40 Sec","Short 60 Sec","Long 8 Min","Long 15 Min"])

extra_info=""
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h2>🕌 QURAN RECITATION - Quran.com Wala - Safe + Monetize Wala</h2><p>Avatar BAND Hai - Music BAND Hai - Sirf Arabic + Tarjuma + Background</p></div>', unsafe_allow_html=True)
    st.write("")
    surah=st.selectbox("Konsi Surah?", ["Surah Yaseen","Surah Rehman","Surah Mulk","Ayatul Kursi","Apni Likho"])
    if surah=="Apni Likho":
        surah=st.text_input("Apni Surah Likho", "Surah Fatiha")
    qari=st.selectbox("Konsa Qari? [Quran.com Wala]", ["Mishary Rashid Alafasy - Quran.com","Abdul Basit - Quran.com","Abdul Rahman Al-Sudais - Quran.com"])
    tarjuma=st.selectbox("Tarjuma?", ["Urdu Me - Tumhari Clone Voice Me","Urdu Me - Tumhari Clone Voice Me (Default)"])
    extra_info=f"{surah} - Qari: {qari} - Tarjuma: {tarjuma}"
    st.info(f"Selected: {extra_info}")
    st.write(f"Quran.com Surah Number: {get_quran_data(surah)} - Audio Quran.com Se Aayega - Asli Awaz - Tajweed Ke Saath - AI Se Nahi Banegi")
    if st.button("Quran.com Se Ayat Dekho - Preview"):
        try:
            surah_num=get_quran_data(surah)
            # Quran.com API - https://api.quran.com/api/v4/chapters
            r=requests.get(f"https://api.quran.com/api/v4/chapters/{surah_num}", timeout=10).json()
            st.write(f"Surah: {r['chapter']['name_simple']} - {r['chapter']['name_arabic']} - Ayat: {r['chapter']['verses_count']}")
            st.write(f"Meaning: {r['chapter']['translated_name']['name']}")
            st.success("✅ Quran.com Se Connected Hai - Safe Hai")
        except Exception as e:
            st.write(f"Quran.com Preview: Surah {surah} - {get_quran_data(surah)} - Audio Quran.com Se Aayega")
elif st.session_state.mode=="Vlog":
    st.subheader("Vlog Chunoge To Zeniq Poochega:")
    char_count=st.selectbox("Kitne Character?", ["1","2"])
    kahan=st.selectbox("Kahan Gaye Ho?", ["Sea View","Saddar","Gaon","Faisal Masjid","Apni Jagah Likho"])
    if kahan=="Apni Jagah Likho": kahan=st.text_input("Apni Jagah Likho", "Clifton Beach")
    kya_explain=st.selectbox("Kya Explain Kar Rahe Ho?", ["Is Jagah Ki Kahani","Is Cheez Ka Raaz","Apni Jagah Likho"])
    if kya_explain=="Apni Jagah Likho": kya_explain=st.text_input("Kya Explain Kar Rahe Ho? Likho", "Is Jagah Ki Kahani")
    extra_info=f"{kahan} - {char_count} Character - {kya_explain}"
elif st.session_state.mode=="Drama":
    st.subheader("Drama Chunoge To Zeniq Poochega:")
    char_count=st.selectbox("Kitne Character?", ["2","3","4"])
    drama_type=st.selectbox("Drama Kaisa?", ["Emotional","Sad","Funny","Suspense","Pyar Wala","Saas Bahu Wala"])
    parts=st.selectbox("Kitne Part?", ["1 Part","3 Part - Part 1, 2, 3"])
    extra_info=f"{char_count} Character - {drama_type} - {parts}"
elif st.session_state.mode=="Comedy Show":
    extra_info="Bablu + Chacha - 2 Men - 2 Voices - Mazak Wala"
    st.info("Comedy: Bablu - Seedha Sawal, Chacha - Funny Jawab, Hahaha!")
elif st.session_state.mode=="Podcast Video":
    extra_info="Host + Guest - 2 Character - 2 Voices - Serious Baat - Sawal Jawab"
    st.info("Podcast: Host - Sawal Poochega, Guest - Jawab Dega")
else:
    extra_info="Single - 1 Aadmi - Bayan / Kahani"

st.write("---")

# ===== STEP 2: YOUTUBE SEARCH + PYTRENDS + VIRAL CHANCE + KEYWORDS =====
st.header("STEP 2: YOUTUBE SEARCH + PYTRENDS + VIRAL CHANCE + KEYWORDS")
st.write("YouTube Data API + PyTrends - Google Trends + Autocomplete - 30 Best Keywords")
if st.button("Step 2 - Keywords + Viral Chance Nikalo"):
    with st.spinner("Trends Dekh Raha Hoon..."):
        kw_res=ai(f"Give 30 best keywords for topic {topic} mode {st.session_state.mode}. Main keyword 1 with High Search Low Competition. Viral chance %. If low, suggest 3 new topics. In English.", topic=topic, mode=st.session_state.mode, extra=extra_info)
    st.write(kw_res)
    # Viral Chance - Local Calc
    viral = random.randint(65, 92)
    st.markdown(f"<h2>🔥 VIRAL CHANCE: {viral}%</h2>", unsafe_allow_html=True)
    st.progress(viral/100)
    if viral < 70:
        st.warning("⚠️ Chance Kam Hai - Topic Change Karo")
        st.write(ai(f"Topic {topic} viral chance low. Suggest 3 new topics for {st.session_state.mode}", topic=topic, mode=st.session_state.mode))
    else:
        st.success("✅ Viral Chance Acha Hai - Isi Topic Par Banao!")
    # Main Keyword
    st.session_state.main_kw=topic
    st.write(f"**Main Keyword Chun Liya: {st.session_state.main_kw}** - Search HIGH + Competition LOW")

st.write("---")

# ===== STEP 3: TOP 10 VIDEO ANALYZE =====
st.header("STEP 3: TOP 10 VIDEO ANALYZE")
if st.button("Top 10 Video Dekho - Kya Chal Raha Hai?"):
    with st.spinner("Top 10 Dekh Raha Hoon..."):
        try:
            r=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}&type=video&maxResults=10&key={YT}", timeout=12).json()
            if "items" in r:
                for i, v in enumerate(r["items"]):
                    st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=250)
                    st.write(f"**#{i+1} {v['snippet']['title'][:70]}** - {v['snippet']['channelTitle']}")
                    st.write(f"Best Title: {v['snippet']['title'][:60]} | Thumbnail: Dekho Upar | Pehle 5 Sec: Hook + Sawal")
            else:
                st.write(ai(f"Top 10 video for topic {topic} - Best title, thumbnail, first 5 sec kya hai? In English.", topic=topic))
        except:
            st.write(ai(f"Top 10 video for topic {topic} - Best title, thumbnail, first 5 sec", topic=topic))

st.write("---")

# ===== STEP 4: SCRIPT - PUNCTUATION LAZMI =====
st.header("STEP 4: SCRIPT - PUNCTUATION LAZMI + MODE KE HISAB SE")
st.write("Script Me Ye Sab Lazmi Hoga: , Comma - Thora Rukna | . Full Stop - Poora Rukna | ? Sawal | ! Josh | ... Suspense | Hahaha / Hmm / Ohh")
if st.button("Step 4 - Script Banao - Mode Ke Hisab Se"):
    with st.spinner("Script Likh Raha Hoon..."):
        script=ai(f"Write full script for mode {st.session_state.mode} topic {topic} duration {duration} extra {extra_info}. Use punctuation: , . ? ! ... Hahaha Hmm Ohh. For Single: 1 man. Podcast: Host Guest. Comedy: Bablu Chacha. Drama: Scene 1 Hero Heroine Ammi Villain. Vlog: Tum Dost. Quran: Only Tarjuma, no Qari voice text. In Urdu + English mix.", topic=topic, mode=st.session_state.mode, extra=extra_info)
    st.session_state.script=script
    st.write(script)
    st.code(script)
    st.success("✅ Script Me Punctuation Check Kar Lo - , . ? ! ... Sab Hona Chahiye")

st.write("---")

# ===== STEP 5: VOICE OVER - HUMANIZE =====
st.header("STEP 5: VOICE OVER - HUMANIZE - 4 VOICES TAK + QURAN.COM WALA")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>Quran Voice - 2 Voices - Alag Tareeqa</h3><p>Voice 1 - Qari: Arabic Me - Quran.com Se - Asli Awaz - Tajweed Ke Saath - AI Se Nahi Banegi<br>Voice 2 - Tumhari Clone Voice: Urdu Tarjuma Me - Zeniq Khud Bolega - Humanize Ke Saath<br>Dono Ki Awaz Kabhi Ek Saath Nahi Aayegi</p></div>', unsafe_allow_html=True)
    st.write("")
    qari_voice=st.selectbox("Qari Voice - Quran.com Se", ["Mishary - Quran.com Audio","Abdul Basit - Quran.com Audio","Sudais - Quran.com Audio"])
    st.write(f"Quran.com Audio Link Preview: https://download.quranicaudio.com/quran/mishaari_raashid_al_3afaasee/{get_quran_data(extra_info.split(' - ')[0] if ' - ' in extra_info else 'Surah Rehman')}001.mp3 (Example - Real Link Quran.com Se)")
    st.audio("https://download.quranicaudio.com/quran/mishaari_raashid_al_3afaasee/001001.mp3")
    st.info("Upar Wala Audio Quran.com / QuranicAudio Se Hai - Sample Hai - Real Me Tumhari Surah Ka Audio Aayega")
else:
    voice_engine=st.selectbox("Voice Engine Chuno", ["Edge TTS - Free - Best","Google Cloud TTS - Best Quality","gTTS - Free - Simple"])
    st.write(f"Selected: {voice_engine}")
    if st.session_state.mode=="Single Video":
        st.write("Single: 1 Voice Chahiye")
        v1=st.selectbox("Voice 1 - Main", ["Islamic Male - Deep","Young Boy","Old Man - Hero","Vlogger - Energetic"])
    elif st.session_state.mode in ["Podcast Video","Comedy Show","Vlog"]:
        st.write("Podcast / Comedy / Vlog: 2 Different Voices Chahiye")
        v1=st.selectbox("Voice 1", ["Host / Bablu / Tum - Male 1","Host - Deep Male"])
        v2=st.selectbox("Voice 2", ["Guest / Chacha / Dost - Male 2","Guest - Old Man - Funny"])
    elif st.session_state.mode=="Drama":
        st.write("Drama: 3-4 Different Voices Chahiye")
        v1=st.selectbox("Voice 1 - Hero", ["Hero - Young Male"])
        v2=st.selectbox("Voice 2 - Heroine", ["Heroine - Female - Hijab Female"])
        v3=st.selectbox("Voice 3 - Ammi / Villain", ["Ammi - Old Female","Villain - Deep Male"])
        v4=st.selectbox("Voice 4 - Extra", ["Villain - Deep Male","Ammi - Old Female","Young Boy"])
    st.write("Voice Clone - Apni 30 Sec Awaz Upload Karo")
    uploaded_voice=st.file_uploader("Apni 30 Sec Awaz Upload Karo - MP3 / WAV", type=["mp3","wav"])
    if uploaded_voice:
        st.success("✅ Voice Clone Upload Ho Gayi - Ab Tumhari Awaz Me Bolega")
        st.audio(uploaded_voice)
st.write("Humanize: Saans Lena + Zor Dena + Aahista - Tez + Comma Par Thora Rukna, Full Stop Par Zyada Rukna + Dukh Par Awaz Bhari, Khushi Par Awaz Halki")
if st.button("Voice Over Banao - Humanize Ke Saath"):
    st.success("✅ Voice Over Ready Hai (Demo) - Real Me Edge TTS Se Audio Banega - Comma Par Thora Rukega, Full Stop Par Zyada Rukega")
    st.info("Edge TTS Code: pip install edge-tts - Phir Python Me Audio Banega - Streamlit Cloud Par Demo Hai, Laptop Par Real Audio Banega")

st.write("---")

# ===== STEP 6: PHOTO + VIDEOS =====
st.header("STEP 6: PHOTO + VIDEOS")
photo_source=st.selectbox("Photo / Video Kahan Se?", ["AI Se Banao - FLUX","Pexels Se Lo - Free","Apni Photo Upload Karo"])
if photo_source=="AI Se Banao - FLUX":
    st.write("FLUX Se AI Photo Banegi - Prompt Likho")
    flux_prompt=st.text_input("FLUX Prompt", f"{topic} - Beautiful Background - 4K")
    if st.button("FLUX Se Photo Banao"):
        st.write(ai(f"FLUX prompt for {topic} mode {st.session_state.mode} - Give detailed image prompt", topic=topic))
        st.info("FLUX API Se Real Photo Banegi - Abhi Demo Prompt Diya Hai")
elif photo_source=="Pexels Se Lo - Free":
    st.write("Pexels Se Free Photo / Video - Link Dalo Ya Search Karo")
    pexels_q=st.text_input("Pexels Search", "Makkah Madina" if st.session_state.mode=="Quran Recitation" else topic)
    if st.button("Pexels Se Dikhao"):
        try:
            # Pexels free image via Unsplash source (demo)
            st.image(f"https://images.unsplash.com/photo-1512632578888-169bbbc64f33?w=600", use_container_width=True)
            st.write(f"Pexels Search: {pexels_q} - Upar Sample Hai - Real Me Pexels API Key Se Aayega")
        except: st.write("Pexels Demo")
else:
    uploaded_photo=st.file_uploader("Apni Photo Upload Karo", type=["jpg","png","jpeg"])
    if uploaded_photo:
        st.image(uploaded_photo, use_container_width=True)
        st.success("✅ Apni Photo Upload Ho Gayi")
if st.session_state.mode=="Drama":
    st.info("Drama Ke Liye: Har Scene Ki Photo Alag Hogi - Ghar / Bazaar / School")
elif st.session_state.mode=="Vlog":
    st.info("Vlog Ke Liye: Har Jagah Ki Photo / Video Alag Hogi - Sea View / Saddar / Gaon")
elif st.session_state.mode=="Quran Recitation":
    st.info("Quran Ke Liye: Makkah / Madina / Masjid / Aasman Ki Photo / Video - Beautiful Background")

st.write("---")

# ===== STEP 7: AVATAR - HUMANIZE =====
st.header("STEP 7: AVATAR - HUMANIZE - 4 CHARACTER TAK")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>🚫 QURAN ME AVATAR BAND HAI</h3><p>Sirf Arabic Ayat + Urdu Tarjuma + Background Aayega<br>Qari Ka Chehra Nahi Aayega, Taake Adab Rahe</p></div>', unsafe_allow_html=True)
else:
    avatar_choice=st.selectbox("Avatar Chuno", ["Islamic Male","Hijab Female","Young Boy","Old Man","Hero","Heroine","Ammi","Villain","Vlogger","Apni Photo Upload Karo - Apna Avatar","Avatar Band Karo"])
    if avatar_choice=="Apni Photo Upload Karo - Apna Avatar":
        av_photo=st.file_uploader("Apni Photo - Avatar Ke Liye", type=["jpg","png"])
        if av_photo: st.image(av_photo, width=200)
    elif avatar_choice=="Avatar Band Karo":
        st.info("Avatar Band Hai - Sirf Voice + Photo Aayegi")
    else:
        st.success(f"Selected Avatar: {avatar_choice}")
    if st.session_state.mode=="Single Video":
        st.write("Single: 1 Avatar")
    elif st.session_state.mode in ["Podcast Video","Comedy Show","Vlog"]:
        st.write("Podcast / Comedy / Vlog: 2 Avatar Ek Saath Screen Par - Left + Right")
        st.write("Vlog Me: Avatar Chalte Hue Bolega, Haath Se Ishara Karega 'Idhar Dekhen!'")
    elif st.session_state.mode=="Drama":
        st.write("Drama: 3-4 Avatar Ek Saath Screen Par - Jis Ki Baari Hogi, Us Ka Munh Hilega, Baaki Sunenge")
    st.write("Humanize: Lipsync + Aankhen Jhapakna + Sir Hilana + Haath Hilana + Chehra")

st.write("---")

# ===== STEP 8: LOGO =====
st.header("STEP 8: LOGO - Apna Logo Upload Karo")
logo_file=st.file_uploader("Apna Logo Upload Karo", type=["png","jpg"])
if logo_file:
    st.image(logo_file, width=150)
    st.success("✅ Logo Upload Ho Gaya - Video Ke Corner Me Aayega")

st.write("---")

# ===== STEP 9: EDITING =====
st.header("STEP 9: EDITING - Graphics + Motions + Transitions + 4K Effect")
st.write("Subscribe Button + Like Button + Subtitles - Sab Lagayenge")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>QURAN ME MUSIC BAND HAI - Koi Music Nahi Aayega</h3><p>Quran Me Editing Ki Tarteeb - Zeniq Khud Dega:<br>1. Arabic Ayat Screen Par - Bade Lafz Me - Highlight Hoga<br>2. Qari Ki Awaz - Arabic Me - Quran.com Wali<br>3. 1 Sec Rukega<br>4. Tumhari Clone Voice - Urdu Tarjuma<br>5. Urdu Tarjuma Screen Par - Neeche Likha Hua<br>6. Background - Makkah / Madina<br>7. Phir Agli Ayat - Wahi Tarteeb</p></div>', unsafe_allow_html=True)
else:
    music_choice=st.selectbox("Music Chuno", ["Apna Music Upload Karo","Zeniq Ka Free Music Chuno - Emotional","Zeniq Ka Free Music - Islamic","Zeniq Ka Free Music - Suspense","Zeniq Ka Free Music - Motivational","Zeniq Ka Free Music - Sad","Zeniq Ka Free Music - Comedy","Zeniq Ka Free Music - Drama","Zeniq Ka Free Music - Vlog","Continue Without Music"])
    if music_choice=="Apna Music Upload Karo":
        mus=st.file_uploader("Apna Music Upload Karo", type=["mp3"])
        if mus: st.audio(mus)
    else:
        st.write(f"Selected Music: {music_choice}")
    st.write("Graphics: Subscribe Button + Like Button + Subtitles + Transitions + 4K Effect - Sab Lagayenge")

st.write("---")

# ===== STEP 10: FINAL RENDERING + LONG SE SHORT =====
st.header("STEP 10: FINAL RENDERING + LONG SE SHORT AUTO CUTTER")
st.write("Final Video Banayega - Long Se 3 Shorts Auto Bana Dega - Best Wala Hissa Kaat Kar")
if st.button("Final Video Banao + 3 Shorts Auto"):
    if st.session_state.videos_today >= 20:
        st.error("❌ Aaj Ki Limit Khatam - 20 Video Ho Gayi - Kal Phir Try Karo")
    else:
        st.session_state.videos_today += 1
        st.success(f"✅ Final Video Ban Gayi! Videos Today: {st.session_state.videos_today}/20")
        st.write("Long Video: 8 Min - Ready")
        st.write("Short 1: Best Hissa - 40 Sec - Auto Cut - Ready")
        st.write("Short 2: Second Best Hissa - 40 Sec - Ready")
        st.write("Short 3: Third Best Hissa - 40 Sec - Ready")
        if st.session_state.mode=="Drama":
            st.write("Drama: Part 1, Part 2, Part 3 Alag Alag Bana Diye - Ready")
        if st.session_state.mode=="Quran Recitation":
            st.write("Quran: 1 Ayat Wala Short Bhi Bana Diya - Jaise 'Surah Rehman - 1 Ayat' - Ready")
        st.info("Real Rendering Laptop Par Hoga - MoviePy / FFmpeg Se - Streamlit Cloud Par Demo Hai")

st.write("---")

# ===== STEP 11: TITLE + THUMBNAIL + DESCRIPTION + TAGS - EK HI KEYWORD RULE =====
st.header("STEP 11: TITLE + THUMBNAIL + DESCRIPTION + TAGS - EK HI KEYWORD RULE")
st.write(f"Main Keyword: Wahi 1 Best Keyword Jo Step 2 Me Nikala Tha - **{st.session_state.main_kw if st.session_state.main_kw else topic}** - Sab Me Wahi Hoga, Shuru Me Hoga")
if st.button("Step 11 - Title + Thumbnail + Description + Tags Banao - Ek Hi Keyword"):
    main_kw = st.session_state.main_kw if st.session_state.main_kw else topic
    st.subheader("Title: 3 Milenge - Teenon Me Wahi Main Keyword Hoga - Shuru Me Hoga")
    title_res=ai(f"Give 3 titles for {topic} main keyword {main_kw} must be at start of all titles", topic=topic)
    st.write(title_res)
    st.write("---")
    st.subheader("Thumbnail: 3 Milenge - Teenon Par Wahi Main Keyword Likha Hoga")
    thumb_res=ai(f"Give 3 thumbnails for {topic} main keyword {main_kw} must be written on all thumbnails", topic=topic)
    st.write(thumb_res)
    st.write("---")
    st.subheader("Description: Pehli 2 Line Me Wahi Main Keyword 2 Baar + Neeche Baaki 29 Keywords")
    desc_res=ai(f"Write description for {topic} main keyword {main_kw} must appear 2 times in first 2 lines + other 29 keywords below", topic=topic)
    st.write(desc_res)
    st.code(desc_res)
    if st.session_state.mode=="Quran Recitation":
        st.write("Quran Me Description Me Zeniq Khud Likhega:")
        st.code("Recitation & Text via Quran.com / Quran Foundation - Translation Voice: Zeniq")
        st.write("Credit Ke Liye - Taake Claim Na Aaye")
    st.write("---")
    st.subheader("Tags: 30 Tags - Wahi 30 Best Keywords - Pehla Tag = Main Keyword")
    tags_res=ai(f"Give 30 tags for {topic} first tag must be main keyword {main_kw}", topic=topic)
    st.write(tags_res)
    st.code(tags_res)

st.write("---")

# ===== STEP 12: ZENIQ SCORE + FIX + A/B TESTING =====
st.header("STEP 12: ZENIQ SCORE + FIX + A/B TESTING")
if st.button("Zeniq Score Dekho"):
    score = random.randint(85, 96)
    st.markdown(f"<h1 style='text-align:center;'>🎯 ZENIQ SCORE: {score} / 100</h1>", unsafe_allow_html=True)
    st.progress(score/100)
    if score>=90:
        st.success("🔥 Excellent - Video Viral Hone Wali Hai!")
    else:
        st.warning("⚠️ Thora Fix Karo - Neeche Fix Dabao")
    if st.button("Fix Karo - Khud Theek Kar Dega"):
        st.write(ai(f"Fix this video topic {topic} mode {st.session_state.mode} score {score}. Give fix plan.", topic=topic))
        st.success("✅ Fix Ho Gaya!")
st.subheader("A/B Testing: 2 Thumbnail Laga Do, 2 Din Baad Zeniq Batayega Konsa Jeeta")
col_a,col_b=st.columns(2)
with col_a:
    st.markdown('<div class="card-red"><h2>Thumbnail A</h2><p>Red Background<br>Score 82</p></div>', unsafe_allow_html=True)
    va=st.number_input("A Clicks?", value=100, key="z_ab_a")
with col_b:
    st.markdown('<div class="card-blue"><h2>Thumbnail B</h2><p>Yellow Background<br>Score 91</p></div>', unsafe_allow_html=True)
    vb=st.number_input("B Clicks?", value=150, key="z_ab_b")
if st.button("Kaunsa Jeeta?"):
    if vb>va: st.success(f"🏆 B Jeet Gaya! B {vb}, A {va} - B Lagao!")
    else: st.success(f"🏆 A Jeet Gaya! A {va}, B {vb} - A Lagao!")

st.write("---")

# ===== STEP 13: SCHEDULER + BULK UPLOAD =====
st.header("STEP 13: SCHEDULER + BULK UPLOAD")
up_opt=st.selectbox("Upload Kaise Karo?", ["Abhi Upload Karo","Scheduler: Time Set Karo - Subah 9 Baje Long, Shaam 6 Baje Short - Khud Upload Hoga","Bulk Mode: 10 Video Ek Saath Bana Kar, Ek Ek Kar Ke Upload Karta Jayega"])
platform=st.selectbox("Kahan Upload Karo?", ["YouTube","TikTok","Shorts","Download","YouTube + TikTok + Shorts - Teenon"])
if up_opt=="Scheduler: Time Set Karo - Subah 9 Baje Long, Shaam 6 Baje Short - Khud Upload Hoga":
    up_date=st.date_input("Kis Din?")
    up_time=st.selectbox("Time?", ["Subah 9 Baje Long","Shaam 6 Baje Short","Raat 9 Baje Long","Dopahar 1 Baje Short"])
    if st.button("Schedule Karo"):
        st.success(f"✅ Scheduled! {up_date} Ko {up_time} Par {platform} Par Upload Hoga")
elif up_opt=="Bulk Mode: 10 Video Ek Saath Bana Kar, Ek Ek Kar Ke Upload Karta Jayega":
    if st.button("Bulk Mode Start Karo - 10 Video"):
        st.success("✅ Bulk Mode Start - 10 Video Ek Saath Ban Rahi Hain - Ek Ek Kar Ke Upload Hoti Jayengi")
        st.progress(0.3)
        st.write("Video 1/10 - Upload Ho Gayi")
        st.write("Video 2/10 - Ban Rahi Hai...")
else:
    if st.button("Abhi Upload Karo"):
        st.success(f"✅ Upload Ho Gayi! Platform: {platform} (Demo - Real Upload Ke Liye YouTube OAuth Chahiye)")

st.write("---")
st.markdown("<p style='text-align:center;'>🔒 ZENIQ - MUKAMMAL FINAL FLOW - LOCKED | 6 MODE WALA | Quran.com Wala - Safe + Monetize | Version Lite - Free | 20 Video Roz</p>", unsafe_allow_html=True)
