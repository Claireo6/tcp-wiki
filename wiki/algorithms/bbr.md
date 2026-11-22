# BBR

BBR 是 Bottleneck Bandwidth and Round-trip propagation time 的縮寫：它不以封包遺失判斷壅塞，而是量測描述路徑的兩個參數，瓶頸頻寬與往返傳播時間 [BBR 2017, "Congestion and Bottlenecks", p.60]。

> 依本專案教學深度設定，BBR 只說明核心概念，不推導 pacing 公式。

## 與 loss-based 演算法的根本差異
- Reno、CUBIC 都以封包遺失作為壅塞信號 [RFC 5681 §3] [RFC 9438 §5.4]。
- BBR 的作者認為，「遺失 = 壅塞」是 1980 年代技術限制下的設計選擇，而非基本原理；loss-based 演算法在大緩衝區會造成 bufferbloat，在小緩衝區會把遺失誤判為壅塞 [BBR 2017, "Congestion-Based Congestion Control", p.58]。

> This equivalence was true at the time but was because of technology limitations, not first principles. [BBR 2017, "Congestion-Based Congestion Control", p.58]

## 核心概念：兩個參數與一個操作點
| 參數 | 意義 | 水管比喻 |
| :--- | :--- | :--- |
| `RTprop` | 往返傳播時間 | 水管的長度 [BBR 2017, "Congestion and Bottlenecks", p.58] |
| `BtlBw` | 瓶頸頻寬 | 水管最窄處的直徑 [BBR 2017, "Congestion and Bottlenecks", p.58] |

最佳操作點：在途資料量等於 BDP（= BtlBw × RTprop）、送進瓶頸的速率等於 BtlBw，此時吞吐量最高、延遲最低 [BBR 2017, "Characterizing the Bottleneck", p.60]。相對地，loss-based 壅塞控制運作在「頻寬受限區域的最右緣」：能用滿瓶頸頻寬，但代價是高延遲與頻繁的封包遺失 [BBR 2017, "Congestion and Bottlenecks", p.59]。

## 如何量測
- 兩個參數無法同時量到：量 BtlBw 需要把管線灌滿，但灌滿造成的佇列會遮蔽 RTprop [BBR 2017, "Characterizing the Bottleneck", p.61]。
- 因此 BBR 交替進行：以估計的 BtlBw 速率送出資料（pacing），週期性地用大於 1 的增益（目前峰值 1.25 倍 BtlBw）多送一點，看頻寬是否變大，再用小於 1 的增益把多出的佇列排掉 [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.62] [BBR 2017, "Mobile Cellular Adaptive Bandwidth", p.66]。
- 若 RTprop 估計值很久沒有更新，BBR 進入 ProbeRTT 狀態，把在途量降到 4 個封包至少一個 RTT，以量到真正的最小 RTT [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.63]。

> BBR enters ProbeRTT, which reduces the inflight to four packets for at least one round trip [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.63]

## 結果
在 Google B4 的一條美歐路徑上，BBR 達到 2 Gbps，CUBIC 只有 15 Mbps [BBR 2017, "Google B4 WAN Deployment Experience", p.64]。

## 參考來源
- [RFC 5681 §3]
- [RFC 9438 §5.4]
- [BBR 2017, "Congestion-Based Congestion Control", p.58]
- [BBR 2017, "Congestion and Bottlenecks", p.58]
- [BBR 2017, "Congestion and Bottlenecks", p.59]
- [BBR 2017, "Congestion and Bottlenecks", p.60]
- [BBR 2017, "Characterizing the Bottleneck", p.60]
- [BBR 2017, "Characterizing the Bottleneck", p.61]
- [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.62]
- [BBR 2017, "Matching the Packet Flow to the Delivery Path", p.63]
- [BBR 2017, "Mobile Cellular Adaptive Bandwidth", p.66]
- [BBR 2017, "Google B4 WAN Deployment Experience", p.64]
