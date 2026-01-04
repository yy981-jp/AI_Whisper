import os
import shutil

CSV_DIR = "csv"
AUDIO_DIR = "audio/mono"
COMPLETED_DIR = os.path.join(AUDIO_DIR, "completed")

os.makedirs(COMPLETED_DIR, exist_ok=True)

# csvのファイル名（拡張子なし）を集める
csv_basenames = set()
for name in os.listdir(CSV_DIR):
	if name.lower().endswith(".csv"):
		csv_basenames.add(os.path.splitext(name)[0])

# audio以下を再帰的に探索
for root, dirs, files in os.walk(AUDIO_DIR):
	# completed 自身は対象外にする
	if os.path.abspath(root) == os.path.abspath(COMPLETED_DIR):
		continue

	for file in files:
		if not file.lower().endswith(".opus"):
			continue

		base, _ = os.path.splitext(file)
		if base in csv_basenames:
			src = os.path.join(root, file)
			dst = os.path.join(COMPLETED_DIR, file)

			# 同名ファイルが already ある場合はスキップ
			if os.path.exists(dst):
				print(f"skip (already exists): {file}")
				continue

			shutil.move(src, dst)
			print(f"moved: {src} -> {dst}")
