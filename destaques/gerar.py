import asyncio, pathlib
from playwright.async_api import async_playwright
B=pathlib.Path(__file__).resolve().parent; LOGO="file://"+str(B.parent/"brand"/"flycomp-logo.png")
I={
"shield":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
"search":'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/><path d="M11 8v6"/><path d="M8 11h6"/>',
"gift":'<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C9.5 3 11 5 12 8c1-3 2.5-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
"code":'<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><path d="m14.5 4-5 16"/>',
"award":'<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
"chat":'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}
def svg(k,size,color): return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{I[k]}</svg>'
D=[
("vision-xdr","shield","Vision XDR","Vision XDR <span>by Vigilant</span>","Monitoramento e resposta <b>24h</b> em todos os computadores e servidores.",["Analisa o comportamento, não só vírus conhecidos","Isola a ameaça sozinho, inclusive de madrugada","Funciona junto com o antivírus que você já tem"]),
("vision-mdr","search","Vision MDR","Vision MDR","Consultoria de cibersegurança da FlyComp: <b>onde você está exposto e o que fazer primeiro.</b>",["Diagnóstico e plano de ação","Teste de invasão com a Thallium Security","Acompanhamento mensal da evolução","Avaliação grátis em mdr.vision/avaliacao"]),
("teste-gratis","gift","Teste grátis","Teste o Vision XDR <span>grátis</span>","Veja na prática o que acontece nos computadores da sua empresa.",["Sem trocar o que você já usa","Em nuvem, sem comprar servidor","Com acompanhamento do nosso time"]),
("software","code","Software","Software <span>sob medida</span>","Da ideia à operação, com segurança desde o projeto.",["Sistemas e plataformas digitais","Integrações entre sistemas","Agentes de IA para atendimento e vendas"]),
("time","award","Time","Nosso <span>time</span>","FlyCompers: profissionais certificados com projetos na segurança pública de SP.",["Muralha Paulista (SSP-SP)","Disque Denúncia 181 (CICC)","Cibersegurança da PMESP"]),
("contato","chat","Contato","Fale com <span>a gente</span>","Atendimento comercial da FlyComp Digital.",["Direct aqui do Instagram","WhatsApp (11) 4283-7330","flycomp.digital"]),
]
CAPA="""<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0}body{width:1080px;height:1920px;background:linear-gradient(160deg,#0B66FF 0%,#0A4A9E 100%);display:flex;align-items:center;justify-content:center}
.c{width:640px;height:640px;border-radius:50%;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center}</style></head><body><div class="c">{ICON}</div></body></html>"""
STORY="""<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;background:linear-gradient(180deg,#EBF5FF 0%,#FFFFFF 60%);font-family:Inter;color:#111827;position:relative}
.w{position:absolute;left:90px;right:90px;top:250px;bottom:370px;display:flex;flex-direction:column}.w>*{flex-shrink:0}
.logo{width:240px;margin-bottom:56px}
.ic{width:170px;height:170px;border-radius:44px;background:linear-gradient(160deg,#0B66FF,#0A4A9E);display:flex;align-items:center;justify-content:center;margin-bottom:44px}
h1{font-family:'Inter Display';font-weight:800;font-size:88px;line-height:1.04;letter-spacing:-1.5px;margin-bottom:36px}h1 span{color:#0B66FF}
p{font-size:42px;line-height:1.4;color:#4B5563;margin-bottom:44px}p b{color:#111827}
ul{list-style:none;display:flex;flex-direction:column;gap:24px}
li{font-size:40px;line-height:1.3;padding:26px 32px;background:#fff;border:2px solid #E5E7EB;border-left:10px solid #0B66FF;border-radius:22px;color:#111827}
.cta{margin-top:auto;font-size:40px;font-weight:700;color:#0A4A9E}
</style></head><body><div class="w"><img class="logo" src="{LOGO}"><div class="ic">{ICON}</div><h1>{T}</h1><p>{P}</p><ul>{LI}</ul><div class="cta">{CTA}</div></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=await b.new_page(viewport={"width":1080,"height":1920})
        for slug,ic,nome,t,txt,itens in D:
            for kind,h in [("capa",CAPA.replace("{ICON}",svg(ic,380,"#FFFFFF"))),
                           ("story",STORY.replace("{LOGO}",LOGO).replace("{ICON}",svg(ic,100,"#FFFFFF")).replace("{T}",t).replace("{P}",txt).replace("{LI}","".join(f"<li>{x}</li>" for x in itens)).replace("{CTA}","Fale com a gente pelo direct" if slug!="contato" else ""))]:
                f=B/f"{kind}-{slug}.html"; f.write_text(h,encoding="utf-8")
                await pg.goto("file://"+str(f)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(120)
                await pg.screenshot(path=str(B/f"{kind}-{slug}.jpg"),type="jpeg",quality=92)
        await b.close()
asyncio.run(main())
