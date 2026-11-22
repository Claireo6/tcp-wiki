# 歧異與衝突對照表（Conflicts）

本頁面彙整跨文獻間不同標準、非正式演進提案（如 Standards Track vs Experimental）、或學術論文與工程標準間存在分歧之記錄。每一項目均標註兩方或以上之來源出處。

> 本頁只收錄**已 ingest** 文獻之間的歧異。尚未 ingest 的文獻（RFC 6582、RFC 6928、RFC 9438、BBR）相關項目，會在 ingest 該篇時才加入。

## 歧異項目彙整

### 1. 連線開始時的 `cwnd` 初始值
- **分歧描述**：1988 論文在連線開始時把 `cwnd` 設為 1 個封包；RFC 5681 則允許初始視窗依 `SMSS` 大小上限為 2 至 4 個區段。兩者之間沒有正式的 Obsoletes/Updates 關係，依本專案規則列為歧異。
- **來源一（學術論文）**：開始或遺失後重新開始時，`cwnd` 設為 1 個封包 [Jacobson 1988, §1, p.4]。
- **來源二（Standards Track）**：`IW` 上限為 2 至 4 個區段，視 `SMSS` 而定 [RFC 5681 §3.1]。
- **補充**：兩者在「逾時之後」的行為一致，都降為 1（1 個封包 vs. 1 個完整區段的 LW）[Jacobson 1988, §B, p.20] [RFC 5681 §3.1]。

### 2. 偵測到壅塞時 `ssthresh` 的計算基準
- **分歧描述**：1988 論文記錄「當前視窗大小的一半」；RFC 5681 改用 `FlightSize / 2`（且不小於 `2*SMSS`），並明確指出直接使用 `cwnd` 是常見錯誤。
- **來源一（學術論文）**：逾時時，把當前視窗大小的一半記錄到 `ssthresh` [Jacobson 1988, §B, p.20]。
- **來源二（Standards Track）**：`ssthresh = max(FlightSize / 2, 2*SMSS)`，並提醒不要用 `cwnd` 取代 `FlightSize` [RFC 5681 §3.1]。

## 參考來源
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §B, p.20]
- [RFC 5681 §3.1]
