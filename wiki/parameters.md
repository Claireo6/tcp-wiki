# TCP 壅塞控制參數與常數索引

本頁面彙整專案所涉及的所有 TCP 壅塞控制常數、視窗初始值與演算法參數數值。所有出現之數值皆有文獻出處。

## 核心常數與參數清單

| 參數名稱 | 數值與定義 | 出處標籤 | 說明 |
| :--- | :--- | :--- | :--- |
| `DupThresh` | 3 [RFC 5681 §3.2] | [RFC 5681 §3.2] | 觸發快速重傳（Fast Retransmit）所需之連續重複 ACK 數量 |
| Initial Window (`IW`) | 2 [RFC 5681 §3.1] 至 4 [RFC 5681 §3.1] 個區段 | [RFC 5681 §3.1] | 古典標準中依 `SMSS` 大小計算之初始視窗 |
| Initial Window (`IW`) 實驗值 | 10 [RFC 6928 §1] 個區段 | [RFC 6928 §1] | 實驗性 RFC 建議之較大初始視窗 |
| CUBIC 縮減係數 $\beta_{cubic}$ | 0.7 [RFC 9438 §4.1] | [RFC 9438 §4.1] | 發生壅塞事件後視窗縮小之比例常數 |
| CUBIC 縮放常數 $C$ | 0.4 [RFC 9438 §4.1] | [RFC 9438 §4.1] | 決定三次曲線凹凸擴張速度之常數 |
| `cwnd` 初始值 / 重啟值 | 1 [Jacobson 1988, §1, p.4] 個封包 | [Jacobson 1988, §1, p.4] | 連線起始或逾時後重啟時 `cwnd` 之設定值 |
| 乘法減少（Multiplicative Decrease）係數 | 0.5 [Jacobson 1988, §D, p.23] | [Jacobson 1988, §D, p.23] | 偵測壅塞時將視窗縮減至原大小之比例（減半） |
| 加法增加（Additive Increase）量 | 1 [Jacobson 1988, §D, p.23] 個封包 / RTT | [Jacobson 1988, §D, p.23] | 無壅塞時每個 RTT 增加之視窗量（實作：每 ACK 增 `1/cwnd`） |
| RTO 偏差乘數 | 4 [Jacobson 1988, §A, p.20] | [Jacobson 1988, §A, p.20] | 重傳計時器計算公式 $RTO = a + 4v$ 中的偏差（mean deviation）乘數 |

## 參考來源
- [RFC 5681 §3.1]
- [RFC 5681 §3.2]
- [RFC 6928 §1]
- [RFC 9438 §4.1]
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §A, p.20]
- [Jacobson 1988, §D, p.23]
