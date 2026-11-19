import json, subprocess, sys
FF="@font-face{font-family:C;src:url(fonts/Courgette.woff2)}"
LAMP='''<svg class="lamp" viewBox="0 0 100 120"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7a0"/><stop offset=".55" stop-color="#f2b92e"/><stop offset="1" stop-color="#c98a12"/></linearGradient></defs>
<g stroke="#e9a91e" stroke-width="5" stroke-linecap="round"><line x1="50" y1="2" x2="50" y2="14"/><line x1="18" y1="14" x2="25" y2="23"/><line x1="82" y1="14" x2="75" y2="23"/><line x1="4" y1="40" x2="15" y2="42"/><line x1="96" y1="40" x2="85" y2="42"/></g>
<path d="M50 22c-16 0-28 12-28 27 0 10 5 17 11 22 3 3 5 6 5 10v4h24v-4c0-4 2-7 5-10 6-5 11-12 11-22 0-15-12-27-28-27z" fill="url(#g)"/>
<path d="M50 63c-8-6-13-10-13-16 0-4 3-7 7-7 3 0 5 2 6 4 1-2 3-4 6-4 4 0 7 3 7 7 0 6-5 10-13 16z" fill="#e2574c"/>
<rect x="38" y="89" width="24" height="7" rx="3" fill="#8a6a2e"/><rect x="40" y="98" width="20" height="7" rx="3" fill="#6e5424"/><rect x="44" y="107" width="12" height="6" rx="3" fill="#57411b"/></svg>'''
SWOOSH='''<svg class="sw" viewBox="0 0 600 60" preserveAspectRatio="none"><defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#e9a91e" stop-opacity="0"/><stop offset=".25" stop-color="#e9a91e"/><stop offset="1" stop-color="#f2c14e"/></linearGradient></defs>
<path d="M10 40 C 150 62, 300 10, 430 34 S 560 44, 590 20" fill="none" stroke="url(#s)" stroke-width="3.5" stroke-linecap="round"/>
<path d="M455 36c-6-5-10-8-10-12 0-3 2-5 5-5 2 0 4 1 5 3 1-2 3-3 5-3 3 0 5 2 5 5 0 4-4 7-10 12z" fill="none" stroke="#e9a91e" stroke-width="2.5"/></svg>'''
CSS=FF+'''*{margin:0;padding:0}html,body{background:transparent}
.wrap{position:relative;display:inline-flex;flex-direction:column;align-items:center;padding:110px 90px 40px}
.wm{font-family:C;line-height:1;white-space:nowrap;position:relative}
.lu{padding:0 .02em 0 .18em;background:linear-gradient(180deg,#fbe08a 0%,#eab12f 45%,#c58712 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 1px 0 rgba(120,80,0,.25))}
.t{padding:0 .18em 0 0;background:linear-gradient(180deg,#38b3a6,#1a8580 55%,#0f6a5e);-webkit-background-clip:text;color:transparent;margin-left:.04em}
.i{position:relative;display:inline-block}
.lamp{position:absolute;left:50%;transform:translateX(-46%);width:.4em;top:-.3em}
.sw{display:block;width:100%;height:.3em;margin-top:-.08em}
.tag{font-family:C;color:#c58a17;margin-top:.2em}
.escuro .lu{filter:drop-shadow(0 0 12px rgba(242,185,46,.55))}.escuro .t{background:linear-gradient(180deg,#7fe3d6,#3cc1b2 60%,#1f9a8e);-webkit-background-clip:text;filter:drop-shadow(0 0 10px rgba(60,193,178,.45))}
'''
def html(size,body,bg="transparent",extra=""):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}{extra}</style></head><body>{body}</body></html>'
def wordmark(size,cls="",tag=False):
    t=f'<div class="tag" style="font-size:{size*0.28}px">A Luz do Amor <span style="color:#e2574c">♥</span> A Força da Inclusão</div>' if tag else ""
    return f'<div class="wrap {cls}" id="alvo"><div class="wm" style="font-size:{size}px"><span class="lu">Lum<span class="i">ı{LAMP}</span>na</span><span class="t">T21</span></div><div style="width:100%;font-size:{size}px">{SWOOSH}</div>{t}</div>'
jobs={
 'luminat21-logo-horizontal':(wordmark(200),"transparent",""),
 'luminat21-logo-horizontal-assinatura':(wordmark(200,tag=True),"transparent",""),
 'luminat21-logo-fundo-escuro-transparente':(wordmark(200,"escuro"),"transparent",""),
 'luminat21-logo-escuro':(wordmark(200,"escuro"),"#141414","body{padding:40px}"),
 'luminat21-logo-empilhado':(f'<div class="wrap" id="alvo"><div class="wm" style="font-size:190px;text-align:center"><span class="lu">Lum<span class="i">ı{LAMP}</span>na</span><br><span class="t" style="margin:0">T21</span></div><div style="width:100%;font-size:190px">{SWOOSH}</div></div>',"transparent",""),
}
import os
os.makedirs('out',exist_ok=True)
for n,(b,bg,ex) in jobs.items(): open(f'{n}.html','w').write(html(0,b,bg,ex))
