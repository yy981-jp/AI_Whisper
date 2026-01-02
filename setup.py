!pip install faster-whisper
import os
import multiprocessing
from faster_whisper import WhisperModel
from pathlib import Path

input_dir = Path("/content/input")
output_dir = Path("/content/output")
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
# model = WhisperModel("small", device="cuda", compute_type="float16")

def transcribe_audio(mp3_path):
    print(f"Transcribing {mp3_path.name}...")

    segments, info = model.transcribe(
        str(mp3_path),
        language="ja",      # ← 日本語指定
        task="transcribe"   # 念のため（翻訳じゃなく文字起こし）
    )

    out_csv = output_dir / (mp3_path.stem + ".csv")

    total_duration = info.duration

    with open(out_csv, "w", encoding="utf-8") as f:
        for seg in segments:
            ms = int(seg.start * 1000)
            f.write(f"{ms},{seg.text.strip()}\n")
            progress = (seg.end / total_duration) * 100
            print(f"{mp3_path.name}: {progress:.2f}%")

    print(f"Finished transcribing {mp3_path.name}. Output saved to {out_csv}")
