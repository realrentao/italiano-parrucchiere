#!/usr/bin/env python3
"""
批量生成意大利语音频 - edge-tts DiegoNeural 男声
使用 Python API 而非 CLI 以避免子进程问题
"""
import asyncio
import json
import os
import time

AUDIO_DIR = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\audio"
DATA_PATH = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\data.json"
VOICE = "it-IT-DiegoNeural"
BATCH_SIZE = 6  # 并行数量
RATE_LIMIT_DELAY = 0.3  # 批次间隔

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data["all_entries"]
print(f"Total entries: {len(entries)}")

# 检测是否包含中文字符
def has_chinese(text):
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

async def generate_one(entry, semaphore):
    audio_id = entry["id"]
    text = entry["ita"]
    out_path = os.path.join(AUDIO_DIR, f"{audio_id}.mp3")
    
    # 跳过纯中文条目（目录行等）
    if has_chinese(text):
        return f"SKIP {audio_id}: non-Italian text"
    
    async with semaphore:
        # 跳过已存在的文件
        if os.path.exists(out_path) and os.path.getsize(out_path) > 200:
            return f"SKIP {audio_id}: {text}"

        try:
            from edge_tts import Communicate
            communicate = Communicate(text, VOICE)
            await communicate.save(out_path)
            
            if os.path.exists(out_path) and os.path.getsize(out_path) > 200:
                size = os.path.getsize(out_path)
                return f"OK {audio_id} ({size}B): {text}"
            else:
                return f"FAIL {audio_id}: file too small or missing"
        except Exception as ex:
            return f"ERROR {audio_id}: {ex}"

async def main():
    semaphore = asyncio.Semaphore(BATCH_SIZE)
    total = len(entries)
    completed = 0
    start_time = time.time()
    
    for i in range(0, total, BATCH_SIZE):
        batch = entries[i:i+BATCH_SIZE]
        tasks = [generate_one(e, semaphore) for e in batch]
        results = await asyncio.gather(*tasks)
        
        for r in results:
            print(r)
        
        completed += len(batch)
        elapsed = time.time() - start_time
        rate = completed / elapsed if elapsed > 0 else 0
        pct = completed / total * 100
        eta = (total - completed) / rate if rate > 0 else 0
        print(f"Progress: {completed}/{total} ({pct:.1f}%) | {rate:.1f} items/s | ETA: {eta:.0f}s\n")
        
        await asyncio.sleep(RATE_LIMIT_DELAY)

    # Count actual files
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3') and os.path.getsize(os.path.join(AUDIO_DIR, f)) > 200]
    print(f"\n=== DONE ===")
    print(f"Valid audio files: {len(audio_files)}/{total}")

if __name__ == "__main__":
    asyncio.run(main())
