<h1 align="center">HAI ĐẤT</h1>

<p align="center"><strong>THE 20 FOUNDATIONAL COMPOSITIONS OF SOUTHERN VIETNAM'S ĐỜN CA TÀI TỬ</strong></p>

<p align="center">Preserving a living musical tradition through traceable evidence, respectful treatment of variants,<br>and responsible access for learners, researchers and AI developers.</p>

<p align="center">
  <a href="README.md">Tiếng Việt</a> ·
  <a href="#start-here">Get started</a> ·
  <a href="web/v3/README.md">V3.0 alpha</a> ·
  <a href="#browse-the-20-compositions">20 compositions</a> ·
  <a href="#research-versions">Version history</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

<p align="center">
  <a href="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v3.yml"><img alt="GitHub Actions V3 test status" src="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v3.yml/badge.svg?branch=v3-development"></a>
  <a href="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml"><img alt="GitHub Actions test status for V2" src="https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml/badge.svg?branch=v2-development"></a>
  <img alt="20 of 20 V2 source-review dossiers opened" src="https://img.shields.io/badge/V2%20source%20reviews-20%2F20-28776D">
  <img alt="Zero compositions have passed performance-level validation" src="https://img.shields.io/badge/Performance%20approved-0%2F20-8B6F47">
</p>

> [!IMPORTANT]
> **Research status — 28 October 2026.** **20/20** composition dossiers have a V2 **source-review record**; **0/20** compositions have passed performance-level validation. This is a developing, source-grounded research project, **not** a certified score/audio collection or a license-cleared AI training dataset. Green software-test badges do not mean musical validation.

> [!NOTE]
> **V3.0-alpha began on 28 October 2026.** [20-piece catalog with 30 documented systems/variants](data/v3/catalog.json), [JSON Schema](data/v3/schema.json), [Vietnamese search interface](web/v3/README.md), and [successful V3 GitHub Actions tests](https://github.com/Form997/Vong-co/actions/runs/40654050406) (**39 tests passed, 170 internal links checked**, including a real local HTTP smoke test). The web viewer is source code **not yet deployed on GitHub Pages**. This is an **alpha research preview**, not a music performance certification.

---

### V3 browser-tested preview — deployment requires owner opt-in

**42 Python tests pass**; [real Chromium acceptance checks pass](https://github.com/Form997/Vong-co/actions/runs/40675487073), including diacritic-insensitive search, the 6/7/3/4 family filters, distinct Phụng Hoàng/Phụng Cầu, deep links and a 390px mobile viewport.

**Pages artifact:** successfully built with **7 allowlisted files**. **Live deployment:** **not enabled** — the Deploy job is `Skipped` until the repository owner approves and configures GitHub Pages. [Safe publishing instructions (Vietnamese)](docs/v3-github-pages.md) · [V3 browser preview guide](web/v3/README.md).

## Start here

| Your goal | The best entry point |
|---|---|
| **Try the V3 catalog viewer** | [How to run the website](web/v3/README.md) · [View HTML source](web/v3/index.html) |
| **Explore the tradition** | [20 composition index](#browse-the-20-compositions) |
| **Learn and perform** | [Per-composition research folders](ban-to/) · [First-piece practice notes (Vietnamese)](docs/01-huong-dan-don-va-ca.md) |
| **Investigate scores and variants** | [V2 findings and unresolved discrepancies](docs/tong-hop-phat-hien-v2.md) · [Evidence registry](docs/nguon-tham-khao.md) |
| **Build research/AI software** | [Read-only MCP prototype (separate branch)](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp) · [Acceptance criteria](docs/ke-hoach-v2.md) |
| **Report issues or contribute** | [Contribution guide](CONTRIBUTING.md) · [Create a documented issue](https://github.com/Form997/Vong-co/issues/new/choose) |

### Why a source-first research corpus?

The same composition can circulate in distinct **short/full variants**, rhythmic conventions, phrase counts, melodic ornaments and separately authored lyrics. Flattening them into a single “standard” answer erases their provenance and misleads both learners and language models.

HAI ĐẤT records **what a source actually supports**, **which page/phrase was checked**, **where accounts disagree**, and **what still requires practitioner review**. When the evidence is insufficient, the proper answer is **“not verified”**.

UNESCO inscribed **the art of Đờn ca tài tử** in 2013 ([decision 8.COM 8.31](https://ich.unesco.org/en/decisions/8.COM/8.31)); this is **not** an endorsement, grant, partnership or certification of this GitHub project.

## What is available?

| Area | Current evidence-based status |
|---|---|
| **Research dossiers** | 20 composition folders and 20 V2 source-review minutes |
| **V3 structured catalog** | 20 pieces, **30 source-specific variants**, schema and offline validator; [JSON](data/v3/catalog.json) |
| **V3 Vietnamese browser** | Search, 4-family filtering, provenance links; [preview instructions](web/v3/README.md) — not yet deployed as a public Pages site |
| **Phrase and variant records** | Available per composition, with different verification levels; not all are complete musical transcriptions |
| **Bibliography** | [Numbered source entries through REF-68](docs/nguon-tham-khao.md), including documented limitations; **not** 68 independently verified primary sources |
| **Code validation** | Working [GitHub Actions workflow](https://github.com/Form997/Vong-co/actions/workflows/kiem-thu-v2.yml) for Python and research-folder structure |
| **MCP experiment** | [Read-only prototype on another branch](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp); not a stable, supported commercial API |
| **Performance acceptance** | **0/20** approved; score/recording alignment, phrasing, song lang, instrument technique and rights remain pending |

## Browse the 20 compositions

The project groups the 20 pieces into **Sáu Bắc (6)**, **Bảy Lễ (7)**, **Ba Nam (3)** and **Bốn Oán (4)**. The numbering is an internal research index, not a claim that every tradition uses the same sequence.

| # | Family | Composition / research folder | V2 source review |
|---:|---|---|---|
| 01 | Sáu Bắc | [Lưu Thủy Trường](ban-to/01-luu-thuy-truong/README.md) | [Review](ban-to/01-luu-thuy-truong/v2-bien-ban-nghiem-thu.md) |
| 02 | Sáu Bắc | [Phú Lục Chấn](ban-to/02-phu-luc-chan/README.md) | [Review](ban-to/02-phu-luc-chan/v2-bien-ban-nghiem-thu.md) |
| 03 | Sáu Bắc | [Bình Bán Chấn](ban-to/03-binh-ban-chan/README.md) | [Review](ban-to/03-binh-ban-chan/v2-bien-ban-nghiem-thu.md) |
| 04 | Sáu Bắc | [Cổ Bản (Vắn / Trường)](ban-to/04-co-ban-van/README.md) | [Review](ban-to/04-co-ban-van/v2-bien-ban-nghiem-thu.md) |
| 05 | Sáu Bắc | [Xuân Tình Chấn](ban-to/05-xuan-tinh-chan/README.md) | [Review](ban-to/05-xuan-tinh-chan/v2-bien-ban-nghiem-thu.md) |
| 06 | Sáu Bắc | [Tây Thi (Vắn / Trường)](ban-to/06-tay-thi-van/README.md) | [Review](ban-to/06-tay-thi-van/v2-bien-ban-nghiem-thu.md) |
| 07 | Bảy Lễ | [Xàng Xê](ban-to/07-xang-xe/README.md) | [Review](ban-to/07-xang-xe/v2-bien-ban-nghiem-thu.md) |
| 08 | Bảy Lễ | [Ngũ Đối Thượng](ban-to/08-ngu-doi-thuong/README.md) | [Review](ban-to/08-ngu-doi-thuong/v2-bien-ban-nghiem-thu.md) |
| 09 | Bảy Lễ | [Ngũ Đối Hạ](ban-to/09-ngu-doi-ha/README.md) | [Review](ban-to/09-ngu-doi-ha/v2-bien-ban-nghiem-thu.md) |
| 10 | Bảy Lễ | [Long Đăng](ban-to/10-long-dang/README.md) | [Review](ban-to/10-long-dang/v2-bien-ban-nghiem-thu.md) |
| 11 | Bảy Lễ | [Long Ngâm](ban-to/11-long-ngam/README.md) | [Review](ban-to/11-long-ngam/v2-bien-ban-nghiem-thu.md) |
| 12 | Bảy Lễ | [Vạn Giá](ban-to/12-van-gia/README.md) | [Review](ban-to/12-van-gia/v2-bien-ban-nghiem-thu.md) |
| 13 | Bảy Lễ | [Tiểu Khúc](ban-to/13-tieu-khuc/README.md) | [Review](ban-to/13-tieu-khuc/v2-bien-ban-nghiem-thu.md) |
| 14 | Ba Nam | [Nam Xuân](ban-to/14-nam-xuan/README.md) | [Review](ban-to/14-nam-xuan/v2-bien-ban-nghiem-thu.md) |
| 15 | Ba Nam | [Nam Ai](ban-to/15-nam-ai/README.md) | [Review](ban-to/15-nam-ai/v2-bien-ban-nghiem-thu.md) |
| 16 | Ba Nam | [Đảo Ngũ Cung](ban-to/16-dao-ngu-cung/README.md) | [Review](ban-to/16-dao-ngu-cung/v2-bien-ban-nghiem-thu.md) |
| 17 | Bốn Oán | [Tứ Đại Oán](ban-to/17-tu-dai-oan/README.md) | [Review](ban-to/17-tu-dai-oan/v2-bien-ban-nghiem-thu.md) |
| 18 | Bốn Oán | [Phụng Hoàng](ban-to/18-phung-hoang/README.md) | [Review](ban-to/18-phung-hoang/v2-bien-ban-nghiem-thu.md) |
| 19 | Bốn Oán | [Giang Nam Cửu Khúc](ban-to/19-giang-nam/README.md) | [Review](ban-to/19-giang-nam/v2-bien-ban-nghiem-thu.md) |
| 20 | Bốn Oán | [Phụng Cầu Hoàng Duyên](ban-to/20-phung-cau/README.md) | [Review](ban-to/20-phung-cau/v2-bien-ban-nghiem-thu.md) |

**Illustrative differences:** Cổ Bản has **34/68-phrase** systems; Tây Thi has **26/52-phrase** systems; Phụng Hoàng (18) and Phụng Cầu (20) are different pieces. For detailed evidence and unresolved anomalies, consult the [V2 research findings (Vietnamese)](docs/tong-hop-phat-hien-v2.md).

## Research versions

| Version | Earliest documented Git milestone | Contribution | Fixed snapshot size |
|---|---|---|---:|
| **V1 — The evidence base** | **12 October 2026** | Twenty folders, sources, variants, auditing notes | **397.63 KiB** |
| **V2 — Tracing each phrase** | **19 October 2026** (V2-labeled commit); formal review framework **27 October** | Twenty source-review minutes, phrase/page ledgers, documented discrepancies; **no performance certifications** | **942.96 KiB** |
| **V3.0-alpha — Evidence-aware browsing** | **28 October 2026** | 20-piece JSON catalog, 30 variant records, automated checks and Vietnamese static viewer | **1,055.84 KiB** |

V1 measures **407,176 bytes / 64 files** at [`f6537c8`](https://github.com/Form997/Vong-co/tree/f6537c83878bca079752dbdd4baec5b1164a1ab4); V2 measures **965,588 bytes / 112 files** at [`4d919d2`](https://github.com/Form997/Vong-co/tree/4d919d2ebdf63df61c8fd723f850830e7eaf5968). V3 alpha measures **1,081,181 bytes / 133 files** at [`d7d9765`](https://github.com/Form997/Vong-co/tree/d7d976561215be5c28e1b10db7ddc868037ed386). These are **uncompressed Git blob sizes at pinned commits**, not ZIP or permanently fixed working-branch sizes.

[**Full version ledger and future-version template (Vietnamese)**](docs/nhat-ky-phien-ban.md) · [Reproducible Python size reporter](scripts/thong-ke-dung-luong.py)

## For researchers and AI developers

The [experimental MCP connector](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp) is maintained on a **separate research branch**. Systems integrating this corpus should preserve **source, page, variant ID, verification status and reuse rights**, and decline unsupported claims.

**V3.0-alpha now includes structured JSON and a working static HTML codebase with a successful CI run; it is not a deployed public website or stable release.** Further planned work: page/phrase-level evidence, permission-cleared audio comparison and responsibly tested AI/MCP integration. [V3 scope and limits](docs/v3-khoi-dong.md).

## Sources, rights and collaboration

[Source registry](docs/nguon-tham-khao.md) · [V2 methodology](docs/ke-hoach-v2.md) · [Contribution guide](CONTRIBUTING.md) · [Open an evidence-based issue](https://github.com/Form997/Vong-co/issues/new/choose)

**A public repository is not a reuse license.** Copyright in individual scores, lyrics, recordings, images, databases, and code must be assessed separately. Do not upload third-party source material or imply institutional endorsement without authorization. **There is no confirmed blanket license for this entire corpus.**

<p align="center"><strong>HAI ĐẤT · Preserve the music. Preserve its provenance.</strong></p>

<p align="center"><sub>Research-first Southern Vietnamese musical heritage · Updated 28 October 2026 · <a href="https://github.com/Form997/Vong-co/tree/v3-development">V3 alpha branch</a></sub></p>
