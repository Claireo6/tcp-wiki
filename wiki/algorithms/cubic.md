# CUBIC

CUBIC 以三次函數取代 Reno 的線性增長函數，改善在高速、長距離網路中的擴展性與穩定性，是 Linux、Windows 與 Apple 協定堆疊的預設演算法 [RFC 9438 §1]。

## 直覺：先凹、後凸
壅塞事件發生時，CUBIC 會記住當時的視窗大小（`W_max`），然後做乘法減少 [RFC 9438 §3.1]。之後的增長分成兩段 [RFC 9438 §3.1]：
1. **凹段（concave）**：一開始增長較快，越接近 `W_max` 越平緩，在 `W_max` 附近形成平台。
2. **凸段（convex）**：超過 `W_max` 後，先緩慢、再逐漸加快地往上探測新的上限。

> When CUBIC enters into congestion avoidance, it starts to increase the congestion window using the concave profile of the cubic function. [RFC 9438 §3.1]

平台設在上次壅塞點附近，是因為那裡被視為網路利用率最高的位置；穩定狀態下多數時間視窗都接近 `W_max`，因此兼顧高利用率與穩定性 [RFC 9438 §3.1]。

## 增長函數（§4.2）
視窗大小是「距離本次 congestion avoidance 開始經過的時間 $t$」的函數，而不是 ACK 次數的函數 [RFC 9438 §4.2]：

$$W_{cubic}(t) = C \cdot (t - K)^3 + W_{max}$$

- $K$：在沒有新壅塞事件的情況下，視窗從目前大小長回 $W_{max}$ 所需的時間，$K = \sqrt[3]{(W_{max} - cwnd_{epoch}) / C}$ [RFC 9438 §4.2]。
- $C$：決定 CUBIC 積極程度的常數，應設為 0.4 [RFC 9438 §5.1]。
- 每次收到新 ACK 時計算下一個 RTT 的目標值，並限制在 `cwnd` 與 `1.5 * cwnd` 之間，確保增長速度不會比 slow start 更快 [RFC 9438 §4.2]。

> Therefore, _C_ SHOULD be set to 0.4. [RFC 9438 §5.1]

## 三個區域
CUBIC 同時計算三次函數的值與「Reno 在相同情況下會有的視窗」（`W_est`），取兩者較大者 [RFC 9438 §4.2]：
1. **Reno-friendly 區域**：三次函數比 Reno 慢時，直接跟隨 Reno 的視窗，確保至少有 Reno 的吞吐量 [RFC 9438 §4.3]。
2. **凹區域**：`cwnd` 小於 `W_max` [RFC 9438 §4.4]。
3. **凸區域**：`cwnd` 大於或等於 `W_max`，也稱為「最大值探測階段」[RFC 9438 §4.5]。

> CUBIC computes both W_cubic(_t_) and _W_est_ (see Section 4.3) on receiving a new ACK in congestion avoidance and chooses the larger of the two values. [RFC 9438 §4.2]

## 乘法減少（§4.6）
偵測到壅塞時，`ssthresh = flight_size * β_cubic`，而 β_cubic 應設為 0.7，與 RFC 5681 fast recovery 使用的係數不同 [RFC 9438 §4.6]。

> SHOULD be set to 0.7, which is different from the multiplicative decrease factor used in [RFC 9438 §4.6]

## 其他機制
- **Fast convergence**：新流量加入時，若本次壅塞時的 `cwnd` 小於上次的 `W_max`，就把 `W_max` 再降為 `cwnd * (1 + β_cubic) / 2`，主動讓出頻寬給新流量 [RFC 9438 §4.7]。
- **逾時**：依 Reno 的方式降低 `cwnd`，但 `ssthresh` 用 β_cubic 計算 [RFC 9438 §4.8]。
- **Slow start**：應使用 HyStart++，少數不適用的情況才用 RFC 5681 的 slow start [RFC 9438 §4.10]。

## 限制
仍以封包遺失判斷壅塞，在無線或行動網路等封包遺失不能代表頻寬使用狀況的環境表現較差；也可能更快填滿大型 drop-tail 緩衝區，增加形成持續性佇列的風險 [RFC 9438 §5.4]。

> it can fill large drop-tail buffers more quickly than Reno and increases the risk of a standing queue [RFC 9438 §5.4]

## 參考來源
- [RFC 9438 §1]
- [RFC 9438 §3.1]
- [RFC 9438 §4.2]
- [RFC 9438 §4.3]
- [RFC 9438 §4.4]
- [RFC 9438 §4.5]
- [RFC 9438 §4.6]
- [RFC 9438 §4.7]
- [RFC 9438 §4.8]
- [RFC 9438 §4.10]
- [RFC 9438 §5.1]
- [RFC 9438 §5.4]
