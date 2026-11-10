const { chromium } = require('playwright');
(async()=>{
  const S=(process.env.TEHRANMAP_WORK||'work')+'/';
  const b=await chromium.launch();
  for (const [name,w,h,scheme] of [['desk',1400,860,'light'],['phone',400,860,'dark']]){
    const p=await b.newPage({viewport:{width:w,height:h},colorScheme:scheme});
    const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
    await p.goto('file://'+S+'test.html'); await p.waitForTimeout(3500);
    if(name==='desk'){ await p.mouse.click(420,560); await p.waitForTimeout(600); }
    await p.screenshot({path:S+'shot-'+name+'.png',fullPage:name==='phone'});
    console.log(name,errs);
  }
  await b.close();
})();
