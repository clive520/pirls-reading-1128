# AI 賦能閱讀理解：從 PIRLS 架構到智慧化課堂實踐

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-emerald?style=flat&logo=github)](https://clive520.github.io/pirls-reading-1128/)
[![Speaker Script](https://img.shields.io/badge/Speaker%20Script-講者逐字稿手冊-orange?style=flat)](https://clive520.github.io/pirls-reading-1128/script.html)

專為國小教師增能研習打造的 HTML 互動簡報與講者逐字稿手冊，結合 PIRLS 國際閱讀素養四層次架構與 Google AI Studio / Gemini 技術，實現智慧提問、即時批改、素養診斷與實體課堂補救。

---

## 🌐 線上預覽與講稿連結

- 🖥️ **線上簡報（Slide Deck）**：[https://clive520.github.io/pirls-reading-1128/](https://clive520.github.io/pirls-reading-1128/)
- 🎙️ **講者逐字稿手冊（Speaker Script）**：[https://clive520.github.io/pirls-reading-1128/script.html](https://clive520.github.io/pirls-reading-1128/script.html)
- 🚀 **GitHub Pages 設定教學簡報**：[https://clive520.github.io/pirls-reading-1128/github-pages-tutorial.html](https://clive520.github.io/pirls-reading-1128/github-pages-tutorial.html)
- 📝 **GitHub Pages 教學講者逐字稿**：[https://clive520.github.io/pirls-reading-1128/github-pages-script.html](https://clive520.github.io/pirls-reading-1128/github-pages-script.html)
- 🎮 **AI Studio 小遊戲實作與 Pages 發布簡報**：[https://clive520.github.io/pirls-reading-1128/ai-studio-game-tutorial.html](https://clive520.github.io/pirls-reading-1128/ai-studio-game-tutorial.html)
- 🎙️ **AI Studio 小遊戲講者逐字稿手冊**：[https://clive520.github.io/pirls-reading-1128/ai-studio-game-script.html](https://clive520.github.io/pirls-reading-1128/ai-studio-game-script.html)
- 📦 **GitHub 專案儲存庫**：[https://github.com/clive520/pirls-reading-1128](https://github.com/clive520/pirls-reading-1128)

---

## 🧩 模組化源碼結構與日常維護指南 (Modular Architecture)

為解決單一 HTML 檔案過於龐大（近 3,000 行）、修改不易且容易誤觸其他頁面的問題，本專案已全面升級為**「模組化拆分 ＋ 零依賴一鍵組裝」**架構：

```text
pirls-reading-1128/
├── src/                                  # ──【源碼修改區】──
│   ├── css/
│   │   ├── style.css                     # 全域基礎、配色主題、自適應版面
│   │   ├── spotlight.css                 # 簡報重點逐項跳出與特大靠中聚焦動畫
│   │   └── script.css                    # 講者逐字稿專用樣式
│   ├── js/
│   │   └── presentation.js               # 鍵盤導航、步驟步進、全螢幕與跳轉
│   ├── slides/                           # ──【各頁投影片獨立檔案】──
│   │   ├── 01-cover.html                 # 封面 (約 30 行)
│   │   ├── ...
│   │   ├── 15-live-test.html             # 現場實測與 QR Code
│   │   └── 16-summary.html
│   ├── script-sections/                  # ──【逐字稿各頁獨立檔案】──
│   │   ├── 01-cover.html
│   │   └── ...
│   └── templates/                        # 骨架樣板 (自動注入 CSS/JS/內容)
│
├── build.py                              # 一鍵自動組裝工具 (零第三方套件依賴)
├── index.html                            # 組裝完成的正式簡報 (發布與雙擊離線開啟)
└── script.html                           # 組裝完成的講者逐字稿
```

### 🛠️ 常見維護指令

1. **修改單頁內容**：
   - 直接開啟 `src/slides/XX-name.html`（僅幾十行），修改完成後執行：
     ```bash
     python build.py
     ```
   - 系統會在 **0.2 秒**內自動重新組裝出正式的 `index.html`。

2. **存檔自動更新 (Watch 模式)**：
   - 編輯時在終端機啟動：
     ```bash
     python build.py --watch
     ```
   - 只要儲存任何 CSS / JS / 投影片小檔案，系統將即時自動重新組裝，體驗極為流暢！

3. **構建並同步至雙雲端硬碟 (G 槽 / H 槽)**：
   ```bash
   python build.py --sync
   ```

4. **調整頁面順序**：
   - 只要直接重命名 `src/slides/` 中的檔案序號（例如將 `15-live-test.html` 移到 `09-live-test.html`），執行 `python build.py`，系統將**自動重新編排 `data-slide`、總頁數與跳轉選單**！

---

## 📑 簡報完整大綱與架構（共 16 頁）

- **Slide 01 封面**：`AI 賦能閱讀理解：PIRLS 提問 × 智慧批改實踐`
- **Slide 02 研習藍圖**：六大模組規劃總覽
- **Slide 03 現場痛點**：國小閱讀三大難題（**出題難**、**批改累**、**回饋慢**）
- **Slide 04 評量指北針**：PIRLS 閱讀理解四層次（**2×2 四象限矩陣排版**）
- **Slide 05 思維轉變**：傳統人工作業 vs. 人機協同模式對比
- **Slide 06 系統實踐**：雲端閱讀認證系統（師生雙端入口與管理總覽）
- **Slide 07 出題雙軌模式**：**AI 原創撰文出題** × **自行提供文章出題**
- **Slide 08 隨時彈性指派任務**：**單次/多次測驗** × **時間期限** × **跨班多選派卷**
- **Slide 09 智慧自動批改**：**2-5 分鐘秒級回饋** × **PIRLS 國際基準對標** × **作答歷程防猜檢視**
- **Slide 10 閱卷規準與二次審閱**：**PIRLS 0~3分 Rubrics 規準參照** × **教師主控微調點選**（人機雙重把關）
- **Slide 11 個人素養診斷報告**：**611分高基準國際常模彩帶** × **四向度認知歷程雷達圖** × **雙向指引**
- **Slide 12 班級弱點巨觀診斷**：**題型斷層（問答題僅17%）** × **PIRLS 四歷程斷崖（L3/L4）** × **時間預警**
- **Slide 13 針對性課堂補救策略**：**AI 專家模型生成 3 大實體教案**（雙段落比對學習單、三級式標記法、詩意辨析）
- **Slide 14 現實與成本考量**：**理想很豐滿、現實很骨感** × **DeepSeek 極致性價比 API** × **OpenRouter 多元生態**
- **Slide 15 現場實際實測 📱**：**手機掃碼進入學生端體驗（QR Code + 專屬網址 + 登入指引）**
- **Slide 16 大綱審閱與後續規劃**：三大步驟（前導架構確認、後續章節擴充、GitHub 部署與現場演講）

---

## 🖥️ 簡報操作快捷鍵

- **下一頁 / 下一步**：鍵盤 `→` / `Space` / `PageDown`，或點擊下方「下一頁」
- **上一頁 / 上一步**：鍵盤 `←` / `PageUp`，或點擊下方「上一頁」
- **全螢幕模式**：按鍵盤 `F` 鍵，或點擊下方「⛶ 全螢幕」
- **快速跳轉目錄**：按鍵盤 `M` 鍵，或點擊下方「📑 目錄」
- **打開講者逐字稿**：點擊下方橘色按鈕「🎙️ 講者逐字稿」（在新分頁開啟）
