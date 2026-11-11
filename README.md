# AI 賦能閱讀理解與國小教學研習簡報系統

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-emerald?style=flat&logo=github)](https://clive520.github.io/pirls-reading-1128/)
[![Speaker Script](https://img.shields.io/badge/Speaker%20Script-講者逐字稿手冊-orange?style=flat)](https://clive520.github.io/pirls-reading-1128/script.html)

本專案為國小教師專業增能研習打造之多專題 HTML 互動簡報系統，支援多份簡報獨立模組化維護與一鍵自動構建發布。

---

## 🌐 線上展示與簡報網址總覽 (GitHub Pages)

### 1. 🖥️ 原版正式簡報（16 頁完整實務）：
**《AI 賦能閱讀理解：從 PIRLS 架構到智慧化課堂實踐》**
* 🖥️ **線上簡報（Slide Deck）**：[https://clive520.github.io/pirls-reading-1128/](https://clive520.github.io/pirls-reading-1128/)
* 🎙️ **講者逐字稿手冊（Speaker Script）**：[https://clive520.github.io/pirls-reading-1128/script.html](https://clive520.github.io/pirls-reading-1128/script.html)
* 💡 內容：PIRLS 四層次提問、雲端閱讀認證系統、AI 自動批改、611分雷達診斷、課堂實體教案與學生端實測。

### 2. 🏫 鹿陽國小專屬簡報（新版 4 頁，支援持續擴增）：
**《鹿陽國民小學「閱讀理解策略與 AI 的結合」》• 講師：高志賢老師**
* 🖥️ **鹿陽專屬簡報網址**：[https://clive520.github.io/pirls-reading-1128/luyang.html](https://clive520.github.io/pirls-reading-1128/luyang.html)
* 🎙️ **鹿陽專屬講者逐字稿**：[https://clive520.github.io/pirls-reading-1128/luyang-script.html](https://clive520.github.io/pirls-reading-1128/luyang-script.html)
* 💡 目前大綱：
  1. **Slide 01 首頁**：研習主題、講師介紹、核心提問（說明閱讀理解測驗時我們會怎麼做）。
  2. **Slide 02 講師經歷**：新竹師範學院、南投縣僑光國小 (19年)、東海大學資訊工程學系、烏日區溪尾國小 (7年)、鹿陽國小 (第2年)（簡約大器排版，無裁切破版）。
  3. **Slide 03 個人獲獎**：教育部教學卓越獎【金質獎】、教育芬芳獎、創新應用團隊優勝等 8 大教育部全國榮譽，支援點擊獎狀彈窗放大。
  4. **Slide 04 臺灣 PIRLS 國際成績**：2023 最新發布（全球第7）、文體斷層 16 分對比、2023–2025 演進對照。

### 3. 🚀 其他教學簡報：
* 🚀 **GitHub Pages 設定教學簡報**：[https://clive520.github.io/pirls-reading-1128/github-pages-tutorial.html](https://clive520.github.io/pirls-reading-1128/github-pages-tutorial.html)
* 🎮 **AI Studio 小遊戲實作簡報**：[https://clive520.github.io/pirls-reading-1128/ai-studio-game-tutorial.html](https://clive520.github.io/pirls-reading-1128/ai-studio-game-tutorial.html)

---

## 🧩 模組化源碼結構 (Modular Architecture)

本專案採用**雙軌獨立模組拆分 ＋ 一鍵編譯**架構：

```text
pirls-reading-1128/
├── src/                                  # ──【源碼修改區】──
│   ├── css/                              # 全域基礎、時間軸、圖表、獎狀與聚焦點樣式
│   ├── js/                               # 鍵盤導航、全螢幕、目錄跳轉、獎狀彈窗操作
│   │
│   ├── slides/                           # ──【首頁 16 頁簡報各頁獨立檔案】──
│   │   ├── 01-cover.html ~ 16-summary.html
│   ├── script-sections/                  # ──【首頁 16 篇逐字稿獨立檔案】──
│   ├── templates/                        # ──【首頁樣板】──
│   │
│   └── luyang/                           # ──【鹿陽國小專屬簡報獨立區】──
│       ├── slides/                       # 01-cover ~ 04-pirls-taiwan.html
│       ├── script-sections/              # 01-cover ~ 04-pirls-taiwan.html
│       └── templates/                    # luyang 專屬樣板 (自動連接 luyang-script)
│
├── build.py                              # 一鍵全量自動構建工具 (0.1秒極速完成)
├── index.html                            # 原版 16 頁正式簡報 (https://.../pirls-reading-1128/)
├── script.html                           # 原版 16 篇講者逐字稿
├── luyang.html                           # 鹿陽國小專屬簡報 (https://.../luyang.html)
└── luyang-script.html                    # 鹿陽國小專屬講者逐字稿
```

### 🛠️ 日常維護與擴充指令

1. **一鍵構建全部簡報**：
   ```bash
   python build.py
   ```
2. **自動同步至雙雲端硬碟 (G 槽 / H 槽)**：
   ```bash
   python build.py --sync
   ```
3. **存檔自動更新 (Watch 模式)**：
   ```bash
   python build.py --watch
   ```
