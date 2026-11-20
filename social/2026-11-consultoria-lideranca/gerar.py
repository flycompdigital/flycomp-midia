import asyncio, pathlib
from playwright.async_api import async_playwright
B=pathlib.Path(__file__).parent
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:%dpx;font-family:Inter,sans-serif;color:#111827;background:linear-gradient(180deg,#EBF5FF 0%%,#FFFFFF 70%%);position:relative;overflow:hidden}
.w{position:absolute;inset:%s;display:flex;flex-direction:column}.ct{flex:1;display:flex;flex-direction:column;justify-content:center}
.logo{height:76px;align-self:flex-start}.eb{align-self:flex-start;font-size:22px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#0B66FF;background:#fff;border:2px solid #cfe0ff;padding:10px 20px;border-radius:999px;margin-bottom:34px}
h1{font-family:'Inter Display';font-size:96px;line-height:1.04;font-weight:800;letter-spacing:-2px}h1 span,h2 span{color:#0B66FF}
h2{font-family:'Inter Display';font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-1px}
p.t{font-size:38px;line-height:1.45;color:#4B5563;margin-top:30px}
.cards{display:grid;gap:22px;margin-top:44px}.c{background:#fff;border:2px solid #E5E7EB;border-left:10px solid #0B66FF;border-radius:26px;padding:32px 36px}.c b{font-size:40px;display:block}.c span{font-size:31px;color:#4B5563;line-height:1.4;display:block;margin-top:6px}
.cta{margin-top:50px;background:linear-gradient(135deg,#0B66FF,#0A4A9E);color:#fff;border-radius:28px;padding:40px 44px}.cta b{font-size:46px;display:block}.cta span{font-size:30px;display:block;margin-top:10px;opacity:.9}
.pg{position:absolute;right:84px;bottom:56px;font-size:24px;color:#9CA3AF;font-weight:700}.ar{position:absolute;left:84px;bottom:56px;font-size:24px;color:#0B66FF;font-weight:700}.ft{position:absolute;left:84px;bottom:56px;font-size:24px;color:#9CA3AF;font-weight:700}
"""
def page(inner,n=None,tot=None,story=False):
    h=1920 if story else 1350; ins='260px 84px 380px' if story else '80px 84px 130px'
    ex=''
    if n: ex+=f'<div class="pg">{n}/{tot}</div>'+('<div class="ar">Arraste →</div>' if n==1 else '<div class="ft">FlyComp Digital</div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS%(h,ins)}</style></head><body><div class="w"><img class="logo" src="logo.png"><div class="ct">{inner}</div></div>{ex}</body></html>'
S=[
'<div class="eb">Consultoria</div><h1>O seu projeto travou? <span>Nem sempre o problema é técnico.</span></h1><p class="t">Muitas vezes o entrave está na forma como a equipe trabalha.</p>',
'<h2>IA nas tarefas <span>repetitivas</span></h2><p class="t">O que é manual e repetitivo passa para a inteligência artificial.</p><div class="cards"><div class="c"><b>As pessoas ficam com as funções mais nobres</b><span>Pensar, decidir e entregar o que gera valor.</span></div></div>',
'<h2>Soft skills que <span>destravam hard skills</span></h2><p class="t">Trabalhamos as soft skills da equipe para ela aceitar aprender o que falta e entregar o que precisa ser feito.</p>',
'<h2>Um agente de <span>transformação</span></h2><p class="t">Tiramos a equipe da zona de conforto e conduzimos a mudança até o projeto sair do papel.</p><div class="cta"><b>Consultoria em Liderança de Equipes de Projetos</b><span>Fale com a gente pelo direct.</span></div>',
]
R='<div class="eb">Consultoria</div><h2>Liderança de Equipes <span>de Projetos</span></h2><p class="t">Para empresas que não conseguem tirar os projetos do papel por entraves técnicos ou de pessoas.</p><div class="cards"><div class="c"><b>IA nas tarefas repetitivas</b></div><div class="c"><b>Soft skills que destravam hard skills</b></div><div class="c"><b>Um agente de transformação</b></div></div>'
ST='<div class="eb">Consultoria</div><h1 style="font-size:84px">O seu projeto travou? <span>Nem sempre o problema é técnico.</span></h1><div class="cards"><div class="c"><b>IA nas tarefas repetitivas</b></div><div class="c"><b>Pessoas nas funções mais nobres</b></div></div><div class="cta"><b>Fale com a gente pelo direct</b></div>'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        jobs=[(f'slide{i+1}',page(s,i+1,len(S)),1350) for i,s in enumerate(S)]+[('resumo',page(R),1350),('story',page(ST,story=True),1920)]
        for n,html,h in jobs:
            f=B/f'{n}.html'; f.write_text(html); pg=await b.new_page(viewport={'width':1080,'height':h})
            await pg.goto('file://'+str(f)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(B/f'{n}.jpg'),type='jpeg',quality=90); await pg.close()
        await b.close()
asyncio.run(main())
