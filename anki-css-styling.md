# AutoAnki CSS Styling Guide

A comprehensive guide for creating clean, effective, and mobile-responsive Anki card templates for language learning.

## Overview

AutoAnki generates cards using a single note type with 24 fields and 5 card templates. This document provides the CSS and template structure needed for professional-quality flashcards that work across all Anki platforms (Desktop, AnkiMobile, AnkiDroid, AnkiWeb).

## Core Design Principles

### Pedagogical CSS
- **Target language prominence**: Larger font size for target language text
- **English secondary**: Smaller, lighter color for translations
- **Minimal distractions**: Clean layout that focuses attention on the learning task
- **Highlight subtlety**: Bold + soft color for target words (not jarring)
- **Clear card type labeling**: Small label at top so learners know what's expected

### Technical Requirements
- **Mobile-responsive**: Must work on phones with various screen sizes
- **Night mode compatible**: Use `.nightMode` class for dark theme
- **Cross-platform**: Works on Desktop, iOS, Android, and Web
- **Font flexibility**: System fonts with fallbacks for non-Latin scripts

## Note Type Structure

### Fields (24 total)

1. `TargetWord` – The word in target language
2. `EnglishTranslation` – English meaning
3. `PartOfSpeech` – Part of speech tag
4. `Sentence1` – Card 1 sentence (with `<b>` highlight)
5. `Sentence1English` – Card 1 English translation
6. `Sentence2Cloze` – Card 2 cloze sentence (with `{{c1::}}`)
7. `Sentence2English` – Card 2 English translation
8. `ClozeHint` – English hint for the cloze
9. `Sentence3` – Card 3 sentence (target language)
10. `Sentence3English` – Card 3 English translation
11. `Sentence4` – Card 4 sentence (no highlight)
12. `Sentence4Highlight` – Card 4 sentence (with `<b>` highlight)
13. `Sentence4English` – Card 4 English translation
14. `Sentence4WordContext` – Contextual translation (e.g., "buys")
15. `Sentence5` – Card 5 sentence (target language)
16. `Sentence5Highlight` – Card 5 sentence (with `<b>` highlight)
17. `Sentence5English` – Card 5 English translation
18. `Sentence5WordContext` – Contextual translation
19. `AudioWord` – `[sound:filename.mp3]` for isolated word
20. `AudioSentence1` – `[sound:filename.mp3]` for sentence 1
21. `AudioSentence2` – `[sound:filename.mp3]` for sentence 2
22. `AudioSentence3` – `[sound:filename.mp3]` for sentence 3
23. `AudioSentence4` – `[sound:filename.mp3]` for sentence 4
24. `AudioSentence5` – `[sound:filename.mp3]` for sentence 5

## CSS Styling

### Shared CSS (Applied to All Cards)

```css
/* ============================================
   BASE STYLES - Shared across all cards
   ============================================ */

/* Card container */
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 24px;
  text-align: center;
  color: #333;
  background-color: #f9f9f9;
  line-height: 1.6;
  padding: 20px;
}

/* Night mode base */
.nightMode .card {
  color: #e0e0e0;
  background-color: #2d2d2d;
}

/* Card type label (small, top of card) */
.card-type {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #666;
  margin-bottom: 15px;
}

.nightMode .card-type {
  color: #999;
}

/* Target language text - prominent */
.target {
  font-size: 32px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 15px 0;
}

.nightMode .target {
  color: #f0f0f0;
}

/* Non-Latin scripts (Korean, Japanese, Chinese, Arabic, etc.) */
.target-cjk {
  font-size: 36px;  /* Even larger for character-based scripts */
  line-height: 1.4;
}

/* Target word highlighting */
.highlight {
  font-weight: 600;
  color: #2563eb;
}

.nightMode .highlight {
  color: #60a5fa;
}

/* English text - secondary */
.english {
  font-size: 18px;
  color: #666;
  font-style: italic;
  margin: 10px 0;
}

.nightMode .english {
  color: #999;
}

/* Part of speech tag */
.pos {
  font-size: 14px;
  font-weight: 500;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 5px 0;
}

.nightMode .pos {
  color: #aaa;
}

/* Sentence styling */
.sentence {
  font-size: 24px;
  margin: 20px 0;
  line-height: 1.5;
}

/* Cloze deletion styling */
.cloze {
  font-weight: 600;
  color: #2563eb;
}

.nightMode .cloze {
  color: #60a5fa;
}

/* Hint styling */
.hint {
  font-size: 16px;
  color: #666;
  font-style: italic;
  margin-top: 10px;
}

.nightMode .hint {
  color: #999;
}

/* Answer separator line */
hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 20px 0;
}

.nightMode hr {
  border-top-color: #555;
}

/* Audio button styling */
.replay-button {
  width: 40px;
  height: 40px;
  margin: 10px auto;
}

.replay-button svg {
  fill: #2563eb;
}

.nightMode .replay-button svg {
  fill: #60a5fa;
}

/* Contextual translation */
.context {
  font-size: 16px;
  color: #555;
  font-weight: 500;
}

.nightMode .context {
  color: #bbb;
}

/* ============================================
   PLATFORM-SPECIFIC ADJUSTMENTS
   ============================================ */

/* Mobile devices - larger touch targets, adjusted spacing */
.mobile .card {
  font-size: 22px;
  padding: 15px;
}

.mobile .target {
  font-size: 30px;
}

.mobile .target-cjk {
  font-size: 34px;
}

.mobile .sentence {
  font-size: 22px;
}

.mobile .english {
  font-size: 16px;
}

/* iOS specific */
.iphone .card,
.ipad .card {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}

/* Android specific */
.android .card {
  font-family: "Roboto", sans-serif;
}

/* Desktop - can be slightly more compact */
.win .card,
.mac .card,
.linux .card {
  max-width: 800px;
  margin: 0 auto;
}

/* ============================================
   CARD-SPECIFIC STYLES
   ============================================ */

/* Card 1: Recognition - word + sentence */
.card-recognition .target {
  margin-bottom: 25px;
}

/* Card 3: Production - English only on front */
.card-production-front .english {
  font-size: 28px;
  font-style: normal;
  font-weight: 500;
  color: #1a1a1a;
}

.nightMode .card-production-front .english {
  color: #f0f0f0;
}

/* Card 5: Listening - large audio on front */
.card-listening-front {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 200px;
}

.card-listening-front .replay-button {
  width: 60px;
  height: 60px;
  margin: 20px auto;
}

/* Card type indicators */
.type-recognition::before { content: "Recognition"; }
.type-cloze::before { content: "Fill in the Blank"; }
.type-production::before { content: "Recall"; }
.type-comprehension::before { content: "Comprehension"; }
.type-listening::before { content: "Listening"; }

/* ============================================
   UTILITY CLASSES
   ============================================ */

.hidden {
  display: none !important;
}

.text-left {
  text-align: left;
}

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 10px; }
.mb-2 { margin-bottom: 20px; }
.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 10px; }
.mt-2 { margin-top: 20px; }
```

## Card Templates

### Card 1: Recognition

**Front Template:**
```html
<div class="card-type type-recognition"></div>
<div class="target">{{TargetWord}}</div>
<div class="pos">{{PartOfSpeech}}</div>
<hr>
<div class="sentence">{{Sentence1}}</div>
```

**Back Template:**
```html
{{FrontSide}}

<hr id="answer">

<div class="english">{{EnglishTranslation}}</div>
<div class="english sentence">{{Sentence1English}}</div>

{{AudioWord}}
{{AudioSentence1}}
```

### Card 2: Cloze

**Front Template:**
```html
<div class="card-type type-cloze"></div>
<div class="sentence">{{Sentence2Cloze}}</div>
<div class="hint">({{ClozeHint}})</div>
```

**Back Template:**
```html
{{FrontSide}}

<hr id="answer">

<div class="sentence">{{Sentence2Cloze}}</div>
<div class="english">{{Sentence2English}}</div>

{{AudioSentence2}}
```

### Card 3: Production

**Front Template:**
```html
<div class="card-type type-production"></div>
<div class="card-production-front">
  <div class="english">{{EnglishTranslation}}</div>
  <div class="pos">{{PartOfSpeech}}</div>
</div>
<!-- NO AUDIO ON FRONT - This is critical for production cards -->
```

**Back Template:**
```html
{{FrontSide}}

<hr id="answer">

<div class="target">{{TargetWord}}</div>
<div class="sentence">{{Sentence3}}</div>
<div class="english">{{Sentence3English}}</div>

{{AudioWord}}
{{AudioSentence3}}
```

### Card 4: Comprehension

**Front Template:**
```html
<div class="card-type type-comprehension"></div>
<div class="sentence text-left">{{Sentence4}}</div>
```

**Back Template:**
```html
{{FrontSide}}

<hr id="answer">

<div class="sentence">{{Sentence4Highlight}}</div>
<div class="context">{{Sentence4WordContext}}</div>
<div class="english">{{Sentence4English}}</div>

{{AudioSentence4}}
```

### Card 5: Listening

**Front Template:**
```html
<div class="card-type type-listening"></div>
<div class="card-listening-front">
  <div class="hint">Listen and understand</div>
  {{AudioSentence5}}
</div>
```

**Back Template:**
```html
{{FrontSide}}

<hr id="answer">

<div class="sentence">{{Sentence5Highlight}}</div>
<div class="context">{{Sentence5WordContext}}</div>
<div class="english">{{Sentence5English}}</div>

<div class="target mt-2">{{TargetWord}}</div>

{{AudioWord}}
{{AudioSentence5}}
```

## Audio Placement Reference

| Card | Front Audio | Back Audio | Notes |
|------|-------------|------------|-------|
| 1 | None | Word + Sentence | Audio confirms after recall |
| 2 | None | Sentence | Audio confirms after filling blank |
| 3 | **NONE** | Word + Sentence | **CRITICAL**: Never audio on front |
| 4 | None | Sentence | Audio confirms comprehension |
| 5 | Sentence | Sentence + Word | Audio IS the test on front |

## Best Practices

### Font Sizes
- **Desktop target language**: 32px (24px for Latin scripts)
- **Desktop CJK scripts**: 36px (larger for readability)
- **Mobile target language**: 30px
- **English translations**: Always 25% smaller than target (e.g., 18px vs 24px)

### Colors
- **Primary text**: #333 (day), #e0e0e0 (night)
- **Highlights**: #2563eb blue (day), #60a5fa lighter blue (night)
- **Secondary text**: #666 (day), #999 (night)
- **Background**: #f9f9f9 (day), #2d2d2d (night)

### Spacing
- Use generous vertical spacing (20px between sections)
- Padding around card edges (15-20px)
- Clear visual hierarchy with size and color, not boxes

### Mobile Considerations
- Touch targets for audio buttons should be 40px minimum
- Text should reflow naturally on narrow screens
- No horizontal scrolling
- Test on actual mobile devices, not just resized desktop windows

### Accessibility
- Sufficient color contrast (WCAG AA minimum)
- Don't rely solely on color to convey information
- Font sizes should be readable without zooming
- Audio controls should be easily tappable

## Platform Quirks & Solutions

### AnkiMobile (iOS)
- Uses `-apple-system` fonts automatically
- Audio buttons styled via `.replay-button`
- Night mode class is `.nightMode`

### AnkiDroid (Android)
- May need explicit `Roboto` font family
- Some CSS3 features may not work
- Test on multiple Android versions

### AnkiWeb
- Most limited CSS support
- Stick to basic CSS properties
- Test thoroughly

### Desktop (All Platforms)
- Full CSS support
- Can use flexbox, grid, etc.
- Max-width containers recommended

## Testing Checklist

Before finalizing your CSS:

- [ ] Renders correctly in Anki Desktop (Windows, macOS, Linux)
- [ ] Renders correctly in AnkiMobile (iOS)
- [ ] Renders correctly in AnkiDroid (Android)
- [ ] Works in night mode on all platforms
- [ ] Audio buttons are tappable on mobile
- [ ] Text is readable without zooming
- [ ] No horizontal scrolling on mobile
- [ ] Card 3 (Production) has NO audio on front
- [ ] Card 5 (Listening) has audio on front
- [ ] Highlights are visible but not jarring
- [ ] English text is visually secondary

## Customization Tips

### Changing Colors
Edit the hex codes in the `.highlight`, `.card`, and `.nightMode` sections.

### Adjusting Font Sizes
Modify the `font-size` values. Keep proportions: target language should be 1.3x larger than English.

### Adding Custom Fonts
```css
@import url('https://fonts.googleapis.com/css2?family=YourFont&display=swap');

.card {
  font-family: 'YourFont', sans-serif;
}
```

**Note**: Custom fonts may not work offline on mobile. Include fallback fonts.

### RTL Languages (Arabic, Hebrew)
Add to `.card`:
```css
direction: rtl;
text-align: right;
```

## References

- [Anki Manual - Styling & HTML](https://docs.ankiweb.net/templates/styling.html)
- [Anki Mobile CSS Classes](https://forums.ankiweb.net/t/how-do-you-manage-css-for-each-platform/38428)
- [Modern Card Template Proposal](https://forums.ankiweb.net/t/modernize-default-card-templates-for-readability/53356)

---

**Remember**: Clean, readable cards lead to better learning outcomes. Avoid visual clutter. Focus the learner's attention on what matters: the language.
