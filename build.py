# 회전체 AR 갤러리 만들기
#   python build.py            ← 제출 폴더의 ZIP 을 모두 풀어 works/ 와 첫 화면(index.html)을 새로 만든다
#   python build.py <폴더>     ← 다른 폴더의 ZIP 으로
# - ZIP 은 그림판3D 의 '저장 → AR 웹뷰어 (ZIP)' 결과(index.html·model.glb·model.usdz). 이 셋만 꺼낸다.
# - 작품마다 works/<파일 이름>/ 에 풀고, 뷰어 위쪽에 작품 이름과 '← 작품 목록' 을 넣는다.
# - 첫 화면은 ZIP 개수만큼 파일 이름 버튼. 고친 뒤 git add -A → commit → push 하면 1~2분 뒤 Pages 에 반영.
import html, json, re, shutil, sys, time, zipfile
from pathlib import Path

ROOT = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r'C:\Users\j333333\OneDrive - 구월중학교\2026학년도\회전체 만들기 3D 모델 제출')
WORKS = ROOT / 'works'
NEED = ('index.html', 'model.glb', 'model.usdz')


def label(zip_path):
    """보여 줄 이름과 폴더 이름. 공개 사이트라 '10101홍길동' → ('10101 홍*동', '10101'): 이름은 가운데를 가리고 폴더는 학번만(10/29 사용자 결정)."""
    s = zip_path.stem
    s = re.sub(r'[_ ]*AR ?웹뷰어$', '', s).strip(' _') or zip_path.stem
    m = re.match(r'^(\d{4,6})[\s_-]*([가-힣]{2,5})', s)
    if not m:
        return s, s
    sid, nm = m.groups()
    masked = nm[0] + '*' if len(nm) == 2 else nm[0] + '*' * (len(nm) - 2) + nm[-1]
    return f'{sid} {masked}', sid


def slug(name, used):
    s = re.sub(r'[\\/:*?"<>|#%&{}\s]+', '_', name).strip('_.') or 'work'
    base, n = s, 2
    while s in used:
        s, n = f'{base}_{n}', n + 1
    used.add(s)
    return s


def patch_viewer(text, name):
    t = html.escape(name)
    text = re.sub(r'<title>.*?</title>', f'<title>{t} · AR로 보기</title>', text, count=1, flags=re.S)
    back = ('<a href="../../" style="position:absolute;left:14px;top:50%;transform:translateY(-50%);'
            'color:inherit;font-size:14px;font-weight:600;text-decoration:none;opacity:.85">← 작품 목록</a>')
    text = re.sub(r'<header>.*?</header>', f'<header style="position:relative">{back}{t}</header>', text, count=1, flags=re.S)
    return re.sub(r'alt="[^"]*"', f'alt="{t}"', text, count=1)


for _ in range(5):   # OneDrive 가 동기화 중이면 빈 폴더 지우기가 잠깐 거부된다 → 조금 기다렸다 다시
    try:
        if WORKS.exists():
            shutil.rmtree(WORKS)
        break
    except PermissionError:
        time.sleep(1.5)
WORKS.mkdir(exist_ok=True)
items, used, skipped = [], set(), []
for z in sorted(SRC.glob('*.zip'), key=lambda p: p.name):
    try:
        with zipfile.ZipFile(z) as zf:
            names = {Path(i.filename).name: i for i in zf.infolist() if not i.is_dir()}
            if not all(k in names for k in NEED):
                skipped.append(f'{z.name} (AR 웹뷰어 ZIP 이 아님: {", ".join(k for k in NEED if k not in names)} 없음)')
                continue
            name, key = label(z)
            d = WORKS / slug(key, used)
            d.mkdir()
            for k in NEED:
                data = zf.read(names[k])
                if k == 'index.html':
                    data = patch_viewer(data.decode('utf-8'), name).encode('utf-8')
                (d / k).write_bytes(data)
            size = sum((d / k).stat().st_size for k in NEED)
            items.append({'name': name, 'dir': d.name, 'mb': round(size / 1e6, 1)})
    except zipfile.BadZipFile:
        skipped.append(f'{z.name} (ZIP 파일이 깨짐)')

total = sum(i['mb'] for i in items)
data = json.dumps(items, ensure_ascii=False).replace('<', '\\u003c')
page = (ROOT / 'page.tpl.html').read_text(encoding='utf-8').replace('__ITEMS__', data)
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print(f'작품 {len(items)}개 · {total:.1f}MB' + (f' · 건너뜀 {len(skipped)}개' if skipped else ''))
for s in skipped:
    print('  건너뜀:', s)
if total > 800:
    print('  ⚠ GitHub Pages 사이트 한도(1GB)에 가까워요. 반별로 저장소를 나누세요.')
