const { chromium } = require('playwright');
(async()=>{
  const S=(process.env.TEHRANMAP_WORK||'work')+'/';
  const b=await chromium.launch();
  const shots=[['desk',1440,900,null],['deskzoom',1440,900,'zoom'],['phone',400,820,null]];
  for (const [name,w,h,mode] of shots){
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
    const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
    await p.goto('http://127.0.0.1:8765/test.html'); await p.waitForTimeout(4000);
    if(mode==='zoom'){ await p.evaluate(()=>{}); for(let i=0;i<3;i++){await p.mouse.move(640,450); await p.mouse.wheel(0,-300); await p.waitForTimeout(700);} await p.waitForTimeout(1500); await p.mouse.move(600,420); await p.waitForTimeout(400);}
    else if(name==='desk'){ await p.mouse.move(330,600); await p.waitForTimeout(500);}
    await p.screenshot({path:S+'s2-'+name+'.png'});
    console.log(name,errs.filter(e=>!e.includes('TUNNEL')));
  }
  await b.close();
})();
