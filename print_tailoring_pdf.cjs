const { chromium } = require('C:/Users/Shishyan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless:true});
  const page = await browser.newPage();
  await page.goto('file:///' + path.resolve('output/pdf/tailoring_exam_questions_answers_tamil.html').replace(/\\/g,'/'));
  await page.pdf({path:path.resolve('output/pdf/tailoring_exam_questions_answers_tamil.pdf'), format:'A4', printBackground:true, displayHeaderFooter:false});
  await browser.close();
})();
