"""Publish a source-specific lý dossier, separate from the 20 bản Tổ."""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

DATA_DIR = Path(__file__).resolve().parents[1] / 'data/ly'
DOSSIERS = (('LY-001', '01-ly-cay-bong'), ('LY-002', '02-ly-con-sao-go-cong'))
PAGES = tuple(f'ly/{slug}/index.html' for _, slug in DOSSIERS)


def load_dossier(slug='01-ly-cay-bong'):
    identities = {slug: identity for identity, slug in DOSSIERS}
    if slug not in identities:
        raise ValueError('Bài lý chưa có trong danh mục xuất bản.')
    data = json.loads((DATA_DIR / (slug + '.json')).read_text(encoding='utf-8'))
    if (data['id'] != identities[slug] or data['slug'] != slug
            or data['status'] != 'research_in_progress'
            or data['performance_accepted'] is not False):
        raise ValueError('Hồ sơ lý chưa được phép đổi trạng thái nghiệm thu.')
    ids = [s['id'] for s in data['sources']]
    if not ids or len(set(ids)) != len(ids) or any(not re.fullmatch(r'S[1-9][0-9]*', i) for i in ids):
        raise ValueError('Mã nguồn lý trùng hoặc rỗng.')
    for source in data['sources']:
        url = urlsplit(source['url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError('Nguồn lý phải có URL HTTPS công khai.')
    for claim in data['claims'] + data.get('comparison', []):
        if not claim['sources'] or not set(claim['sources']) <= set(ids):
            raise ValueError('Kết luận lý thiếu mã nguồn hợp lệ.')
    if not data['pending']:
        raise ValueError('Hồ sơ nghiên cứu phải giữ các việc còn thiếu.')
    return data


def render_dossier(data):
    e = escape
    slug = data['slug']
    navigation = ' · '.join('<a href="../'+e(other)+'/">'+e(identity)+'</a>' for identity, other in DOSSIERS if other != slug)
    comparison = ''
    if data.get('comparison'):
        rows = ''.join('<tr><th scope="row">'+e(row['label'])+'</th><td>'+e(row['detail'])+'</td><td>'+', '.join('<a href="#'+e(ref)+'">'+e(ref)+'</a>' for ref in row['sources'])+'</td></tr>' for row in data['comparison'])
        comparison = '<section><h2>Phân biệt đối tượng</h2><div class="table-scroll" role="region" aria-label="Bảng đối chiếu nguồn" tabindex="0"><table><thead><tr><th>Đối tượng</th><th>Ghi nhận theo nguồn</th><th>Nguồn</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>'
    claims = ''.join('<section><h2>'+e(c['topic'])+'</h2><p>'+e(c['text'])+'</p><p>Nguồn: '+
                     ', '.join('<a href="#'+e(s)+'">'+e(s)+'</a>' for s in c['sources'])+
                     '</p></section>' for c in data['claims'])
    sources = ''.join('<li id="'+e(s['id'])+'"><h3>'+e(s['id'])+' · <a href="'+e(s['url'],quote=True)+'">'+
                      e(s['title'])+'</a></h3><p>'+e(s['publisher']+' · '+s['date'])+'</p><p>'+e(s['scope'])+'</p></li>'
                      for s in data['sources'])
    pending = ''.join('<li>'+e(p)+'</li>' for p in data['pending'])
    return '''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>'''+e(data['name'])+' · Hồ sơ '+e(data['id'])+''' · HAI ĐẤT</title>
<meta name="description" content="Hồ sơ kiểm nguồn '''+e(data['name'],quote=True)+''': đối chiếu tư liệu, phân biệt các bản và theo dõi việc chưa kiểm chứng.">
<link rel="canonical" href="https://form997.github.io/Vong-co/ly/'''+e(slug,quote=True)+'''/">
<style>body{margin:0;background:#f7f3e8;color:#233d37;font:18px/1.7 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:24px}a{color:#176658;overflow-wrap:anywhere}h1{font-family:Georgia,serif;font-size:clamp(2rem,7vw,3.4rem)}h2{font-size:1.35rem}section{border-top:1px solid #b5c2b8;padding:16px 0}.status{background:#e9dfbf;padding:16px;border-left:4px solid #816322}li{margin:16px 0}table{border-collapse:collapse;width:100%;font-size:16px}th,td{padding:10px;text-align:left;border:1px solid #b5c2b8;vertical-align:top}.table-scroll{overflow-x:auto}a:focus-visible{outline:3px solid #816322;outline-offset:4px}</style></head><body><main>
<nav aria-label="Điều hướng"><a href="../../web/v3/">← Thư viện HAI ĐẤT</a> · Hồ sơ khác: '''+navigation+'''</nav>
<p>HỒ SƠ BÀI LÝ · '''+e(data['id'])+'''</p><h1>'''+e(data['name'])+'''</h1>
<p class="status"><strong>Đang nghiên cứu · Chưa nghiệm thu diễn xướng</strong><br>Ngày kiểm nguồn: '''+e(data['reviewed_on'])+'''</p>
<p>'''+e(data['numbering_note'])+'''</p>'''+claims+comparison+'''
<section><h2>Sổ nguồn</h2><ol>'''+sources+'''</ol></section>
<section><h2>Việc còn lại của bài này</h2><ul>'''+pending+'''</ul></section>
<p>Trang này chỉ công bố mô tả và liên kết nguồn; chưa phát hành lời ca, ký âm hoặc âm thanh. Kiểm thử phần mềm không thay thế thẩm định âm nhạc.</p>
<p><a href="../../data/ly/'''+e(slug,quote=True)+'''.json">Dữ liệu hồ sơ JSON</a> · <a href="https://github.com/Form997/Vong-co/blob/main/ly/'''+e(slug,quote=True)+'''/README.md">Hồ sơ và sổ công việc trên GitHub</a></p>
</main></body></html>'''
