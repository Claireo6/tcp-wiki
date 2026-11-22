#!/usr/bin/env python3
"""渲染檢查節點：用瀏覽器實際開啟 slides/index.html，逐頁檢查並截圖。

檢查項目：
  1. 每頁在「補充區塊收合」時，內容不得超出投影片框（scrollHeight <= clientHeight）
  2. 圖表（第 7、8、11 頁的 <svg>）必須真的畫出內容
  3. 第 7 頁切換按鈕必須能切換兩種情境
  4. 不得有 JavaScript 錯誤
結果寫入 reports/render-YYYYMMDD-HHMMSS.md，截圖存於 reports/render/。失敗時回傳非 0。

需要 playwright（pip install playwright）與 Chrome / Chromium；此檢查不屬於只用標準庫的 lint.py。
"""
import os
import sys
from datetime import datetime

from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLIDES = os.path.join(ROOT, "slides", "index.html")
SHOT_DIR = os.path.join(ROOT, "reports", "render")
VIEWPORT = {"width": 1280, "height": 800}


def main():
    os.makedirs(SHOT_DIR, exist_ok=True)
    errors, rows, js_errors = [], [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH") or None)
        page = browser.new_page(viewport=VIEWPORT)
        page.on("pageerror", lambda e: js_errors.append(str(e)))
        page.on("console", lambda m: js_errors.append(m.text) if m.type == "error" else None)
        page.goto("file://" + SLIDES)
        n = page.evaluate("document.querySelectorAll('main > section').length")
        for i in range(1, n + 1):
            page.goto(f"file://{SLIDES}#{i}")
            page.reload()
            page.wait_for_timeout(150)
            info = page.evaluate("""() => {
                const s = document.querySelector('main > section.active');
                const svgs = [...s.querySelectorAll('svg')].map(v => v.childElementCount);
                return {src: s.dataset.src, sh: s.scrollHeight, ch: s.clientHeight, svgs};
            }""")
            shot = os.path.join(SHOT_DIR, f"slide-{i:02d}.png")
            page.screenshot(path=shot)
            ok = info["sh"] <= info["ch"] + 1
            if not ok:
                errors.append(f"第 {i} 頁內容超出投影片框（scrollHeight {info['sh']} > clientHeight {info['ch']}），需要捲動才看得完")
            for k, cnt in enumerate(info["svgs"]):
                if cnt == 0:
                    errors.append(f"第 {i} 頁第 {k + 1} 個圖表是空的")
            rows.append(f"| {i} | `{info['src']}` | {'OK' if ok else '溢出'} | {info['sh']}/{info['ch']} | {', '.join(map(str, info['svgs'])) or '—'} | `reports/render/slide-{i:02d}.png` |")
        # 第 7 頁互動切換
        page.goto(f"file://{SLIDES}#7")
        page.reload()
        before = page.inner_text("#cwnd-caption")
        page.click("button[data-mode=dupack]")
        after = page.inner_text("#cwnd-caption")
        page.screenshot(path=os.path.join(SHOT_DIR, "slide-07-dupack.png"))
        if before == after:
            errors.append("第 7 頁切換按鈕沒有改變圖表說明（互動失效）")
        browser.close()
    errors += [f"JavaScript 錯誤：{e}" for e in js_errors]

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    report = os.path.join(ROOT, "reports", f"render-{ts}.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"# 渲染檢查報告 - {ts}\n\n- **狀態**：{'通過 (PASS)' if not errors else '失敗 (FAIL)'}\n")
        f.write(f"- **視窗大小**：{VIEWPORT['width']}x{VIEWPORT['height']}\n- **問題數**：{len(errors)}\n\n")
        f.write("| 頁 | data-src | 版面 | scroll/client 高度 | 圖表元素數 | 截圖 |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        f.write("\n".join(rows) + "\n\n## 問題清單\n")
        f.write("\n".join(f"- {e}" for e in errors) if errors else "無。")
        f.write("\n")
    print(f"[{'PASS' if not errors else 'FAIL'}] 渲染檢查完成，共 {len(rows)} 頁，{len(errors)} 個問題。報告：{os.path.relpath(report, ROOT)}")
    for e in errors:
        print("  -", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
