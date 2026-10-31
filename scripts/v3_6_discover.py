#!/usr/bin/env python3
"""V3.6: free scholarly metadata discovery, never self-publish to catalog."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/v3_6/source_queries.json"
DOI = re.compile(r"^10\.\d{4,9}/[^\s<>]+$", re.I)
ENDPOINTS = {("api.crossref.org", "/works"), ("api.openalex.org", "/works")}


def unique_keys(pairs):
    out = {}
    for key, val in pairs:
        if key in out:
            raise ValueError("JSON duplicate key")
        out[key] = val
    return out


def read_config(path=CONFIG):
    with open(path, encoding="utf-8") as f:
        c = json.load(f, object_pairs_hook=unique_keys)
    keys = {"schema_version", "scope", "review_policy", "auto_publish",
            "query_terms", "title_match_phrases", "per_page", "max_candidates"}
    if not isinstance(c, dict) or set(c) != keys:
        raise ValueError("Bad V3.6 config schema")
    if (c["schema_version"] != "3.6.0-alpha.1" or c["scope"] != "metadata_only" or
        c["review_policy"] != "human_required" or c["auto_publish"] is not False):
        raise ValueError("Automatic approval is forbidden")
    for field, length in (("query_terms", 6), ("title_match_phrases", 15)):
        a = c[field]
        if not isinstance(a, list) or not 1 <= len(a) <= length or any(
            not isinstance(t, str) or not 3 <= len(t) <= 90 or
            any(ord(ch) < 32 for ch in t) for t in a
        ):
            raise ValueError("Bad query terms")
    if (type(c["per_page"]) is not int or not 1 <= c["per_page"] <= 10 or
        type(c["max_candidates"]) is not int or not 1 <= c["max_candidates"] <= 50):
        raise ValueError("Unbounded result count")
    return c


def plain(s):
    s = unicodedata.normalize("NFKD", s).lower().replace("đ", "d")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(re.findall("[a-z0-9]+", s))


def doi_clean(v):
    if not isinstance(v, str):
        return None
    v = v.strip()
    if v.lower().startswith("https://doi.org/"):
        v = v[16:]
    return v.lower() if len(v) <= 200 and DOI.fullmatch(v) else None


def clean_title(v):
    if isinstance(v, list):
        v = next((s for s in v if isinstance(s, str) and s.strip()), "")
    if not isinstance(v, str):
        return ""
    v = re.sub(r"<[^>]*>", "", " ".join(v.split()))
    return "".join(ch for ch in v if ch.isprintable() and ch not in "<>")[:240].strip()


def normalize(item, provider, terms):
    if not isinstance(item, dict):
        return None
    title = clean_title(item.get("title") if provider == "crossref" else item.get("display_name"))
    hits = [x for x in terms if (" " + plain(x) + " ") in (" " + plain(title) + " ")]
    if not hits:
        return None
    doi = doi_clean(item.get("DOI") if provider == "crossref" else item.get("doi"))
    if doi:
        key = "doi:" + doi
        link = "https://doi.org/" + quote(doi, safe="/()-.;:_")
    else:
        if provider == "crossref":
            return None
        link = item.get("id")
        if not isinstance(link, str) or not re.fullmatch(r"https://openalex\.org/W[0-9]{3,20}", link):
            return None
        key = "openalex:" + link.rsplit("/", 1)[-1]
    year = None
    if provider == "openalex":
        year = item.get("publication_year")
    else:
        for field in ("published", "published-print", "published-online", "issued"):
            part = item.get(field, {})
            try:
                year = part["date-parts"][0][0]
            except (KeyError, IndexError, TypeError):
                continue
            if type(year) is int:
                break
    year = year if type(year) is int and 1800 <= year <= 2100 else None
    return {
        "candidate_id": hashlib.sha256(key.encode()).hexdigest()[:20],
        "title": title, "year": year, "doi": doi, "source": provider,
        "url": link, "matched_terms": hits,
        "review_status": "pending_review", "rights_status": "unverified",
        "performance_status": "pending", "approved_for_publication": False,
    }


def load_api(url, *, auth=None, opener=urlopen, sleep=time.sleep):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or (parsed.netloc, parsed.path) not in ENDPOINTS:
        raise ValueError("Disallowed API URL")
    headers = {"Accept": "application/json",
               "User-Agent": "HaiDatVongCoV3.6 (+https://github.com/Form997/Vong-co)"}
    if auth:
        headers["Authorization"] = "Bearer " + auth
    for retry in range(3):
        try:
            with opener(Request(url, headers=headers), timeout=18) as f:
                data = f.read(1_500_001)
            if len(data) > 1_500_000:
                raise ValueError("Oversized API reply")
            return json.loads(data.decode("utf-8"))
        except HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or retry == 2:
                raise RuntimeError("HTTP " + str(e.code)) from None
        except (URLError, TimeoutError):
            if retry == 2:
                raise RuntimeError("Network error") from None
        sleep(2 ** retry)
    raise RuntimeError("No response")


def scan(config, *, requester=load_api, openalex_key=None, at=None):
    found, errors = {}, []
    successful = 0
    counts = {"crossref": 0, "openalex": 0, "openalex_skipped": not bool(openalex_key)}
    for term in config["query_terms"]:
        url = "https://api.crossref.org/works?" + urlencode({
            "query.bibliographic": term, "rows": config["per_page"],
            "select": "DOI,title,published,published-print,published-online,issued"})
        try:
            records = requester(url)["message"]["items"]
            if not isinstance(records, list):
                raise ValueError("Crossref items malformed")
            successful += 1
            counts["crossref"] += 1
            for rec in records:
                obj = normalize(rec, "crossref", config["title_match_phrases"])
                if obj:
                    found.setdefault(obj["candidate_id"], obj)
        except (ValueError, RuntimeError, KeyError, TypeError):
            errors.append("crossref_error")
    if openalex_key:
        for term in config["query_terms"][:2]:
            url = "https://api.openalex.org/works?" + urlencode({
                "search": term, "per_page": config["per_page"]})
            try:
                records = requester(url, auth=openalex_key)["results"]
                if not isinstance(records, list):
                    raise ValueError("OpenAlex results malformed")
                successful += 1
                counts["openalex"] += 1
                for rec in records:
                    obj = normalize(rec, "openalex", config["title_match_phrases"])
                    if obj:
                        found.setdefault(obj["candidate_id"], obj)
            except (ValueError, RuntimeError, KeyError, TypeError):
                errors.append("openalex_error")
    matches = sorted(found.values(), key=lambda r: (r["year"] or 0, r["candidate_id"]), reverse=True)
    matches = matches[:config["max_candidates"]]
    date = at or datetime.now(timezone.utc)
    return {
        "schema_version": config["schema_version"],
        "collected_at": date.astimezone(timezone.utc).isoformat(),
        "status": "failed" if successful == 0 else "partial" if errors else "complete",
        "human_review_required": True, "auto_publish": False,
        "candidate_count": len(matches), "requests_ok": counts,
        "errors": errors, "candidates": matches,
    }


def render_issue(result):
    body = ("# V3.6 — Metadata nguồn mới chờ kiểm\n\n"
            "**CHƯA XÁC MINH.** DOI và nhan đề không chứng minh câu, nhịp, "
            "bản ký âm, bản thu hoặc quyền sử dụng. **0/20 nghiệm thu diễn xướng.**\n\n"
            "Thu thập UTC: " + result["collected_at"] + "\n\n"
            "Hồ sơ: " + str(result["candidate_count"]) + "\n\n")
    if result["status"] != "complete":
        body += "**Quét chưa đầy đủ:** " + result["status"] + "\n\n"
    for row in result["candidates"]:
        title = row["title"]
        for ch in ("[", "]", "*", "_", "|", "!", chr(96), "\\"):
            title = title.replace(ch, " ")
        body += "- **" + title + "** (" + str(row["year"] or "?") + ") " + row["url"] + \
                "\n  - " + row["candidate_id"] + " · " + row["source"] + " · chờ duyệt\n"
    return body + ("\n**Chỉ cập nhật các hồ sơ bài qua PR do người kiểm định phê duyệt.**\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="v3_6_scan.json")
    p.add_argument("--issue-body", default="v3_6_issue.md")
    args = p.parse_args()
    report = scan(read_config(), openalex_key=os.environ.get("OPENALEX_API_KEY") or None)
    for pathname, content in (
        (args.out, json.dumps(report, ensure_ascii=False, indent=2) + "\n"),
        (args.issue_body, render_issue(report)),
    ):
        path = Path(pathname)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(json.dumps({"status": report["status"], "candidates": report["candidate_count"],
                      "requests_ok": report["requests_ok"]}, ensure_ascii=False))
    return 2 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
