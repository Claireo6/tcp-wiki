# 快速重傳與快速恢復（Fast Retransmit & Fast Recovery）

快速重傳（Fast Retransmit）讓 TCP 不必等到重傳計時器逾時，就能提早修復遺失的區段；快速恢復（Fast Recovery）則在重傳之後，控制新資料的送出方式 [RFC 5681 §3.2]。

## 文獻記載與歷史定位

Jacobson 與 Karels 1988 年的論文將 fast retransmit 列為已納入 4BSD TCP 的 7 個新演算法之一（項次 vii），但該文只詳述 (i) 至 (v)，fast retransmit 留待之後發表的 RFC 說明 [Jacobson 1988, §Intro, p.2]。RFC 5681 是目前 raw/ 中第一份完整規範這兩個演算法的文件 [RFC 5681 §3.2]。

## 觸發條件：3 個 duplicate ACK

接收端收到不按順序的區段時，應立即送出 duplicate ACK [RFC 5681 §3.2]。傳送端收到 3 個 duplicate ACK（中間沒有推進 `SND.UNA` 的 ACK）時，就把它視為區段遺失，不等計時器逾時直接重傳 [RFC 5681 §3.2]。

> The fast retransmit algorithm uses the arrival of 3 duplicate ACKs (as defined in section 2, without any intervening ACKs which move SND.UNA) as an indication that a segment has been lost. [RFC 5681 §3.2]

## 為什麼不退回 slow start

收到 duplicate ACK 除了代表有區段遺失，也代表**有區段已經離開網路、抵達接收端**，因此 ACK 時脈仍在運作，傳送端可以用縮小後的 `cwnd` 繼續送新資料，而不必像逾時那樣退回 slow start [RFC 5681 §3.2]。

> the receipt of the duplicate ACKs not only indicates that a segment has been lost, but also that segments are most likely leaving the network [RFC 5681 §3.2]

## Fast recovery 的 6 個步驟（RFC 5681）

1. 收到第 1、2 個 duplicate ACK 時，在接收視窗允許、且 `FlightSize` 不超過 `cwnd + 2*SMSS` 的情況下，可以送出尚未送過的新資料（Limited Transmit），但不改變 `cwnd` [RFC 5681 §3.2]。
2. 收到第 3 個 duplicate ACK 時，把 `ssthresh` 設為不超過 `max(FlightSize/2, 2*SMSS)` [RFC 5681 §3.2]。
3. 重傳從 `SND.UNA` 開始的遺失區段，並把 `cwnd` 設為 `ssthresh + 3*SMSS`；加上的 3 個區段代表已經離開網路、存在接收端的那 3 個區段（人為「膨脹」視窗）[RFC 5681 §3.2]。
4. 之後每多收到一個 duplicate ACK，`cwnd` 再增加 `SMSS` [RFC 5681 §3.2]。
5. 若 `cwnd` 與接收視窗允許，送出 1 個 `SMSS` 的新資料 [RFC 5681 §3.2]。
6. 收到確認新資料的 ACK 時，把 `cwnd` 設回 `ssthresh`，稱為「deflating」（縮回）視窗 [RFC 5681 §3.2]。

> The lost segment starting at SND.UNA MUST be retransmitted and cwnd set to ssthresh plus 3*SMSS. [RFC 5681 §3.2]

> When the next ACK arrives that acknowledges previously unacknowledged data, a TCP MUST set cwnd to ssthresh (the value set in step 2). This is termed "deflating" the window. [RFC 5681 §3.2]

## 已知限制：同一視窗多個遺失

RFC 5681 自己承認，這個演算法在同一批封包中有多個遺失時，通常無法有效率地恢復，並建議實作能處理這種情況的進階遺失修復演算法 [RFC 5681 §3.2] [RFC 5681 §4.3]。這正是下一篇 RFC 6582（NewReno）要解決的問題。

> Note: This algorithm is known to generally not recover efficiently from multiple losses in a single flight of packets [FF96]. [RFC 5681 §3.2]

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [RFC 5681 §3.2]
- [RFC 5681 §4.3]
