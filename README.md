# 회전체 작품 AR 갤러리 (구월중 1학년)

학생들이 그림판3D에서 `저장 → AR 웹뷰어 (ZIP)`으로 만든 작품을 한 화면에 모아 AR로 보는 사이트.

## 새 작품 올리기
1. 학생 ZIP이 `OneDrive - 구월중학교\2026학년도\회전체 만들기 3D 모델 제출`에 모인다(파일 이름 = 학번이름.zip).
2. 이 폴더에서 `python build.py` → `works/`와 첫 화면 `index.html`을 새로 만든다.
3. `git add -A && git commit -m "작품 갱신" && git push` → 1~2분 뒤 Pages에 반영.

## 규칙
- 공개 사이트라 이름은 가린다: 버튼은 `10101 홍*동`, 폴더는 학번(`works/10101/`). 원래 ZIP 이름은 저장소에 남지 않는다.
  학번 뒤가 영문(한글 이름을 영문 자판으로 친 `10626wjsdudwls` 등)이면 학번만 보인다.
- ZIP에서 `index.html`·`model.glb`·`model.usdz`만 꺼낸다. 셋 중 하나라도 없으면 건너뛰고 이유를 출력한다.
- 학생이 만든 하위 폴더 속 ZIP과 압축을 풀어 둔 폴더(세 파일이 바로 들어 있는 폴더, 이름은 폴더 이름에서)도 읽는다. 맨 위 ZIP과 같은 학번이면 `같은 작품이 이미 있음`으로 건너뛴다(친구 ZIP을 함께 넣는 일이 많음).
- 파일 이름 앞에 붙은 이모지·기호(`❤️10912…`)는 떼고 이름을 가린다.
- 뷰어 위쪽에 작품 이름, `← 작품 목록`, `📱 휴대폰으로`(그 작품 주소 QR)를 넣는다(`patch_viewer`).
- 첫 화면 오른쪽 위에 갤러리 주소 QR(좁은 화면=휴대폰에서는 숨김). QR 주소는 build.py 의 `BASE`.
- GitHub Pages 사이트 한도는 1GB. 작품 하나가 0.1~4MB라 800MB가 넘으면 build.py가 경고한다 → 반별 저장소로 나눈다.
- 카드 미리보기 사진 `works/<학번>/thumb.webp`: build.py 가 `thumbs.mjs`(헤드리스 크롬 + model-viewer, 비스듬한 각도, 투명 바탕)로 찍는다.
  model.glb 내용이 같으면 `_thumbcache/`(git 제외)의 사진을 다시 써서 새 작품만 찍는다(작품당 1초 남짓). node·크롬·playwright-core(algeo3d-paint 폴더) 필요.
- 첫 화면 위쪽에 반 고르기 칩(전체·1학년 7반…·기타). 반은 폴더 이름 학번 5자리에서 뽑고, 학번이 아니면 '기타'. 주소 끝 `#1-7`로 그 반만 열린다.

## 안드로이드 AR 실행 수정 (2026-11-08)

- `viewer.tpl.html`이 작품 뷰어의 공통 원본입니다. 브라우저 AR(WebXR)을 먼저 시도하고, 안드로이드에는 별도의 `Google 3D/AR로 열기` 링크를 제공합니다. iPhone/iPad Quick Look은 유지합니다.
- AR 지원 확인이 모델 로딩보다 늦게 끝나도 버튼 상태가 갱신됩니다. 실행 실패, 카메라 권한, 앱 안의 브라우저, HTTPS가 아닌 주소에 대한 안내를 표시합니다.
- `build.py`의 `patch_viewer`는 학생 ZIP에 들어 있는 오래된 뷰어 대신 이 공통 원본을 사용합니다. 모델·썸네일·학생 이름 가림 규칙은 그대로 유지합니다.
- 이미 올라간 작품의 뷰어만 바꿀 때는 `python repair_ar_viewers.py`를 실행합니다. 제출 ZIP을 다시 가져오거나 작품 목록·모델 파일을 수정하지 않습니다. 기존 작품 제목과 목록 이동·QR 버튼을 보존합니다.
- 실제 AR에는 지원 기기와 최신 Google 앱·Google Play AR 서비스가 필요합니다. 브라우저 자동 검증으로는 실물 스마트폰의 카메라 추적까지 확인할 수 없습니다.

참고: [model-viewer AR](https://modelviewer.dev/examples/augmentedreality/), [Google Scene Viewer](https://developers.google.com/ar/develop/scene-viewer)

## 11/10 특별 수업 작품(학교 앱 제출) 싣기 (2026-11-08 추가)

- 특별 수업(odap-rediscovery.web.app/rotation-special)은 학생이 활동지 안에서 GLB·USDZ를 올린다(Firestore `wbFiles/rotation-special_*`).
- `node special_sync.mjs` → `_special/<학번이름>/model.glb(·model.usdz)`로 받아 둔다(읽기만, 바뀐 것만). 이 PC의 firebase CLI 로그인을 쓴다.
- `python build.py`가 `_special/`도 읽어 `works/<학번>_sp/`에 '학번 이*름 · 특별 수업' 카드로 싣는다(10/29 작품과 따로). USDZ가 없으면 뷰어의 `ios-src`를 뺀다.
- 한 번에: `special_update.ps1`(받기 → 빌드 → 바뀌면 커밋·푸시, 기록 special_update.log).
- 수업 날 자동: `special_schedule.ps1`로 작업 스케줄러 '특별수업 AR갤러리 갱신'(11/10 08:00부터 9시간, 1분마다) 등록. 끄기 `Unregister-ScheduledTask -TaskName '특별수업 AR갤러리 갱신' -Confirm:$false`.
- `_special/`·동기화 스크립트들은 실명 폴더·로컬 토큰을 쓰므로 git에 올리지 않는다(.gitignore).

## 11/11 바뀐 점
- 갤러리에는 활동지(/rotation-special 15쪽)로 낸 작품만 싣는다(`build.py` 의 `USE_ONEDRIVE = False`). 원드라이브 제출 폴더의 기존 작품은 싣지 않는다(원본 그대로, 다시 실으려면 True).
- 그전 갤러리(기존 작품 전체)는 git 태그 `gallery-before-1111` 에 남겨 둠.
- 자동 갱신 예약: 11/11 14:30부터 4시간, 1분마다(`special_schedule.ps1`). 끄기: `Unregister-ScheduledTask -TaskName '특별수업 AR갤러리 갱신' -Confirm:$false`
