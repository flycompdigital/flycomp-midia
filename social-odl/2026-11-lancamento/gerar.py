"""Gera os posts de lançamento do @odl.camera (carrosséis 1080x1350 e story 1080x1920)."""
import asyncio, pathlib
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).parent.resolve()
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#07090c;color:#fff;font-family:Inter,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;left:-260px;top:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(240,149,74,.22),transparent 62%)}
body:after{content:"";position:absolute;right:-300px;bottom:-300px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(112,226,234,.16),transparent 62%)}
.w{position:absolute;inset:96px 90px 150px;display:flex;flex-direction:column;z-index:2}
.eb{font-size:30px;font-weight:800;letter-spacing:5px;color:#70e2ea;text-transform:uppercase}
h1{font-family:'Inter Display',Inter;font-weight:900;font-size:92px;line-height:1.02;letter-spacing:-1.5px;margin-top:26px}
h2{font-family:'Inter Display',Inter;font-weight:900;font-size:70px;line-height:1.06;letter-spacing:-1px;margin-top:22px}
.o{color:#f0954a}.c{color:#70e2ea}.y{color:#F2C230}
p.s{font-size:38px;line-height:1.45;color:#c9d1d9;margin-top:30px}
.card{border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);border-radius:28px;padding:30px 36px;margin-top:24px}
.card h3{font-size:44px;font-weight:800}.card p{font-size:32px;color:#c9d1d9;line-height:1.4;margin-top:8px}
.card .n{font-size:56px;font-weight:900}
.foot{position:absolute;left:90px;right:90px;bottom:60px;display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#8b96a1;z-index:2;border-top:2px solid rgba(255,255,255,.08);padding-top:24px}
.foot b{color:#fff}.sw{color:#f0954a;font-weight:700}
.lince{position:absolute;z-index:1}
ul{list-style:none;margin-top:20px}li{font-size:44px;line-height:1.35;padding:20px 0 20px 60px;position:relative;color:#e6edf3}
li:before{content:"";position:absolute;left:0;top:38px;width:26px;height:26px;border-radius:50%;background:#f0954a;box-shadow:0 0 18px rgba(240,149,74,.7)}
.btn{display:inline-block;margin-top:40px;background:#f0954a;color:#07090c;font-weight:900;font-size:38px;padding:24px 40px;border-radius:999px;align-self:flex-start}
"""

def pagina(corpo, rodape, lince=None, story=False):
    extra = "body{height:1920px}.w{inset:260px 90px 420px}.foot{bottom:380px}" if story else ""
    img = ""
    if lince:
        img = f'<img class="lince" src="lince.png" style="{lince}">'
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}{extra}</style></head>
<body>{img}<div class="w">{corpo}</div><div class="foot">{rodape}</div></body></html>"""

def rod(n, tot, ultimo=False):
    seta = f'<span class="sw">{n}/{tot}</span>' if ultimo else f'<span class="sw">Arraste →&nbsp;&nbsp;{n}/{tot}</span>'
    return f'<span><b>ODL.camera</b> · Olho de Lince</span>{seta}'

POSTS = {
 "post1-apresentacao": [
  pagina('<div class="eb">Olho de Lince</div><h1>Pare de apenas<br><span class="o">gravar.</span><br>Comece a<br><span class="c">proteger.</span></h1>',
         rod(1,4), lince="right:-40px;bottom:120px;width:520px;opacity:.95"),
  pagina('<div class="eb">O que é</div><h2>Mais que um totem <span class="o">de câmeras.</span></h2><ul><li>Câmeras Full HD que filmam colorido à noite</li><li>Sirene e giroflex integrados</li><li>Botão de emergência no app</li><li>Gravação de 7 dias</li></ul>', rod(2,4), lince="right:-70px;bottom:110px;width:430px;opacity:.35"),
  pagina('<div class="eb">Na emergência</div><h2>Ajuda <span class="c">imediata</span>, sem esperar.</h2><div class="card"><h3>1. Você aperta no app</h3><p>De onde estiver.</p></div><div class="card"><h3>2. Sirene e giroflex disparam</h3><p>Na hora, no local.</p></div><div class="card"><h3>3. A ocorrência abre na plataforma MWL.camera</h3><p>As forças cadastradas veem os 30 segundos anteriores ao alerta.</p></div>', rod(3,4)),
  pagina('<img src="lince.png" style="width:300px;align-self:center;margin-top:10px"><h2 style="text-align:center">Segurança inteligente e <span class="c">amiga do meio ambiente.</span></h2><p class="s" style="text-align:center">Conheça o Totem Olho de Lince em <b class="y">olhodelince.com.br</b></p><span class="btn" style="align-self:center">Fale com a gente pelo direct</span>', rod(4,4,True)),
 ],
 "post2-modelos": [
  pagina('<div class="eb">Três modelos</div><h1>Um para cada <span class="o">rua.</span></h1><p class="s">Totem, Box e Fisheye: escolha o que cabe na sua calçada e na sua fachada.</p>', rod(1,4), lince="right:-60px;bottom:110px;width:460px;opacity:.9"),
  pagina('<div class="eb">Totem</div><h2><span class="o">360°</span> na calçada.</h2><ul><li>Poste de aço com quatro câmeras</li><li>Sirene, giroflex e LED</li><li>Fiação protegida, em baixa voltagem</li><li>Bateria opcional de até 1h20</li></ul>', rod(2,4), lince="right:-70px;bottom:110px;width:430px;opacity:.35"),
  pagina('<div class="eb">Box</div><h2><span class="c">180°</span> na fachada.</h2><ul><li>Duas câmeras para toda a frente do imóvel</li><li>Sirene, giroflex e LED</li><li>Áudio do ambiente</li><li>Mesma plataforma, mesma rede</li></ul>', rod(3,4), lince="right:-70px;bottom:110px;width:430px;opacity:.35"),
  pagina('<div class="eb">Fisheye</div><h2>Uma lente, <span class="y">instalação simples.</span></h2><ul><li>Câmera olho de peixe acima do portão</li><li>Só um cabo de rede e uma tomada comum 127V</li><li>Com áudio</li></ul><span class="btn">Fale com a gente pelo direct</span>', rod(4,4,True), lince="right:-70px;bottom:110px;width:430px;opacity:.35"),
 ],
 "post3-por-que-olho-de-lince": [
  pagina('<div class="eb">Por que Olho de Lince</div><h1>Um nome com <span class="o">história.</span></h1><p class="s">Quando percebia alguém mal-intencionado e conseguia impedir antes que algo acontecesse, ele dizia que tinha <b class="y">olho de lince</b>.</p>', rod(1,3), lince="right:-70px;bottom:110px;width:430px;opacity:.35"),
  pagina('<img src="pai.webp" style="width:100%;height:560px;object-fit:cover;border-radius:28px"><h2 style="font-size:58px">Marco Antônio Munis Pontes, <span class="y">o Paizão.</span></h2><p class="s" style="font-size:34px">Atento, protetor e de riso fácil. O Olho de Lince é a homenagem de um filho ao homem mais humano que conheceu.</p>', rod(2,3)),
  pagina('<img src="fusca.webp" style="width:100%;height:560px;object-fit:cover;border-radius:28px"><h2 style="font-size:58px">Até a cor tem <span class="y">significado.</span></h2><p class="s" style="font-size:34px">O amarelo do totem vem do Fusca 77 amarelo Java que ele deu ao filho. <i>Seu Filhão, Marcus M. Pontes</i></p>', rod(3,3,True)),
 ],
}

STORY = pagina('<div class="eb">Olho de Lince · ODL.camera</div><h1 style="font-size:96px">Pare de apenas <span class="o">gravar.</span> Comece a <span class="c">proteger.</span></h1><ul><li>Totem, Box e Fisheye</li><li>Sirene e giroflex integrados</li><li>Emergência no app e na plataforma MWL.camera</li></ul><span class="btn">Fale com a gente pelo direct</span>',
               '<span><b>ODL.camera</b> · Olho de Lince</span><span class="sw">olhodelince.com.br</span>', lince="left:405px;bottom:440px;width:270px;opacity:.85", story=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for nome, telas in POSTS.items():
            pasta = D / nome; pasta.mkdir(exist_ok=True)
            for i, html in enumerate(telas, 1):
                f = pasta / f"slide{i}.html"; f.write_text(html.replace('src="', 'src="../'), encoding="utf-8")
                pg = await b.new_page(viewport={"width": 1080, "height": 1350})
                await pg.goto(f.as_uri().replace(f"/{nome}/", f"/{nome}/")); await pg.wait_for_timeout(400)
                await pg.screenshot(path=str(pasta / f"slide{i}.jpg"), type="jpeg", quality=92); await pg.close()
        f = D / "story.html"; f.write_text(STORY, encoding="utf-8")
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(D / "story.jpg"), type="jpeg", quality=92)
        await b.close()

asyncio.run(main())
