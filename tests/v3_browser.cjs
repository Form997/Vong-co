/* HAI ĐẤT V3: end-to-end Chromium test using real DOM and actual JSON fetch.
 * Run: npm i --no-save playwright@1.56.1 && npx playwright install chromium
 * Serve repository root: python -m http.server 8765 --bind 127.0.0.1
 * Then: node tests/v3_browser.cjs
 */
"use strict";
const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const BASE = process.env.V3_TEST_URL || "http://127.0.0.1:8765/web/v3/";

async function expectCount(page, count, label) {
  const actual = await page.locator("button.piece").count();
  assert.equal(actual, count, label + " expected " + count + ", got " + actual);
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 1,
    locale: "vi-VN",
    colorScheme: "dark",
  });
  const consoleErrors = [];
  page.on("pageerror", err => consoleErrors.push(String(err)));
  page.on("response", response => {
    if (response.url().endsWith("/data/v3/catalog.json") && response.status() !== 200) {
      consoleErrors.push("JSON response: " + response.status());
    }
  });
  try {
    const res = await page.goto(BASE, { waitUntil: "networkidle", timeout: 25000 });
    assert.equal(res.status(), 200, "HTML must load over HTTP");
    await page.waitForSelector("button.piece", { timeout: 8000 });
    await expectCount(page, 20, "Full catalog");
    assert.equal((await page.locator("#count-pieces").innerText()).trim(), "20");
    assert.equal((await page.locator("#count-variants").innerText()).trim(), "30");
    console.log("PASS: load 20 pieces and 30 variants");

    const groups = [
      ["sau-bac", 6],
      ["bay-le", 7],
      ["ba-nam", 3],
      ["bon-oan", 4],
    ];
    for (const [group, count] of groups) {
      await page.locator('button.tab[data-group="' + group + '"]').click();
      await expectCount(page, count, "Filter " + group);
      assert.equal(
        await page.locator('button.tab[data-group="' + group + '"]').getAttribute("aria-pressed"),
        "true"
      );
    }
    await page.locator('button.tab[data-group="all"]').click();
    await expectCount(page, 20, "Reset filter");
    console.log("PASS: 6/7/3/4 family filters");

    const search = page.locator("#search");
    await search.fill("phung cau");
    await expectCount(page, 1, "Unaccented search Phung Cau");
    assert.match(await page.locator("#detail h3").innerText(), /Phụng Cầu/);
    assert.match(await page.locator("#detail").innerText(), /chờ nghiệm thu/i);
    console.log("PASS: Vietnamese diacritic-insensitive search and warning");

    await search.fill("co ban van");
    await expectCount(page, 1, "Unaccented search Co Ban Van");
    assert.match(await page.locator("#detail h3").innerText(), /Cổ Bản/);
    assert.equal(await page.locator("#detail .variant").count(), 2);
    console.log("PASS: distinct Vắn/Trường variants");

    await search.fill("");
    await page.locator("button.piece").filter({hasText:"Nam Ai"}).click();
    assert.match(await page.locator("#detail h3").innerText(), /Nam Ai/);
    assert.equal(await page.locator("#detail .variant").count(), 2);
    console.log("PASS: select piece with conflicting 84/68 systems");

    await page.goto(BASE + "#bai-20", {waitUntil: "networkidle"});
    await page.waitForSelector("button.piece");
    assert.match(await page.locator("#detail h3").innerText(), /Phụng Cầu/);
    console.log("PASS: deep-link to piece 20");

    const display = await page.evaluate(() => ({
      vw: innerWidth,
      scroll: document.documentElement.scrollWidth,
      total: document.querySelectorAll("button.piece").length,
    }));
    assert.ok(display.scroll <= display.vw + 1, "Mobile viewport overflows horizontally: " + JSON.stringify(display));
    assert.equal(display.total, 20);
    console.log("PASS: mobile 390px responsive layout has no horizontal overflow");

    const links = await page.locator("#detail .detail-links a").evaluateAll(els =>
      els.map(a => ({ href: a.href, rel: a.rel, target: a.target }))
    );
    assert.equal(links.length, 2);
    for (const link of links) {
      assert.match(link.href, /^https:\/\/github\.com\/Form997\/Vong-co\/blob\/v3-development\/ban-to\//);
      assert.equal(link.target, "_blank");
      assert.ok(link.rel.includes("noopener"));
    }
    assert.deepEqual(consoleErrors, [], "No uncaught browser JavaScript errors");
    console.log("PASS: local V2 review links and error-free browser rendering");

    fs.mkdirSync("browser-evidence", {recursive:true});
    await page.screenshot({path:"browser-evidence/v3-mobile.png", fullPage:true});
    await page.setViewportSize({width:1366,height:900});
    await page.screenshot({path:"browser-evidence/v3-desktop.png", fullPage:true});
    console.log("PASS: saved mobile and desktop UI snapshots");
  } finally {
    await browser.close();
  }
}

run().catch(err => {console.error("FAIL V3 BROWSER:",err);process.exitCode=1;});
