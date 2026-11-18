import asyncio, html, pathlib, json
from playwright.async_api import async_playwright
BASE = pathlib.Path("/home/claude/flyseg-posts")
LOGO = "file://" + str(BASE / "logo.png")

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:radial-gradient(120% 80% at 80% 0%,#3a1214 0%,#11161b 55%,#0b0f13 100%);color:#fff;font-family:'Inter';position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;right:0;height:10px;background:linear-gradient(90deg,#e31c24,#8b1e22)}
.wrap{position:absolute;inset:90px 90px 170px 90px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-weight:700;font-size:30px;letter-spacing:4px;text-transform:uppercase;color:#e9c260;margin-bottom:34px}
h1{font-family:'Inter Display';font-weight:800;font-size:92px;line-height:1.04;letter-spacing:-1.5px}
h2{font-family:'Inter Display';font-weight:800;font-size:82px;line-height:1.06;letter-spacing:-1.2px;margin-bottom:48px}
.sub{font-size:40px;line-height:1.4;color:#c5ccd3;margin-top:40px}
p.t{font-size:48px;line-height:1.42;color:#dfe4e9}
.gold{color:#e9c260}.red{color:#ff3b42}
ol{list-style:none;display:flex;flex-direction:column;gap:44px}
ol li{display:flex;gap:30px;align-items:flex-start;font-size:45px;line-height:1.35;color:#dfe4e9}
ol li b{flex:0 0 74px;height:74px;border-radius:50%;background:linear-gradient(135deg,#e31c24,#8b1e22);display:flex;align-items:center;justify-content:center;font-size:38px;color:#fff;font-family:'Inter Display'}
.card{border:2px solid rgba(233,194,96,.45);background:rgba(233,194,96,.08);border-radius:28px;padding:42px 46px;margin-top:28px}
.card h3{font-family:'Inter Display';font-size:46px;color:#e9c260;margin-bottom:12px}
.card p{font-size:40px;line-height:1.4;color:#dfe4e9}
.logo{width:300px;margin-bottom:56px}
.logo.big{width:440px}
.foot{position:absolute;left:90px;right:90px;bottom:60px;display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#7f8a94;border-top:2px solid rgba(255,255,255,.08);padding-top:26px}
.foot b{color:#fff}
.foot .sw{color:#e9c260;font-weight:700}
.cta{display:inline-block;margin-top:50px;padding:26px 44px;border-radius:18px;background:linear-gradient(90deg,#e31c24,#8b1e22);font-size:40px;font-weight:700}
.center{justify-content:center}
"""

def page(body, n, total):
    sw = f'<span class="sw">Arraste →&nbsp;&nbsp;{n}/{total}</span>' if n < total else f'<span class="sw">{n}/{total}</span>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bar"></div>
<div class="wrap">{body}</div><div class="foot"><span><b>FlySeg Vision</b> · Segurança colaborativa</span>{sw}</div></body></html>"""

POSTS = {
 "seguranca-colaborativa": [
  f'<img class="logo" src="{LOGO}"><div class="eyebrow">Programa Vizinhança Segura</div><h1>Um cinturão digital <span class="gold">contra o crime.</span></h1><p class="sub">Segurança colaborativa com o MWL.camera, rua por rua.</p>',
  '<div class="eyebrow">Comece pelo que já existe</div><h2>As câmeras que você já tem entram na rede.</h2><p class="t">Sem trocar o seu equipamento: as câmeras da sua casa ou do seu comércio são integradas à plataforma <span class="gold">MWL.camera</span>.</p>',
  '<div class="eyebrow">Raio de 500 metros</div><h2>Veja a rua, não só a sua porta.</h2><p class="t">Quem participa acompanha as câmeras <span class="gold">compartilhadas pelos vizinhos</span> num raio de 500 m do seu endereço, não importa quem instalou cada uma.</p>',
  '<div class="eyebrow">Como funciona</div><h2>A rua conectada</h2><ol><li><b>1</b><span>As câmeras compartilhadas formam o <span class="gold">cinturão digital</span>.</span></li><li><b>2</b><span>Um alerta ou botão de pânico avisa os vizinhos.</span></li><li><b>3</b><span>A central <span class="gold">Vision SOC</span> acompanha 24h e aciona as autoridades.</span></li></ol>',
  '<div class="eyebrow">Placa Vizinhança Segura</div><h2>A rua avisa quem passa.</h2><p class="t">A placa <span class="gold">Vizinhança Segura</span> mostra que aquela rua faz parte do programa.</p><div class="card"><h3>Pioneira no MWL.camera</h3><p>E criadora do ODL.camera, o totem de segurança da rua.</p></div>',
  f'<div class="center" style="display:flex;flex-direction:column;height:100%"><img class="logo big" src="{LOGO}"><h2>Coloque a sua rua no Vizinhança Segura.</h2><p class="t">Monitoramento eletrônico 24h, com quem entende do assunto.</p><span class="cta">Fale com a gente pelo direct</span></div>',
 ],
 "odl-camera": [
  f'<img class="logo" src="{LOGO}"><div class="eyebrow">ODL.camera</div><h1>O totem de segurança <span class="gold">da sua rua.</span></h1><p class="sub">ODL, de <span class="gold">Olho de Lince</span>. Criado pela FlySeg e ligado ao MWL.camera.</p>',
  '<div class="eyebrow">Duas versões</div><h2>Para a rua e para a fachada.</h2><div class="card"><h3>Totem / poste</h3><p>Instalado na rua, cobre a via e o movimento ao redor.</p></div><div class="card"><h3>Fachada (box)</h3><p>Para casas e comércios que querem fazer parte da rede.</p></div>',
  '<div class="eyebrow">Na prática</div><h2>Tudo no MWL.camera</h2><ol><li><b>1</b><span>Imagens da rua na plataforma de segurança colaborativa.</span></li><li><b>2</b><span>Botão de pânico e alertas para os vizinhos.</span></li><li><b>3</b><span>Aviso se a câmera, o gravador ou a internet ficarem fora do ar.</span></li><li><b>4</b><span>Central Vision SOC 24h acionando as autoridades.</span></li></ol>',
  f'<div class="center" style="display:flex;flex-direction:column;height:100%"><img class="logo big" src="{LOGO}"><h2>Quer um ODL.camera na sua rua?</h2><p class="t">Saiba mais em <span class="gold">flyseg.vision</span></p><span class="cta">Fale com a gente pelo direct</span></div>',
 ],
 "vision-soc-integradores": [
  f'<img class="logo" src="{LOGO}"><div class="eyebrow">Para integradores</div><h1>Venda monitoramento 24h <span class="gold">com a sua marca.</span></h1><p class="sub">Vision SOC white label, sem montar central própria.</p>',
  '<div class="eyebrow">O modelo</div><h2>Você vende. A central opera.</h2><p class="t">Você atende o seu cliente com a sua marca. A central <span class="gold">Vision SOC</span> da FlySeg acompanha as ocorrências 24h, todos os dias.</p>',
  '<div class="eyebrow">O que a central faz</div><h2>Monitoramento eletrônico 24h</h2><ol><li><b>1</b><span>Acompanha as ocorrências do <span class="gold">MWL.camera</span>: alerta, emergência e pânico.</span></li><li><b>2</b><span>Aciona as autoridades quando é preciso.</span></li><li><b>3</b><span>Avisa quando câmera, gravador ou link ficam fora do ar.</span></li></ol>',
  f'<div class="center" style="display:flex;flex-direction:column;height:100%"><img class="logo big" src="{LOGO}"><h2>Planos e preços no site.</h2><p class="t"><span class="gold">flyseg.vision</span></p><span class="cta">Fale com a gente pelo direct</span></div>',
 ],
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for nome, slides in POSTS.items():
            d = BASE / nome; d.mkdir(exist_ok=True)
            for i, body in enumerate(slides, 1):
                f = d / f"slide{i}.html"; f.write_text(page(body, i, len(slides)), encoding="utf-8")
                await pg.goto("file://" + str(f)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(150)
                await pg.screenshot(path=str(d / f"slide{i}.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
