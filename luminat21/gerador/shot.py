import asyncio,sys,glob
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for f in sorted(glob.glob('luminat21-*.html')):
            pg=await b.new_page(viewport={'width':1600,'height':900},device_scale_factor=2)
            await pg.goto('file:///home/claude/lumina-brand/'+f); await pg.wait_for_timeout(500)
            transp=not f.startswith('luminat21-logo-escuro')
            el=await pg.query_selector('#alvo') if transp else await pg.query_selector('body')
            if not transp:
                bb=await (await pg.query_selector('#alvo')).bounding_box()
                await pg.screenshot(path='out/'+f[:-5]+'.png',clip={'x':0,'y':0,'width':bb['x']+bb['width']+40,'height':bb['y']+bb['height']+40})
            else:
                await el.screenshot(path='out/'+f[:-5]+'.png',omit_background=True)
        await b.close()
asyncio.run(m())
