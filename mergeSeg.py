from pathlib import Path
from collections import defaultdict

SEGMENT_SEC = 7200  # 2時間
INPUT_DIR = Path(".")
OUTPUT_DIR = Path("all")

OUTPUT_DIR.mkdir(exist_ok=True)

groups = defaultdict(list)

# 再帰的に *_NN.csv を収集
for csv_path in INPUT_DIR.rglob("*_*.csv"):
	stem = csv_path.stem
	if "_" not in stem:
		continue

	base, idx = stem.rsplit("_", 1)
	if not idx.isdigit():
		continue

	groups[base].append(csv_path)

for base, files in groups.items():
	files.sort(key=lambda p: int(p.stem.rsplit("_", 1)[1]))
	output_path = OUTPUT_DIR / f"{base}.csv"

	with output_path.open("w", encoding="utf-8", newline="") as out:
		for csv_path in files:
			index = int(csv_path.stem.rsplit("_", 1)[1])
			offset_ms = index * SEGMENT_SEC * 1000

			with csv_path.open(encoding="utf-8") as f:
				for line in f:
					line = line.rstrip("\n")
					if not line:
						continue

					pos = line.find(",")
					if pos == -1:
						continue

					ms = line[:pos]
					if not ms.isdigit():
						continue

					text = line[pos+1:]
					out.write(f"{int(ms) + offset_ms},{text}\n")

	print(f"merged: {output_path}")
