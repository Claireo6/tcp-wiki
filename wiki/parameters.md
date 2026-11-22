# TCP 壅塞控制參數與常數索引

本頁面彙整專案所涉及的所有 TCP 壅塞控制常數、視窗初始值與演算法參數數值。所有出現之數值皆有文獻出處。

## 核心常數與參數清單

| 參數名稱 | 數值與定義 | 出處標籤 | 說明 |
| :--- | :--- | :--- | :--- |
| `DupThresh` | 3 [RFC 5681 §3.2] | [RFC 5681 §3.2] | 觸發快速重傳（Fast Retransmit）所需之連續重複 ACK 數量 |
| Initial Window (`IW`) | 2 [RFC 5681 §3.1] 至 4 [RFC 5681 §3.1] 個區段 | [RFC 5681 §3.1] | 古典標準中依 `SMSS` 大小計算之初始視窗 |
| `IW` 的 `SMSS` 分界 | 2190 [RFC 5681 §3.1] 與 1095 [RFC 5681 §3.1] 位元組 | [RFC 5681 §3.1] | `SMSS` 大於 2190 時 IW 上限 2 個區段；介於 1095 與 2190 之間為 3 個；不超過 1095 為 4 個 |
| Loss Window (`LW`) | 1 [RFC 5681 §3.1] 個完整區段 | [RFC 5681 §3.1] | 重傳計時器逾時後的 `cwnd` 上限，與 IW 無關 |
| Restart Window (`RW`) | min(IW, cwnd) [RFC 5681 §4.1] | [RFC 5681 §4.1] | 閒置超過一個 RTO 後重新傳送時的 `cwnd` 上限 |
| 逾時／遺失後的 `ssthresh` | max(FlightSize / 2 [RFC 5681 §3.1], 2*SMSS [RFC 5681 §3.1]) | [RFC 5681 §3.1] | 公式 (4)，使用 `FlightSize` 而非 `cwnd` |
| Fast recovery 視窗膨脹量 | 3*SMSS [RFC 5681 §3.2] | [RFC 5681 §3.2] | 進入 fast recovery 時 `cwnd = ssthresh + 3*SMSS` |
| Limited Transmit 上限 | FlightSize 不超過 cwnd + 2*SMSS [RFC 5681 §3.2] | [RFC 5681 §3.2] | 第 1、2 個 duplicate ACK 時可送新資料的條件 |
| Delayed ACK 最長延遲 | 500 [RFC 5681 §4.2] ms | [RFC 5681 §4.2] | 至少每 2 [RFC 5681 §4.2] 個完整區段回一個 ACK |
| 預設 `RMSS` | 536 [RFC 5681 §2] 位元組 | [RFC 5681 §2] | 未使用 MSS 選項時的接收端最大區段大小 |
| `cwnd` 初始值 / 重啟值 | 1 [Jacobson 1988, §1, p.4] 個封包 | [Jacobson 1988, §1, p.4] | 連線起始或逾時後重啟時 `cwnd` 之設定值 |
| 乘法減少（Multiplicative Decrease）係數 | 0.5 [Jacobson 1988, §D, p.23] | [Jacobson 1988, §D, p.23] | 偵測壅塞時將視窗縮減至原大小之比例（減半） |
| 加法增加（Additive Increase）量 | 1 [Jacobson 1988, §D, p.23] 個封包 / RTT | [Jacobson 1988, §D, p.23] | 無壅塞時每個 RTT 增加之視窗量（實作：每 ACK 增 `1/cwnd`） |
| RTO 偏差乘數 | 4 [Jacobson 1988, §A, p.20] | [Jacobson 1988, §A, p.20] | 重傳計時器計算公式 $RTO = a + 4v$ 中的偏差（mean deviation）乘數 |

## 參考來源
- [RFC 5681 §3.1]
- [RFC 5681 §3.2]
- [RFC 5681 §2]
- [RFC 5681 §4.1]
- [RFC 5681 §4.2]
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §A, p.20]
- [Jacobson 1988, §D, p.23]
