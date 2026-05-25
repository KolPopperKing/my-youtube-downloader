import streamlit as st
import yt_dlp
import os

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
st.write("הדביקו לינק, בחרו פורמט, ותורידו ישירות למכשיר בחינם.")

# תיבת קלט ללינק
url_input = st.text_input("הלינק שלך:", placeholder="https://www.youtube.com/watch?v=...")

# בחירת סוג ההורדה (שיר או וידאו)
download_type = st.radio("מה ברצונך להוריד?", ["שיר (MP3)", "סרטון וידאו (MP4)"])

if st.button("הכן קובץ להורדה"):
    if not url_input:
        st.error("🚨 אופס, שכחת להדביק לינק!")
    else:
        with st.spinner("⏳ המנוע מעבד את הקובץ בענן... רק רגע"):
            try:
                # הגדרות דינמיות לפי בחירת המשתמש שעובדות פיקס על שרת ענן
                if download_type == "שיר (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio',  # מוריד את האודיו הכי טוב שזמין מובנה
                        'outtmpl': '%(title)s.mp3', # שומר ישר כ-MP3 בלי המרות מורכבות שעושות תקלות
                        'restrictfilenames': True,
                    }
                    mime_type = "audio/mpeg"
                    default_ext = ".mp3"
                else:
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best', # מוריד וידאו קומפלט כולל סאונד בפורמט MP4
                        'outtmpl': '%(title)s.mp4',
                        'restrictfilenames': True,
                    }
                    mime_type = "video/mp4"
                    default_ext = ".mp4"
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_input, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # וידוא סיומת נכונה למניעת באגים
                    if download_type == "שיר (MP3)" and not filename.endswith('.mp3'):
                        base, _ = os.path.splitext(filename)
                        new_name = base + '.mp3'
                        if os.path.exists(filename):
                            os.rename(filename, new_name)
                        filename = new_name

                    with open(filename, "rb") as file:
                        file_bytes = file.read()
                        
                        st.success(f"✅ ה{download_type.split(' ')[0]} מוכן!")
                        st.download_button(
                            label="⬇️ לחצו כאן לשמירת הקובץ",
                            data=file_bytes,
                            file_name=os.path.basename(filename),
                            mime=mime_type
                        )
                
                # ניקוי השרת
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error("❌ תקלה בהורדה. יוטיוב חסם את הבקשה או שהלינק לא תקין. נסה לינק אחר.")
