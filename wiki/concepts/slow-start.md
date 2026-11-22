# 慢啟動（Slow Start）

慢啟動（Slow Start）是 TCP 用於在連線建立初期或封包遺失重啟時，逐步探測網路容量並建立傳輸節奏的核心機制 [Jacobson 1988, §1, p.2-5]。

## 核心設計理念：封包守恆與自我時脈

慢啟動演算法植根於「封包守恆原則（Conservation of Packets Principle）」[Jacobson 1988, §Intro, p.2]。在穩定平衡（equilibrium）的連線中，只有當舊封包離開網路後，傳送端才允許將等量的新封包注入網路 [Jacobson 1988, §Intro, p.2]。

傳送端透過接收端回傳的 ACK 作為「時脈（Self-clocking）」來調節送出封包的間隔，使其傳送節奏自然對齊路徑上最慢瓶頸鏈路的處理速率 [Jacobson 1988, §1, p.3]。然而，自我時脈機制在連線剛開始時面臨啟動困難（沒有流通的封包就沒有 ACK，沒有 ACK 就無法觸發送出新封包）[Jacobson 1988, §1, p.3]。慢啟動正是為了解決啟動 ACK 時鐘的問題而設計 [Jacobson 1988, §1, p.3]。

## 視窗調整規則

傳送端在連線狀態中引入壅塞視窗 `cwnd` [Jacobson 1988, §1, p.4]：
1. **初始值與重啟值**：連線剛開始或因逾時（Timeout）重啟時，將 `cwnd` 設為 1 個封包 [Jacobson 1988, §1, p.4]。
2. **ACK 驅動增長**：每收到一個針對新資料的 ACK，`cwnd` 增加 1 個封包 [Jacobson 1988, §1, p.4]。
3. **傳送上限**：傳送端實際送出的資料量不得超過接收端通告視窗與 `cwnd` 的較小者，即 $\min(\text{advertised window}, \text{cwnd})$ [Jacobson 1988, §1, p.4]。

> "• Add a congestion window, cwnd, to the per-connection state. • When starting or restarting after a loss, set cwnd to one packet. • On each ack for new data, increase cwnd by one packet. • When sending, send the minimum of the receiver’s advertised window and cwnd." [Jacobson 1988, §1, p.4]

在此機制下，每個往返傳輸時間（RTT）內，視窗將隨時間呈指數級擴增（每輪翻倍），開啟至視窗大小 $W$ 僅需耗時 $R \log_2 W$ [Jacobson 1988, §1, p.4]。

## 與門檻值（`ssthresh`）之切換

為了避免 slow start 無休止擴張導致嚴重壅塞，傳送端引入慢啟動門檻 `ssthresh` [Jacobson 1988, §B, p.20]。
- 當 `cwnd < ssthresh` 時，傳送端處於 slow start 狀態，持續以指數擴增視窗 [Jacobson 1988, §B, p.20]。
- 當 `cwnd >= ssthresh` 時，傳送端脫離 slow start，轉入壅塞避免階段，改以線性慢速探測頻寬 [Jacobson 1988, §B, p.20]。

## 連線閒置重設（Idle Reset）

若連線在一段時間內無任何在途資料（資料皆已確認）且閒置時間超過 $RTO$（`idle && now - lastsnd > rto`），網路管線已排空，ACK 時脈亦已消失 [Jacobson 1988, §C, p.22]。此時若直接發送全視窗封包會形成突發衝擊，因此必須將 `cwnd` 重設為 1 個封包，強制重新進入 slow start 重新建立時脈 [Jacobson 1988, §C, p.22]。

## RFC 5681 的正式規範（2009）

RFC 5681 將 slow start 規定為傳送端**必須**使用的演算法，用途是在網路狀況未知時慢慢探測可用容量，並啟動 ACK 時脈 [RFC 5681 §3.1]。

### 初始視窗（IW）
`IW` 的上限依 `SMSS` 大小而定 [RFC 5681 §3.1]：

| `SMSS` 大小 | `IW` 上限 |
| :--- | :--- |
| 大於 2190 位元組 [RFC 5681 §3.1] | 2 個區段 [RFC 5681 §3.1] |
| 大於 1095 且不超過 2190 位元組 [RFC 5681 §3.1] | 3 個區段 [RFC 5681 §3.1] |
| 不超過 1095 位元組 [RFC 5681 §3.1] | 4 個區段 [RFC 5681 §3.1] |

> If SMSS > 2190 bytes: IW = 2 * SMSS bytes and MUST NOT be more than 2 segments [RFC 5681 §3.1]

### 何時使用 slow start
- `ssthresh` 的初始值應設得任意高，讓網路狀況而不是主機設定決定傳送速率 [RFC 5681 §3.1]。
- `cwnd < ssthresh` 時使用 slow start；`cwnd > ssthresh` 時使用 congestion avoidance；兩者相等時可任選其一 [RFC 5681 §3.1]。

> The slow start algorithm is used when cwnd < ssthresh, while the congestion avoidance algorithm is used when cwnd > ssthresh. [RFC 5681 §3.1]

### 每個 ACK 增加多少
slow start 期間，每個確認新資料的 ACK 最多讓 `cwnd` 增加 `SMSS` 位元組；建議使用 `cwnd += min(N, SMSS)`，其中 N 為該 ACK 新確認的位元組數，可防止接收端以「ACK Division」手法灌大 `cwnd` [RFC 5681 §3.1]。

### 逾時後與閒置後
- 重傳計時器逾時後，`cwnd` 不得超過 loss window（LW），而 LW 等於 1 個完整區段，與 IW 大小無關；之後以 slow start 重新長回 `ssthresh` [RFC 5681 §3.1]。
- 超過一個重傳逾時時間沒有送出資料時，傳送前 `cwnd` 不得超過 restart window，RW = min(IW, cwnd) [RFC 5681 §4.1]。

> cwnd MUST be set to no more than the loss window, LW, which equals 1 full-sized segment (regardless of the value of IW). [RFC 5681 §3.1]

> For the purposes of this standard, we define RW = min(IW,cwnd). [RFC 5681 §4.1]

與 Jacobson 1988 的初始值差異（1 個封包 vs. 2～4 個區段）記錄於 [歧異與衝突對照表](../conflicts.md)。

## IW10：實驗性提案（RFC 6928，2013）

**注意：這是 Experimental 文件，不是正式標準。**RFC 6928 提議把初始視窗上限從 RFC 5681 的 2～4 個區段提高到 10 個區段，最多 14600 位元組，且使用與否為選用 [RFC 6928 §1] [RFC 6928 §2]。

> This document proposes to raise the upper bound on TCP's initial window (IW) to 10 segments (maximum 14600 B). [RFC 6928 §1]

- **為什麼要提高**：網頁物件變大 [RFC 6928 §5.2]，而網際網路上很大比例的流量是短的網頁交易，在離開 slow start 前就結束 [RFC 6928 §4]；IW 從 3 提高到 10，對超過 4 KB 的資料最多可省 4 個 RTT [RFC 6928 §5.1]。
- **哪些不變**：逾時後的 loss window 仍是 1 個區段 [RFC 6928 §2]。
- **部署限制**：沒有監控能力的系統不得預設開啟 [RFC 6928 §12]。

與 RFC 5681 的差異（IW 上限、SYN 遺失後是否重設 IW）記錄於 [歧異與衝突對照表](../conflicts.md)。

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [Jacobson 1988, §1, p.3]
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §B, p.20]
- [Jacobson 1988, §C, p.22]
- [RFC 5681 §3.1]
- [RFC 5681 §4.1]
- [RFC 6928 §1]
- [RFC 6928 §2]
- [RFC 6928 §4]
- [RFC 6928 §5.1]
- [RFC 6928 §12]
- [RFC 6928 §5.2]
