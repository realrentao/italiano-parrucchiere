#!/usr/bin/env python3
"""
解析意大利语美发手册 Markdown → 结构化JSON数据
"""
import re, json

md_path = r"C:\Users\迪丽希斯\OneDrive\Desktop\🇮🇹 意大利语美发实用手册.md"
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ── 数据结构 ──
sections = []
current_section = None
current_subsection = None
is_table = False
table_headers = []
table_rows = []
table_mode = None  # 'normal' | 'dialog' | 'phrase'

def add_entry(ita, chn, extra=""):
    entry = {"ita": ita.strip(), "chn": chn.strip()}
    if extra.strip():
        entry["extra"] = extra.strip()
    if current_subsection:
        entry["subsection"] = current_subsection
    if current_section:
        entry["section"] = current_section
    return entry

def end_table():
    global is_table, table_headers, table_rows
    if table_rows:
        entries = []
        for row in table_rows:
            if len(row) >= 2:
                ita = row[0].strip()
                chn = row[1].strip()
                extra = row[2].strip() if len(row) >= 3 else ""
                if ita and ita != '-':
                    entries.append(add_entry(ita, chn, extra))
        if entries:
            if current_subsection:
                sections[-1]["subsections"][-1]["entries"].extend(entries)
            elif current_section:
                sections[-1]["entries"].extend(entries)
    table_rows = []
    table_headers = []
    is_table = False

i = 0
while i < len(lines):
    line = lines[i].rstrip()

    # ── 一级标题（第X部分）──
    m1 = re.match(r'^#\s+(第.+部分|附录)\s*[·•]?\s*(.*)', line)
    if not m1:
        m1 = re.match(r'^#\s+(.+?美发)', line)
    if m1:
        end_table()
        sec_title = m1.group(1).strip()
        sec_sub = m1.group(2).strip() if len(m1.groups()) > 1 else ""
        full_title = sec_title
        if sec_sub:
            full_title += " · " + sec_sub
        current_section = full_title
        sections.append({"title": full_title, "subsections": [], "entries": []})
        current_subsection = None
        i += 1
        continue

    # ── 二级标题（##）──
    m2 = re.match(r'^##\s+(.*)', line)
    if m2 and current_section:
        end_table()
        sub_title = m2.group(1).strip()
        current_subsection = sub_title
        sections[-1]["subsections"].append({"title": sub_title, "entries": []})
        i += 1
        continue

    # ── 表格分隔行（|---|---|）──
    if re.match(r'^\s*\|[\s\-|]+\|\s*$', line):
        i += 1
        continue

    # ── 表头行（| **意大利语** | **中文** |）──
    if re.match(r'^\s*\|.*\*\*.*\*\*.*\|', line):
        if current_section:
            end_table()
            is_table = True
            headers = [h.strip().strip('*') for h in line.split('|') if h.strip()]
            table_headers = headers
        i += 1
        continue

    # ── 表格行 ──
    if is_table and line.startswith('|') and line.endswith('|'):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 2 and cells[0] and cells[0] != '-':
            table_rows.append(cells)
        i += 1
        continue

    # ── 角色对话行（| 👩 | ... | ... |）──
    if line.startswith('|') and '🗣️' in line:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            role = cells[0] if 'emoji' in cells[0] or '👩' in cells[0] or '✂️' in cells[0] or '👨' in cells[0] else ""
            ita = ""
            chn = ""
            for c in cells:
                if '🗣️' in c:
                    ita = c.replace('🗣️', '').strip()
                elif '📝' in c:
                    chn = c.replace('📝', '').strip()
            if ita and chn:
                entry = add_entry(ita, chn, role)
                if current_subsection:
                    sections[-1]["subsections"][-1]["entries"].append(entry)
                elif current_section:
                    sections[-1]["entries"].append(entry)
        i += 1
        continue

    # ── 轮次/角色类（| ① | 👩 | ... |）──
    if is_table and line.startswith('|') and re.match(r'^\|\s*[①②③④⑤⑥⑦⑧⑨⑩]', line):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 4:
            ita = cells[2].strip() if len(cells) > 2 else ""
            chn = cells[3].strip() if len(cells) > 3 else ""
            if ita and chn:
                table_rows.append([ita, chn, cells[1] if len(cells) > 1 else ""])
        elif len(cells) >= 3:
            ita = cells[1].strip() if len(cells) > 1 else ""
            chn = cells[2].strip() if len(cells) > 2 else ""
            if ita and chn:
                table_rows.append([ita, chn, ""])
        i += 1
        continue

    # ── 普通表格行 ──
    if is_table and line.startswith('|'):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 2:
            table_rows.append(cells)
        i += 1
        continue

    i += 1

end_table()

# ── 生成 audio manifest ──
all_entries = []
seen = set()
for sec in sections:
    for sub in sec.get("subsections", []):
        for e in sub["entries"]:
            key = e["ita"][:30]
            if key not in seen:
                seen.add(key)
                all_entries.append(e)
    for e in sec.get("entries", []):
        key = e["ita"][:30]
        if key not in seen:
            seen.add(key)
            all_entries.append(e)

print(f"Total sections: {len(sections)}")
print(f"Total entries: {len(all_entries)}")

# 为每个条目分配ID
for idx, e in enumerate(all_entries):
    e["id"] = f"audio_{idx:04d}"

# 输出JSON
output = {
    "sections": sections,
    "all_entries": all_entries
}

json_path = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\data.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Data saved to: {json_path}")
print(f"Audio files needed: {len(all_entries)}")
