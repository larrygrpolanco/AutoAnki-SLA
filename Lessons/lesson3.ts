import type { Lesson } from '../../types';

export const lessonThree: Lesson = {
    id: 3,
    titleEn: 'The University Campus',
    titleKr: '대학 캠퍼스',

    exercises: ['sentence-scramble'],

    segments: [
        {
            id: 'L3-C1',
            type: 'conversation',
            title: 'Conversation 1',
            subtitle: 'Yumi is looking for the school cafeteria and runs into Lisa.',
            "content": [
                {
                    "speaker": "유미",
                    "text": "저 . . . 학교 식당이 어디 있어요?",
                    "translation": "Uh... where is the school cafeteria?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C1_3rd_Edition.mp3",
                        "start": 26,
                        "end": 31
                    }
                },
                {
                    "speaker": "리사",
                    "text": "유니온(‘Union’) 빌딩 1층에 있어요. 그리고 도서관 뒤에도 있어요.",
                    "translation": "It’s on the first floor of the Union Building. There is one behind the library, too.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C1_3rd_Edition.mp3",
                        "start": 32,
                        "end": 39
                    }
                },
                {
                    "speaker": "유미",
                    "text": "유니온 빌딩은 어디 있어요?",
                    "translation": "Where is the Union Building?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C1_3rd_Edition.mp3",
                        "start": 40,
                        "end": 43
                    }
                },
                {
                    "speaker": "리사",
                    "text": "우체국 앞에 있어요.",
                    "translation": "It’s in front of the post office.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C1_3rd_Edition.mp3",
                        "start": 44,
                        "end": 48
                    }
                }
            ],
            newVocabulary: [
                { id: 'v3-1', korean: '가방', english: 'bag', pos: 'noun' },
                { id: 'v3-2', korean: '기숙사', english: 'dormitory', pos: 'noun' },
                { id: 'v3-3', korean: '대학교', english: 'college, university', pos: 'noun' },
                { id: 'v3-4', korean: '뒤', english: 'back, behind', pos: 'noun' },
                { id: 'v3-5', korean: '밑', english: 'bottom, below', pos: 'noun' },
                { id: 'v3-6', korean: '밖', english: 'outside', pos: 'noun' },
                { id: 'v3-7', korean: '빌딩', english: 'building', pos: 'noun' },
                { id: 'v3-8', korean: '서점', english: 'bookstore', pos: 'noun' },
                { id: 'v3-9', korean: '시계', english: 'clock, watch', pos: 'noun' },
                { id: 'v3-10', korean: '안', english: 'inside', pos: 'noun' },
                { id: 'v3-11', korean: '앞', english: 'front', pos: 'noun' },
                { id: 'v3-12', korean: '어디', english: 'what place, where', pos: 'noun' },
                { id: 'v3-13', korean: '옆', english: 'side, beside', pos: 'noun' },
                { id: 'v3-14', korean: '우체국', english: 'post office', pos: 'noun' },
                { id: 'v3-15', korean: '의자', english: 'chair', pos: 'noun' },
                { id: 'v3-16', korean: '위', english: 'the top side, above', pos: 'noun' },
                { id: 'v3-17', korean: '책상', english: 'desk', pos: 'noun' },
                { id: 'v3-18', korean: '책', english: 'book', pos: 'noun' },
                { id: 'v3-19', korean: '학생회관', english: 'student center', pos: 'noun' },
                { id: 'v3-20', korean: '캠퍼스', english: 'campus', pos: 'noun' },
                { id: 'v3-21', korean: '층', english: 'floor, layer', pos: 'counter' },
                { id: 'v3-22', korean: '있다', english: 'to be (existence)', pos: 'adjective' },
                { id: 'v3-23', korean: '저', english: 'uh (hesitation)', pos: 'interjection' },
                { id: 'v3-24', korean: '에', english: 'in, at, on (static location)', pos: 'particle' }
            ],
            newExpressions: [
                {
                    id: 'exp-3-1',
                    title: 'The Hesitation Marker 저',
                    content: '저 is used for hesitation before the speaker says something, drawing the attention of the listener.'
                },
                {
                    id: 'exp-3-2',
                    title: '이에요/예요 vs. 있어요',
                    content: "In Korean, 'to be' is split between equation (이다) and existence (있다).",
                    tables: [
                        {
                            id: 'tbl-be-diff',
                            type: 'comparison',
                            headers: ['Function', 'Korean Form', 'Example'],
                            rows: [
                                ['Equation', '이다 (이에요/예요)', '저는 학생이에요. (I am a student.)'],
                                ['Existence', '있다 (있어요)', '식당이 빌딩에 있어요. (The cafeteria is in the building.)']
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "L3-C2",
            "type": "conversation",
            "title": "Conversation 2",
            "subtitle": "Jenny and Michael talk about their classes.",
            "content": [
                {
                    "speaker": "제니",
                    "text": "마이클 씨, 오늘 수업 있으세요?",
                    "translation": "Michael, do you have class today?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 7,
                        "end": 11
                    }
                },
                {
                    "speaker": "마이클",
                    "text": "네, 한국어 수업이 있어요. 제니 씨는요?",
                    "translation": "Yes, I have Korean class. How about you, Jenny?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 11,
                        "end": 15
                    }
                },
                {
                    "speaker": "제니",
                    "text": "오늘은 수업이 없어요. 그런데, 내일은 경제학 수업이 있어요. 한국어 수업은 재미있어요?",
                    "translation": "I don't have class today. But, I have economics class tomorrow. Is Korean class interesting?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 17,
                        "end": 30
                    }
                },
                {
                    "speaker": "마이클",
                    "text": "네, 아주 재미있어요. 그리고 선생님도 좋으세요. 그래서 매일 열심히 한국어를 공부해요.",
                    "translation": "Yes, it’s very interesting. And the teacher is also nice. So I study Korean diligently every day.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 30,
                        "end": 43
                    }
                },
                {
                    "speaker": "제니",
                    "text": "한국어 교실은 어디 있어요?",
                    "translation": "Where is the Korean classroom?",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 44,
                        "end": 47
                    }
                },
                {
                    "speaker": "마이클",
                    "text": "로이스 (‘Royce’) 홀 3층에 있어요.",
                    "translation": "It’s on the 3rd floor of Royce Hall.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_C2_3rd_Edition.mp3",
                        "start": 48,
                        "end": 52
                    }
                }
            ],
            newVocabulary: [
                { id: 'v3-25', korean: '경제학', english: 'economics', pos: 'noun' },
                { id: 'v3-26', korean: '교과서', english: 'textbook', pos: 'noun' },
                { id: 'v3-27', korean: '교실', english: 'classroom', pos: 'noun' },
                { id: 'v3-28', korean: '반', english: 'class', pos: 'noun' },
                { id: 'v3-29', korean: '사전', english: 'dictionary', pos: 'noun' },
                { id: 'v3-30', korean: '시간', english: 'time', pos: 'noun' },
                { id: 'v3-31', korean: '여자', english: 'woman', pos: 'noun' },
                { id: 'v3-32', korean: '우산', english: 'umbrella', pos: 'noun' },
                { id: 'v3-33', korean: '질문', english: 'question', pos: 'noun' },
                { id: 'v3-34', korean: '집', english: 'home, house', pos: 'noun' },
                { id: 'v3-35', korean: '컴퓨터', english: 'computer', pos: 'noun' },
                { id: 'v3-36', korean: '홀', english: 'hall', pos: 'noun' },
                { id: 'v3-37', korean: '누구', english: 'who', pos: 'noun' },
                { id: 'v3-38', korean: '가다', english: 'to go', pos: 'verb' },
                { id: 'v3-39', korean: '인사하다', english: 'to greet', pos: 'verb' },
                { id: 'v3-40', korean: '읽다', english: 'to read', pos: 'verb' },
                { id: 'v3-41', korean: '없다', english: 'to not be / not have', pos: 'adjective' },
                { id: 'v3-42', korean: '매일', english: 'every day', pos: 'adverb' },
                { id: 'v3-43', korean: '열심히', english: 'diligently', pos: 'adverb' },
                { id: 'v3-44', korean: '그래서', english: 'so, therefore', pos: 'conjunction' },
                { id: 'v3-45', korean: '그런데', english: 'but, however', pos: 'conjunction' }
            ],
            newExpressions: [
                {
                    id: 'exp-3-3',
                    title: '누구 vs 누가',
                    content: "When 누구 (who) is combined with the subject particle 가, it becomes 누가."
                }
            ]
        },
        {
            "id": "L3-N1",
            "type": "narration",
            "title": "Campus",
            "content": [
                {
                    "speaker": "Narrator",
                    "text": "대학교 캠퍼스는 넓어요. 학생들이 아주 많아요. 그래서 기숙사가 커요.",
                    "translation": "The university campus is extensive. There are really many students. Therefore the dormitory is very big.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_N_3rd_Edition.mp3",
                        "start": 5,
                        "end": 15
                    }
                },
                {
                    "speaker": "Narrator",
                    "text": "그리고 도서관도 많아요. 학교 식당은 유니온 빌딩 안에 있어요. 음식이 싸요. 그리고 커피가 맛있어요.",
                    "translation": "And there are many libraries. The school cafeteria is inside the Union Building. The food is affordable and the coffee is good.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_N_3rd_Edition.mp3",
                        "start": 16,
                        "end": 32
                    }
                },
                {
                    "speaker": "Narrator",
                    "text": "유니온 빌딩 안에 서점도 있어요. 로이스 홀 3층에 한국어 교실이 있어요. 매일 한국어 수업이 있어요.",
                    "translation": "There is also a bookstore inside the Union Building. The Korean classroom is located on the third floor of Royce Hall. There is a Korean class every day.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_N_3rd_Edition.mp3",
                        "start": 32,
                        "end": 46
                    }
                },
                {
                    "speaker": "Narrator",
                    "text": "선생님은 이민수 선생님이세요. 선생님이 아주 좋으세요.",
                    "translation": "The instructor of the Korean class is Professor Minsoo Lee. He is very nice.",
                    "audio": {
                        "file": "/audio/Textbook_Lesson3_N_3rd_Edition.mp3",
                        "start": 46,
                        "end": 54
                    }
                }
            ],
            newVocabulary: [],
            newExpressions: []
        }
    ],

    grammar: [
        {
            id: 'G3.1',
            title: 'Expressing location: [Place]에 있어요',
            pattern: '[Place] + 에 있어요',
            description: 'Indicates where an entity exists. Requires a location, the particle 에, and the adjective 있다.',
            examples: [
                { kor: '서점이 어디 있어요?', eng: 'Where is the bookstore?' },
                { kor: '우체국 옆에 있어요.', eng: 'It is beside the post office.' }
            ],
            tables: [
                {
                    id: 'tbl-pos-nouns',
                    type: 'generic',
                    headers: ['Position', 'Korean'],
                    rows: [
                        ['Front', '앞'],
                        ['Back/Behind', '뒤'],
                        ['Side/Beside', '옆'],
                        ['Inside', '안'],
                        ['Outside', '밖'],
                        ['Above/Top', '위'],
                        ['Below/Under', '밑 / 아래']
                    ]
                }
            ]
        },
        {
            id: 'G3.2',
            title: 'Changing the topic: particle 은/는',
            pattern: 'N + 은/는',
            description: 'Used to shift the topic from one item to another in a conversation.',
            examples: [
                { kor: '기숙사는 어디 있어요?', eng: 'As for the dormitory, where is it?' },
                { kor: '서점은요?', eng: 'How about the bookstore?' }
            ]
        },
        {
            id: 'G3.3',
            title: 'Expressing possession: N이/가 있어요/없어요',
            pattern: 'N이/가 있어요/없어요',
            description: 'Used to express having or not having an object or person.',
            examples: [
                { kor: '한국어 사전 있어요?', eng: 'Do you have a Korean dictionary?' },
                { kor: '질문 있어요?', eng: 'Do you have any questions?' }
            ]
        },
        {
            id: 'G3.4',
            title: 'The honorific ending ~(으)세요',
            pattern: 'Vst + (으)세요',
            description: 'A combination of honorific marker ~(으)시 and polite ending ~어요. Used to show respect to the person being talked about or addressed.',
            examples: [
                { kor: '선생님, 우산 있으세요?', eng: 'Teacher, do you have an umbrella?' },
                { kor: '스티브 씨, 앉으세요.', eng: 'Steve, please have a seat.' }
            ],
            tables: [
                {
                    id: 'tbl-honorific-conj',
                    type: 'conjugation',
                    headers: ['Stem Ending', 'Ending', 'Example'],
                    rows: [
                        ['Consonant', '으세요', '앉으세요'],
                        ['Vowel', '세요', '가세요']
                    ]
                }
            ]
        }
    ],

    culture: [
        {
            title: 'Korean National Symbols',
            content: 'The 태극기 (flag) represents the dualism of the universe (Yin-Yang). The 무궁화 (Rose of Sharon) is the national flower, meaning "the flower that never withers." The national anthem is 애국가.'
        }
    ],

    usage: [
        {
            id: 'U3-A',
            title: 'Asking about location',
            description: 'Ask for and give the location of people or buildings.',
            exampleDialogue: [
                { speaker: 'A', text: '책이 어디 있어요?', translation: 'Where is the book?' },
                { speaker: 'B', text: '가방 안에 있어요.', translation: 'It is in the bag.' }
            ]
        },
        {
            id: 'U3-B',
            title: 'Talking about majors',
            description: 'Common ways to ask about someone’s field of study.',
            exampleDialogue: [
                { speaker: 'A', text: '전공이 뭐예요?', translation: 'What is your major?' },
                { speaker: 'B', text: '경제학이에요.', translation: 'It is Economics.' }
            ]
        },
        {
            id: 'U3-C',
            title: 'Making requests',
            description: 'Polite classroom instructions using honorifics.',
            exampleDialogue: [
                { speaker: 'Teacher', text: '책을 펴세요.', translation: 'Please open your book.' },
                { speaker: 'Student', text: '천천히 말씀해 주세요.', translation: 'Please speak slowly.' }
            ]
        }
    ]
}