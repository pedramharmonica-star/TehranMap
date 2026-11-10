const { chromium } = require('playwright');
(async()=>{
  const S=(process.env.TEHRANMAP_WORK||'work')+'/';
  const b=await chromium.launch();
  for (const [name,w,h] of [['desk',1440,900],['phone',400,820]]){
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
    const errs=[]; p.on('pageerror',e=>errs.push(e.message));
    await p.goto('file://'+S+'pub/test.html'); await p.waitForTimeout(4500);
    await p.screenshot({path:S+'s5-'+name+'.png'});
    console.log(name,errs);
  }
  await b.close();
})();
