# Reno

## 名稱由來
「Reno」不是 RFC 5681 使用的名稱。RFC 6582 說明：RFC 5681 所描述的 fast recovery 典型實作，最早出現在 1990 年的 BSD Reno 版本，並在 [FF96] 這篇文獻中被稱為「Reno algorithm」[RFC 6582 §1]。

> first implemented in the 1990 BSD Reno release, and referred to as the "Reno algorithm" in [FF96] [RFC 6582 §1]

因此本頁以「Reno」指稱 RFC 5681 的四個演算法（slow start、congestion avoidance、fast retransmit、fast recovery）的組合 [RFC 5681 §3]。

## 行為摘要
- 連線開始時使用 slow start，`cwnd` 超過 `ssthresh` 後改用 congestion avoidance [RFC 5681 §3.1]。詳見 [慢啟動](../concepts/slow-start.md)、[壅塞避免](../concepts/congestion-avoidance.md)。
- **逾時**：`ssthresh = max(FlightSize/2, 2*SMSS)`，`cwnd` 降為 1 個區段，重新 slow start [RFC 5681 §3.1]。
- **3 個 duplicate ACK**：fast retransmit 重傳遺失區段，進入 fast recovery，`cwnd = ssthresh + 3*SMSS`；收到確認新資料的 ACK 後把 `cwnd` 縮回 `ssthresh` [RFC 5681 §3.2]。詳見 [快速重傳與快速恢復](../concepts/fast-retransmit-fast-recovery.md)。

## 弱點：同一視窗多個遺失
- Reno 傳送端只在逾時或收到 3 個 duplicate ACK 時重傳，而每次 fast retransmit 只重傳 1 個區段 [RFC 6582 §1]。
- 同一視窗多個封包遺失時，Reno 常常逾時；即使沒有逾時，也可能發生多次 fast retransmit 與多次視窗縮減 [RFC 6582 §1]。RFC 5681 本身也承認這一點 [RFC 5681 §3.2]。

> Two problems arise with Reno TCP when multiple packet losses occur in a single window. [RFC 6582 §1]

改良版本見 [NewReno](new-reno.md)。

## 參考來源
- [RFC 5681 §3]
- [RFC 5681 §3.1]
- [RFC 5681 §3.2]
- [RFC 6582 §1]
