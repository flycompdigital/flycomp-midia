"""Vídeo de 30 s do MWL.camera em motion graphics (Reels 1080x1920), sem avatar e sem narração.
Gera as telas em HTML, renderiza com Playwright e monta com ffmpeg (zoom suave + transições)."""
import asyncio, pathlib, subprocess

D = pathlib.Path(__file__).parent.resolve()
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:Inter,sans-serif;color:#f8fafc;background:radial-gradient(110% 60% at 85% 0%,#1e3a8a 0%,#0b1120 62%);position:relative;overflow:hidden}
.w{position:absolute;left:90px;right:90px;top:260px;bottom:420px;display:flex;flex-direction:column;justify-content:center}
.eb{font-size:34px;font-weight:800;letter-spacing:5px;color:#93c5fd;text-transform:uppercase}
h1{font-family:'Inter Display',Inter;font-weight:900;font-size:112px;line-height:1.04;letter-spacing:-1.5px;margin-top:22px}
h1 span{color:#8fb4ff}
p{font-size:48px;line-height:1.42;color:#cbd5e1;margin-top:28px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:60px;position:relative}
.cam{height:340px;border-radius:26px;background:#111a2e;border:2px solid #24314f;position:relative;padding:20px;font-size:32px;color:#cbd5e1}
.cam:after{content:"AO VIVO";position:absolute;right:16px;top:16px;background:#dc2626;color:#fff;font-size:20px;font-weight:800;padding:6px 12px;border-radius:8px}
.cam.off{opacity:.45}.cam.off:after{content:"SOZINHA";background:#334155}
svg.lig{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.raio{width:600px;height:600px;flex-shrink:0;border-radius:50%;border:4px dashed #60a5fa;margin:60px auto 0;position:relative;background:radial-gradient(circle,rgba(59,130,246,.18),transparent 70%)}
.raio i{position:absolute;width:44px;height:44px;border-radius:50%;background:#60a5fa;box-shadow:0 0 30px #60a5fa}
.raio b{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:64px;font-weight:900}
.duo{display:grid;gap:30px;margin-top:50px}
.pl{display:flex;gap:40px;align-items:center;background:#16213a;border:2px solid #24314f;border-radius:34px;padding:44px}
.pl img{width:220px;height:220px;object-fit:contain}
.pl small{display:block;font-size:26px;font-weight:800;letter-spacing:3px;color:#93c5fd;text-transform:uppercase}
.pl b{display:block;font-size:60px;margin-top:6px}
.oc{background:#2a0f14;border:2px solid #7f1d1d;border-radius:30px;padding:44px;margin-top:60px;font-size:44px;line-height:1.4}
.oc b{color:#fca5a5;display:block;font-size:48px;margin-bottom:8px}
.painel{background:#16213a;border:2px solid #24314f;border-left:10px solid #34d399;border-radius:28px;padding:44px;margin-top:34px;font-size:42px;line-height:1.42;color:#cbd5e1}
.painel b{display:block;color:#6ee7b7;font-size:46px;margin-bottom:6px}
.fim{align-items:center;text-align:center}
.fim img.logo{width:240px}
.qr{width:360px;height:360px;flex-shrink:0;background:#fff;border-radius:24px;padding:16px;margin:40px auto 0}
.url{font-size:76px;font-weight:900;color:#8fb4ff;margin-top:26px}
.l190{position:absolute;left:90px;right:90px;bottom:430px;text-align:center;font-size:36px;color:#94a3b8}
.marca{position:absolute;left:90px;top:130px;display:flex;align-items:center;gap:18px;font-size:34px;font-weight:800}
.marca img{width:70px}
"""

def tela(corpo, marca=True, extra=""):
    m = '<div class="marca"><img src="mwl-logo.png">MWL.camera</div>' if marca else ""
    return f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{m}<div class="w {extra}">{corpo}</div></body></html>'

CAMS = ["Casa 12", "Padaria", "Condomínio", "Mercadinho"]
def grade(ligada):
    cams = "".join(f'<div class="cam{"" if ligada else " off"}">{c}</div>' for c in CAMS)
    linhas = ('<svg class="lig" viewBox="0 0 900 528" preserveAspectRatio="none"><g stroke="#60a5fa" stroke-width="6" stroke-dasharray="14 10">'
              '<line x1="225" y1="125" x2="675" y2="125"/><line x1="225" y1="403" x2="675" y2="403"/><line x1="225" y1="125" x2="225" y2="403"/>'
              '<line x1="675" y1="125" x2="675" y2="403"/><line x1="225" y1="125" x2="675" y2="403"/></g></svg>') if ligada else ""
    return f'<div class="grid">{cams}{linhas}</div>'

TELAS = [
 ("t1a", tela('<div class="eb">Segurança privada colaborativa</div><h1>Na sua rua já tem <span>câmera.</span></h1><p>Mas cada uma olha só para o próprio portão.</p>' + grade(False))),
 ("t1b", tela('<div class="eb">Segurança privada colaborativa</div><h1>As câmeras da sua rua, <span>numa rede só.</span></h1><p>Quem decide o que compartilha é sempre o dono da câmera.</p>' + grade(True))),
 ("t2", tela('<div class="eb">Como funciona</div><h1>Vizinhos acompanham <span>pelo celular.</span></h1><p>As câmeras compartilhadas num raio de 500 metros, ao vivo e com gravação.</p>'
             '<div class="raio"><i style="left:120px;top:90px"></i><i style="right:110px;top:160px"></i><i style="left:200px;bottom:110px"></i><i style="right:180px;bottom:80px"></i><i style="left:60px;top:300px"></i><b>500 m</b></div>')),
 ("t3", tela('<div class="eb">Duas plataformas white label</div><h1>O sistema e <span>o hardware.</span></h1><div class="duo">'
             '<div class="pl"><img src="mwl-logo.png"><div><small>Sistema</small><b>Plataforma MWL</b></div></div>'
             '<div class="pl"><img src="lince.png" style="filter:drop-shadow(0 0 14px rgba(240,149,74,.5))"><div><small>Hardware</small><b>Totem Olho de Lince</b></div></div></div>')),
 ("t4", tela('<div class="eb">Na ocorrência</div><h1>A gravação chega <span>junto.</span></h1>'
             '<div class="oc"><b>● Ocorrência registrada</b>Com local, hora e a gravação anexada, para quem está perto.</div>'
             '<div class="painel"><b>Painel das forças de segurança</b>As polícias e a Guarda Civil da região que aderirem veem as ocorrências no painel delas, sem custo.</div>')),
 ("t5", tela('<img class="logo" src="mwl-logo.png" style="align-self:center"><h1 style="text-align:center;font-size:88px">A sua rua vigiada <span>por quem mora nela.</span></h1>'
             '<img class="qr" src="qr.svg"><div class="url">mwl.camera</div><p style="font-size:42px">Encontre um integrador na sua região.</p><p style="font-size:34px;color:#94a3b8;margin-top:22px">Em emergência, ligue 190.</p>', marca=False, extra="fim")
          ),
]
DUR = {"t1a": 3.5, "t1b": 4.5, "t2": 5.5, "t3": 5.5, "t4": 5.5, "t5": 5.5}
XF = 0.6

async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for nome, html in TELAS:
            f = D / f"{nome}.html"; f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(D / f"{nome}.png"))
        await b.close()

def montar():
    nomes = [n for n, _ in TELAS]
    ins, filt = [], []
    for i, n in enumerate(nomes):
        d = DUR[n] + XF
        ins += ["-loop", "1", "-t", f"{d}", "-i", str(D / f"{n}.png")]
        fr = int(d * 30)
        filt.append(f"[{i}:v]scale=1188:-1,zoompan=z='min(zoom+0.0007,1.08)':d={fr}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p,setsar=1[v{i}]")
    cur, t = "v0", DUR[nomes[0]]
    for i in range(1, len(nomes)):
        out = f"x{i}"
        filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration={XF}:offset={t - XF + XF}[{out}]")
        cur = out; t += DUR[nomes[i]]
    total = sum(DUR.values()) + XF
    cmd = ["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", ";".join(filt), "-map", f"[{cur}]", "-map", f"{len(nomes)}:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
           "-movflags", "+faststart", str(D / "reel.mp4")]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    from playwright.async_api import async_playwright
    asyncio.run(render())
    montar()
