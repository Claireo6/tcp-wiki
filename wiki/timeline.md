# TCP 壅塞控制歷史演進時間軸

本頁面彙整 TCP 壅塞控制各代演算法之誕生年份、解決之前代痛點以及正式標準文件更新（`Updates` / `Obsoletes`）脈絡。

## 演進總覽

| 年份 | 演算法 / 提案 | 關鍵痛點與解決方案 | 正式文獻與關係 |
| :--- | :--- | :--- | :--- |
| 1988 | Jacobson 演算法（7 項） | 解決 1986 年網際網路「壅塞崩潰（Congestion Collapse）」問題，提出封包守恆原則，並將以下 7 個新演算法實作於 4BSD TCP：(i) 往返時間變異量估算（RTT variance estimation）、(ii) 指數型重傳計時器退避（Exponential retransmit timer backoff）、(iii) 慢啟動（Slow-start）、(iv) 更主動的接收端確認策略（More aggressive receiver ACK policy）、(v) 發生壅塞時之動態視窗調整（Dynamic window sizing on congestion）、(vi) Karn 箝位重傳退避演算法（Karn's clamped retransmit backoff）、(vii) 快速重傳（Fast retransmit） | [Jacobson 1988, §Intro, p.2] |
| 2009 | Reno 規範化 | 標準化 slow start、congestion avoidance、fast retransmit 與 fast recovery 核心機制 | [RFC 5681 §1] |
| 2012 | NewReno | 解決 Reno 在單一視窗遺失多個封包時頻繁逾時（Timeout）退回 slow start 的問題，支援 Partial ACK 處理 | [RFC 6582 §1] |
| 2013 | IW10 提案 | 解決現代 Web 傳輸延遲過長問題，提議將 Initial Window 擴大至 10 個區段（實驗性提案） | [RFC 6928 §1] |
| 2016 | BBR 概念提出 | 解決 Bufferbloat 造成的過度延遲與將隨機封包遺失誤判為壅塞的問題，以頻寬與延遲量測模型取代封包遺失回饋 | [BBR 2016, "Introduction"] |
| 2023 | CUBIC 標準化 | 解決古典 TCP 在高速長距離（High-BDP）網路中頻寬恢復過慢的問題，以三次曲線取代線性探測 | [RFC 9438 §1] |

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [RFC 5681 §1]
- [RFC 6582 §1]
- [RFC 6928 §1]
- [BBR 2016, "Introduction"]
- [RFC 9438 §1]
