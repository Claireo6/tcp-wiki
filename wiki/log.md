# 異動與審查日誌（Log）

本文件按時間倒序記錄知識庫之所有文件消化（Ingestion）、頁面異動以及自動化檢驗（Lint）執行結果。

---

## 2026-11-22 - 簡報修訂：使用者回饋「初學者看不懂、頁面下方很空」（大圈退回）

- **回饋來源**：使用者在交件前親自瀏覽簡報後提出。這是流程中**第一次從最後一關退回到大綱／逐頁稿**的大圈。
- **根本原因**：訪談時為了避免版面溢出，把每頁正文上限訂為 100 字；但這條規格從未用「目標讀者是否看得懂」檢驗過，導致每頁只剩重點、缺少解釋，版面也偏空。
- **規格變更**：正文上限 100 → **180 字**（`scripts/lint.py` 的 `SLIDE_WORD_LIMIT`、AGENTS.md §8、§9 同步更新）。
- **逐頁稿重寫**：13 頁都改成固定的教學結構：「這頁要回答的問題」→ 分步驟解釋 →「一句話記住」。內容仍只來自 wiki。
- **lint --slides（2 輪）**：
  - 第 1 輪 FAIL（`reports/lint-20261122-211326.md`）：第 6、9、10、12 頁超過 180 字 → 退回逐頁稿縮短。縮短時一併做忠實度自查，刪除 2 句 wiki 找不到依據的說法（第 5 頁「『慢』是相對於一開始就全速送出」、第 6 頁「讓網路有機會恢復」）；第 11 頁的 RTT 公平性出自 `sources/rfc9438.md`，補進 data-src。
  - 第 2 輪 PASS（`reports/lint-20261122-211343.md`）。各頁正文字數：136、156、170、179、150、157、95、131、174、176、134、179、133。
- **渲染檢查（4 輪）**：
  - 第 1 輪 FAIL（`reports/render-20261122-211402.md`）：6 頁超出框。新版面元素（重點框、雙欄、步驟）尚無 CSS → 留在渲染節點補 CSS。
  - 第 2 輪 PASS，但目視截圖發現內容只佔上半部、下方大片空白（正是使用者回饋的問題）→ 放大字級。
  - 第 3 輪 PASS，目視仍有空白 → 根本原因是投影片框固定 700px 高；改為「框高度隨內容、垂直置中」。
  - 第 4 輪 PASS（`reports/render-20261122-211515.md`），目視確認各頁版面平均。
- **觀察**：渲染檢查的程式只能抓「溢出」，抓不到「太空、不好讀」；這類問題只能靠目視截圖與使用者回饋。

---

## 2026-11-22 - 教學 HTML 簡報製作（接手者：Claude）

依 AGENTS.md §10 的 graph 執行。

- **檢索 wiki + 覆蓋率關卡**：13 頁投影片各對應至少 1 個 wiki 頁，沒有任何一頁需要 wiki 以外的知識 → 通過。大綱寫入 `slides/outline.md`。
- **人工確認**：使用者確認大綱（13 頁）。
- **lint 規則修正（寫稿前）**：原本的 `--slides` 數字檢查會掃描整份 HTML（含 CSS 的 px、JS 常數），必定大量誤報。改為：數字只檢查各頁 `<section>` 內讀者看得到的文字；字數上限不計 `<svg>` 圖表標籤；新增「圖表參數」檢查：圖表常數集中在 `chart-params` JSON，每個值都必須在 `parameters.md` 中登錄且附 source。
- **parameters.md**：新增「簡報引用之情境數字」（32 Kbps、40 bps、7 個演算法、2 Gbps、15 Mbps、133 倍），皆附出處。
- **逐頁稿**：寫入 `slides/drafts/01.html` 至 `13.html`。作者自我比對 wiki 後修正 2 處：第 13 頁「2009 RFC 5681：四個演算法標準化」與事實不符（RFC 5681 是取代 RFC 2581 的修訂版），改為「現行標準（取代 RFC 2581）」；第 12 頁「不排隊，也不浪費」是自己的說法，改回 wiki 的「吞吐量最高、延遲最低」。
- **lint --slides**：第 1 輪 PASS（`reports/lint-20261122-210008.md`）。負向測試：加入未登錄數字 400 與超過 100 字的段落，兩者都被抓到（`reports/lint-20261122-210017.md`），還原後 PASS。各頁正文字數 18～86 字。
- **渲染**：`scripts/build_slides.py` 組合逐頁稿，不修改文字。
- **渲染檢查（3 輪）**：
  - **第 1 輪 FAIL**（`reports/render-20261122-210043.md`）：第 7、11 頁內容超出投影片框。原因是圖表依寬度等比放大，高度超過 300px。字數合格，因此**留在渲染節點**以 CSS 限制圖表最大高度修正，未退回逐頁稿。
  - **第 2 輪 PASS**（`reports/render-20261122-210058.md`），但作者目視截圖發現程式抓不到的問題：第 8 頁狀態轉移圖標籤與方框重疊、第 11 頁 CUBIC 曲線縱軸範圍過大而被壓扁。修正 SVG 座標與縱軸範圍。
  - **第 3、4 輪 PASS**（`reports/render-20261122-210131.md`、`reports/render-20261122-210148.md`），並微調 CUBIC 標籤位置。截圖存於 `reports/render/`。
- **待辦**：獨立 AI 審查（依 AGENTS.md §1，須由使用者另開新對話進行，作者不得自我審查）。

---

## 2026-11-22 - 文獻 6/6 bbr2017（接手者：Claude）

- **步驟 0 來源驗證**：raw/ 中的 BBR 檔案是 Communications of the ACM，February 2017，Vol. 60，No. 2，pp. 58-66（DOI 10.1145/3009824），作者 Cardwell / Cheng / Gunn / Hassas Yeganeh / Jacobson，文章由 queue.acm.org 發展而來。專案原本以「BBR 2016」（ACM Queue 網頁版的年份）規劃，但檔案中沒有出現 2016，無法從 raw/ 驗證，因此**全面改為 BBR 2017**；檔案已由使用者改名為 `raw/bbr2017.pdf` 與 `raw/bbr2017.txt`。這份是正式排版期刊 PDF，頁碼固定，出處格式改為 `BBR 2017` + 小節標題 + 頁碼（原本「網頁另存 PDF 頁碼不可靠」的理由已不成立）。全文搜尋 Tahoe：0 次。
- **規則調整（寫入前）**：lint 的 [c] 改用新格式；[k] 檢查 BBR 小節標題存在且頁碼在 58-66；[d] 原句比對加入 `raw/bbr2017.txt`；AGENTS.md 同步更新。
- **步驟 3 寫入**：
  - 新增 `sources/bbr2017.md`、`algorithms/bbr.md`（依教學深度設定只講核心概念，不推導 pacing 公式）
  - `conflicts.md` 新增第 7 筆：壅塞信號（封包遺失 vs. 量測 BtlBw 與 RTprop），並移除「尚未 ingest」的提示
  - `parameters.md` 新增 ProbeBW 峰值增益 1.25、ProbeRTT 在途量 4 個封包；`timeline.md` 新增 2017 列；`glossary.md` 新增 BBR、BtlBw、RTprop、BDP、Bufferbloat、Pacing gain；`index.md` 新增 2 頁
  - 自我複查：bbr.md 原本寫「loss-based 演算法一直增加在途量直到緩衝區滿」並標成開場段落 p.58，複查原文後改為 "Congestion and Bottlenecks" p.59 的原意（運作在頻寬受限區域的最右緣，代價是高延遲與頻繁遺失）。
- **步驟 4 Lint（2 輪）**：
  - **第 1 輪 FAIL**（`reports/lint-20261122-205121.md`，6 項）：其中 5 項是 **lint 誤判**，Markdown 連結文字（如連到 BBR 頁、Jacobson 1988 頁的連結）以 BBR / Jacobson 開頭，被 [c] 當成格式錯誤的出處；另外說明出處格式的行內程式碼也被當成出處。修正：[c] 與 [k] 掃描前先移除行內程式碼與 Markdown 連結文字。
  - **第 2 輪 PASS**（`reports/lint-20261122-205132.md`，21 個檔案，0 項違規）。
  - **修正後負向測試**：放入 4 個錯誤出處（不存在的 BBR 小節 "Introduction"、舊格式 BBR 2016、超出範圍的 p.70、不存在的 RFC 5681 §1.2），4 個全部被抓到（`reports/lint-20261122-205137.md`），還原後 PASS（`reports/lint-20261122-205138.md`）。
- **Wiki 完成狀態**：6 篇文獻全部 ingest 完成（Jacobson 1988、RFC 5681、RFC 6582、RFC 6928、RFC 9438、BBR 2017），共 21 頁。

---

## 2026-11-22 - 文獻 5/6 rfc9438（接手者：Claude）

- **步驟 0 來源驗證**：標題 "CUBIC for Fast and Long-Distance Networks"、作者 Xu / Ha / Rhee / Goel / Eggert（編輯）、August 2023、Standards Track、Obsoletes 8312、**Updates 5681**，與原文相符。本 RFC 為新版格式，純文字檔沒有頁碼，因此 sources 頁不記錄頁數。全文搜尋 Tahoe：0 次。
- **關係判定**：第一份對 RFC 5681 有正式 Updates 關係的文件 → 依 AGENTS.md §5，與 RFC 5681 的差異寫入 `timeline.md` 與概念頁「歷史演進」小節，不列入 conflicts。論文（Jacobson 0.5）與 RFC 9438（0.7）之間沒有正式關係，列入 conflicts 第 6 筆。
- **引文處理**：RFC 9438 §4.6 原句含有 RFC 自身的參考標記（中括號包住的 RFC5681），會被 lint [c] 誤判為格式錯誤的出處標籤，因此只截取不含該標記的片段引用。
- **步驟 3 寫入**：
  - 新增 `sources/rfc9438.md`、`algorithms/cubic.md`
  - `concepts/congestion-avoidance.md`、`concepts/slow-start.md` 各新增「歷史演進」小節（CUBIC 更積極的增長、HyStart++）
  - `parameters.md` 新增 β_cubic 0.7（§4.6，取代骨架階段錯標的 §4.1）、C 0.4（§5.1）、1.5 倍目標上限、fast convergence 係數；這些即為簡報 CUBIC 曲線使用的參數
  - `conflicts.md` 新增第 6 筆；`timeline.md` 新增 2023 列；`glossary.md` 新增 CUBIC、W_max、K、Reno-friendly region、HyStart++；`index.md` 新增 2 頁
- **步驟 4 Lint**：第 1 輪 PASS（`reports/lint-20261122-204651.md`，19 個檔案，0 項違規）。

---

## 2026-11-22 - 文獻 4/6 rfc6928（接手者：Claude）

- **步驟 0 來源驗證**：標題 "Increasing TCP's Initial Window"、作者 Chu / Dukkipati / Cheng / Mathis（Google）、April 2013、**Category: Experimental**、無 Obsoletes / Updates、共 24 頁，與原文相符。全文搜尋 Tahoe：0 次。
- **關係判定**：§1 自稱對 RFC 3390 與 RFC 5681 做了 "minor revision"，但標頭沒有 Updates 欄位。依 AGENTS.md「以標頭為準」，與 RFC 5681 的差異列入 conflicts，不列為演進。這也解釋了訪談階段 AI 誤判「RFC 6928 取代 RFC 5681」的原因：正文的說法與標頭的正式關係不一致。
- **lint 調整**：RFC 6928 原文的 §5.1 標題排版不一致（「5.1 Reducing Latency」少了句點與一個空白），會讓 [k] 誤判 §5.1 不存在。放寬章節標題比對規則（句點與空白數可變，標題需以大寫字母開頭），並逐一列出 4 份 RFC 偵測到的章節清單確認沒有誤抓。
- **步驟 3 寫入**：
  - 新增 `sources/rfc6928.md`
  - `concepts/slow-start.md` 新增「IW10：實驗性提案」小節（明確標示 Experimental）
  - `conflicts.md` 新增第 4、5 筆：IW 上限（2～4 vs 10）、SYN 遺失後的 IW（MUST 為 1 vs 建議不重設）
  - `parameters.md` 新增 IW10 上限、14600 位元組、4 KB 回退門檻、最多省 4 個 RTT、實驗結果數字；`timeline.md` 新增 2013 列；`glossary.md` 新增 IW10；`index.md` 新增來源頁
  - 自我複查：slow-start 頁「網頁物件變大」原本標成 §4，實際出自 §5.2，已修正。
- **步驟 4 Lint**：第 1 輪 PASS（`reports/lint-20261122-204345.md`，17 個檔案，0 項違規）。

---

## 2026-11-22 - 文獻 3/6 rfc6582（接手者：Claude）

- **步驟 0 來源驗證**：標題 "The NewReno Modification to TCP's Fast Recovery Algorithm"、作者 Henderson / Floyd / Gurtov / Nishida、April 2012、Standards Track、Obsoletes 3782、共 16 頁，與原文相符。
- **名稱查證**：
  - 「Reno」：§1 說明 RFC 5681 fast recovery 的典型實作最早出現在 1990 BSD Reno 版本、並在 [FF96] 被稱為 "Reno algorithm"，因此本輪起可以建立 `algorithms/reno.md`。
  - 「Tahoe」：討論階段原本回報「全文未出現」，寫入前複查發現**出現 1 次**，但只在參考文獻 [FF96] 的論文標題中，正文沒有任何定義。已向使用者更正，並維持不建立 Tahoe 內容。（教訓：名稱查證要用全文搜尋確認，不能只憑閱讀印象。）
- **步驟 3 寫入**：
  - 新增 `sources/rfc6582.md`、`algorithms/reno.md`、`algorithms/new-reno.md`
  - 更新 `concepts/fast-retransmit-fast-recovery.md`（NewReno 修正段落）
  - `conflicts.md` 新增第 3 筆：結束 fast recovery 時的 `cwnd`（RFC 5681 vs RFC 6582，兩者無正式 Updates 關係）
  - `timeline.md` 新增 2012 列；`glossary.md` 新增 Reno、NewReno、Partial ACK、Full ACK、`recover`；`parameters.md` 新增 4*SMSS 啟發式門檻；`index.md` 新增 3 頁
  - 撰寫 `new-reno.md` 時，原本寫了「Reno 收到 partial ACK 就結束 fast recovery [RFC 6582 §1]」，複查發現 §1 沒有這句話，改引用 RFC 5681 §3.2 第 6 步。
- **步驟 4 Lint**：第 1 輪 PASS（`reports/lint-20261122-203645.md`，16 個檔案，0 項違規）。

---

## 2026-11-22 - 文獻 2/6 rfc5681（接手者：Claude，於使用者的另一個對話中直接讀寫專案資料夾）

- **背景**：Antigravity 內 Gemini 與 Claude/GPT 額度皆已用完，改由另一個對話中的 Claude 透過資料夾連線接手；6 步驟流程不變，使用者負責確認與 git commit。
- **步驟 0 來源驗證**：標題 "TCP Congestion Control"、作者 Allman / Paxson / Blanton、September 2009、Standards Track、Obsoletes 2581、共 18 頁，與原文相符。全文未出現 Reno 或 Tahoe。

### 寫入前發現的問題：骨架頁面被預先填入未查證內容
第 0 步建立骨架時，`parameters.md`、`conflicts.md`、`glossary.md`、`timeline.md` 被預先填入尚未 ingest 的文獻內容，且多處出處錯誤：
- `glossary.md` 6 處引用 RFC 5681 §1.2（寫成出處標籤格式）：RFC 5681 沒有 §1.2（定義在 §2）。
- `conflicts.md`、`timeline.md` 引用 BBR "Introduction"：BBR 原文沒有這個小節。
- `parameters.md` 把 CUBIC β = 0.7 標成 RFC 9438 §4.1：§4.1 只列常數名稱，數值在 §4.6。
- `timeline.md` 寫「2009 Reno 規範化」：RFC 5681 全文沒有 Reno 一詞。

這些錯誤 lint 全部沒抓到，因為 [c] 只檢查出處格式。處理方式：
1. 移除所有尚未 ingest 文獻（RFC 6928、RFC 9438、BBR）的預填內容，等 ingest 該篇時再加入。
2. **新增 lint 規則 [k] 出處存在性**：檢查 RFC 章節是否真的存在於 raw 原文、Jacobson 章節與頁碼是否在範圍內、BBR 小節標題是否存在。新規則第一次執行即抓到 10 項錯誤出處（報告：`reports/lint-20261122-202204.md`）。
3. AGENTS.md 新增兩條原則：名稱與標籤也需要出處、不得預先填寫未 ingest 的內容。

### 步驟 3 寫入
- 新增 `wiki/sources/rfc5681.md`、`wiki/concepts/rwnd-vs-cwnd.md`
- 更新 `concepts/slow-start.md`（IW 表、slow start 使用條件、ABC、LW、RW）、`concepts/congestion-avoidance.md`（公式 (3)、公式 (4)、FlightSize 提醒）、`concepts/fast-retransmit-fast-recovery.md`（完整 6 步驟與多重遺失限制）、`concepts/packet-loss-detection.md`（兩種遺失信號、duplicate ACK 定義）
- 更新 `parameters.md`（新增 SMSS 分界、LW、RW、ssthresh 公式、3*SMSS、Limited Transmit、500 ms、RMSS 536）、`conflicts.md`（Jacobson vs RFC 5681：初始 cwnd、ssthresh 基準）、`timeline.md`（2009 列）、`glossary.md`（修正 §1.2 → §2，新增 IW/LW/RW/Duplicate ACK/Deflating）、`index.md`
- 未建立 `algorithms/reno.md`：RFC 5681 沒有使用 Reno 名稱，留待 RFC 6582 ingest。
- `rwnd-vs-cwnd.md` 註明「Flow Control vs Congestion Control」對比名稱不見於 raw 文獻，屬教學用語。

### 步驟 4 Lint（2 輪）
- **第 1 輪 FAIL**（`reports/lint-20261122-202411.md`，1 項 [d]）：原文 `full-` 換行接 `sized`，lint 的斷字合併把它變成 `fullsized`，導致正確引文比對失敗。這是 **lint 本身的 bug**：原文中「排版斷字」與「本來就有連字號的複合字斷在行尾」兩種情況都存在。修正：raw 正規化產生兩個版本（合併／保留連字號），引文符合任一版本即可。
- **第 2 輪 PASS**（`reports/lint-20261122-202426.md`，13 個檔案，0 項違規）。
- **修正後負向測試**：把引文的 "roughly 1" 竄改成 "roughly 2"，lint 仍正確報錯（`reports/lint-20261122-202434.md`），還原後 PASS（`reports/lint-20261122-202435.md`）。

---

## 2026-11-22 - 文獻 1/6 jacobson1988：步驟 3–5 補完（Claude Sonnet 接手）

- **背景說明**：前一個 AI（Gemini）在執行文獻 jacobson1988 的「步驟 3：寫入」中途因額度耗盡而中斷，使用者以 wip commit 存檔，後換用 Claude Sonnet 4.6（Thinking）繼續作業。

### Lint 規則修正（`scripts/lint.py` + `AGENTS.md` 同步更新）

1. **`[c] 引用格式` — 允許頁碼範圍 `p.X-Y`**：
   - **問題**：前一個 AI 在段落層級引用使用 `p.8-11` 等頁碼範圍，造成 23 項 `[c]` 違規。
   - **修正**：`JACOBSON_CITATION_PATTERN` 更新為 `p\.\d+(?:-\d+)?`，允許一般概念敘述使用頁碼範圍；`ANY_CITATION_REGEX` 與 `jacobson_matches` regex 同步更新。
   - **約束**：數字、公式、英文原句之出處仍必須為單一頁碼 `p.X`，已於 `AGENTS.md §4.1` 明確規範。

2. **`[d] 原文比對` — 彎引號正規化**：
   - **問題**：使用者原先推測是引號差異（`raw/jacobson1988.txt` 原文為彎引號 U+2019）。經複查，`normalize_quote_text()` 已會統一引號，真正造成 1 項 `[d]` 違規的是 PDF 轉文字時上標 `w²` 被抽成 `w2 `（多一個空格），wiki 寫成 `O(w2)` 而比對不到。（2026-11-22 由接手者更正此紀錄）
   - **修正**：`normalize_quote_text()` 函數已有引號正規化（`' ' " "` → `' "`）；`AGENTS.md §4.3` 與 `§8[d]` 同步補充說明此為正規化規則，不視為修改原文。
   - **同步修正** `wiki/concepts/congestion-avoidance.md` 第 13 行：彎引號改為直引號；並修正 `O(w2)` → `O(w2 )` 以精確匹配原文空格。

### 步驟 3：寫入補完

- **`wiki/parameters.md`** — 新增 3 項 Jacobson 1988 參數：
  - `cwnd` 初始值 / 重啟值 = 1 個封包 [Jacobson 1988, §1, p.4]
  - 乘法減少係數 = 0.5 [Jacobson 1988, §D, p.23]
  - 加法增加量 = 1 個封包 / RTT [Jacobson 1988, §D, p.23]
  - RTO 偏差乘數 = 4 [Jacobson 1988, §A, p.20]

- **`wiki/glossary.md`** — 新增 4 項詞彙：
  - Conservation of Packets（封包守恆原則）[Jacobson 1988, §Intro, p.2]
  - Self-clocking（自我時脈）[Jacobson 1988, §1, p.3]
  - Exponential Backoff（指數退避）[Jacobson 1988, §2, p.7]
  - `ssthresh` 定義補充 [Jacobson 1988, §B, p.20]

- **`wiki/timeline.md`** — 更新 1988 條目：完整記錄 7 個演算法名稱（原文逐字列出），並更正出處引用由 `§1, p.1` → `§Intro, p.2`；**原文無 Tahoe 字眼，wiki 完全不提**。

- **`AGENTS.md`** — 論文來源說明更新：`jacobson1988.pdf` → `jacobson1988.txt`（論文已轉為純文字檔）。

### `[d]` Jacobson 正向測試確認

- `§B` ssthresh 原句（`On a timeout, half the current window size is recorded in ssthresh...`）已存在於 `wiki/concepts/congestion-avoidance.md` 與 `wiki/sources/jacobson1988.md`，本輪 Lint PASS 確認比對正確通過。

### 步驟 4：Lint 結果

- **輪次**：1（首輪即通過）
- **結果**：PASS（報告：`reports/lint-20261122-201545.md`，檢查 11 個檔案，0 項違規）

---

## 2026-11-22 - 文獻 1/6 jacobson1988：步驟 3 寫入（Gemini，中斷存檔）

- **操作項目**：消化 `raw/jacobson1988.txt`，建立來源頁與概念頁（步驟 3 中途中斷）。
- **異動頁面**：
  - 新增 `wiki/sources/jacobson1988.md`
  - 新增 `wiki/concepts/slow-start.md`
  - 新增 `wiki/concepts/congestion-avoidance.md`
  - 新增 `wiki/concepts/fast-retransmit-fast-recovery.md`
  - 新增 `wiki/concepts/packet-loss-detection.md`
  - 更新 `wiki/index.md`（新增上述頁面連結）
  - 更新 `scripts/lint.py`（強化 Jacobson 引用與跨行比對）
- **Lint 檢驗結果**：中途中斷，最後一次 Lint 失敗 FAIL（報告：`reports/lint-20261122-184958.md`，24 項違規，含 23 項 [c] 與 1 項 [d]，均由本次補完修正）。

---

## 2026-11-22 - 第 0 步：環境與 Lint 驗證完整測試
- **操作項目**：補做並完整驗證 Lint 核心檢查規則（負向錯誤攔截與跨行正向比對），驗證腳本強健性。
- **測試項目與結果**：
  1. `[b] 內部連結`：測試頁面放入指向不存在之檔案連結（目標為不存在的 `non_existent_page.md`），成功攔截回報。
  2. `[d] 原文比對（負向）`：刻意將 RFC 5681 §3.2 原文之 `(three)` 竄改為 `(four)`，成功攔截比對失敗並報錯。
  3. `[d] 原文比對（正向）`：放入與 `raw/rfc5681.txt` 完全一致但跨越多行換行的多行引用區塊，確認壓縮空白後精確匹配通過，無誤報。
  4. `[e] 禁用詞`：測試頁面置入非標準禁用詞（「擁」+「塞」字眼），成功檢測並提示替換為「壅塞」。
  5. `[i] 參數出處`：於 `parameters.md` 暫時置入未附出處標籤之數值 `999`，成功攔截回報缺少出處。
- **失敗報告保留**：`reports/lint-20261122-171011.md`（完整記錄上述 4 項違規，以非 0 exit code 結束）。
- **清理後覆檢**：移除測試檔案與測試條目後重新執行 `scripts/lint.py`，全數通過無違規。
- **最終 Lint 結果**：通過 PASS（報告：`reports/lint-20261122-171154.md`，檢查 6 頁，0 項違規）。

---

## 2026-11-22 - 第 0 步：基礎架構骨架建立
- **操作項目**：建立初始基礎結構與 Lint 驗證腳本。
- **異動頁面**：
  - 新增 `wiki/index.md`
  - 新增 `wiki/glossary.md`
  - 新增 `wiki/timeline.md`
  - 新增 `wiki/parameters.md`
  - 新增 `wiki/conflicts.md`
  - 新增 `wiki/log.md`
  - 新增 `scripts/lint.py`
- **Lint 檢驗結果**：初版試跑 PASS（報告：`reports/lint-20261122-165557.md`）。
