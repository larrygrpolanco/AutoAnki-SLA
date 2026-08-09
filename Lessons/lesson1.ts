import type { Lesson } from '../../types';

	export const lessonOne: Lesson = {
		id: 1,
		titleEn: 'Greetings',
		titleKr: '인사',

		exercises: ['sentence-scramble'],

		segments: [
		{
			id: 'L1-C1',
			type: 'conversation',
			title: 'Conversation 1',
			subtitle: 'Students introduce themselves in a classroom.',
			content: [
				{
					speaker: '스티브',
					text: '안녕하세요? 저는 스티브 윌슨이에요. 3학년이에요.',
					translation: 'Hello. I’m Steve Wilson. I’m a junior.',
					audio: {
						file: '/audio/Textbook_Lesson1_C1_3rd_Edition.mp3',
						start: 41.5,
						end: 49.0
					}
				},
				{
					speaker: '유미',
					text: '안녕하세요? 저는 김유미예요. 저는 1학년이에요.',
					translation: 'Hi. I’m Yumi Kim. I’m a freshman.',
					audio: {
						file: '/audio/Textbook_Lesson1_C1_3rd_Edition.mp3',
						start: 50.0,
						end: 59.0
					}
				},
				{
					speaker: '마이클',
					text: '마이클 정이에요. 저도 1학년이에요.',
					translation: 'I’m Michael Jung. I’m also a freshman.',
					audio: {
						file: '/audio/Textbook_Lesson1_C1_3rd_Edition.mp3',
						start: 59.0,
						end: 66.0
					}
				}
			],
			newVocabulary: [
				{ id: 'v1-1', korean: '1학년', english: 'freshman', pos: 'noun' },
				{ id: 'v1-2', korean: '2학년', english: 'sophomore', pos: 'noun' },
				{ id: 'v1-3', korean: '3학년', english: 'junior', pos: 'noun' },
				{ id: 'v1-4', korean: '4학년', english: 'senior', pos: 'noun' },
				{ id: 'v1-5', korean: '대학생', english: 'college student', pos: 'noun' },
				{ id: 'v1-6', korean: '미국', english: 'the United States', pos: 'noun' },
				{ id: 'v1-7', korean: '사람', english: 'person, people', pos: 'noun' },
				{ id: 'v1-8', korean: '인사', english: 'greeting', pos: 'noun' },
				{ id: 'v1-9', korean: '학년', english: 'school year', pos: 'noun' },
				{ id: 'v1-10', korean: '학생', english: 'student', pos: 'noun' },
				{ id: 'v1-11', korean: '한국', english: 'Korea', pos: 'noun' },
				{ id: 'v1-12', korean: '저', english: 'I', pos: 'noun', tags: ['humble'] },
				{ id: 'v1-13', korean: '안녕하다', english: 'to be well', pos: 'adjective' },
				{ id: 'v1-14', korean: '이다', english: 'to be (equation)', pos: 'copula' },
				{ id: 'v1-15', korean: '과', english: 'lesson, chapter', pos: 'counter' },
				{ id: 'v1-16', korean: '도', english: 'also, too', pos: 'particle' },
				{ id: 'v1-17', korean: '은/는', english: "topic particle ('as for')", pos: 'particle' }
			],
			newExpressions: [
				{
					id: 'exp-1-1',
					title: '안녕하세요 (Hello)',
					content:
						'A greeting that asks about the other person’s well-being. Appropriate at any time of day.'
				},
				{
					id: 'exp-1-2',
					title: 'Reference to Self (Plain vs Humble)',
					content: 'Korean uses different pronouns depending on who you are talking to.',
					tables: [
						{
							id: 'tbl-pronouns',
							type: 'comparison',
							headers: ['Meaning', 'Plain Form', 'Humble Form'],
							rows: [
								['I', '나', '저'],
								['As for me (Topic)', '나는', '저는'],
								['I also', '나도', '저도']
							]
						}
					]
				},
				{
					id: 'exp-1-3',
					title: 'Sino-Korean Numbers (0-10)',
					content: 'Used for telephone numbers, school years, etc. Zero is read as 영 or 공.',
					tables: [
						{
							id: 'tbl-numbers-sino',
							type: 'generic',
							headers: ['Number', 'Korean'],
							rows: [
								['0', '영/공'],
								['1', '일'],
								['2', '이'],
								['3', '삼'],
								['4', '사'],
								['5', '오'],
								['6', '육'],
								['7', '칠'],
								['8', '팔'],
								['9', '구'],
								['10', '십']
							]
						}
					]
				}
			]
		},
		{
			id: 'L1-C2',
			type: 'conversation',
			title: 'Conversation 2',
			subtitle: 'Michael meets Sophia for the first time.',
			content: [
				{
					speaker: '마이클',
					text: '안녕하세요? 저는 마이클 정이에요. 이름이 뭐예요?',
					translation: 'Hello. I’m Michael Jung. What is your name?',
					audio: {
						file: '/audio/Textbook_Lesson1_C2_3rd_Edition.mp3',
						start: 10.0,
						end: 18.0
					}
				},
				{
					speaker: '소피아',
					text: '소피아 왕이에요. 반갑습니다.',
					translation: 'I’m Sophia Wang. Glad to meet you.',
					audio: {
						file: '/audio/Textbook_Lesson1_C2_3rd_Edition.mp3',
						start: 18,
						end: 22
					}
				},
				{
					speaker: '마이클',
					text: '소피아 씨는 한국 사람이에요?',
					translation: 'Are you Korean?',
					audio: {
						file: '/audio/Textbook_Lesson1_C2_3rd_Edition.mp3',
						start: 23,
						end: 27
					}
				},
				{
					speaker: '소피아',
					text: '아니요, 한국 사람이 아니에요. 중국 사람이에요.',
					translation: 'No, I’m not Korean. I’m Chinese.',
					audio: {
						file: '/audio/Textbook_Lesson1_C2_3rd_Edition.mp3',
						start: 27,
						end: 34
					}
				},
				{
					speaker: '마이클',
					text: '아, 그래요? 저는 한국 사람이에요.',
					translation: 'Oh, really? I’m Korean.',
					audio: {
						file: '/audio/Textbook_Lesson1_C2_3rd_Edition.mp3',
						start: 34,
						end: 41
					}
				}
			],
			newVocabulary: [
				{ id: 'v1-18', korean: '선생님', english: 'teacher', pos: 'noun' },
				{ id: 'v1-19', korean: '씨', english: 'Mr./Ms.', pos: 'suffix' },
				{ id: 'v1-20', korean: '영국', english: 'United Kingdom', pos: 'noun' },
				{ id: 'v1-21', korean: '영어', english: 'English language', pos: 'noun' },
				{ id: 'v1-22', korean: '이름', english: 'name', pos: 'noun' },
				{ id: 'v1-23', korean: '일본', english: 'Japan', pos: 'noun' },
				{ id: 'v1-24', korean: '중국', english: 'China', pos: 'noun' },
				{ id: 'v1-25', korean: '클래스', english: 'class', pos: 'noun' },
				{ id: 'v1-26', korean: '한국어', english: 'Korean language', pos: 'noun' },
				{ id: 'v1-27', korean: '아', english: 'oh', pos: 'interjection' },
				{ id: 'v1-28', korean: '네', english: 'yes/I see', pos: 'adverb' },
				{ id: 'v1-29', korean: '아니요', english: 'no', pos: 'adverb' },
				{ id: 'v1-30', korean: '이/가', english: 'subject particle', pos: 'particle' },
				{ id: 'v1-31', korean: '그렇다', english: "to be so ('Is that right?')", pos: 'adjective' },
				{ id: 'v1-32', korean: '반갑다', english: 'to be glad', pos: 'adjective' },
				{ id: 'v1-33', korean: '아니다', english: 'to not be (negative equation)', pos: 'copula' },
				{ id: 'v1-34', korean: '뭐', english: 'what', pos: 'pronoun' }
			],
			newExpressions: [
				{
					id: 'exp-1-4',
					title: 'Countries and Languages',
					content: 'Language is usually Country + 어. Nationality is Country + 사람.',
					tables: [
						{
							id: 'tbl-nations',
							type: 'generic',
							headers: ['Country', 'Language', 'Nationality'],
							rows: [
								['한국 (Korea)', '한국어', '한국 사람'],
								['미국 (U.S.)', '영어', '미국 사람'],
								['영국 (U.K.)', '영어', '영국 사람'],
								['일본 (Japan)', '일본어', '일본 사람'],
								['중국 (China)', '중국어', '중국 사람'],
								['프랑스 (France)', '프랑스어', '프랑스 사람']
							]
						}
					]
				}
			]
		},
		{
			id: 'L1-N1',
			type: 'narration',
			title: 'Korean Class',
			content: [
				{
					speaker: 'Narrator',
					text: '이민수 선생님은 한국어 선생님이에요. 한국 사람이에요.',
					translation: 'Professor Minsoo Lee is the Korean instructor. He is Korean.',
					audio: {
						file: '/audio/Textbook_Lesson1_N_3rd_Edition.mp3',
						start: 5,
						end: 13.3
					}
				},
				{
					speaker: 'Narrator',
					text: '김유미, 마이클 정, 소피아 왕, 스티브 윌슨은 한국어 클래스 학생이에요.',
					translation:	
						'Yumi Kim, Michael Jung, Sophia Wang, and Steve Wilson are students in the Korean class.',
					audio: {
						file: '/audio/Textbook_Lesson1_N_3rd_Edition.mp3',
						start: 13.4,
						end: 23
					}
				},
				{
					speaker: 'Narrator',
					text: '김유미는 한국 사람이에요. 마이클 정도 한국 사람이에요.',
					translation: 'Yumi Kim is Korean. Michael Jung is also Korean.',
					audio: {
						file: '/audio/Textbook_Lesson1_N_3rd_Edition.mp3',
						start: 23,
						end: 31
					}
				},
				{
					speaker: 'Narrator',
					text: '소피아 왕은 한국 사람이 아니에요. 중국 사람이에요.',
					translation: 'Sophia Wang is not Korean. She is Chinese.',
					audio: {
						file: '/audio/Textbook_Lesson1_N_3rd_Edition.mp3',
						start: 32,
						end: 40
					}
				},
				{
					speaker: 'Narrator',
					text: '스티브 윌슨도 한국 사람이 아니에요. 미국 사람이에요.',
					translation: 'Steve Wilson is also not Korean. He is American.',
					audio: {
						file: '/audio/Textbook_Lesson1_N_3rd_Edition.mp3',
						start: 40,
						end: 47
					}
				}
			],
			newVocabulary: [],
			newExpressions: []
		}
	],

	grammar: [
		{
			id: 'G1.1',
			title: 'Equational expression: N1은/는 N2이에요/예요',
			pattern: 'N1은/는 N2이에요/예요',
			description:
				"Topic-comment structure. 은/는 marks the topic. 이에요/예요 is the copula 'to be'.",
			examples: [
				{ kor: '마이클은 대학생이에요.', eng: 'Michael is a college student.' },
				{ kor: '저는 김유미예요.', eng: 'I am Yumi Kim.' }
			],
			tables: [
				{
					id: 'tbl-copula-aff',
					type: 'conjugation',
					headers: ['Noun Ending', 'Topic Particle', 'Copula'],
					rows: [
						['Consonant', '은', '이에요'],
						['Vowel', '는', '예요']
					]
				}
			]
		},
		{
			id: 'G1.2',
			title: 'Omission of redundant elements',
			pattern: 'Context dependent',
			description: 'Subjects/topics are often omitted when they are obvious from context.',
			examples: [
				{ kor: '(저는) 3학년이에요.', eng: '[I] am a junior.' },
				{ kor: '(이름이) 뭐예요?', eng: 'What is [your name]?' }
			]
		},
		{
			id: 'G1.3',
			title: 'Comparing items: 은/는 vs. 도',
			pattern: 'N도',
			description: 'The particles 은/는 and 도 are used to compare two or more items.',
			examples: [
				{ kor: '김유미는 한국 사람이에요.', eng: 'Yumi Kim is Korean.' },
				{ kor: '저도 1학년이에요.', eng: 'I am also a freshman.' }
			],
			tables: [
				{
					id: 'tbl-particles-comp',
					type: 'comparison',
					headers: ['Particle', 'Function'],
					rows: [
						['은/는', 'The items are different or contrastive.'],
						['도', 'The items are parallel (also/too).']
					]
				}
			]
		},
		{
			id: 'G1.4',
			title: 'Yes/no questions',
			pattern: 'N이에요/예요? (Rising Intonation)',
			description:
				'In Korean, the word order remains the same for questions; only the intonation rises.',
			examples: [
				{ kor: '한국 사람이에요?', eng: 'Are you Korean?' },
				{ kor: '네, 한국 사람이에요.', eng: 'Yes, I am Korean.' }
			]
		},
		{
			id: 'G1.5',
			title: 'Negative equational expression',
			pattern: 'N1은/는 N2이/가 아니에요',
			description:
				"To say 'N1 is not N2', use the pattern with the subject particle 이/가 followed by 아니에요.",
			examples: [
				{ kor: '소피아 왕은 한국 사람이 아니에요.', eng: 'Sophia Wang is not Korean.' },
				{ kor: '저는 1학년이 아니에요.', eng: 'I am not a freshman.' }
			],
			tables: [
				{
					id: 'tbl-copula-neg',
					type: 'conjugation',
					headers: ['Noun Ending', 'Subject Particle', 'Negative Copula'],
					rows: [
						['Consonant', '이', '아니에요'],
						['Vowel', '가', '아니에요']
					]
				}
			]
		}
	],

	culture: [
		{
			title: 'Greetings with a bow',
			content:
				'When you greet someone in Korean culture, bowing shows courtesy. The depth of the bow depends on age and social status. For most people, a slight bow is used. Shaking hands is also common; usually, the younger person bows first, then shakes hands if offered.'
		},
		{
			title: 'Korean Names',
			content:
				'The surname (family name) comes first, followed by the given name. Most names are three syllables (e.g., Kim Yu-mi). Women do not change their family names upon marriage.'
		}
	],

	usage: [
		{
			id: 'U1-A',
			title: 'Introducing Oneself',
			description: 'Introduce yourself including your Name, School Year, and Nationality.',
			exampleDialogue: [
				{
					speaker: 'Me',
					text: '안녕하세요? 저는 마이클 정이에요.',
					translation: 'Hello, I am Michael Jung.'
				},
				{
					speaker: 'Me',
					text: '1학년이에요. 한국 사람이에요.',
					translation: "I'm a freshman. I'm Korean."
				}
			]
		},
		{
			id: 'U1-B',
			title: 'Describing Another Person',
			description:
				'Interview a partner to find out their name, year, and nationality, then describe them.',
			exampleDialogue: [
				{ speaker: 'A', text: '이름이 뭐예요?', translation: 'What is your name?' },
				{ speaker: 'B', text: '마이클 정이에요.', translation: 'I am Michael Jung.' },
				{ speaker: 'A', text: '2학년이에요?', translation: 'Are you a sophomore?' },
				{ speaker: 'B', text: '아니요, 1학년이에요.', translation: 'No, I am a freshman.' }
			]
		}
	]
};
