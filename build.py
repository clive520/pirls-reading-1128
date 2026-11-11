# -*- coding: utf-8 -*-
"""
=============================================================================
PIRLS 閱讀理解簡報 - 多專題零依賴模組化構建工具 (Multi-Deck Build Tool)
=============================================================================
功能說明：
  1. 構建首頁正式簡報 (index.html / script.html)：
     - 來源：src/slides/ (16 頁完整版) 與 src/script-sections/
     - 主題：AI 賦能閱讀理解：從 PIRLS 架構到智慧化課堂實踐
  2. 構建鹿陽國小研習簡報 (luyang.html / luyang-script.html)：
     - 來源：src/luyang/slides/ 與 src/luyang/script-sections/
     - 主題：鹿陽國民小學「閱讀理解策略與 AI 的結合」
  3. 自動同步更新各簡報之頁碼、目錄跳轉彈窗 (Agenda Modal) 與快速跳轉列 (Quick Jump)
  4. 支援 --watch 存檔自動監控重構，以及 --sync 自動同步至雙雲端硬碟

使用方式：
  python build.py          # 單次構建所有簡報與講稿
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

# ===== 1. 首頁正式 16 頁簡報設定 =====
ORIGINAL_CUSTOM_TITLES = {
    1: "封面：AI 賦能閱讀理解",
    2: "研習藍圖：六大模組規劃",
    3: "國小閱讀三大現場痛點",
    4: "評量指北針：PIRLS 四層次",
    5: "思維轉變：人機協同新模式",
    6: "實踐成果：雲端閱讀認證系統",
    7: "出題雙軌模式：AI撰寫 vs 自備文本",
    8: "隨時彈性指派任務：單次/多次與期限",
    9: "後台自行批改：2-5分極速回饋與基準",
    10: "閱卷規準與二次審閱：人機把關",
    11: "個人診斷報告：611分高基準與雷達圖",
    12: "班級弱點巨觀診斷：題型斷層與歷程",
    13: "課堂補救策略：AI生成實體教案",
    14: "理想與現實：多模型API與極致性價比",
    15: "現場實際實測：學生端登入作答 (QR Code)",
    16: "大綱審閱與後續規劃"
}

ORIGINAL_CUSTOM_SCRIPT_PILLS = {
    1: "01 封面開場",
    2: "02 研習藍圖",
    3: "03 現場痛點",
    4: "04 PIRLS 四層次",
    5: "05 人機協同",
    6: "06 系統實踐",
    7: "07 雙軌出題",
    8: "08 任務指派",
    9: "09 自動批改",
    10: "10 規準與二次審閱",
    11: "11 個人素養雷達圖",
    12: "12 班級弱點巨觀分析",
    13: "13 課堂補救實體策略",
    14: "14 成本考量與多模型",
    15: "15 現場實際實測",
    16: "16 審閱總結"
}

# ===== 2. 鹿陽國小研習簡報設定 =====
LUYANG_CUSTOM_TITLES = {
    1: "首頁：閱讀理解策略與 AI 的結合",
    2: "講師經歷：高志賢老師簡介",
    3: "個人獲獎：教育部教學大獎肯定",
    4: "數據指標：臺灣 PIRLS 成績與趨勢洞察",
}

LUYANG_CUSTOM_SCRIPT_PILLS = {
    1: "01 封面開場",
    2: "02 講師經歷",
    3: "03 個人獲獎",
    4: "04 PIRLS 國際成績",
}

def clean_tag(text):
    """去除 HTML 標籤"""
    return re.sub(r'<[^>]+>', '', text).strip()

def get_combined_css():
    """讀取並合併全域 CSS"""
    css_files = ['style.css', 'spotlight.css']
    combined_css = []
    for cfile in css_files:
        cpath = os.path.join(SRC_DIR, 'css', cfile)
        if os.path.exists(cpath):
            with open(cpath, 'r', encoding='utf-8') as f:
                combined_css.append(f"/* ====== {cfile} ====== */\n" + f.read())
    return '\n\n'.join(combined_css)

def get_shared_js():
    """讀取共用 JS"""
    js_path = os.path.join(SRC_DIR, 'js', 'presentation.js')
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

def build_deck(slides_dir, tpl_path, output_filename, custom_titles, css_content, js_content):
    """通用簡報構建函式"""
    if not os.path.exists(tpl_path):
        print(f"  [WARN] 找不到樣板 {tpl_path}，略過 {output_filename}")
        return

    with open(tpl_path, 'r', encoding='utf-8') as f:
        html = f.read()

    slide_files = sorted(glob.glob(os.path.join(slides_dir, '*.html')))
    slides_html_list = []
    jump_items = []

    for idx, sfile in enumerate(slide_files, start=1):
        with open(sfile, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # 規範化 section 開頭
        content = re.sub(r'<section\s+class="slide([^"]*)"\s+data-slide="\d+"',
                         r'<section class="slide\1"', content)

        if idx == 1:
            content = re.sub(r'<section\s+class="slide(?:\s+active)?([^"]*)"',
                             f'<section class="slide active\\1" data-slide="{idx}"', content)
        else:
            content = re.sub(r'<section\s+class="slide(?:\s+active)?([^"]*)"',
                             f'<section class="slide\\1" data-slide="{idx}"', content)

        slides_html_list.append(f"    <!-- ==================== SLIDE {idx} ==================== -->\n    {content}\n")

        # 提取標題
        title = custom_titles.get(idx)
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

    output_path = os.path.join(BASE_DIR, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [OK] {output_filename} 已生成 (共 {len(slide_files)} 頁投影片)")

def build_script(sections_dir, tpl_path, output_filename, custom_pills):
    """通用逐字稿構建函式"""
    if not os.path.exists(tpl_path):
        print(f"  [WARN] 找不到樣板 {tpl_path}，略過 {output_filename}")
        return

    with open(tpl_path, 'r', encoding='utf-8') as f:
        html = f.read()

    css_path = os.path.join(SRC_DIR, 'css', 'script.css')
    css_content = ''
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

    sec_files = sorted(glob.glob(os.path.join(sections_dir, '*.html')))
    sections_html_list = []
    quick_pills = ["      <span>快速跳轉：</span>"]

    for idx, sfile in enumerate(sec_files, start=1):
        with open(sfile, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        content = re.sub(r'<article\s+class="script-section"\s+id="slide-\d+"',
                         f'<article class="script-section" id="slide-{idx}"', content)
        content = re.sub(r'<span\s+class="slide-tag">SLIDE\s+\d+</span>',
                         f'<span class="slide-tag">SLIDE {idx:02d}</span>', content)

        sections_html_list.append(f"    <!-- ==================== SLIDE {idx} 講稿 ==================== -->\n    {content}\n")

        pill_text = custom_pills.get(idx)
        if not pill_text:
            h2_match = re.search(r'<h2 class="slide-topic">(.*?)</h2>', content, re.DOTALL)
            if h2_match:
                topic = clean_tag(h2_match.group(1))
                pill_text = f"{idx:02d} {topic[:8]}"
            else:
                pill_text = f"{idx:02d} 講稿"

        quick_pills.append(f'      <a href="#slide-{idx}" class="quick-pill">{pill_text}</a>')

    html = html.replace('/* {{CSS}} */', css_content)
    html = html.replace('<!-- {{QUICK_JUMP}} -->', '\n'.join(quick_pills))
    html = html.replace('<!-- {{SECTIONS}} -->', '\n'.join(sections_html_list))

    output_path = os.path.join(BASE_DIR, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  [OK] {output_filename} 已生成 (共 {len(sec_files)} 篇講稿)")

def sync_drives():
    """同步至 Google Drive 備份目錄"""
    synced_any = False
    files_to_sync = ['index.html', 'script.html', 'luyang.html', 'luyang-script.html']
    for target in DRIVE_TARGETS:
        if os.path.exists(target):
            try:
                for fname in files_to_sync:
                    src_f = os.path.join(BASE_DIR, fname)
                    if os.path.exists(src_f):
                        shutil.copy2(src_f, target)
                print(f"  [SYNC] 已複製更新至雲端硬碟: {target}")
                synced_any = True
            except Exception as e:
                print(f"  [SYNC WARN] 複製至 {target} 失敗: {e}")
    if not synced_any:
        print("  [SYNC INFO] 雲端硬碟路徑未掛載或未找到，略過同步。")

def build_all(sync=False):
    """執行全量構建 (首頁 16 頁版 + 鹿陽國小研習版)"""
    t0 = time.time()
    print(">>> 開始全量構建簡報與逐字稿手冊...")

    css_content = get_combined_css()
    js_content = get_shared_js()

    # 1. 構建首頁 16 頁正式簡報與講稿
    print(" [1/2] 構建首頁正式簡報 (index.html & script.html)...")
    build_deck(
        slides_dir=os.path.join(SRC_DIR, 'slides'),
        tpl_path=os.path.join(SRC_DIR, 'templates', 'index.html.template'),
        output_filename='index.html',
        custom_titles=ORIGINAL_CUSTOM_TITLES,
        css_content=css_content,
        js_content=js_content
    )
    build_script(
        sections_dir=os.path.join(SRC_DIR, 'script-sections'),
        tpl_path=os.path.join(SRC_DIR, 'templates', 'script.html.template'),
        output_filename='script.html',
        custom_pills=ORIGINAL_CUSTOM_SCRIPT_PILLS
    )

    # 2. 構建鹿陽國小研習簡報與講稿
    print(" [2/2] 構建鹿陽國小研習簡報 (luyang.html & luyang-script.html)...")
    build_deck(
        slides_dir=os.path.join(SRC_DIR, 'luyang', 'slides'),
        tpl_path=os.path.join(SRC_DIR, 'luyang', 'templates', 'index.html.template'),
        output_filename='luyang.html',
        custom_titles=LUYANG_CUSTOM_TITLES,
        css_content=css_content,
        js_content=js_content
    )
    build_script(
        sections_dir=os.path.join(SRC_DIR, 'luyang', 'script-sections'),
        tpl_path=os.path.join(SRC_DIR, 'luyang', 'templates', 'script.html.template'),
        output_filename='luyang-script.html',
        custom_pills=LUYANG_CUSTOM_SCRIPT_PILLS
    )

    if sync:
        sync_drives()
    elapsed = time.time() - t0
    print(f">>> 全量構建完成！耗時 {elapsed:.3f} 秒。\n")

def watch_mode():
    """存檔監控模式"""
    print("=====================================================")
    print("  [WATCH] 正在監控 src/ 目錄 (含首頁版與鹿陽版)...")
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
