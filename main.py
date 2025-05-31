import whisper
from moviepy import VideoFileClip
import os

VIDEO_FILE = "video2.mp4" #اسم ویدیو ای ک میخواهید برسی شود
KEYWORDS_FILE = "keywords.txt" # کلمات کلیدی
OUTPUT_DIR = "clips" #ویدیو های استخراج شده در این پوشه قرار میگیرند
PRE_POST_SECONDS = 15

print("LOADING MODEL")
model = whisper.load_model("base") #Change to "Large" to Try Persian Language
print("LOADING MODEL DONE")

# مرحله ۱: تبدیل گفتار به متن با تایم‌استمپ
print("Transcribing video...")
result = model.transcribe(VIDEO_FILE, word_timestamps=False)

segments = result['segments']
full_text = result['text'].lower()
print(full_text)

# مرحله ۲: خواندن کلمات کلیدی
with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
    keywords = [line.strip().lower() for line in f if line.strip()]

# مرحله ۳: یافتن تطابق
print("Finding matches...")
matched_segments = []

for keyword in keywords:
    for seg in segments:
        if keyword in seg['text'].lower():
            matched_segments.append({
                "keyword": keyword,
                "start": max(0, seg['start'] - PRE_POST_SECONDS),
                "end": seg['end'] + PRE_POST_SECONDS
            })
if not matched_segments:
    print("No match Found")

# مرحله ۴: برش کلیپ‌ها
os.makedirs(OUTPUT_DIR, exist_ok=True)
clip = VideoFileClip(VIDEO_FILE)

print("Cutting clips...")
for i, seg in enumerate(matched_segments):
    subclip = clip.subclipped(seg['start'], seg['end'])
    out_file = os.path.join(OUTPUT_DIR, f"{i+1}_{seg['keyword']}.mp4")
    subclip.write_videofile(out_file, codec="libx264", audio_codec="aac")

print("✅ Done!")
