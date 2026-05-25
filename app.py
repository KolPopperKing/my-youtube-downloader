import streamlit as st
import requests
import re

# הגדרות עמוד ועיצוב בעברית
st.set_page_config(page_title="Premium Downloader", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .main { text-align: center; direction: rtl; }
    div.stButton > button:first-child {
        background-color: #4d76fd;
        color: white;
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(77, 118, 253, 0.3);
        width: 100%;
        font-size: 1.1rem;
    }
    input { text-align: left; direction: ltr; }
    .stRadio > div { flex-direction: row; justify-content: center; gap: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("הורדת שירים וסרטונים מיוטיוב 🎬🎵")
st.write("גרסה יציבה ועוקפת חסימות. הדביקו לינק, בחרו פורמט והורידו ישירות למכשיר.")

# תיבת קלט ללינק
url_input = st.text_input("הלינק שלך:", placeholder="https://www.youtube.com/watch?v=...")

# בחירת סוג ההורדה
download_type = st.radio("מה ברצונך להוריד?", ["שיר (MP3)", "סרטון וידאו (MP4)"])

def extract_video_id(url):
    pattern = r'(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

if st.button("הכן קובץ להורדה"):
    if not url_input:
        st.error("🚨 אופס, שכחת להדביק לינק!")
    else:
        video_id = extract_video_id(url_input)
        if not video_id:
            st.error("❌ הלינק לא תקין, אנא ודא שהעתקת לינק נכון מיוטיוב.")
        else:
            with st.spinner("⏳ המנוע החיצוני מעבד את השיר... זה לוקח כמה שניות"):
                try:
                    # שימוש ב-API ציבורי חזק של קהילת המפתחים לעקיפת יוטיוב
                    format_type = "mp3" if download_type == "שיר (MP3)" else "mp4"
                    api_url = f"https://api.vexdw.com/download?v={video_id}&format={format_type}"
                    
                    response = requests.get(api_url, timeout=30)
                    
                    if response.status_code != 200:
                        raise Exception("השרת החיצוני עמוס כרגע. נסה שוב בעוד רגע.")
                    
                    data = response.json()
                    
                    if not data.get("success") or not data.get("download_url"):
                        raise Exception("לא הצלחנו לחלץ את הלינק להורדה. נסה שיר אחר.")
                    
                    download_link = data.get("download_url")
                    title = data.get("title", "download")
                    ext = "mp3" if format_type == "mp3" else "mp4"
                    
                    # מורידים את הקובץ מה-API לזיכרון של האתר שלנו כדי להגיש למשתמש בלחיצה
                    file_response = requests.get(download_link, stream=True)
                    file_bytes = file_response.content
                    
                    st.success(f"✅ ה{download_type.split(' ')[0]} מוכן!")
                    st.download_button(
                        label="⬇️ לחצו כאן לשמירת הקובץ במכשיר",
                        data=file_bytes,
                        file_name=f"{title}.{ext}",
                        mime="audio/mpeg" if format_type == "mp3" else "video/mp4"
                    )
                        
                except Exception as e:
                    st.error(f"❌ תקלה במנוע ההורדות: {str(e)}")
