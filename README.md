# 회전체 작품 AR 갤러리 (구월중 1학년)

학생들이 그림판3D에서 `저장 → AR 웹뷰어 (ZIP)`으로 만든 작품을 한 화면에 모아 AR로 보는 사이트.

## 새 작품 올리기
1. 학생 ZIP이 `OneDrive - 구월중학교\2026학년도\회전체 만들기 3D 모델 제출`에 모인다(파일 이름 = 학번이름.zip).
2. 이 폴더에서 `python build.py` → `works/`와 첫 화면 `index.html`을 새로 만든다.
3. `git add -A && git commit -m "작품 갱신" && git push` → 1~2분 뒤 Pages에 반영.

## 규칙
- 공개 사이트라 이름은 가린다: 버튼은 `10101 홍*동`, 폴더는 학번(`works/10101/`). 원래 ZIP 이름은 저장소에 남지 않는다.
- ZIP에서 `index.html`·`model.glb`·`model.usdz`만 꺼낸다. 셋 중 하나라도 없으면 건너뛰고 이유를 출력한다.
- 뷰어 위쪽에 작품 이름, `← 작품 목록`, `📱 휴대폰으로`(그 작품 주소 QR)를 넣는다(`patch_viewer`).
- 첫 화면 오른쪽 위에 갤러리 주소 QR(좁은 화면=휴대폰에서는 숨김). QR 주소는 build.py 의 `BASE`.
- GitHub Pages 사이트 한도는 1GB. 작품 하나가 0.1~4MB라 800MB가 넘으면 build.py가 경고한다 → 반별 저장소로 나눈다.
- 카드 미리보기 사진 `works/<학번>/thumb.webp`: build.py 가 `thumbs.mjs`(헤드리스 크롬 + model-viewer, 비스듬한 각도, 투명 바탕)로 찍는다.
  model.glb 내용이 같으면 `_thumbcache/`(git 제외)의 사진을 다시 써서 새 작품만 찍는다(작품당 1초 남짓). node·크롬·playwright-core(algeo3d-paint 폴더) 필요.
- 첫 화면 위쪽에 반 고르기 칩(전체·1학년 7반…·기타). 반은 폴더 이름 학번 5자리에서 뽑고, 학번이 아니면 '기타'. 주소 끝 `#1-7`로 그 반만 열린다.
