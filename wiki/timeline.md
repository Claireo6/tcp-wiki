# TCP 壅塞控制歷史演進時間軸

本頁面彙整 TCP 壅塞控制各代演算法之誕生年份、解決之前代痛點以及正式標準文件更新（`Updates` / `Obsoletes`）脈絡。

> 本頁只收錄**已 ingest** 的文獻；其餘文獻會在 ingest 時才加入，避免寫入未經查證的內容。

## 演進總覽

| 年份 | 文獻 | 關鍵痛點與解決方案 | 正式文獻與關係 |
| :--- | :--- | :--- | :--- |
| 1988 | Jacobson & Karels〈Congestion Avoidance and Control〉 | 解決 1986 年網際網路「壅塞崩潰（Congestion Collapse）」問題，提出封包守恆原則，並將以下 7 個新演算法實作於 4BSD TCP：(i) 往返時間變異量估算、(ii) 指數型重傳計時器退避、(iii) 慢啟動、(iv) 更主動的接收端確認策略、(v) 發生壅塞時之動態視窗調整、(vi) Karn 箝位重傳退避演算法、(vii) 快速重傳 | 學術論文，無 RFC 關係 [Jacobson 1988, §Intro, p.2] |
| 2009 | RFC 5681〈TCP Congestion Control〉 | 以標準文件定義 slow start、congestion avoidance、fast retransmit、fast recovery 四個演算法，並規範 IW、逾時後的 LW、閒置後的 RW 與 ACK 產生方式；自承在同一視窗多個遺失時恢復效率不佳 | Standards Track；Obsoletes 2581（2581 先前取代 2001）[RFC 5681 §1] |
| 2012 | RFC 6582〈The NewReno Modification to TCP's Fast Recovery Algorithm〉 | 解決 Reno 在同一視窗多個封包遺失時常常逾時、或多次縮減視窗的問題：收到 partial ACK 時立即重傳下一個區段並留在 fast recovery | Standards Track；Obsoletes 3782（RFC 5681 §4.3 推薦的 RFC 3782 即為其前一版）[RFC 6582 §1] |
| 2013 | RFC 6928〈Increasing TCP's Initial Window〉 | 網頁物件變大、多數短連線在離開 slow start 前就結束，小的初始視窗成為延遲瓶頸；提議把 IW 上限提高到 10 個區段 | **Experimental**；標頭無 Obsoletes / Updates [RFC 6928 §1] |

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [RFC 5681 §1]
- [RFC 6582 §1]
- [RFC 6928 §1]
