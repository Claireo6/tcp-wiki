# 異動與審查日誌（Log）

本文件按時間倒序記錄知識庫之所有文件消化（Ingestion）、頁面異動以及自動化檢驗（Lint）執行結果。

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
