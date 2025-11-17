# CLAUDE.md - AI Assistant Guide

## Project Overview

**Project Name:** Jeonju University Major Type Assessment Platform (전주대학교 전공 유형 검사 프로젝트)

**Purpose:** An interactive web application that helps students identify suitable majors among 70 academic programs at Jeonju University through a science-based aptitude assessment system.

**Project Language:** Korean (코드 주석과 문서는 한글 선호)

**Team:** 강민석, 유지헌, 조현우

**Tech Stack:**
- **Backend:** Python 3.x + FastAPI
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6+) - No frameworks
- **Server:** Python http.server or FastAPI uvicorn

---

## Directory Structure

```
CareerAssessmentWebTeamProject/
├── main.py                              # FastAPI backend application
├── test_main.http                       # HTTP REST client testing file
├── README.md                            # Project documentation (Korean)
├── CLAUDE.md                            # This file - AI assistant guide
└── frontend/                            # Frontend application root
    ├── index.html                       # Main landing page
    ├── css/                             # Stylesheets (component-based)
    │   ├── reset.css                    # CSS normalization & base styles
    │   ├── variables.css                # Design tokens (colors, spacing, etc.)
    │   ├── common.css                   # Shared utilities & layout
    │   ├── components/                  # Component-specific styles
    │   │   ├── header.css               # Navigation/header styling
    │   │   └── button.css               # Liquid glass button component
    │   └── pages/                       # Page-specific styles
    │       └── main.css                 # Main landing page styles
    ├── js/                              # JavaScript modules
    │   ├── components/                  # Reusable component logic
    │   │   └── header.js                # Header interactivity & mobile menu
    │   └── pages/                       # Page-specific functionality
    │       └── main.js                  # Main page interactions
    └── assets/                          # Media files (currently empty)
        ├── images/                      # Background images, icons
        ├── videos/                      # Background videos
        └── fonts/                       # Custom web fonts
```

---

## Architecture & Design Patterns

### 1. Component-Based Architecture

**CSS Components:**
- Each component has its own CSS file in `css/components/`
- Component styles are self-contained and reusable
- Follow BEM-inspired naming (e.g., `hero-section`, `feature-card`)

**JavaScript Components:**
- Modular files matching component names
- Each component handles its own initialization and events
- Use DOMContentLoaded for safe DOM access

### 2. Design System (CSS Variables)

The entire design system is defined in `css/variables.css` using CSS custom properties:

```css
Color Palette:
  --primary-color: #1a237e          /* Jeonju University Blue */
  --primary-light: #534bae
  --primary-dark: #000051
  --secondary-color: #00897b        /* Teal */
  --accent-color: #ffd600           /* Yellow */

Grayscale (9 levels):
  --gray-50 through --gray-900
  --white, --black

Spacing Scale (rem-based):
  --spacing-xs: 0.25rem
  --spacing-sm: 0.5rem
  --spacing-md: 1rem
  --spacing-lg: 1.5rem
  --spacing-xl: 2rem
  --spacing-2xl: 3rem
  --spacing-3xl: 4rem

Border Radius:
  --radius-sm: 4px
  --radius-md: 8px
  --radius-lg: 12px
  --radius-xl: 16px
  --radius-2xl: 24px
  --radius-full: 9999px

Transitions:
  --transition-fast: 150ms ease
  --transition-base: 300ms ease
  --transition-slow: 500ms ease

Shadows (4 elevation levels):
  --shadow-sm, --shadow-md, --shadow-lg, --shadow-xl

Z-Index Scale:
  --z-dropdown: 1000
  --z-sticky: 1020
  --z-fixed: 1030
  --z-modal: 1050
  --z-tooltip: 1070
```

### 3. Glassmorphism Design Pattern

The project heavily uses glassmorphism effects:

```css
/* Standard glass effect pattern */
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.2);
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
```

Applied to:
- Header navigation (scrolled state)
- Primary buttons
- Card overlays

### 4. Responsive Design Strategy

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1399px
- Desktop: 1400px+

**Approach:**
- Mobile-first base styles
- Media queries for tablet/desktop enhancements
- Hamburger menu on mobile, horizontal nav on desktop
- Flexible grid layouts using `repeat(auto-fit, minmax(...))`
- Fluid typography with rem units

---

## Coding Conventions

### HTML

**Structure:**
- Use semantic HTML5 elements (`<header>`, `<section>`, `<footer>`, `<nav>`)
- Maintain proper heading hierarchy (h1 → h2 → h3)
- Include meaningful alt text for images
- Use data attributes for JavaScript hooks (e.g., `data-component="header"`)

**Class Naming:**
- kebab-case (e.g., `hero-section`, `mobile-menu-btn`)
- BEM-inspired for complex components (e.g., `header-container`, `nav-links`)
- State classes without prefixes: `active`, `scrolled`, `visible`

**Example:**
```html
<section class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">
      <span class="gradient-text">Title</span>
    </h1>
  </div>
</section>
```

### CSS

**File Organization:**
1. Foundation layer: `reset.css`, `variables.css`
2. Common layer: `common.css` (utilities, layout)
3. Component layer: `components/*.css`
4. Page layer: `pages/*.css` (page-specific overrides)

**Import Order in HTML:**
```html
<link rel="stylesheet" href="css/reset.css">
<link rel="stylesheet" href="css/variables.css">
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/components/header.css">
<link rel="stylesheet" href="css/components/button.css">
<link rel="stylesheet" href="css/pages/main.css">
```

**Best Practices:**
- Always use CSS variables from `variables.css`
- Avoid magic numbers - use spacing/color variables
- Mobile-first media queries
- Use CSS Grid for layouts, Flexbox for alignment
- Prefer `rem` for sizing, `em` for component-relative sizing

**Example:**
```css
.feature-card {
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  background: var(--white);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-base);
}
```

### JavaScript

**Module Pattern:**
- Each file wraps code in DOMContentLoaded
- Use const/let, never var
- Prefer arrow functions
- Use template literals for strings
- Modern DOM APIs (querySelector, classList, etc.)

**Event Handling:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const element = document.querySelector('.my-element');

  element.addEventListener('click', (e) => {
    e.preventDefault();
    // Handle click
  });
});
```

**Naming Conventions:**
- camelCase for variables and functions
- UPPER_CASE for constants
- Descriptive names (e.g., `toggleMobileMenu`, not `toggle`)

**Performance Considerations:**
- Use Intersection Observer for scroll animations
- Debounce scroll/resize events when needed
- Remove event listeners and elements when done (memory management)
- Prefer CSS animations over JavaScript when possible

---

## Design System Details

### Color Usage Guidelines

**Primary Color (#1a237e - Jeonju Blue):**
- Navigation elements
- Primary buttons
- Important headings
- Brand elements
- Use `--primary-color` variable

**Secondary Color (#00897b - Teal):**
- Secondary actions
- Accent elements in gradients
- Hover states
- Use `--secondary-color` variable

**Accent Color (#ffd600 - Yellow):**
- Highlighted text
- Call-to-action highlights
- Small decorative elements
- Use `--accent-color` variable

**Grayscale:**
- Text: `--text-primary` (#212121), `--text-secondary` (#757575)
- Backgrounds: `--gray-50` to `--gray-900`
- Borders: `--gray-200` to `--gray-400`

### Typography Scale

**Default Font Stack:**
```css
font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Size Scale:**
- Headings: Large on desktop (h1: 3.5rem), scale down on mobile (h1: 2rem)
- Body: 1rem base (16px)
- Small text: 0.875rem

**Font Weights:**
- Regular: 400
- Medium: 500
- Bold: 700

### Button Components

Three variants defined in `components/button.css`:

1. **Glass Button (Primary CTA):**
```html
<button class="btn btn-glass">
  검사 시작하기
  <span class="btn-icon">→</span>
</button>
```

2. **Solid Primary Button:**
```html
<button class="btn btn-primary">
  더 알아보기
</button>
```

3. **Outline Button:**
```html
<button class="btn btn-outline">
  학과 안내
</button>
```

**Large Size Modifier:**
```html
<button class="btn btn-glass btn-lg">큰 버튼</button>
```

### Animation Patterns

**Keyframe Animations:**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Staggered Animations:**
Use setTimeout with incremental delays:
```javascript
elements.forEach((element, index) => {
  setTimeout(() => {
    element.classList.add('visible');
  }, index * 100);
});
```

---

## Backend Architecture

### FastAPI Application (main.py)

**Current Endpoints:**
```python
GET /              # Root - returns {"message": "Hello World"}
GET /hello/{name}  # Greeting endpoint
```

**Running the Server:**
```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

**API Testing:**
Use `test_main.http` with REST Client extension in VS Code:
```http
GET http://localhost:8000/
GET http://localhost:8000/hello/World
```

**Future Expansion:**
- POST /api/test/submit - Submit test answers
- GET /api/test/questions - Get test questions
- GET /api/results/{id} - Get test results
- POST /api/departments/search - Search departments

---

## Development Workflow

### Setting Up Development Environment

1. **Backend Setup:**
```bash
# Install FastAPI and dependencies
pip install fastapi uvicorn

# Run backend server
uvicorn main:app --reload
```

2. **Frontend Setup:**
```bash
# Option 1: Python HTTP server
cd frontend
python -m http.server 8000

# Option 2: VS Code Live Server
# Right-click index.html → "Open with Live Server"
```

3. **Access Application:**
- Frontend: http://localhost:8000
- Backend API: http://localhost:8000 (if running FastAPI)
- API Docs: http://localhost:8000/docs (FastAPI auto-generated)

### Adding New Pages

**Template for New Page:**

1. Create HTML file in `frontend/pages/`
2. Create CSS file in `frontend/css/pages/`
3. Create JS file in `frontend/js/pages/`
4. Update navigation in header

**Example - Test Page:**

```html
<!-- pages/test.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>검사하기 - 전주대학교 전공 유형 검사</title>
  <link rel="stylesheet" href="../css/reset.css">
  <link rel="stylesheet" href="../css/variables.css">
  <link rel="stylesheet" href="../css/common.css">
  <link rel="stylesheet" href="../css/components/header.css">
  <link rel="stylesheet" href="../css/pages/test.css">
</head>
<body>
  <!-- Include header component -->
  <!-- Page content -->
  <script src="../js/components/header.js"></script>
  <script src="../js/pages/test.js"></script>
</body>
</html>
```

### Adding New Components

**Steps:**
1. Create `css/components/component-name.css`
2. Create `js/components/component-name.js`
3. Add CSS import to HTML head
4. Add JS import before closing body tag

**Component Structure:**
```javascript
// js/components/component-name.js
document.addEventListener('DOMContentLoaded', () => {
  // Component initialization
  const component = document.querySelector('[data-component="name"]');

  // Event listeners
  component.addEventListener('click', handleClick);

  // Functions
  function handleClick(e) {
    // Logic
  }
});
```

---

## Key Files Reference

### index.html (Main Landing Page)
**Path:** `/frontend/index.html`

**Sections:**
- Header: Fixed navigation with mobile menu
- Hero: Full-screen background with CTAs
- Features: 3-column grid showcasing benefits
- Departments: Placeholder for department showcase
- Footer: 4-column info grid with links

**Key Elements:**
- `<video class="hero-video">` - Background video
- `.btn.btn-glass` - Primary CTA button
- `.mobile-menu-btn` - Hamburger toggle
- `.scroll-indicator` - Animated scroll prompt

### css/variables.css
**Purpose:** Central design token repository

**When to Edit:**
- Changing brand colors
- Adjusting spacing scale
- Modifying animation timings
- Updating shadow elevations

**Never:**
- Don't add component-specific styles here
- Don't override in other files; always use variables

### js/pages/main.js
**Functions:**
1. `setupSmoothScroll()` - Anchor link smooth scrolling
2. `setupVideoFallback()` - Video error handling
3. `setupParallax()` - Hero parallax effect
4. `setupIntersectionObserver()` - Feature card animations
5. `setupRippleEffect()` - Button ripple animation
6. `setupLoadAnimations()` - Page load transitions

### js/components/header.js
**Functions:**
1. Scroll detection → Add/remove 'scrolled' class
2. Mobile menu toggle → Open/close navigation
3. Active link highlighting
4. Hamburger animation (transform to X icon)

---

## Common Tasks for AI Assistants

### 1. Adding a New Section to Landing Page

**Steps:**
1. Add HTML markup in `index.html` before footer
2. Create styles in `css/pages/main.css`
3. Add animations in `js/pages/main.js` if needed
4. Use existing design system variables
5. Test responsiveness (mobile, tablet, desktop)

**Example - New "How It Works" Section:**
```html
<section class="section how-it-works">
  <div class="container">
    <h2 class="section-title">이용 방법</h2>
    <p class="section-subtitle">간단한 3단계로 나에게 맞는 전공을 찾으세요</p>
    <div class="steps-grid">
      <!-- Step cards -->
    </div>
  </div>
</section>
```

### 2. Modifying Color Scheme

**Process:**
1. Open `css/variables.css`
2. Modify color variables in `:root` selector
3. Changes propagate automatically to all components
4. Test contrast for accessibility

**Example:**
```css
:root {
  --primary-color: #0066cc;  /* New blue */
  --secondary-color: #ff6b6b; /* New red */
}
```

### 3. Creating New Button Variant

**Steps:**
1. Add variant class in `css/components/button.css`
2. Follow existing pattern (base `.btn` + modifier)
3. Use variables for consistency

**Example:**
```css
.btn-success {
  background: linear-gradient(135deg, #00c853, #64dd17);
  color: var(--white);
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### 4. Implementing API Integration

**Backend (main.py):**
```python
from fastapi import FastAPI
from pydantic import BaseModel

class TestAnswer(BaseModel):
    question_id: int
    answer: str

@app.post("/api/test/submit")
async def submit_test(answer: TestAnswer):
    # Process answer
    return {"status": "success"}
```

**Frontend (JavaScript):**
```javascript
async function submitAnswer(questionId, answer) {
  const response = await fetch('http://localhost:8000/api/test/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question_id: questionId,
      answer: answer
    })
  });

  return await response.json();
}
```

### 5. Adding Intersection Observer Animation

**Pattern:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // Trigger once
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

// Observe elements
const elements = document.querySelectorAll('.animate-on-scroll');
elements.forEach(el => observer.observe(el));
```

**CSS:**
```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Testing Guidelines

### Manual Testing Checklist

**Responsive Design:**
- [ ] Test on mobile viewport (< 768px)
- [ ] Test on tablet viewport (768px - 1399px)
- [ ] Test on desktop viewport (1400px+)
- [ ] Hamburger menu works on mobile
- [ ] All text is readable at all sizes

**Cross-Browser:**
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

**Interactions:**
- [ ] All buttons clickable
- [ ] Smooth scroll works
- [ ] Hover effects visible
- [ ] Animations perform smoothly (60fps)
- [ ] Forms validate properly

**Accessibility:**
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Alt text on images
- [ ] Sufficient color contrast
- [ ] Semantic HTML structure

### Performance Testing

**Lighthouse Scores to Target:**
- Performance: 90+
- Accessibility: 95+
- Best Practices: 90+
- SEO: 90+

**Optimization Checklist:**
- [ ] Images optimized (WebP format, lazy loading)
- [ ] CSS minified in production
- [ ] JavaScript minified in production
- [ ] No render-blocking resources
- [ ] Fonts preloaded

---

## Important Conventions for AI Assistants

### When Making Changes

1. **Always Use Existing Variables:**
   - Never hardcode colors, spacing, or timing
   - Reference `css/variables.css` for all design tokens
   - If a new variable is needed, add it to variables.css first

2. **Maintain Consistency:**
   - Follow existing naming patterns
   - Match code style (indentation, spacing)
   - Use Korean for user-facing content
   - Use English for code comments

3. **Preserve Responsiveness:**
   - Test changes at all breakpoints
   - Don't break mobile layout
   - Maintain touch-friendly tap targets (44x44px minimum)

4. **Component Isolation:**
   - Keep component styles in component files
   - Don't add page-specific styles to common.css
   - Avoid global scope pollution in JavaScript

5. **Performance First:**
   - Prefer CSS over JavaScript for animations
   - Use Intersection Observer for scroll-based effects
   - Optimize images before adding to assets
   - Lazy load below-the-fold content

### Code Review Checklist

Before committing changes, verify:
- [ ] No console errors in browser
- [ ] Code follows project conventions
- [ ] Korean text uses appropriate typography
- [ ] All variables used from variables.css
- [ ] Responsive at all breakpoints
- [ ] Animations smooth (no jank)
- [ ] Comments added for complex logic
- [ ] No dead code or unused variables

### Common Pitfalls to Avoid

**CSS:**
- ❌ Don't use `!important` (indicates architecture issue)
- ❌ Don't use inline styles
- ❌ Don't use fixed widths (use max-width or percentages)
- ❌ Don't use pixel values for font sizes (use rem)

**JavaScript:**
- ❌ Don't use var (use const/let)
- ❌ Don't attach multiple listeners to same element
- ❌ Don't forget to remove event listeners
- ❌ Don't manipulate DOM in loops

**General:**
- ❌ Don't commit assets without optimization
- ❌ Don't break existing functionality
- ❌ Don't skip testing on mobile
- ❌ Don't ignore console warnings

---

## Future Development Roadmap

### Phase 1: Core Assessment (Planned)
- [ ] Test question database (JSON or API)
- [ ] Test page with SPA-style question flow
- [ ] Progress bar component
- [ ] Answer validation and storage
- [ ] Navigation between questions

### Phase 2: Results & Recommendations (Planned)
- [ ] Result calculation algorithm
- [ ] Results page with radar chart (Chart.js)
- [ ] Top 3 department recommendations
- [ ] Detailed major explanations
- [ ] Share functionality (social media, link copy)

### Phase 3: Department Pages (Planned)
- [ ] Template for department detail pages
- [ ] 70 individual department pages
- [ ] Department info cards (curriculum, career paths)
- [ ] Image galleries
- [ ] Related majors section

### Phase 4: Advanced Features (Future)
- [ ] User accounts and saved results
- [ ] Comparison tool (compare multiple majors)
- [ ] AI-powered chat assistant
- [ ] Video testimonials from students
- [ ] Admin dashboard for test management

---

## Asset Management

### Images
**Location:** `frontend/assets/images/`

**Guidelines:**
- Use WebP format for photos (fallback to JPEG)
- Use SVG for icons and logos
- Optimize before adding (TinyPNG, Squoosh)
- Naming: kebab-case, descriptive (e.g., `hero-background.jpg`)

### Videos
**Location:** `frontend/assets/videos/`

**Guidelines:**
- Compress for web (H.264 codec)
- Keep file size under 5MB
- Provide poster image for preview
- Always include fallback image

### Fonts
**Location:** `frontend/assets/fonts/`

**Current:** Using Google Fonts CDN (Noto Sans KR)

**If Self-Hosting:**
- Use WOFF2 format (best compression)
- Subset fonts (Korean glyphs only)
- Preload critical fonts

---

## Debugging Tips

### Common Issues

**Issue: Styles Not Applying**
- Check CSS import order in HTML
- Verify class name spelling
- Check browser DevTools for specificity conflicts
- Clear browser cache

**Issue: JavaScript Not Running**
- Check console for errors
- Verify DOMContentLoaded wrapper
- Check file path in script tag
- Ensure element exists before accessing

**Issue: Mobile Menu Not Working**
- Check media query breakpoint
- Verify hamburger button event listener
- Check z-index stacking
- Test JavaScript in mobile viewport

**Issue: Animation Stuttering**
- Use CSS transforms instead of position changes
- Check for forced reflows (layout thrashing)
- Reduce animation complexity
- Use will-change property sparingly

### DevTools Workflows

**CSS Debugging:**
1. Right-click element → Inspect
2. Check computed styles tab
3. Toggle CSS properties on/off
4. Edit values live to test

**JavaScript Debugging:**
1. Add breakpoints in Sources tab
2. Use console.log strategically
3. Check Network tab for API issues
4. Use Performance tab for animation issues

---

## Korean Language Guidelines

### Content Tone
- Formal but friendly (존댓말)
- Clear and concise
- Encouraging and supportive
- Avoid jargon where possible

### Common Terms
- 전공: Major
- 검사: Test/Assessment
- 결과: Results
- 학과: Department
- 추천: Recommendation
- 분석: Analysis
- 유형: Type

### Typography
- Use appropriate Korean fonts (Noto Sans KR)
- Proper spacing between Korean and Latin characters
- Use Korean punctuation (。,! ?)
- Break lines at natural Korean phrase boundaries

---

## Contact & Support

**Team Members:**
- 강민석 (Kang Min-seok)
- 유지헌 (Yoo Ji-heon)
- 조현우 (Cho Hyun-woo)

**Institution:**
전주대학교 (Jeonju University)

**Project Year:** 2025

---

## Version History

**Current Version:** 1.0.0 (Initial Release)

**Change Log:**
- 2025-11-17: Initial CLAUDE.md creation with comprehensive codebase documentation

---

## Quick Reference

### File Paths Cheat Sheet
```
Frontend Entry: /frontend/index.html
Design Tokens:  /frontend/css/variables.css
Common Styles:  /frontend/css/common.css
Header Styles:  /frontend/css/components/header.css
Button Styles:  /frontend/css/components/button.css
Main Page CSS:  /frontend/css/pages/main.css
Header JS:      /frontend/js/components/header.js
Main Page JS:   /frontend/js/pages/main.js
Backend API:    /main.py
```

### Essential Commands
```bash
# Run Frontend (Python HTTP Server)
cd frontend && python -m http.server 8000

# Run Backend (FastAPI)
uvicorn main:app --reload

# Test API
# Use test_main.http with REST Client extension
```

### Key CSS Classes
```css
.container          /* Max-width centered container */
.section            /* Standard section padding */
.section-title      /* Centered section heading */
.btn                /* Base button */
.btn-glass          /* Glassmorphism button */
.btn-primary        /* Solid gradient button */
.btn-outline        /* Outline button */
.hero-section       /* Full-screen hero */
.feature-card       /* Feature showcase card */
```

---

**Last Updated:** 2025-11-17
**Maintained By:** Development Team + AI Assistants
