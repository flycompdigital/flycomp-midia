"""Gera o lote semanal de 24 a 27/11/2026: carrossel, resumo, story, telas do Reels, capa do Reels.
Uso: python3 social/gerar_posts_2026-11-24.py  (depois: PDF e MP4 com o script de montagem)"""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = "../../brand/flycomp-logo.png"  # relativo à pasta do post

ICONS = {
 "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
 "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>',
 "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
}
def svg(k, s=100, c="#FFFFFF"):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

POSTS = [
 dict(slug="2026-11-24-golpes-black-friday", icon="cart", kicker="BLACK FRIDAY",
  titulo="Na Black Friday, o golpe também <span>usa a sua marca.</span>",
  sub="Sites e perfis falsos copiam lojas conhecidas para enganar clientes e funcionários.",
  fatos=["Pesquisa da Check Point mostrou que os ataques contra varejo e serviços subiram <b>28%</b> antes da Black Friday.",
         "Mais de <b>4 mil sites novos</b> com tema de novembro foram registrados. Quase 1 em cada 5 já era considerado arriscado.",
         "No Brasil, uma falsa promoção usou o nome de uma grande loja para coletar dados das pessoas."],
  fonte="Check Point Research",
  riscos=["O cliente enganado culpa a sua marca, não o golpista.",
          "Sua equipe recebe os mesmos links falsos no e-mail e no WhatsApp.",
          "Com mais vendas e mais pressa, um clique errado passa despercebido."],
  passos=["Divulgue seus canais oficiais e avise que não pede pagamento por link avulso.",
          "Acompanhe perfis e sites que imitam a sua marca e peça a remoção.",
          "Treine a equipe a conferir o endereço do site antes de clicar.",
          "Ative a verificação em duas etapas no e-mail e nos sistemas."],
  passos_curtos=["Divulgue seus canais oficiais", "Vigie perfis e sites que imitam sua marca",
                 "Treine a equipe a conferir links", "Ative a verificação em duas etapas"],
  story_t="Golpe de Black Friday <span>usa a sua marca</span>",
  story_p="Proteja seus clientes e sua equipe dos sites e perfis falsos.",
  story_li=["Divulgue os canais oficiais", "Vigie quem imita a sua marca", "Treine a equipe para conferir links"]),
 dict(slug="2026-11-25-senha-valida", icon="key", kicker="ACESSO INDEVIDO",
  titulo="Nem toda invasão <span>arromba a porta.</span>",
  sub="Às vezes, o criminoso entra com uma senha verdadeira, e ninguém percebe.",
  fatos=["Um grande banco brasileiro informou que terceiros usaram uma <b>credencial válida</b> para acessar dados cadastrais de clientes.",
         "Entre os dados estavam nome, CPF e e-mail. O banco cancelou o acesso e disse que senhas e códigos não foram expostos.",
         "E orientou os clientes a desconfiar de mensagens e ligações suspeitas."],
  fonte="Olhar Digital",
  riscos=["Login com senha certa não dispara o alarme comum.",
          "Acessos de fornecedores e ex-funcionários costumam ficar esquecidos.",
          "Dados de clientes viram isca para golpes em nome da sua empresa."],
  passos=["Ative a verificação em duas etapas em todos os acessos.",
          "Revise quem tem acesso e remova o que não é mais usado.",
          "Dê a cada pessoa só o acesso que ela precisa.",
          "Fique de olho em login fora do horário ou de lugar estranho."],
  passos_curtos=["Ative a verificação em duas etapas", "Remova acessos que não são mais usados",
                 "Cada pessoa só com o acesso necessário", "Vigie logins em horário estranho"],
  story_t="A senha certa <span>na mão errada</span>",
  story_p="Quando o criminoso entra com uma senha verdadeira, o alarme comum não toca.",
  story_li=["Verificação em duas etapas", "Revise e remova acessos antigos", "Vigie logins fora do padrão"]),
 dict(slug="2026-11-26-ransomware-logistica", icon="lock", kicker="RANSOMWARE",
  titulo="Quando o parceiro para, <span>sua empresa sente.</span>",
  sub="Ataques a portos mostram como o sequestro de dados afeta toda a cadeia.",
  fatos=["Desde o início de novembro, um ataque de <b>ransomware</b> atingiu operações no Porto de Santos, com pedido de resgate.",
         "Segundo a reportagem, os dados podem ser recuperados por <b>backup</b>.",
         "Em outubro, o Brasil teve 32 empresas citadas por grupos de ransomware: <b>4º lugar no mundo</b>."],
  fonte="TV Sim Brasil e ANTI/HYPE",
  riscos=["O ransomware trava os sistemas e cobra para liberar.",
          "Se um parceiro para, entregas, notas e pagamentos atrasam.",
          "Quem tem backup protegido e plano pronto volta mais rápido."],
  passos=["Tenha backup separado da rede e teste a restauração.",
          "Escreva um plano: quem faz o quê se tudo parar.",
          "Pergunte aos fornecedores como eles se protegem.",
          "Mantenha os sistemas atualizados e treine a equipe."],
  passos_curtos=["Backup separado da rede e testado", "Plano: quem faz o quê se tudo parar",
                 "Cobre proteção dos fornecedores", "Sistemas atualizados e equipe treinada"],
  story_t="Ransomware <span>para a cadeia toda</span>",
  story_p="Se um parceiro para, entregas e pagamentos da sua empresa atrasam.",
  story_li=["Backup separado e testado", "Plano para quando tudo parar", "Fornecedores também protegidos"]),
]

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{width:{W}px;height:{H}px;background:linear-gradient(180deg,#EBF5FF 0%,#FFFFFF 60%);font-family:Inter,sans-serif;color:#111827;position:relative;overflow:hidden}
h1,h2{font-family:'Inter Display',Inter,sans-serif;font-weight:800;letter-spacing:-1.5px;color:#111827}
h1 span,h2 span{color:#0B66FF}
.k{font-size:26px;font-weight:600;letter-spacing:4px;color:#0B66FF}
.logo{width:211px;height:120px;object-fit:contain;object-position:left}
.ic{width:150px;height:150px;border-radius:40px;background:linear-gradient(160deg,#0B66FF,#0A4A9E);display:flex;align-items:center;justify-content:center}
.lead{font-size:40px;line-height:1.38;color:#4B5563}
.fato{font-size:40px;line-height:1.38;color:#4B5563;padding-left:28px;border-left:6px solid #2BA3FF}
.fato b,.lead b{color:#111827}
.src{font-size:26px;color:#6B7280}
.card{background:#fff;border:2px solid #E5E7EB;border-left:10px solid #0B66FF;border-radius:22px;padding:28px 34px;font-size:40px;line-height:1.32;color:#111827}
.step{display:flex;gap:28px;align-items:flex-start;font-size:40px;line-height:1.32;color:#111827}
.n{flex:0 0 68px;height:68px;border-radius:20px;background:#0B66FF;color:#fff;font-weight:700;font-size:34px;display:flex;align-items:center;justify-content:center}
.fly{background:#0A4A9E;color:#fff;border-radius:26px;padding:30px 34px}
.fly h3{font-family:'Inter Display';font-weight:800;font-size:38px;margin-bottom:6px}
.fly p{font-size:30px;line-height:1.35;color:#DCEBFF}
.cta{background:#fff;border:3px solid #0B66FF;border-radius:24px;padding:24px 32px;font-size:34px;font-weight:700;color:#0A4A9E}
.foot{position:absolute;left:96px;right:96px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#6B7280;border-top:1px solid #E5E7EB;padding-top:28px}
.foot strong{color:#0A4A9E}
"""

def page(W, H, body):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS.replace("{W}",str(W)).replace("{H}",str(H))}</style></head><body>{body}</body></html>'

def foot(i, n, arraste=False):
    right = '<span style="color:#111827;font-weight:600">Arraste →</span>' if arraste else ''
    return f'<div class="foot"><span><strong>FlyComp Digital</strong> · {i}/{n}</span>{right}</div>'

def telas(p):
    """Conteúdo das 5 telas, sem moldura (usado no carrossel e no Reels)."""
    t1 = f'''<img class="logo" src="{LOGO}"><div style="height:40px"></div><div class="ic">{svg(p["icon"])}</div><div style="height:48px"></div>
<div class="k">{p["kicker"]}</div><div style="height:28px"></div>
<h1 style="font-size:92px;line-height:1.04">{p["titulo"]}</h1><div style="height:40px"></div><p class="lead">{p["sub"]}</p>'''
    t2 = '<div class="k">O QUE ACONTECEU</div><div style="height:28px"></div><h2 style="font-size:72px;line-height:1.06">Nesta semana, <span>no noticiário</span></h2><div style="height:52px"></div>' + \
         '<div style="display:flex;flex-direction:column;gap:36px">' + "".join(f'<p class="fato">{f}</p>' for f in p["fatos"]) + \
         f'</div><div style="height:40px"></div><p class="src">Fonte: {p["fonte"]}</p>'
    t3 = '<div class="k">O RISCO</div><div style="height:28px"></div><h2 style="font-size:72px;line-height:1.06">O que isso tem a ver <span>com a sua empresa</span></h2><div style="height:52px"></div>' + \
         '<div style="display:flex;flex-direction:column;gap:24px">' + "".join(f'<div class="card">{r}</div>' for r in p["riscos"]) + '</div>'
    t4 = '<div class="k">O QUE FAZER</div><div style="height:28px"></div><h2 style="font-size:72px;line-height:1.06">4 passos <span>para começar</span></h2><div style="height:52px"></div>' + \
         '<div style="display:flex;flex-direction:column;gap:34px">' + "".join(f'<div class="step"><div class="n">{i}</div><div>{s}</div></div>' for i, s in enumerate(p["passos"], 1)) + '</div>'
    t5 = f'''<img class="logo" src="{LOGO}"><div style="height:28px"></div><h2 style="font-size:72px;line-height:1.06">Como a FlyComp <span>ajuda</span></h2><div style="height:36px"></div>
<div style="display:flex;flex-direction:column;gap:22px">
<div class="fly"><h3>Vision XDR by Vigilant</h3><p>Monitoramento e resposta 24h em todas as máquinas. Analisa o comportamento, não só vírus conhecidos, e integra com o que você já tem.</p></div>
<div class="fly"><h3>Vision MDR</h3><p>Analista da FlyComp que responde e corrige o incidente. Inclui diagnóstico e teste de invasão com a Thallium Security.</p></div>
<p style="font-size:27px;line-height:1.4;color:#4B5563">Time com atuação no Muralha Paulista (SSP-SP), no Disque Denúncia 181 e na segurança da PMESP.</p>
<div class="cta">Teste grátis do Vision XDR. Fale com a gente pelo direct.</div></div>'''
    return [t1, t2, t3, t4, t5]

def carrossel(p):
    out = []
    for i, c in enumerate(telas(p), 1):
        out.append(page(1080, 1350, f'<div style="position:absolute;left:96px;right:96px;top:88px;bottom:150px;display:flex;flex-direction:column;justify-content:center"><div>{c}</div></div>{foot(i, 5, arraste=(i == 1))}'))
    return out

def reel(p):
    # área segura: 250 px em cima, 350 px embaixo; tela centralizada nessa faixa
    return [page(1080, 1920, f'<div style="position:absolute;left:96px;right:96px;top:250px;bottom:350px;display:flex;flex-direction:column;justify-content:center"><div>{c}</div></div>') for c in telas(p)]

def resumo(p):
    passos = "".join(f'<div class="step" style="font-size:38px"><div class="n" style="flex-basis:66px;height:66px;font-size:32px">{i}</div><div style="padding-top:8px">{s}</div></div>' for i, s in enumerate(p["passos_curtos"], 1))
    body = f'''<div style="position:absolute;left:80px;right:80px;top:64px;bottom:56px;display:flex;flex-direction:column">
<div style="display:flex;justify-content:space-between;align-items:center"><img class="logo" style="width:190px;height:100px" src="{LOGO}"><div class="k" style="font-size:24px">{p["kicker"]}</div></div>
<div style="height:24px"></div><h1 style="font-size:70px;line-height:1.05">{p["titulo"]}</h1>
<div style="height:48px"></div><div class="k" style="font-size:24px">O QUE FAZER</div><div style="height:20px"></div>
<div style="display:flex;flex-direction:column;gap:30px">{passos}</div>
<div style="margin-top:auto" class="fly"><div style="font-size:24px;letter-spacing:3px;font-weight:600;color:#9CC8FF;margin-bottom:14px">COMO A FLYCOMP AJUDA</div>
<h3 style="font-size:36px">Vision XDR by Vigilant</h3><p style="margin-bottom:14px">Monitoramento e resposta 24h em todas as máquinas</p>
<h3 style="font-size:36px">Vision MDR</h3><p>Analista que responde e corrige o incidente</p></div>
<div style="height:18px"></div><div style="display:flex;justify-content:space-between;align-items:center;font-size:30px"><b style="color:#0A4A9E">Peça o teste grátis do Vision XDR</b><span style="font-size:22px;color:#6B7280">Fonte: {p["fonte"]}</span></div></div>'''
    return page(1080, 1350, body)

def story(p):
    lis = "".join(f'<li>{x}</li>' for x in p["story_li"])
    body = f'''<style>.w{{position:absolute;left:90px;right:90px;top:250px;bottom:370px;display:flex;flex-direction:column}}.w>*{{flex-shrink:0}}
.w .logo{{width:240px;height:auto;margin-bottom:56px}}.w .ic{{width:170px;height:170px;border-radius:44px;margin-bottom:44px}}
.w h1{{font-size:88px;line-height:1.04;margin-bottom:36px}}.w p{{font-size:42px;line-height:1.4;color:#4B5563;margin-bottom:44px}}
ul{{list-style:none;display:flex;flex-direction:column;gap:24px}}li{{font-size:40px;line-height:1.3;padding:26px 32px;background:#fff;border:2px solid #E5E7EB;border-left:10px solid #0B66FF;border-radius:22px;color:#111827}}
.sc{{margin-top:auto;font-size:40px;font-weight:700;color:#0A4A9E}}</style>
<div class="w"><img class="logo" src="{LOGO}"><div class="ic">{svg(p["icon"])}</div><h1>{p["story_t"]}</h1><p>{p["story_p"]}</p><ul>{lis}</ul><div class="sc">Fale com a gente pelo direct</div></div>'''
    return page(1080, 1920, body)

async def shot(pg, html_path, out, w, h):
    await pg.set_viewport_size({"width": w, "height": h})
    await pg.goto("file://" + str(html_path)); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(150)
    await pg.screenshot(path=str(out), type="jpeg", quality=92, clip={"x": 0, "y": 0, "width": w, "height": h})

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = await b.new_page()
        for p in POSTS:
            d = ROOT / "social" / p["slug"]; (d / "html").mkdir(parents=True, exist_ok=True); (d / "reel-telas").mkdir(exist_ok=True)
            jobs = []
            for i, h in enumerate(carrossel(p), 1): jobs.append((f"html/slide{i}.html", h, f"slide{i}.jpg", 1080, 1350))
            for i, h in enumerate(reel(p), 1): jobs.append((f"html/reel{i}.html", h, f"reel-telas/reel{i}.jpg", 1080, 1920))
            jobs.append(("html/resumo.html", resumo(p), "resumo.jpg", 1080, 1350))
            jobs.append(("html/story.html", story(p), "story.jpg", 1080, 1920))
            for hp, h, out, w, hh in jobs:
                f = d / hp; f.write_text(h.replace('src="../../brand', 'src="../../../brand'), encoding="utf-8")
                await shot(pg, f, d / out, w, hh)
        await b.close()

asyncio.run(main())
