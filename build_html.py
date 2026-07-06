#!/usr/bin/env python3
"""生成意大利语美发实用手册 - 交互式HTML页面 (完整版)
Features: 左侧栏导航(桌面) + 汉堡菜单(手机) + hasAudio智能播放按钮 + CSS国旗 + 场景对话
"""
import json

with open(r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

sections_js = json.dumps(data["sections"], ensure_ascii=False)
all_entries_js = json.dumps(data["all_entries"], ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>意大利语美发实用手册 · Parrucchiere Italiano</title>
<style>
  :root {
    --bg: #f5f6f8; --surface: #ffffff; --surface2: #eef0f3; --border: #dde0e4;
    --text: #161a1f; --text-dim: #4b5563; --text-faint: #8b95a5;
    --green: #1a7f37; --green-l: #e6f4ea; --blue: #0550ae; --blue-l: #e3edfc;
    --gold: #855f1c; --gold-l: #fef3e2; --purple: #6f42c1; --purple-l: #f0eaff;
    --teal: #0e7c7b; --teal-l: #e1f3f3; --red: #cf222e; --red-l: #ffe7e7;
    --shadow-sm: 0 1px 3px rgba(0,0,0,.06); --shadow-lg: 0 8px 32px rgba(0,0,0,.1);
    --radius-sm: 6px;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    --nav-h: 56px; --tab-h: 48px; --sidebar-w: 200px;
  }
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body { background: var(--bg); color: var(--text); font-family: var(--font); min-height: 100vh; line-height: 1.6; -webkit-font-smoothing: antialiased; padding-top: var(--nav-h); }

  .flag-it { display:inline-block; width:28px; height:19px; background:linear-gradient(90deg,#009246 0%,#009246 33.33%,#fff 33.33%,#fff 66.66%,#ce2b37 66.66%,#ce2b37 100%); border-radius:2px; box-shadow:0 1px 3px rgba(0,0,0,.18); vertical-align:middle; flex-shrink:0; }
  .flag-it-sm { width:20px; height:14px; }

  .top-bar { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: var(--surface); border-bottom: 1px solid var(--border); box-shadow: var(--shadow-sm); }
  .top-bar-inner { display: flex; align-items: center; gap: 12px; padding: 0 16px; height: var(--nav-h); max-width: 1200px; margin: 0 auto; }
  .top-bar .logo { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 15px; white-space: nowrap; color: var(--text); }
  .search-wrap { flex: 1; position: relative; max-width: 400px; }
  .search-wrap input { width: 100%; padding: 8px 12px 8px 36px; border: 1px solid var(--border); border-radius: 20px; font-size: 14px; background: var(--bg); color: var(--text); outline: none; transition: all .2s; }
  .search-wrap input:focus { border-color: var(--blue); background: var(--surface); box-shadow: 0 0 0 3px var(--blue-l); }
  .search-wrap .search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-faint); font-size: 14px; }
  .search-wrap .clear-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-faint); cursor: pointer; padding: 2px 6px; border-radius: 50%; font-size: 16px; display: none; }
  .search-wrap .clear-btn.show { display: block; }
  .search-wrap .clear-btn:hover { background: var(--surface2); }

  .layout-wrap { display: flex; min-height: calc(100vh - var(--nav-h)); }
  .tab-bar { width: var(--sidebar-w); flex-shrink: 0; background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 8px 0; }
  .tab-bar::-webkit-scrollbar { width: 4px; }
  .tab-bar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
  .tab-bar-inner { display: flex; flex-direction: column; gap: 2px; padding: 0 6px; }
  .tab-btn { display: flex; align-items: center; gap: 8px; padding: 10px 12px; border: none; background: none; font-size: 13px; font-weight: 500; color: var(--text-dim); cursor: pointer; border-radius: var(--radius-sm); text-align: left; transition: all .15s; font-family: var(--font); white-space: nowrap; }
  .tab-btn:hover { background: var(--surface2); color: var(--text); }
  .tab-btn.active { color: var(--blue); background: var(--blue-l); font-weight: 600; }
  .tab-btn .tab-label { overflow: hidden; text-overflow: ellipsis; }
  .nav-toggle { display: none; }
  .nav-dropdown { display: none; }
  .nav-overlay { display: none; }

  .main { flex: 1; max-width: 960px; padding: 24px 24px 80px; margin: 0 auto; }
  .section-title { font-size: 22px; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 10px; }
  .section-desc { color: var(--text-dim); font-size: 14px; margin-bottom: 24px; }
  .subsection-title { font-size: 17px; font-weight: 600; margin: 28px 0 14px; padding: 10px 16px; background: var(--surface2); border-radius: var(--radius-sm); border-left: 4px solid var(--blue); color: var(--text); position: sticky; top: var(--nav-h); z-index: 10; }

  .entry-card { display: flex; align-items: flex-start; gap: 10px; padding: 10px 14px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 6px; transition: all .15s; }
  .entry-card:hover { border-color: var(--blue); box-shadow: 0 0 0 1px var(--blue-l); }
  .entry-card .play-btn { flex-shrink: 0; width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--border); background: var(--bg); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 14px; color: var(--text-dim); transition: all .2s; }
  .entry-card .play-btn:hover { background: var(--blue); border-color: var(--blue); color: #fff; }
  .entry-card .play-btn.playing { background: var(--green); border-color: var(--green); color: #fff; animation: pulse 1s infinite; }
  @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.08); } }
  .entry-card .entry-body { flex: 1; min-width: 0; }
  .entry-card .entry-ita { font-size: 15px; font-weight: 600; color: var(--text); word-break: break-word; }
  .entry-card .entry-chn { font-size: 14px; color: var(--text-dim); margin-top: 2px; }
  .entry-card .entry-extra { font-size: 12px; color: var(--text-faint); margin-top: 3px; font-style: italic; }
  .entry-card .entry-role { display: inline-block; font-size: 12px; padding: 1px 8px; border-radius: 10px; background: var(--surface2); color: var(--text-faint); margin-bottom: 4px; }

  .dialog-group { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin-bottom: 16px; }
  .dialog-group .entry-card { border: none; border-radius: 0; margin-bottom: 0; border-bottom: 1px solid var(--border); }
  .dialog-group .entry-card:last-child { border-bottom: none; }

  .null-state { text-align: center; padding: 60px 20px; color: var(--text-faint); }
  .null-state .null-icon { font-size: 48px; margin-bottom: 12px; }
  .search-info { margin-bottom: 12px; font-size: 13px; color: var(--text-dim); }
  .audio-loading { display: none; position: fixed; bottom: 20px; right: 20px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 12px 18px; box-shadow: var(--shadow-lg); font-size: 13px; color: var(--text-dim); z-index: 200; }
  .audio-loading.show { display: block; }
  .footer { text-align: center; padding: 32px 16px; border-top: 1px solid var(--border); color: var(--text-faint); font-size: 13px; background: var(--surface); margin-top: 40px; }

  @media (max-width: 768px) {
    body { padding-top: calc(var(--nav-h) + var(--tab-h)); }
    .top-bar-inner { padding: 0 10px; gap: 8px; }
    .top-bar .logo { font-size: 13px; }
    .layout-wrap { display: block; min-height: auto; }
    .tab-bar { position: fixed; top: var(--nav-h); left: 0; right: 0; z-index: 99; width: auto; border-right: none; border-bottom: 1px solid var(--border); overflow-x: auto; overflow-y: hidden; padding: 0; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    .tab-bar::-webkit-scrollbar { display: none; }
    .tab-bar-inner { display: flex; flex-direction: row; height: var(--tab-h); padding: 0 8px; gap: 0; }
    .tab-btn { flex-shrink: 0; padding: 0 14px; height: 100%; border-radius: 0; text-align: center; white-space: nowrap; font-size: 12px; justify-content: center; }
    .tab-btn:hover { background: none; }
    .tab-btn.active { background: none; color: var(--blue); box-shadow: inset 0 -3px 0 var(--blue); }
    .nav-toggle { display: flex !important; position: fixed; top: var(--nav-h); left: 0; right: 0; z-index: 100; height: var(--tab-h); background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 12px; cursor: pointer; align-items: center; gap: 8px; user-select: none; -webkit-tap-highlight-color: transparent; }
    .nav-toggle .hamburger { display: flex; flex-direction: column; gap: 4px; padding: 4px; }
    .nav-toggle .hamburger span { display: block; width: 20px; height: 2px; background: var(--text-dim); border-radius: 2px; transition: all .3s; }
    .nav-toggle.open .hamburger span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
    .nav-toggle.open .hamburger span:nth-child(2) { opacity: 0; }
    .nav-toggle.open .hamburger span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
    .nav-toggle .nav-current { flex: 1; font-size: 14px; font-weight: 600; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .nav-toggle .nav-arrow { font-size: 12px; color: var(--text-faint); transition: transform .3s; }
    .nav-toggle.open .nav-arrow { transform: rotate(180deg); }
    .nav-overlay { display: none; position: fixed; top: calc(var(--nav-h) + var(--tab-h)); left: 0; right: 0; bottom: 0; background: rgba(0,0,0,.35); z-index: 98; opacity: 0; transition: opacity .25s; }
    .nav-overlay.show { display: block; opacity: 1; }
    .nav-dropdown { display: none; position: fixed; top: calc(var(--nav-h) + var(--tab-h)); left: 0; right: 0; max-height: 70vh; overflow-y: auto; background: var(--surface); border-bottom: 1px solid var(--border); box-shadow: var(--shadow-lg); z-index: 99; padding: 8px 0; opacity: 0; transform: translateY(-8px); transition: all .25s ease; }
    .nav-dropdown.show { display: block; opacity: 1; transform: translateY(0); }
    .nav-dropdown .nav-drop-btn { display: flex; align-items: center; gap: 10px; width: 100%; padding: 12px 18px; border: none; background: none; font-size: 14px; font-weight: 500; color: var(--text-dim); cursor: pointer; text-align: left; transition: all .12s; font-family: var(--font); -webkit-tap-highlight-color: transparent; }
    .nav-dropdown .nav-drop-btn:hover { background: var(--surface2); }
    .nav-dropdown .nav-drop-btn.active { color: var(--blue); background: var(--blue-l); font-weight: 600; }
    .nav-dropdown .nav-drop-btn .drop-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .nav-dropdown .nav-drop-btn .drop-label { flex: 1; }
    .nav-dropdown .nav-drop-btn .drop-check { font-size: 14px; color: var(--blue); opacity: 0; transition: opacity .15s; }
    .nav-dropdown .nav-drop-btn.active .drop-check { opacity: 1; }
    .main { max-width: 100%; padding: 14px 10px 80px; }
    .section-title { font-size: 19px; }
    .subsection-title { font-size: 15px; padding: 8px 12px; top: calc(var(--nav-h) + var(--tab-h)); }
    .entry-card { padding: 8px 10px; }
    .entry-card .entry-ita { font-size: 14px; }
    .entry-card .entry-chn { font-size: 13px; }
    .entry-card .play-btn { width: 28px; height: 28px; font-size: 12px; }
    .search-wrap { max-width: none; }
  }
  @media (max-width: 400px) {
    .top-bar .logo { font-size: 11px; }
    .tab-btn { padding: 0 8px; font-size: 11px; }
  }
</style>
</head>
<body>

<div class="top-bar">
  <div class="top-bar-inner">
    <div class="logo"><span class="flag-it"></span> 美发意大利语</div>
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="搜索意大利语或中文..." autocomplete="off">
      <button class="clear-btn" id="clearBtn">✕</button>
    </div>
  </div>
</div>

<div class="layout-wrap">
  <div class="tab-bar" id="tabBar"><div class="tab-bar-inner" id="tabBarInner"></div></div>
  <div class="nav-toggle" id="navToggle"><div class="hamburger"><span></span><span></span><span></span></div><span class="nav-current" id="navCurrent">加载中...</span><span class="nav-arrow">▾</span></div>
  <div class="nav-dropdown" id="navDropdown"></div>
  <div class="nav-overlay" id="navOverlay"></div>
  <div class="main" id="mainContent"></div>
</div>

<div class="footer">
  <p><span class="flag-it flag-it-sm"></span> <em>意大利语美发实用手册 · Manuale di Parrucchiere</em></p>
  <p style="margin-top:4px;font-size:12px;color:var(--text-faint);">面向意大利华人理发师 · 🔊 点击意大利语播放配音 · edge-tts 意大利男声</p>
</div>
<div class="audio-loading" id="audioLoading">⏳ 音频加载中...</div>

<script>
const SECTIONS = """ + sections_js + r""";
const ALL_ENTRIES = """ + all_entries_js + r""";

let activeSection = 0;
let searchQuery = '';
let currentAudio = null;
let currentBtn = null;
const audioCache = {};
const sectionColors = ['var(--green)','var(--blue)','var(--gold)','var(--purple)','var(--teal)','var(--red)','var(--green)','var(--blue)','var(--gold)','var(--purple)','var(--teal)'];

function escHtml(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function renderTitle(title) { return title.replace(/🇮🇹/g, '<span class="flag-it" style="width:22px;height:15px;display:inline-block;vertical-align:middle;"></span>'); }
function hasChinese(t) { for (let c of t) { if (c >= '\u4e00' && c <= '\u9fff') return true; } return false; }
function hasAudio(e) { return !hasChinese(e.ita) && e.ita.trim().length > 1; }

function renderTabs() {
  const c = document.getElementById('tabBarInner');
  c.innerHTML = '';
  SECTIONS.forEach((sec, i) => {
    if (i === 0) return;
    const btn = document.createElement('button');
    btn.className = 'tab-btn' + (activeSection === i ? ' active' : '');
    let label = sec.title.replace(/🇮🇹/g, '').trim();
    const m = label.match(/(第.+部分|附录)\s*[·•]?\s*(.*)/);
    if (m) label = (m[2] || m[1]).substring(0, 14);
    const ci = (i - 1) % sectionColors.length;
    btn.innerHTML = '<span class="drop-dot" style="background:' + sectionColors[ci] + ';width:8px;height:8px;border-radius:50%;flex-shrink:0;display:inline-block;"></span><span class="tab-label">' + escHtml(label) + '</span>';
    btn.dataset.idx = i;
    btn.addEventListener('click', () => switchSection(i));
    c.appendChild(btn);
  });
}

function switchSection(idx) {
  activeSection = idx;
  document.querySelectorAll('.tab-btn').forEach(b => { b.classList.toggle('active', parseInt(b.dataset.idx) === idx); });
  renderContent();
}

function renderContent() {
  const main = document.getElementById('mainContent');

  // Global search mode: show results from ALL sections
  if (searchQuery) {
    let html = '<div class="section-title">🔍 搜索结果</div>';
    let total = 0;
    SECTIONS.forEach(sec => {
      if (sec.title.startsWith('🇮🇹')) return; // skip overview
      let secMatches = 0;
      let secHtml = '';
      const subs = sec.subsections || [];
      subs.forEach(sub => {
        const ve = sub.entries.filter(e => matchesSearch(e));
        if (ve.length === 0) return;
        secMatches += ve.length;
        secHtml += '<div class="subsection-title">' + escHtml(sub.title) + ' <span style="font-weight:400;color:var(--text-faint);font-size:13px;">' + ve.length + '</span></div>';
        const isDialog = sub.title.includes('对话') || sub.title.includes('场景');
        if (isDialog) { secHtml += renderDialogEntries(ve); }
        else { secHtml += ve.map(e => renderEntry(e)).join(''); }
      });
      if (sec.entries && sec.entries.length > 0) {
        const v = sec.entries.filter(e => matchesSearch(e));
        if (v.length > 0) { secMatches += v.length; secHtml += v.map(e => renderEntry(e)).join(''); }
      }
      if (secMatches > 0) {
        total += secMatches;
        html += '<div class="subsection-title" style="margin-top:24px;font-size:18px;border-left-color:var(--purple);">' + renderTitle(sec.title) + ' <span style="font-weight:400;color:var(--text-faint);font-size:13px;">' + secMatches + ' 条</span></div>';
        html += secHtml;
      }
    });
    html = html.replace('<div class="section-title">🔍 搜索结果</div>', '<div class="section-title">🔍 搜索结果</div><div class="section-desc">关键词 "' + escHtml(searchQuery) + '" 共匹配 ' + total + ' 条</div>');
    if (total === 0) { html = '<div class="null-state"><div class="null-icon">🔍</div><p>没有找到匹配 "' + escHtml(searchQuery) + '" 的内容</p></div>'; }
    main.innerHTML = html;
    document.querySelectorAll('.play-btn[data-audio-id]').forEach(btn => { btn.addEventListener('click', function(e) { e.stopPropagation(); playAudio(this); }); });
    return;
  }

  // Normal mode: show current section
  const sec = SECTIONS[activeSection];
  if (!sec) { main.innerHTML = '<div class="null-state"><p>暂无内容</p></div>'; return; }
  let html = '<div class="section-title">' + renderTitle(sec.title) + '</div>';
  html += '<div class="section-desc">' + (sec.subsections.length + ' 个分类 · ' + countSectionEntries(sec) + ' 条内容') + '</div>';
  const subs = sec.subsections || [];
  subs.forEach(sub => {
    const ve = sub.entries.filter(e => matchesSearch(e));
    if (searchQuery && ve.length === 0) return;
    html += '<div class="subsection-title">' + escHtml(sub.title) + ' <span style="font-weight:400;color:var(--text-faint);font-size:13px;">' + ve.length + '</span></div>';
    const isDialog = sub.title.includes('对话') || sub.title.includes('场景');
    if (isDialog) { html += renderDialogEntries(ve); }
    else { ve.forEach(e => { html += renderEntry(e); }); }
  });
  if (sec.entries && sec.entries.length > 0) {
    const v = sec.entries.filter(e => matchesSearch(e));
    if (!searchQuery || v.length > 0) { v.forEach(e => { html += renderEntry(e); }); }
  }
  if (html.indexOf('entry-card') === -1) { html = '<div class="null-state"><div class="null-icon">🔍</div><p>没有找到匹配 "' + escHtml(searchQuery) + '" 的内容</p></div>'; }
  main.innerHTML = html;
  document.querySelectorAll('.play-btn[data-audio-id]').forEach(btn => { btn.addEventListener('click', function(e) { e.stopPropagation(); playAudio(this); }); });
}

function renderDialogEntries(entries) {
  let html = '<div class="dialog-group">';
  entries.forEach(e => {
    const role = e.extra && (e.extra.includes('👩') || e.extra.includes('✂️') || e.extra.includes('👨')) ? e.extra : '';
    const au = hasAudio(e);
    html += '<div class="entry-card">';
    if (au) html += '<button class="play-btn" data-audio-id="' + e.id + '">▶</button>';
    html += '<div class="entry-body">';
    if (role) html += '<div class="entry-role">' + escHtml(role) + '</div>';
    html += '<div class="entry-ita">' + escHtml(e.ita) + '</div>';
    html += '<div class="entry-chn">' + escHtml(e.chn) + '</div>';
    if (e.extra && !role) html += '<div class="entry-extra">' + escHtml(e.extra) + '</div>';
    html += '</div></div>';
  });
  html += '</div>';
  return html;
}

function renderEntry(e) {
  const role = e.extra && (e.extra.includes('👩') || e.extra.includes('✂️') || e.extra.includes('👨')) ? e.extra : '';
  const au = hasAudio(e);
  let html = '<div class="entry-card">';
  if (au) html += '<button class="play-btn" data-audio-id="' + e.id + '">▶</button>';
  html += '<div class="entry-body">';
  if (role) html += '<div class="entry-role">' + escHtml(role) + '</div>';
  html += '<div class="entry-ita">' + escHtml(e.ita) + '</div>';
  html += '<div class="entry-chn">' + escHtml(e.chn) + '</div>';
  if (e.extra && e.extra !== '—' && !role) html += '<div class="entry-extra">' + escHtml(e.extra) + '</div>';
  html += '</div></div>';
  return html;
}

function playAudio(btn) {
  const aid = btn.dataset.audioId;
  const entry = ALL_ENTRIES.find(e => e.id === aid);
  if (!entry) return;
  if (currentAudio && !currentAudio.paused) {
    if (currentAudio.dataset.audioId === aid) { currentAudio.pause(); currentAudio.currentTime = 0; if (currentBtn) { currentBtn.textContent = '▶'; currentBtn.classList.remove('playing'); } currentAudio = null; currentBtn = null; return; }
    currentAudio.pause(); currentAudio.currentTime = 0;
    if (currentBtn) { currentBtn.textContent = '▶'; currentBtn.classList.remove('playing'); }
  }
  const ap = 'audio/' + aid + '.mp3?v=' + Date.now();
  if (!audioCache[aid]) {
    const a = new Audio(ap);
    a.dataset.audioId = aid; a.preload = 'none';
    a.addEventListener('ended', function() { if (currentBtn) { currentBtn.textContent = '▶'; currentBtn.classList.remove('playing'); } currentAudio = null; currentBtn = null; });
    a.addEventListener('error', function() { btn.textContent = '⚠'; btn.style.color = 'var(--red)'; setTimeout(() => { btn.textContent = '▶'; btn.style.color = ''; }, 2000); if (currentBtn) { currentBtn.textContent = '▶'; currentBtn.classList.remove('playing'); } currentAudio = null; currentBtn = null; });
    audioCache[aid] = a;
  }
  const a = audioCache[aid]; a.currentTime = 0;
  a.play().then(() => { btn.textContent = '⏸'; btn.classList.add('playing'); currentAudio = a; currentBtn = btn; }).catch(err => {});
}

function matchesSearch(e) { if (!searchQuery) return true; const q = searchQuery.toLowerCase(); return e.ita.toLowerCase().includes(q) || e.chn.toLowerCase().includes(q) || (e.extra && e.extra.toLowerCase().includes(q)); }
function countSectionEntries(sec) { let c = 0; (sec.subsections || []).forEach(s => { c += s.entries.length; }); c += (sec.entries || []).length; return c; }
function countVisibleEntries(sec) { let c = 0; (sec.subsections || []).forEach(s => { s.entries.forEach(e => { if (matchesSearch(e)) c++; }); }); (sec.entries || []).forEach(e => { if (matchesSearch(e)) c++; }); return c; }

// Mobile Nav
const navToggle = document.getElementById('navToggle');
const navDropdown = document.getElementById('navDropdown');
const navOverlay = document.getElementById('navOverlay');
const navCurrent = document.getElementById('navCurrent');
let navOpen = false;
const sectionLabels = [];

function buildNavLabels() {
  sectionLabels.length = 0;
  SECTIONS.forEach((sec, i) => {
    if (i === 0) { sectionLabels.push(''); return; }
    let label = sec.title.replace(/🇮🇹/g, '').trim();
    const m = label.match(/(第.+部分|附录)\s*[·•]?\s*(.*)/);
    if (m) label = (m[2] || m[1]).substring(0, 14); else label = label.substring(0, 14);
    sectionLabels.push(label);
  });
}

function renderNavDropdown() {
  if (!navDropdown) return;
  navDropdown.innerHTML = '';
  SECTIONS.forEach((sec, i) => {
    if (i === 0) return;
    const label = sectionLabels[i] || '';
    const btn = document.createElement('button');
    btn.className = 'nav-drop-btn' + (activeSection === i ? ' active' : '');
    const ci = (i - 1) % sectionColors.length;
    btn.innerHTML = '<span class="drop-dot" style="background:' + sectionColors[ci] + '"></span><span class="drop-label">' + escHtml(label) + '</span><span class="drop-check">✓</span>';
    btn.addEventListener('click', function() { switchSection(i); closeNav(); });
    navDropdown.appendChild(btn);
  });
}

function closeNav() { navOpen = false; if (navToggle) navToggle.classList.remove('open'); if (navDropdown) navDropdown.classList.remove('show'); if (navOverlay) navOverlay.classList.remove('show'); document.body.style.overflow = ''; }
function toggleNav() { navOpen = !navOpen; if (navToggle) navToggle.classList.toggle('open', navOpen); if (navDropdown) navDropdown.classList.toggle('show', navOpen); if (navOverlay) navOverlay.classList.toggle('show', navOpen); document.body.style.overflow = navOpen ? 'hidden' : ''; }
function updateNavCurrent() { if (navCurrent) navCurrent.textContent = sectionLabels[activeSection] || '选择分类'; }

const _origSwitch = switchSection;
switchSection = function(idx) {
  _origSwitch(idx);
  updateNavCurrent();
  window.scrollTo(0, 0);
  if (navDropdown && navDropdown.children.length > 0) { navDropdown.querySelectorAll('.nav-drop-btn').forEach((b, i) => { b.classList.toggle('active', (i + 1) === idx); }); }
};

if (navToggle) navToggle.addEventListener('click', toggleNav);
if (navOverlay) navOverlay.addEventListener('click', closeNav);

// Search
const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearBtn');
searchInput.addEventListener('input', function() { searchQuery = this.value.trim(); clearBtn.classList.toggle('show', searchQuery.length > 0); renderContent(); });
clearBtn.addEventListener('click', function() { searchInput.value = ''; searchQuery = ''; clearBtn.classList.remove('show'); renderContent(); searchInput.focus(); });
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'f') { e.preventDefault(); searchInput.focus(); }
  if (e.key === 'Escape' && navOpen) closeNav();
});

// Init
buildNavLabels();
renderTabs();
renderNavDropdown();
switchSection(1);
</script>
</body>
</html>"""

output_path = r"D:\workbuddy工作区\2026-07-06-15-50-44\parrucchiere-italiano\index.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML generated: {output_path}")
print(f"File size: {len(html)} chars")
print(f"Sections: {len(data['sections'])}")
print(f"Total entries: {len(data['all_entries'])}")
