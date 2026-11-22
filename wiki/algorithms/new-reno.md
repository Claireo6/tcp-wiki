# NewReno

NewReno 是對 RFC 5681 fast recovery 的修改，專門處理「同一視窗多個封包遺失」時 Reno 的問題；由於它是 Reno 一個小但重要的變化，因此稱為 NewReno [RFC 6582 §1]。適用於無法使用 SACK 的連線 [RFC 6582 §1]。

## 核心概念：partial ACK
多個封包遺失時，重傳區段換來的 ACK 只會確認進入 fast retransmit 前已送出資料的**一部分**，這種 ACK 稱為 partial acknowledgment [RFC 6582 §1]。依 RFC 5681 第 6 步，Reno 收到任何確認新資料的 ACK 就把 `cwnd` 縮回 `ssthresh`、結束 fast recovery [RFC 5681 §3.2]；NewReno 則依 Janey Hoe 的建議，把 partial ACK 視為「下一個區段也遺失了」的訊號並立即重傳 [RFC 6582 §1]。

## 新的狀態變數 `recover`
`recover` 記錄 fast recovery 結束前必須被確認的送出序號 [RFC 6582 §2]。

> When in fast recovery, this variable records the send sequence number that must be acknowledged before the fast recovery procedure is declared to be over. [RFC 6582 §2]

## 演算法（RFC 6582 §3.2）
1. **初始化**：`recover` 設為初始送出序號 [RFC 6582 §3.2]。
2. **3 個 duplicate ACK**：先檢查累積確認是否涵蓋超過 `recover`；若是，把 `recover` 設為目前送出的最高序號，進入 fast retransmit；若不是，不進入 fast retransmit、也不重設 `ssthresh` [RFC 6582 §3.2]。
3. **收到確認新資料的 ACK**，分兩種情況 [RFC 6582 §3.2]：
   - **Full ACK**（確認到 `recover` 為止的全部資料）：把 `cwnd` 設為 `min(ssthresh, max(FlightSize, SMSS) + SMSS)` 或 `ssthresh`，然後結束 fast recovery [RFC 6582 §3.2]。
   - **Partial ACK**：立即重傳第一個未確認的區段；`cwnd` 減去這次新確認的資料量，若確認量至少 1 個 `SMSS` 再加回 `SMSS`；**不離開** fast recovery。第一個 partial ACK 也要重設重傳計時器 [RFC 6582 §3.2]。
4. **逾時**：把目前送出的最高序號記到 `recover`，並結束 fast recovery [RFC 6582 §3.2]。

> If this ACK does *not* acknowledge all of the data up to and including recover, then this is a partial ACK. In this case, retransmit the first unacknowledged segment. [RFC 6582 §3.2]

## 與 Reno 的差異
| | Reno | NewReno |
| :--- | :--- | :--- |
| 收到 partial ACK | 縮回視窗、結束 fast recovery [RFC 5681 §3.2] | 重傳下一個未確認區段，留在 fast recovery [RFC 6582 §3.2] |
| 同一視窗多個遺失 | 常常逾時，或多次縮減視窗 [RFC 6582 §1] | 避免逾時與多次縮減視窗 [RFC 6582 §3.1] |

## 結論
沒有 SACK 的連線，重點是實作 NewReno 而不是 Reno [RFC 6582 §8]。

> That is, the important thing is to implement NewReno instead of Reno for a TCP connection without SACK; it is less important exactly which variant of NewReno is implemented. [RFC 6582 §8]

## 參考來源
- [RFC 5681 §3.2]
- [RFC 6582 §1]
- [RFC 6582 §2]
- [RFC 6582 §3.1]
- [RFC 6582 §3.2]
- [RFC 6582 §8]
