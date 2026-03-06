# FlashForge — Flashcard Pedagogy & Vocabulary Card Specification

**Version:** 1.0  
**Purpose:** This document defines the educational philosophy, card design rules, and JSON data template for FlashForge vocabulary flashcards. It is the authoritative reference for all LLM prompt design, card generation, and quality review. Every design decision is grounded in second language acquisition (SLA) research and real learner experience.

---

## 1. Core Philosophy

### 1.1 What We Are Building

FlashForge generates vocabulary flashcard decks from educational input (textbook chapters, course materials, word lists). The tool is **language-agnostic** and **textbook-agnostic** — it works for Korean, Spanish, Arabic, Mandarin, or any target language. The input defines the vocabulary; FlashForge builds the scaffolding around it.

We focus exclusively on **vocabulary acquisition**. Grammar, expressions, and dialogue comprehension are valuable but variable across languages and curricula. Vocabulary is the universal bottleneck: it is the single strongest predictor of overall language ability (Nation, 2001; Laufer, 1989; Schmitt, 2010), it is what SRS is best suited for (Cozzens & Bartolotti, 2024), and it is where learners most often stall — not because vocabulary is hard, but because it is boring. FlashForge exists to make vocabulary study rich, multi-sensory, and effective.

### 1.2 Guiding Principles

**One word, deep knowledge.** Nation's (2013) word knowledge framework identifies 18 aspects of knowing a word across form, meaning, and use — each with receptive and productive dimensions. A single flashcard tests one sliver of that knowledge. FlashForge generates **five card types per vocabulary word**, each targeting a different aspect of word knowledge, each using a unique example sentence. This gives the learner 5 distinct, meaningful encounters with each word — approaching the 8–12 encounters research indicates are needed to establish a stable mental representation (Webb, 2007; Conti, 2025).

**Comprehensible input in every sentence.** Krashen's input hypothesis (i+1) and Nation's research on text coverage converge on a clear rule: learners need to understand 90–98% of the language around a new word for acquisition to occur (Hu & Nation, 2000; Laufer, 1989). When example sentences contain 3 unknown words, they become noise. Every example sentence in FlashForge must be overwhelmingly comprehensible, with the target word as the only challenge.

**Scaffolded progression from receptive to productive.** Vocabulary knowledge develops incrementally (Henriksen, 1999; Schmitt, 1998). Learners first recognize a word's form, then connect form to meaning, then use it in context, then produce it. The five card types follow this natural acquisition order: recognition → contextual use → production → sentence comprehension → listening.

**Audio is not decoration — it is a learning modality.** Multimodal presentation (combining written form, pronunciation, and contextual audio) produces significantly better retention than translation alone (Barcroft, 2004). But audio must be strategically placed: on the *back* of cards where the learner is producing (to confirm, not reveal), and on the *front* of listening cards (to train the receptive spoken-form skill). Audio that gives away an answer defeats the purpose entirely.

**Retrieval practice over passive review.** Karpicke and Roediger (2008) demonstrated that active recall produces dramatically better long-term retention than passive re-exposure. Every card must require the learner to retrieve something from memory before seeing the answer. Cards that can be "read through" without mental effort are pedagogically empty.

**The learner should never feel tricked.** If a card could have multiple correct answers, it is a bad card. If the learner has to get it wrong once to learn what the card wanted, it is a bad card. Cards must be unambiguous, fair, and solvable with the knowledge available. This is not a test — it is practice. Anxiety raises the affective filter and blocks acquisition (Krashen, 1982).

**We are one part of a larger learning ecosystem.** FlashForge does not teach grammar, does not replace textbook study, does not substitute for reading or conversation practice. It does one thing: it helps learners internalize vocabulary through spaced, multi-modal, scaffolded retrieval practice. We do not add crutches (like romanization for non-Latin scripts) because we expect learners to develop those skills through their broader study. We do not try to do everything — we try to do vocabulary excellently.

---

## 2. The Five Card Types

Each vocabulary word generates exactly **five cards** from a single note. Each card targets a different dimension of word knowledge, uses a different example sentence, and handles audio differently. The cards are ordered from easiest (receptive recognition) to hardest (pure listening comprehension).

### Card 1: Recognition
**What it tests:** Receptive form-meaning link — "I see the word, do I know what it means?"  
**Nation dimension:** Form (written) → Meaning (form-meaning connection), Receptive

| Side | Content |
|------|---------|
| **Front** | Target word in target language + Example sentence (target word **highlighted**) |
| **Back** | English translation of word + English translation of sentence + Audio: isolated word pronunciation + Audio: example sentence |

**Design rationale:** This is the entry point. The learner sees the word, reads it in a simple context, and tries to recall the meaning. Audio plays only on the back as reinforcement after the learner has attempted recall. The example sentence provides a first contextual encounter. This card builds the foundational form-meaning link that all other cards depend on.

**Audio placement:** Back only. Audio here is confirmation and pronunciation modeling, not a prompt.

---

### Card 2: Contextual Recall (Cloze)
**What it tests:** Productive meaning recall in context — "Given a sentence with a blank and an English hint, can I produce the right word?"  
**Nation dimension:** Meaning (form-meaning connection) + Use (grammatical function, collocation), Productive

| Side | Content |
|------|---------|
| **Front** | Sentence in target language with target word blanked `{{c1::targetword}}` + English hint: the English meaning of the target word in parentheses |
| **Back** | Complete sentence with target word revealed + English translation of full sentence + Audio: complete sentence |

**Design rationale:** The cloze card is the most commonly misdesigned card type. The critical failure mode is ambiguity — if you blank a noun and almost any noun could fit, the card is useless. The English hint solves this completely and cheaply: it tells the learner *what* to produce without telling them *how* to produce it in the target language. This tests whether the learner can go from meaning → form, which is the productive direction.

**The English hint is mandatory.** Without it, cloze cards are guessing games. With it, they are focused retrieval practice exercises.

**Audio placement:** Back only. The complete sentence audio plays after the learner has attempted the answer, reinforcing the word in its spoken context.

---

### Card 3: Production
**What it tests:** Productive form recall — "I see the English word, can I recall the target language word?"  
**Nation dimension:** Form (written, spoken) → Meaning (form-meaning connection), Productive

| Side | Content |
|------|---------|
| **Front** | English word only (no audio, no sentence, no hints) |
| **Back** | Target word in target language + New example sentence (different from Cards 1 and 2) + English translation of sentence + Audio: isolated word pronunciation + Audio: example sentence |

**Design rationale:** This is the hardest text-based card. The learner sees only the English and must retrieve the target-language form from memory. No context clues, no audio hints. The back then rewards the effort with the word, a brand new example sentence (another contextual encounter), and audio for pronunciation reinforcement.

**Audio placement:** Back only, strictly. Audio on the front of a production card gives away the answer — this was a real bug in earlier versions and must never happen.

---

### Card 4: Sentence Comprehension
**What it tests:** Receptive use in context — "I see a full sentence using this word. Can I understand what it means?"  
**Nation dimension:** Meaning (concepts and referents) + Use (collocations, constraints), Receptive

| Side | Content |
|------|---------|
| **Front** | New example sentence in target language (target word present but **not** highlighted — the learner must parse the whole sentence) |
| **Back** | English translation of the sentence + Target word highlighted with its individual translation + Audio: full sentence |

**Design rationale:** This card reverses the typical direction. Instead of going from an isolated word to its meaning, the learner encounters the word naturally embedded in a sentence and must comprehend the whole. This is closest to real reading/listening comprehension. The word is not highlighted on the front because the learner should be processing the sentence holistically, not just scanning for one word.

**Audio placement:** Back only. The sentence audio on the back lets the learner hear the natural spoken form of what they just read, connecting written and spoken input.

---

### Card 5: Listening Comprehension
**What it tests:** Receptive spoken form — "I hear the word in a sentence. Can I understand it?"  
**Nation dimension:** Form (spoken) → Meaning (form-meaning connection), Receptive

| Side | Content |
|------|---------|
| **Front** | Audio only: a new example sentence containing the target word (auto-plays). No text. |
| **Back** | Full sentence in target language (written) + Target word highlighted + English translation of sentence + English translation of target word + Audio: replay button for the sentence + Audio: isolated word pronunciation |

**Design rationale:** This is the most advanced card and the one learners report valuing most. Pure listening forces the learner to process the spoken form without any written scaffolding. This directly trains the skill that matters in real conversation: hearing a word you know and understanding it at natural speed. The back provides full written support so the learner can check their comprehension and see exactly what they heard.

This card uses a **fifth unique example sentence** — another novel encounter with the word in a different context, maximizing the diversity of the learner's semantic network for this word.

**Audio placement:** Front (as the primary prompt). This is the only card type where audio appears on the front, because the audio IS the test.

---

## 3. Example Sentence Requirements

Example sentences are the backbone of every card. Bad sentences ruin good cards. The following rules are non-negotiable.

### 3.1 The i+1 Rule

Every example sentence must be **comprehensible input**. The target word should be the **only** unknown element. All other words in the sentence must be:

- Words from the same chapter/input material that the learner is expected to know, OR
- Very high-frequency, universally-known words that any learner at this level would recognize (equivalents of "I", "the", "is", "go", "eat", "good" in the target language)

**Concretely:** If you are generating cards for Chapter 5 vocabulary, the example sentences may use vocabulary from Chapters 1–5 and basic universal words. They must NOT use vocabulary from Chapter 8 or low-frequency words that a learner at this level has not encountered.

The LLM prompt must include: *"Use only words from the provided input text and basic, universally-known words at the learner's level. The target vocabulary word should be the only challenging element in each sentence. When in doubt, simpler is always better."*

### 3.2 Simplicity Over Cleverness

Sentences should be **short** (5–10 words is ideal for beginners, up to 12–15 for intermediate). They should express simple, concrete, everyday situations. Abstract or culturally complex sentences are harder to parse and add unnecessary cognitive load.

Good: "I eat rice every morning."  
Bad: "The unprecedented culinary traditions of the region emphasize rice."

Good: "My friend is tall."  
Bad: "Among the group, his stature was remarkably distinguishable."

### 3.3 Five Unique Sentences Per Word

Each word requires **five different example sentences**, one per card type. These sentences should show the word used in **different contexts** to build a rich semantic network (Webb, 2007). Varied contexts help learners generalize the word's meaning rather than associating it with a single memorized phrase.

For a word like "to buy" (사다 in Korean):
1. Card 1 (Recognition): "I **buy** fruit at the store."
2. Card 2 (Cloze): "My mom ___ bread every Saturday." (hint: to buy)
3. Card 3 (Production): "We bought new shoes yesterday."
4. Card 4 (Sentence Comprehension): "My older brother buys coffee every day."
5. Card 5 (Listening): "I want to buy a gift for my friend."

Note how each sentence uses different subjects, objects, and time frames while remaining simple and comprehensible. The word appears in slightly different grammatical forms where natural for the target language.

### 3.4 Sentence Complexity Progression

While all sentences must be comprehensible, they may increase slightly in complexity across the five cards to match the scaffolded difficulty:

- **Cards 1–2:** Simplest possible. Short, direct, present tense preferred.
- **Card 3:** Slightly varied (different tense or sentence structure, still simple).
- **Cards 4–5:** Can be marginally longer or use a different grammatical pattern, since these cards test comprehension rather than production.

This is a soft guideline, not a hard rule. Simplicity always wins over variety.

---

## 4. Audio Specification

### 4.1 Audio Files Per Word

Each vocabulary word generates the following audio files:

| Audio File | Content | Used In |
|------------|---------|---------|
| `word_isolated` | The target word spoken in isolation, clearly | Cards 1, 3, 5 (back) |
| `sentence_1` | Example sentence from Card 1 | Card 1 (back) |
| `sentence_2` | Example sentence from Card 2 (cloze, complete version) | Card 2 (back) |
| `sentence_3` | Example sentence from Card 3 | Card 3 (back) |
| `sentence_4` | Example sentence from Card 4 | Card 4 (back) |
| `sentence_5` | Example sentence from Card 5 | Card 5 (front and back) |

**Total: 7 audio files per vocabulary word** (1 isolated word + 5 sentences + the isolated word is reused).

### 4.2 Audio Placement Rules (Non-Negotiable)

| Card Type | Front Audio | Back Audio |
|-----------|-------------|------------|
| Card 1: Recognition | None | Word + Sentence |
| Card 2: Cloze | None | Sentence (complete) |
| Card 3: Production | **None — NEVER** | Word + Sentence |
| Card 4: Sentence Comprehension | None | Sentence |
| Card 5: Listening | Sentence (auto-play) | Sentence (replay) + Word |

**The rule is simple:** Audio on the front is only allowed when audio IS the test (Card 5). On all other cards, audio appears exclusively on the back as reinforcement after the learner has attempted recall.

### 4.3 TTS Query Cleaning

The text sent to TTS must be **clean target-language text only**. Before generating audio:

- Remove all cloze syntax: `{{c1::word}}` → `word`
- Remove all English text, parentheticals, hints
- Remove all HTML tags and formatting
- Strip trailing whitespace and punctuation artifacts

---

## 5. JSON Data Schema

The JSON file is the single source of truth for deck generation. Every vocabulary word is a single object containing all five cards' worth of data.

### 5.1 Top-Level Structure

```json
{
  "schema_version": 1,
  "source_info": {
    "title": "Korean Lesson 5 - Shopping",
    "source_language": "ko",
    "target_language_name": "Korean",
    "level_description": "Beginner, Chapter 5",
    "available_vocabulary_context": "Words from chapters 1-5 may be used in example sentences."
  },
  "vocabulary": [
    { ... }
  ]
}
```

### 5.2 Vocabulary Entry

Each entry in the `vocabulary` array represents one word and contains all data needed to generate five cards and their associated audio.

```json
{
  "id": "uuid-string",
  "target_word": "사다",
  "target_word_romanization": "",
  "english_translation": "to buy",
  "part_of_speech": "verb",
  "category": "Shopping",
  "notes": "",
  "generate_audio": true,
  
  "card_1_recognition": {
    "sentence_target": "저는 가게에서 과일을 사요.",
    "sentence_target_highlight": "저는 가게에서 과일을 <b>사요</b>.",
    "sentence_english": "I buy fruit at the store."
  },
  
  "card_2_cloze": {
    "sentence_cloze": "엄마는 토요일마다 빵을 {{c1::사요}}.",
    "sentence_english": "My mom buys bread every Saturday.",
    "english_hint": "to buy"
  },
  
  "card_3_production": {
    "sentence_target": "우리는 어제 새 신발을 샀어요.",
    "sentence_english": "We bought new shoes yesterday."
  },
  
  "card_4_comprehension": {
    "sentence_target": "형은 매일 커피를 사요.",
    "sentence_english": "My older brother buys coffee every day.",
    "word_in_sentence_highlight": "형은 매일 커피를 <b>사요</b>.",
    "word_translation_in_context": "buys"
  },
  
  "card_5_listening": {
    "sentence_target": "저는 친구에게 줄 선물을 사고 싶어요.",
    "sentence_english": "I want to buy a gift for my friend.",
    "word_in_sentence_highlight": "저는 친구에게 줄 선물을 <b>사고 싶어요</b>.",
    "word_translation_in_context": "want to buy"
  },
  
  "audio_queries": {
    "word_isolated": "사다",
    "sentence_1": "저는 가게에서 과일을 사요.",
    "sentence_2": "엄마는 토요일마다 빵을 사요.",
    "sentence_3": "우리는 어제 새 신발을 샀어요.",
    "sentence_4": "형은 매일 커피를 사요.",
    "sentence_5": "저는 친구에게 줄 선물을 사고 싶어요."
  }
}
```

### 5.3 Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Stable UUID. Assigned once, never changes. Used for Anki GUID generation. |
| `target_word` | Yes | The word in its dictionary/base form in the target language. |
| `target_word_romanization` | No | Optional romanization. Left empty by default; user may populate if desired. Not shown on cards — available as metadata only. |
| `english_translation` | Yes | Concise English translation. Should be the primary, most common meaning. |
| `part_of_speech` | Yes | Noun, verb, adjective, adverb, particle, etc. |
| `category` | No | Thematic grouping from the source material (e.g., "Food", "Travel", "Greetings"). |
| `notes` | No | Optional free-text field for user annotations. Not shown on cards. |
| `generate_audio` | Yes | Boolean. Per-word audio toggle. Defaults to true. |
| `card_N_*` | Yes | Each card's sentence data. See card type specifications above. |
| `audio_queries` | Yes | Clean target-language text strings to send to TTS. Pre-cleaned: no cloze syntax, no English, no HTML. |

### 5.4 Schema Design Rationale

**Why is everything in one object?** A vocabulary word is a single unit of knowledge. The five cards are five *views* of the same knowledge. Storing them together ensures consistency (the same English translation appears everywhere) and makes editing simple (change the word once, it updates everywhere).

**Why are audio_queries pre-computed?** TTS requires clean target-language text. By computing these at generation time (stripping cloze brackets, HTML, English hints), we prevent bugs in the deck builder and make the TTS pipeline a simple loop over strings.

**Why no romanization on cards?** Romanization is a crutch that delays the learner's ability to read the target script. Learners of Korean, Japanese, Arabic, etc. should be developing reading fluency through their broader study. FlashForge is not a reading tutor — it is a vocabulary tutor. The romanization field exists as optional metadata for user convenience, not as a card display element.

---

## 6. LLM Generation Pipeline

### 6.1 Three-Step Process

The generation pipeline uses three LLM calls, each with a distinct focus:

**Step 1: Extraction & Card Drafting (Pedagogical Focus)**
- Input: Raw extracted text from the user's source material
- System prompt: References this philosophy document. Instructs the LLM to act as an experienced language teacher designing vocabulary flashcards.
- Task: Identify vocabulary words, generate English translations, write all five example sentences per word, create cloze versions with hints.
- Output: Semi-structured text with card content. Does NOT need to be valid JSON. Focus is entirely on content quality — good translations, good sentences, correct difficulty level.

**Step 2: Review & Quality Check (QA Focus)**
- Input: The Step 1 output + the original extracted text (for reference)
- System prompt: Instructs the LLM to act as a quality reviewer checking against specific criteria from this document.
- Task: Review every sentence against the i+1 rule. Flag sentences that use words not present in the source material or not universally known at this level. Check that each word has 5 genuinely different sentences. Check that cloze cards have unambiguous answers with the English hint. Check that no audio would appear on the front of production cards. Fix any issues found.
- Output: Corrected, reviewed card content.

**Step 3: Structuring (Formatting Focus)**
- Input: The reviewed output from Step 2
- System prompt: Contains the exact JSON schema from section 5.2. Instructs strict JSON-only output.
- Task: Convert the reviewed content into valid JSON matching the schema. Generate UUIDs. Compute audio_queries by stripping formatting from sentences. Generate highlighted versions of sentences.
- Output: Valid JSON. Validated by Pydantic.

### 6.2 Why Three Steps

The two-step pipeline from the original technical plan (create → structure) missed a critical failure mode: the LLM generates sentences that look fine individually but violate the i+1 rule or contain ambiguous cloze deletions. These errors are invisible at creation time and only become obvious during review. Adding a dedicated review step catches these issues before they reach the learner.

The review step also has access to the *original source text*, which lets it verify that example sentences only use vocabulary from the source material. Step 1 might "know" this rule but still drift; Step 2 explicitly checks it.

### 6.3 Sentence Generation Constraints for LLM Prompts

The following constraints must appear in the Step 1 prompt (card drafting):

> **Sentence Rules:**
> 1. Every example sentence must use the target vocabulary word.
> 2. All other words in the sentence must come from the provided source text or be basic, universally-known words at the learner's stated level. Do not use words the learner has not encountered.
> 3. Sentences should be 5–10 words for beginner levels, up to 12–15 for intermediate.
> 4. Each of the 5 sentences for a word must use a DIFFERENT context (different subject, different object, different situation, different time frame).
> 5. Sentences must express simple, concrete, everyday situations. No abstract language.
> 6. For cloze sentences: the blank must have exactly ONE correct answer given the English hint. If multiple words could fill the blank even with the hint, rewrite the sentence to be more specific.
> 7. The word may appear in different conjugated/inflected forms across sentences where natural for the language.
> 8. Do not reuse the same sentence structure across the five sentences. Vary the patterns.

The following constraints must appear in the Step 2 prompt (review):

> **Review Checklist:**
> 1. For each sentence: Does every non-target word appear in the source text or qualify as universally basic? If not, replace the unfamiliar word with one from the source text.
> 2. For each cloze: Given only the sentence and the English hint, is there exactly one correct answer? Try to think of alternative answers. If any exist, rewrite the sentence.
> 3. Are all five sentences genuinely different contexts? If two sentences are structurally similar (same subject, same pattern), rewrite one.
> 4. Is any sentence longer than 15 words? If so, simplify it.
> 5. Would the audio of any sentence, if played, give away the answer on a card where the learner is supposed to be producing the word? (This should never happen given the card design, but verify.)

---

## 7. Anki Note Model Design

### 7.1 Note Type

FlashForge uses a single Anki note type that generates five cards via five card templates. This is a core Anki feature: one note with many fields can produce multiple cards, each showing different fields on front and back.

**Note Type Name:** `FlashForge Vocab`

**Fields:**
1. `TargetWord` — The word in the target language
2. `EnglishTranslation` — English meaning
3. `PartOfSpeech` — Part of speech tag
4. `Sentence1` — Card 1 sentence (with highlight HTML)
5. `Sentence1English` — Card 1 sentence English translation
6. `Sentence2Cloze` — Card 2 cloze sentence (with `{{c1::}}` syntax)
7. `Sentence2English` — Card 2 sentence English translation
8. `ClozeHint` — English hint for the cloze
9. `Sentence3` — Card 3 sentence (target language)
10. `Sentence3English` — Card 3 English translation
11. `Sentence4` — Card 4 sentence (no highlight on front)
12. `Sentence4Highlight` — Card 4 sentence (with highlight, for back)
13. `Sentence4English` — Card 4 English translation
14. `Sentence4WordContext` — Target word's contextual translation in Card 4
15. `Sentence5` — Card 5 sentence (target language, for back display)
16. `Sentence5Highlight` — Card 5 sentence (with highlight, for back)
17. `Sentence5English` — Card 5 English translation
18. `Sentence5WordContext` — Target word's contextual translation in Card 5
19. `AudioWord` — `[sound:filename.mp3]` for isolated word
20. `AudioSentence1` — `[sound:filename.mp3]` for sentence 1
21. `AudioSentence2` — `[sound:filename.mp3]` for sentence 2
22. `AudioSentence3` — `[sound:filename.mp3]` for sentence 3
23. `AudioSentence4` — `[sound:filename.mp3]` for sentence 4
24. `AudioSentence5` — `[sound:filename.mp3]` for sentence 5

### 7.2 Card Templates (Summary)

| Template | Front Shows | Back Shows |
|----------|-------------|------------|
| 1: Recognition | TargetWord + Sentence1 | EnglishTranslation + Sentence1English + AudioWord + AudioSentence1 |
| 2: Cloze | Sentence2Cloze + ClozeHint | Revealed word + Sentence2English + AudioSentence2 |
| 3: Production | EnglishTranslation | TargetWord + Sentence3 + Sentence3English + AudioWord + AudioSentence3 |
| 4: Comprehension | Sentence4 (no highlight) | Sentence4Highlight + Sentence4English + Sentence4WordContext + AudioSentence4 |
| 5: Listening | AudioSentence5 (auto-play) | Sentence5Highlight + Sentence5English + Sentence5WordContext + AudioWord + AudioSentence5 |

### 7.3 CSS Guidelines

- Target word highlights should use a distinct but non-distracting style (e.g., bold + subtle color).
- Card type should be labeled subtly (e.g., small text at top: "Recognition", "Cloze", "Production", "Comprehension", "Listening") so the learner knows what's expected.
- Font size should be generous for target language text, especially for non-Latin scripts.
- English text should be visually secondary (smaller, lighter color) so the learner's eyes go to the target language first.
- Audio buttons should be large and obvious on Card 5's front.

---

## 8. What We Deliberately Exclude

### 8.1 Grammar Cards
Grammar is language-specific and highly variable. A cloze card that tests a grammar pattern (e.g., conjugation) without testing vocabulary is a different pedagogical exercise that requires different design principles. Out of scope for v1.

### 8.2 Reading/Dialogue Cards
Taking sentences from a dialogue and putting them on flashcards out of order is confusing and pedagogically questionable. Dialogue comprehension is better served by re-reading the dialogue, not by flashcards. Out of scope.

### 8.3 Romanization/Transliteration on Cards
Displaying romanization trains learners to read romanization, not the target script. Learners of non-Latin scripts should develop reading fluency through dedicated study. FlashForge stores romanization as optional metadata but never displays it on card faces.

### 8.4 Frequency Analysis
While word frequency data is valuable for curriculum design, it is out of scope for v1. FlashForge uses the user's input text as its vocabulary corpus. The LLM prompt constrains sentences to use vocabulary from that corpus, which naturally keeps sentences at the learner's level without requiring frequency databases.

---

## 9. Quality Criteria Checklist

Use this checklist to evaluate generated cards before export. Every card should pass all applicable checks.

**Per Word:**
- [ ] English translation is accurate and concise (1–4 words)
- [ ] Part of speech is correct
- [ ] All 5 sentences are genuinely different contexts
- [ ] No two sentences share the same subject AND the same sentence structure

**Per Sentence:**
- [ ] Target word appears in the sentence
- [ ] All non-target words are from the source material or universally basic
- [ ] Sentence length is appropriate (5–15 words depending on level)
- [ ] Sentence expresses a concrete, everyday situation
- [ ] Sentence is grammatically correct in the target language

**Card 2 (Cloze) Specific:**
- [ ] English hint is present
- [ ] Blank has exactly one correct answer given the hint and context
- [ ] No other word could reasonably replace the blank

**Audio:**
- [ ] Audio queries contain only clean target-language text
- [ ] No cloze syntax in audio queries
- [ ] No English text in audio queries
- [ ] Audio is placed on correct card sides (back for Cards 1–4, front for Card 5)

---

## 10. References

- Barcroft, J. (2004). Second language vocabulary acquisition: A lexical input processing approach. *Foreign Language Annals*, 37, 200–208.
- Henriksen, B. (1999). Three dimensions of vocabulary development. *Studies in Second Language Acquisition*, 21(2), 303–317.
- Hu, M. & Nation, P. (2000). Unknown word density and reading comprehension. *Reading in a Foreign Language*, 13(1), 403–430.
- Karpicke, J. D. & Roediger, H. L. (2008). The critical importance of retrieval for learning. *Science*, 319, 966–968.
- Krashen, S. (1982). *Principles and practice in second language acquisition*. Pergamon Press.
- Laufer, B. (1989). What percentage of text-lexis is essential for comprehension? In C. Lauren & M. Nordman (Eds.), *Special Language: From Humans to Thinking Machines*.
- Nation, I. S. P. (2001). *Learning vocabulary in another language*. Cambridge University Press.
- Nation, I. S. P. (2013). *Learning vocabulary in another language* (2nd ed.). Cambridge University Press.
- Schmitt, N. (2010). *Researching vocabulary: A vocabulary research manual*. Palgrave Macmillan.
- Webb, S. (2007). The effects of repetition on vocabulary knowledge. *Applied Linguistics*, 28(1), 46–65.
- Webb, S. (2008). The effects of context on incidental vocabulary learning. *Reading in a Foreign Language*, 20(2), 232–245.
