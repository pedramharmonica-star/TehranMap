const { chromium } = require('playwright');
(async()=>{
  const S=(process.env.TEHRANMAP_WORK||'work')+'/';
  const b=await chromium.launch();
  for (const [name,w,h] of [['over',1440,900],['west',1440,900]]){
    const p=await b.newPage({viewport:{width:w,height:h}});
    const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
    await p.goto('file://'+S+'pub/test.html'); await p.waitForTimeout(5000);
    if(name==='west'){ for(let i=0;i<4;i++){await p.mouse.move(170,360); await p.mouse.wheel(0,-250); await p.waitForTimeout(800);} await p.waitForTimeout(2500); await p.mouse.move(700,500); await p.waitForTimeout(400);}
    else { await p.mouse.move(900,560); await p.waitForTimeout(400); }
    await p.screenshot({path:S+'s3-'+name+'.png'});
    console.log(name,errs.filter(e=>!e.includes('TUNNEL')&&!e.includes('fonts')));
  }
  await b.close();
})();
