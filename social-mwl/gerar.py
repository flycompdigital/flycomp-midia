import asyncio, os, pathlib
from playwright.async_api import async_playwright
BASE = pathlib.Path(__file__).parent
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;font-family:Inter,sans-serif;color:#f8fafc;background:radial-gradient(110% 70% at 85% 0%,#1e3a8a 0%,#0b1120 62%);position:relative;overflow:hidden}
.w{position:absolute;inset:80px 84px 120px;display:flex;flex-direction:column}.ct{flex:1;display:flex;flex-direction:column;justify-content:center}.ct>*:first-child{margin-top:0!important}.ct .eb{align-self:flex-start}.marca{display:flex;align-items:center;gap:18px}.marca img{width:84px;filter:drop-shadow(0 0 18px rgba(59,130,246,.6))}.marca b{font-size:38px;font-weight:800}.marca small{display:block;font-size:17px;letter-spacing:3px;color:#94a3b8;font-weight:700;text-transform:uppercase}
.eb{display:inline-block;margin-top:70px;font-size:22px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#c4b5fd;background:rgba(139,92,246,.15);border:2px solid rgba(139,92,246,.4);padding:10px 20px;border-radius:999px}
h1{font-family:'Inter Display';font-size:100px;line-height:1.04;font-weight:800;letter-spacing:-2px;margin-top:34px}h1 span{color:#8fb4ff}
h2{font-family:'Inter Display';font-size:78px;line-height:1.08;font-weight:800;letter-spacing:-1px;margin-top:60px}h2 span{color:#8fb4ff}
p.t{font-size:38px;line-height:1.45;color:#cbd5e1;margin-top:34px}
.cards{display:grid;gap:22px;margin-top:46px}.c{background:#16213a;border:2px solid #24314f;border-radius:28px;padding:34px 36px;border-left:10px solid var(--c,#60a5fa)}.c b{font-size:40px;display:block}.c span{font-size:31px;color:#94a3b8;line-height:1.4;display:block;margin-top:6px}
.pg{position:absolute;right:84px;bottom:56px;font-size:24px;color:#64748b;font-weight:700}.ar{position:absolute;left:84px;bottom:56px;font-size:24px;color:#8fb4ff;font-weight:700}
.cta{margin-top:60px;background:linear-gradient(135deg,#7c3aed,#1d4ed8);border-radius:30px;padding:40px 44px}.cta b{font-size:46px;display:block}.cta span{font-size:30px;color:#e0e7ff;display:block;margin-top:12px;line-height:1.4}
.av{position:absolute;left:84px;right:84px;bottom:50px;font-size:20px;color:#64748b;line-height:1.4}
"""
MARCA = '<div class="marca"><img src="logo.png"><div><b>MWL.camera</b><small>Segurança privada colaborativa</small></div></div>'
def page(inner, n=None, tot=None, arraste=False, story=False):
    h = 1920 if story else 1350
    extra = f'<div class="pg">{n}/{tot}</div>' if n else ''
    extra += '<div class="ar">Arraste →</div>' if arraste else ''
    css = CSS.replace('height:1350px', f'height:{h}px')
    if story: css += '.w{inset:250px 84px 380px}'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="w">{MARCA}<div class="ct">{inner}</div></div>{extra}</body></html>'
POSTS = {
 '2026-11-mwl-integradores': {
  'slides': [
   '<div class="eb">Para integradores</div><h1>Sistema e hardware <span>white label</span> com a sua marca.</h1><p class="t">O MWL.camera é o sistema. O ODL.camera é o hardware. Os dois saem com a marca da sua empresa.</p>',
   '<h2>MWL.camera: <span>o sistema</span></h2><div class="cards"><div class="c"><b>Câmeras da rua no celular</b><span>Ao vivo e gravações, pela web e pelo celular.</span></div><div class="c"><b>Raio de 500 m</b><span>Vizinhos compartilham câmeras e a rede cresce sozinha.</span></div><div class="c"><b>Ocorrências e painel das forças</b><span>Com a gravação anexada, visível para as forças que aderirem.</span></div></div>',
   '<h2>ODL.camera: <span>o hardware</span></h2><div class="cards"><div class="c" style="--c:#a78bfa"><b>Totem 360° ou fachada</b><span>Câmeras Full HD que filmam colorido à noite.</span></div><div class="c" style="--c:#a78bfa"><b>Sirene, giroflex e botão de emergência</b><span>Integrados ao MWL.camera.</span></div><div class="c" style="--c:#a78bfa"><b>Locação mensal</b><span>Sem custo de equipamento para o seu cliente.</span></div></div>',
   '<h2>O ODL com a <span>sua marca</span></h2><p class="t">Sai com a marca ODL.camera ou com a sua. Para usar a sua, você envia:</p><div class="cards"><div class="c" style="--c:#34d399"><b>Kit de adesivos e cor do totem</b><span>A arte com o seu logo e a cor da sua marca.</span></div><div class="c" style="--c:#34d399"><b>WhatsApp e site</b><span>O seu atendimento e onde o cliente conhece o produto.</span></div></div>',
   '<h2>Seja um <span>integrador</span></h2><p class="t">Você fica com o cliente e com a receita da instalação, da locação e da manutenção. A FlyComp cuida da tecnologia.</p><div class="cta"><b>Fale com a gente pelo direct</b><span>Ou tire suas dúvidas com o agente Bip IA em mwl.camera.</span></div>',
  ],
  'resumo': '<div class="eb">Para integradores</div><h2 style="margin-top:40px">Sistema e hardware <span>white label</span> com a sua marca.</h2><div class="cards"><div class="c"><b>MWL.camera: o sistema</b><span>Câmeras da rua no celular, raio de 500 m e ocorrências.</span></div><div class="c" style="--c:#a78bfa"><b>ODL.camera: o hardware</b><span>Totem ou fachada com sirene, giroflex e botão de emergência.</span></div><div class="c" style="--c:#34d399"><b>Com a sua marca</b><span>Adesivos, cor do totem, seu WhatsApp e seu site.</span></div></div>',
  'story': '<div class="eb">Para integradores</div><h1 style="font-size:84px">Sistema e hardware <span>white label</span> com a sua marca.</h1><div class="cards"><div class="c"><b>MWL.camera: o sistema</b></div><div class="c" style="--c:#a78bfa"><b>ODL.camera: o hardware</b></div></div><div class="cta"><b>Fale com a gente pelo direct</b></div>',
 },
 '2026-11-mwl-sua-rua': {
  'slides': [
   '<div class="eb">Segurança colaborativa</div><h1>A sua rua vigiada <span>por quem mora nela.</span></h1><p class="t">Com o MWL.camera, vizinhos compartilham câmeras e acompanham a rua pelo celular.</p>',
   '<h2>Como <span>funciona</span></h2><div class="cards"><div class="c"><b>1. O integrador conecta</b><span>As câmeras que você já tem entram na plataforma.</span></div><div class="c"><b>2. Os vizinhos compartilham</b><span>Cada um vê as câmeras num raio de 500 m.</span></div><div class="c"><b>3. A rua acompanha junto</b><span>Ocorrências chegam com a gravação anexada.</span></div></div>',
   '<h2>E as forças de <span>segurança?</span></h2><p class="t">As polícias e a Guarda Civil da região que aderirem veem as ocorrências no painel delas, sem custo.</p><div class="cards"><div class="c" style="--c:#34d399"><b>Cada comando vê só a sua área</b><span>E todo acesso fica registrado.</span></div></div>',
   '<h2>Quer a sua rua <span>na rede?</span></h2><p class="t">Encontre um integrador certificado perto de você.</p><div class="cta"><b>Fale com a gente pelo direct</b><span>Ou acesse mwl.camera e clique em Buscar integrador.</span></div><p class="t" style="font-size:22px;color:#64748b;margin-top:40px">O MWL.camera é uma plataforma de tecnologia e não substitui o 190.</p>',
  ],
  'resumo': '<div class="eb">Segurança colaborativa</div><h2 style="margin-top:40px">A sua rua vigiada <span>por quem mora nela.</span></h2><div class="cards"><div class="c"><b>1. O integrador conecta as câmeras</b></div><div class="c"><b>2. Vizinhos compartilham num raio de 500 m</b></div><div class="c" style="--c:#34d399"><b>3. Ocorrências chegam com a gravação</b><span>E aparecem no painel das forças que aderirem.</span></div></div>',
  'story': '<div class="eb">Segurança colaborativa</div><h1 style="font-size:84px">A sua rua vigiada <span>por quem mora nela.</span></h1><div class="cards"><div class="c"><b>Câmeras num raio de 500 m</b></div><div class="c" style="--c:#34d399"><b>Painel das forças de segurança</b></div></div><div class="cta"><b>Fale com a gente pelo direct</b></div>',
 },
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for slug, d in POSTS.items():
            out = BASE / slug; out.mkdir(exist_ok=True)
            (out/'logo.png').write_bytes((BASE/'logo.png').read_bytes())
            jobs = [(f'slide{i+1}', page(s, i+1, len(d['slides']), i == 0), 1350) for i, s in enumerate(d['slides'])]
            jobs += [('resumo', page(d['resumo']), 1350), ('story', page(d['story'], story=True), 1920)]
            for name, html, h in jobs:
                f = out/f'{name}.html'; f.write_text(html)
                pg = await b.new_page(viewport={'width':1080,'height':h})
                await pg.goto('file://'+str(f)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
                await pg.screenshot(path=str(out/f'{name}.jpg'), type='jpeg', quality=90); await pg.close()
        await b.close()
asyncio.run(main())
