#!/usr/bin/env python3
"""渲染節點：把 slides/drafts/NN.html（已通過檢查的逐頁稿）原封不動組進 HTML 範本。

規則（AGENTS.md / 課程 Graph 設計）：本節點只負責排版與圖表程式，不得修改逐頁稿的任何文字。
圖表使用的常數集中在 CHART_PARAMS，每個值都附 wiki 出處，lint --slides 會檢查它們都已登錄於 wiki/parameters.md。
"""
import glob
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DRAFTS = sorted(glob.glob(os.path.join(ROOT, "slides", "drafts", "*.html")))
OUT = os.path.join(ROOT, "slides", "index.html")

CHART_PARAMS = {
    "IW": {"value": 3, "source": "RFC 5681 §3.1（SMSS 介於 1095 與 2190 位元組時 IW 上限為 3 個區段）"},
    "LW": {"value": 1, "source": "RFC 5681 §3.1（逾時後 cwnd 不超過 1 個完整區段）"},
    "DupThresh": {"value": 3, "source": "RFC 5681 §3.2"},
    "ssthreshDivisor": {"value": 2, "source": "RFC 5681 §3.1（ssthresh = max(FlightSize/2, 2*SMSS)）"},
    "ssthreshMin": {"value": 2, "source": "RFC 5681 §3.1（下限 2*SMSS）"},
    "caIncrementPerRTT": {"value": 1, "source": "RFC 5681 §3.1（每個 RTT 約增加 1 個完整區段）"},
    "C": {"value": 0.4, "source": "RFC 9438 §5.1"},
    "betaCubic": {"value": 0.7, "source": "RFC 9438 §4.6"},
    "betaReno": {"value": 0.5, "source": "RFC 9438 §3.4"},
}

STATE_DIAGRAM = """
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker></defs>
<g class="node"><rect x="10" y="95" width="130" height="56" rx="10"/><text x="75" y="129">慢啟動</text></g>
<g class="node"><rect x="255" y="95" width="130" height="56" rx="10"/><text x="320" y="129">壅塞避免</text></g>
<g class="node fr"><rect x="500" y="95" width="130" height="56" rx="10"/><text x="565" y="129">快速恢復</text></g>
<path class="edge" d="M140,123 L255,123" marker-end="url(#arr)"/><text class="lbl" x="197" y="115">cwnd &gt; ssthresh</text>
<path class="edge" d="M385,123 L500,123" marker-end="url(#arr)"/><text class="lbl" x="442" y="115">3 個重複 ACK</text>
<path class="edge warn" d="M300,95 C300,40 95,40 95,95" marker-end="url(#arr)"/><text class="lbl warn" x="197" y="48">逾時：cwnd = 1</text>
<path class="edge warn" d="M565,95 C565,-12 55,-12 55,95" marker-end="url(#arr)"/><text class="lbl warn" x="310" y="9">逾時：cwnd = 1</text>
<path class="edge" d="M545,151 C545,210 340,210 340,151" marker-end="url(#arr)"/><text class="lbl" x="442" y="214">新 ACK：cwnd = ssthresh</text>
<path class="edge" d="M75,151 C75,255 585,255 585,151" marker-end="url(#arr)" opacity="0.6"/><text class="lbl" x="330" y="246">3 個重複 ACK</text>
"""

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>網路為什麼會塞車？TCP 壅塞控制入門</title>
<style>
:root{--bg:#f7f5f0;--ink:#1f2937;--muted:#64748b;--accent:#1d4ed8;--warn:#c2410c;--card:#ffffff;--line:#e2e8f0}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
main{height:100%;display:flex;align-items:center;justify-content:center;padding:12px 16px 68px}
section{display:none;width:min(1060px,100%);min-height:min(520px,calc(100vh - 92px));max-height:calc(100vh - 92px);background:var(--card);border-radius:18px;box-shadow:0 8px 30px rgba(15,23,42,.08);padding:34px 52px 28px;overflow:auto;position:relative;flex-direction:column;justify-content:center;gap:14px}
section.active{display:flex}
section > *{margin-top:0;margin-bottom:0}
h1{font-size:2.5rem;margin:.3em 0 0}
h2{font-size:2rem;color:var(--ink)}
h3{font-size:1.2rem;margin:0 0 6px;color:var(--accent)}
p,li{font-size:1.32rem;line-height:1.7}
ul,ol{padding-left:1.3em;margin:0}
.subtitle{font-size:1.4rem;color:var(--accent)}
.q{color:var(--muted);font-size:1.1rem;border-left:3px solid var(--line);padding-left:10px}
.key{font-weight:700;color:var(--accent);font-size:1.2rem}
.tag{align-self:flex-start;background:#fff7ed;color:var(--warn);border:1px solid #fed7aa;border-radius:999px;padding:2px 14px;font-size:.95rem}
.bigstat{display:flex;gap:24px;align-items:center;font-size:2.8rem;font-weight:800}
.bigstat .bad{color:var(--warn)} .bigstat .arrow{color:var(--muted)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:stretch}
.grid2.tight .box{font-size:1.1rem;line-height:1.6}
.box{background:#f8fafc;border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px}
.box p,.box li{font-size:1.2rem;margin:0;line-height:1.65}
.warn-box{border-left-color:var(--warn);background:#fffaf5}
.key-box{margin-top:6px!important;background:#eff6ff;font-weight:600;font-size:1.25rem}
ol.steps{display:flex;flex-direction:column;gap:4px}
ol.steps.compact li,ul.compact li{line-height:1.5}
table.cmp{border-collapse:collapse;width:100%;font-size:1.2rem}
table.cmp th,table.cmp td{border-bottom:1px solid var(--line);padding:12px 14px;text-align:left}
table.cmp th{color:var(--accent)}
ol.timeline{list-style:none;padding:0 0 0 4px;border-left:3px solid var(--accent);margin-left:8px}
ol.timeline li{padding-left:18px;position:relative;line-height:2.3;font-size:1.25rem}
ol.timeline li::before{content:"";position:absolute;left:-10px;top:.75em;width:14px;height:14px;border-radius:50%;background:var(--accent)}
details{background:#f1f5f9;border-radius:10px;padding:8px 16px;flex-shrink:0}
details summary{cursor:pointer;color:var(--accent);font-weight:600}
details p{font-size:1rem;margin:.5em 0}
.cite{color:var(--muted);font-size:.9rem!important}
svg{width:100%;height:auto;max-height:230px;display:block;margin:0 auto;flex-shrink:0}
.toggle{display:flex;gap:8px}
.toggle button{border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:999px;padding:5px 16px;font-size:.95rem;cursor:pointer}
.toggle button.on{background:var(--accent);color:#fff}
.caption{color:var(--muted);font-size:1rem}
.node rect{fill:#eff6ff;stroke:var(--accent);stroke-width:2}.node.fr rect{fill:#fff7ed;stroke:var(--warn)}
.node text{text-anchor:middle;font-size:18px;font-weight:700;fill:var(--ink)}
.edge{fill:none;stroke:#475569;stroke-width:2}.edge.warn{stroke:var(--warn);stroke-dasharray:6 4}
.lbl{font-size:13px;fill:#334155;text-anchor:middle}.lbl.warn{fill:var(--warn)}
footer{position:fixed;left:0;right:0;bottom:0;height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-size:.95rem;color:var(--muted)}
footer button{border:none;background:var(--ink);color:#fff;border-radius:8px;padding:8px 16px;font-size:1rem;cursor:pointer}
footer a{color:var(--muted)}
#progress{position:fixed;top:0;left:0;height:4px;background:var(--accent);transition:width .2s}
@media (max-width:760px){section{padding:20px;height:auto;min-height:calc(100vh - 92px)}.grid2{grid-template-columns:1fr}h1{font-size:2rem}h2{font-size:1.4rem}p,li{font-size:1rem}}
</style>
</head>
<body>
<div id="progress"></div>
<main>
__SLIDES__
</main>
<footer>
<button id="prev" aria-label="上一頁">←</button>
<span><span id="pageno"></span>　內容來源：<a id="srclink" href="#"></a></span>
<button id="next" aria-label="下一頁">→</button>
</footer>
<script id="chart-params" type="application/json">__PARAMS__</script>
<script>
(function(){
const P = JSON.parse(document.getElementById('chart-params').textContent);
const v = k => P[k].value;
const slides = [...document.querySelectorAll('main > section')];
let cur = 0;
function show(i){
  cur = Math.max(0, Math.min(slides.length-1, i));
  slides.forEach((s,j)=>s.classList.toggle('active', j===cur));
  document.getElementById('pageno').textContent = (cur+1) + ' / ' + slides.length;
  const src = slides[cur].dataset.src.split(' ');
  const a = document.getElementById('srclink');
  a.textContent = src.join('、'); a.href = '../' + src[0];
  document.getElementById('progress').style.width = ((cur+1)/slides.length*100) + '%';
  history.replaceState(null,'','#'+(cur+1));
}
document.getElementById('prev').onclick = ()=>show(cur-1);
document.getElementById('next').onclick = ()=>show(cur+1);
document.addEventListener('keydown', e=>{ if(e.key==='ArrowRight'||e.key==='PageDown') show(cur+1); if(e.key==='ArrowLeft'||e.key==='PageUp') show(cur-1); });

const NS='http://www.w3.org/2000/svg';
function el(tag, attrs, text){ const n=document.createElementNS(NS,tag); for(const k in attrs) n.setAttribute(k,attrs[k]); if(text!==undefined) n.textContent=text; return n; }

// ---- 第 7 頁：cwnd 模擬（依 RFC 5681 規則；網路容量為示意值）----
function simulate(mode){
  const capacity = 20, rounds = 32;  // 示意情境，非協定參數
  let cwnd = v('IW'), ssthresh = Infinity; const pts=[], th=[], loss=[];
  for(let r=0;r<rounds;r++){
    pts.push(cwnd); th.push(ssthresh);
    if(cwnd > capacity){
      loss.push(r);
      ssthresh = Math.max(Math.floor(cwnd / v('ssthreshDivisor')), v('ssthreshMin'));
      cwnd = (mode==='timeout') ? v('LW') : ssthresh;
      continue;
    }
    if(cwnd < ssthresh) cwnd = Math.min(cwnd*2, ssthresh===Infinity ? cwnd*2 : Math.max(ssthresh, cwnd+1));
    else cwnd = cwnd + v('caIncrementPerRTT');
  }
  return {pts, th, loss, capacity, rounds};
}
function drawCwnd(mode){
  const svg=document.getElementById('cwnd-chart'); if(!svg) return; svg.innerHTML='';
  const d=simulate(mode), W=640,H=260,L=50,R=20,T=20,B=40;
  const maxY=Math.max(...d.pts)+4, x=i=>L+i*(W-L-R)/(d.rounds-1), y=c=>H-B-c*(H-T-B)/maxY;
  svg.append(el('line',{x1:L,y1:H-B,x2:W-R,y2:H-B,stroke:'#94a3b8'}), el('line',{x1:L,y1:T,x2:L,y2:H-B,stroke:'#94a3b8'}));
  svg.append(el('text',{x:W-R,y:H-10,'text-anchor':'end','font-size':13,fill:'#64748b'},'時間（RTT）→'));
  svg.append(el('text',{x:L-8,y:T+4,'text-anchor':'end','font-size':13,fill:'#64748b'},'cwnd'));
  svg.append(el('line',{x1:L,y1:y(d.capacity),x2:W-R,y2:y(d.capacity),stroke:'#94a3b8','stroke-dasharray':'2 4'}));
  svg.append(el('text',{x:W-R,y:y(d.capacity)-6,'text-anchor':'end','font-size':12,fill:'#94a3b8'},'網路容量（示意）'));
  let thPath=''; d.th.forEach((t,i)=>{ if(t!==Infinity) thPath+=(thPath?'L':'M')+x(i)+','+y(t); });
  if(thPath) svg.append(el('path',{d:thPath,fill:'none',stroke:'#c2410c','stroke-dasharray':'6 4','stroke-width':2}));
  svg.append(el('path',{d:d.pts.map((c,i)=>(i?'L':'M')+x(i)+','+y(c)).join(''),fill:'none',stroke:'#1d4ed8','stroke-width':3}));
  d.loss.forEach(i=>svg.append(el('circle',{cx:x(i),cy:y(d.pts[i]),r:5,fill:'#c2410c'})));
  svg.append(el('text',{x:L+10,y:T+12,'font-size':13,fill:'#1d4ed8'},'— cwnd'));
  svg.append(el('text',{x:L+80,y:T+12,'font-size':13,fill:'#c2410c'},'- - ssthresh　● 遺失'));
  document.getElementById('cwnd-caption').textContent = mode==='timeout'
    ? '逾時：cwnd 掉回 1，重新慢啟動到新的 ssthresh，再改用壅塞避免。'
    : '3 個重複 ACK：cwnd 只降到 ssthresh，直接進入壅塞避免，形成鋸齒狀。';
}
document.querySelectorAll('.toggle button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.toggle button').forEach(x=>x.classList.toggle('on', x===b)); drawCwnd(b.dataset.mode); });
drawCwnd('timeout');


// ---- 第 11 頁：CUBIC 曲線 W(t) = C(t-K)^3 + Wmax（RFC 9438 §4.2）----
(function(){
  const svg=document.getElementById('cubic-chart'); if(!svg) return;
  const Wmax=100, C=v('C'), beta=v('betaCubic');      // Wmax 為示意值
  const start=Wmax*beta, K=Math.cbrt((Wmax-start)/C), tEnd=2*K;
  const W=640,H=240,L=50,R=20,T=20,B=36, x=t=>L+(t+0.15*K)*(W-L-R)/(tEnd+0.15*K), y0=start*0.9, y1=C*Math.pow(tEnd-K,3)+Wmax, y=w=>H-B-(w-y0)*(H-T-B)/(y1*1.03-y0);
  svg.append(el('line',{x1:L,y1:H-B,x2:W-R,y2:H-B,stroke:'#94a3b8'}), el('line',{x1:L,y1:T,x2:L,y2:H-B,stroke:'#94a3b8'}));
  svg.append(el('text',{x:W-R,y:H-8,'text-anchor':'end','font-size':13,fill:'#64748b'},'距上次壅塞的時間 t →'));
  svg.append(el('text',{x:L-8,y:T+4,'text-anchor':'end','font-size':13,fill:'#64748b'},'cwnd'));
  svg.append(el('line',{x1:L,y1:y(Wmax),x2:W-R,y2:y(Wmax),stroke:'#c2410c','stroke-dasharray':'6 4'}));
  svg.append(el('text',{x:L+6,y:y(Wmax)-6,'font-size':13,fill:'#c2410c'},'W_max（上次壅塞點）'));
  svg.append(el('path',{d:'M'+x(-0.15*K)+','+y(Wmax)+'L'+x(0)+','+y(Wmax)+'L'+x(0)+','+y(start),fill:'none',stroke:'#94a3b8','stroke-width':2}));
  svg.append(el('text',{x:x(0)+8,y:y(start)+16,'font-size':13,fill:'#64748b'},'壅塞：× β'));
  let p=''; for(let i=0;i<=120;i++){ const t=tEnd*i/120, w=C*Math.pow(t-K,3)+Wmax; p+=(i?'L':'M')+x(t)+','+y(w); }
  svg.append(el('path',{d:p,fill:'none',stroke:'#1d4ed8','stroke-width':3}));
  svg.append(el('line',{x1:x(K),y1:y(Wmax)-6,x2:x(K),y2:H-B,stroke:'#94a3b8','stroke-dasharray':'2 4'}));
  svg.append(el('text',{x:x(K),y:H-B+16,'text-anchor':'middle','font-size':13,fill:'#64748b'},'K'));
  svg.append(el('text',{x:x(K*0.55),y:y(start+(Wmax-start)*0.45),'text-anchor':'start','font-size':13,fill:'#1d4ed8'},'凹：先快後慢'));
  svg.append(el('text',{x:x(K*1.5),y:y(Wmax+(y1-Wmax)*0.75),'text-anchor':'end','font-size':13,fill:'#1d4ed8'},'凸：先慢後快'));
})();

const start=parseInt(location.hash.slice(1))||1; show(start-1);
})();
</script>
</body>
</html>
"""


def main():
    sections = []
    for path in DRAFTS:
        with open(path, "r", encoding="utf-8") as f:
            sections.append(f.read().strip())
    html = TEMPLATE.replace("__SLIDES__", "\n".join(sections))
    html = html.replace("__PARAMS__", json.dumps(CHART_PARAMS, ensure_ascii=False, indent=1))
    # 第 8 頁狀態轉移圖：在建置時把靜態 SVG 填入逐頁稿預留的空白 <svg>，讓 lint 也能檢查圖中文字與數字
    html = html.replace('<svg id="state-diagram" viewBox="0 0 640 250" role="img" aria-label="TCP 壅塞控制狀態轉移圖"></svg>',
                        '<svg id="state-diagram" viewBox="0 -8 640 268" role="img" aria-label="TCP 壅塞控制狀態轉移圖">' + STATE_DIAGRAM + '</svg>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已組合 {len(sections)} 頁 → {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
