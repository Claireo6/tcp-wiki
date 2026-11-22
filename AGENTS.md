# AGENTS.md - TCP 壅塞控制 LLM Wiki 作業標準操作手冊 (SOP)

本文件定義 AI 協作者在「TCP 壅塞控制」LLM Wiki 專案中的唯一作業守則。所有進入本專案的 AI 均須嚴格遵照本規範執行任務。

---

## 1. 專案核心原則與邊界

1. **嚴格真實與可溯源性（Strict Provenance）**：
   - 所有寫入 Wiki 的技術細節、公式、參數與狀態轉移規則，皆必須 100% 來自 `raw/` 中的原始資料。
   - 找不到文獻來源的內容**嚴禁推測或腦補**，一律明確標註「資料不足」。
   - **名稱與標籤也需要出處**：演算法暱稱（如 Tahoe、Reno）只有在 raw/ 文獻本身使用該名稱時才能使用。
   - **不得預先填寫**：尚未 ingest 的文獻內容不得預先寫入任何頁面（包含骨架頁面），必須在該篇 ingest 時才加入。
2. **獨立審查原則（Independent Review）**：
   - **禁止自我審查**：同一個對話 session 不得同時扮演作者與審查者。
   - 忠實度審查（Fidelity Review）必須由使用者於「全新對話」中發起，僅提供產出成品（Wiki/簡報）與 `raw/` 來源檔，審查報告存至 `reports/review-*.md`。
3. **版本控制與檔案權限**：
   - `raw/*.pdf` 僅留存於本機環境，已設定於 `.gitignore`，**嚴禁提交至 Git**。
   - 一般檔案連結一律使用標準 Markdown 格式 `[文字](路徑.md)`，不得使用 `[[wikilink]]`，以確保在 GitHub 原生正常瀏覽。

---

## 2. 目標讀者與教學深度

- **目標讀者**：修過基礎計算機概論的大學生（已具備封包交換、TCP 三向交握、Sequence/ACK 序號概念）。
- **教學起點**：必須在簡報前段簡短複習並釐清最易混淆的觀念：**Flow Control（`rwnd`，接收端能力）vs. Congestion Control（`cwnd`，網路承載力）**。
- **深度界定**：
  - **演進歷史（重點）**：講清楚為了解決前一代演算法的何種痛點（Jacobson 1988 $\rightarrow$ Reno $\rightarrow$ NewReno $\rightarrow$ CUBIC $\rightarrow$ BBR）。
  - **狀態機與核心機制（重點）**：Slow Start、Congestion Avoidance、Fast Retransmit、Fast Recovery 的觸發條件與 `cwnd` 變化。
  - **數學模型（直觀引導）**：
    - CUBIC：僅說明三次曲線形狀與直覺（先快 $\rightarrow$ 接觸上次壅塞點變平緩 $\rightarrow$ 再度向上探測），不推導公式。
    - BBR：僅傳達「不以封包遺失判定壅塞，改量測瓶頸頻寬（BtlBw）與往返傳輸延遲（RTprop）」的核心哲學，不推導 pacing 公式。

---

## 3. 語言與專有名詞規範

1. **語系**：一律使用台灣繁體中文（zh-TW）。
2. **專有名詞與變數**：
   - 變數與演算法名稱一律保留英文並以程式碼標籤呈現（如 `` `cwnd` ``、`` `rwnd` ``、`` `ssthresh` ``、`` `FlightSize` ``、`` `SMSS` ``）。
   - 核心機制名稱在**每頁第一次出現時**寫「中文（English）」（例如「慢啟動（Slow Start）」、「壅塞避免（Congestion Avoidance）」、「快速重傳（Fast Retransmit）」、「快速恢復（Fast Recovery）」）；**之後一律直接使用英文**（如 slow start、fast recovery）。
3. **禁用詞檢驗清單**（lint 會強制掃描，出現即中斷）：
   - 擁塞 $\rightarrow$ **壅塞**
   - 數據包 $\rightarrow$ **封包**
   - 帶寬 $\rightarrow$ **頻寬**
   - 三次握手 $\rightarrow$ **三向交握**
   - 緩存 $\rightarrow$ **緩衝區**
   - 默認 $\rightarrow$ **預設**

---

## 4. 出處引用與引文規範

1. **標記格式**：
   - RFC 文件：`[RFC 5681 §3.1]`（必須包含章節編號，允許附錄字母如 `[RFC 9438 §B]`）。
   - Jacobson 論文：`[Jacobson 1988, §2, p.3]`（章節編號 + 頁碼，引言用 `§Intro`，附錄用 `§A`～`§D`，例如 `[Jacobson 1988, §B, p.20]`）。
     - **頁碼範圍**：一般概念敘述（段落層級）允許使用頁碼範圍格式 `p.X-Y`（例如 `[Jacobson 1988, §A, p.18-20]`）；但數字、公式、英文原句之出處標記**必須為單一頁碼** `p.X`，不得使用範圍格式。
   - BBR 論文：`[BBR 2016, "小節標題"]`（以原文 Section 標題為準，因 PDF 頁碼不可靠）。
2. **標記密度**：
   - 數字、公式、狀態轉移條件：**逐句標註**，且出處頁碼必須為單一頁碼。
   - 一般概念敘述：**逐段標註**，允許頁碼範圍。
   - 頁尾必備章節：每一頁最下方必須具備「## 參考來源」清單（排除 `wiki/index.md` 與 `wiki/log.md`）。
3. **英文原句摘錄（Direct Quotes）**：
   - 關鍵定義（如 `FlightSize`、`ssthresh` 計算規則、`DupThresh` 定義）與關鍵數值，必須在中文說明後附上英文原句引用區塊。
   - 摘錄文字與 `raw/*.txt` 於壓縮連續空白與折行後，必須 100% 精確匹配（完全一致之子字串比對，嚴禁模糊比對）。
   - 正規化規則：(a) 壓縮連續空白與換行；(b) 處理行尾連字號斷字：原文同時存在「排版斷字」（`win-\nter` → `winter`）與「本來就有連字號的複合字剛好斷在行尾」（`full-\nsized` → `full-sized`），lint 會對 raw 各產生一個版本，引文符合任一版本即通過；(c) 將 `' ' " "` 等彎引號統一換成 `' "`（直引號），與壓縮空白屬同等級正規化，不視為修改原文。

---

## 5. 演進（Evolution）vs. 衝突（Conflicts）判定標準

1. **客觀判斷準繩**：
   - **演進（Evolution）**：RFC 標頭若有正式 `Obsoletes` 或 `Updates` 關係（如 RFC 9438 Updates 5681），記載於 `wiki/timeline.md` 及各概念頁的「歷史演進」小節。
   - **衝突 / 歧異（Conflicts）**：凡無正式更新關係、文件類別不同（如 Standards Track vs RFC 6928 Experimental）、或學術論文與 RFC 工程實作說法分歧者，一律收錄於 `wiki/conflicts.md`。每筆記載必須至少具備**兩個不同來源**的出處標註。
2. **主述基準**：
   - 概念頁一律以 **Standards Track** 文件為主述，Experimental 文件及學術論文標明身份後作為補充。
   - `sources/*.md` 頁面的標題**必須嚴格依照 `raw/` 文件的原文標題**命名（例如 RFC 9438 標題為 `"CUBIC for Fast and Long-Distance Networks"`）。

---

## 6. 資料夾結構

```text
tcp-wiki/
├── AGENTS.md                  # 本操作手冊
├── .gitignore                 # 包含 raw/*.pdf 等忽略項目
├── raw/                       # 原始文獻（rfc5681.txt, rfc6582.txt, rfc6928.txt, rfc9438.txt, jacobson1988.pdf, bbr2016.pdf）
├── scripts/
│   └── lint.py                # 自動化檢查腳本（僅使用 Python 標準庫）
├── reports/                   # lint-YYYYMMDD-HHMMSS.md 與 review-*.md 報告紀錄
├── slides/
│   └── index.html             # 最終產出之單一獨立自修教材 HTML 簡報
└── wiki/
    ├── index.md               # 頁面目錄 + 一句話摘要（純目錄）
    ├── log.md                 # 每次異動與 Lint 結果歷史審查紀錄
    ├── glossary.md            # 標準詞彙表 + 禁用詞過濾對照表
    ├── timeline.md            # 年份、痛點、RFC 關係之演進表
    ├── parameters.md          # 所有數字與參數索引（必須全數標註出處）
    ├── conflicts.md           # 歧異與衝突對照表（每筆至少兩來源）
    ├── sources/               # 單篇摘要（文首必帶 Category/Obsoletes/Updates）
    ├── concepts/              # 機制頁（rwnd-vs-cwnd, slow-start, congestion-avoidance, fast-retransmit-fast-recovery, packet-loss-detection）
    └── algorithms/            # 演算法頁（reno, new-reno, cubic, bbr）
```

---

## 7. Ingest 標準作業流程

### 第 0 步：環境與 Lint 驗證（Pre-ingest Setup）
在消化第一份文獻之前，必須先撰寫好 `scripts/lint.py`，並在初版 Wiki 架構上試跑一次，確認報告檔案 `reports/lint-YYYYMMDD-HHMMSS.md` 能正常產出且回傳碼機制正確。

### 依序處理文獻（Chronological Order）：
1. `jacobson1988.txt`（注意：論文已轉為 `raw/jacobson1988.txt` 純文字檔；嚴格查證原文是否使用「Tahoe」字眼；若無論及，Wiki 嚴禁宣稱「Jacobson 1988 = Tahoe」，必須如實記載來源事實）。
2. `raw/rfc5681.txt`
3. `raw/rfc6582.txt`
4. `raw/rfc6928.txt`
5. `raw/rfc9438.txt`
6. `raw/bbr2016.pdf`

### 單篇循環流程（Fixed Cycle）：
每篇文獻之消化與寫入均必須依序完成以下步驟，不得跳步：
0. **來源驗證**：在進入討論前，嚴格核對 `raw/` 檔案之標題、作者、日期、頁數是否與原始文獻相符；若不符（如二手評述或殘缺檔）必須立即停止並回報使用者。
1. **討論**：向使用者報告此文獻核心重點、預計新增/修改之頁面清單、與現有頁面是否有潛在衝突或更新。
2. **確認**：等待使用者回覆確認或指示調整。
3. **寫入**：依確認內容建立/更新對應之 `sources/`、`concepts/`、`algorithms/`、`parameters.md`、`timeline.md` 或 `conflicts.md`；同步更新 `wiki/index.md`（將新頁面加入目錄）與 `wiki/glossary.md`（收錄新出現之專門詞彙）。
4. **Lint**：執行 `python scripts/lint.py` 進行全庫檢驗。若 Lint 失敗，依錯誤清單修正並重新執行，最多 3 輪；若 3 輪後仍未通過，必須立即停止作業，將未解決的錯誤完整回報給使用者，不得進入下一步。
5. **Log**：更新 `wiki/log.md`，記載本輪更動之頁面、文獻來源以及 Lint 檢驗結果。
6. **使用者 Commit**：提示使用者執行 `git commit`。待使用者確認完成提交後，方可開啟下一篇文獻之討論。

---

## 8. 自動化檢查規範（`scripts/lint.py`）

腳本一律僅使用 Python 標準函式庫，若有違規必須回傳非 0 exit code，並產出 `reports/lint-YYYYMMDD-HHMMSS.md`。

### Wiki 檢查規則：
- `[a] 孤兒頁面`：所有 `wiki/**/*.md` 均必須列入 `wiki/index.md`。
- `[b] 內部連結`：所有 `[text](path.md)` 之目標路徑皆必須存在。
- `[c] 引用格式`：正則驗證 `[RFC \d+ §[\d\.A-Za-z]+]`、`[Jacobson 1988, §[0-9A-Za-z]+, p\.\d+]`（允許頁碼範圍 `p.X-Y` 供段落層級引用）、`[BBR 2016, "標題"]` 格式（RFC 章節允許附錄字母如 `[RFC 9438 §B]`，Jacobson 論文允許 `§Intro` 與附錄字母 `§A`～`§D`，例如 `[Jacobson 1988, §B, p.20]`）。
- `[d] 原文比對`：針對 RFC 與 Jacobson 1988 引用的英文原句，以下正規化後與 `raw/*.txt` 進行完全一致的子字串比對（嚴禁模糊比對）；PDF 論文之引用留待獨立 AI 審查。正規化步驟：(1) 處理行尾連字號斷字；(2) 壓縮連續空白與換行；(3) 將 `' ' " "` 等彎引號統一換成 `' "`（直引號）。
- `[e] 禁用詞`：對照 `wiki/glossary.md` 禁用詞，檢測到即回報檔案與行號（掃描時必須排除 `wiki/glossary.md` 本身的禁用詞對照表區塊）。
- `[f] 來源欄位`：`sources/*.md` 頂部必須具備 `Category`、`Obsoletes`、`Updates`。
- `[g] 標頭忠實`：`sources/*.md` 標頭值直接與 `raw/*.txt` 標頭原文比對。
- `[h] 必備章節`：所有頁面末尾必須包含「## 參考來源」（排除 `wiki/index.md` 與 `wiki/log.md`）。
- `[i] 參數出處`：`wiki/parameters.md` 內所有數字均必須緊跟出處標籤。
- `[j] 衝突來源`：`wiki/conflicts.md` 每一項目必須具備至少兩個不同出處。
- `[k] 出處存在性`：出處不只格式要對，被引用的位置必須真的存在：RFC 章節編號必須出現在 `raw/rfcNNNN.txt` 的章節標題中；Jacobson 1988 章節須屬於 `Intro, 1-4, A-D` 且頁碼在 1-25 之間；BBR 小節標題必須出現在 BBR 原文中。（2026-11-22 ingest 2 時新增：發現骨架頁面引用了不存在的 `RFC 5681 §1.2` 與 BBR "Introduction"，但 [c] 只檢查格式而全數通過。）

### 簡報檢查規則（`--slides`）：
- 每一頁 `<section>` 必須包含 `data-src="wiki/..."` 且該 Wiki 頁面真實存在。
- 每頁正文字數上限為 **100 字**（嚴格排除 `<details>` 補充區塊）。
- 禁用詞過濾。
- 數字查核：簡報出現的所有數字均必須在 `wiki/parameters.md` 中存在（**排除**：4 位數年份、RFC 編號、出處標籤內數字）。

---

## 9. 最終產出：HTML 簡報規範（`slides/index.html`）

1. **架構**：單一獨立 HTML 檔案，零外部套件（零 CDN、零 npm 依賴），可離線以任何現代瀏覽器開啟。
2. **版面**：自修教材型。正文在 100 字內，深入細節收納於可點擊展開的 `<details><summary>詳細補充</summary>...</details>`。
3. **原生視覺化**：
   - 零依賴，純手寫 Inline SVG 與原生 JavaScript。
   - **`cwnd` 鋸齒動態模擬圖**：以 JS 依據 RFC 5681 規範動態算繪，提供按鈕即時切換「**Timeout（逾時）**」與「**3 Duplicate ACKs（三次重複確認）**」兩種遺失情境，動態展示 `cwnd` 與 `ssthresh` 之變化曲線。
   - **狀態轉移圖**：手繪 Inline SVG，展示 Slow Start、Congestion Avoidance、Fast Recovery 轉移條件。
   - **CUBIC 曲線圖**：以 RFC 9438 參數 $C=0.4, \beta=0.7$ 及公式 $W(t) = C(t-K)^3 + W_{max}$ 繪製原生 SVG 曲線。
   - 圖表中使用的每一個常數與規則，皆必須與 `wiki/parameters.md` 記載完全吻合。
