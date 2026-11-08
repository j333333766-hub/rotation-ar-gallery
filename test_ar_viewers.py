import ast, html, re
from pathlib import Path
from repair_ar_viewers import update_viewer
root = Path(__file__).parent
source = ast.parse((root / 'build.py').read_text(encoding='utf-8'))
fn = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'patch_viewer')
ns = {'html':html,'re':re,'ROOT':root,'qr_svg':lambda url:'<svg aria-label="QR"/>'}
exec(compile(ast.Module(body=[fn], type_ignores=[]), 'patch_viewer', 'exec'), ns)
page = ns['patch_viewer']('<html>OLD SCRIPT</html>', '10135 홍*동', 'https://example.test/works/10135/')
assert 'OLD SCRIPT' not in page
assert 'webxr scene-viewer quick-look' in page
assert '10135 홍*동' in page
assert page.count('id="wb-qr"') == 1
assert 'Google 3D/AR로 열기' in page
assert update_viewer(page, (root/'viewer.tpl.html').read_text(encoding='utf-8')) == page
print('PASS future ZIP builds use repaired viewer and preserve masked name/navigation; repair is idempotent')
