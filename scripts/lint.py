#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/lint.py - TCP 壅塞控制 LLM Wiki 自動化檢驗腳本
使用 Python 標準函式庫，負責 Wiki 與簡報的品質與一致性檢查。
產出 reports/lint-YYYYMMDD-HHMMSS.md 報告。
"""

import sys
import os
import re
import argparse
from datetime import datetime

# 專案路徑常數
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WIKI_DIR = os.path.join(WORKSPACE_DIR, "wiki")
RAW_DIR = os.path.join(WORKSPACE_DIR, "raw")
REPORTS_DIR = os.path.join(WORKSPACE_DIR, "reports")
SLIDES_PATH = os.path.join(WORKSPACE_DIR, "slides", "index.html")

# 正則表達式規範
# Jacobson 引用格式：
#   - 一般概念敘述（段落層級）：允許頁碼範圍 p.X-Y（例如 §Intro, p.1-2）
#   - 數字、公式、英文原句之出處：必須為單一頁碼 p.X
RFC_CITATION_PATTERN = re.compile(r'^\[RFC\s+\d+\s+§[\d\.A-Za-z]+\]$')
JACOBSON_CITATION_PATTERN = re.compile(r'^\[Jacobson\s+1988,\s+§[0-9A-Za-z]+,\s+p\.\d+(?:-\d+)?\]$')
BBR_CITATION_PATTERN = re.compile(r'^\[BBR\s+2016,\s+"[^"]+"\]$')
ANY_CITATION_REGEX = re.compile(r'\[(?:RFC\s+\d+\s+§[\d\.A-Za-z]+|Jacobson\s+1988,\s+§[0-9A-Za-z]+,\s+p\.\d+(?:-\d+)?|BBR\s+2016,\s+"[^"]+")\]')
SUSPICIOUS_CITATION_REGEX = re.compile(r'\[(RFC|Jacobson|BBR)[^\]]*\]')

DEFAULT_FORBIDDEN_TERMS = [
    ("擁塞", "壅塞"),
    ("數據包", "封包"),
    ("帶寬", "頻寬"),
    ("三次握手", "三向交握"),
    ("緩存", "緩衝區"),
    ("默認", "預設")
]

class LintReporter:
    def __init__(self):
        self.errors = []
        self.files_checked = 0
        self.checked_file_list = []

    def add_error(self, rule_id, message, file_path=None, line_num=None):
        rel_path = os.path.relpath(file_path, WORKSPACE_DIR) if file_path else "全域"
        self.errors.append({
            "rule": rule_id,
            "message": message,
            "file": rel_path,
            "line": line_num
        })

    def record_file(self, file_path):
        rel_path = os.path.relpath(file_path, WORKSPACE_DIR)
        if rel_path not in self.checked_file_list:
            self.checked_file_list.append(rel_path)
            self.files_checked += 1

    def generate_report(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_file = os.path.join(REPORTS_DIR, f"lint-{timestamp}.md")
        
        status = "通過 (PASS)" if len(self.errors) == 0 else "失敗 (FAIL)"
        
        content = []
        content.append(f"# Lint 檢驗報告 - {timestamp}\n")
        content.append(f"- **檢驗狀態**：{status}")
        content.append(f"- **檢驗時間**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"- **檢查檔案數量**：{self.files_checked} 個檔案")
        content.append(f"- **發現違規總數**：{len(self.errors)} 項\n")
        
        content.append("## 已檢驗檔案清單")
        for f in self.checked_file_list:
            content.append(f"- `{f}`")
        content.append("")
        
        content.append("## 違規項目清單")
        if not self.errors:
            content.append("無違規項目，所有檢查規則皆已順利通過。\n")
        else:
            content.append("| 規則編號 | 檔案 | 行號 | 違規說明 |")
            content.append("| :--- | :--- | :--- | :--- |")
            for err in self.errors:
                line_str = str(err["line"]) if err["line"] else "-"
                content.append(f"| `{err['rule']}` | `{err['file']}` | {line_str} | {err['message']} |")
            content.append("")
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
            
        return report_file, len(self.errors) == 0


def get_all_wiki_files():
    wiki_files = []
    for root, _, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md"):
                wiki_files.append(os.path.join(root, file))
    return wiki_files


def check_orphan_pages(reporter, wiki_files):
    """[a] 孤兒頁面檢查：所有 wiki/**/*.md 均必須列於 wiki/index.md"""
    index_path = os.path.join(WIKI_DIR, "index.md")
    if not os.path.exists(index_path):
        reporter.add_error("[a] 孤兒頁面", "wiki/index.md 不存在！")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 擷取 index.md 中的所有 markdown 連結目標
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', content)
    referenced_files = set()
    for link in links:
        link_clean = link.split("#")[0].strip()
        if not link_clean or link_clean.startswith("http"):
            continue
        # 相對於 wiki/
        resolved = os.path.normpath(os.path.join(WIKI_DIR, link_clean))
        referenced_files.add(resolved)

    for wf in wiki_files:
        if os.path.abspath(wf) == os.path.abspath(index_path):
            continue
        if os.path.normpath(wf) not in referenced_files:
            reporter.add_error("[a] 孤兒頁面", f"頁面未列入 wiki/index.md 目錄中", file_path=wf)


def check_internal_links(reporter, wiki_files):
    """[b] 內部連結檢查：所有 [text](path.md) 之目標路徑皆必須存在"""
    for wf in wiki_files:
        with open(wf, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
                for text, target in links:
                    clean_target = target.split("#")[0].strip()
                    if not clean_target or clean_target.startswith("http") or clean_target.startswith("mailto"):
                        continue
                    resolved_target = os.path.normpath(os.path.join(os.path.dirname(wf), clean_target))
                    if not os.path.exists(resolved_target):
                        reporter.add_error("[b] 內部連結", f"目標檔案不存在: `{target}`", file_path=wf, line_num=idx)


def check_citations(reporter, wiki_files):
    """[c] 引用格式檢查"""
    for wf in wiki_files:
        with open(wf, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                # 找出看似出處標籤的所有中括號
                suspicious_matches = SUSPICIOUS_CITATION_REGEX.finditer(line)
                for match in suspicious_matches:
                    tag = match.group(0)
                    is_valid = (
                        RFC_CITATION_PATTERN.match(tag) or
                        JACOBSON_CITATION_PATTERN.match(tag) or
                        BBR_CITATION_PATTERN.match(tag)
                    )
                    if not is_valid:
                        reporter.add_error("[c] 引用格式", f"引用格式不符規範: `{tag}`", file_path=wf, line_num=idx)


def normalize_quote_text(text):
    if not text:
        return ""
    # 處理行尾連字號斷字，例如 "win- dow" 或 "win-\ndow" -> "window"
    text = re.sub(r'(\b\w+)-[\s\r\n]+(\w+\b)', r'\1\2', text)
    # 將常見引號標準化
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    return " ".join(text.split())


def check_verbatim_quotes(reporter, wiki_files):
    """[d] 原文比對：針對 RFC 與 Jacobson 1988 引用的英文原句，壓縮連續空白與換行後，與 raw/*.txt 進行完全一致的子字串比對"""
    raw_texts = {}

    def get_raw_content(source_key):
        if source_key not in raw_texts:
            if source_key.startswith("rfc"):
                raw_path = os.path.join(RAW_DIR, f"{source_key}.txt")
            elif source_key == "jacobson1988":
                raw_path = os.path.join(RAW_DIR, "jacobson1988.txt")
            else:
                raw_path = None

            if raw_path and os.path.exists(raw_path):
                with open(raw_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_texts[source_key] = normalize_quote_text(f.read())
            else:
                raw_texts[source_key] = None
        return raw_texts[source_key]

    for wf in wiki_files:
        with open(wf, "r", encoding="utf-8") as f:
            lines = f.readlines()

        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if line.strip().startswith(">"):
                start_line = idx + 1
                quote_lines = []
                while idx < len(lines) and lines[idx].strip().startswith(">"):
                    clean_l = lines[idx].strip().lstrip('>').strip()
                    quote_lines.append(clean_l)
                    idx += 1
                
                block_text = " ".join(quote_lines)
                
                # 檢查 RFC 或 Jacobson 引用
                rfc_matches = re.findall(r'\[RFC\s+(\d+)\s+§[\d\.A-Za-z]+\]', block_text)
                jacobson_matches = re.findall(r'\[Jacobson\s+1988,\s+§[0-9A-Za-z]+,\s+p\.\d+(?:-\d+)?\]', block_text)

                target_source = None
                display_source = None
                if rfc_matches:
                    target_source = f"rfc{rfc_matches[0]}"
                    display_source = f"raw/{target_source}.txt"
                elif jacobson_matches:
                    target_source = "jacobson1988"
                    display_source = "raw/jacobson1988.txt"

                if target_source:
                    # 去除所有出處標籤
                    quote_text = ANY_CITATION_REGEX.sub('', block_text)
                    quote_text = quote_text.strip().strip('"').strip('“').strip('”').strip("'")
                    
                    if len(quote_text) > 10 and re.search(r'[a-zA-Z]{3,}', quote_text):
                        compressed_quote = normalize_quote_text(quote_text)
                        raw_content = get_raw_content(target_source)
                        if not raw_content:
                            reporter.add_error("[d] 原文比對", f"找不到對應的 {display_source} 來源檔", file_path=wf, line_num=start_line)
                        elif compressed_quote not in raw_content:
                            reporter.add_error("[d] 原文比對", f"英文原句無法在 {display_source} 找到完全一致匹配: `{compressed_quote[:50]}...`", file_path=wf, line_num=start_line)
            else:
                idx += 1


def check_forbidden_terms(reporter, wiki_files):
    """[e] 禁用詞檢查：對照 wiki/glossary.md 禁用詞，檢測到即回報檔案與行號（排除 glossary.md 禁用詞對照表）"""
    forbidden_terms = DEFAULT_FORBIDDEN_TERMS

    glossary_path = os.path.join(WIKI_DIR, "glossary.md")
    
    for wf in wiki_files:
        is_glossary = os.path.abspath(wf) == os.path.abspath(glossary_path)
        in_forbidden_table = False
        
        with open(wf, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                if is_glossary:
                    if "## 2. 禁用詞對照表" in line or "禁用詞對照" in line:
                        in_forbidden_table = True
                        continue
                    elif in_forbidden_table and line.startswith("## "):
                        in_forbidden_table = False
                    
                    if in_forbidden_table:
                        continue

                for bad, good in forbidden_terms:
                    if bad in line:
                        reporter.add_error("[e] 禁用詞", f"檢測到禁用詞「{bad}」（應改為「{good}」）", file_path=wf, line_num=idx)


def check_source_headers(reporter, wiki_files):
    """[f] 來源欄位 與 [g] 標頭忠實性檢查"""
    sources_dir = os.path.join(WIKI_DIR, "sources")
    for wf in wiki_files:
        if os.path.dirname(os.path.abspath(wf)) == os.path.abspath(sources_dir):
            with open(wf, "r", encoding="utf-8") as f:
                header_lines = [f.readline() for _ in range(30)]
            
            header_text = "".join(header_lines)
            has_category = bool(re.search(r'Category\s*:', header_text, re.IGNORECASE))
            has_obsoletes = bool(re.search(r'Obsoletes\s*:', header_text, re.IGNORECASE))
            has_updates = bool(re.search(r'Updates\s*:', header_text, re.IGNORECASE))

            missing = []
            if not has_category: missing.append("Category")
            if not has_obsoletes: missing.append("Obsoletes")
            if not has_updates: missing.append("Updates")

            if missing:
                reporter.add_error("[f] 來源欄位", f"sources 頁面缺少必備標頭欄位: {', '.join(missing)}", file_path=wf, line_num=1)

            # [g] 標頭忠實比對
            fname = os.path.basename(wf)
            m = re.match(r'(rfc\d+)\.md', fname, re.IGNORECASE)
            if m:
                raw_rfc_file = os.path.join(RAW_DIR, f"{m.group(1).lower()}.txt")
                if os.path.exists(raw_rfc_file):
                    with open(raw_rfc_file, "r", encoding="utf-8", errors="ignore") as rf:
                        raw_head = "".join([rf.readline() for _ in range(40)])
                    
                    for field in ["Category", "Obsoletes", "Updates"]:
                        raw_field_match = re.search(rf'^{field}\s*:\s*([^\r\n]+)', raw_head, re.MULTILINE | re.IGNORECASE)
                        doc_field_match = re.search(rf'{field}\s*:\s*([^\r\n]+)', header_text, re.IGNORECASE)
                        if raw_field_match and doc_field_match:
                            raw_val = raw_field_match.group(1).strip()
                            doc_val = doc_field_match.group(1).strip()
                            if raw_val.lower() not in doc_val.lower() and doc_val.lower() not in raw_val.lower():
                                reporter.add_error("[g] 標頭忠實", f"標頭欄位 {field} 與原文不一致: 原文 `{raw_val}` vs 頁面 `{doc_val}`", file_path=wf)


def check_required_sections(reporter, wiki_files):
    """[h] 必備章節檢查：所有頁面末尾必須包含「## 參考來源」（排除 index.md 與 log.md）"""
    index_path = os.path.abspath(os.path.join(WIKI_DIR, "index.md"))
    log_path = os.path.abspath(os.path.join(WIKI_DIR, "log.md"))

    for wf in wiki_files:
        abs_wf = os.path.abspath(wf)
        if abs_wf == index_path or abs_wf == log_path:
            continue

        with open(wf, "r", encoding="utf-8") as f:
            content = f.read()

        if "## 參考來源" not in content:
            reporter.add_error("[h] 必備章節", "頁面末尾缺少必備章節「## 參考來源」", file_path=wf)


def check_parameters_file(reporter):
    """[i] 參數出處檢查：wiki/parameters.md 內所有數字均必須緊跟出處標籤"""
    param_path = os.path.join(WIKI_DIR, "parameters.md")
    if not os.path.exists(param_path):
        return

    with open(param_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            # 排除標題、空行、表格分隔線
            if not line_str or line_str.startswith("#") or set(line_str).issubset(set("|- :")):
                continue
            
            # 若包含數字（且排除 markdown 編號如 1. 2.）
            digits = re.findall(r'\b\d+(?:\.\d+)?\b', line_str)
            if digits:
                # 必須帶有出處標籤
                has_citation = bool(ANY_CITATION_REGEX.search(line_str))
                if not has_citation:
                    reporter.add_error("[i] 參數出處", f"數值行缺少出處標註: `{line_str}`", file_path=param_path, line_num=idx)


def check_conflicts_file(reporter):
    """[j] 衝突來源檢查：wiki/conflicts.md 每一項目必須具備至少兩個不同出處"""
    conflicts_path = os.path.join(WIKI_DIR, "conflicts.md")
    if not os.path.exists(conflicts_path):
        return

    with open(conflicts_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 以 ### 切割每一項衝突
    sections = re.split(r'\n###\s+', content)
    # 第一段通常是介紹
    for sec in sections[1:]:
        lines = sec.strip().split("\n")
        title = lines[0] if lines else "未知衝突項"
        citations = set(ANY_CITATION_REGEX.findall(sec))
        if len(citations) < 2:
            reporter.add_error("[j] 衝突來源", f"衝突項目出處不足 2 個（目前僅 {len(citations)} 個）: `{title}`", file_path=conflicts_path)


def check_slides(reporter):
    """簡報檢查規則（--slides）"""
    if not os.path.exists(SLIDES_PATH):
        reporter.add_error("簡報檢查", f"簡報檔案不存在: `{SLIDES_PATH}`")
        return

    reporter.record_file(SLIDES_PATH)
    with open(SLIDES_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 禁用詞過濾
    for idx, line in enumerate(content.splitlines(), 1):
        for bad, good in DEFAULT_FORBIDDEN_TERMS:
            if bad in line:
                reporter.add_error("簡報禁用詞", f"檢測到禁用詞「{bad}」（應改為「{good}」）", file_path=SLIDES_PATH, line_num=idx)

    # 2. 檢查每一頁 section
    sections = re.findall(r'<section\b([^>]*)>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
    for idx, (attrs, sec_content) in enumerate(sections, 1):
        # 檢查 data-src
        data_src_match = re.search(r'data-src=["\']([^"\']+)["\']', attrs)
        if not data_src_match:
            reporter.add_error("簡報章節", f"第 {idx} 個 <section> 缺少 data-src 屬性", file_path=SLIDES_PATH)
        else:
            target_wiki = os.path.normpath(os.path.join(WORKSPACE_DIR, data_src_match.group(1)))
            if not os.path.exists(target_wiki):
                reporter.add_error("簡報章節", f"data-src 指定之 Wiki 頁面不存在: `{data_src_match.group(1)}`", file_path=SLIDES_PATH)

        # 3. 字數上限 100 字（排除 <details>...</details> 與 HTML 標籤）
        filtered_content = re.sub(r'<details\b[^>]*>.*?</details>', '', sec_content, flags=re.DOTALL | re.IGNORECASE)
        plain_text = re.sub(r'<[^>]+>', '', filtered_content).strip()
        # 計算中文字數 + 英文字數
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', plain_text))
        english_words = len(re.findall(r'[a-zA-Z0-9_]+', plain_text))
        total_words = chinese_chars + english_words

        if total_words > 100:
            reporter.add_error("簡報字數", f"第 {idx} 頁正文字數 ({total_words} 字) 超過 100 字上限", file_path=SLIDES_PATH)

    # 4. 數字查核：簡報出現的所有數字均必須在 wiki/parameters.md 存在
    # 排除：4 位數年份、RFC 編號、出處標籤內數字
    param_path = os.path.join(WIKI_DIR, "parameters.md")
    if os.path.exists(param_path):
        with open(param_path, "r", encoding="utf-8") as pf:
            param_content = pf.read()
        valid_numbers = set(re.findall(r'\b\d+(?:\.\d+)?\b', param_content))

        # 移除出處標籤
        clean_slides = ANY_CITATION_REGEX.sub('', content)
        # 移除 <details>
        clean_slides = re.sub(r'<details\b[^>]*>.*?</details>', '', clean_slides, flags=re.DOTALL | re.IGNORECASE)
        # 找出所有數字
        all_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', clean_slides)
        
        rfc_numbers = {"5681", "6582", "6928", "9438", "8312"}
        for num in all_numbers:
            # 排除 4 位數年份 (1900-2099)
            if len(num) == 4 and (num.startswith("19") or num.startswith("20")):
                continue
            # 排除 RFC 編號
            if num in rfc_numbers:
                continue
            if num not in valid_numbers:
                reporter.add_error("簡報數字", f"簡報中的數值 `{num}` 未在 wiki/parameters.md 中登錄", file_path=SLIDES_PATH)


def main():
    parser = argparse.ArgumentParser(description="TCP 壅塞控制 LLM Wiki 自動化檢驗工具")
    parser.add_argument("--slides", action="store_true", help="執行 HTML 簡報專屬檢查")
    args = parser.parse_args()

    reporter = LintReporter()

    wiki_files = get_all_wiki_files()
    for wf in wiki_files:
        reporter.record_file(wf)

    # 執行 Wiki 檢驗清單
    check_orphan_pages(reporter, wiki_files)
    check_internal_links(reporter, wiki_files)
    check_citations(reporter, wiki_files)
    check_verbatim_quotes(reporter, wiki_files)
    check_forbidden_terms(reporter, wiki_files)
    check_source_headers(reporter, wiki_files)
    check_required_sections(reporter, wiki_files)
    check_parameters_file(reporter)
    check_conflicts_file(reporter)

    # 若指定 --slides 或簡報檔案存在時執行簡報檢查
    if args.slides:
        check_slides(reporter)

    report_file, success = reporter.generate_report()
    
    rel_report = os.path.relpath(report_file, WORKSPACE_DIR)
    print(f"[{'PASS' if success else 'FAIL'}] Lint 檢驗完成！共檢查 {reporter.files_checked} 個檔案，發現 {len(reporter.errors)} 項違規。")
    print(f"報告已產出至: {rel_report}")
    
    if not success:
        for err in reporter.errors:
            line_str = f":{err['line']}" if err['line'] else ""
            print(f"  - [{err['rule']}] {err['file']}{line_str} -> {err['message']}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
