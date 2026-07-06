import json
with open(r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\data.json", encoding='utf-8') as f:
    data = json.load(f)
entries = data["all_entries"]

# Check failed entries
print("=== Failed entries ===")
for i in range(446, 452):
    e = entries[i]
    print(f"{e['id']}: ita='{e['ita']}' chn='{e['chn']}'")

print("\n=== Emoji entries ===")
for i in range(630, 632):
    e = entries[i]
    print(f"{e['id']}: ita='{e['ita']}' chn='{e['chn']}'")

# Count audio files
import os
audio_dir = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\audio"
files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3') and os.path.getsize(os.path.join(audio_dir, f)) > 200]
print(f"\nValid audio files: {len(files)}")

# List missing files
missing = []
for e in entries:
    if e['ita'] and any(ord(c) > 0x4e00 for c in e['ita']):
        continue  # skip Chinese-only
    aid = e['id']
    fpath = os.path.join(audio_dir, f"{aid}.mp3")
    if not os.path.exists(fpath) or os.path.getsize(fpath) < 200:
        missing.append(f"{aid}: '{e['ita']}'")
        
print(f"\nMissing important audio ({len(missing)}):")
for m in missing[:20]:
    print(f"  {m}")
if len(missing) > 20:
    print(f"  ... and {len(missing)-20} more")
