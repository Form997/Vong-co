"""Read-only source gateway for the Vong-co 20-song corpus.

Only fixed, vetted repository paths are retrieved. Source content remains
untrusted research material, not instructions to an AI assistant.
"""
from __future__ import annotations

import re
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Callable

REPO = "Form997/Vong-co"
RAW_ROOT = "https://raw.githubusercontent.com/Form997/Vong-co"
WEB_ROOT = "https://github.com/Form997/Vong-co/blob"
BRANCHES = {"v1": "v1-frozen", "v2": "v2-development"}
MAX_BYTES = 180_000
MAX_CHARS = 22_000

ENTRIES = (
    ("luu-thuy-truong", "Lưu Thủy Trường"),
    ("phu-luc-chan", "Phú Lục Chấn"),
    ("binh-ban-chan", "Bình Bán Chấn"),
    ("co-ban-van", "Cổ Bản (Vắn / Trường)"),
    ("xuan-tinh-chan", "Xuân Tình Chấn"),
    ("tay-thi-van", "Tây Thi (Vắn / Trường)"),
    ("xang-xe", "Xàng Xê"),
    ("ngu-doi-thuong", "Ngũ Đối Thượng"),
    ("ngu-doi-ha", "Ngũ Đối Hạ"),
    ("long-dang", "Long Đăng"),
    ("long-ngam", "Long Ngâm"),
    ("van-gia", "Vạn Giá"),
    ("tieu-khuc", "Tiểu Khúc"),
    ("nam-xuan", "Nam Xuân"),
    ("nam-ai", "Nam Ai"),
    ("dao-ngu-cung", "Đảo Ngũ Cung"),
    ("tu-dai-oan", "Tứ Đại Oán"),
    ("phung-hoang", "Phụng Hoàng"),
    ("giang-nam", "Giang Nam"),
    ("phung-cau", "Phụng Cầu"),
)


@dataclass(frozen=True)
class Work:
    number: int
    name: str
    slug: str
    group: str

    @property
    def folder(self) -> str:
        return f"ban-to/{self.number:02d}-{self.slug}"

    def descriptor(self) -> dict:
        return {
            "number": self.number,
            "name": self.name,
            "group": self.group,
            "folder": self.folder,
            "v1_url": f"{WEB_ROOT}/v1-frozen/{self.folder}/README.md",
        }


WORKS = tuple(
    Work(
        i,
        name,
        slug,
        "Sáu Bắc" if i <= 6 else "Bảy Lễ" if i <= 13
        else "Ba Nam" if i <= 16 else "Bốn Oán",
    )
    for i, (slug, name) in enumerate(ENTRIES, 1)
)


class SourceNotFound(Exception):
    """A requested approved source path has no file on GitHub."""


class SourceAccessError(Exception):
    """GitHub was unavailable or returned an unexpected response."""


def _valid_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return (
        isinstance(path, str)
        and not path.startswith("/")
        and ".." not in parsed.parts
        and not "\\" in path
        and path.endswith(".md")
        and len(path) <= 160
        and re.fullmatch(r"[a-zA-Z0-9/_-]+\.md", path) is not None
        and (path.startswith("docs/") or path.startswith("ban-to/"))
    )


def _download(branch: str, path: str) -> str:
    if branch not in BRANCHES.values() or not _valid_path(path):
        raise ValueError("Unsupported source reference")
    url = f"{RAW_ROOT}/{branch}/{path}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "VongCo-MCP-readonly/0.1", "Accept": "text/plain"},
    )
    try:
        with urllib.request.urlopen(req, timeout=9) as response:
            body = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise SourceNotFound(path) from exc
        raise SourceAccessError(f"Source HTTP error: {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SourceAccessError("Cannot currently reach the GitHub source") from exc
    if len(body) > MAX_BYTES:
        raise SourceAccessError("Source document exceeds safety limit")
    return body.decode("utf-8", errors="replace")


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower()).replace("đ", "d")
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _work(number: int) -> Work:
    if type(number) is not int or not 1 <= number <= 20:
        raise ValueError("bai_so must be an integer from 1 to 20")
    return WORKS[number - 1]


class Catalog:
    def __init__(self, fetch_text: Callable[[str, str], str] | None = None):
        self.fetch_text = fetch_text or _download

    def _read(self, branch: str, path: str) -> str:
        if branch not in BRANCHES.values() or not _valid_path(path):
            raise ValueError("Disallowed repository path or branch")
        return self.fetch_text(branch, path)

    @staticmethod
    def _reference(branch: str, path: str) -> str:
        return f"{WEB_ROOT}/{branch}/{path}"

    def list_ban_to(self) -> dict:
        return {
            "repository": REPO,
            "total": len(WORKS),
            "works": [w.descriptor() for w in WORKS],
            "notice": "20 hồ sơ V1, không đồng nghĩa 20 bài đã đạt nghiệm thu V2.",
        }

    def search_ban_to(self, query: str) -> dict:
        if not isinstance(query, str) or not 1 <= len(query.strip()) <= 100:
            raise ValueError("query must have 1 to 100 characters")
        needle = _fold(query.strip())
        matches = [
            w.descriptor() for w in WORKS
            if needle in _fold(f"{w.number:02d} {w.name} {w.group} {w.slug}")
        ]
        return {
            "query": query,
            "match_count": len(matches),
            "works": matches,
            "scope": "Tên bài, tên thư mục và nhóm; KHÔNG tìm toàn văn.",
        }

    def get_ban_to(self, bai_so: int, version: str = "v1") -> dict:
        w = _work(bai_so)
        if version not in BRANCHES:
            raise ValueError("version must be v1 or v2")
        branch = BRANCHES[version]
        path = f"{w.folder}/README.md"
        content = self._read(branch, path)
        return {
            "work": w.descriptor(),
            "version": version,
            "source_branch": branch,
            "source_url": self._reference(branch, path),
            "content": content[:MAX_CHARS],
            "truncated": len(content) > MAX_CHARS,
            "disclaimer": "Hồ sơ nghiên cứu, không phải chứng nhận nghệ nhân.",
        }

    def get_nghiem_thu(self, bai_so: int) -> dict:
        w = _work(bai_so)
        branch = BRANCHES["v2"]
        path = f"{w.folder}/v2-bien-ban-nghiem-thu.md"
        url = self._reference(branch, path)
        try:
            content = self._read(branch, path)
        except SourceNotFound:
            return {
                "work": w.descriptor(),
                "status": "CHUA_CO_BIEN_BAN_V2",
                "accepted": False,
                "source_url": url,
                "notice": "Không có biên bản không đồng nghĩa bài sai hoặc bài đạt.",
            }
        upper = content.upper()
        if "CHỜ NGHIỆM THU" in upper:
            verdict = "CHO_NGHIEM_THU"
        elif "KHÔNG ĐẠT" in upper:
            verdict = "CAN_KIEM_TRA_PHAN_QUYET"
        else:
            verdict = "CHUA_XAC_MINH_PHAN_QUYET"
        return {
            "work": w.descriptor(),
            "status": verdict,
            "accepted": False,  # Never automatically award musical certification.
            "source_branch": branch,
            "source_url": url,
            "report": content[:MAX_CHARS],
            "truncated": len(content) > MAX_CHARS,
            "notice": "Biên bản nghiên cứu; xác nhận ĐẠT cần kết quả kiểm chuyên môn độc lập.",
        }

    def get_di_ban(self, bai_so: int) -> dict:
        w = _work(bai_so)
        path = f"{w.folder}/README.md"
        text = self._read(BRANCHES["v1"], path)
        lines = text.splitlines()
        pattern = re.compile(
            r"dị bản|truyền bản|vắn|trường|khác biệt|cách đếm|phiên bản|nhịp tư|nhịp tám",
            flags=re.IGNORECASE,
        )
        selected = [line for line in lines if pattern.search(line)][:24]
        return {
            "work": w.descriptor(),
            "source_url": self._reference(BRANCHES["v1"], path),
            "excerpts": selected,
            "notice": "Dòng trích từ nguồn V1; không khẳng định các dị bản tương đương.",
        }

    def get_nguon(self, bai_so: int) -> dict:
        w = _work(bai_so)
        path = f"{w.folder}/README.md"
        text = self._read(BRANCHES["v1"], path)
        links = re.findall(r"\[([^\]]{1,160})\]\((https?://[^)\s]+)\)", text)
        seen = set()
        sources = []
        for label, url in links:
            if url in seen:
                continue
            seen.add(url)
            sources.append({"label": label, "url": url})
        return {
            "work": w.descriptor(),
            "source_url": self._reference(BRANCHES["v1"], path),
            "links": sources[:35],
            "notice": "Liên kết chép từ hồ sơ, chưa tự kiểm mọi URL và quyền tái bản.",
        }

    def get_quy_che_v2(self) -> dict:
        branch = BRANCHES["v2"]
        path = "docs/ke-hoach-v2.md"
        content = self._read(branch, path)
        return {
            "source_url": self._reference(branch, path),
            "content": content[:MAX_CHARS],
            "disclaimer": "Tiêu chí nghiệm thu, không phải chứng nhận mọi bài đã đạt.",
        }
