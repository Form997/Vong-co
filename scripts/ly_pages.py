"""Publish a source-specific lý dossier, separate from the 20 bản Tổ."""
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

DATA = Path(__file__).resolve().parents[1] / 'data/ly/01-ly-cay-bong.json'
PAGE = 'ly/01-ly-cay-bong/index.html'


def load_dossier():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    if (data['id'] != 'LY-001' or data['slug'] != '01-ly-cay-bong'
            or data['status'] != 'research_in_progress'
            or data['performance_accepted'] is not False):
        raise ValueError('Hồ sơ lý chưa được phép đổi trạng thái nghiệm thu.')
    ids = [s['id'] for s in data['sources']]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Mã nguồn lý trùng hoặc rỗng.')
    for source in data['sources']:
        url = urlsplit(source['url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError('Nguồn lý phải có URL HTTPS công khai.')
    for claim in data['claims']:
        if not claim['sources'] or not set(claim['sources']) <= set(ids):
            raise ValueError('Kết luận lý thiếu mã nguồn hợp lệ.')
    if not data['pending']:
        raise ValueError('Hồ sơ nghiên cứu phải giữ các việc còn thiếu.')
    return data


def render_dossier(data):
    e = escape
    claims = ''.join('<section><h2>'+e(c['topic'])+'</h2><p>'+e(c['text'])+'</p><p>Nguồn: '+
                     ', '.join('<a href="#'+e(s)+'">'+e(s)+'</a>' for s in c['sources'])+
                     '</p></section>' for c in data['claims'])
    sources = ''.join('<li id="'+e(s['id'])+'"><h3>'+e(s['id'])+' · <a href="'+e(s['url'],quote=True)+'">'+
                      e(s['title'])+'</a></h3><p>'+e(s['publisher']+' · '+s['date'])+'</p><p>'+e(s['scope'])+'</p></li>'
                      for s in data['sources'])
    pending = ''.join('<li>'+e(p)+'</li>' for p in data['pending'])
    return '''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lý cây bông · Hồ sơ LY-001 · HAI ĐẤT</title>
<meta name="description" content="Hồ sơ kiểm nguồn Lý cây bông: bản ký âm, nguồn VOV, phân biệt tác phẩm cùng tên và các việc chưa kiểm chứng.">
<link rel="canonical" href="https://form997.github.io/Vong-co/ly/01-ly-cay-bong/">
<style>body{margin:0;background:#f7f3e8;color:#233d37;font:18px/1.7 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:24px}a{color:#176658;overflow-wrap:anywhere}h1{font-family:Georgia,serif;font-size:clamp(2rem,7vw,3.4rem)}h2{font-size:1.35rem}section{border-top:1px solid #b5c2b8;padding:16px 0}.status{background:#e9dfbf;padding:16px;border-left:4px solid #816322}li{margin:16px 0}a:focus-visible{outline:3px solid #816322;outline-offset:4px}</style></head><body><main>
<nav aria-label="Điều hướng"><a href="../../web/v3/">← Thư viện HAI ĐẤT</a></nav>
<p>HỒ SƠ BÀI LÝ · LY-001</p><h1>Lý cây bông</h1>
<p class="status"><strong>Đang nghiên cứu · Chưa nghiệm thu diễn xướng</strong><br>Ngày kiểm nguồn: '''+e(data['reviewed_on'])+'''</p>
<p>'''+e(data['numbering_note'])+'''</p>'''+claims+'''
<section><h2>Sổ nguồn</h2><ol>'''+sources+'''</ol></section>
<section><h2>Việc còn lại của bài này</h2><ul>'''+pending+'''</ul></section>
<p>Trang này chỉ công bố mô tả và liên kết nguồn; chưa phát hành lời ca, ký âm hoặc âm thanh. Kiểm thử phần mềm không thay thế thẩm định âm nhạc.</p>
<p><a href="../../data/ly/01-ly-cay-bong.json">Dữ liệu hồ sơ JSON</a> · <a href="https://github.com/Form997/Vong-co/blob/main/ly/01-ly-cay-bong/README.md">Hồ sơ và sổ công việc trên GitHub</a></p>
</main></body></html>'''
