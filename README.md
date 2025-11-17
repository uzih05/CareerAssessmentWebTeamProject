# 전주대학교 전공 유형 검사 프로젝트

## 🎨 프로젝트 구조

```
major-test/
└── frontend/
    ├── index.html                    # 메인 페이지
    ├── pages/                        # 페이지들
    │   ├── test.html                 # 검사 페이지 (추후 구현)
    │   ├── result.html               # 결과 페이지 (추후 구현)
    │   └── departments/              # 학과 소개 페이지들 (추후 구현)
    ├── css/
    │   ├── reset.css                 # CSS 리셋
    │   ├── variables.css             # CSS 변수 (색상, 간격 등)
    │   ├── common.css                # 공통 스타일
    │   ├── components/               # 컴포넌트별 스타일
    │   │   ├── header.css            # 헤더 스타일
    │   │   └── button.css            # 리퀴드 글래스 버튼
    │   └── pages/
    │       └── main.css              # 메인 페이지 스타일
    ├── js/
    │   ├── components/
    │   │   └── header.js             # 헤더 인터랙션
    │   └── pages/
    │       └── main.js               # 메인 페이지 로직
    └── assets/
        ├── images/                   # 이미지 파일들
        ├── videos/                   # 비디오 파일들
        └── fonts/                    # 폰트 파일들
```

## 📋 완성된 기능

### ✅ 메인 페이지 (index.html)

1. **헤더 (Header)**
   - 로고 및 브랜드명
   - 네비게이션 메뉴 (홈, 검사하기, 학과소개, 소개)
   - 모바일 반응형 햄버거 메뉴
   - 스크롤 시 배경색 변경 효과

2. **히어로 섹션 (Hero Section)**
   - 풀스크린 배경 (동영상 또는 이미지 지원)
   - 어두운 그라데이션 오버레이
   - 타이틀 및 서브타이틀
   - **리퀴드 글래스 버튼** (검사 시작하기)
   - 스크롤 인디케이터
   - 페이드인 애니메이션

3. **특징 섹션 (Features Section)**
   - 3개의 특징 카드 (정확한 분석, 맞춤 추천, 빠른 결과)
   - 호버 시 카드 상승 효과
   - 스크롤 시 순차적 나타남 애니메이션

4. **푸터 (Footer)**
   - 4단 정보 구역
   - 바로가기 링크
   - 연락처 정보

### 🎨 디자인 특징

1. **리퀴드 글래스 효과**
   - 반투명 배경 (`rgba(255, 255, 255, 0.1)`)
   - 블러 효과 (`backdrop-filter: blur(20px)`)
   - 그라데이션 테두리
   - 호버 시 물결 효과
   - 클릭 시 리플 애니메이션

2. **색상 시스템**
   - Primary: `#1a237e` (전주대 블루)
   - Secondary: `#00897b` (틸)
   - Accent: `#ffd600` (옐로우)
   - 완전한 그레이스케일 팔레트

3. **반응형 디자인**
   - 데스크톱 (1400px+)
   - 태블릿 (768px - 1399px)
   - 모바일 (~ 767px)

## 🚀 실행 방법

### 1. 로컬에서 바로 열기
```bash
# index.html 파일을 브라우저로 드래그하거나 더블클릭
```

### 2. 로컬 서버로 실행 (권장)
```bash
# Python 3 사용
cd frontend
python -m http.server 8000

# 브라우저에서 http://localhost:8000 접속
```

### 3. Live Server (VS Code)
- VS Code에서 index.html 우클릭
- "Open with Live Server" 선택

## 📝 배경 설정하기

### 동영상 배경 사용

1. `assets/videos/` 폴더에 `bg-video.mp4` 파일 넣기
2. index.html에서 이미 설정되어 있음:
```html
<video class="hero-video" autoplay muted loop playsinline>
    <source src="assets/videos/bg-video.mp4" type="video/mp4">
</video>
```

### 이미지 배경 사용

1. `assets/images/` 폴더에 `bg-image.jpg` 파일 넣기
2. index.html에서 video 태그를 주석처리하고 img 태그 주석 해제:
```html
<!-- <video class="hero-video" ...></video> -->
<img class="hero-image" src="assets/images/bg-image.jpg" alt="Background">
```

3. 또는 CSS에서 전환:
```css
/* pages/main.css */
.hero-video {
    display: none; /* 동영상 숨김 */
}

.hero-image {
    display: block; /* 이미지 표시 */
}
```

## 🎯 다음 단계

### 즉시 추가 가능한 기능

1. **테스트 페이지 (test.html)**
   - SPA 방식 질문 전환
   - 프로그레스 바
   - 뒤로가기 버튼

2. **결과 페이지 (result.html)**
   - 레이더 차트 (Chart.js)
   - Top 3 학과 추천
   - 공유 기능

3. **학과 소개 페이지**
   - 70개 학과 개별 페이지
   - 학과별 정보 카드

## 🛠️ 기술 스택

- **HTML5**: 시맨틱 마크업
- **CSS3**: 
  - CSS Variables (커스텀 속성)
  - Flexbox & Grid
  - Animations & Transitions
  - Glassmorphism
- **Vanilla JavaScript**: 
  - ES6+
  - DOM Manipulation
  - Intersection Observer API
  - Event Handling

## 📱 브라우저 지원

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 💡 커스터마이징 가이드

### 색상 변경
`css/variables.css` 파일에서 색상 변수 수정:
```css
:root {
    --primary-color: #1a237e;  /* 원하는 색상으로 변경 */
    --secondary-color: #00897b;
    --accent-color: #ffd600;
}
```

### 폰트 변경
`css/reset.css` 파일에서 폰트 패밀리 수정:
```css
body {
    font-family: 'Noto Sans KR', sans-serif; /* 원하는 폰트로 */
}
```

### 애니메이션 속도 조절
`css/variables.css`:
```css
:root {
    --transition-fast: 150ms ease;   /* 빠른 전환 */
    --transition-base: 300ms ease;   /* 기본 전환 */
    --transition-slow: 500ms ease;   /* 느린 전환 */
}
```

## 📞 문의

프로젝트 관련 문의사항이 있으시면 팀원에게 연락주세요.

---

**개발 팀**: 강민석, 유지헌, 조현우  
**제작**: 2025년  
**학교**: 전주대학교