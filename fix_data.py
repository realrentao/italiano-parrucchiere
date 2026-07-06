#!/usr/bin/env python3
"""
修复第八部分对话数据 + 补全缺少的音频 + 处理第十部分
"""
import re, json, os, base64, asyncio, hashlib

MD_PATH = r"C:\Users\迪丽希斯\OneDrive\Desktop\🇮🇹 意大利语美发实用手册.md"
DATA_PATH = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\data.json"
AUDIO_DIR = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\audio"
VOICE = "it-IT-DiegoNeural"

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── Part 1: Fix dialog data by re-reading markdown ──
with open(MD_PATH, 'r', encoding='utf-8') as f:
    md = f.read()

# Find all dialog scenes in Part 8
part8_start = md.find("## 场景一")
part9_start = md.find("# 第九部分")
dialog_text = md[part8_start:part9_start]

# Parse each scene
scene_pattern = re.compile(r'^## (场景[^：]+[：]?\s*[^(\n]*)\n\n((?:\|.+\|\n?)+)', re.MULTILINE)

new_dialog_entries = []
scene_id_counter = 0

for m in scene_pattern.finditer(dialog_text):
    scene_title = m.group(1).strip()
    table_text = m.group(2)
    
    # Parse table rows
    lines = table_text.strip().split('\n')
    header_line = None
    data_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) < 2:
            continue
        # Check if this is a header (contains *)
        if any('**' in c for c in cells):
            header_line = cells
            continue
        data_lines.append(cells)
    
    # Process rows based on column count
    for cells in data_lines:
        if len(cells) >= 4:
            # Format: 轮次 | 角色 | 意大利语 | 中文
            role = cells[1]
            ita = cells[2]
            chn = cells[3]
        elif len(cells) >= 3:
            # Format: 角色 | 意大利语 | 中文
            role = cells[0]
            ita = cells[1]
            chn = cells[2]
        else:
            continue
        
        # Clean up
        ita = ita.strip()
        chn = chn.strip()
        role = role.strip()
        
        if not ita or ita == '🗣️ 意大利语':
            continue
        
        # Skip if no actual Italian text
        if not ita or len(ita) < 2:
            continue
        
        new_dialog_entries.append({
            "ita": ita,
            "chn": chn,
            "extra": role,
            "scene": scene_title
        })

print(f"从Markdown提取了 {len(new_dialog_entries)} 条对话条目")

# ── Part 2: Fix data.json Part 8 ──
sections = data["sections"]
part8_idx = None
for i, sec in enumerate(sections):
    if "第八" in sec["title"]:
        part8_idx = i
        break

if part8_idx is not None:
    # Group entries by scene
    scene_groups = {}
    for e in new_dialog_entries:
        scene = e["scene"]
        if scene not in scene_groups:
            scene_groups[scene] = []
        scene_groups[scene].append(e)
    
    # Update subsections in Part 8
    scene_keys = list(scene_groups.keys())
    for si, sub in enumerate(sections[part8_idx]["subsections"]):
        if si < len(scene_keys):
            scene_name = scene_keys[si]
            entries = scene_groups[scene_name]
            # Assign IDs
            for ei, entry in enumerate(entries):
                # Create deterministic ID based on content
                h = hashlib.md5(entry["ita"].encode()).hexdigest()[:8]
                entry["id"] = f"audio_d{h}"
                entry["section"] = sections[part8_idx]["title"]
                entry["subsection"] = sub["title"]
            sub["entries"] = entries
            print(f"  更新 {sub['title']}: {len(entries)} 条")

# ── Part 3: Collect all Italian text entries needing audio ──
print("\n收集需要配音的条目...")
audio_tasks = []
processed_texts = set()

for sec in sections:
    for sub in sec.get("subsections", []):
        for e in sub.get("entries", []):
            ita = e.get("ita", "").strip()
            if not ita:
                continue
            # Skip Chinese-only text
            has_chinese = any('\u4e00' <= c <= '\u9fff' for c in ita)
            if has_chinese:
                continue
            # Skip emoji-only
            if re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩—\-​✂️👩👨\U0001F9B0\U0001F484\s]+$', ita):
                continue
            # Skip very short symbols
            if len(ita) < 2:
                continue
            
            # Check if audio exists
            aid = e.get("id", "")
            if not aid:
                # Generate new ID
                h = hashlib.md5(ita.encode()).hexdigest()[:8]
                aid = f"audio_h{h}"
                e["id"] = aid
            
            audio_path = os.path.join(AUDIO_DIR, f"{aid}.mp3")
            if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 200:
                if ita not in processed_texts:
                    audio_tasks.append((aid, ita))
                    processed_texts.add(ita)

print(f"需要生成音频: {len(audio_tasks)} 条")

# ── Part 4: Generate audio ──
if audio_tasks:
    async def generate():
        from edge_tts import Communicate
        sem = asyncio.Semaphore(6)
        
        async def gen_one(aid, text):
            async with sem:
                out = os.path.join(AUDIO_DIR, f"{aid}.mp3")
                try:
                    c = Communicate(text, VOICE)
                    await c.save(out)
                    if os.path.exists(out) and os.path.getsize(out) > 200:
                        return f"OK {aid}: {text[:30]}"
                    else:
                        return f"FAIL {aid}: {text[:30]}"
                except Exception as ex:
                    return f"ERROR {aid}: {ex}"
        
        tasks = [gen_one(aid, text) for aid, text in audio_tasks]
        for i in range(0, len(tasks), 6):
            batch = tasks[i:i+6]
            results = await asyncio.gather(*batch)
            for r in results:
                print(f"  {r}")
    
    asyncio.run(generate())

# ── Part 5: Save updated data ──
# Also fix Part 10 entries: remove audio for Chinese-only text
for sec in sections:
    if "第十" in sec["title"] and "文化" in sec["title"]:
        for sub in sec.get("subsections", []):
            for e in sub.get("entries", []):
                ita = e.get("ita", "").strip()
                has_chinese = any('\u4e00' <= c <= '\u9fff' for c in ita)
                if has_chinese or not ita:
                    # Chinese-only entries - don't remove ID but ensure no audio
                    pass

# Add entries that don't have IDs
# Re-collect ALL entries for all_entries
all_entries = []
seen_itas = set()
for sec in sections:
    for sub in sec.get("subsections", []):
        for e in sub.get("entries", []):
            ita = e.get("ita", "").strip()
            if ita and ita not in seen_itas:
                seen_itas.add(ita)
                all_entries.append(e)

data["all_entries"] = all_entries

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存: {DATA_PATH}")
print(f"总条目: {len(all_entries)}")
