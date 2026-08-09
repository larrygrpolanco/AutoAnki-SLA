import type { Lesson } from '../../types';

export const lessonFive: Lesson = {
	id: 5,
	titleEn: 'At the Bookstore',
	titleKr: '서점에서',

	exercises: ['sentence-scramble'],

	segments: [
		{
			id: 'L5-C1',
			type: 'conversation',
			title: 'Conversation 1',
			subtitle: 'Meeting a friend at the bookstore.',
			content: [
				{
					speaker: '제니',
					text: '리사 씨, 안녕하세요?',
					translation: 'Hi, Lisa!',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 19.5,
						end: 22
					}
				},
				{
					speaker: '리사',
					text: '어, 제니 씨, 오래간만이에요.',
					translation: 'Oh, hi, Jenny. It’s been a long time.',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 23,
						end: 27
					}
				},
				{
					speaker: '제니',
					text: '네, 오래간만이에요. 그런데 어디 가세요?',
					translation: 'Yes, it’s been a long while. (By the way,) where are you going?',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 27,
						end: 33
					}
				},
				{
					speaker: '리사',
					text: '커피숍에 가요. 제니 씨는 어디 가세요?',
					translation: 'I’m going to the cafe. Where are you going, Jenny?',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 33,
						end: 39
					}
				},
				{
					speaker: '제니',
					text: '저는 서점에 가요. 친구가 학교 앞 서점에서 일을 해요.',
					translation:
						'I’m going to the bookstore. My friend works at the bookstore across campus.',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 39,
						end: 46
					}
				},
				{
					speaker: '리사',
					text: '아, 그래요? 그럼, 다음에 또 봐요.',
					translation: 'Oh, really? Okay, I’ll see you (next time).',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 46,
						end: 51
					}
				},
				{
					speaker: '제니',
					text: '네, 안녕히 가세요.',
					translation: 'Okay, good-bye.',
					audio: {
						file: '/audio/Textbook_Lesson5_C1_3rd_Edition.mp3',
						start: 51.5,
						end: 55
					}
				}
			],
			newVocabulary: [
				{ id: 'v5-1', korean: '공원', english: 'park', pos: 'noun' },
				{ id: 'v5-2', korean: '다음', english: 'next, following', pos: 'noun' },
				{ id: 'v5-3', korean: '랩', english: 'lab', pos: 'noun' },
				{ id: 'v5-4', korean: '백화점', english: 'department store', pos: 'noun' },
				{ id: 'v5-5', korean: '생일', english: 'birthday', pos: 'noun' },
				{ id: 'v5-6', korean: '선물', english: 'present, gift', pos: 'noun' },
				{ id: 'v5-7', korean: '쇼핑(하다)', english: 'shopping', pos: 'noun' },
				{ id: 'v5-8', korean: '연습(하다)', english: 'practice', pos: 'noun' },
				{ id: 'v5-9', korean: '오래간만', english: 'after a long time', pos: 'noun' },
				{ id: 'v5-10', korean: '운동(하다)', english: 'exercise', pos: 'noun' },
				{ id: 'v5-11', korean: '일(하다)', english: 'work', pos: 'noun' },
				{ id: 'v5-12', korean: '저녁', english: 'evening / dinner', pos: 'noun' },
				{ id: 'v5-13', korean: '전화(하다)', english: 'phone call', pos: 'noun' },
				{ id: 'v5-14', korean: '점심', english: 'lunch', pos: 'noun' },
				{ id: 'v5-15', korean: '커피숍', english: 'coffee shop, cafe', pos: 'noun' },
				{ id: 'v5-16', korean: '테니스', english: 'tennis', pos: 'noun' },
				{ id: 'v5-17', korean: '햄버거', english: 'hamburger', pos: 'noun' },
				{ id: 'v5-18', korean: '가르치다', english: 'to teach', pos: 'verb' },
				{ id: 'v5-19', korean: '사다', english: 'to buy', pos: 'verb' },
				{ id: 'v5-20', korean: '치다', english: 'to play (tennis)', pos: 'verb' },
				{ id: 'v5-21', korean: '또', english: 'again', pos: 'adverb' },
				{ id: 'v5-22', korean: '에', english: 'to (dest) / at, in (time)', pos: 'particle' },
				{ id: 'v5-23', korean: '에서', english: 'in, at (dynamic location)', pos: 'particle' },
				{ id: 'v5-24', korean: '그런데', english: 'by the way / however', pos: 'conjunction' },
				{ id: 'v5-25', korean: '그럼', english: '(if so) then', pos: 'conjunction' }
			],
			newExpressions: [
				{
					id: 'exp-5-1',
					title: '오래간만이에요',
					content:
						"Equivalent to 'It's been a long while' or 'Long time no see'. Used when meeting after a long gap."
				},
				{
					id: 'exp-5-2',
					title: 'Farewells: 가세요 vs 계세요',
					content:
						"안녕히 가세요 (Go in peace) is said to the person leaving. 안녕히 계세요 (Stay in peace) is said to the person staying.",
					tables: [
						{
							id: 'tbl-farewells',
							type: 'comparison',
							headers: ['Situation', 'Speaker Says'],
							rows: [
								['You stay, they leave', '안녕히 가세요'],
								['You leave, they stay', '안녕히 계세요'],
								['Both leave (neutral)', '안녕히 가세요']
							]
						}
					]
				}
			]
		},
		{
			id: 'L5-C2',
			type: 'conversation',
			title: 'Conversation 2',
			subtitle: 'I’m going to the department store to buy a gift.',
			content: [
				{
					speaker: '소피아',
					text: '마이클 씨, 오늘 뭐 하세요?',
					translation: 'Michael, what are you doing today?',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 7,
						end: 11
					}
				},
				{
					speaker: '마이클',
					text: '친구 생일 선물 사러 백화점에 가요.',
					translation: 'I’m going to the department store to buy a birthday gift for my friend.',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 11,
						end: 15
					}
				},
				{
					speaker: '소피아',
					text: '친구 생일이 언제예요?',
					translation: 'When is it?',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 15,
						end: 18.5
					}
				},
				{
					speaker: '마이클',
					text: '이번 토요일이에요. 소피아 씨는 오늘 뭐 하세요?',
					translation: 'This Saturday. Sophia, what are you doing today?',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 18.5,
						end: 24.5
					}
				},
				{
					speaker: '소피아',
					text: '저는 수업 들으러 학교에 가요.',
					translation: 'I’m going to school for my morning class (to take a class).',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 24.5,
						end: 28
					}
				},
				{
					speaker: '마이클',
					text: '수업이 몇 시에 있어요?',
					translation: 'What time is your class?',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 28.5,
						end: 31
					}
				},
				{
					speaker: '소피아',
					text: '오전 10시에 있어요.',
					translation: 'At ten o’clock.',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 31,
						end: 34
					}
				},
				{
					speaker: '마이클',
					text: '그럼, 오후에 저하고 같이 백화점에 가요.',
					translation: 'Then let’s go to the department store together in the afternoon.',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 34.5,
						end: 40
					}
				},
				{
					speaker: '소피아',
					text: '네, 좋아요.',
					translation: 'Okay, sounds good.',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 40,
						end: 42
					}
				},
				{
					speaker: '마이클',
					text: '3시 30분 괜찮아요?',
					translation: 'Is 3:30 okay?',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 42,
						end: 45.5
					}
				},
				{
					speaker: '소피아',
					text: '네, 괜찮아요.',
					translation: 'Yes, it’s okay.',
					audio: {
						file: '/audio/Textbook_Lesson5_C2_3rd_Edition.mp3',
						start: 45.5,
						end: 48
					}
				}
			],
			newVocabulary: [
				{ id: 'v5-26', korean: '가게', english: 'store', pos: 'noun' },
				{ id: 'v5-27', korean: '오전', english: 'morning, a.m.', pos: 'noun' },
				{ id: 'v5-28', korean: '오후', english: 'afternoon, p.m.', pos: 'noun' },
				{ id: 'v5-29', korean: '옷', english: 'clothes', pos: 'noun' },
				{ id: 'v5-30', korean: '이번', english: 'this (time)', pos: 'noun' },
				{ id: 'v5-31', korean: '정치학', english: 'political science', pos: 'noun' },
				{ id: 'v5-32', korean: '학기', english: 'semester', pos: 'noun' },
				{ id: 'v5-33', korean: '월요일', english: 'Monday', pos: 'noun' },
				{ id: 'v5-34', korean: '화요일', english: 'Tuesday', pos: 'noun' },
				{ id: 'v5-35', korean: '수요일', english: 'Wednesday', pos: 'noun' },
				{ id: 'v5-36', korean: '목요일', english: 'Thursday', pos: 'noun' },
				{ id: 'v5-37', korean: '금요일', english: 'Friday', pos: 'noun' },
				{ id: 'v5-38', korean: '토요일', english: 'Saturday', pos: 'noun' },
				{ id: 'v5-39', korean: '일요일', english: 'Sunday', pos: 'noun' },
				{ id: 'v5-40', korean: '걷다', english: 'to walk', pos: 'verb' },
				{ id: 'v5-41', korean: '듣다', english: 'to listen / to take (a course)', pos: 'verb' },
				{ id: 'v5-42', korean: '좋아하다', english: 'to like', pos: 'verb' },
				{ id: 'v5-43', korean: '같이', english: 'together', pos: 'adverb' },
				{ id: 'v5-44', korean: '언제', english: 'when', pos: 'adverb' },
				{ id: 'v5-45', korean: '과목', english: 'course, subject', pos: 'counter' },
				{ id: 'v5-46', korean: '분', english: 'minute', pos: 'counter' },
				{ id: 'v5-47', korean: '시', english: 'hour, o’clock', pos: 'counter' },
				{ id: 'v5-48', korean: '하고', english: 'with', pos: 'particle' },
				{ id: 'v5-49', korean: '(으)러', english: 'in order to', pos: 'suffix' }
			],
			newExpressions: [
				{
					id: 'exp-5-3',
					title: 'Telling Time',
					content:
						'시 (hour) uses Native Korean numbers, while 분 (minute) uses Sino-Korean numbers.',
					tables: [
						{
							id: 'tbl-time-nums',
							type: 'comparison',
							headers: ['Unit', 'Number System', 'Example'],
							rows: [
								['시 (Hour)', 'Native', '12시 (열두 시)'],
								['분 (Minute)', 'Sino-Korean', '50분 (오십 분)']
							]
						}
					]
				}
			]
		},
		{
			id: 'L5-N1',
			type: 'narration',
			title: 'Birthday Gift',
			content: [
				{
					speaker: 'Narrator',
					text: '이번 토요일이 제 친구 스티브 생일이에요.',
					translation: 'This Saturday is my friend Steve’s birthday.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 5,
						end: 11
					}
				},
				{
					speaker: 'Narrator',
					text: '그래서 오늘 생일 선물을 사러 백화점에 가요. 소피아하고 같이 가요.',
					translation:
						'So I’m going to the department store today to buy a birthday present. I’m going with Sophia.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 11.8,
						end: 22
					}
				},
				{
					speaker: 'Narrator',
					text: '백화점 안에는 커피숍, 식당, 옷가게, 서점이 있어요.',
					translation:
						'In the department store there is a coffee shop, restaurant, clothing store, and a bookstore.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 22,
						end: 31
					}
				},
				{
					speaker: 'Narrator',
					text: '1층에 서점하고 커피숍이 있어요. 2층에는 옷가게가 있어요. 그리고 3층에는 식당이 있어요.',
					translation:
						'The bookstore and coffee shop are on the 1st floor. The clothing store is on the 2nd floor. And the restaurant is on the 3rd floor.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 31,
						end: 46
					}
				},
				{
					speaker: 'Narrator',
					text: '스티브가 책을 아주 좋아해요. 그래서 저는 서점에 책을 사러 가요.',
					translation:
						'Steve really likes books. So I’m going to the bookstore to buy a book.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 46,
						end: 57
					}
				},
				{
					speaker: 'Narrator',
					text: '소피아는 옷가게에 옷을 사러 가요. 옷가게 옷이 아주 예뻐요.',
					translation:
						'Sophia is going to the clothing store to buy clothes. The clothing store’s clothes are very pretty.',
					audio: {
						file: '/audio/Textbook_Lesson5_N_3rd_Edition.mp3',
						start: 57,
						end: 68
					}
				}
			],
			newVocabulary: [],
			newExpressions: []
		}
	],

	grammar: [
		{
			id: 'G5.1',
			title: 'The locative particles 에 and 에서',
			pattern: 'N에 vs N에서',
			description:
				'에 indicates a static location (existence) or a destination. 에서 indicates the location where an activity takes place.',
			examples: [
				{ kor: '집에 계세요.', eng: 'He is at home. (Static)' },
				{ kor: '학교에 가요.', eng: 'I go to school. (Destination)' },
				{ kor: '공원에서 운동해요.', eng: 'I exercise at the park. (Dynamic Activity)' }
			],
			tables: [
				{
					id: 'tbl-locative-particles',
					type: 'comparison',
					headers: ['Function', 'Particle', 'Associated Verbs'],
					rows: [
						['Static Location', '에', '있다, 없다, 계시다'],
						['Destination/Goal', '에', '가다, 오다, 다니다'],
						['Dynamic Location', '에서', '공부하다, 일하다, 만나다 (Action Verbs)']
					]
				}
			]
		},
		{
			id: 'G5.2',
			title: 'The basic sentence pattern (SOV)',
			pattern: 'Subject + Object + Verb',
			description:
				'The basic word order is Subject-Object-Verb. The order of subject and object is flexible, but the verb must always come at the end.',
			examples: [
				{ kor: '유미가 교실에서 한국어를 공부해요.', eng: 'Yumi studies Korean in the classroom.' },
				{
					kor: '교실에서 한국어를 유미가 공부해요.',
					eng: 'Yumi studies Korean in the classroom (emphasis changed).'
				}
			]
		},
		{
			id: 'G5.3',
			title: 'Purpose of movement ~(으)러',
			pattern: 'Vst + (으)러 + 가다/오다',
			description:
				'Indicates the purpose of going or coming. Parallel to "(in order) to [verb]".',
			examples: [
				{ kor: '점심 먹으러 식당에 가요.', eng: 'I go to the cafeteria to eat lunch.' },
				{ kor: '테니스 치러 가요.', eng: 'I go to play tennis.' }
			],
			tables: [
				{
					id: 'tbl-purpose-conj',
					type: 'conjugation',
					headers: ['Stem Ending', 'Suffix', 'Example'],
					rows: [
						['Consonant', '~으러', '먹다 → 먹으러'],
						['Vowel', '~러', '사다 → 사러'],
						['ㄹ ending', '~러', '살다 → 살러']
					]
				}
			]
		},
		{
			id: 'G5.4',
			title: 'Irregular verbs in /ㄷ/',
			pattern: 'Irregular Conjugation',
			description:
				'For some verbs ending in ㄷ, the ㄷ changes to ㄹ when followed by a vowel.',
			examples: [
				{ kor: '음악을 들어요.', eng: 'I listen to music.' },
				{ kor: '공원을 걸어요.', eng: 'I walk in the park.' }
			],
			tables: [
				{
					id: 'tbl-irr-d',
					type: 'conjugation',
					headers: ['Type', 'Stem', 'Polite (아요/어요)', 'Honorific (으세요)'],
					rows: [
						['Irregular', '듣다 (to listen)', '들어요', '들으세요'],
						['Irregular', '걷다 (to walk)', '걸어요', '걸으세요'],
						['Regular', '받다 (to receive)', '받아요', '받으세요'],
						['Regular', '닫다 (to close)', '닫아요', '닫으세요']
					]
				}
			]
		}
	],

	culture: [
		{
			title: 'Seaweed Soup (미역국)',
			content:
				'Seaweed soup is a traditional birthday dish in Korea. It is also eaten by women after childbirth for recovery due to its calcium and iodine content. However, because seaweed is slippery, students avoid it on exam days to avoid "slipping" (failing) the test.'
		}
	],

	usage: [
		{
			id: 'U5-A',
			title: 'Saying Good-bye',
			description:
				'Practice the correct closing greeting based on who is leaving and who is staying.',
			exampleDialogue: [
				{
					speaker: 'Host (Staying)',
					text: '안녕히 가세요.',
					translation: 'Go in peace.'
				},
				{
					speaker: 'Guest (Leaving)',
					text: '안녕히 계세요.',
					translation: 'Stay in peace.'
				}
			]
		},
		{
			id: 'U5-B',
			title: 'Destination and Purpose',
			description: "Practice asking 'Where are you going?' and answering with the purpose.",
			exampleDialogue: [
				{
					speaker: 'A',
					text: '어디 가세요?',
					translation: 'Where are you going?'
				},
				{
					speaker: 'B',
					text: '선물 사러 백화점에 가요.',
					translation: 'I am going to the department store to buy a gift.'
				}
			]
		},
		{
			id: 'U5-D',
			title: 'Asking and Telling Time',
			description: 'Ask for the time and reply using Native (hour) and Sino (minute) numbers.',
			exampleDialogue: [
				{
					speaker: 'A',
					text: '지금 몇 시예요?',
					translation: 'What time is it now?'
				},
				{
					speaker: 'B',
					text: '10시 24분이에요.',
					translation: 'It is 10:24.'
				}
			]
		}
	]
};