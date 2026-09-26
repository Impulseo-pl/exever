import sys
from playwright.sync_api import sync_playwright
url,out,w=sys.argv[1],sys.argv[2],int(sys.argv[3])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg=b.new_page(viewport={'width':w,'height':900},device_scale_factor=1)
    pg.goto(url,wait_until='networkidle',timeout=60000)
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(1200); pg.evaluate("window.scrollTo(0,0)")
    pg.screenshot(path=out,full_page=True)
    b.close()
