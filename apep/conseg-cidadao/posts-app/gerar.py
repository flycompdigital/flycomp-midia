"""Carrossel (1080x1350) e story (1080x1920): app do CONSEG Cidadão e o Bip IA."""
import asyncio, pathlib, shutil
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).parent.resolve()
for f in ["conseg-cidadao.svg", "apep-logo.png"]:
    shutil.copy(D.parent / f, D / f)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#17212d;color:#fff;font-family:Inter,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;right:-240px;top:-240px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(227,166,48,.22),transparent 65%)}
.w{position:absolute;inset:100px 90px 160px;display:flex;flex-direction:column;justify-content:center;z-index:2}
.lg{height:96px;align-self:flex-start}
.eb{font-size:30px;font-weight:800;letter-spacing:5px;color:#e3a630;text-transform:uppercase;margin-top:40px}
h1{font-family:'Inter Display',Inter;font-weight:900;font-size:100px;line-height:1.02;letter-spacing:-1.5px;margin-top:22px}
h2{font-family:'Inter Display',Inter;font-weight:900;font-size:74px;line-height:1.06;letter-spacing:-1px;margin-top:18px}
.g{color:#e3a630}
p.s{font-size:44px;line-height:1.45;color:#cbd5e1;margin-top:30px}
.card{background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.1);border-left:10px solid #e3a630;border-radius:26px;padding:28px 34px;margin-top:22px}
.card b{display:block;font-size:30px;color:#e3a630;letter-spacing:2px}.card h3{font-size:44px;margin-top:6px}.card p{font-size:32px;color:#cbd5e1;line-height:1.35;margin-top:6px}
.pauta{background:#06543c;border-radius:30px;padding:40px;margin-top:40px}
.pauta div{background:rgba(255,255,255,.1);border-radius:18px;padding:22px 26px;font-size:38px;margin-top:16px}
.foot{position:absolute;left:90px;right:90px;bottom:60px;display:flex;justify-content:space-between;font-size:28px;color:#94a3b8;border-top:2px solid rgba(255,255,255,.1);padding-top:24px;z-index:2}
.foot b{color:#fff}.sw{color:#e3a630;font-weight:700}
.btn{display:inline-block;margin-top:40px;background:#e3a630;color:#17212d;font-weight:900;font-size:40px;padding:24px 44px;border-radius:999px;align-self:flex-start}
.fone{position:absolute;right:0;top:430px;width:280px;border-radius:56px;border:12px solid #0b1118;box-shadow:0 30px 80px rgba(0,0,0,.5);overflow:hidden;z-index:3}
.fone img{display:block;width:100%}
.chip{display:inline-block;border:3px solid rgba(227,166,48,.6);border-radius:999px;padding:18px 30px;font-size:34px;margin:14px 10px 0 0;color:#fff}
.passo{display:flex;gap:22px;align-items:center;font-size:40px;margin-top:26px}.passo i{flex:none;width:72px;height:72px;border-radius:50%;background:#e3a630;color:#17212d;font-style:normal;font-weight:900;display:grid;place-items:center}
.aviso{font-size:28px;color:#94a3b8;margin-top:36px;line-height:1.4}
"""

def tela(corpo, rodape, story=False):
    extra = "body{height:1920px}.w{inset:260px 90px 430px}.foot{bottom:370px}" if story else ""
    return f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}{extra}</style></head><body><div class="w">{corpo}</div><div class="foot">{rodape}</div></body></html>'

def rod(n, t, fim=False):
    return f'<span><b>CONSEG Cidadão</b> · APEP Brasil</span><span class="sw">{"" if fim else "Arraste →&nbsp;&nbsp;"}{n}/{t}</span>'

SLIDES = [
 tela('<style>.w{justify-content:flex-start}</style><img class="lg" src="conseg-cidadao.svg"><div class="eb">Novo</div><h1 style="font-size:90px">O CONSEG Cidadão <span class="g">no seu celular.</span></h1><p class="s" style="max-width:540px;font-size:40px">App gratuito, com o Bip IA para tirar dúvidas e a área para registrar as demandas da rua.</p><div class="fone"><img src="app-bip.png"></div>', rod(1, 4)),
 tela('<div class="eb" style="margin-top:0">Conheça o Bip IA</div><h2>Dúvidas sobre o CONSEG? <span class="g">Pergunte 24h.</span></h2><p class="s">O assistente do CONSEG Cidadão explica como funciona o conselho, ajuda a organizar a rua e transforma a reclamação em uma demanda bem escrita.</p><div style="margin-top:26px"><span class="chip">O que é o CONSEG?</span><span class="chip">Poste apagado é com quem?</span><span class="chip">Como escrevo a demanda?</span></div>', rod(2, 4)),
 tela('<div class="eb" style="margin-top:0">Área do cidadão</div><h2>A demanda da rua <span class="g">registrada e acompanhada.</span></h2><div class="card"><b>1</b><h3>Registre</h3><p>O que é, onde e desde quando. Sem nomes de pessoas.</p></div><div class="card"><b>2</b><h3>Apoie</h3><p>Toque em "Também quero" nas demandas dos vizinhos.</p></div><div class="card"><b>3</b><h3>Acompanhe</h3><p>Veja o que foi à pauta e o retorno do CONSEG.</p></div>', rod(3, 4)),
 tela('<div class="eb" style="margin-top:0">Instale em segundos</div><h2>Abra <span class="g">con.seg.br/app</span> no celular.</h2><div class="passo"><i>📱</i><span><b>iPhone:</b> Compartilhar → Adicionar à Tela de Início</span></div><div class="passo"><i>🤖</i><span><b>Android:</b> toque em Instalar</span></div><span class="btn">con.seg.br/app</span><p class="aviso">Não é canal oficial nem de emergência. Emergência: 190. Denúncia anônima: 181.</p>', rod(4, 4, True)),
]
STORY = tela('<img class="lg" src="conseg-cidadao.svg"><h1 style="font-size:92px">O CONSEG Cidadão <span class="g">no seu celular.</span></h1><p class="s">Bip IA 24h e as demandas da sua rua num app gratuito.</p><img src="qr-app.png" style="width:300px;border-radius:24px;margin-top:40px"><span class="btn" style="margin-top:28px">con.seg.br/app</span>',
             '<span><b>CONSEG Cidadão</b> · APEP Brasil</span><span class="sw">Iniciativa da sociedade civil</span>', story=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for i, html in enumerate(SLIDES, 1):
            f = D / f"slide{i}.html"; f.write_text(html, encoding="utf-8")
            pg = await b.new_page(viewport={"width": 1080, "height": 1350}); await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(D / f"slide{i}.jpg"), type="jpeg", quality=92); await pg.close()
        f = D / "story.html"; f.write_text(STORY, encoding="utf-8")
        pg = await b.new_page(viewport={"width": 1080, "height": 1920}); await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(D / "story.jpg"), type="jpeg", quality=92)
        await b.close()

asyncio.run(main())
