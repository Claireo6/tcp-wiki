# 簡報大綱（Graph 節點：大綱 → 待人工確認）

主題：**網路為什麼會塞車？TCP 壅塞控制入門**
讀者：修過基礎計概、但沒學過 TCP 壅塞控制的大學生（AGENTS.md §2）
形式：單一 HTML、自修教材型、每頁正文 ≤ 100 字，細節放 `<details>`（AGENTS.md §9）

## 覆蓋率關卡結果
每一頁都至少對應 1 個 wiki 頁面，且該頁面的內容都有出處；沒有任何一頁需要 wiki 以外的知識。

| # | 投影片 | 教學目的 | 對應 wiki 頁（data-src） | 視覺元素 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 網路為什麼會塞車？ | 開場與路線圖 | `wiki/index.md` | — |
| 2 | 1986：網路真的塞爆了 | 用真實事件建立動機 | `wiki/sources/jacobson1988.md` | 大數字對比 |
| 3 | 兩個視窗：rwnd 與 cwnd | 先釐清最常混淆的概念 | `wiki/concepts/rwnd-vs-cwnd.md` | 對照表 |
| 4 | 封包守恆與 ACK 時脈 | 理解「為什麼需要 slow start」 | `wiki/concepts/slow-start.md` | — |
| 5 | Slow start：從小開始、每輪翻倍 | slow start 規則與 IW | `wiki/concepts/slow-start.md` | — |
| 6 | Congestion avoidance：加法增、乘法減 | AIMD 與 ssthresh | `wiki/concepts/congestion-avoidance.md` | — |
| 7 | 兩種遺失信號 | timeout vs 3 dup ACK 的不同反應 | `wiki/concepts/packet-loss-detection.md` | **互動 cwnd 鋸齒圖**（可切換兩種情境） |
| 8 | Fast retransmit 與 fast recovery | 為什麼不必退回 slow start | `wiki/concepts/fast-retransmit-fast-recovery.md` | **狀態轉移圖** |
| 9 | Reno 的弱點與 NewReno | partial ACK 的概念 | `wiki/algorithms/new-reno.md` | — |
| 10 | IW10：把起跑點拉高（實驗性） | 標準 vs 實驗性提案 | `wiki/sources/rfc6928.md` | — |
| 11 | CUBIC：用時間畫出的三次曲線 | 先凹後凸的直覺 | `wiki/algorithms/cubic.md` | **CUBIC 曲線圖**（C = 0.4、β = 0.7） |
| 12 | BBR：遺失不等於壅塞 | 換一種思路 | `wiki/algorithms/bbr.md` | 水管比喻 |
| 13 | 總整理：35 年的演進 | 串起整個故事、常見誤解 | `wiki/timeline.md`、`wiki/conflicts.md` | 時間軸 |

## 教學主線
問題（1986 崩潰）→ 兩個視窗 → 怎麼起步（slow start）→ 怎麼穩定（AIMD）→ 出事怎麼辦（兩種遺失信號、fast recovery）→ 前人方法的弱點與改良（NewReno、IW10、CUBIC）→ 換個思路（BBR，作者之一正是 1988 年的 Jacobson）→ 總整理。

## 已知限制（寫給讀者的誠實說明）
- Tahoe 這個常見名稱在 raw/ 文獻中沒有定義，簡報不使用。
- 「Flow Control vs Congestion Control」對比名稱為教學用語，第 3 頁會標明。
- BBR 只講核心概念，不推導公式。
