import type { Lesson } from '../../types';

	export const lessonTwo: Lesson = {
		id: 2,
		titleEn: 'Korean Language Class',
		titleKr: '한국어 수업',

		exercises: ['sentence-scramble'],

		segments: [
		{
			id: 'L2-C1',
			type: 'conversation',
			title: 'Conversation 1',
			subtitle: 'Steve saw Lisa studying Korean in the school cafeteria.',
			content: [
				{
					speaker: '리사',
					text: '안녕하세요, 스티브 씨?',
					translation: 'Hi, Steve.',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 26,
						end: 28
					}
				},
				{
					speaker: '스티브',
					text: '어, 리사 씨. 안녕하세요?',
					translation: 'Oh, Lisa. How are you?',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 29,
						end: 32
					}
				},
				{
					speaker: '리사',
					text: '한국어 수업이 어때요?',
					translation: 'How is your Korean class?',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 33,
						end: 36
					}
				},
				{
					speaker: '스티브',
					text: '아주 재미있어요. 친구들도 좋아요.',
					translation: 'It’s very interesting and my classmates are also nice.',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 36,
						end: 40
					}
				},
				{
					speaker: '리사',
					text: '숙제가 많아요?',
					translation: 'Is there a lot of homework?',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 41,
						end: 43
					}
				},
				{
					speaker: '스티브',
					text: '네, 많아요.',
					translation: 'Yes, there is a lot.',
					audio: {
						file: '/audio/Textbook_Lesson2_C1_3rd_Edition.mp3',
						start: 43,
						end: 46
					}
				}
			],
			newVocabulary: [
				{ id: 'v2-1', korean: '도서관', english: 'library', pos: 'noun' },
				{ id: 'v2-2', korean: '수업', english: 'course, class', pos: 'noun' },
				{ id: 'v2-3', korean: '숙제', english: 'homework', pos: 'noun' },
				{ id: 'v2-4', korean: '식당', english: 'restaurant / cafeteria', pos: 'noun' },
				{ id: 'v2-5', korean: '아침', english: 'breakfast / morning', pos: 'noun' },
				{ id: 'v2-6', korean: '친구', english: 'friend', pos: 'noun' },
				{ id: 'v2-7', korean: '커피', english: 'coffee', pos: 'noun' },
				{ id: 'v2-8', korean: '학교', english: 'school', pos: 'noun' },
				{ id: 'v2-9', korean: '들', english: 'plural particle', pos: 'particle' },
				{ id: 'v2-10', korean: '어', english: 'oh', pos: 'interjection' },
				{ id: 'v2-11', korean: '괜찮다', english: 'to be all right, okay', pos: 'adjective' },
				{ id: 'v2-12', korean: '넓다', english: 'to be spacious, wide', pos: 'adjective' },
				{ id: 'v2-13', korean: '많다', english: 'to be many, much', pos: 'adjective' },
				{ id: 'v2-14', korean: '맛있다', english: 'to be delicious', pos: 'adjective' },
				{ id: 'v2-15', korean: '어떻다', english: 'to be how', pos: 'adjective' },
				{ id: 'v2-16', korean: '재미있다', english: 'to be fun, interesting', pos: 'adjective' },
				{ id: 'v2-17', korean: '좋다', english: 'to be good, nice', pos: 'adjective' },
				{ id: 'v2-18', korean: '먹다', english: 'to eat', pos: 'verb' },
				{ id: 'v2-19', korean: '앉다', english: 'to sit', pos: 'verb' },
				{ id: 'v2-20', korean: '알다', english: 'to know', pos: 'verb' },
				{ id: 'v2-21', korean: '아주', english: 'very, really', pos: 'adverb' }
			],
			newExpressions: [
				{
					id: 'exp-2-1',
					title: '어때요? (How is...?)',
					content:
						"An expression asking the other party's opinion. It is a contraction of [어떻 + 어요 = 어때요].",
					tables: [
						{
							id: 'tbl-how-is',
							type: 'generic',
							headers: ['Question', 'Translation'],
							rows: [
								['음식이 어때요?', "How's the food?"],
								['학교가 어때요?', "How's school?"]
							]
						}
					]
				},
				{
					id: 'exp-2-2',
					title: 'Plural Particle 들',
					content:
						'Attached to nouns to indicate plurality (e.g., 학생들, 선생님들). In Korean, plurality is not mandatorily marked.'
				}
			]
		},
		{
			id: 'L2-C2',
			type: 'conversation',
			title: 'Conversation 2',
			subtitle: 'Sophia is studying Korean.',
			content: [
				{
					speaker: '소피아',
					text: '리사 씨, 요즘 어떻게 지내요?',
					translation: 'Hi, Lisa. How are you these days?',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 6,
						end: 11
					}
				},
				{
					speaker: '리사',
					text: '잘 지내요. 소피아 씨는 어떻게 지내요?',
					translation: 'I’m doing well. How are you, Sophia?',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 11.5,
						end: 17.5
					}
				},
				{
					speaker: '소피아',
					text: '저도 잘 지내요.',
					translation: 'I’m also doing well.',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 18,
						end: 20
					}
				},
				{
					speaker: '리사',
					text: '지금 뭐 해요?',
					translation: 'What are you doing now?',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 21,
						end: 23.5
					}
				},
				{
					speaker: '소피아',
					text: '한국어를 공부해요. 오늘 한국어 시험을 봐요. 그리고 내일은 한국 역사 시험을 봐요.',
					translation:
						'I’m studying Korean. I take a Korean exam today, and take a Korean history exam tomorrow.',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 23.5,
						end: 36
					}
				},
				{
					speaker: '리사',
					text: '아, 그래요?',
					translation: 'Oh, really?',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 36.5,
						end: 39
					}
				},
				{
					speaker: '소피아',
					text: '네.',
					translation: 'Yes.',
					audio: {
						file: '/audio/Textbook_Lesson2_C2_3rd_Edition.mp3',
						start: 39,
						end: 40
					}
				}
			],
			newVocabulary: [
				{ id: 'v2-22', korean: '공부(하다)', english: 'study', pos: 'verb' },
				{ id: 'v2-23', korean: '남자', english: 'man', pos: 'noun' },
				{ id: 'v2-24', korean: '내일', english: 'tomorrow', pos: 'noun' },
				{ id: 'v2-25', korean: '시험', english: 'test, exam', pos: 'noun' },
				{ id: 'v2-26', korean: '역사', english: 'history', pos: 'noun' },
				{ id: 'v2-27', korean: '오늘', english: 'today', pos: 'noun' },
				{ id: 'v2-28', korean: '음식', english: 'food', pos: 'noun' },
				{ id: 'v2-29', korean: '주스', english: 'juice', pos: 'noun' },
				{ id: 'v2-30', korean: '텔레비전', english: 'television', pos: 'noun' },
				{ id: 'v2-31', korean: '을/를', english: 'object particle', pos: 'particle' },
				{ id: 'v2-32', korean: '그리고', english: 'and', pos: 'conjunction' },
				{ id: 'v2-33', korean: '만나다', english: 'to meet', pos: 'verb' },
				{ id: 'v2-34', korean: '보다', english: 'to see, watch', pos: 'verb' },
				{ id: 'v2-35', korean: '쓰다', english: 'to write', pos: 'verb' },
				{ id: 'v2-36', korean: '지내다', english: 'to get along', pos: 'verb' },
				{ id: 'v2-37', korean: '하다', english: 'to do', pos: 'verb' },
				{ id: 'v2-38', korean: '맛없다', english: 'to be tasteless', pos: 'adjective' },
				{ id: 'v2-39', korean: '싸다', english: 'to be cheap', pos: 'adjective' },
				{ id: 'v2-40', korean: '재미없다', english: 'to be uninteresting', pos: 'adjective' },
				{ id: 'v2-41', korean: '크다', english: 'to be big', pos: 'adjective' },
				{ id: 'v2-42', korean: '어떻게', english: 'how', pos: 'adverb' },
				{ id: 'v2-43', korean: '요즘', english: 'these days', pos: 'adverb' },
				{ id: 'v2-44', korean: '잘', english: 'well', pos: 'adverb' },
				{ id: 'v2-45', korean: '지금', english: 'now', pos: 'adverb' }
			],
			newExpressions: [
				{
					id: 'exp-2-3',
					title: 'Verbs with 하다',
					content:
						"Verbs like 공부하다 (to study) are [Noun + 하다]. They can be split into 'Noun + Object Particle + 하다' (e.g., 공부를 하다)."
				},
				{
					id: 'exp-2-4',
					title: '시험을 보다',
					content: "Literally 'to see a test', this phrase means 'to take a test'."
				}
			]
		},
		{
			"id": "L2-N1",
			"type": "narration",
			"title": "Korean Class",
			"content": [
				{
					"speaker": "Narrator",
					"text": "저는 한국어를 공부해요. 한국어 수업이 아주 재미있어요.",
					"translation": "I study Korean. The Korean class is very interesting.",
					"audio": {
						"file": "/audio/Textbook_Lesson2_N_3rd_Edition.mp3",
						"start": 5,
						"end": 14
					}
				},
				{
					"speaker": "Narrator",
					"text": "친구들도 좋아요. 그리고 학생들이 많아요.",
					"translation": "My classmates are also nice and there are many students.",
					"audio": {
						"file": "/audio/Textbook_Lesson2_N_3rd_Edition.mp3",
						"start": 15,
						"end": 21
					}
				},
				{
					"speaker": "Narrator",
					"text": "중국 학생, 일본 학생이 많아요.",
					"translation": "There are many Chinese and Japanese students.",
					"audio": {
						"file": "/audio/Textbook_Lesson2_N_3rd_Edition.mp3",
						"start": 22,
						"end": 26
					}
				},
				{
					"speaker": "Narrator",
					"text": "오늘도 학생들이 한국어를 공부해요. 그리고 한국어 시험을 봐요.",
					"translation": "Today as well the students are studying Korean. And they are taking a Korean exam.",
					"audio": {
						"file": "/audio/Textbook_Lesson2_N_3rd_Edition.mp3",
						"start": 27,
						"end": 38
					}
				}
			],
			"newVocabulary": [],
			"newExpressions": []
		}
	],

	grammar: [
		{
			id: 'G2.1',
			title: 'The subject particle 이/가',
			pattern: 'N이/가',
			description:
				'Indicates the subject of the sentence. 이 follows a consonant, 가 follows a vowel. Note that first-person pronouns change form when combined with 가.',
			examples: [
				{ kor: '커피가 맛있어요.', eng: 'The coffee is delicious.' },
				{ kor: '한국어 수업이 재미있어요.', eng: 'Korean class is fun.' }
			],
			tables: [
				{
					id: 'tbl-subj-particle',
					type: 'conjugation',
					headers: ['Noun Ending', 'Particle'],
					rows: [
						['Consonant', '이'],
						['Vowel', '가']
					]
				},
				{
					id: 'tbl-pronouns-subj',
					type: 'comparison',
					headers: ['Type', 'Plain', 'Humble', 'Plain + Subj', 'Humble + Subj'],
					rows: [
						['Base Form', '나', '저', '내가', '제가'],
						['Topic (은/는)', '나는', '저는', '-', '-']
					]
				}
			]
		},
		{
			id: 'G2.2',
			title: 'The polite ending ~어요/아요 I (Regular)',
			pattern: 'Vst + 어요/아요',
			description:
				"The most frequently used form in conversation. ~아요 is used if the last vowel of the stem is '오' or '아'. Otherwise, ~어요 is used.",
			examples: [
				{ kor: '숙제가 많아요.', eng: 'There is a lot of homework.' },
				{ kor: '커피가 맛있어요.', eng: 'The coffee is delicious.' }
			],
			tables: [
				{
					id: 'tbl-conj-basic',
					type: 'conjugation',
					headers: ['Stem', 'Ending', 'Polite Form'],
					rows: [
						['괜찮', '다', '괜찮아요'],
						['재미있', '다', '재미있어요'],
						['먹', '다', '먹어요'],
						['앉', '다', '앉아요'],
						['좋', '다', '좋아요']
					]
				}
			]
		},
		{
			id: 'G2.3',
			title: 'The polite ending ~어요/아요 II (Irregular)',
			pattern: 'Vst + 어요/아요',
			description: "Applies to '하다' verbs, vowel contractions, and '으' deletion.",
			examples: [
				{ kor: '한국어를 공부해요.', eng: 'I study Korean.' },
				{ kor: '학교가 커요.', eng: 'The school is big.' }
			],
			tables: [
				{
					id: 'tbl-conj-irr',
					type: 'conjugation',
					headers: ['Type', 'Stem', 'Polite Form'],
					rows: [
						['하다 Verb', '공부하다', '공부해요'],
						['하다 Verb', '숙제하다', '숙제해요'],
						['Vowel Contraction', '가다', '가요'],
						['Vowel Contraction', '싸다', '싸요'],
						['Vowel Contraction', '보다', '봐요'],
						["'으' Deletion", '크다', '커요'],
						["'으' Deletion", '쓰다', '써요']
					]
				}
			]
		},
		{
			id: 'G2.4',
			title: 'The object particle 을/를',
			pattern: 'N을/를',
			description: 'Marks the object of the verb. 을 follows a consonant, 를 follows a vowel.',
			examples: [
				{ kor: '리사가 아침을 먹어요.', eng: 'Lisa eats breakfast.' },
				{ kor: '유미가 텔레비전을 봐요.', eng: 'Yumi watches television.' }
			],
			tables: [
				{
					id: 'tbl-obj-particle',
					type: 'conjugation',
					headers: ['Noun Ending', 'Particle'],
					rows: [
						['Consonant', '을'],
						['Vowel', '를']
					]
				}
			]
		}
	],

	culture: [
		{
			title: 'The Academic Calendar',
			content:
				'In Korea, the school year is divided into two terms. The first semester starts in early March. The second semester resumes in late August. There are long summer and winter breaks.'
		},
		{
			title: 'Blind Dates',
			content:
				"Dating is not very common in high school due to study pressure. After high school, students often participate in 'Meeting' (group blind dates) or 'Sogaeting' (one-on-one blind dates). 'Matseon' is a formal date arranged by parents."
		}
	],

	usage: [
		{
			id: 'U2-A',
			title: 'Inquiring about well-being',
			description: "Ask how someone is doing using '어떻게 지내세요?'.",
			exampleDialogue: [
				{
					speaker: '리사',
					text: '스티브 씨, 요즘 어떻게 지내세요?',
					translation: 'Steve, how are you doing these days?'
				},
				{
					speaker: '스티브',
					text: '잘 지내요. 리사 씨는 어때요?',
					translation: "I'm doing well. How about you, Lisa?"
				},
				{ speaker: '리사', text: '저는 바빠요.', translation: 'I am busy.' }
			]
		},
		{
			id: 'U2-C',
			title: 'Describing People',
			description: "Describe a person's Year, Nationality, and Major.",
			exampleDialogue: [
				{
					speaker: 'Student',
					text: '소피아 왕은 2학년이에요. 중국 사람이에요.',
					translation: 'Sophia Wang is a sophomore. She is Chinese.'
				},
				{ speaker: 'Student', text: '경제학을 공부해요.', translation: 'She studies Economics.' }
			]
		}
	]
};
