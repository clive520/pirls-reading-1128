# -*- coding: utf-8 -*-
"""
=============================================================================
PIRLS 閱讀理解簡報 - 零依賴模組化構建工具 (Build Tool)
=============================================================================
功能說明：
  1. 將 src/slides/ 下的各頁投影片小檔案，自動拼裝成根目錄的 index.html
  2. 將 src/script-sections/ 下的逐字稿小檔案，自動拼裝成根目錄的 script.html
  3. 自動同步更新頁碼、目錄跳轉彈窗 (Agenda Modal) 與快速跳轉列 (Quick Jump)
  4. 支援 --watch 存檔自動監控重構，以及 --sync 自動同步至雙雲端硬碟

使用方式：
  python build.py          # 單次構建 index.html 與 script.html
  python build.py --watch  # 監控 src/ 變更，存檔即刻自動重構
  python build.py --sync   # 構建完成後自動複製至 G 槽與 H 槽共用雲端硬碟
=============================================================================
"""

import os
import sys
import re
import glob
import time
import shutil

# 終端機 UTF-8 輸出防亂碼相容
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

DRIVE_TARGETS = [
    r"G:\共用雲端硬碟\志賢個人資料\Antigravity\1128閱讀簡報",
    r"H:\共用雲端硬碟\志賢個人資料\Antigravity\1128閱讀簡報"
]

# 自訂每頁在目錄彈窗 (Agenda) 與快捷列中的精簡標題（若無則自動由 h2 提煉，極具擴充性）
CUSTOM_TITLES = {
    1: "首頁：閱讀理解策略與 AI 的結合",
    2: "講師經歷：高志賢老師簡介",
    3: "個人獲獎：教育部教學大獎肯定",
    4: "數據指標：臺灣 PIRLS 成績與趨勢洞察",
}

CUSTOM_SCRIPT_PILLS = {
    1: "01 封面開場",
    2: "02 講師經歷",
    3: "03 個人獲獎",
    4: "04 PIRLS 國際成績",
}

def clean_tag(text):
    """去除 HTML 標籤"""
    return re.sub(r'<[^>]+>', '', text).strip()

def build_index():
    """構建 index.html"""
    tpl_path = os.path.join(SRC_DIR, 'templates', 'index.html.template')
    with open(tpl_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 組合 CSS
    css_files = ['style.css', 'spotlight.css']
    combined_css = []
    for cfile in css_files:
        cpath = os.path.join(SRC_DIR, 'css', cfile)
        if os.path.exists(cpath):
            with open(cpath, 'r', encoding='utf-8') as f:
                combined_css.append(f"/* ====== {cfile} ====== */\n" + f.read())
    css_content = '\n\n'.join(combined_css)

    # 2. 讀取 JS
    js_path = os.path.join(SRC_DIR, 'js', 'presentation.js')
    js_content = ''
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()

    # 3. 讀取所有 slides
    slide_files = sorted(glob.glob(os.path.join(SRC_DIR, 'slides', '*.html')))
    slides_html_list = []
    jump_items = []

    for idx, sfile in enumerate(slide_files, start=1):
        with open(sfile, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # 自動校準 data-slide 屬性與 active class
        # 移除舊有的 active 或 prev class
        content = re.sub(r'<section\s+class="slide([^"]*)"\s+data-slide="\d+"',
                         r'<section class="slide\1"', content)
        
        # 規範化 section 開頭
        if idx == 1:
            # 第一頁加上 active
            content = re.sub(r'<section\s+class="slide(?:\s+active)?([^"]*)"',
                             f'<section class="slide active\\1" data-slide="{idx}"', content)
        else:
            # 其他頁面無 active
            content = re.sub(r'<section\s+class="slide(?:\s+active)?([^"]*)"',
                             f'<section class="slide\\1" data-slide="{idx}"', content)

        slides_html_list.append(f"    <!-- ==================== SLIDE {idx} ==================== -->\n    {content}\n")

        # 提取標題
        title = CUSTOM_TITLES.get(idx)
        if not title:
            h2_match = re.search(r'<h2 class="slide-title">(.*?)</h2>', content, re.DOTALL)
            if h2_match:
                title = clean_tag(h2_match.group(1))
            else:
                title = f"Slide {idx:02d}"

        jump_items.append(f'        <div class="jump-item" data-jump="{idx}"><span>{idx:02d}</span> {title}</div>')

    # 注入樣板
    html = html.replace('/* {{CSS}} */', css_content)
    html = html.replace('// {{JS}}', js_content)
    html = html.replace('<!-- {{SLIDES}} -->', '\n'.join(slides_html_list))
    html = html.replace('<!-- {{MODAL_JUMP_ITEMS}} -->', '\n'.join(jump_items))

    output_path = os.path.join(BASE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [OK] index.html 已生成 (共 {len(slide_files)} 頁投影片)")

def build_script():
    """構建 script.html"""
    tpl_path = os.path.join(SRC_DIR, 'templates', 'script.html.template')
    with open(tpl_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 讀取 CSS
    css_path = os.path.join(SRC_DIR, 'css', 'script.css')
    css_content = ''
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

    # 2. 讀取所有 sections
    sec_files = sorted(glob.glob(os.path.join(SRC_DIR, 'script-sections', '*.html')))
    sections_html_list = []
    quick_pills = ["      <span>快速跳轉：</span>"]

    for idx, sfile in enumerate(sec_files, start=1):
        with open(sfile, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # 自動校準 id="slide-{idx}" 與 <span class="slide-tag">SLIDE {idx:02d}</span>
        content = re.sub(r'<article\s+class="script-section"\s+id="slide-\d+"',
                         f'<article class="script-section" id="slide-{idx}"', content)
        content = re.sub(r'<span\s+class="slide-tag">SLIDE\s+\d+</span>',
                         f'<span class="slide-tag">SLIDE {idx:02d}</span>', content)

        sections_html_list.append(f"    <!-- ==================== SLIDE {idx} 講稿 ==================== -->\n    {content}\n")

        # 產生快捷 pill
        pill_text = CUSTOM_SCRIPT_PILLS.get(idx)
        if not pill_text:
            h2_match = re.search(r'<h2 class="slide-topic">(.*?)</h2>', content, re.DOTALL)
            if h2_match:
                topic = clean_tag(h2_match.group(1))
                pill_text = f"{idx:02d} {topic[:8]}"
            else:
                pill_text = f"{idx:02d} 講稿"

        quick_pills.append(f'      <a href="#slide-{idx}" class="quick-pill">{pill_text}</a>')

    # 注入樣板
    html = html.replace('/* {{CSS}} */', css_content)
    html = html.replace('<!-- {{QUICK_JUMP}} -->', '\n'.join(quick_pills))
    html = html.replace('<!-- {{SECTIONS}} -->', '\n'.join(sections_html_list))

    output_path = os.path.join(BASE_DIR, 'script.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [OK] script.html 已生成 (共 {len(sec_files)} 篇講稿)")

def sync_drives():
    """同步至 Google Drive 備份目錄"""
    synced_any = False
    for target in DRIVE_TARGETS:
        if os.path.exists(target):
            try:
                shutil.copy2(os.path.join(BASE_DIR, 'index.html'), target)
                shutil.copy2(os.path.join(BASE_DIR, 'script.html'), target)
                print(f"  [SYNC] 已複製更新至雲端硬碟: {target}")
                synced_any = True
            except Exception as e:
                print(f"  [SYNC WARN] 複製至 {target} 失敗: {e}")
    if not synced_any:
        print("  [SYNC INFO] 雲端硬碟路徑未掛載或未找到，略過同步。")

def build_all(sync=False):
    """執行全量構建"""
    t0 = time.time()
    print(">>> 開始構建簡報與逐字稿...")
    build_index()
    build_script()
    if sync:
        sync_drives()
    elapsed = time.time() - t0
    print(f">>> 構建完成！耗時 {elapsed:.3f} 秒。\n")

def watch_mode():
    """存檔監控模式"""
    print("=====================================================")
    print("  [WATCH] 正在監控 src/ 目錄...")
    print("  只要修改任何 CSS / JS / Slides / 講稿小檔案，立即自動重新組裝！")
    print("  按 Ctrl + C 可退出監控。")
    print("=====================================================")

    def get_src_mtimes():
        mtimes = {}
        for root, _, files in os.walk(SRC_DIR):
            for file in files:
                p = os.path.join(root, file)
                try:
                    mtimes[p] = os.path.getmtime(p)
                except OSError:
                    pass
        return mtimes

    last_mtimes = get_src_mtimes()

    try:
        while True:
            time.sleep(0.5)
            current_mtimes = get_src_mtimes()
            changed = False

            if set(current_mtimes.keys()) != set(last_mtimes.keys()):
                changed = True
            else:
                for p, mtime in current_mtimes.items():
                    if mtime > last_mtimes.get(p, 0):
                        changed = True
                        rel_path = os.path.relpath(p, BASE_DIR)
                        print(f"\n[DETECT] 偵測到檔案變更: {rel_path}")
                        break

            if changed:
                last_mtimes = current_mtimes
                build_all(sync=('--sync' in sys.argv))
    except KeyboardInterrupt:
        print("\n[WATCH] 監控已停止。")

if __name__ == '__main__':
    args = sys.argv[1:]
    if '--watch' in args:
        build_all(sync=('--sync' in args))
        watch_mode()
    else:
        do_sync = ('--sync' in args)
        build_all(sync=do_sync)
