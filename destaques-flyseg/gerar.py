import asyncio, pathlib
from playwright.async_api import async_playwright
B=pathlib.Path(__file__).resolve().parent; LOGO="file://"+str(B.parent/"brand"/"flyseg-logo.png")
I={
"users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
"cctv":'<path d="M16.75 12h3.632a1 1 0 0 1 .894 1.447l-2.034 4.069a1 1 0 0 1-1.708.134l-2.124-2.97"/><path d="M17.106 9.053a1 1 0 0 1 .447 1.341l-3.106 6.211a1 1 0 0 1-1.342.447L3.61 12.3a2.92 2.92 0 0 1-1.3-3.91L3.69 5.6a2.92 2.92 0 0 1 3.92-1.3z"/><path d="M2 19h3.76a2 2 0 0 0 1.8-1.1L9 15"/><path d="M2 21v-4"/><path d="M7 9h.01"/>',
"monitor":'<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/><path d="m7 10 2 2 4-4 4 4"/>',
"handshake":'<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
"shield":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
"chat":'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}
def svg(k,size,color): return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{I[k]}</svg>'
D=[
("vizinhanca-segura","users","Programa <span>Vizinhança Segura</span>","Um cinturão digital contra o crime, rua por rua.",["As câmeras que você já tem entram no MWL.camera","Veja as câmeras dos vizinhos num raio de 500 m","Painel para as forças de segurança locais"]),
("odl-camera","cctv","ODL<span>.camera</span>","A segurança da rua num conjunto completo, criado pela FlySeg.",["Totem com visão 360° e versão fachada","Sirene, giroflex e botão de emergência","Ocorrências no painel das forças de segurança"]),
("sobre","shield","Sobre a <span>FlySeg</span>","Segurança colaborativa de verdade.",["Pioneira na integração com o MWL.camera","Criadora do ODL.camera","Venda, instalação e locação"]),
("contato","chat","Fale com <span>a gente</span>","Atendimento comercial da FlySeg Vision.",["Direct aqui do Instagram","WhatsApp (11) 4283-7330","flyseg.vision"]),
]
CAPA="""<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0}body{width:1080px;height:1920px;background:radial-gradient(70% 45% at 50% 50%,#3a1214 0%,#11161b 70%);display:flex;align-items:center;justify-content:center}
.c{width:640px;height:640px;border-radius:50%;background:linear-gradient(145deg,#e31c24,#8b1e22);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 14px rgba(233,194,96,.55)}</style></head><body><div class="c">{ICON}</div></body></html>"""
STORY="""<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;background:radial-gradient(120% 70% at 80% 0%,#3a1214 0%,#11161b 55%,#0b0f13 100%);font-family:Inter;color:#fff;position:relative}
.bar{position:absolute;top:0;left:0;right:0;height:12px;background:linear-gradient(90deg,#e31c24,#8b1e22)}
.w{position:absolute;left:90px;right:90px;top:250px;bottom:370px;display:flex;flex-direction:column}.w>*{flex-shrink:0}
.logo{width:300px;margin-bottom:56px}
.ic{width:170px;height:170px;border-radius:44px;background:linear-gradient(145deg,#e31c24,#8b1e22);display:flex;align-items:center;justify-content:center;margin-bottom:44px}
h1{font-family:'Inter Display';font-weight:800;font-size:92px;line-height:1.04;letter-spacing:-1.5px;margin-bottom:32px}h1 span{color:#e9c260}
p{font-size:44px;line-height:1.4;color:#c5ccd3;margin-bottom:44px}
ul{list-style:none;display:flex;flex-direction:column;gap:24px}
li{font-size:40px;line-height:1.3;padding:26px 32px;background:rgba(233,194,96,.07);border:2px solid rgba(233,194,96,.35);border-left:10px solid #e31c24;border-radius:22px;color:#eef1f4}
.cta{margin-top:auto;padding-top:40px;font-size:40px;font-weight:700;color:#e9c260}
</style></head><body><div class="bar"></div><div class="w"><img class="logo" src="{LOGO}"><div class="ic">{ICON}</div><h1>{T}</h1><p>{P}</p><ul>{LI}</ul><div class="cta">{CTA}</div></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=await b.new_page(viewport={"width":1080,"height":1920})
        for slug,ic,t,txt,itens in D:
            for kind,h in [("capa",CAPA.replace("{ICON}",svg(ic,380,"#e9c260"))),
                           ("story",STORY.replace("{LOGO}",LOGO).replace("{ICON}",svg(ic,100,"#FFFFFF")).replace("{T}",t).replace("{P}",txt).replace("{LI}","".join(f"<li>{x}</li>" for x in itens)).replace("{CTA}","Fale com a gente pelo direct" if slug!="contato" else ""))]:
                f=B/f"{kind}-{slug}.html"; f.write_text(h,encoding="utf-8")
                await pg.goto("file://"+str(f)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(120)
                await pg.screenshot(path=str(B/f"{kind}-{slug}.jpg"),type="jpeg",quality=92)
        await b.close()
asyncio.run(main())
