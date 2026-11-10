const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:680,height:420}});
await p.goto('http://127.0.0.1:8766/prev.html');await p.waitForTimeout(800);await p.screenshot({path:(process.env.TEHRANMAP_WORK||'work')+'/logo-prev.png'});await b.close()})();
