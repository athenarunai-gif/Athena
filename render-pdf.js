const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file:///home/user/Athena/AthenaRun-Marktbeobachtung-CDMO.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  await p.pdf({
    path: '/home/user/Athena/AthenaRun-Marktbeobachtung-CDMO.pdf',
    width: '13.31944in', height: '7.5in', printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await b.close();
  console.log('pdf ok');
})();
