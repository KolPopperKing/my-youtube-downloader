import streamlit as st
import requests

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
st.write("גרסה יציבה ועוקפת חסימות (Cobalt API). הדביקו לינק והורידו ישירות.")

# תיבת קלט ללינק
url_input = st.text_input("הלינק שלך:", placeholder="https://www.youtube.com/watch?v=...")

# בחירת סוג ההורדה
download_type = st.radio("מה ברצונך להוריד?", ["שיר (MP3)", "סרטון וידאו (MP4)"])

if st.button("הכן קובץ להורדה"):
    if not url_input:
        st.error("🚨 אופס, שכחת להדביק לינק!")
    else:
        with st.spinner("⏳ המנוע מעבד את הקובץ... זה לוקח כמה שניות"):
            try:
                # הגדרת הבקשה לשרת Cobalt הציבורי והרשמי
                api_url = "https://api.cobalt.tools/"
                
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                # הגדרות הפורמט לפי הבחירה של המשתמש
                is_audio_only = True if download_type == "שיר (MP3)" else False
                
                payload = {
                    "url": url_input,
                    "vCodec": "h264",      # פורמט וידאו סטנדרטי שנתמך בכל מכשיר
                    "isAudioOnly": is_audio_only,
                    "aFormat": "mp3",      # אם זה רק אודיו, שיוריד כ-MP3
                    "filenamePattern": "classic" # שומר על שם הסרטון המקורי
                }
                
                # שליחת הבקשה ל-Cobalt
                response = requests.post(api_url, json=payload, headers=headers, timeout=30)
                
                if response.status_code != 200:
                    raise Exception("השרת עמוס כרגע או שיוטיוב חסם את הבקשה הספציפית הזו.")
                
                data = response.json()
                
                # Cobalt מחזיר סטטוס picker או tunnel או url
                status = data.get("status")
                download_link = data.get("url")
                
                if status == "error":
                    raise Exception(data.get("text", "שגיאה לא ידועה במנוע ההורדה."))
                
                if not download_link:
                    raise Exception("לא התקבל לינק תקין להורדה.")
                
                # מורידים את הקובץ המוכן מ-Cobalt ומעבירים למשתמש
                file_response = requests.get(download_link, stream=True)
                file_bytes = file_response.content
                
                ext = "mp3" if is_audio_only else "mp4"
                filename = f"download.{ext}"
                
                st.success(f"✅ ה{download_type.split(' ')[0]} מוכן!")
                st.download_button(
                    label="⬇️ לחצו כאן לשמירת הקובץ במכשיר",
                    data=file_bytes,
                    file_name=filename,
                    mime="audio/mpeg" if is_audio_only else "video/mp4"
                )
                    
            except Exception as e:
                st.error(f"❌ תקלה במנוע ההורדות: {str(e)}")
