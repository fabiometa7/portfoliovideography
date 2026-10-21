// Writes the Dutch text into index.html so search engines and link previews
// see the full page without running JavaScript. The page still renders itself
// with JavaScript as before; this only fills in the starting HTML.
//
// Run after changing any text in index.html:
//   node tools/prerender.js
// Needs Playwright (npm i playwright) and a Chromium it can launch.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const file = path.join(__dirname, "..", "index.html");
const CONTAINERS = ["services-list", "cases-list", "pkg-list", "steps"];

const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const page = await browser.newPage({ locale: "nl-NL", timezoneId: "Europe/Amsterdam" });
  await page.goto("file://" + file);
  const nl = await page.evaluate(() => T.nl);
  const html = await page.evaluate(ids => Object.fromEntries(ids.map(id => {
    const el = document.getElementById(id).cloneNode(true);
    el.querySelectorAll("video").forEach(v => v.remove());
    return [id, el.innerHTML];
  })), CONTAINERS);
  await browser.close();

  let src = fs.readFileSync(file, "utf8");
  src = src.replace(/(<(\w+)\b[^>]*\sdata-i18n="([^"]+)"[^>]*>)[^<]*(<\/\2>)/g,
    (m, open, tag, key, close) => key in nl ? open + esc(nl[key]) + close : m);
  src = src.replace(/(<(\w+)\b[^>]*\sdata-i18n-html="([^"]+)"[^>]*>)[\s\S]*?(<\/\2>)/g,
    (m, open, tag, key, close) => key in nl ? open + nl[key] + close : m);
  for (const id of CONTAINERS) {
    const re = new RegExp(`(id="${id}"><!--pre-->)[\\s\\S]*?(<!--/pre-->)`);
    if (!re.test(src)) throw new Error("missing prerender marker for #" + id);
    src = src.replace(re, (m, a, b) => a + html[id].trim() + b);
  }
  fs.writeFileSync(file, src);
  console.log("prerendered", file);
})();
