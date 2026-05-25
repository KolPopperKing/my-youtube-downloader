import streamlit as st
import yt_dlp
import os

# הגדרות עמוד ועיצוב בעברית
st.set_page_config(page_title="YouTube Downloader", page_icon="🎵", layout="centered")

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
    </style>
""", unsafe_allow_html=True)

st.title("הורדת שירים מיוטיוב 🎵")
st.write("הדביקו לינק מיוטיוב, לחצו על הכפתור ותקבלו קובץ שמע ישירות למכשיר.")

url_input = st.text_input("הלינק שלך:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("הפוך ל-MP3 והורד"):
    if not url_input:
        st.error("🚨 אופס, שכחת להדביק לינק!")
    else:
        with st.spinner("⏳ המנוע מעבד את השיר... זה לוקח כמה שניות"):
            try:
                # הגדרות הורדה קלות שמתאימות לשרת ענן ללא FFmpeg חיצוני
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'restrictfilenames': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_input, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # שינוי סיומת זמני כדי שהדפדפן יזהה את זה כקובץ שמע בקלות
                    base, ext = os.path.splitext(filename)
                    mp3_filename = base + '.mp3'
                    os.rename(filename, mp3_filename)
                    
                    with open(mp3_filename, "rb") as file:
                        file_bytes = file.read()
                        
                        st.success("✅ השיר מוכן!")
                        st.download_button(
                            label="⬇️ לחצו כאן לשמירת השיר",
                            data=file_bytes,
                            file_name=os.path.basename(mp3_filename),
                            mime="audio/mpeg"
                        )
                
                # ניקוי השרת
                if os.path.exists(mp3_filename):
                    os.remove(mp3_filename)
                    
            except Exception as e:
                st.error("❌ תקלה בהורדה. ודאו שהלינק תקין ונסו שוב.")