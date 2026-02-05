import os
import subprocess

OUT_DIR = "data/ai"
os.makedirs(OUT_DIR, exist_ok=True)

voices = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-IN-NeerjaNeural",
    "en-IN-PrabhatNeural",
    "en-GB-LibbyNeural",
    "en-AU-NatashaNeural"
]

# Read sentences from file
with open("sentences.txt", "r", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]

count = 1

for voice in voices:
    for text in sentences:
        out_mp3 = os.path.join(OUT_DIR, f"ai_{count:04d}.mp3")

        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", out_mp3
        ]

        subprocess.run(cmd, check=True)
        print(f"Generated {out_mp3}")

        count += 1

print(f"\n✅ Done. Generated {count-1} AI voice samples.")
