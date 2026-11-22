# 獨立 AI 忠實度審查：使用說明與 Prompt

依 AGENTS.md §1「獨立審查原則」：審查必須在**全新對話**中進行，審查者只拿到成品與來源，不知道製作過程。建議使用與作者**不同的模型**（作者為 Claude；可用 Gemini、ChatGPT 等）。

## 要附上的檔案
解壓縮 `review-packet.zip`，把裡面的檔案全部附加到新對話：
- `slides/index.html`（受審成品）
- `wiki/` 下的所有 `.md`（簡報的知識來源）
- `raw/` 下的 `.txt`（原始文獻）

## 貼給審查者的 Prompt

```
你是一位嚴格的技術審查者。附件是一份「TCP 壅塞控制」教學 HTML 簡報（slides/index.html），
以及它的知識來源：wiki/*.md（整理過的知識庫）與 raw/*.txt（原始文獻：RFC 5681、6582、6928、9438、
Jacobson 1988 論文、BBR 2017 文章）。

簡報規則：每一頁 <section> 的 data-src 屬性標示它依據的 wiki 頁面；簡報只能使用 wiki 中有的內容，
wiki 的每個說法都標了 raw 文獻出處。

請逐頁（共 13 頁，含 <details> 補充區塊與圖表標籤）檢查：
1. 忠實度：每個說法是否能在 data-src 指定的 wiki 頁找到？是否有講反、誇大、或 wiki 沒有的內容？
2. 數字：每個數字是否與 wiki/parameters.md 和原始文獻一致？
3. 出處：<details> 裡的出處標籤，是否真的支持該頁內容？請到 raw/*.txt 抽查。
4. 覆蓋率：以「讓沒學過的人理解 TCP 壅塞控制」為目標，是否漏掉 wiki 中重要的概念？
5. 第 7 頁 cwnd 圖與第 11 頁 CUBIC 圖的規則（在 HTML 的 <script> 中）是否符合 RFC 5681 與 RFC 9438？

請用以下格式輸出，不要修改任何檔案：

| 頁 | 問題 | 嚴重度（錯誤／不精確／建議） | 依據（wiki 或 raw 的位置） |

最後給一段總評，並明確說明「沒有發現問題」的頁面有哪些。
```

## 審查完成後
把審查者的回覆存成 `reports/review-YYYYMMDD.md`。若有「錯誤」等級的問題，依 graph 退回對應節點修正（文字問題退回逐頁稿、數字問題退回 parameters.md 查證），修正後重跑 lint 與渲染檢查。
