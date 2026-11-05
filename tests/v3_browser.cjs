/* HAI ĐẤT V3.2: Chromium E2E for 20 detail pages, source filters and navigation.
 * Run: npm i --no-save playwright@1.56.1 && npx playwright install chromium
 * Build site: python scripts/v3_build_site.py --out _site\n * Serve artifact: python -m http.server 8765 --directory _site --bind 127.0.0.1
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

// Exercise real browser navigation, including a CDN that briefly serves stale HTML.
async function checkAutoUpdateNavigation(browser, staleHtml) {
  const testPage = await browser.newPage();
  const oldVersion = "a".repeat(64), newVersion = "b".repeat(64);
  const client = fs.readFileSync("web/v3/auto-update.js", "utf8");
  let documentLoads = 0, manifestRequests = 0;
  await testPage.route("http://updates.test/**", async route => {
    const url = new URL(route.request().url());
    if (url.pathname.endsWith("/site-version.json")) {
      manifestRequests++;
      // Let the first document load before the asynchronous manifest response.
      await new Promise(resolve => setTimeout(resolve, 150));
      return route.fulfill({status:200, contentType:"application/json", body:JSON.stringify({version:newVersion})});
    }
    if (url.pathname.endsWith("/web/v3/auto-update.js")) {
      return route.fulfill({status:200, contentType:"application/javascript", body:client});
    }
    if (route.request().isNavigationRequest()) {
      documentLoads++;
      const version = !staleHtml && url.searchParams.has("hai_dat_version") ? newVersion : oldVersion;
      const html = `<meta name="hai-dat-revision" content="${version}"><script src="../../web/v3/auto-update.js"></script>`;
      return route.fulfill({status:200, contentType:"text/html", body:html});
    }
    return route.abort();
  });
  try {
    await testPage.goto("http://updates.test/Vong-co/bai/05/?lang=vi#cau-37", {waitUntil:"domcontentloaded"});
    await testPage.waitForURL(url => url.searchParams.get("hai_dat_version") === newVersion, {timeout:8000});
    await testPage.waitForLoadState("load");
    // Give an accidental second refresh enough time to occur.
    await testPage.waitForTimeout(650);
    const result = new URL(testPage.url());
    assert.equal(result.searchParams.get("lang"), "vi");
    assert.equal(result.hash, "#cau-37");
    assert.equal(documentLoads, 2, "only one automatic refresh for a given revision");
    assert.ok(manifestRequests >= 2, "both old and refreshed pages check the manifest");
    assert.equal(await testPage.locator('meta[name="hai-dat-revision"]').getAttribute("content"), staleHtml ? oldVersion : newVersion);
  } finally {
    await testPage.close();
  }
}

async function checkSearchAndRecovery(browser) {
  const page = await browser.newPage();
  try {
    await page.goto(BASE, {waitUntil:"networkidle"});
    await page.waitForSelector("button.piece");
    for (const [query, title] of [["1", "Lưu Thủy Trường"], ["17", "Tứ Đại Oán"], ["20", "Phụng Cầu Hoàng Duyên"]]) {
      await page.locator("#search").fill(query);
      await expectCount(page, 1, "Exact song number " + query);
      assert.equal(await page.locator("button.piece strong").innerText(), title);
    }
    await page.locator("#reset-filters").click();
    await expectCount(page, 20, "Reset restores all songs");
    await page.locator('[data-group="bon-oan"]').click();
    await page.locator("#sort-order").selectOption("name");
    const shared = new URL(page.url());
    assert.equal(shared.searchParams.get("group"), "bon-oan");
    assert.equal(shared.searchParams.get("sort"), "name");
    await page.reload({waitUntil:"networkidle"});
    await page.waitForSelector("button.piece");
    await expectCount(page, 4, "Shared filters survive reload");
    assert.equal(await page.locator("#sort-order").inputValue(), "name");
    await page.locator("#reset-filters").click();
    assert.equal(new URL(page.url()).searchParams.has("group"), false);
    await page.goto(BASE + "?group=invalid&evidence=invalid&lesson=invalid&sort=invalid", {waitUntil:"networkidle"});
    await page.waitForSelector("button.piece");
    await expectCount(page, 20, "Invalid URL filters use defaults");
    let failed = false;
    await page.route("**/data/v3/catalog.json", async route => {
      if (!failed) { failed=true; return route.fulfill({status:503, body:"unavailable"}); }
      return route.continue();
    });
    await page.goto(BASE, {waitUntil:"networkidle"});
    await page.locator("#retry-load").waitFor();
    assert.equal(await page.locator("#pieces").getAttribute("aria-busy"), "false");
    await page.locator("#retry-load").click();
    await page.waitForSelector("button.piece");
    await expectCount(page, 20, "Retry recovers without a page reload");
    await page.unroute("**/data/v3/catalog.json");
    await page.clock.install();
    await page.addInitScript(() => {
      const original = window.fetch.bind(window);
      window.stallCatalog = true;
      window.fetch = (url, options) => {
        if (window.stallCatalog && String(url).includes("catalog.json"))
          return new Promise((resolve, reject) => options.signal.addEventListener("abort",
            () => reject(new DOMException("timeout", "AbortError")), {once:true}));
        return original(url, options);
      };
    });
    await page.goto(BASE, {waitUntil:"domcontentloaded"});
    await page.clock.fastForward(13000);
    await page.locator("#retry-load").waitFor();
    assert.match(await page.locator("#pieces").innerText(), /quá lâu/);
    await page.evaluate(() => { window.stallCatalog = false; });
    await page.locator("#retry-load").click();
    await page.waitForSelector("button.piece");
    await expectCount(page, 20, "Timed-out request can recover");
    console.log("PASS: exact numeric search, reset, shared filters, HTTP failure and timeout recovery");
  } finally { await page.close(); }
}

async function run() {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 1,
    locale: "vi-VN",
    colorScheme: "light",
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
    assert.equal((await page.locator("#count-lessons").innerText()).trim(), "6");
    console.log("PASS: load 20 pieces and 30 variants");

    // Visual regression contract: coherent heritage color system and hero landmarks.
    assert.match(await page.locator("#hero-title").innerText(), /Giữ hồn tiếng đờn/);
    assert.equal(await page.locator(".hero-art").getAttribute("aria-hidden"), "true");
    const palette = await page.evaluate(() => ({
      body: getComputedStyle(document.body).backgroundColor,
      foreground: getComputedStyle(document.body).color,
      hero: getComputedStyle(document.querySelector(".hero")).backgroundImage,
      focusableCards: [...document.querySelectorAll("button.piece")].every(e => e.type === "button")
    }));
    assert.equal(palette.body, "rgb(246, 244, 238)");
    assert.match(palette.hero, /linear-gradient/);
    assert.ok(palette.focusableCards);
    console.log("PASS: editorial ivory/jade palette, accessible hero and real button cards");
    await page.setViewportSize({width:360,height:800});
    assert.equal(await page.locator('.taskbar a').count(), 4);
    await page.locator('#search').fill('17');
    await expectCount(page, 1, 'Search before taskbar navigation');
    const queryBeforeTask = new URL(page.url()).search;
    await page.locator('.taskbar [data-task="ly"]').click();
    await page.waitForFunction(() => Math.abs(document.getElementById('bai-ly').getBoundingClientRect().top) < 150 && document.querySelector('.taskbar [aria-current]')?.dataset.task === 'ly');
    assert.equal(new URL(page.url()).search, queryBeforeTask);
    await page.locator('#ly-dossier-002-link').click();
    assert.equal(await page.locator('.taskbar [aria-current]').getAttribute('data-task'), 'ly');
    await page.locator('.taskbar [data-task="search"]').click();
    await page.waitForSelector('button.piece');
    await page.locator('.taskbar [data-task="search"]').click();
    assert.equal(await page.locator('#search').evaluate(el => el === document.activeElement), true);
    assert.ok(await page.locator('.taskbar').evaluate(el => el.getBoundingClientRect().bottom <= innerHeight));
    await page.locator('.taskbar [data-task="sources"]').click();
    assert.equal(new URL(page.url()).hash, '#nguon');
    await page.locator('.taskbar [data-task="home"]').click();
    await page.goto(BASE, {waitUntil:'networkidle'});
    console.log('PASS: mobile taskbar, section navigation, nested return, search focus and query preservation');

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
    // Four dedicated family pages must be navigable, source-linked and return 200.
    for (const [group, count] of groups) {
      const familyLink = page.locator('.group-directory-grid a[href="../../nhom/' + group + '/"]');
      assert.equal(await familyLink.count(), 1, "Group link missing: " + group);
      const url = new URL("../../nhom/" + group + "/", BASE).toString();
      const response = await page.request.get(url);
      assert.equal(response.status(), 200, "Family page HTTP: " + group);
      const markup = await response.text();
      assert.ok(markup.includes("0/20"), "Family disclaimer: " + group);
      assert.equal((markup.match(/class="family-piece"/g) || []).length, count,
        "Family page count: " + group);
    }
    console.log("PASS: four standalone family group pages via HTTP");

    // Evidence selector returns only pieces with this kind of evidence.
    const catalogResponse = await page.request.get(new URL("../../data/v3/catalog.json", BASE).toString());
    assert.equal(catalogResponse.status(), 200);
    const catalog = await catalogResponse.json();
    const evidence = page.locator("#evidence");
    for (const status of ["source_indexed", "source_reported", "derived_unverified"]) {
      await evidence.selectOption(status);
      const expected = catalog.items.filter(item => item.variants.some(v => v.evidence_status === status)).length;
      await expectCount(page, expected, "Evidence filter " + status);
    }
    await evidence.selectOption("all");
    await expectCount(page, 20, "Reset evidence filter");
    console.log("PASS: filter by source-indexed, reported and unverified evidence");

    await page.locator("#sort-order").selectOption("name");
    const shownNames = await page.locator("button.piece strong").allInnerTexts();
    const sortedNames = [...shownNames].sort((a, b) => a.localeCompare(b, "vi"));
    assert.deepEqual(shownNames, sortedNames);
    await page.locator("#sort-order").selectOption("number");
    assert.match(await page.locator("button.piece").first().innerText(), /Lưu Thủy/);
    console.log("PASS: Vietnamese A–Z sort and numeric reset");

    // V3.2 legal release: users must see the law/privacy notice from the homepage.
    const policyLink = page.locator('footer a[href="legal.html"]');
    assert.equal(await policyLink.count(), 1, "Privacy and legal notice must be in homepage footer");
    const legalResponse = await page.request.get(new URL("legal.html", BASE).toString());
    assert.equal(legalResponse.status(), 200);
    const legalBody = await legalResponse.text();
    for (const word of ["PRIVACY.md", "SECURITY.md", "RIGHTS_AND_LICENSING.md",
                        "116/2025/QH15", "91/2025/QH15", "2026/1744",
                        "0/20", "phi thương mại"]) {
      assert.ok(legalBody.includes(word), "Legal page missing " + word);
    }
    await policyLink.click();
    await page.waitForURL("**/web/v3/legal.html");
    assert.match(await page.locator("h1").innerText(), /Pháp lý/);
    const countries = [
      ["my", "Hoa Kỳ", 4], ["nga", "Nga", 4], ["trung-quoc", "Trung Quốc", 6],
      ["uc", "Úc", 5], ["nhat-ban", "Nhật Bản", 4], ["han-quoc", "Hàn Quốc", 5]
    ];
    for (const [slug, label, n] of countries) {
      const countryURL = new URL("quoc-gia/" + slug + ".html", BASE).toString();
      const response = await page.request.get(countryURL);
      assert.equal(response.status(), 200, "Country page missing " + slug);
      await page.goto(countryURL,{waitUntil:"networkidle"});
      assert.match(await page.locator("h1").innerText(), new RegExp(label));
      assert.equal(await page.locator("article.source").count(), n);
      assert.equal(await page.locator('article.source a[href^="https://"]').count(), n);
      assert.match(await page.locator("main").innerText(), /NO-GO/);
      assert.equal(await page.locator("iframe,video,audio,form").count(), 0);
    }
    await page.goto(new URL("legal.html", BASE).toString(),{waitUntil:"networkidle"});
    for (const [slug] of countries) {
      assert.equal(await page.locator('a[href="quoc-gia/'+slug+'.html"]').count(), 1);
    }
    await page.setViewportSize({width:390,height:844});
    const countryOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    assert.equal(countryOverflow,false,"Six-country legal hub must fit mobile 390px");
    await page.goto(BASE,{waitUntil:"networkidle"});
    await page.waitForSelector("button.piece");
    console.log("PASS: six 2026 country law pages (28 official sources), mobile links and privacy disclosure");

    const lessonSelect = page.locator("#lesson-status");
    await lessonSelect.selectOption("indexed");
    await expectCount(page, 6, "Six pieces with source indexes in V3.5");
    const indexedNames = await page.locator("button.piece strong").allInnerTexts();
    assert.ok(indexedNames.some(t => t.includes("Lưu Thủy")));
    assert.ok(indexedNames.some(t => t.includes("Phụng Cầu")));
    await lessonSelect.selectOption("pending");
    await expectCount(page, 14, "14 without normalized source-label indexes");
    await lessonSelect.selectOption("all");
    await expectCount(page, 20, "Reset lesson availability");
    console.log("PASS: V3.5 lesson filter: 6 pieces and 14 waiting");

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
    assert.match(await page.locator("#detail").innerText(), /34 nhãn/);
    assert.match(await page.locator("#detail").innerText(), /68 nhãn/);
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
    assert.equal(links.length, 4);
    assert.match(links[0].href, /\/Vong-co\/bai\/20-phung-cau\/$|\/bai\/20-phung-cau\/$/);
    assert.match(links[1].href, /\/bai\/20-phung-cau\/#hoc-tung-cau$/);
    for (const link of links.slice(2)) {
      assert.match(link.href, /^https:\/\/github\.com\/Form997\/Vong-co\/blob\/main\/ban-to\//);
      assert.equal(link.target, "_blank");
      assert.ok(link.rel.includes("noopener"));
    }
    await page.locator("#detail .piece-page-link").click();
    await page.waitForURL("**/bai/20-phung-cau/");
    assert.match(await page.locator("h1").innerText(), /Phụng Cầu/);
    assert.equal(await page.locator("article.variant").count(), 1);
    assert.equal(await page.locator("details.phrase-row").count(), 40);
    await page.locator("#cau-40 summary").click();
    const lastPhrase = await page.locator("#cau-40").innerText();
    assert.match(lastPhrase, /340/);
    assert.match(lastPhrase, /341/);
    assert.match(lastPhrase, /chưa/i);
    const audioNodes = await page.locator("audio,video,iframe").count();
    assert.equal(audioNodes, 0, "No unlicensed media embeds");
    console.log("PASS: Phung Cau source index has 40 labels; final phrase on pp.340/341");
    assert.match(await page.locator("main").innerText(), /0\/20/);
    assert.equal(await page.locator(".detail-hero").count(), 1);
    assert.equal(await page.locator("nav.quick-links").count(), 0); // semantic anchors live inside hero
    assert.equal(await page.locator("details.phrase-row").count(), 40);
    const detailLayout = await page.evaluate(() => ({ vw: innerWidth, sw: document.documentElement.scrollWidth }));
    assert.ok(detailLayout.sw <= detailLayout.vw + 1, "Detail page overflows mobile viewport");
    console.log("PASS: standalone Phung Cau page, 0/20 disclaimer and mobile layout");

    // All 20 standalone pages are accessible from the generated artifact.
    for (const item of catalog.items) {
      const itemPage = await page.request.get(new URL("../../bai/" + item.slug + "/", BASE).toString());
      assert.equal(itemPage.status(), 200, "Missing detail URL " + item.slug);
    }
    console.log("PASS: 20/20 dedicated URLs serve HTTP 200");

    const learningURL = new URL("../../bai/01-luu-thuy-truong/", BASE).toString();
    await page.goto(learningURL,{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 32);
    await page.locator("#cau-01 summary").click();
    assert.match(await page.locator("#cau-01").innerText(), /HO/);
    await page.locator("#cau-03 summary").click();
    assert.match(await page.locator("#cau-03").innerText(), /HÒ/);
    assert.match(await page.locator("#hoc-tung-cau").innerText(), /0\/20/);
    console.log("PASS: Luu Thuy 32 source-specific rows, HO versus HÒ preserved");


    // V3.3: independently verified source-label locators, not musical validation.
    await page.goto(new URL("../../bai/02-phu-luc-chan/", BASE).toString(),{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 34);
    await page.locator("#cau-08 summary").click();
    assert.match(await page.locator("#cau-08").innerText(), /DỊ BẢN/);
    assert.match(await page.locator("#cau-08").innerText(), /Xáng Tồn/);
    await page.locator("#cau-33 summary").click();
    await page.locator("#cau-34 summary").click();
    for (const n of [33,34]) {
      const row = await page.locator("#cau-"+n).innerText();
      assert.match(row, /KHÔNG CÓ/);
      assert.match(row, /Văn Dần/);
      assert.doesNotMatch(row, /trang nhạc 130/); // no fabricated page offsets for Nhi Tan II
    }
    assert.equal(await page.locator("#cau-34 a[href*='#page=']").count(), 0);
    console.log("PASS: Phu Luc Chan 34/32 discrepancy, source variants 08/34 and no false PDF page mapping");

    await page.goto(new URL("../../bai/03-binh-ban-chan/", BASE).toString(),{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 44);
    await page.locator("#cau-44 summary").click();
    assert.match(await page.locator("#cau-44").innerText(), /134/);
    assert.match(await page.locator("#cau-44").innerText(), /135/);
    assert.equal(await page.locator("#cau-44 a[href*='#page=']").count(), 0);
    console.log("PASS: Binh Ban Chan 44 indexed source labels with source-specific printed page citations");

    await page.goto(new URL("../../bai/04-co-ban-van/", BASE).toString(),{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 102);
    assert.match(await page.locator("#hoc-tung-cau").innerText(), /Vắn/);
    assert.match(await page.locator("#hoc-tung-cau").innerText(), /Trường/);
    assert.equal(await page.locator("#hoc-tung-cau").count(), 1);
    assert.deepEqual(await page.evaluate(() => {
      const ids = [...document.querySelectorAll("[id]")].map(x => x.id);
      return ids.filter((id, i) => ids.indexOf(id) !== i);
    }), [], "IDs for both systems must be unique");
    assert.equal(await page.locator("audio").count(), 0);
    console.log("PASS: Co Ban Vắn and Trường 34/68 labels, unique anchors, no audio");

    await page.goto(new URL("../../bai/05-xuan-tinh-chan/", BASE).toString(),{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 48);
    await page.locator("#cau-37 summary").click();
    assert.match(await page.locator("#cau-37").innerText(), /khác|khác biệt/i);
    assert.equal(await page.locator("#cau-37 a[href*='#page=']").count(), 0);
    assert.equal(await page.locator("audio").count(), 0);
    console.log("PASS: Xuan Tinh 48 source labels and unresolved discrepancy");

    await page.goto(new URL("../../bai/18-phung-hoang/", BASE).toString(),{waitUntil:"networkidle"});
    assert.equal(await page.locator("details.phrase-row").count(), 0);
    assert.match(await page.locator("#hoc-tung-cau").innerText(), /chờ sổ nguồn/i);
    console.log("PASS: piece 18 provisional ledger is NOT published as verified phrase index");

    await page.goto(BASE, {waitUntil:"networkidle"});
    await page.locator('#ly-dossier-link').click();
    assert.equal(await page.locator("h1").innerText(), "Lý cây bông");
    assert.match(await page.locator(".status").innerText(), /Chưa nghiệm thu diễn xướng/);
    assert.equal(await page.locator("ol > li").count(), 4);
    assert.equal(await page.locator("a[href$='#page=96']").count(), 1);
    assert.equal(await page.locator("audio, iframe").count(), 0);
    for (const width of [360, 768, 1366]) {
      await page.setViewportSize({width,height:900});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1));
    }
    console.log("PASS: Ly cay bong dossier, 4 sources, PDF page 96, responsive and no media");
    await page.goto(BASE, {waitUntil:"networkidle"});
    await page.setViewportSize({width:360,height:900});
    await page.locator('#ly-dossier-002-link').click();
    assert.equal(await page.locator('h1').innerText(), 'Lý con sáo Gò Công');
    assert.equal(await page.locator('ol > li').count(), 6);
    assert.equal(await page.locator('table tbody tr').count(), 5);
    assert.equal(await page.locator("a[href$='#page=116']").count(), 1);
    assert.equal(await page.locator("a[href$='#page=96']").count(), 0);
    assert.equal(await page.locator('audio, iframe').count(), 0);
    for (const width of [360, 768, 1366]) {
      await page.setViewportSize({width,height:900});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1));
    }
    await page.locator('nav a[href="../01-ly-cay-bong/"]').click();
    assert.equal(await page.locator('h1').innerText(), 'Lý cây bông');
    console.log('PASS: Ly con sao Go Cong, 6 sources, source isolation, 5 comparison rows and sibling navigation');
    await page.setViewportSize({width:360,height:844});
    await page.locator('.reading-tools summary').click();
    await page.locator('[data-reading="larger"]').click();
    await page.locator('[data-reading="larger"]').click();
    assert.equal(await page.locator('body').getAttribute('data-reading-size'), '2');
    assert.equal(await page.locator('[data-reading="larger"]').isDisabled(), true);
    await page.locator('[data-reading="focus"]').click();
    assert.equal(await page.locator('[data-reading="focus"]').getAttribute('aria-pressed'), 'true');
    assert.match(await page.locator('main').innerText(), /Chưa nghiệm thu diễn xướng/);
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await page.reload({waitUntil:'networkidle'});
    assert.equal(await page.locator('body').getAttribute('data-reading-size'), '2');
    assert.equal(await page.locator('body').getAttribute('data-reading-focus'), 'true');
    await page.locator('.reading-tools summary').click();
    await page.locator('[data-reading="reset"]').click();
    assert.equal(await page.locator('body').getAttribute('data-reading-size'), '0');
    assert.equal(await page.locator('body').getAttribute('data-reading-focus'), 'false');
    assert.equal(await page.evaluate(() => localStorage.getItem('hai-dat-reading-v1')), null);
    await page.locator('[data-reading="top"]').click();
    assert.equal(await page.locator('h1').evaluate(el => el === document.activeElement), true);
    const noScript = await browser.newContext({javaScriptEnabled:false});
    const plain = await noScript.newPage();
    await plain.goto(new URL('../../ly/01-ly-cay-bong/',BASE).toString());
    assert.equal(await plain.locator('.reading-tools').isVisible(), false);
    assert.equal(await plain.locator('h1').innerText(), 'Lý cây bông');
    await noScript.close();
    const denied = await browser.newContext();
    await denied.addInitScript(() => Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}}));
    const deniedPage = await denied.newPage();
    await deniedPage.goto(new URL('../../ly/01-ly-cay-bong/',BASE).toString());
    await deniedPage.locator('.reading-tools summary').click();
    await deniedPage.locator('[data-reading="larger"]').click();
    assert.equal(await deniedPage.locator('body').getAttribute('data-reading-size'), '1');
    await denied.close();
    console.log('PASS: reader size limits, persistence, reset, focus, no JavaScript and blocked storage');

    await page.goto(BASE, {waitUntil:"networkidle"});
    await page.waitForSelector("button.piece");
    assert.deepEqual(consoleErrors, [], "No uncaught browser JavaScript errors");
    console.log("PASS: local V2 review links and error-free browser rendering");

    // Check that mobile, tablet, and desktop widths do not horizontally overflow.
    for (const width of [360, 390, 768, 1024, 1366]) {
      await page.setViewportSize({width,height:900});
      const bounds = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        scroll: document.documentElement.scrollWidth,
        hero: document.querySelector(".hero").getBoundingClientRect().width,
        art: getComputedStyle(document.querySelector(".hero-art")).display
      }));
      assert.ok(bounds.scroll <= bounds.viewport + 1,
        "Horizontal overflow at " + width + ": " + JSON.stringify(bounds));
      assert.ok(bounds.hero > 250, "Hero unexpectedly narrow at " + width);
      if (width <= 700) assert.equal(bounds.art, "none");
    }
    console.log("PASS: responsive layout at 360/390/768/1024/1366px, no horizontal overflow");

    fs.mkdirSync("browser-evidence", {recursive:true});
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:"browser-evidence/v3-mobile.png", fullPage:true});
    await page.locator(".hero").screenshot({path:"browser-evidence/v3-mobile-hero.png"});
    await page.setViewportSize({width:768,height:960});
    await page.screenshot({path:"browser-evidence/v3-tablet.png", fullPage:true});
    await page.setViewportSize({width:1366,height:900});
    await page.screenshot({path:"browser-evidence/v3-desktop.png", fullPage:true});
    await page.locator(".hero").screenshot({path:"browser-evidence/v3-desktop-hero.png"});

    await page.goto(new URL("../../bai/20-phung-cau/", BASE).toString(),{waitUntil:"networkidle"});
    await page.setViewportSize({width:1366,height:900});
    await page.screenshot({path:"browser-evidence/v3-lesson-desktop.png", fullPage:true});
    await page.setViewportSize({width:390,height:844});
    await page.locator("#cau-01 summary").click();
    await page.screenshot({path:"browser-evidence/v3-lesson-mobile.png", fullPage:true});
    console.log("PASS: saved mobile/tablet/desktop home and lesson visual snapshots");

    await checkSearchAndRecovery(browser);
    await checkAutoUpdateNavigation(browser, false);
    await checkAutoUpdateNavigation(browser, true);
    console.log("PASS: automatic version refresh preserves query/hash and avoids stale-cache loops");
  } finally {
    await browser.close();
  }
}

run().catch(err => {console.error("FAIL V3 BROWSER:",err);process.exitCode=1;});

