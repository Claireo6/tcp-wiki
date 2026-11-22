# 詞彙對照表（Glossary）

本文件統整「TCP 壅塞控制」之標準中英文術語對照、變數代號與禁用詞清單。

## 1. 標準詞彙表

| 英文術語 / 變數 | 台灣繁體中文 | 簡短定義 | 來源依據 |
| :--- | :--- | :--- | :--- |
| `cwnd` | 壅塞視窗 | 傳送端依據網路承載能力所維護的視窗上限 | [RFC 5681 §2] |
| `rwnd` | 接收端視窗 | 接收端透過 TCP 標頭回傳之可用接收緩衝區大小 | [RFC 5681 §2] |
| `ssthresh` | 慢啟動門檻 | 區隔 slow start 與 congestion avoidance 之門檻值；逾時後設為當前視窗一半 | [RFC 5681 §2], [Jacobson 1988, §B, p.20] |
| `SMSS` | 傳送端最大區段大小 | 傳送端能傳輸的最大 TCP 區段大小（位元組） | [RFC 5681 §2] |
| `FlightSize` | 飛行中資料量 | 已送出但尚未收到累加確認（ACK）的資料量 | [RFC 5681 §2] |
| Slow Start | 慢啟動（Slow Start） | 連線初期或逾時後指數型擴增 `cwnd` 之機制 | [RFC 5681 §3.1] |
| Congestion Avoidance | 壅塞避免（Congestion Avoidance） | 線性探測可用網路頻寬之機制 | [RFC 5681 §3.1] |
| Fast Retransmit | 快速重傳（Fast Retransmit） | 收到三次重複 ACK 時不必等待逾時即重傳之機制 | [RFC 5681 §3.2] |
| Fast Recovery | 快速恢復（Fast Recovery） | 快速重傳後維持資料管線流動之視窗調整機制 | [RFC 5681 §3.2] |
| `IW`（Initial Window） | 初始視窗 | 三向交握完成後的 `cwnd` 大小 | [RFC 5681 §2] |
| `LW`（Loss Window） | 遺失視窗 | 重傳計時器偵測到遺失後的 `cwnd` 大小 | [RFC 5681 §2] |
| `RW`（Restart Window） | 重啟視窗 | 閒置一段時間後重新傳送時的 `cwnd` 大小 | [RFC 5681 §2] |
| Duplicate ACK | 重複確認 | 符合 RFC 5681 §2 五個條件、確認號未前進的 ACK | [RFC 5681 §2] |
| Deflating the window | 縮回視窗 | fast recovery 結束時把 `cwnd` 設回 `ssthresh` | [RFC 5681 §3.2] |
| Reno | Reno | RFC 5681 fast recovery 的典型實作，最早出現在 1990 BSD Reno 版本 | [RFC 6582 §1] |
| NewReno | NewReno | 修改 fast recovery 對 partial ACK 的反應，處理同一視窗多個遺失 | [RFC 6582 §1] |
| Partial ACK | 部分確認 | 只確認進入 fast retransmit 前已送出資料一部分的 ACK | [RFC 6582 §1] |
| Full ACK | 完全確認 | 確認到 `recover` 為止全部資料的 ACK，NewReno 收到後結束 fast recovery | [RFC 6582 §3.2] |
| `recover` | 恢復點 | fast recovery 結束前必須被確認的送出序號 | [RFC 6582 §2] |
| IW10 | 10 區段初始視窗 | RFC 6928 實驗性提案，把初始視窗上限提高到 10 個區段 | [RFC 6928 §1] |
| CUBIC | CUBIC | 以三次函數取代線性增長的壅塞控制演算法，Linux、Windows、Apple 的預設 | [RFC 9438 §1] |
| `W_max` | 上次壅塞點視窗 | 上一次壅塞事件發生前的 `cwnd` 大小 | [RFC 9438 §3.1] |
| `K` | 回到平台時間 | 視窗從目前大小長回 `W_max` 所需的時間 | [RFC 9438 §4.2] |
| Reno-friendly region | Reno 友善區域 | 三次函數比 Reno 慢時，CUBIC 直接跟隨 Reno 視窗的區域 | [RFC 9438 §4.3] |
| HyStart++ | HyStart++ | RFC 9438 建議 CUBIC 使用的 slow start 演算法 | [RFC 9438 §4.10] |
| BBR | BBR | Bottleneck Bandwidth and Round-trip propagation time；以量測兩參數取代遺失信號的壅塞控制 | [BBR 2017, "Congestion and Bottlenecks", p.60] |
| `BtlBw` | 瓶頸頻寬 | 路徑上最慢鏈路的頻寬（水管最窄處的直徑） | [BBR 2017, "Congestion and Bottlenecks", p.58] |
| `RTprop` | 往返傳播時間 | 不含排隊延遲的往返時間（水管的長度） | [BBR 2017, "Congestion and Bottlenecks", p.58] |
| BDP | 頻寬延遲乘積 | BtlBw × RTprop，最佳操作點的在途資料量 | [BBR 2017, "Characterizing the Bottleneck", p.60] |
| Bufferbloat | 緩衝區膨脹 | loss-based 演算法把大型瓶頸緩衝區塞滿造成的高延遲 | [BBR 2017, "Congestion-Based Congestion Control", p.58] |
| Pacing gain | 速率增益 | BBR 以 BtlBw 的倍數控制送出速率，>1 探測頻寬、<1 排除佇列 | [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.62] |
| Conservation of Packets | 封包守恆原則 | 在穩定平衡連線中，舊封包離開網路前不得注入新封包；傳送端以 ACK 作為時脈調節 | [Jacobson 1988, §Intro, p.2] |
| Self-clocking | 自我時脈 | 傳送端以接收端回傳的 ACK 為觸發信號送出新封包，使傳輸節奏對齊瓶頸鏈路速率 | [Jacobson 1988, §1, p.3] |
| Exponential Backoff | 指數退避 | 連續逾時重傳時將 RTO 區間每次加倍，以防止壅塞崩潰 | [Jacobson 1988, §2, p.7] |

## 2. 禁用詞對照表

本區塊定義專案禁用詞彙。`scripts/lint.py` 會自動掃描全庫 Markdown 與 HTML 檔案，出現下列非標準用語即回報錯誤：

| 禁用非標準用詞 | 規範標準用詞 | 說明 |
| :--- | :--- | :--- |
| 擁塞 | 壅塞 | 統一使用台灣繁體「壅塞」 |
| 數據包 | 封包 | 網路傳輸單位標準用詞為「封包」 |
| 帶寬 | 頻寬 | 通訊傳輸能量標準用詞為「頻寬」 |
| 三次握手 | 三向交握 | TCP 連線建立標準用詞為「三向交握」 |
| 緩存 | 緩衝區 | 記憶體暫存區域統一使用「緩衝區」 |
| 默認 | 預設 | 預設設定統一使用「預設」 |

## 參考來源
- [RFC 5681 §2]
- [RFC 5681 §3.1]
- [RFC 5681 §3.2]
- [Jacobson 1988, §Intro, p.2]
- [Jacobson 1988, §1, p.3]
- [Jacobson 1988, §2, p.7]
- [Jacobson 1988, §B, p.20]
- [RFC 6582 §1]
- [RFC 6582 §2]
- [RFC 6582 §3.2]
- [RFC 6928 §1]
- [RFC 9438 §1]
- [RFC 9438 §3.1]
- [RFC 9438 §4.2]
- [RFC 9438 §4.3]
- [RFC 9438 §4.10]
- [BBR 2017, "Congestion and Bottlenecks", p.58]
- [BBR 2017, "Congestion and Bottlenecks", p.60]
- [BBR 2017, "Characterizing the Bottleneck", p.60]
- [BBR 2017, "Congestion-Based Congestion Control", p.58]
- [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.62]
