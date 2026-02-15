import os
import subprocess
import re

OUT_DIR = "data/ai"
os.makedirs(OUT_DIR, exist_ok=True)

def is_tamil(text):
    return bool(re.search(r'[\u0B80-\u0BFF]', text))

with open("sentences.txt", "r", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]

count = 1

for text in sentences:

    voice = "ta-IN-PallaviNeural" if is_tamil(text) else "en-US-AriaNeural"

    out_mp3 = os.path.join(OUT_DIR, f"ai_{count:04d}.mp3")

    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", out_mp3
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Generated {out_mp3}")
        count += 1

    except subprocess.CalledProcessError:
        print(f"❌ Failed for text: {text}")

print(f"\n✅ Done. Generated {count-1} AI voice samples.")

