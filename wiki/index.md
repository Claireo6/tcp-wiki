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

## 核心機制（Concepts）
- [慢啟動](concepts/slow-start.md) - 依據封包守恆與 ACK 時脈指數級探測頻寬，初始與逾時後設 cwnd=1。
- [壅塞避免](concepts/congestion-avoidance.md) - 以封包逾時為壅塞信號，採加法增加（每 RTT 增 1）與乘法減少（減半 0.5）調節視窗。
- [快速重傳與快速恢復](concepts/fast-retransmit-fast-recovery.md) - 1988 論文列為 4BSD TCP 7 大演算法之一，具體機制留待後續 RFC 規範。
- [封包遺失偵測](concepts/packet-loss-detection.md) - 介紹 RTO 均值與變異量估算（RTO=a+4v）、指數退避與早期快速重傳概念。

## 演算法（Algorithms）
（尚無演算法頁，待消化文獻時建立）
