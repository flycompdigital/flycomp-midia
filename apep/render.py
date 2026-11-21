import sys,asyncio
from playwright.async_api import async_playwright
async def main(jobs):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for html,png,w,h,scale,transp,pdf in jobs:
            pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=scale)
            await pg.goto('file://'+html); await pg.wait_for_timeout(300)
            await pg.screenshot(path=png,omit_background=transp)
            if pdf: await pg.pdf(path=pdf,width=f'{w}px',height=f'{h}px',print_background=True)
            await pg.close()
        await b.close()
import json; asyncio.run(main(json.loads(sys.argv[1])))
