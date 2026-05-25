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
st.write("הדביקו לינק, בחרו פורמט, והורידו ישירות למכשיר שלכם בצורה יציבה.")

# תיבת קלט ללינק
RENDER_BACKEND_URL = "https://my-downloader-ap.onrender.com/download"
# בחירת סוג ההורדה
download_type = st.radio("מה ברצונך להוריד?", ["שיר (MP3)", "סרטון וידאו (MP4)"])

# ⚠️ חשוב מאוד: תחליף את הכתובת למטה בלינק האמיתי שקיבלת מ-Render!
RENDER_BACKEND_URL = "https://your-downloader-api.onrender.com/download"

if st.button("הכן קובץ להורדה"):
    if not url_input:
        st.error("🚨 אופס, שכחת להדביק לינק!")
    elif "your-downloader-api" in RENDER_BACKEND_URL:
        st.error("🔧 עצור אחי! שכחת לעדכן את הלינק של Render בתוך הקוד של ה-Streamlit.")
    else:
        with st.spinner("⏳ השרת הפרטי שלך מעבד את הקובץ... זה לוקח כמה שניות"):
            try:
                # קביעת סוג הפורמט עבור השרת
                backend_type = "mp3" if download_type == "שיר (MP3)" else "mp4"
                
                # פנייה לשרת ה-Render שלך שיעשה את העבודה הקשה
                params = {"url": url_input, "type": backend_type}
                response = requests.get(RENDER_BACKEND_URL, params=params, stream=True, timeout=60)
                
                if response.status_code != 200:
                    raise Exception("השרת של Render החזיר שגיאה. ודא שהלינק ביוטיוב תקין.")
                
                # שליפת שם הקובץ ש-Render שלח בתוך ה-Headers
                content_disp = response.headers.get('Content-Disposition', '')
                filename = "download.mp3" if backend_type == "mp3" else "download.mp4"
                if "filename=" in content_disp:
                    filename = content_disp.split('filename=')[1].strip('"')
                
                # קריאת הקובץ המוזרם לזיכרון
                file_bytes = response.content
                
                st.success(f"✅ ה{download_type.split(' ')[0]} מוכן!")
                st.download_button(
                    label="⬇️ לחצו כאן לשמירת הקובץ במכשיר",
                    data=file_bytes,
                    file_name=filename,
                    mime="audio/mpeg" if backend_type == "mp3" else "video/mp4"
                )
                    
            except Exception as e:
                st.error(f"❌ תקלה בהורדה: {str(e)}")
