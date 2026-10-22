// usage: node epoch_check.cjs <_site dir>
const fs = require('fs'), path = require('path');
const { chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const site = process.argv[2];
let html = fs.readFileSync(path.join(site, 'index.html'), 'utf8');
const extra = `
    <div class="clock unix hidden" data-timezone="EPOCH"><div class="time"></div><div class="location">Unix</div></div>
    <div class="clock epoch hidden" data-timezone="UTC"><div class="time"></div><div class="location">EPOCH</div></div>
  </div>`;
html = html.replace(/<\/div>\s*<\/body>/, extra + '\n</body>');
fs.writeFileSync(path.join(site, 'check.html'), html);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(site, 'check.html'));
  await p.waitForTimeout(1000);
  const r = await p.$$eval('.clock', cs => cs.map(c => [c.querySelector('.location').textContent, c.dataset.timezone,
    getComputedStyle(c.querySelector('.time')).fontSize, getComputedStyle(c.querySelector('.location')).fontSize]));
  console.log(JSON.stringify(r));
  let ok = true;
  for (const [name, tz, t, l] of r) {
    const ratio = parseFloat(t) / parseFloat(l); // .time 2em vs .location 0.75em → 2.67; small 1.25/0.75 → 1.67
    const small = ratio < 2;
    if (small !== (tz === 'EPOCH')) { ok = false; console.log(`FAIL ${name} (${tz}): ratio ${ratio.toFixed(2)}`); }
  }
  console.log(ok ? 'PASS' : 'FAILED'); await b.close(); process.exit(ok ? 0 : 1);
})();
