import os
import shutil

CSV_DIR = "csv"
AUDIO_DIR = "audio/mono"
COMPLETED_DIR = os.path.join(AUDIO_DIR, "completed")

# csv にある basename をセットで持つ
csv_basenames = {
    os.path.splitext(f)[0]
    for f in os.listdir(CSV_DIR)
    if f.lower().endswith(".csv")
}

# completed 内の opus をチェック
for fname in os.listdir(COMPLETED_DIR):
    if not fname.lower().endswith(".opus"):
        continue

    base = os.path.splitext(fname)[0]

    # csv が存在するなら放置
    if base in csv_basenames:
        continue

    # なければ audio/mono に戻す
    src = os.path.join(COMPLETED_DIR, fname)
    dst = os.path.join(AUDIO_DIR, fname)

    if os.path.exists(dst):
        print(f"skip (already exists): {dst}")
        continue

    shutil.move(src, dst)
    print(f"moved: {src} -> {dst}")
