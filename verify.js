const { chromium } = require('/Users/hadiayoub/Desktop/saba/probe-scroll-sequence/node_modules/playwright');
// expected counts computed independently by coverage.py
const EXPECT = { 'Beirut':15,'Kuwait City':16,'Cairo':14,'Dubai':15,'Riyadh':16,
                 'London':13,'Lagos':14,'Singapore':7,'Sydney':3,'New York':2 };
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8943/coverage.html', {waitUntil:'networkidle'});
  await p.waitForSelector('.readout .row');
  let pass = 0, fail = 0;
  for (const [name, want] of Object.entries(EXPECT)){
    await p.click(`.mkt:has-text("${name}")`);
    await p.waitForTimeout(120);
    const got = +(await p.$eval('#rcount', e => e.innerText)).split(' ')[0];
    const ok = got === want;
    ok ? pass++ : fail++;
    console.log(`${ok?'ok  ':'FAIL'} ${name.padEnd(12)} browser=${got} python=${want}`);
  }
  // click-to-place-a-station path
  await p.mouse.click(720+120, 560);
  await p.waitForTimeout(200);
  const custom = await p.$eval('.mkt[aria-selected="true"]', e=>e.innerText).catch(()=>'(none selected)');
  console.log(`\nclick-to-place: market selection cleared -> ${custom}`);
  console.log(`rows rendered: ${(await p.$$('.readout .row')).length}`);
  // keyboard reachability
  await p.focus('.readout .row:nth-child(3)');
  await p.keyboard.press('Enter');
  await p.waitForTimeout(300);
  console.log('keyboard select ->', await p.$eval('#globeSub', e=>e.innerText));
  console.log('focused element:', await p.evaluate(()=>document.activeElement.className));
  const contrast = await p.$$eval('.row .rname u', els => els.map(e=>getComputedStyle(e).color)[0]);
  console.log('row title colour:', contrast);
  await b.close();
  console.log(`\n${pass} passed, ${fail} failed${errs.length?'\nERRORS: '+errs.join('; '):''}`);
})();
