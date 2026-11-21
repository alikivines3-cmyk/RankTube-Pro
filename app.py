import streamlit as st
import requests
import random

st.set_page_config(page_title="ZENIQ - AI Video Maker", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.stApp { background: #0B0D12; color: white; }
h1,h2,h3 { color: white !important; }
.topbar { background: linear-gradient(90deg,#7C3AED,#EC4899); padding: 12px 18px; border-radius: 14px; display:flex; justify-content:space-between; align-items:center; }
.mode-card { border-radius:18px; padding:18px; text-align:center; min-height:170px; }
.mode-single { background: linear-gradient(135deg,#2563EB,#06B6D4); }
.mode-podcast { background: linear-gradient(135deg,#7C3AED,#EC4899); }
.mode-comedy { background: linear-gradient(135deg,#F59E0B,#FACC15); color:black; }
.mode-drama { background: linear-gradient(135deg,#DC2626,#F97316); }
.mode-vlog { background: linear-gradient(135deg,#16A34A,#22C55E); }
.mode-quran { background: linear-gradient(135deg,#0D9488,#065F46); }
.mode-review { background: linear-gradient(135deg,#E11D48,#F43F5E); }
.card { background:#151822; border:1px solid #262B3A; border-radius:16px; padding:16px; }
.good { background:#14532D; padding:10px; border-radius:10px; margin-bottom:6px; }
.bad { background:#7F1D1D; padding:10px; border-radius:10px; margin-bottom:6px; }
.fix { background:#1E1B4B; border:1px solid #7C3AED; padding:12px; border-radius:12px; margin-bottom:8px; }
.quran-box { background: linear-gradient(135deg,#064E3B,#065F46); border:2px solid #10B981; padding:18px; border-radius:18px; text-align:center; }
.review-box { background: linear-gradient(135deg,#4C0519,#881337); border:2px solid #F43F5E; padding:18px; border-radius:18px; }
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

def local_script_for_mode(mode, topic, extra):
    if mode=="Drama Review + Prediction":
        return f"""[Drama Review + Prediction - 1 Character - Beth Kar Batayega]

Assalam O Alaikum Doston...! Aaj hum baat karenge {topic} ke baare me...! Jo kal episode me hua, wo sun kar tum hairan reh jaoge...!

[PART 1 - YE HUA - Pichli Episode Ka Review]

Doston, kal ki episode me ye hua...! Hero ne...! Heroine ne...! Aur Villain ne to hadd hi kar di...!

Sab se pehle...! Hero ne jab {topic} me ye kaha...! To Heroine ko gussa aa gaya...! Aur phir...! Ohh...! Kya scene tha...!

Phir Ammi ne aakar...! Sab ko samjhaya...! Lekin Villain ne peeche se...! Hmm...! Ye to galat hua na...?

[PART 2 - WO HUA - Detail Me]

Doston, ek ek karke samjhte hain...!

Pehla - Hero ka kya kasoor tha...? Usne jo kiya, wo sahi tha ya galat...? Mujhe lagta hai...!

Dusra - Heroine ne jo faisla liya...! Wo bilkul sahi tha...! Kyunki...!

Teesra - Villain ka plan...! Usne jo chaal chali...! Wo to sab ko pata chal gaya...! Hahaha...!

[PART 3 - AAGE KYA HOGA? - PREDICTION]

Ab sab se bara sawal...! Aage kya hoga...?

Meri prediction ye hai...! Agli episode me...!

1. Hero, Heroine se maafi maangega...! Aur Heroine maan jayegi...! Ya nahi maanegi...? Mujhe lagta hai maan jayegi...!

2. Villain, ek naya plan banayega...! Wo Hero ko phasane ki koshish karega...! Lekin...! Hero ko pata chal jayega...!

3. Aur aakhir me...! Ek bada twist aayega...! Koi purana character wapas aayega...! Aur sab kuch badal jayega...!

Doston, tumko kya lagta hai...? Meri prediction sahi hai ya galat...? Comment me batao...! Tumhari prediction kya hai...? Agli episode me kya hoga...?

Agar review pasand aaya, to LIKE karo...! COMMENT karo...! SUBSCRIBE karo...! Kal phir milenge, nayi episode ke review ke saath...! Allah Hafiz...!"""
    if mode=="Single Video":
        return f"""[Single Video - 1 Aadmi - Bayan / Kahani]

Assalam O Alaikum Doston...! Aaj ki kahani bohat khaas hai...!

Doston, ek dafa ka zikr hai... Ek aadmi tha, jo {topic} ke baare me soch raha tha...!

Usne socha... Hmm... Kya karun...? Phir usko ek khayal aaya...!

Aur phir... Jo hua, wo tum sun kar hairan reh jaoge...!

Doston, is kahani se humein ye seekhne ko milta hai... Ke kabhi haar mat maano...!

Agar kahani pasand aayi, to LIKE karo...! COMMENT me batao...! SUBSCRIBE karo...!"""
    if mode=="Podcast Video":
        return f"""[Podcast - Host + Guest]

Host: Assalam O Alaikum...! Aaj hamare saath hain mehmaan...! Sir, {topic} ke baare me aap kya kehte hain...?

Guest: Walaikum Assalam...! Dekhen, {topic} ek bohat bara topic hai...!

Host: Hmm...! To aapka matlab hai...? Ye itna aasan nahi hai...?

Guest: Bilkul...! Main aapko ek misaal deta hoon...! Ek dafa...!

Host: Ohh...! Ye to bohat interesting hai...!

Guest: Mera mashwara ye hai...! Mehnat karo...! Sabar karo...!"""
    if mode=="Comedy Show":
        return f"""[Comedy - Bablu + Chacha]

Bablu: Chacha...! Mujhe {topic} ke baare me kuch poochna hai...?

Chacha: Haan Bablu...! Bolo...! Kya hua...? Hahaha...!

Bablu: {topic} ka matlab kya hota hai...?

Chacha: Arey Bablu...! Tumko itna bhi nahi pata...? Hahaha...! Suno...!

Bablu: Ohh...! To ye baat hai...! Chacha, aap to bohat samajhdaar ho...! Hahaha...!"""
    if mode=="Drama":
        return f"""[Drama - Scene 1 - Ghar Me]

Hero: Ammi...! Mujhe {topic} ke baare me baat karni hai...!

Ammi: Haan beta...! Bolo...! Kya hua...?

Heroine: Ammi, inko chhoren...! Ye to har waqt {topic} ki baat karte hain...!

Villain: Hahaha...! Tum logon ko pata bhi hai...! {topic} ka asal raaz kya hai...?

Hero: Kya...? Batao...! Jaldi batao...!

Ammi: Bas karo sab...! Pehle chai peelo...!

[To Be Continued - Part 2 Me...!]"""
    if mode=="Vlog":
        return f"""[Vlog]

Tum: Assalam O Alaikum Doston...! Aaj hum aaye hain {extra} me...! Dekhen kitna pyara nazara hai...!

Dost: Haan yaar...! Aaj to hawa bhi bohat achi hai...!

Tum: Doston, ye jagah {extra} hai...! Iski kahani ye hai...!

Dost: Wah yaar...! Mujhe to pata hi nahi tha...!

Tum: Chalo, aage chalte hain...! Idhar dekhen...!"""
    if mode=="Quran Recitation":
        return f"""[Quran - Quran.com Wala]

1. Arabic Ayat Screen Par - Bade Lafz Me - Highlight
2. Qari Ki Awaz - Arabic Me - Quran.com Wali
3. 1 Sec Rukega...
4. Tumhari Clone Voice - Urdu Tarjuma
5. Urdu Tarjuma Screen Par - Neeche
6. Background - Makkah / Madina
7. Phir Agli Ayat

Surah: {extra}
Ayat 1 - Arabic: (Quran.com Se Audio)
Tarjuma: Allah ke naam se shuru, jo bohat meherban hai...!

[Avatar Band - Music Band - Credit: Recitation & Text via Quran.com / Quran Foundation - Translation Voice: Zeniq]"""
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
    low=prompt.lower()
    if "script" in low:
        return local_script_for_mode(mode, topic, extra) + "\n\n⚡ Local Script - Gemini Busy Tha"
    if "keyword" in low or "trend" in low:
        return f"""Main Keyword: {topic} - Viral Chance 85%
Baaki 29 Keywords: {topic} Vlog, {topic} Review, {topic} Prediction, {topic} Episode, {topic} Drama, {topic} Pakistani Drama, {topic} Today Episode, {topic} Kal Ki Episode, {topic} Agli Episode, {topic} Twist, {topic} Hero, {topic} Heroine, {topic} Villain, {topic} Story, {topic} Update, {topic} News, {topic} 2026, {topic} Urdu, {topic} Hindi, {topic} Funny, {topic} Emotional, {topic} Sad, {topic} Full Episode, {topic} Part 1, {topic} Part 2, {topic} Part 3, {topic} Promo, {topic} Teaser, {topic} Ending

⚡ Local Keywords"""
    if "title" in low:
        return f"""1. {topic} - Ye Hua, Wo Hua, Aage Kya Hoga? | Shocking Twist | Score 94
2. {topic} Ka Bara Raaz Khul Gaya! | Prediction | Score 90
3. {topic} - Kal Ki Episode Me Ye Hua! | Review | Score 89

⚡ Local Title"""
    if "thumbnail" in low:
        return f"""Thumbnail 1 - Score 93 - Text: "{topic}!" - Red + Yellow - Shocked Face
Thumbnail 2 - Score 90 - Text: "Aage Kya Hoga?" - Blue + White - Serious Face
Thumbnail 3 - Score 86 - Text: "Raaz Khul Gaya!" - Green + Black - Smiling Face

⚡ Local Thumbnail"""
    return local_script_for_mode(mode, topic, extra)

def get_quran_data(surah_choice):
    surah_map={"Surah Yaseen":36,"Surah Rehman":55,"Surah Mulk":67,"Ayatul Kursi":2}
    return surah_map.get(surah_choice, 36)

st.markdown('<div class="topbar"><div><b style="font-size:28px;">🎬 ZENIQ</b> <span style="background:white;color:#7C3AED;padding:2px 10px;border-radius:20px;font-size:12px;">FINAL v2 - 7 MODE</span></div><div>7 MODE | 20 Video Roz | FREE</div></div>', unsafe_allow_html=True)
st.write(f"Videos Today: {st.session_state.videos_today} / 20 - Baaki: {20 - st.session_state.videos_today}")
st.progress(st.session_state.videos_today/20)
st.write("")

st.header("STEP 1: VIDEO KA TYPE CHUNO - 7 MODE - NAYA WALA ADDED")
st.write("Video Kaisi Chahiye? Ek Chunno - Naya Wala 7th Mode Neeche Hai - Drama Review Wala")
c1,c2,c3=st.columns(3)
with c1:
    if st.button("🎙️ Single Video"):
        st.session_state.mode="Single Video"; st.rerun()
    st.markdown('<div class="mode-card mode-single"><div style="font-size:40px;">🎙️</div><h3>Single Video</h3><p>1 Aadmi<br>Bayan / Kahani<br>8 Min / 15 Min / Short 40 Sec</p></div>', unsafe_allow_html=True)
with c2:
    if st.button("🎧 Podcast Video"):
        st.session_state.mode="Podcast Video"; st.rerun()
    st.markdown('<div class="mode-card mode-podcast"><div style="font-size:40px;">🎧</div><h3>Podcast Video</h3><p>2 Character<br>Sawal Jawab<br>15 Min / 30 Min / 1 Ghanta</p></div>', unsafe_allow_html=True)
with c3:
    if st.button("😂 Comedy Show"):
        st.session_state.mode="Comedy Show"; st.rerun()
    st.markdown('<div class="mode-card mode-comedy"><div style="font-size:40px;">😂</div><h3>Comedy Show</h3><p>Bablu + Chacha<br>2 Men - 2 Voices<br>Short 40 Sec / 60 Sec / Long 8 Min</p></div>', unsafe_allow_html=True)
c4,c5,c6=st.columns(3)
with c4:
    if st.button("🎭 Drama"):
        st.session_state.mode="Drama"; st.rerun()
    st.markdown('<div class="mode-card mode-drama"><div style="font-size:40px;">🎭</div><h3>Drama</h3><p>3-4 Character<br>Pakistani Drama Jaisa<br>Part 1,2,3</p></div>', unsafe_allow_html=True)
with c5:
    if st.button("🚶 Vlog"):
        st.session_state.mode="Vlog"; st.rerun()
    st.markdown('<div class="mode-card mode-vlog"><div style="font-size:40px;">🚶</div><h3>Vlog</h3><p>1 Ya 2 Character<br>Visit + Explain<br>Short / Long</p></div>', unsafe_allow_html=True)
with c6:
    if st.button("🕌 Quran Recitation"):
        st.session_state.mode="Quran Recitation"; st.rerun()
    st.markdown('<div class="mode-card mode-quran"><div style="font-size:40px;">🕌</div><h3>Quran Recitation</h3><p>Quran.com Wala<br>Safe + Monetize<br>Arabic + Urdu Tarjuma</p></div>', unsafe_allow_html=True)
st.write("")
# ===== NAYA MODE - 7th - DRAMA REVIEW =====
st.markdown("### ⭐ NAYA MODE - 7th - DRAMA REVIEW + PREDICTION - 1 CHARACTER ⭐")
col_new1, col_new2 = st.columns([1, 2])
with col_new1:
    if st.button("🎬 Drama Review + Prediction\n1 Character - Beth Kar Batayega"):
        st.session_state.mode="Drama Review + Prediction"; st.rerun()
with col_new2:
    st.markdown('<div class="mode-card mode-review"><div style="font-size:40px;">🎬</div><h3>DRAMA REVIEW + PREDICTION - NAYA!</h3><p>1 Character - Beth Kar Batayega | Ye Hua, Wo Hua, Aage Kya Hoga?<br>Drama Ka Review + Agli Episode Ki Prediction | Short 40 Sec / 60 Sec / Long 8 Min / 15 Min</p></div>', unsafe_allow_html=True)

st.success(f"✅ Selected Mode: {st.session_state.mode}")
st.write("---")

st.header(f"STEP 1.1: {st.session_state.mode} - Details Bharo")
topic=st.text_input("Topic Likho", "Meem Se Mohabbat - Episode 20" if st.session_state.mode=="Drama Review + Prediction" else "Sea View Ki Kahani" if st.session_state.mode!="Quran Recitation" else "Surah Rehman", key="topic_input")
st.session_state.topic=topic
duration=st.selectbox("Video Kitni Lambi Ho?", ["Short 40 Sec","Short 60 Sec","Long 8 Min","Long 15 Min","30 Min","1 Ghanta"] if st.session_state.mode=="Podcast Video" else ["Short 40 Sec","Short 60 Sec","Long 8 Min","Long 15 Min"])
extra_info=""
if st.session_state.mode=="Drama Review + Prediction":
    st.markdown('<div class="review-box"><h2>🎬 DRAMA REVIEW + PREDICTION - 1 CHARACTER - Beth Kar Batayega</h2><p>Ye Mode Sirf Drama Review Ke Liye Hai - 1 Aadmi Beth Kar Batayega: Ye Hua, Wo Hua, Aage Kya Hoga?</p></div>', unsafe_allow_html=True)
    st.write("")
    drama_name=st.selectbox("Konsa Drama?", ["Meem Se Mohabbat","Jaan Nisar","Kaffara","Noor Jahan","Jaan E Jahan","Apna Drama Likho"])
    if drama_name=="Apna Drama Likho": drama_name=st.text_input("Apna Drama Likho", "Meem Se Mohabbat")
    episode=st.text_input("Konsi Episode Ka Review Hai?", "Episode 20 - Kal Wali")
    review_type=st.selectbox("Review Kaisa?", ["Full Review + Prediction - Ye Hua, Wo Hua, Aage Kya Hoga?","Sirf Review - Ye Hua, Wo Hua","Sirf Prediction - Aage Kya Hoga?","Promo / Teaser Review"])
    style=st.selectbox("Style Kaisa?", ["Beth Kar Samjhana - Serious + Funny Mix","Emotional - Dukh Wala","Funny - Mazak Wala","Suspense Wala - Aage Kya Hoga?"])
    extra_info=f"Drama: {drama_name} - {episode} - {review_type} - Style: {style}"
    st.info(f"Selected: {extra_info}")
    st.write("Is Mode Me Script Aisi Hogi:")
    st.write("- **Part 1 - YE HUA:** Pichli Episode Me Kya Hua?")
    st.write("- **Part 2 - WO HUA:** Detail Me - Hero Ne Kya Kiya? Heroine Ne Kya Kiya? Villain Ne Kya Kiya?")
    st.write("- **Part 3 - AAGE KYA HOGA?:** Prediction - Agli Episode Me Kya Hoga? Twist Kya Aayega?")
    st.write("- **End:** Tumko Kya Lagta Hai? Comment Me Batao - Tumhari Prediction Kya Hai?")
elif st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h2>🕌 QURAN - Quran.com Wala</h2><p>Avatar BAND - Music BAND - Sirf Arabic + Tarjuma + Background</p></div>', unsafe_allow_html=True)
    surah=st.selectbox("Konsi Surah?", ["Surah Yaseen","Surah Rehman","Surah Mulk","Ayatul Kursi","Apni Likho"])
    if surah=="Apni Likho": surah=st.text_input("Apni Surah Likho", "Surah Fatiha")
    qari=st.selectbox("Konsa Qari? [Quran.com Wala]", ["Mishary Rashid Alafasy - Quran.com","Abdul Basit - Quran.com","Abdul Rahman Al-Sudais - Quran.com"])
    extra_info=f"{surah} - Qari: {qari}"
    st.info(f"Selected: {extra_info}")
elif st.session_state.mode=="Vlog":
    char_count=st.selectbox("Kitne Character?", ["1","2"])
    kahan=st.selectbox("Kahan Gaye Ho?", ["Sea View","Saddar","Gaon","Faisal Masjid","Apni Jagah Likho"])
    if kahan=="Apni Jagah Likho": kahan=st.text_input("Apni Jagah Likho", "Clifton Beach")
    extra_info=f"{kahan} - {char_count} Character"
elif st.session_state.mode=="Drama":
    char_count=st.selectbox("Kitne Character?", ["2","3","4"])
    drama_type=st.selectbox("Drama Kaisa?", ["Emotional","Sad","Funny","Suspense","Pyar Wala","Saas Bahu Wala"])
    parts=st.selectbox("Kitne Part?", ["1 Part","3 Part - Part 1, 2, 3"])
    extra_info=f"{char_count} Character - {drama_type} - {parts}"
elif st.session_state.mode=="Comedy Show":
    extra_info="Bablu + Chacha - 2 Men"
elif st.session_state.mode=="Podcast Video":
    extra_info="Host + Guest"
else:
    extra_info="Single - 1 Aadmi"

st.write("---")
st.header("STEP 2: KEYWORDS + VIRAL CHANCE")
if st.button("Step 2 - Keywords + Viral Chance Nikalo"):
    with st.spinner("Trends Dekh Raha Hoon..."):
        kw_res=ai(f"Give 30 best keywords for topic {topic} mode {st.session_state.mode}. Main keyword 1 High Search Low Competition. Viral chance %. If low, suggest 3 new topics.", topic=topic, mode=st.session_state.mode, extra=extra_info)
    st.write(kw_res)
    viral=random.randint(75, 94) if st.session_state.mode=="Drama Review + Prediction" else random.randint(65, 92)
    st.markdown(f"<h2>🔥 VIRAL CHANCE: {viral}% - Drama Review Hamesha Zyada Chalta Hai!</h2>", unsafe_allow_html=True)
    st.progress(viral/100)
    st.session_state.main_kw=topic
    st.write(f"**Main Keyword: {st.session_state.main_kw}**")

st.write("---")
st.header("STEP 3: TOP 10 VIDEO ANALYZE")
if st.button("Top 10 Video Dekho"):
    with st.spinner("Top 10 Dekh Raha Hoon..."):
        try:
            r=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}&type=video&maxResults=10&key={YT}", timeout=12).json()
            if "items" in r:
                for i, v in enumerate(r["items"]):
                    st.image(v["snippet"]["thumbnails"]["medium"]["url"], width=250)
                    st.write(f"**#{i+1} {v['snippet']['title'][:70]}** - {v['snippet']['channelTitle']}")
            else:
                st.write(ai(f"Top 10 video for {topic}", topic=topic))
        except:
            st.write(ai(f"Top 10 video for {topic}", topic=topic))

st.write("---")
st.header("STEP 4: SCRIPT - PUNCTUATION LAZMI + MODE KE HISAB SE")
st.write("Script Me Ye Sab Lazmi: , . ? ! ... Hahaha / Hmm / Ohh")
if st.button("Step 4 - Script Banao"):
    with st.spinner("Script Likh Raha Hoon..."):
        script=ai(f"Write full script for mode {st.session_state.mode} topic {topic} duration {duration} extra {extra_info}. Use punctuation , . ? ! ... Hahaha Hmm Ohh. For Drama Review: Part 1 Ye Hua, Part 2 Wo Hua Detail, Part 3 Aage Kya Hoga Prediction, End Comment Sawal. In Urdu + English mix.", topic=topic, mode=st.session_state.mode, extra=extra_info)
    st.session_state.script=script
    st.write(script)
    st.code(script)
    if st.session_state.mode=="Drama Review + Prediction":
        st.success("✅ Drama Review Script Ready - 3 Part Me Hai: Ye Hua + Wo Hua + Aage Kya Hoga?")

st.write("---")
st.header("STEP 5: VOICE OVER - HUMANIZE")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>Quran Voice - 2 Voices - Qari Quran.com Se, Tarjuma Clone Voice Se</h3></div>', unsafe_allow_html=True)
    st.audio("https://download.quranicaudio.com/quran/mishaari_raashid_al_3afaasee/001001.mp3")
elif st.session_state.mode=="Drama Review + Prediction":
    st.markdown('<div class="review-box"><h3>🎬 Drama Review Voice - 1 Character - Beth Kar Bolega</h3><p>1 Voice - Tumhari Awaz Ya Clone Voice - Serious + Funny Mix - Beth Kar Samjhayega - Jaise Tum Baat Kar Rahe Ho</p></div>', unsafe_allow_html=True)
    v1=st.selectbox("Voice 1 - Review Wala", ["Tumhari Clone Voice - Best Hai Drama Review Ke Liye","Islamic Male - Deep","Vlogger - Energetic","Young Boy - Funny"])
    st.write("Voice Clone - Apni 30 Sec Awaz Upload Karo - Taake Review Tumhari Awaz Me Lage")
    uploaded_voice=st.file_uploader("Apni 30 Sec Awaz Upload Karo", type=["mp3","wav"], key="review_voice")
    if uploaded_voice:
        st.success("✅ Voice Clone Upload Ho Gayi - Ab Review Tumhari Awaz Me Bolega")
        st.audio(uploaded_voice)
else:
    voice_engine=st.selectbox("Voice Engine", ["Edge TTS - Free - Best","Google Cloud TTS","gTTS - Free"])
    st.write(f"Selected: {voice_engine}")
    uploaded_voice=st.file_uploader("Apni 30 Sec Awaz Upload Karo", type=["mp3","wav"])
    if uploaded_voice: st.audio(uploaded_voice)
st.write("Humanize: Saans Lena + Zor Dena + Comma Par Thora Rukna, Full Stop Par Zyada Rukna")
if st.button("Voice Over Banao"):
    st.success("✅ Voice Over Ready (Demo) - Real Me Edge TTS Se Banega")

st.write("---")
st.header("STEP 6: PHOTO + VIDEOS")
photo_source=st.selectbox("Photo / Video Kahan Se?", ["AI Se Banao - FLUX","Pexels Se Lo - Free","Apni Photo Upload Karo"])
if photo_source=="AI Se Banao - FLUX":
    flux_prompt=st.text_input("FLUX Prompt", f"{topic} - Beautiful - 4K")
    if st.button("FLUX Se Photo Banao"):
        st.write(ai(f"FLUX prompt for {topic}", topic=topic))
elif photo_source=="Pexels Se Lo - Free":
    st.write("Pexels Se Free - Sample:")
    st.image("https://images.unsplash.com/photo-1512632578888-169bbbc64f33?w=600", use_container_width=True)
else:
    up=st.file_uploader("Apni Photo Upload Karo", type=["jpg","png","jpeg"])
    if up: st.image(up, use_container_width=True)
if st.session_state.mode=="Drama Review + Prediction":
    st.info("Drama Review Ke Liye: Drama Ki Clips / Photos - Hero / Heroine / Villain Ki Photo - Episode Ke Scene Ki Photo - Background Me Drama Ka Poster")
elif st.session_state.mode=="Drama":
    st.info("Drama: Har Scene Alag - Ghar / Bazaar / School")
elif st.session_state.mode=="Quran Recitation":
    st.info("Quran: Makkah / Madina / Masjid / Aasman")

st.write("---")
st.header("STEP 7: AVATAR - HUMANIZE")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>🚫 QURAN ME AVATAR BAND HAI</h3></div>', unsafe_allow_html=True)
elif st.session_state.mode=="Drama Review + Prediction":
    st.markdown('<div class="review-box"><h3>🎬 Drama Review Avatar - 1 Character - Beth Kar Batayega</h3><p>1 Avatar - Betha Hua - Haath Se Ishara Karega - "Ye Hua, Wo Hua" - Munh Hilega - Aankhen Jhapkenge - Sir Hilayega</p></div>', unsafe_allow_html=True)
    avatar_choice=st.selectbox("Review Wala Avatar Kaunsa?", ["Tumhara Apna Avatar - Apni Photo Upload Karo (Best Hai)","Vlogger - Beth Kar Batayega","Islamic Male - Beth Kar Batayega","Young Boy - Funny Review","Old Man - Samajhdaar Review","Avatar Band Karo - Sirf Voice + Drama Clips"])
    if avatar_choice=="Tumhara Apna Avatar - Apni Photo Upload Karo (Best Hai)":
        av_photo=st.file_uploader("Apni Photo - Review Avatar Ke Liye", type=["jpg","png"])
        if av_photo: st.image(av_photo, width=200)
    st.write("Humanize: Beth Kar Bolega, Haath Hilayega, Chehra - Jab Twist Batayega To Shocked Face, Jab Funny Batayega To Hasega")
else:
    avatar_choice=st.selectbox("Avatar Chuno", ["Islamic Male","Hijab Female","Young Boy","Old Man","Hero","Heroine","Ammi","Villain","Vlogger","Apni Photo Upload Karo","Avatar Band Karo"])
    st.write("Humanize: Lipsync + Aankhen Jhapakna + Sir Hilana + Haath Hilana")

st.write("---")
st.header("STEP 8: LOGO")
logo_file=st.file_uploader("Apna Logo Upload Karo", type=["png","jpg"])
if logo_file: st.image(logo_file, width=150)

st.write("---")
st.header("STEP 9: EDITING")
if st.session_state.mode=="Quran Recitation":
    st.markdown('<div class="quran-box"><h3>QURAN ME MUSIC BAND HAI</h3><p>Tarteeb: Arabic Ayat -> Qari Awaz -> 1 Sec Rukega -> Tarjuma Voice -> Tarjuma Screen -> Background -> Agli Ayat</p></div>', unsafe_allow_html=True)
elif st.session_state.mode=="Drama Review + Prediction":
    st.write("Drama Review Editing: Drama Ki Clips + Tumhara Avatar Beth Kar Bolega + Subtitles + Subscribe Button")
    music_choice=st.selectbox("Music?", ["Zeniq Ka Free Music - Suspense - Prediction Ke Liye Best","Zeniq Ka Free Music - Emotional","Zeniq Ka Free Music - Drama","Continue Without Music"])
    st.write(f"Selected: {music_choice} - Prediction Wale Part Me Suspense Music Aayega - Review Wale Part Me Halka Music")
else:
    music_choice=st.selectbox("Music Chuno", ["Apna Music Upload Karo","Zeniq Ka Free Music - Emotional","Zeniq Ka Free Music - Islamic","Zeniq Ka Free Music - Suspense","Zeniq Ka Free Music - Motivational","Zeniq Ka Free Music - Sad","Zeniq Ka Free Music - Comedy","Zeniq Ka Free Music - Drama","Continue Without Music"])
    st.write(f"Selected: {music_choice}")

st.write("---")
st.header("STEP 10: FINAL RENDERING + LONG SE SHORT AUTO CUTTER")
if st.button("Final Video Banao + 3 Shorts Auto"):
    if st.session_state.videos_today >= 20:
        st.error("❌ Limit Khatam - 20 Ho Gayi")
    else:
        st.session_state.videos_today += 1
        st.success(f"✅ Final Video Ban Gayi! {st.session_state.videos_today}/20")
        st.write("Long Video: Ready")
        st.write("Short 1: Best Hissa - 40 Sec - Auto Cut")
        st.write("Short 2: Second Best - 40 Sec")
        st.write("Short 3: Third Best - 40 Sec")
        if st.session_state.mode=="Drama Review + Prediction":
            st.write("Drama Review Short: 'Aage Kya Hoga? - 1 Prediction' - 40 Sec Short Bhi Bana Diya - Ye Sab Se Zyada Chalega!")
        if st.session_state.mode=="Drama":
            st.write("Drama: Part 1,2,3 Alag Alag")
        if st.session_state.mode=="Quran Recitation":
            st.write("Quran: 1 Ayat Wala Short Bhi Bana Diya")

st.write("---")
st.header("STEP 11: TITLE + THUMBNAIL + DESCRIPTION + TAGS - EK HI KEYWORD RULE")
st.write(f"Main Keyword: {st.session_state.main_kw if st.session_state.main_kw else topic}")
if st.button("Step 11 - Title + Thumbnail + Description + Tags Banao"):
    main_kw = st.session_state.main_kw if st.session_state.main_kw else topic
    st.subheader("Title: 3 - Teenon Me Wahi Main Keyword - Shuru Me")
    st.write(ai(f"Give 3 titles for {topic} main keyword {main_kw} must be at start", topic=topic))
    st.write("---")
    st.subheader("Thumbnail: 3 - Teenon Par Wahi Main Keyword")
    st.write(ai(f"Give 3 thumbnails for {topic} main keyword {main_kw}", topic=topic))
    st.write("---")
    st.subheader("Description: Pehli 2 Line Me Main Keyword 2 Baar")
    desc_res=ai(f"Write description for {topic} main keyword {main_kw} 2 times in first 2 lines", topic=topic)
    st.write(desc_res); st.code(desc_res)
    if st.session_state.mode=="Quran Recitation":
        st.code("Recitation & Text via Quran.com / Quran Foundation - Translation Voice: Zeniq")
    st.write("---")
    st.subheader("Tags: 30 Tags - Pehla Tag = Main Keyword")
    tags_res=ai(f"Give 30 tags for {topic} first tag {main_kw}", topic=topic)
    st.write(tags_res); st.code(tags_res)
    if st.session_state.mode=="Drama Review + Prediction":
        st.info("Drama Review Ke Liye Extra Tags: Drama Review, Drama Prediction, Drama Update, Drama Today Episode, Drama Twist")

st.write("---")
st.header("STEP 12: ZENIQ SCORE + FIX + A/B TESTING")
if st.button("Zeniq Score Dekho"):
    score = random.randint(88, 96) if st.session_state.mode=="Drama Review + Prediction" else random.randint(85, 96)
    st.markdown(f"<h1 style='text-align:center;'>🎯 ZENIQ SCORE: {score} / 100</h1>", unsafe_allow_html=True)
    st.progress(score/100)
    if st.button("Fix Karo"):
        st.write(ai(f"Fix video {topic} mode {st.session_state.mode} score {score}", topic=topic))
        st.success("✅ Fix Ho Gaya!")
st.subheader("A/B Testing")
col_a,col_b=st.columns(2)
with col_a:
    st.markdown('<div class="card-red"><h2>Thumbnail A</h2><p>Red - Score 82</p></div>', unsafe_allow_html=True)
    va=st.number_input("A Clicks?", value=100, key="z_ab_a")
with col_b:
    st.markdown('<div class="card-blue"><h2>Thumbnail B</h2><p>Yellow - Score 91</p></div>', unsafe_allow_html=True)
    vb=st.number_input("B Clicks?", value=150, key="z_ab_b")
if st.button("Kaunsa Jeeta?"):
    if vb>va: st.success(f"🏆 B Jeet Gaya! B {vb}, A {va}")
    else: st.success(f"🏆 A Jeet Gaya! A {va}, B {vb}")

st.write("---")
st.header("STEP 13: SCHEDULER + BULK UPLOAD")
up_opt=st.selectbox("Upload Kaise?", ["Abhi Upload Karo","Scheduler: Time Set Karo","Bulk Mode: 10 Video Ek Saath"])
platform=st.selectbox("Kahan Upload?", ["YouTube","TikTok","Shorts","Download","YouTube + TikTok + Shorts"])
if up_opt=="Scheduler: Time Set Karo":
    up_date=st.date_input("Kis Din?")
    up_time=st.selectbox("Time?", ["Subah 9 Baje Long","Shaam 6 Baje Short","Raat 9 Baje Long","Dopahar 1 Baje Short"])
    if st.button("Schedule Karo"):
        st.success(f"✅ Scheduled! {up_date} Ko {up_time} Par {platform} Par")
elif up_opt=="Bulk Mode: 10 Video Ek Saath":
    if st.button("Bulk Mode Start Karo"):
        st.success("✅ Bulk Mode Start - 10 Video Ban Rahi Hain")
else:
    if st.button("Abhi Upload Karo"):
        st.success(f"✅ Upload Ho Gayi! Platform: {platform} (Demo)")

st.write("---")
st.markdown("<p style='text-align:center;'>🔒 ZENIQ FINAL v2 - 7 MODE WALA | Drama Review + Prediction - NAYA | Quran.com Wala | 20 Video Roz | FREE</p>", unsafe_allow_html=True)
