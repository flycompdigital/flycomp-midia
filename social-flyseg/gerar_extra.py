import asyncio, pathlib, re
from playwright.async_api import async_playwright
B=pathlib.Path("/home/claude/flyseg-posts"); LOGO="file://"+str(B/"logo.png")
CSS_BASE="""*{margin:0;padding:0;box-sizing:border-box}body{background:radial-gradient(120% 80% at 80% 0%,#3a1214 0%,#11161b 55%,#0b0f13 100%);color:#fff;font-family:Inter;position:relative;overflow:hidden}
.bar{position:absolute;top:0;left:0;right:0;height:10px;background:linear-gradient(90deg,#e31c24,#8b1e22)}
.w{position:absolute;display:flex;flex-direction:column}.w>*{flex-shrink:0}
.logo{width:250px;margin-bottom:44px}.eb{font-weight:700;letter-spacing:4px;text-transform:uppercase;color:#e9c260;margin-bottom:26px}
h1{font-family:'Inter Display';font-weight:800;letter-spacing:-1.2px;line-height:1.05;margin-bottom:30px}h1 span{color:#e9c260}
.s{color:#c5ccd3;line-height:1.4;margin-bottom:38px}
ol{list-style:none;display:flex;flex-direction:column}
li{display:flex;align-items:flex-start;color:#dfe4e9;line-height:1.32}
li b{border-radius:50%;background:linear-gradient(135deg,#e31c24,#8b1e22);display:flex;align-items:center;justify-content:center;color:#fff;font-family:'Inter Display';flex-shrink:0}
.ft{position:absolute;display:flex;justify-content:space-between;align-items:center;color:#7f8a94;border-top:2px solid rgba(255,255,255,.08)}.ft b{color:#fff}.ft .g{color:#e9c260;font-weight:700}"""
FEED=CSS_BASE+"""body{width:1080px;height:1350px}.w{left:90px;right:90px;top:90px;bottom:170px;justify-content:center}.eb{font-size:28px}h1{font-size:78px}.s{font-size:38px}
ol{gap:28px}li{gap:26px;font-size:38px}li b{width:64px;height:64px;font-size:32px}.ft{left:90px;right:90px;bottom:60px;padding-top:24px;font-size:28px}"""
STORY=CSS_BASE+"""body{width:1080px;height:1920px}.w{left:90px;right:90px;top:250px;bottom:370px;justify-content:center}.logo{width:300px}.eb{font-size:32px}h1{font-size:96px}.s{font-size:44px}
ol{gap:34px}li{gap:28px;font-size:44px}li b{width:76px;height:76px;font-size:38px}.cta{margin-top:56px;align-self:flex-start;padding:28px 46px;border-radius:20px;background:linear-gradient(90deg,#e31c24,#8b1e22);font-size:42px;font-weight:700}"""
POSTS={
"seguranca-colaborativa":("Programa Vizinhança Segura","Um cinturão digital <span>contra o crime.</span>","Segurança colaborativa com o MWL.camera.",["As câmeras que você já tem entram na rede","Veja as câmeras compartilhadas pelos vizinhos num raio de 500 m","Instalação e integração pela FlySeg"]),
"odl-camera":("ODL.camera","A segurança da rua <span>num conjunto completo.</span>","Totem com visão 360° e versão fachada, criados pela FlySeg.",["Sirene e giroflex integrados","Câmeras Full HD coloridas à noite e 7 dias de gravação","Integrado ao MWL.camera"]),
"vision-soc-integradores":("Para integradores","Monitoramento 24h <span>com a sua marca.</span>","Vision SOC white label, sem montar central.",["Você vende e atende o seu cliente","A central acompanha as ocorrências do MWL.camera 24h","Planos e preços em flyseg.vision"]),
}
def body(eb,t,s,itens,css,story):
    li="".join(f"<li><b>{i}</b><span>{x}</span></li>" for i,x in enumerate(itens,1))
    extra='<div class="cta">Fale com a gente pelo direct</div>' if story else ''
    ft='' if story else '<div class="ft"><span><b>FlySeg Vision</b> · Segurança colaborativa</span><span class="g">flyseg.vision</span></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bar"></div><div class="w"><img class="logo" src="{LOGO}"><div class="eb">{eb}</div><h1>{t}</h1><p class="s">{s}</p><ol>{li}</ol>{extra}</div>{ft}</body></html>'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for nome,(eb,t,s,itens) in POSTS.items():
            for kind,css,vp,story in [("resumo",FEED,(1080,1350),False),("story",STORY,(1080,1920),True)]:
                pg=await b.new_page(viewport={"width":vp[0],"height":vp[1]})
                f=B/nome/f"{kind}.html"; f.write_text(body(eb,t,s,itens,css,story),encoding="utf-8")
                await pg.goto("file://"+str(f)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(120)
                await pg.screenshot(path=str(B/nome/f"{kind}.jpg"),type="jpeg",quality=92); await pg.close()
        await b.close()
asyncio.run(main())
