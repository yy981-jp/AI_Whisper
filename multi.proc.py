mp3_files = list(input_dir.glob("*.mp3"))

for mp3Input in mp3_files:
    transcribe_audio(mp3Input)