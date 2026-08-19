const { chromium } = require('/Users/hadiayoub/Desktop/saba/probe-scroll-sequence/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const errs = [];
  const shot = async (name, w, h, fn) => {
    const p = await (await b.newContext({viewport:{width:w,height:h}, deviceScaleFactor:2})).newPage();
    p.on('console', m => m.type()==='error' && errs.push(`${name}: ${m.text()}`));
    p.on('pageerror', e => errs.push(`${name}: ${e.message}`));
    await p.goto('http://127.0.0.1:8940/index.html', {waitUntil:'networkidle'});
    await p.waitForTimeout(900);
    if (fn) { await fn(p); await p.waitForTimeout(1000); }
    await p.screenshot({path:name, fullPage: h>900});
    return p;
  };
  await shot('shot-full.png', 1440, 1500);
  const p = await shot('shot-sel.png', 1440, 980, async pg => {
    await pg.click('.readout .row:nth-child(1)');
  });
  console.log('readout row 1:', await p.$eval('.readout .row:nth-child(1)', e=>e.innerText.replace(/\n/g,' | ')));
  console.log('visible count:', await p.$eval('#rcount', e=>e.innerText));
  console.log('arc note:', await p.$eval('#arcnote', e=>e.innerText));
  await shot('shot-mobile.png', 390, 844);
  await b.close();
  console.log(errs.length ? 'ERRORS:\n'+errs.join('\n') : 'no console errors');
})();
