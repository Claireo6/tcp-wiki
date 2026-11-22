# 封包遺失偵測（Packet Loss Detection）

在 TCP 壅塞控制中，傳送端如何準確且即時地判定「封包已於網路中遺失」是調節視窗的關鍵先決條件 [Jacobson 1988, §Intro, p.1-2]。

## 1. 重傳計時器逾時（Retransmission Timeout, RTO）

在 Jacobson 1988 的架構中，封包遺失主要藉由重傳計時器逾時（Timeout）進行判定 [Jacobson 1988, §3, p.8-9]。若計時器設定過短，會將正常排隊延遲誤判為遺失而引發偽重傳（Spurious retransmissions），進一步惡化網路負載 [Jacobson 1988, §2, p.7]。

### RTO 均值與變異量估算（Appendix A）
為了精確捕捉往返時間（RTT）在高負載下的劇烈波動，作者提出同時估算平均 RTT（$a$）與平均偏差（Mean Deviation, $v$）之定點數濾波演算法 [Jacobson 1988, §A, p.18-20]：
- 誤差計算：$Err = m - a$（$m$ 為最新量測到的 RTT）[Jacobson 1988, §A, p.19]
- 均值更新：$a \leftarrow a + g Err$（增益 $g = 0.125$）[Jacobson 1988, §A, p.19]
- 偏差更新：$v \leftarrow v + g(|Err| - v)$（增益採 $0.25$）[Jacobson 1988, §A, p.19-20]
- 計時器計算：$RTO = a + 4v$ [Jacobson 1988, §A, p.20]

### 註腳 21 修正歷程
在 SIGCOMM '88 原始論文中，作者原建議設定 $RTO = R + 2V$ [Jacobson 1988, §C, p.21]。但在後續低速 SLIP 撥接鏈路測試中，作者觀察到連線啟動階段頻繁發生偽重傳，經數學分析慢啟動期間 RTT 最糟情況每輪翻倍，確認偏差乘數必須提高至 4 倍方能避免啟動期間的偽重傳，因而於本修訂版正式將公式更新為 $RTO = a + 4v$ [Jacobson 1988, §C, p.21]。

## 2. 指數退避（Exponential Backoff）

當同一封包遭遇連續逾時需要再次重傳時，傳送端無法得知全域網路拓撲與競爭連線狀況 [Jacobson 1988, §2, p.7]。為提供足夠的阻尼以穩定系統、防止壅塞崩潰，傳送端必須對逾時週期採用「指數退避（Exponential Backoff）」，即每次重傳將 RTO 區間加倍 [Jacobson 1988, §2, p.7-8]。

## 3. 快速重傳（Fast Retransmit）之提出

除計時器逾時之外，作者在 1988 年論文中已將快速重傳（Fast Retransmit）列入 4BSD TCP 之 7 個新演算法中 [Jacobson 1988, §Intro, p.2]。然而該文並未展開其詳細偵測機制，僅預告將於後續 RFC 文件中完整規範 [Jacobson 1988, §Intro, p.2]。

## 參考來源
- [Jacobson 1988, §Intro, p.1-2]
- [Jacobson 1988, §Intro, p.2]
- [Jacobson 1988, §2, p.7]
- [Jacobson 1988, §2, p.7-8]
- [Jacobson 1988, §3, p.8-9]
- [Jacobson 1988, §A, p.18-20]
- [Jacobson 1988, §A, p.19]
- [Jacobson 1988, §A, p.19-20]
- [Jacobson 1988, §A, p.20]
- [Jacobson 1988, §C, p.21]
