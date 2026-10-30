"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const client = fs.readFileSync(path.join(__dirname, "../web/v3/auto-update.js"), "utf8");
const oldVersion = "a".repeat(64), newVersion = "b".repeat(64);
const turn = () => new Promise(resolve => setImmediate(resolve));

async function launch(options = {}) {
  const calls = [], replacements = [], handlers = {}, footerItems = [];
  const location = {
    href: options.href || "https://example.test/Vong-co/bai/05/?lang=vi#cau-37",
    origin: "https://example.test",
    replace: url => replacements.push(url)
  };
  const doc = {
    currentScript: {src: options.script || "https://example.test/Vong-co/web/v3/auto-update.js"},
    visibilityState: options.hidden ? "hidden" : "visible",
    querySelector: selector => selector === 'meta[name="hai-dat-revision"]'
      ? {content: options.current || oldVersion}
      : selector === "footer" ? {querySelector: () => null, append: value => footerItems.push(value)} : null,
    createElement: () => ({}),
    addEventListener: (name, callback) => {handlers[name] = callback;}
  };
  let response = options.response || {ok:true, json: async () => ({version: newVersion})};
  const context = {
    document:doc, URL,
    window:{location, setInterval: (callback, delay) => {handlers.timer=callback; handlers.delay=delay;}},
    fetch: async (url, init) => {
      calls.push({url, init});
      if (response instanceof Error) throw response;
      return response;
    }
  };
  vm.runInNewContext(client, context);
  await turn();
  return {calls,replacements,handlers,doc,footerItems,setResponse: r => {response=r;}};
}

test("a new deployed revision refreshes the current page and preserves its state in the URL", async () => {
  const x = await launch();
  assert.equal(x.calls.length,1);
  assert.equal(x.calls[0].url,"https://example.test/Vong-co/site-version.json");
  assert.equal(x.calls[0].init.cache,"no-store");
  assert.equal(x.handlers.delay,60_000);
  assert.equal(x.footerItems[0].textContent, "Mã bản website: " + oldVersion.slice(0,12));
  assert.equal(x.replacements.length,1);
  const target = new URL(x.replacements[0]);
  assert.equal(target.pathname,"/Vong-co/bai/05/");
  assert.equal(target.searchParams.get("lang"),"vi");
  assert.equal(target.searchParams.get("hai_dat_version"),newVersion);
  assert.equal(target.hash,"#cau-37");
});

test("same revision, invalid manifest, and failed network leave the page intact", async () => {
  for (const response of [
    {ok:true,json:async () => ({version: oldVersion})},
    {ok:true,json:async () => ({version:"not-a-sha"})},
    {ok:false}, new Error("offline")
  ]) {
    const x=await launch({response});
    assert.deepEqual(x.replacements,[]);
  }
});

test("stale HTML returned after refresh cannot cause an endless refresh loop", async () => {
  const x=await launch({href:`https://example.test/Vong-co/web/v3/?hai_dat_version=${newVersion}#bai-05`});
  x.handlers.timer();
  x.handlers.visibilitychange();
  await turn();
  assert.deepEqual(x.replacements,[]);
});

test("hidden pages wait until visible before checking for an update", async () => {
  const x=await launch({hidden:true});
  assert.equal(x.calls.length,0);
  x.doc.visibilityState="visible";
  x.handlers.visibilitychange();
  await turn();
  assert.equal(x.calls.length,1);
  assert.equal(x.replacements.length,1);
});

test("cross-origin script URL cannot trigger update checks", async () => {
  const x=await launch({script:"https://elsewhere.test/web/v3/auto-update.js"});
  assert.equal(x.calls.length,0);
  assert.deepEqual(x.replacements,[]);
});
