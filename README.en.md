# HAI ĐẤT — 20 Foundational Đờn Ca Tài Tử Compositions

**Preserving a living musical tradition through source-grounded research, transparent variants, and responsible AI access.**

[**Đọc README tiếng Việt**](README.md) · [**Source registry (33 documented source entries)**](docs/nguon-tham-khao.md) · [**AI/MCP prototype**](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp)

> **Research status, 28 October 2026:** 20/20 research folders indexed; 14/20 compositions have a V2 **source-review record**; **0/20** have passed independent performance-level validation. **This is an evolving research corpus, not a finished, licensed, or musicologist-certified transcription/audio dataset.**

## What is this project?

HAI ĐẤT collects research dossiers and source links about the **20 foundational pieces (20 bài bản Tổ)** of **Đờn ca tài tử**, a chamber-music and song tradition of Southern Viet Nam.

[UNESCO inscribed the *art of Đờn ca tài tử* in 2013](https://ich.unesco.org/en/decisions/8.COM/8.31). This refers to the **living heritage**, **not an endorsement, certification, or sponsorship of this GitHub project**.

The repository's legacy name `Vong-co` should not be mistaken for a complete repository of vọng cổ or cải lương songs: **the project's current scope is the 20 Đờn ca tài tử compositions**.

## Why a source-first approach?

A single composition may circulate as different versions, with different phrase counts, metre conventions, notation, melodic ornamentation, and independently authored lyric sets. Traditional performance also depends on expert practice, personal interpretation, and context.

A search engine or a language model can easily flatten such evidence into a single, wrongly confident answer. This project aims to help researchers and developers **trace each claim back to a named source** and distinguish:

- a source document **located** versus a passage **checked**;
- a numbered phrase **indexed** versus a melody/rhythm **verified against a recording**;
- a version **described** versus a performance **validated by qualified practitioners**;
- an externally available document versus a document **licensed for reuse**.

## Corpus and status

| Family | Composition count | Directories |
|---|---:|---|
| **Sáu Bắc** | 6 | [01–06](docs/20-ban-to.md) |
| **Bảy Lễ** | 7 | [07–13](docs/20-ban-to.md) |
| **Ba Nam** | 3 | [14–16](docs/20-ban-to.md) |
| **Bốn Oán** | 4 | [17–20](docs/20-ban-to.md) |
| **Total** | **20** | [Full index and per-composition folders](docs/20-ban-to.md) |

Two research issues already flagged in the V2 documents illustrate why version management matters:

- **Cổ Bản:** a 68-phrase **Trường** version must not be conflated with a 34-phrase **Vắn** version.
- **Tây Thi:** a 52-phrase **Trường** version and a 26-phrase **Vắn** version are managed separately. An online “34 phrases” heading does not match the corresponding 26 numbered phrases and is treated as an unresolved editorial error, not as evidence of a third complete score.
- **Ngũ Đối Thượng:** a source-verified 61-phrase score (Nhị Tấn, Vol. III, pp. 226–233) and a **60-phrase variant described as omitting source phrase 53**. The 60-phrase crosswalk is preliminary, **not yet independently audio-validated**. [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/08-ngu-doi-thuong/v2-bien-ban-nghiem-thu.md).
- **Ngũ Đối Hạ:** a newly located printed **38-phrase score** (Nhị Tấn, Vol. III, pp. 234/236) and **38 numbered lyric phrases** for *Kim, Kiều hoa viên ngộ* (pp. 235/237; book credits Cao Hoài Sang, 1940). Five printed sections; an academic study also mentions a three-section grouping. **Performance status remains unverified**. [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/09-ngu-doi-ha/v2-bien-ban-nghiem-thu.md).
- **Long Đăng:** a complete **40-phrase score** was found in Nhị Tấn, Vol. III (printed pp.238, 240 and **242**), with separately numbered lyrics *Kiều vãng Trọng hiên* (pp.239, 241, **243**; attributed in print to Cao Hoài Sang, 1940). **Phrases 39–40 are at the start of pages 242/243, before the following *Long Ngâm* section.** Vol. V pp.501–502 contains a **different 40-phrase lyric set**, *Bàng Quyên xuống núi*, attributed to Thái Thụy Phong. [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/10-long-dang/v2-bien-ban-nghiem-thu.md).
- **Long Ngâm:** the following section of Nhị Tấn, Vol. III contains a **33-phrase score** (pp.242/244) and **33 numbered phrases of lyrics** *Tống Trọng qui tang* (pp.243/245; credited in print to Cao Hoài Sang, 1940). The first pages also contain the final two phrases of Long Đăng, while Vạn Giá begins after phrase 33. Three sections **8–11–14**; opening pitch terminology differs between an academic discussion (**Xư**) and the printed first notation (**Líu**), and remains subject to specialist review. **No performance phrases have been validated.** [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/11-long-ngam/v2-bien-ban-nghiem-thu.md).
- **Vạn Giá:** Nhị Tấn, Vol. III has a **47-phrase score** on printed pp.**244/246/248/250**, and 47 indexed lyric phrases *Biệt mãi thanh lâu* on pp.**245/247/249/251** (the printed book attributes the lyric to **Cao Hoài Sang, 1940**). The **last six phrases 42–47** precede the next work *Tiểu Khúc*; do not truncate the score at p.249. Five sections **8–6–10–14–9**. The separate 47-phrase lyric *Nhẫn nhịn*, credited by an online lyrics site to Hoài Như, remains unverified for music alignment and rights. **No performance certification.** [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/12-van-gia/v2-bien-ban-nghiem-thu.md).
- **Tiểu Khúc:** the last of the seven Lễ pieces has a **29-phrase score in four sections (10–7–8–4)** in Nhị Tấn, Vol. III, pp.**250/252**; 29 lyric phrases *Dữ Thúc thành hôn*, credited in print to **Cao Hoài Sang (1940)**, appear on pp.**251/253**. A **distinct** 29-phrase lyric *Bàng Quyên chặt chơn Tôn Tẫn* is attributed to **Thái Thụy Phong** in Vol. V pp.**503–504**; VOH's 2022 educational program uses another lyric *Anh hùng Nguyễn Trung Trực* (attributed to **Thiếu Bá**). **Do not merge the versions or infer that any is performance-certified.** [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/13-tieu-khuc/v2-bien-ban-nghiem-thu.md).
- **Nam Xuân:** the first of the three Nam pieces has a printed **68-phrase score** (Nhị Tấn, Vol. III, pp.**260/262/264/266/268**) and **68 numbered lyric phrases of *Tích Thúy Kiều*** (pp.**261/263/265/267/269**, attributed in the book to **Phan Trúc Quân, also called Sáu Lục, before 1900**). The print labels eight 8-phrase sections followed by **Section IX containing phrases 65–68**; do not conflate these four phrases with the separately numbered transition into Nam Ai. An online transcription by Văn Dần differs at **phrases 38 and 42**. Vol. IV, pp.395–397 has a **different *Tô Huệ – Chức Cẩm Hồi Văn* performance lyric** with 48 numbered Nam Xuân phrases plus an instruction to return to the first 20 before Nam Ai; this is not an independently documented 68-phrase continuous lyric for the same piece. **Performance review still pending.** [See V2 review](https://github.com/Form997/Vong-co/blob/v2-development/ban-to/14-nam-xuan/v2-bien-ban-nghiem-thu.md).

**The seven Lễ pieces (07–13) now all have a V2 source-review dossier; none has passed specialist performance-level certification.**

[**V2 review policy**](https://github.com/Form997/Vong-co/blob/v2-development/docs/ke-hoach-v2.md) · [**Source audit records for pieces 01–14**](https://github.com/Form997/Vong-co/tree/v2-development/ban-to) · [**V1 audit**](docs/kiem-toan-v1-20-ban.md)

## For AI researchers, heritage institutions, and technology companies

Use cases to **evaluate**, subject to source reliability, permission and legal review:

- Retrieval-augmented generation (RAG) grounded in bibliographic URLs and review findings.
- Music-education discovery interfaces where unverified passages are visibly marked.
- Cross-source comparison of piece names, versions, phrase counts, and lyric authorship.
- Cultural-heritage catalogs with explicit provenance and uncertainty fields.
- Vietnamese terminology retrieval and human-in-the-loop musicological quality control.

**Experimental read-only MCP:** [code and installation notes](https://github.com/Form997/Vong-co/tree/feature/mcp-readonly-v1/integrations/vong-co-mcp).

The prototype provides the following tools:

```text
list_ban_to()
search_ban_to(query="Tay Thi")
get_ban_to(bai_so=6, version="v1")
get_nghiem_thu(bai_so=6)
get_di_ban(bai_so=6)
get_nguon(bai_so=6)
get_quy_che_v2()
```

[**12/12 GitHub Actions test cases passed on 27 October 2026**](https://github.com/Form997/Vong-co/actions/runs/40479366376), including initial MCP-protocol checks and a small number of live reads against public V1/V2 sources.

**Not yet offered:** a publicly hosted HTTPS MCP endpoint, published ChatGPT Plugin, production API, commercial service/SLA, verified full-length audio library, or permission for AI-model training. The application integrating this prototype is responsible for access controls, testing, version pinning, source citation, and licensing review.

### Branch and version discipline

| Git ref | Function |
|---|---|
| `main` | Public documentation and navigation |
| `v1-frozen` | Historical V1 research snapshot; preservation is a workflow convention, not proof of branch-protection settings |
| `v2-development` | Ongoing source comparison and acceptance records |
| `feature/mcp-readonly-v1` | Independent proof-of-concept connector |

For stable third-party adoption, the future production connector should **pin a reviewed release tag or commit**, not automatically serve every newly edited V2 document as verified.

## References you can actually follow

The [**full bibliography and provenance register**](docs/nguon-tham-khao.md) lists 13 sources used by the project, with publisher/author, date, research purpose, URLs, access status, and limitations.

Selected primary and scholarly references:

1. [UNESCO — inscription decision 8.COM 8.31 (2013)](https://ich.unesco.org/en/decisions/8.COM/8.31).
2. [Vietnamese Institute for Musicology (VIM) / ICHCAP — *Đờn ca tài tử, a chamber music of Southern Vietnam* (2015)](https://archive.unesco-ichcap.org/eng/ek/sub16/pdf_file/handbook_cd8.pdf).
3. [Vietnamese Institute for Musicology — *Twenty principal pieces of Đờn ca tài tử*](https://vienamnhac.vn/Media/Default/Download/20%20ban%20to%20ch.pdf) — **source URL returned HTTP 502 during a direct-access check on 27 October 2026**; search indexing is not an independent page-level verification.
4. [Nhị Tấn — *Nhạc Tài Tử Nam Bộ*, Vol. I (1997), digitized copy](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%201%20-%20Nhi%20Tan.pdf) and [Vol. II](https://www.namkyluctinh.org/eBooks/AmNhac/Nhac%20Tai%20Tu%20Nam%20Bo%202%20-%20Nhi%20Tan.pdf).
5. [Văn Dần's blog — historical survey of Đờn ca tài tử pieces (2013; on-page author: Tấn Nhì)](https://nhacsivandan.wordpress.com/2013/11/03/luoc-khao-hinh-thanh-bai-ban-don-ca-tai-tu-nam-bo/).
6. [Bùi Thiên Hoàng Quân — *The structure of seven ceremonial compositions in southern Tài tử music* (2017; third-party copy of journal article)](https://tailieuvn.net/cau-truc-bay-ban-le-nhac-tai-tu-nam-bo-8526/).
7. [ICH Links — Lưu thủy trường audio metadata; master Nguyễn Vĩnh Bảo, 1977](https://www.ichlinks.com/archive/materials/audiosV.do?ichDataUid=16097184005120000346&nation=VN).

These are cited as independent sources **for the facts they support**. Institutions listed here do not certify the repository. Online scores, transcriptions, lyrics, and audio are **not redistributed** by this project without verified reuse rights.

## Rights and collaboration

**Public visibility is not a license.** As checked on 27 October 2026, the GitHub repository has **no confirmed LICENSE file**. Researchers and companies must determine permissions for code, texts, recordings, performances, reproduction, distribution, training, and commercial use **separately**. Source citations alone confer none of those rights.

To report an error or propose a documented comparison, [open a GitHub issue](https://github.com/Form997/Vong-co/issues) with the **piece number, version identifier, phrase number, source URL/page, evidence, and proposed correction**. Claims without adequate support should remain explicitly **unverified**.

**HAI ĐẤT aims to make Vietnamese musical heritage easier to explore without obscuring variation, authorship, or the knowledge of its practitioners.**
