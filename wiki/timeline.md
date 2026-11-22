# TCP 壅塞控制歷史演進時間軸

本頁面彙整 TCP 壅塞控制各代演算法之誕生年份、解決之前代痛點以及正式標準文件更新（`Updates` / `Obsoletes`）脈絡。

> 本頁只收錄**已 ingest** 的文獻；其餘文獻會在 ingest 時才加入，避免寫入未經查證的內容。

## 演進總覽

| 年份 | 文獻 | 關鍵痛點與解決方案 | 正式文獻與關係 |
| :--- | :--- | :--- | :--- |
| 1988 | Jacobson & Karels〈Congestion Avoidance and Control〉 | 解決 1986 年網際網路「壅塞崩潰（Congestion Collapse）」問題，提出封包守恆原則，並將以下 7 個新演算法實作於 4BSD TCP：(i) 往返時間變異量估算、(ii) 指數型重傳計時器退避、(iii) 慢啟動、(iv) 更主動的接收端確認策略、(v) 發生壅塞時之動態視窗調整、(vi) Karn 箝位重傳退避演算法、(vii) 快速重傳 | 學術論文，無 RFC 關係 [Jacobson 1988, §Intro, p.2] |
| 2009 | RFC 5681〈TCP Congestion Control〉 | 以標準文件定義 slow start、congestion avoidance、fast retransmit、fast recovery 四個演算法，並規範 IW、逾時後的 LW、閒置後的 RW 與 ACK 產生方式；自承在同一視窗多個遺失時恢復效率不佳 | Standards Track；Obsoletes 2581（2581 先前取代 2001）[RFC 5681 §1] |

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [RFC 5681 §1]
