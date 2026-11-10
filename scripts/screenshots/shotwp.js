const { chromium } = require('playwright');
(async()=>{const S=(process.env.TEHRANMAP_WORK||'work')+'/';const b=await chromium.launch();
for(const [n,w,h] of [['desk',1300,1000],['phone',400,900]]){const p=await b.newPage({viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8770/index.html');await p.waitForTimeout(6000);await p.screenshot({path:S+'wp-'+n+'.png',fullPage:true});console.log(n,errs);}
await b.close()})();
