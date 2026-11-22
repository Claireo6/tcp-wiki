# 歧異與衝突對照表（Conflicts）

本頁面彙整跨文獻間不同標準、非正式演進提案（如 Standards Track vs Experimental）、或學術論文與工程標準間存在分歧之記錄。每一項目均標註兩方或以上之來源出處。

## 歧異項目彙整

### 1. Initial Window (`IW`) 設定建議大小
- **分歧描述**：正式標準規範建議依 `SMSS` 大小設定為 2 至 4 個區段；而後續實驗性提案建議一律提升至 10 個區段以降低 Web 延遲。
- **來源一（Standards Track）**：`IW` 為 2 至 4 segments [RFC 5681 §3.1]。
- **來源二（Experimental）**：`IW` 建議提升至 10 segments [RFC 6928 §1]。

### 2. 壅塞判定哲學（封包遺失 vs. 延遲與頻寬量測）
- **分歧描述**：古典 RFC 演算法皆以封包遺失（逾時或重複 ACK）作為網路壅塞之唯一信號；BBR 論文則認為在現代網路環境中，封包遺失並非壅塞的最佳指標，應改採延遲與頻寬量測。
- **來源一（Standards Track）**：以封包遺失代表網路進入壅塞 [RFC 5681 §3.1]。
- **來源二（學術論文）**：封包遺失不等於壅塞，應基於 BtlBw 與 RTprop 建模 [BBR 2016, "Introduction"]。

## 參考來源
- [RFC 5681 §3.1]
- [RFC 6928 §1]
- [BBR 2016, "Introduction"]
