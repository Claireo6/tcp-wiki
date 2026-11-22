# 獨立 AI 忠實度審查報告（2026-11-22）

- **審查者**：Gemini 網頁版（gemini.google.com），全新對話；與作者（Claude）不同模型，未看過製作過程
- **提供給審查者的資料**：`review-bundle.txt`（slides/index.html、wiki/*.md、raw/*.txt 合併成單一檔），以及 `reports/review-prompt.md` 的審查 prompt
- **受審版本**：簡報修訂版（正文上限 180 字）

## 作者處理結果

| 頁 | 審查意見摘要 | 判斷 | 處理 |
| :--- | :--- | :--- | :--- |
| 10 | 重傳率「0.3% / 0.7%」應為百分點（1.98%→2.29%、3.54%→4.21%），易誤解為相對增幅 | **錯誤（源頭在 wiki）** | 退回 wiki：修正 `wiki/parameters.md` 與 `wiki/sources/rfc6928.md`，再修簡報第 10 頁 |
| 8 | 狀態圖寫 `cwnd ≥ ssthresh`，RFC 5681 為 `>`；「cwnd 從 ssthresh 附近繼續」不精確 | 接受 | 圖改為 `cwnd > ssthresh`；步驟改為「cwnd 先設為 ssthresh 加 3 個區段」 |
| 11 | 「遇到壅塞乘 0.7」不精確：β 是乘在在途量上得到 ssthresh；圖省略 Reno-friendly 與 1.5 倍上限 | 接受 | 改為「ssthresh 設為在途量乘 0.7」；details 註明圖只呈現形狀 |
| 5 | 未說明相等時的情況；details 提到 RFC 6928 但未標出處 | 接受 | 加「剛好相等時兩種都可以」；補 RFC 6928 §1 出處 |
| 6 | 主文未呈現 ssthresh 下限 2*SMSS | 接受 | 加「但不小於 2 個區段」 |
| 2 | 計時器說明過度簡化，原文重點是未考慮 RTT 變動 | 接受 | 改為「重傳計時器沒有考慮往返時間的變動」 |
| 9 | 提到 Tahoe，但 data-src 頁面未討論 Tahoe | 接受 | data-src 補上 `wiki/sources/rfc6582.md` |
| 12 | 「粗細」應依原文用「直徑」 | 接受 | 改為「直徑」 |
| 1 | 先備知識不在 wiki/index.md | 接受（說明） | details 註明先備知識依專案設定的目標讀者列出 |
| 7 | 模擬省略 fast recovery 膨脹／縮回，遺失條件為示意 | 不修改 | details 已明確說明為簡化示意，且這是為了讓初學者看清兩種反應的差異 |

修正後：lint --slides PASS（`reports/lint-20261122-212703.md`）、渲染檢查 PASS（`reports/render-20261122-212709.md`）。

## 審查者原文

以下針對 `slides/index.html` 共 13 頁投影片（含 `<details>` 補充區塊、SVG 圖表與 `<script>` 模擬邏輯）逐頁進行技術與忠實度審查：

| 頁 | 問題 | 嚴重度（錯誤／不精確／建議） | 依據（wiki 或 raw 的位置） |
| --- | --- | --- | --- |
| 1 | 列出「封包交換、TCP 三向交握、序號與 ACK（確認）」為先備知識，但 `data-src` 指定的 `wiki/index.md` 僅為目錄索引，未定義這些先備知識項目。 | 建議 | `slides/index.html`（第 1 頁 `data-src="wiki/index.md"`）、`wiki/index.md` |
| 2 | 正文提到重傳計時器設得太短會把排隊延遲誤當遺失並重送未遺失封包；原文與 wiki 更精確指出固定倍數計時器在負載較高時無法適應 RTT 變異而導致偽重傳，且重傳退避與逾時偵測在各節有各自脈絡。 | 建議 | `slides/index.html`（第 2 頁）、`wiki/sources/jacobson1988.md`（§2）、`raw/jacobson1988.txt`（§2, p.7 & Appendix A） |
| 5 | 第 4 點寫「`cwnd` 超過門檻 `ssthresh` 後，改用壅塞避免」；RFC 5681 規範 `cwnd < ssthresh` 時用 slow start、`cwnd > ssthresh` 時用 congestion avoidance（相等時可任選其一），而 Jacobson 1988 則以 `cwnd >= ssthresh` 切換。此外 `<details>` 提及 `RFC 6928`（IW10）與 `RTT`，但出處列僅標示 `[Jacobson 1988, §1, p.4]` 與 `[RFC 5681 §3.1]`。 | 不精確 | `slides/index.html`（第 5 頁）、`wiki/concepts/slow-start.md`、`raw/rfc5681.txt`（§3.1）、`raw/jacobson1988.txt`（Appendix B, p.20） |
| 6 | 右欄寫「門檻 `ssthresh` 降為在途資料量的一半」，未呈現 RFC 5681 的下限 `2*SMSS`（`max(FlightSize/2, 2*SMSS)`），雖在 `<details>` 有補充，但主卡片敘述略顯簡化。 | 建議 | `slides/index.html`（第 6 頁）、`wiki/concepts/congestion-avoidance.md`、`wiki/parameters.md`、`raw/rfc5681.txt`（§3.1, Eq. 4） |
| 7 | `<script>` 中 `simulate(mode)` 在 `dupack` 模式下於 `cwnd > capacity` 觸發遺失後直接將 `cwnd` 設為 `ssthresh`，未模擬 RFC 5681 fast recovery 期間的視窗膨脹（`ssthresh + 3*SMSS` 與後續重複 ACK 膨脹）與收到新 ACK 後縮回（deflate）；此外模擬以 `cwnd > capacity`（20）作為遺失條件並以 `cwnd` 推算 `ssthresh`，屬於簡化示意模型（`<details>` 已說明省略膨脹與容量為示意）。 | 不精確 | `slides/index.html`（第 7 頁 `<script>` `simulate` 與 `<details>`）、`wiki/concepts/packet-loss-detection.md`、`raw/rfc5681.txt`（§3.1–3.2） |
| 8 | SVG 狀態圖中「慢啟動 → 壅塞避免」標示 `cwnd ≥ ssthresh`，與 RFC 5681 §3.1 的 `cwnd > ssthresh` 略有出入（較貼近 Jacobson 1988 Appendix B 的 `>=`）；另第 2 點文字「`cwnd` 從 `ssthresh` 附近繼續」在 RFC 5681 §3.2 實作中進入 fast recovery 時是設為 `ssthresh + 3*SMSS` 並隨重複 ACK 膨脹，結束時才縮回 `ssthresh`。 | 不精確 | `slides/index.html`（第 8 頁 SVG 與步驟 2）、`wiki/concepts/fast-retransmit-fast-recovery.md`、`raw/rfc5681.txt`（§3.1, §3.2） |
| 9 | `<details>` 提到「常見的『Tahoe』在本教材的文獻中沒有定義，所以不使用」，但 `data-src` 指定的 `wiki/algorithms/new-reno.md` 未討論 Tahoe（僅 `wiki/sources/rfc6582.md` 提及參考文獻標題含 Tahoe）。 | 建議 | `slides/index.html`（第 9 頁 `<details>`）、`wiki/algorithms/new-reno.md`、`wiki/sources/rfc6582.md` |
| 10 | 寫「重傳率小幅上升 0.3% 與 0.7%」；RFC 6928 §10.2 實際呈現的是 AvgDC 重傳率由 1.98% 升至 2.29%（增加約 0.3 個百分點）、SlowDC 由 3.54% 升至 4.21%（增加約 0.7 個百分點），表述上易被誤解為相對增幅。 | 不精確 | `slides/index.html`（第 10 頁）、`wiki/parameters.md`、`wiki/sources/rfc6928.md`（§10.2）、`raw/rfc6928.txt`（§10.2, p.12） |
| 11 | 1) 正文寫「遇到壅塞乘 0.7」，RFC 9438 §4.6 定義 `β_cubic = 0.7` 用於計算 `ssthresh = flight_size * β_cubic`，而 `cwnd` 降為 `max(ssthresh, 2)`（逾時則依 Reno 降為 1 區段並以 `β_cubic` 算 `ssthresh`）。<br>

<br>2) `<script>` 繪製 `cubic-chart` 時以 `start = Wmax * beta` 代入 `K = Math.cbrt((Wmax - start) / C)`，並未呈現 RFC 9438 §4.2 的 `target` 上下限（`1.5 * cwnd`）與 §4.3 的 Reno-friendly `W_est` 切換，僅為曲線形狀示意。 | 不精確 | `slides/index.html`（第 11 頁文字與 `<script>` `cubic-chart`）、`wiki/algorithms/cubic.md`、`wiki/parameters.md`、`raw/rfc9438.txt`（§4.2–4.8） |
| 12 | `BtlBw` 比喻寫為「像水管最細處的粗細」；`wiki/algorithms/bbr.md` 與 `raw/bbr2017.txt` 皆明確使用「直徑」而非籠統的「粗細」。 | 建議 | `slides/index.html`（第 12 頁）、`wiki/algorithms/bbr.md`、`raw/bbr2017.txt`（"Congestion and Bottlenecks", p.58） |

---

### 總評

整體而言，這份 13 頁的 HTML 簡報架構清楚、視覺互動設計（第 7 頁遺失信號切換模擬與第 11 頁 CUBIC 曲線）有助於大學生建立直覺，且核心參數（如 `DupThresh = 3`、`LW = 1`、`C = 0.4`、`β_cubic = 0.7`、`IW10` 10 區段／14600 位元組與 Google 實驗數據、BBR 2 Gbps vs. 15 Mbps）與 `wiki/parameters.md` 及原始文獻大致一致，未出現違背核心原理的重大錯誤或禁用詞違規；主要瑕疵集中在部分邊界條件（如 `>` 與 `>=`、fast recovery 的膨脹與縮回、`0.3% / 0.7%` 百分點差異）的簡化，以及圖表腳本對協定細節的省略。對初次接觸 TCP 壅塞控制的大學生而言，建議在講解第 7 頁與第 11 頁圖表時搭配口頭說明「此為簡化示意模型」，並補充說明 `ssthresh` 與 `cwnd` 在進入／離開恢復階段的差異，會更有助於建立精確心智模型。

**沒有發現問題的頁面：第 3 頁、第 4 頁、第 13 頁。**