# 歧異與衝突對照表（Conflicts）

本頁面彙整跨文獻間不同標準、非正式演進提案（如 Standards Track vs Experimental）、或學術論文與工程標準間存在分歧之記錄。每一項目均標註兩方或以上之來源出處。

> 本頁只收錄**已 ingest** 文獻之間的歧異。

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

### 3. 結束 fast recovery 時的 `cwnd`
- **分歧描述**：RFC 5681 在收到確認新資料的 ACK 時一律把 `cwnd` 設回 `ssthresh`；RFC 6582 只在 full ACK 時結束 fast recovery，並允許兩種設定方式。RFC 6582 標頭只取代 RFC 3782，與 RFC 5681 沒有正式 Updates 關係，依規則列為歧異；不過 RFC 5681 本身建議實作能處理多重遺失的進階修復演算法。
- **來源一（Standards Track）**：收到確認先前未確認資料的 ACK 時，`cwnd` 設為 `ssthresh`（deflating）[RFC 5681 §3.2]；並建議採用如 RFC 3782 的進階修復演算法 [RFC 5681 §4.3]。
- **來源二（Standards Track）**：只有 full ACK 才結束 fast recovery，`cwnd` 設為 `min(ssthresh, max(FlightSize, SMSS) + SMSS)` 或 `ssthresh`；partial ACK 則繼續留在 fast recovery [RFC 6582 §3.2]。

### 4. 初始視窗（IW）上限
- **分歧描述**：Standards Track 的 RFC 5681 依 `SMSS` 規定 IW 上限為 2 至 4 個區段；Experimental 的 RFC 6928 提議提高到 10 個區段。RFC 6928 標頭沒有 Updates 欄位，屬於實驗性提案，主述仍以 RFC 5681 為準。
- **來源一（Standards Track）**：IW 上限為 2、3 或 4 個區段，視 `SMSS` 而定 [RFC 5681 §3.1]。
- **來源二（Experimental）**：IW 上限提高到 10 個區段（最多 14600 位元組），使用與否為選用 [RFC 6928 §1] [RFC 6928 §2]。

### 5. SYN 或 SYN/ACK 遺失後的初始視窗
- **分歧描述**：RFC 5681 規定 SYN 遺失後初始視窗**必須**為 1 個區段；RFC 6928 則建議除非重傳超過一次或真的偵測到遺失，否則**不要**重設為 1。
- **來源一（Standards Track）**：SYN 或 SYN/ACK 遺失時，初始視窗必須為 1 個區段 [RFC 5681 §3.1]。
- **來源二（Experimental）**：建議不要把初始視窗重設為 1 個區段，除非 SYN 或 SYN/ACK 重傳超過一次 [RFC 6928 §2]。

> Further, if the SYN or SYN/ACK is lost, the initial window used by a sender after a correctly transmitted SYN MUST be one segment consisting of at most SMSS bytes. [RFC 5681 §3.1]

> For this reason, it is RECOMMENDED that implementations refrain from resetting the initial window to 1 segment, unless there have been more than one SYN or SYN/ACK retransmissions or true loss detection has been made. [RFC 6928 §2]

### 6. 乘法減少係數
- **分歧描述**：1988 論文的乘法減少係數為 0.5，RFC 9438 的 CUBIC 則使用 0.7。CUBIC 與 RFC 5681（Reno）之間是正式的 Updates 關係，已記錄於概念頁的「歷史演進」；此處記錄的是論文與 RFC 9438 之間的差異。
- **來源一（學術論文）**：0.5 的減少有較充分的理由，而 1 個封包的增加理由較弱 [Jacobson 1988, §D, p.23]。
- **來源二（Standards Track）**：CUBIC 把乘法減少係數設為 0.7，以在擴展性與收斂速度之間取得平衡；Reno 使用 0.5 [RFC 9438 §3.4]。

### 7. 壅塞信號：封包遺失 vs. 頻寬與延遲量測
- **分歧描述**：RFC 5681 與 RFC 9438 的演算法以封包遺失作為壅塞信號；BBR 認為封包遺失與壅塞只有弱相關，改以量測 BtlBw 與 RTprop 來控制。值得注意的是，RFC 9438 本身也承認 loss-based 演算法在封包遺失不能代表頻寬使用狀況的網路中表現較差。
- **來源一（Standards Track）**：本文件的演算法以封包遺失作為壅塞信號 [RFC 5681 §3]；CUBIC 同樣是 loss-based，在無線或行動網路中表現較差 [RFC 9438 §5.4]。
- **來源二（期刊文章）**：把封包遺失視為壅塞是 1980 年代技術限制下的設計選擇 [BBR 2017, "Congestion-Based Congestion Control", p.58]；BBR 改從 Kleinrock 的壅塞模型與最佳操作點出發 [BBR 2017, "Conclusion", p.66]。

## 參考來源
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §B, p.20]
- [RFC 5681 §3.1]
- [RFC 5681 §3.2]
- [RFC 5681 §4.3]
- [RFC 6582 §3.2]
- [RFC 6928 §1]
- [RFC 6928 §2]
- [Jacobson 1988, §D, p.23]
- [RFC 9438 §3.4]
- [RFC 5681 §3]
- [RFC 9438 §5.4]
- [BBR 2017, "Congestion-Based Congestion Control", p.58]
- [BBR 2017, "Conclusion", p.66]
