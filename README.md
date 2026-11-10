# 鹿陽國民小學「閱讀理解策略與 AI 的結合」教學研習簡報

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-emerald?style=flat&logo=github)](https://clive520.github.io/pirls-reading-1128/)
[![Speaker Script](https://img.shields.io/badge/Speaker%20Script-講者逐字稿手冊-orange?style=flat)](https://clive520.github.io/pirls-reading-1128/script.html)

專為國小教師專業成長研習打造之高質感 HTML 互動網頁簡報與講者逐字稿手冊。
**主講人：高志賢 老師（鹿陽國民小學）**
**研習核心探討：當我們進行閱讀理解測驗的時候，我們會怎麼做？**

---

## 🌐 線上展示與講稿連結 (GitHub Pages)

- 🖥️ **線上簡報網頁（Slide Deck）**：[https://clive520.github.io/pirls-reading-1128/](https://clive520.github.io/pirls-reading-1128/)
- 🎙️ **講者逐字稿手冊（Speaker Script）**：[https://clive520.github.io/pirls-reading-1128/script.html](https://clive520.github.io/pirls-reading-1128/script.html)
- 📦 **GitHub 專案儲存庫**：[https://github.com/clive520/pirls-reading-1128](https://github.com/clive520/pirls-reading-1128)

---

## 📑 目前簡報大綱（第一階段：前三頁，支援後續高度擴充）

1. **Slide 01 首頁**：
   - 鹿陽國民小學「閱讀理解策略與 AI 的結合」
   - 講師：高志賢老師
   - 核心問題：當我們進行閱讀理解測驗時，我們會怎麼做？
2. **Slide 02 講師經歷**：
   - 國立新竹師範學院畢業
   - 臺中市僑光國小 任職 19 年
   - 東海大學 資訊工程學系畢業（跨領域進修）
   - 臺中市霧峰區四德國小 任職 7 年
   - 臺中市鹿陽國民小學（目前第二年）
   - 跨領域優勢：28 年國小教學深耕 × 資訊工程科技思維
3. **Slide 03 臺灣 PIRLS 國際成績調查與趨勢圖表（2023–2025 深度剖析）**：
   - **國際評量週期**：PIRLS 每 5 年評量一次，最新 PIRLS 2021 成績於 **2023 年 5 月 16 日正式發布**（全面改為數位線上評量）。
   - **成績圖表**：臺灣平均 544 分，全球排名第 7 名（與瑞典並列，歷屆排名最高）。
   - **文體斷崖**：說明文 549 分（全球第 7）vs 故事體 533 分（全球第 17），落差高達 16 分！
   - **歷程瓶頸**：L1 提取與 L2 推論穩定，但 L3 詮釋整合與 L4 檢驗評估出現認知斷層。
   - **2023–2025 演進對照**：2023 成績發布 ➔ 2024 歷程診斷 ➔ 2025 雙閱讀素養推動與備戰 2026 PIRLS 數位評量。
   - **測驗現場反思**：傳統出題偏向表層提取，藉由 AI 賦能快速生成 PIRLS 四歷程深度理解題。

---

## 🧩 模組化源碼結構與日常擴增指南 (Modular Architecture)

本專案採用**「模組化拆分 ＋ 零依賴一鍵組裝」**架構，未來要增加第 4 頁、第 5 頁極為簡單：

```text
pirls-reading-1128/
├── src/                                  # ──【源碼修改區】──
│   ├── css/
│   │   ├── style.css                     # 全域主題、字體、版面配置、時間軸與圖表樣式
│   │   ├── spotlight.css                 # 簡報重點逐項跳出與聚焦動畫
│   │   └── script.css                    # 講者逐字稿專用樣式
│   ├── js/
│   │   └── presentation.js               # 鍵盤導航、全螢幕、目錄跳轉、進度條
│   ├── slides/                           # ──【各頁投影片獨立檔案】──
│   │   ├── 01-cover.html                 # 封面 (約 50 行)
│   │   ├── 02-speaker.html               # 講師經歷
│   │   └── 03-pirls-taiwan.html          # PIRLS 國際成績圖表與分析
│   ├── script-sections/                  # ──【逐字稿各頁獨立檔案】──
│   │   ├── 01-cover.html
│   │   ├── 02-speaker.html
│   │   └── 03-pirls-taiwan.html
│   └── templates/                        # 骨架樣板 (自動注入 CSS/JS/內容)
│
├── archive/                              # ──【歷史版本安全封存區】──
│   └── v1-16slides/                      # 先前 16 頁版本的完整備份
│
├── build.py                              # 一鍵自動組裝工具 (零第三方套件依賴)
├── index.html                            # 組裝完成的正式簡報 (可直接雙擊離線開啟)
└── script.html                           # 組裝完成的講者逐字稿
```

### 🛠️ 日常擴充投影片方式

1. **新增投影片**：
   - 在 `src/slides/` 目錄下建立新檔案，例如 `04-strategy.html`。
   - 在 `src/script-sections/` 目錄下建立對應講稿，例如 `04-strategy.html`。
2. **執行編譯**：
   ```bash
   python build.py
   ```
   系統會在 **0.05 秒**內自動重新組裝 `index.html` 與 `script.html`，並自動更新目錄跳轉彈窗、頁碼與快捷列！

---

## 🖥️ 簡報操作快捷鍵

- **下一頁 / 下一步**：鍵盤 `→` / `Space` / `PageDown`，或點擊下方「下一頁」
- **上一頁 / 上一步**：鍵盤 `←` / `PageUp`，或點擊下方「上一頁」
- **全螢幕播放**：鍵盤 `F` 鍵，或點擊下方「⛶ 全螢幕」
- **快速目錄**：點擊下方「📑 目錄」按鈕，可即時彈出全域選單跳轉任意頁面
- **講者逐字稿**：點擊「🎙️ 講者逐字稿」，在新分頁開啟同步講稿備忘錄
