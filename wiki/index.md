# TCP 壅塞控制 Wiki 目錄

本索引列出知識庫中所有頁面與一句話摘要。

## 系統與索引頁面
- [詞彙對照表](glossary.md) - 標準專業術語定義與禁用詞檢驗對照表。
- [歷史演進時間軸](timeline.md) - TCP 壅塞控制演進歷史、痛點與 RFC 演進關係總覽。
- [參數與常數索引](parameters.md) - 關鍵常數、初始值與演算法參數數值清單。
- [歧異與衝突對照表](conflicts.md) - 各文獻與標準間未統一之歧異、學術論文與工程實作差異。
- [異動日誌](log.md) - 知識庫異動、文獻消化與自動化檢驗紀錄。

## 文獻摘要（Sources）
- [Congestion Avoidance and Control (Jacobson 1988)](sources/jacobson1988.md) - 奠定現代 TCP 壅塞控制基礎，提出慢啟動、AIMD 壅塞避免與 RTT 變異估算等 7 大演算法。
- [TCP Congestion Control (RFC 5681)](sources/rfc5681.md) - 2009 年 Standards Track，正式定義 slow start、congestion avoidance、fast retransmit、fast recovery。
- [The NewReno Modification to TCP's Fast Recovery Algorithm (RFC 6582)](sources/rfc6582.md) - 2012 年 Standards Track，以 partial ACK 處理同一視窗多個遺失。
- [Increasing TCP's Initial Window (RFC 6928)](sources/rfc6928.md) - 2013 年 Experimental，提議把初始視窗上限提高到 10 個區段。
- [CUBIC for Fast and Long-Distance Networks (RFC 9438)](sources/rfc9438.md) - 2023 年 Standards Track，Updates 5681，以三次函數取代線性增長。
- [BBR: Congestion-Based Congestion Control (BBR 2017)](sources/bbr2017.md) - 2017 年期刊文章，主張封包遺失不等於壅塞，改量測 BtlBw 與 RTprop。

## 核心機制（Concepts）
- [接收視窗與壅塞視窗](concepts/rwnd-vs-cwnd.md) - rwnd 保護接收端、cwnd 保護網路，實際傳送量取兩者較小值。
- [慢啟動](concepts/slow-start.md) - 依據封包守恆與 ACK 時脈指數級探測頻寬，初始與逾時後設 cwnd=1。
- [壅塞避免](concepts/congestion-avoidance.md) - 以封包逾時為壅塞信號，採加法增加（每 RTT 增 1）與乘法減少（減半 0.5）調節視窗。
- [快速重傳與快速恢復](concepts/fast-retransmit-fast-recovery.md) - 3 個 duplicate ACK 觸發重傳，fast recovery 6 步驟調整 cwnd；多個遺失時效率不佳。
- [封包遺失偵測](concepts/packet-loss-detection.md) - 逾時與 3 個 duplicate ACK 兩種遺失信號、RTO 估算（RTO=a+4v）與指數退避。

## 演算法（Algorithms）
- [Reno](algorithms/reno.md) - RFC 5681 四個演算法的組合，名稱來自 1990 BSD Reno 版本；多個遺失時常逾時。
- [NewReno](algorithms/new-reno.md) - 收到 partial ACK 時重傳下一個區段並留在 fast recovery。
- [CUBIC](algorithms/cubic.md) - 先凹後凸的三次函數增長，β = 0.7、C = 0.4，Linux/Windows/Apple 預設。
- [BBR](algorithms/bbr.md) - 量測瓶頸頻寬與往返傳播時間，讓在途量維持在 BDP 附近。
