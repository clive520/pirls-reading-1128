# AI 賦能閱讀理解：從 PIRLS 架構到智慧化課堂實踐

專為國小教師增能研習打造的 HTML 互動簡報與講者逐字稿手冊，結合 PIRLS 國際閱讀素養四層次架構與 Google AI Studio / Gemini 技術，實現智慧提問、即時批改與深度思維對話。

---

## 📂 專案檔案結構

- **`index.html`**：演講投影片主頁（極簡重點、大字級、鍵盤與觸控翻頁、全螢幕播放）。
- **`script.html`**：講者專用演講逐字稿手冊（附建議時間、現場互動指示、完整口語逐字講稿、支援列印與另存 PDF）。
- **`assets/images/`**：
  - `reading_system_login.png`：雲端閱讀認證系統前台入口截圖。
  - `teacher_dashboard.png`：教師管理後台截圖。

---

## 📑 簡報完整大綱與架構（共 11 頁）

- **Slide 01 封面**：`AI 賦能閱讀理解：PIRLS 提問 × 智慧批改實踐`
- **Slide 02 研習藍圖**：六大模組規劃總覽
- **Slide 03 現場痛點**：國小閱讀三大難題（**出題難**、**批改累**、**回饋慢**）
- **Slide 04 評量指北針**：PIRLS 閱讀理解四層次（**2×2 四象限矩陣排版**）
- **Slide 05 思維轉變**：傳統人工作業 vs. 人機協同模式對比
- **Slide 06 系統實踐**：雲端閱讀認證系統（師生雙端入口與管理總覽）
- **Slide 07 出題雙軌模式**：**AI 原創撰文出題** × **自行提供文章出題**
- **Slide 08 隨時指派任務**：**單次/多次測驗**、**時間期限**、**跨班多選派卷**
- **Slide 09 成果總覽與後台批改**：**2-5 分鐘秒級回饋** × **PIRLS 國際基準對標** × **作答歷程防猜檢視**
- **Slide 10 AI 評改 × 老師二次審閱**：**PIRLS 0~3分 Rubrics 規準微調** × **四向度認知雷達圖診斷**
- **Slide 11 審閱與後續規劃**：大綱審閱與後續章節擴充規劃

- **下一頁**：鍵盤 `→` / `Space` / `PageDown`，或點擊下方「下一頁」
- **上一頁**：鍵盤 `←` / `PageUp`，或點擊下方「上一頁」
- **全螢幕模式**：按鍵盤 `F` 鍵，或點擊下方「⛶ 全螢幕」
- **快速跳轉目錄**：按鍵盤 `M` 鍵，或點擊下方「📑 目錄」
- **打開講者逐字稿**：點擊下方橘色按鈕「🎙️ 講者逐字稿」（在新分頁開啟）

---

## 🚀 如何部署到 GitHub Pages（一鍵上線）

本專案為純靜態 HTML/CSS/JS，無須任何建置工具（零安裝、零相依）：

1. **建立 GitHub 儲存庫 (Repository)**
   - 至 [GitHub](https://github.com/) 建立一個全新的公開 (Public) 儲存庫，例如：`pirls-ai-reading-deck`。

2. **推送本專案至 GitHub**
   在本地終端機（PowerShell）執行：
   ```bash
   git add .
   git commit -m "feat: 初版完成（PIRLS閱讀簡報重點頁 + 獨立逐字稿手冊網頁）"
   git branch -M main
   git remote add origin https://github.com/<您的GitHub帳號>/<儲存庫名稱>.git
   git push -u origin main
   ```

3. **啟用 GitHub Pages**
   - 進入 GitHub 儲存庫頁面，點選 **Settings（設定）**。
   - 左側選單點選 **Pages**。
   - 在 **Build and deployment > Source** 選擇 **Deploy from a branch**。
   - Branch 選擇 **`main`**，資料夾選擇 **`/ (root)`**，點選 **Save**。
   - 等待約 1 分鐘，GitHub 就會提供專屬網址：
     `https://<您的GitHub帳號>.github.io/<儲存庫名稱>/`
   - 點進去即可直接投影演講，或在手機/平板開啟 `script.html` 觀看逐字稿！
