import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import requests

app = FastAPI()

# מאפשר לכל אתר לגשת לשרת שלנו
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.get("/download")
def download(url: str, type: str):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # הגדרות מתקדמות שעוקפות את החסימה על ידי התחזות לאפליקציית מובייל
    ydl_opts = {
        'format': 'bestaudio' if type == "mp3" else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        # הקסם שעוקף את החסימות: מכריח את yt-dlp להתחזות ללקוח אנדרואיד רשמי
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # לוקחים ישירות את הלינק הישיר לקובץ הגולמי משרתי יוטיוב
            download_url = info.get('url') if type == "mp3" else info.get('url')
            if not download_url and 'formats' in info:
                # אם זה וידאו, ניקח את הפורמט הכי מתאים שיש לו גם סאונד וגם וידאו
                formats = [f for f in info['formats'] if f.get('acodec') != 'none' and f.get('vcodec') != 'none']
                if not formats:
                    formats = info['formats']
                download_url = formats[-1]['url']
                
            title = info.get('title', 'download').replace(' ', '_')
            ext = "mp3" if type == "mp3" else "mp4"
            
            # מזרימים את הקובץ ישירות מהשרת של יוטיוב למשתמש (בלי לשמור על השרת שלנו!)
            req = requests.get(download_url, stream=True)
            
            headers = {
                'Content-Disposition': f'attachment; filename="{title}.{ext}"'
            }
            
            return StreamingResponse(
                req.iter_content(chunk_size=1024*1024), 
                media_type="audio/mpeg" if type == "mp3" else "video/mp4",
                headers=headers
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
