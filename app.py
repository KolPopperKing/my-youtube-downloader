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
st.write("הגרסה העוקפת חסימות. הדביקו לינק, בחרו פורמט והורידו ישירות.")

# תיבת קלט ללינק
url_input = st.text_input("הלינק שלך:", placeholder="https://www.youtube.com/watch?v=...")

# בחירת סוג ההורדה
download_type = st.radio("מה ברצונך להוריד?", ["שיר (MP3)", "סרטון וידאו (MP4)"])

# פונקציה לחילוץ מזהה הסרטון (Video ID)
def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
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
            with st.spinner("⏳ עוקף את החסימה ומחלץ את הקובץ... רק רגע"):
                try:
                    # רשימת שרתים מבוזרים למקרה שאחד עמוס
                    instances = [
                        "https://invidious.vpsbroy.at",
                        "https://yewtu.be",
                        "https://invidious.nerdvpn.de",
                        "https://inv.tux.digital"
                    ]
                    
                    data = None
                    # לולאה שמנסה למשוך את המידע מהשרת הראשון שזמין
                    for instance in instances:
                        try:
                            api_url = f"{instance}/api/v1/videos/{video_id}"
                            response = requests.get(api_url, timeout=7)
                            if response.status_code == 200:
                                data = response.json()
                                break
                        except:
                            continue
                    
                    if not data:
                        raise Exception("כל השרתים העוקפים עמוסים כרגע, נסה שוב בעוד רגע.")
                    
                    title = data.get('title', 'download').replace(' ', '_')
                    
                    # פילטור הלינקים הנכונים (אודיו או וידאו)
                    format_url = None
                    if download_type == "שיר (MP3)":
                        # מחפש קובץ אודיו בלבד
                        audio_streams = [f for f in data.get('adaptiveFormats', []) if 'audio/' in f.get('type', '')]
                        if audio_streams:
                            format_url = audio_streams[0]['url']
                        filename = f"{title}.mp3"
                        mime_type = "audio/mpeg"
                    else:
                        # מחפש קובץ וידאו מוכן כולל סאונד
                        video_streams = [f for f in data.get('formatStreams', []) if 'video/' in f.get('type', '')]
                        if video_streams:
                            format_url = video_streams[0]['url']
                        filename = f"{title}.mp4"
                        mime_type = "video/mp4"
                    
                    if not format_url:
                        raise Exception("לא נמצא פורמט מתאים להורדה.")
                    
                    # הורדת הקובץ עצמו לזיכרון השרת באופן זמני ושליחה למשתמש
                    file_response = requests.get(format_url, stream=True)
                    file_bytes = file_response.content
                    
                    st.success(f"✅ ה{download_type.split(' ')[0]} מוכן!")
                    st.download_button(
                        label="⬇️ לחצו כאן לשמירת הקובץ",
                        data=file_bytes,
                        file_name=filename,
                        mime=mime_type
                    )
                        
                except Exception as e:
                    st.error(f"❌ שגיאה במערכת העקיפה: {str(e)}")
