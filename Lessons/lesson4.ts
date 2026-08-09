import type { Lesson } from '../../types';

export const lessonFour: Lesson = {
    id: 4,
    titleEn: 'At Home',
    titleKr: '집',

    exercises: ['sentence-scramble'],  

    segments: [
        {
            id: 'L4-C1',
            type: 'conversation',
            title: 'Conversation 1',
            subtitle: '동생이 두 명 있어요.',
            content: [
                { speaker: '소피아', text: '스티브 씨, 집이 어디예요?', translation: 'Steve, where is your home?', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 19, end: 23 } },
                { speaker: '스티브', text: '보스턴이에요. 아버지하고 어머니가 보스턴에 계세요. 소피아 씨 부모님은 어디 계세요?', translation: 'It’s in Boston. My parents are in Boston. Sophia, where are your parents?', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 23, end: 34 } },
                { speaker: '소피아', text: '홍콩에 계세요. 오빠하고 동생도 홍콩에 있어요.', translation: 'They are in Hong Kong. My siblings are also in Hong Kong.', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 34, end: 42 } },
                { speaker: '스티브', text: '오빠하고 동생도 대학생이에요?', translation: 'Are your older brother and younger sibling college students, too?', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 42, end: 46 } },
                { speaker: '소피아', text: '아니요, 오빠는 대학원생이에요. 그리고 동생은 지금 고등학생이에요.', translation: 'No, my older brother is a graduate student, and my younger sibling is a high school student.', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 46, end: 55 } },
                { speaker: '스티브', text: '남동생이에요, 여동생이에요?', translation: 'Is that a brother or sister?', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 56, end: 59 } },
                { speaker: '소피아', text: '여동생이에요. 스티브 씨도 동생 있어요?', translation: 'It’s a younger sister. Do you have any younger siblings?', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 60, end: 65 } },
                { speaker: '스티브', text: '네, 남동생이 두 명 있어요.', translation: 'Yes, I have two younger brothers.', audio: { file: '/audio/Textbook_Lesson4_C1_3rd_Edition.mp3', start: 65, end: 70 } }
            ],
            newVocabulary: [
                { id: 'v4-1', korean: '개', english: 'dog', pos: 'noun' },
                { id: 'v4-2', korean: '고등학생', english: 'high school student', pos: 'noun' },
                { id: 'v4-3', korean: '남동생', english: 'younger brother', pos: 'noun' },
                { id: 'v4-4', korean: '대학원생', english: 'graduate student', pos: 'noun' },
                { id: 'v4-5', korean: '동생', english: 'younger sibling', pos: 'noun' },
                { id: 'v4-6', korean: '보스턴', english: 'Boston', pos: 'noun' },
                { id: 'v4-7', korean: '부모님', english: 'parents', pos: 'noun' },
                { id: 'v4-8', korean: '아버지', english: 'father', pos: 'noun' },
                { id: 'v4-9', korean: '어머니', english: 'mother', pos: 'noun' },
                { id: 'v4-10', korean: '여동생', english: 'younger sister', pos: 'noun' },
                { id: 'v4-11', korean: '오빠', english: 'older brother (of a female)', pos: 'noun' },
                { id: 'v4-12', korean: '형', english: 'older brother (of a male)', pos: 'noun' },
                { id: 'v4-13', korean: '홍콩', english: 'Hong Kong', pos: 'noun' },
                { id: 'v4-14', korean: '한', english: 'one (with counter)', pos: 'number' },
                { id: 'v4-15', korean: '두', english: 'two (with counter)', pos: 'number' },
                { id: 'v4-16', korean: '세', english: 'three (with counter)', pos: 'number' },
                { id: 'v4-17', korean: '스무', english: 'twenty (with counter)', pos: 'number' },
                { id: 'v4-18', korean: '개', english: 'item counter', pos: 'counter' },
                { id: 'v4-19', korean: '권', english: 'volume counter', pos: 'counter' },
                { id: 'v4-20', korean: '마리', english: 'animal counter', pos: 'counter' },
                { id: 'v4-21', korean: '명', english: 'people counter', pos: 'counter' },
                { id: 'v4-22', korean: '몇', english: 'how many / what (with counter)', pos: 'noun' },
                { id: 'v4-23', korean: '계시다', english: 'to stay, to be (honorific)', pos: 'verb' },
                { id: 'v4-24', korean: '하고', english: 'and (with nouns)', pos: 'particle' }
            ],
            newExpressions: [
                {
                    id: 'exp-4-1',
                    title: 'Honorific Existence: 계시다',
                    content: "계시다 is the honorific word for 있다. Used when the subject is a respected person (parents, teachers).",
                    tables: [
                        {
                            id: 'tbl-hon-exist',
                            type: 'comparison',
                            headers: ['Usage', 'Plain', 'Honorific'],
                            rows: [
                                ['Identification', '이에요/예요', '이세요/세요'],
                                ['Existence', '있어요', '계세요'],
                                ['Possession', '있어요', '있으세요']
                            ]
                        }
                    ]
                },
                {
                    id: 'exp-4-2',
                    title: 'School Levels',
                    content: 'Educational levels use the suffixes -학교 (school) and -학생 (student).',
                    tables: [
                        {
                            id: 'tbl-schools',
                            type: 'generic',
                            headers: ['Level', 'School', 'Student'],
                            rows: [
                                ['Elementary', '초등학교', '초등학생'],
                                ['Middle', '중학교', '중학생'],
                                ['High', '고등학교', '고등학생'],
                                ['College', '대학교', '대학생'],
                                ['Graduate', '대학원', '대학원생']
                            ]
                        }
                    ]
                }
            ]
        },
        {
            id: 'L4-C2',
            type: 'conversation',
            title: 'Conversation 2',
            subtitle: '누구 방이에요?',
            content: [
                { speaker: '소피아', text: '리사 씨, 아파트에 방이 몇 개 있어요?', translation: 'Lisa, how many rooms are there in your apartment?', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 10, end: 15 } },
                { speaker: '리사', text: '세 개 있어요.', translation: 'There are three rooms.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 15, end: 17 } },
                { speaker: '소피아', text: '룸메이트 있어요?', translation: 'Do you have any roommates?', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 18, end: 20 } },
                { speaker: '리사', text: '네, 두 명 있어요.', translation: 'Yes, I have two roommates.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 20, end: 24 } },
                { speaker: '소피아', text: '룸메이트도 학생이에요?', translation: 'Are your roommates also students?', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 24, end: 28 } },
                { speaker: '리사', text: '네, 제니하고 유미는 생물학을 공부해요. 그리고 제니는 저희 한국어 반 친구예요.', translation: 'Yes, Jenny and Yumi study biology, and Jenny is my classmate in Korean class.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 28, end: 39 } },
                { speaker: '소피아', text: '룸메이트들하고 사이가 좋아요?', translation: 'Is your relationship with your roommates good?', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 39.5, end: 43 } },
                { speaker: '리사', text: '네, 사이가 아주 좋아요.', translation: 'Yes, our relationship is very good.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 44, end: 47.5 } },
                { speaker: '소피아', text: '이건 누구 방이에요?', translation: 'Whose room is this?', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 48.5, end: 51 } },
                { speaker: '리사', text: '제 방이에요.', translation: 'It’s my room.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 52, end: 54 } },
                { speaker: '소피아', text: '방이 참 예뻐요.', translation: 'Your room is really pretty.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 55, end: 57.5 } },
                { speaker: '리사', text: '고마워요.', translation: 'Thank you.', audio: { file: '/audio/Textbook_Lesson4_C2_3rd_Edition.mp3', start: 58, end: 59 } }
            ],
            newVocabulary: [
                { id: 'v4-25', korean: '거', english: 'thing (contracted)', pos: 'noun' },
                { id: 'v4-26', korean: '누나', english: 'older sister (of a male)', pos: 'noun' },
                { id: 'v4-27', korean: '룸메이트', english: 'roommate', pos: 'noun' },
                { id: 'v4-28', korean: '방', english: 'room', pos: 'noun' },
                { id: 'v4-29', korean: '사이', english: 'relationship / between', pos: 'noun' },
                { id: 'v4-30', korean: '생물학', english: 'biology', pos: 'noun' },
                { id: 'v4-31', korean: '아파트', english: 'apartment', pos: 'noun' },
                { id: 'v4-32', korean: '언니', english: 'older sister (of a female)', pos: 'noun' },
                { id: 'v4-33', korean: '만', english: 'only', pos: 'particle' },
                { id: 'v4-34', korean: '의', english: 'of (possessive)', pos: 'particle' },
                { id: 'v4-35', korean: '고맙다', english: 'to be thankful', pos: 'adjective' },
                { id: 'v4-36', korean: '나쁘다', english: 'to be bad', pos: 'adjective' },
                { id: 'v4-37', korean: '비싸다', english: 'to be expensive', pos: 'adjective' },
                { id: 'v4-38', korean: '예쁘다', english: 'to be pretty', pos: 'adjective' },
                { id: 'v4-39', korean: '작다', english: 'to be small', pos: 'adjective' },
                { id: 'v4-40', korean: '마시다', english: 'to drink', pos: 'verb' },
                { id: 'v4-41', korean: '배우다', english: 'to learn', pos: 'verb' },
                { id: 'v4-42', korean: '오다', english: 'to come', pos: 'verb' },
                { id: 'v4-43', korean: '자다', english: 'to sleep', pos: 'verb' },
                { id: 'v4-44', korean: '주다', english: 'to give', pos: 'verb' },
                { id: 'v4-45', korean: '참', english: 'very / truly', pos: 'adverb' },
                { id: 'v4-46', korean: '이거', english: 'this thing', pos: 'noun' },
                { id: 'v4-47', korean: '저희', english: 'we/our (humble)', pos: 'noun' },
                { id: 'v4-48', korean: '제', english: 'my (humble)', pos: 'noun' }
            ],
            newExpressions: [
                {
                    id: 'exp-4-3',
                    title: 'Contractions: 거 and 이건',
                    content: '거 is a contraction of 것 (thing). 이건 is a contraction of 이것 (this thing) + 은 (topic particle).'
                }
            ]
        },
        {
            id: 'L4-N1',
            type: 'narration',
            title: 'My Friend Sophia',
            content: [
                { speaker: 'Narrator', text: '소피아는 우리 반 친구예요. 한국어하고 경제학을 공부해요.', translation: 'Sophia is my classmate. (She) studies Korean and economics.', audio: { file: '/audio/Textbook_Lesson4_N_3rd_Edition.mp3', start: 6, end: 14 } },
                { speaker: 'Narrator', text: '소피아는 중국 사람이에요. 집이 홍콩이에요. 홍콩에 아버지하고 어머니가 계세요.', translation: 'Sophia is Chinese. Her home is in Hong Kong. Her father and mother are in Hong Kong.', audio: { file: '/audio/Textbook_Lesson4_N_3rd_Edition.mp3', start: 14.5, end: 26 } },
                { speaker: 'Narrator', text: '그리고 오빠하고 동생도 홍콩에 있어요. 소피아만 미국에 있어요.', translation: 'And her older brother and younger sibling are also in Hong Kong. Only Sophia is in the United States.', audio: { file: '/audio/Textbook_Lesson4_N_3rd_Edition.mp3', start: 26, end: 35 } },
                { speaker: 'Narrator', text: '소피아 오빠는 대학원생이에요. 생물학을 공부해요.', translation: 'Sophia’s older brother is a graduate student. He studies biology.', audio: { file: '/audio/Textbook_Lesson4_N_3rd_Edition.mp3', start: 36, end: 43 } },
                { speaker: 'Narrator', text: '소피아 여동생은 고등학생이에요. 소피아하고 소피아 동생은 사이가 참 좋아요.', translation: 'Sophia’s younger sister is a high school student. Sophia and Sophia’s younger sibling have a very good relationship.', audio: { file: '/audio/Textbook_Lesson4_N_3rd_Edition.mp3', start: 44, end: 54 } }
            ],
            newVocabulary: [],
            newExpressions: []
        }
    ],

    grammar: [
        {
            id: 'G4.1',
            title: 'Alternative questions',
            pattern: 'A이에요/예요, B이에요/예요?',
            description: 'Used to ask someone to choose one from the given choices.',
            examples: [
                { kor: '남동생이에요, 여동생이에요?', eng: 'Is it a younger brother or a younger sister?' },
                { kor: '일본 사람이에요, 중국 사람이에요?', eng: 'Are you Japanese or Chinese?' }
            ]
        },
        {
            id: 'G4.2',
            title: 'Numbers',
            pattern: 'Sino-Korean vs Native Korean',
            description: 'Korean uses two sets of numbers. Native numbers are used for counting items/people, while Sino-Korean are used for dates, money, and floors.',
            examples: [
                { kor: '동생이 두 명 있어요.', eng: 'I have two younger siblings.' },
                { kor: '일 달러는 천 원이에요.', eng: 'One dollar is 1,000 won.' }
            ],
            tables: [
                {
                    id: 'tbl-numbers',
                    type: 'comparison',
                    headers: ['Num', 'Sino', 'Native', 'Before Counter'],
                    rows: [
                        ['1', '일', '하나', '한'],
                        ['2', '이', '둘', '두'],
                        ['3', '삼', '셋', '세'],
                        ['4', '사', '넷', '네'],
                        ['5', '오', '다섯', '다섯'],
                        ['10', '십', '열', '열'],
                        ['20', '이십', '스물', '스무']
                    ]
                }
            ]
        },
        {
            id: 'G4.3',
            title: 'Noun counters',
            pattern: '[Noun] [Number] [Counter]',
            description: 'Specific counters must be used depending on the object type.',
            examples: [
                { kor: '학생이 스무 명이에요.', eng: 'There are twenty students.' },
                { kor: '책이 네 권 있어요.', eng: 'There are four books.' }
            ],
            tables: [
                {
                    id: 'tbl-counters-native',
                    type: 'conjugation',
                    headers: ['Counter', 'Used for', 'Example'],
                    rows: [
                        ['명/사람', 'People', '한 명'],
                        ['마리', 'Animals', '두 마리'],
                        ['개', 'Items', '세 개'],
                        ['권', 'Volumes/Books', '네 권'],
                        ['시간', 'Hours (duration)', '한 시간']
                    ]
                }
            ]
        },
        {
            id: 'G4.4',
            title: 'Possessive relations',
            pattern: 'N1 N2',
            description: "Possession is usually expressed by placing the possessor before the possessed. The particle '의' is often omitted in conversation.",
            examples: [
                { kor: '마이클 책', eng: "Michael's book" },
                { kor: '제 동생 거예요.', eng: "It's my sibling's." }
            ],
            tables: [
                {
                    id: 'tbl-possessive-pronouns',
                    type: 'comparison',
                    headers: ['Form', 'I', 'My'],
                    rows: [
                        ['Plain', '나', '내'],
                        ['Humble', '저', '제']
                    ]
                }
            ]
        },
        {
            id: 'G4.5',
            title: 'Vowel contraction',
            pattern: 'Vst + 어요/아요',
            description: 'When two vowels meet in conjugation, they often contract into one syllable.',
            examples: [
                { kor: '가 + 아요 -> 가요', eng: 'to go' },
                { kor: '마시 + 어요 -> 마셔요', eng: 'to drink' },
                { kor: '보 + 아요 -> 봐요', eng: 'to see' }
            ],
            tables: [
                {
                    id: 'tbl-vowel-contractions',
                    type: 'conjugation',
                    headers: ['Stem Vowel', 'Ending', 'Contracted'],
                    rows: [
                        ['아/어', '아요/어요', '아/어 (drop one)'],
                        ['이', '어요', '여'],
                        ['우', '어요', '워'],
                        ['오', '아요', '와'],
                        ['으', '아요/어요', 'Drop 으']
                    ]
                }
            ]
        }
    ],

    culture: [
        {
            title: 'Korean Collectivism: 우리',
            content: "Koreans often use '우리' (our) instead of '내' (my) for things shared or belonging to a group, like '우리 집' (my house) or '우리 어머니' (my mother)."
        },
        {
            title: 'Traditional Korean House: 한옥 and 온돌',
            content: "Hanok is the traditional house. Ondol is the unique under-floor heating system that uses heat from a stove to warm stone slabs under the floor."
        }
    ],

    usage: [
        {
            id: 'U4-A',
            title: 'Inquiring about hometown and family',
            description: 'Ask where someone is from and who is in their family.',
            exampleDialogue: [
                { speaker: '스티브', text: '소피아 씨는 집이 어디예요?', translation: 'Sophia, where is your home?' },
                { speaker: '소피아', text: '홍콩이에요. 부모님은 홍콩에 계세요.', translation: 'It is Hong Kong. My parents are in Hong Kong.' }
            ]
        },
        {
            id: 'U4-B',
            title: 'Asking about quantity',
            description: 'Using 몇 with counters to ask "how many".',
            exampleDialogue: [
                { speaker: 'A', text: '방이 몇 개 있어요?', translation: 'How many rooms are there?' },
                { speaker: 'B', text: '세 개 있어요.', translation: 'There are three.' }
            ]
        }
    ]
};