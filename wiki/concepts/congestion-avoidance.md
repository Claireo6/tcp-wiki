# 壅塞避免（Congestion Avoidance）

壅塞避免（Congestion Avoidance）是 TCP 在視窗越過安全門檻後，以保守速率線性探測網路剩餘可用頻寬的調節機制 [Jacobson 1988, §3, p.8-11]。

## 壅塞信號與控制模型

在多數網路路徑上，因硬體損壞導致的封包遺失極為罕見（通常小於 1%），因此封包遺失絕大多數是由網路佇列溢位所引發 [Jacobson 1988, §3, p.8]。傳送端可直接將「封包逾時（Packet timeout due to loss）」視為網路發生壅塞之客觀信號 [Jacobson 1988, §3, p.8-9]。

當網路進入壅塞狀態時，瓶頸佇列會呈指數級成長 [Jacobson 1988, §3, p.9]。為穩定系統，傳送端必須迅速抑制發送負載，其視窗控制策略必須遵循「加法增加 / 乘法減少（AIMD）」原則 [Jacobson 1988, §3, p.9-10]：
1. **乘法減少（Multiplicative Decrease）**：當偵測到壅塞信號時，視窗進行大幅度縮減，設定為原本視窗大小的 0.5 倍（即減半）[Jacobson 1988, §D, p.23]。
2. **加法增加（Additive Increase）**：當未偵測到壅塞信號時，視窗僅能以小幅常數進行線性增加，設定每個往返時間（RTT）增加 1 個封包 [Jacobson 1988, §D, p.23]。

> "The 1-packet increase has less justification than the 0.5 decrease. In fact, it's almost certainly too large. If the algorithm converges to a window size of w, there are O(w2 ) packets between drops with an additive increase policy." [Jacobson 1988, §D, p.23]

作者評析指出，0.5 的減少係數具備穩定網路佇列的理論保證，但 1 個封包的加法增量「幾乎肯定太大（almost certainly too large）」[Jacobson 1988, §D, p.23]。若未來 Gateway 能在佇列被推擠過膝點（knee）時提早執行封包丟棄以示警，此增量應再縮小約 4 倍 [Jacobson 1988, §D, p.23]。

## 演算法實作與狀態轉移

在 4BSD TCP 實作中，congestion avoidance 與 slow start 透過門檻變數 `ssthresh` 緊密結合 [Jacobson 1988, §B, p.20]：
- **進入條件**：當 `cwnd >= ssthresh` 時，傳送端停止指數增長，進入 congestion avoidance 階段 [Jacobson 1988, §B, p.20]。
- **視窗調整**：在 congestion avoidance 階段，每收到一個新資料 ACK，`cwnd` 僅增加 `1/cwnd` [Jacobson 1988, §B, p.20]。由於每個 RTT 約可收到 `cwnd` 個 ACK，整體視窗在一個 RTT 內剛好增加 1 個封包 [Jacobson 1988, §3, p.10-11]。
- **逾時懲罰**：一旦發生逾時，將當前視窗大小的一半（half the current window size）記錄至 `ssthresh` 作為新的安全門檻，隨後將 `cwnd` 重設為 1 個封包，重新退回 slow start [Jacobson 1988, §B, p.20]。

> "On a timeout, half the current window size is recorded in ssthresh (this is the multiplicative decrease part of the congestion avoidance algorithm), then cwnd is set to 1 packet (this initiates slow-start)." [Jacobson 1988, §B, p.20]

## 參考來源
- [Jacobson 1988, §3, p.8]
- [Jacobson 1988, §3, p.8-9]
- [Jacobson 1988, §3, p.9]
- [Jacobson 1988, §3, p.9-10]
- [Jacobson 1988, §3, p.10]
- [Jacobson 1988, §3, p.10-11]
- [Jacobson 1988, §B, p.20]
- [Jacobson 1988, §D, p.23]
