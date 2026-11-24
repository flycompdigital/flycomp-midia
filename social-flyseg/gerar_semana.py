"""Gera o lote semanal da FlySeg Vision a partir de conteudo_semana.py.

Saída em social-flyseg/<pasta>/: slideN.html/.jpg, carrossel.pdf, resumo.html/.jpg,
story.html/.jpg, reelN.html/.jpg, reel-capa.jpg, reel.mp4, previa.jpg.
Uso: python3 gerar_semana.py
"""
import asyncio, pathlib, re, subprocess, sys
from playwright.async_api import async_playwright
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from conteudo_semana import POSTS

LOGO = "../../flyseg-materiais/folder-pvs/logo.png"
CHROME = "/usr/bin/google-chrome"

def y(t):
    return re.sub(r"<y>(.*?)</y>", r'<span class="y">\1</span>', t)

BASE = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#111111;color:#fff;font-family:Inter,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(70% 45% at 100% 0%,rgba(185,37,43,.35),transparent 70%),radial-gradient(60% 40% at 0% 100%,rgba(242,194,48,.10),transparent 70%)}
.bar{position:absolute;top:0;left:0;right:0;height:14px;background:linear-gradient(90deg,#F2C230 0 30%,#B9252B 30% 100%)}
.y{color:#F2C230}
.w{position:absolute;display:flex;flex-direction:column}.w>*{flex-shrink:0}
.logo{display:block}
.eb{font-weight:800;letter-spacing:4px;text-transform:uppercase;color:#F2C230}
h1,h2{font-family:'Inter Display';font-weight:900;letter-spacing:-1.5px;line-height:1.03}
h2{font-weight:800}
.sub{color:#d6d6d6;line-height:1.38}
ol{list-style:none;display:flex;flex-direction:column}
ol li{display:flex;align-items:flex-start;line-height:1.3;color:#f1f1f1}
ol li b{border-radius:50%;background:#B9252B;display:flex;align-items:center;justify-content:center;color:#fff;font-family:'Inter Display';font-weight:800;flex-shrink:0}
ul.fs{list-style:none;display:flex;flex-direction:column}
ul.fs li{display:flex;align-items:flex-start;line-height:1.32;color:#f1f1f1}
ul.fs li:before{content:"";flex-shrink:0;background:#F2C230;border-radius:4px}
.band{background:#F2C230;color:#111111;border-radius:26px}
.band h3{font-family:'Inter Display';font-weight:900;text-transform:uppercase;letter-spacing:1px}
.band ul{list-style:none;display:flex;flex-direction:column}
.band li{display:flex;align-items:flex-start;font-weight:700;line-height:1.25}
.band li:before{content:"";flex-shrink:0;background:#B9252B;border-radius:50%}
.pill{display:inline-block;align-self:flex-start;background:#B9252B;color:#fff;font-weight:800;text-transform:uppercase;letter-spacing:2px;border-radius:12px}
.cta{align-self:flex-start;background:#B9252B;color:#fff;font-weight:800;border-radius:18px}
.fonte{color:#9a9a9a}
.ft{position:absolute;display:flex;justify-content:space-between;align-items:center;color:#9a9a9a;border-top:2px solid rgba(255,255,255,.10)}
.ft b{color:#fff}.ft .sw{color:#F2C230;font-weight:800}
"""

FEED = BASE + """body{width:1080px;height:1350px}
.w{left:90px;right:90px;top:100px;bottom:180px;justify-content:center}
.logo{width:250px;margin-bottom:56px}.logo.big{width:420px;margin-bottom:60px}
.eb{font-size:30px;margin-bottom:30px}
h1{font-size:104px;margin-bottom:40px}h2{font-size:76px;margin-bottom:46px}
.sub{font-size:42px}
.fato{font-size:46px;line-height:1.42;color:#f1f1f1}
.fonte{font-size:30px;margin-top:44px}
ol{gap:40px}ol li{gap:30px;font-size:44px}ol li b{width:72px;height:72px;font-size:36px}
ul.fs{gap:38px}ul.fs li{gap:28px;font-size:42px}ul.fs li:before{width:14px;height:56px;margin-top:2px}
.extra{margin-top:40px;font-size:32px;color:#d6d6d6;border-left:6px solid #B9252B;padding-left:24px;line-height:1.35}
.cta{margin-top:56px;font-size:40px;padding:28px 46px}
.ft{left:90px;right:90px;bottom:64px;padding-top:26px;font-size:30px}
"""

RESUMO = BASE + """body{width:1080px;height:1350px}
.w{left:72px;right:72px;top:62px;bottom:52px}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px}
.top .logo{width:190px}
.top .eb{font-size:30px;text-align:right}
h1{font-size:76px;margin-bottom:26px}
.pill{font-size:30px;padding:8px 18px;margin-bottom:14px}
.risco{font-size:34px;line-height:1.35;color:#f1f1f1;margin-bottom:28px}
.pt{font-family:'Inter Display';font-weight:800;font-size:38px;margin-bottom:18px}
ol{gap:16px;margin-bottom:28px}ol li{gap:20px;font-size:34px}ol li b{width:52px;height:52px;font-size:30px}
.band{padding:26px 32px}
.band h3{font-size:32px;margin-bottom:14px}
.band ul{gap:10px}.band li{gap:16px;font-size:32px}.band li:before{width:16px;height:16px;margin-top:13px}
.rod{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:30px;color:#9a9a9a}
.rod b{color:#F2C230}
"""

STORY = BASE + """body{width:1080px;height:1920px}
.w{left:80px;right:80px;top:265px;bottom:385px;justify-content:center}
.logo{width:220px;margin-bottom:34px}
.eb{font-size:32px;margin-bottom:20px}
h1{font-size:80px;margin-bottom:30px}
.pt{font-family:'Inter Display';font-weight:800;font-size:42px;margin-bottom:20px}
ol{gap:18px;margin-bottom:34px}ol li{gap:24px;font-size:38px}ol li b{width:62px;height:62px;font-size:32px}
.band{padding:32px 36px}
.band h3{font-size:36px;margin-bottom:16px}
.band ul{gap:10px}.band li{gap:18px;font-size:34px}.band li:before{width:18px;height:18px;margin-top:14px}
.cta{margin-top:34px;font-size:40px;padding:24px 42px}
"""

REEL = BASE + """body{width:1080px;height:1920px}
.w{left:80px;right:80px;top:280px;bottom:380px;justify-content:center}
.logo{width:300px;margin-bottom:56px}.logo.big{width:480px;margin-bottom:64px}
.eb{font-size:36px;margin-bottom:34px}
h1{font-size:124px;margin-bottom:48px}h2{font-size:90px;margin-bottom:56px}
.sub{font-size:50px}
.fato{font-size:54px;line-height:1.42;color:#f1f1f1}
.fonte{font-size:34px;margin-top:48px}
ol{gap:48px}ol li{gap:32px;font-size:52px}ol li b{width:84px;height:84px;font-size:42px}
ul.fs{gap:44px}ul.fs li{gap:30px;font-size:50px}ul.fs li:before{width:16px;height:66px;margin-top:2px}
.cta{margin-top:60px;font-size:46px;padding:30px 50px}
"""

def doc(css, inner, foot=""):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bar"></div><div class="w">{inner}</div>{foot}</body></html>'

def ol(itens):
    return "<ol>" + "".join(f"<li><b>{i}</b><span>{y(t)}</span></li>" for i, t in enumerate(itens, 1)) + "</ol>"

def fs(itens):
    return '<ul class="fs">' + "".join(f"<li><span>{y(t)}</span></li>" for t in itens) + "</ul>"

def band(itens):
    return '<div class="band"><h3>Como a FlySeg ajuda</h3><ul>' + "".join(f"<li><span>{y(t)}</span></li>" for t in itens) + "</ul></div>"

def telas(p, reel=False):
    """Conteúdo das 5 telas (carrossel ou reel)."""
    fonte = f'<p class="fonte">Fonte: {p["fonte"]}</p>'
    extra = f'<p class="extra">{p["extra"]}</p>' if p.get("extra") and not reel else ""
    cta = "Fale com a gente pelo direct"
    return [
        f'<img class="logo" src="{LOGO}"><div class="eb">{p["eyebrow"]}</div><h1>{y(p["titulo"])}</h1><p class="sub">{p["sub"]}</p>',
        f'<div class="eb">{p["fato_titulo"]}</div><p class="fato">{p["fato"]}</p>{fonte}',
        f'<h2>{p["passos_titulo"]}</h2>{ol(p["passos"])}',
        f'<h2>Como a <span class="y">FlySeg</span> ajuda</h2>{fs(p["flyseg"])}{extra}',
        f'<img class="logo big" src="{LOGO}"><h2>{y(p["cta_titulo"])}</h2><p class="sub">{p["cta_sub"]}</p><div class="cta">{cta}</div>',
    ]

def resumo(p):
    return doc(RESUMO,
        f'<div class="top"><img class="logo" src="{LOGO}"><div class="eb">{p["eyebrow"]}</div></div>'
        f'<h1>{y(p["titulo"])}</h1>'
        f'<span class="pill">O risco</span><p class="risco">{p["risco"]}</p>'
        f'<div class="pt">{p["passos_titulo"]}</div>{ol(p["passos"])}'
        f'{band(p["flyseg_curto"])}'
        f'<div class="rod"><span>Fonte: {p["fonte"]}</span><b>flyseg.vision</b></div>')

def story(p):
    return doc(STORY,
        f'<img class="logo" src="{LOGO}"><div class="eb">{p["eyebrow"]}</div><h1>{y(p["titulo"])}</h1>'
        f'<div class="pt">{p["passos_titulo"]}</div>{ol(p["passos"])}{band(p["flyseg_curto"])}'
        f'<div class="cta">Fale com a gente pelo direct</div>')

async def shot(browser, html_path, out, w, h):
    pg = await browser.new_page(viewport={"width": w, "height": h})
    await pg.goto(html_path.as_uri())
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(200)
    over = await pg.evaluate("""() => { const w=document.querySelector('.w'); return w.scrollHeight - w.clientHeight; }""")
    await pg.screenshot(path=str(out), type="jpeg", quality=92)
    await pg.close()
    if over > 2:
        print(f"  ATENÇÃO: conteúdo transborda {over}px em {out.name}")

def video(d, n, seg=4.4, tr=0.5):
    ins, filt = [], []
    for i in range(1, n + 1):
        ins += ["-loop", "1", "-t", str(seg), "-framerate", "30", "-i", str(d / f"reel{i}.jpg")]
    ins += ["-f", "lavfi", "-t", "30", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    for i in range(n):
        filt.append(f"[{i}:v]scale=1080:1920,setsar=1,format=yuv420p,fps=30[v{i}]")
    prev, off = "v0", 0.0
    for i in range(1, n):
        off += seg - tr
        out = f"x{i}"
        filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={tr}:offset={off:.2f}[{out}]")
        prev = out
    total = seg * n - tr * (n - 1)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt),
           "-map", f"[{prev}]", "-map", f"{n}:a", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(d / "reel.mp4")]
    subprocess.run(cmd, check=True)

def previa(d, n):
    ims = [Image.open(d / f"slide{i}.jpg") for i in range(1, n + 1)]
    W = 360; H = int(1350 * W / 1080); g = 16
    sheet = Image.new("RGB", (g + n * (W + g), H + 2 * g), "#2a2a2a")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((W, H)), (g + i * (W + g), g))
    sheet.save(d / "previa.jpg", quality=88)
    a = Image.open(d / "resumo.jpg"); b = Image.open(d / "story.jpg"); c = Image.open(d / "reel-capa.jpg")
    h = 900
    parts = [im.resize((int(im.width * h / im.height), h)) for im in (a, b, c)]
    s2 = Image.new("RGB", (g + sum(p.width + g for p in parts), h + 2 * g), "#2a2a2a")
    x = g
    for p in parts:
        s2.paste(p, (x, g)); x += p.width + g
    s2.save(d / "previa-resumo-story-capa.jpg", quality=88)

async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path=CHROME)
        for p in POSTS:
            d = AQUI / p["pasta"]; d.mkdir(exist_ok=True)
            print(p["pasta"])
            sl = telas(p)
            for i, inner in enumerate(sl, 1):
                sw = f"Arraste →&nbsp;&nbsp;{i}/{len(sl)}" if i < len(sl) else f"{i}/{len(sl)}"
                foot = f'<div class="ft"><span><b>FlySeg Vision</b></span><span class="sw">{sw}</span></div>'
                f = d / f"slide{i}.html"; f.write_text(doc(FEED, inner, foot), encoding="utf-8")
                await shot(br, f, d / f"slide{i}.jpg", 1080, 1350)
            f = d / "resumo.html"; f.write_text(resumo(p), encoding="utf-8")
            await shot(br, f, d / "resumo.jpg", 1080, 1350)
            f = d / "story.html"; f.write_text(story(p), encoding="utf-8")
            await shot(br, f, d / "story.jpg", 1080, 1920)
            rl = telas(p, reel=True)
            for i, inner in enumerate(rl, 1):
                f = d / f"reel{i}.html"; f.write_text(doc(REEL, inner), encoding="utf-8")
                await shot(br, f, d / f"reel{i}.jpg", 1080, 1920)
            Image.open(d / "reel1.jpg").save(d / "reel-capa.jpg", quality=92)
            subprocess.run(["img2pdf", *[str(d / f"slide{i}.jpg") for i in range(1, len(sl) + 1)], "-o", str(d / "carrossel.pdf")], check=True)
            video(d, len(rl))
            previa(d, len(sl))
        await br.close()

asyncio.run(main())
