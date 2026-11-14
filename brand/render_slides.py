import re, sys, pathlib, asyncio
from playwright.async_api import async_playwright
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); logo = sys.argv[3]
names = ["Main","Slide2","Slide3","Slide4","Slide5"]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i,n in enumerate(names,1):
            h = (src/f"{n}.dc.html").read_text()
            h = h.replace("{{accent}}","#0B66FF").replace('<script src="./support.js"></script>','')
            h = re.sub(r"/_blob/[0-9a-f]+", "file://"+logo, h)
            h = h.replace("<helmet>","").replace("</helmet>","")
            tmp = out/f"s{i}.html"; tmp.write_text(h)
            await pg.goto("file://"+str(tmp)); await pg.wait_for_load_state("networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(out/f"slide{i}.jpg"), type="jpeg", quality=92, clip={"x":0,"y":0,"width":1080,"height":1350})
        await b.close()
asyncio.run(main())
