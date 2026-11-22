# 慢啟動（Slow Start）

慢啟動（Slow Start）是 TCP 用於在連線建立初期或封包遺失重啟時，逐步探測網路容量並建立傳輸節奏的核心機制 [Jacobson 1988, §1, p.2-5]。

## 核心設計理念：封包守恆與自我時脈

慢啟動演算法植根於「封包守恆原則（Conservation of Packets Principle）」[Jacobson 1988, §Intro, p.2]。在穩定平衡（equilibrium）的連線中，只有當舊封包離開網路後，傳送端才允許將等量的新封包注入網路 [Jacobson 1988, §Intro, p.2]。

傳送端透過接收端回傳的 ACK 作為「時脈（Self-clocking）」來調節送出封包的間隔，使其傳送節奏自然對齊路徑上最慢瓶頸鏈路的處理速率 [Jacobson 1988, §1, p.3]。然而，自我時脈機制在連線剛開始時面臨啟動困難（沒有流通的封包就沒有 ACK，沒有 ACK 就無法觸發送出新封包）[Jacobson 1988, §1, p.3]。慢啟動正是為了解決啟動 ACK 時鐘的問題而設計 [Jacobson 1988, §1, p.3]。

## 視窗調整規則

傳送端在連線狀態中引入壅塞視窗 `cwnd` [Jacobson 1988, §1, p.4]：
1. **初始值與重啟值**：連線剛開始或因逾時（Timeout）重啟時，將 `cwnd` 設為 1 個封包 [Jacobson 1988, §1, p.4]。
2. **ACK 驅動增長**：每收到一個針對新資料的 ACK，`cwnd` 增加 1 個封包 [Jacobson 1988, §1, p.4]。
3. **傳送上限**：傳送端實際送出的資料量不得超過接收端通告視窗與 `cwnd` 的較小者，即 $\min(\text{advertised window}, \text{cwnd})$ [Jacobson 1988, §1, p.4]。

> "• Add a congestion window, cwnd, to the per-connection state. • When starting or restarting after a loss, set cwnd to one packet. • On each ack for new data, increase cwnd by one packet. • When sending, send the minimum of the receiver’s advertised window and cwnd." [Jacobson 1988, §1, p.4]

在此機制下，每個往返傳輸時間（RTT）內，視窗將隨時間呈指數級擴增（每輪翻倍），開啟至視窗大小 $W$ 僅需耗時 $R \log_2 W$ [Jacobson 1988, §1, p.4]。

## 與門檻值（`ssthresh`）之切換

為了避免 slow start 無休止擴張導致嚴重壅塞，傳送端引入慢啟動門檻 `ssthresh` [Jacobson 1988, §B, p.20]。
- 當 `cwnd < ssthresh` 時，傳送端處於 slow start 狀態，持續以指數擴增視窗 [Jacobson 1988, §B, p.20]。
- 當 `cwnd >= ssthresh` 時，傳送端脫離 slow start，轉入壅塞避免階段，改以線性慢速探測頻寬 [Jacobson 1988, §B, p.20]。

## 連線閒置重設（Idle Reset）

若連線在一段時間內無任何在途資料（資料皆已確認）且閒置時間超過 $RTO$（`idle && now - lastsnd > rto`），網路管線已排空，ACK 時脈亦已消失 [Jacobson 1988, §C, p.22]。此時若直接發送全視窗封包會形成突發衝擊，因此必須將 `cwnd` 重設為 1 個封包，強制重新進入 slow start 重新建立時脈 [Jacobson 1988, §C, p.22]。

## 參考來源
- [Jacobson 1988, §Intro, p.2]
- [Jacobson 1988, §1, p.3]
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §B, p.20]
- [Jacobson 1988, §C, p.22]
