# 異動與審查日誌（Log）

本文件按時間倒序記錄知識庫之所有文件消化（Ingestion）、頁面異動以及自動化檢驗（Lint）執行結果。

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
