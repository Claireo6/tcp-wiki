# Congestion Avoidance and Control

Category: Academic Paper (SIGCOMM '88)
Obsoletes: None
Updates: None

## 文件基本資訊
- **作者**：Van Jacobson (Lawrence Berkeley Laboratory), Michael J. Karels (University of California at Berkeley) [Jacobson 1988, §Intro, p.1]
- **日期**：November, 1988（為 SIGCOMM '88 發表論文之微幅修訂版）[Jacobson 1988, §Intro, p.1]
- **頁數**：共 25 頁 [Jacobson 1988, §Intro, p.1]

## 核心研究背景
1986 年 10 月，網際網路發生嚴重的「壅塞崩潰（Congestion Collapse）」，從 LBL 到 UC Berkeley（相隔僅 400 碼、兩個 IMP 節點跳躍）的吞吐量從 32 Kbps 暴跌至 40 bps（驟降千分之一）[Jacobson 1988, §Intro, p.1]。作者研究發現問題主因並非協定本身，而是傳輸協定實作於面對網路壅塞時表現出錯誤行為 [Jacobson 1988, §Intro, p.1]。

## 4BSD TCP 納入的 7 個新演算法
作者於文中指出已將 7 個新演算法實作於 4BSD TCP 中 [Jacobson 1988, §Intro, p.2]：
1. `(i) round-trip-time variance estimation`（往返時間變異量估算）[Jacobson 1988, §Intro, p.2]
2. `(ii) exponential retransmit timer backoff`（指數型重傳計時器退避）[Jacobson 1988, §Intro, p.2]
3. `(iii) slow-start`（慢啟動）[Jacobson 1988, §Intro, p.2]
4. `(iv) more aggressive receiver ack policy`（更主動的接收端確認策略）[Jacobson 1988, §Intro, p.2]
5. `(v) dynamic window sizing on congestion`（發生壅塞時之動態視窗調整）[Jacobson 1988, §Intro, p.2]
6. `(vi) Karn's clamped retransmit backoff`（Karn 箝位重傳退避演算法）[Jacobson 1988, §Intro, p.2]
7. `(vii) fast retransmit`（快速重傳）[Jacobson 1988, §Intro, p.2]

> "Since that time, we have put seven new algorithms into the 4BSD TCP: (i) round-trip-time variance estimation (ii) exponential retransmit timer backoff (iii) slow-start (iv) more aggressive receiver ack policy (v) dynamic window sizing on congestion (vi) Karn’s clamped retransmit backoff (vii) fast retransmit" [Jacobson 1988, §Intro, p.2]

論文明確說明本篇僅詳細闡述 (i) 至 (v) 以及其背後原理；(vi) 為 Phil Karn 提出之演算法；(vii) fast retransmit 則由即將發布之 ARPANET RFC 另行說明 [Jacobson 1988, §Intro, p.2]。

## 封包守恆原則與失效原因
連線在穩定平衡狀態下，在舊封包離開網路前不得將新封包注入網路 [Jacobson 1988, §Intro, p.2]。傳送端以收到的 ACK 作為觸發時脈（Self-clocking）送出新封包 [Jacobson 1988, §1, p.3]。
封包守恆失效僅有三種原因 [Jacobson 1988, §Intro, p.2]：
1. 連線未達到平衡（The connection doesn’t get to equilibrium）[Jacobson 1988, §Intro, p.2]
2. 傳送端在舊封包離開前即注入新封包（A sender injects a new packet before an old packet has exited）[Jacobson 1988, §Intro, p.2]
3. 沿途資源限制導致無法達到平衡（The equilibrium can’t be reached because of resource limits along the path）[Jacobson 1988, §Intro, p.2]

## 各機制核心細節

### 1. 慢啟動（Slow-Start）
- 連線初始建立或發生封包遺失重啟時，將 `cwnd` 設為 1 個封包 [Jacobson 1988, §1, p.4]。
- 每次收到新資料之 ACK，`cwnd` 增加 1 個封包 [Jacobson 1988, §1, p.4]。
- 視窗大小隨時間呈指數級增長，打開視窗費時 $R \log_2 W$ [Jacobson 1988, §1, p.4]。
- 傳送時發送量為 $\min(\text{advertised window}, \text{cwnd})$ [Jacobson 1988, §1, p.4]。

### 2. 往返時間估算與 RTO（RTT Timing & Appendix A）
- RFC 793 僅估計平均 RTT 而忽略變異量 $\sigma_R$，在負載超過 30% 時容易因正常延遲變異引發偽重傳（Spurious retransmissions）[Jacobson 1988, §2, p.7]。
- 提出以平均偏差（Mean Deviation, $v$）估計變異量，整數濾波更新式為 $Err = m - a$、$a \leftarrow a + g Err$、$v \leftarrow v + g(|Err| - v)$ [Jacobson 1988, §A, p.19]。
- 最終重傳計時器計算為 $RTO = a + 4v$ [Jacobson 1988, §A, p.20]。
- **註腳 21 歷史演進記錄**：SIGCOMM '88 原始發表版本建議計算公式為 $R + 2V$；本修訂版因在低速 SLIP 鏈路上觀察到連線啟動時的偽重傳現象，深入分析後正式修訂為 $R + 4V$ [Jacobson 1988, §C, p.21]。
- 連續重傳時使用指數退避（Exponential Backoff）[Jacobson 1988, §2, p.7-8]。

### 3. 壅塞避免（Congestion Avoidance / AIMD）
- 以封包遺失（逾時）作為壅塞信號 [Jacobson 1988, §3, p.8-9]。
- 採用加法增加 / 乘法減少（AIMD）控制策略 [Jacobson 1988, §3, p.10]：
  - 發生壅塞時：乘法減少，視窗乘以 $0.5$（減半）[Jacobson 1988, §D, p.23]。
  - 無壅塞時：加法增加，每次增加常數 $1$ 個封包 [Jacobson 1988, §D, p.23]，實作上每收到一個 ACK 增加 $1/\text{cwnd}$ [Jacobson 1988, §3, p.10]。
- **作者對 1 個封包增量之評述**：作者明確指出 1-packet increase 缺乏理論依據，且「幾乎肯定太大（almost certainly too large）」；若未來 Gateway 能在佇列被推擠過膝點（knee）時提早丟包偵測，此增量應縮減約 4 倍 [Jacobson 1988, §D, p.23]。

### 4. 慢啟動與壅塞避免之結合（Appendix B）
傳送端維護兩個狀態變數：壅塞視窗 `cwnd` 與慢啟動門檻 `ssthresh` [Jacobson 1988, §B, p.20]。
- 發生逾時（Timeout）時：將「當前視窗大小的一半（half the current window size）」記錄至 `ssthresh`，並將 `cwnd` 設為 1 個封包重啟慢啟動 [Jacobson 1988, §B, p.20]。
- 收到新資料 ACK 時 [Jacobson 1988, §B, p.20]：
  - 若 `cwnd < ssthresh`：執行 slow start，`cwnd += 1` [Jacobson 1988, §B, p.20]。
  - 若 `cwnd >= ssthresh`：執行 congestion avoidance，`cwnd += 1/cwnd` [Jacobson 1988, §B, p.20]。

> "On a timeout, half the current window size is recorded in ssthresh (this is the multiplicative decrease part of the congestion avoidance algorithm), then cwnd is set to 1 packet (this initiates slow-start)." [Jacobson 1988, §B, p.20]

### 5. 連線閒置重設（Appendix C）
若連線閒置無資料在途且超過一個 RTO（`idle && now - lastsnd > rto`），管線已空無 ACK 時鐘，下次發送時將 `cwnd` 重設為 1 個封包以強制重新 slow start [Jacobson 1988, §C, p.22]。

## 參考來源
- [Jacobson 1988, §Intro, p.1]
- [Jacobson 1988, §Intro, p.2]
- [Jacobson 1988, §1, p.3]
- [Jacobson 1988, §1, p.4]
- [Jacobson 1988, §2, p.7]
- [Jacobson 1988, §2, p.7-8]
- [Jacobson 1988, §3, p.8-9]
- [Jacobson 1988, §3, p.10]
- [Jacobson 1988, §A, p.18-20]
- [Jacobson 1988, §A, p.19]
- [Jacobson 1988, §A, p.20]
- [Jacobson 1988, §B, p.20]
- [Jacobson 1988, §C, p.21]
- [Jacobson 1988, §C, p.22]
- [Jacobson 1988, §D, p.23]
