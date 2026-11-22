# 快速重傳與快速恢復（Fast Retransmit & Fast Recovery）

快速重傳（Fast Retransmit）是 TCP 用於不等待計時器逾時、提早修復封包遺失的機制。

## 文獻記載與歷史定位

在 Jacobson 與 Karels 於 1988 年發表的論文中，作者將 fast retransmit 明確列為已實作並納入 4BSD TCP 中的 7 個新演算法之一（項次 vii）[Jacobson 1988, §Intro, p.2]。

然而，該篇論文在引言中特別聲明，該文僅重點闡述項次 (i) 至 (v) 及其背後原理，而 (vii) fast retransmit 將於即將發布之 ARPANET RFC 文件中另行專文說明 [Jacobson 1988, §Intro, p.2]。

因此，本論文僅列出此演算法名稱與實作歸屬，具體觸發條件、視窗調整細節與快速恢復（Fast Recovery）之機制，均留待後續正式 RFC 文件（如 RFC 5681）正式規範 [Jacobson 1988, §Intro, p.2]。

## 參考來源
- [Jacobson 1988, §Intro, p.2]
