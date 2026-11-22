# 接收視窗與壅塞視窗（rwnd vs. cwnd）

TCP 傳送端同時受到兩個視窗限制：一個保護**接收端**，一個保護**網路**。初學者最常把兩者混為一談，本頁整理兩者差異。

## 兩個視窗的定義
- **`rwnd`（接收視窗）**：接收端最近一次通告的視窗，代表接收端還能容納多少資料，是「接收端這邊的上限」[RFC 5681 §2]。
- **`cwnd`（壅塞視窗）**：傳送端自行維護的狀態變數，限制在收到 ACK 之前能送進網路的資料量，是「傳送端這邊的上限」[RFC 5681 §3.1]。

> CONGESTION WINDOW (cwnd): A TCP state variable that limits the amount of data a TCP can send. [RFC 5681 §2]

## 實際傳送量取兩者的較小值
不論 1988 年的原始設計或現行標準，傳送端每次能送出的量都是兩個視窗的較小者：
- Jacobson 1988：傳送時送出「接收端通告視窗與 `cwnd` 的較小者」[Jacobson 1988, §1, p.4]。
- RFC 5681：`cwnd` 與 `rwnd` 的最小值決定資料傳送 [RFC 5681 §3.1]。

> The minimum of cwnd and rwnd governs data transmission. [RFC 5681 §3.1]

## 一句話區分
| | `rwnd` | `cwnd` |
| :--- | :--- | :--- |
| 保護對象 | 接收端的緩衝區 | 網路（路徑上的瓶頸） |
| 由誰決定 | 接收端通告 | 傳送端依壅塞控制演算法自行調整 |

上表整理自 [RFC 5681 §2] 與 [RFC 5681 §3.1] 對兩個變數的描述（receiver-side limit 與 sender-side limit）。

**註**：「流量控制（Flow Control）」與「壅塞控制（Congestion Control）」這組對比名稱是教學上的慣用說法，目前 raw/ 中的文獻並未以這組名稱並列比較兩個視窗，因此簡報使用時應標明為教學用語。

## 參考來源
- [RFC 5681 §2]
- [RFC 5681 §3.1]
- [Jacobson 1988, §1, p.4]
