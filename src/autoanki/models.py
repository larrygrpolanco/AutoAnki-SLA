from pydantic import BaseModel


class SourceInfo(BaseModel):
    title: str
    source_language: str
    target_language_name: str
    level_description: str
    available_vocabulary_context: str


class Card1Recognition(BaseModel):
    sentence_target: str
    sentence_target_highlight: str  # with <b> tags around target word
    sentence_english: str


class Card2Cloze(BaseModel):
    sentence_cloze: str  # with {{c1::word}} syntax
    sentence_english: str
    english_hint: str


class Card3Production(BaseModel):
    sentence_target: str
    sentence_english: str


class Card4Comprehension(BaseModel):
    sentence_target: str
    sentence_english: str
    word_in_sentence_highlight: str  # sentence with <b> tags
    word_translation_in_context: str


class Card5Listening(BaseModel):
    sentence_target: str
    sentence_english: str
    word_in_sentence_highlight: str  # sentence with <b> tags
    word_translation_in_context: str


class AudioQueries(BaseModel):
    word_isolated: str
    sentence_1: str
    sentence_2: str  # cloze sentence, clean (no {{c1::}} syntax)
    sentence_3: str
    sentence_4: str
    sentence_5: str


class VocabEntry(BaseModel):
    id: str
    target_word: str
    target_word_romanization: str = ""
    english_translation: str
    part_of_speech: str
    category: str = "General"
    notes: str = ""

    card_1_recognition: Card1Recognition
    card_2_cloze: Card2Cloze
    card_3_production: Card3Production
    card_4_comprehension: Card4Comprehension
    card_5_listening: Card5Listening
    audio_queries: AudioQueries


class AutoAnkiCards(BaseModel):
    schema_version: int = 1
    source_info: SourceInfo
    vocabulary: list[VocabEntry] = []
