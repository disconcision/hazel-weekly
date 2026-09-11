const {chromium}=require('/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path'),fs=require('fs');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});
for(const [slug,port] of [['neg100',8920],['neg060',8921],['neg019',8922]]){
 const ctx=await browser.newContext({viewport:{width:1440,height:1050},deviceScaleFactor:2});const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${port}/`,{waitUntil:'networkidle'});await page.waitForTimeout(1200);
 console.log(slug,'ERRORS',errors,'BODY',(await page.locator('body').innerText()).slice(0,6000));
 await page.screenshot({path:path.join(__dirname,slug,'assets/build-initial.png')});
 fs.writeFileSync(path.join(__dirname,slug,'research/build-dom.html'),await page.content());await ctx.close();
}await browser.close()})();
