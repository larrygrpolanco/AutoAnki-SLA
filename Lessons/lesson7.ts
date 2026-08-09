import type { Lesson } from '../../types';

export const lessonSeven: Lesson = {
  id: 7,
  titleEn: "The Weekend",
  titleKr: "주말",

	exercises: ['sentence-scramble'],   

  segments: [
    {
      id: "L7-C1",
      type: "conversation",
      title: "Conversation 1",
      subtitle: "Steve and Lisa talk about their weekend plans.",
      content: [
        { 
          speaker: "리사", 
          text: "스티브 씨, 이번 주말에 약속 있으세요?", 
          translation: "Steve, do you have any plans for this weekend?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 25, end: 31 } 
        },
        { 
          speaker: "스티브", 
          text: "아니요, 없어요.", 
          translation: "No, I don't." ,
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 31, end: 34 } 
        },
        { 
          speaker: "리사", 
          text: "저는 친구하고 영화 볼 거예요. 스티브 씨도 같이 가요.", 
          translation: "I'm going to see a movie with my friend. Why don't you join us, Steve?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 34, end: 43 } 
        },
        { 
          speaker: "스티브", 
          text: "무슨 영화 볼 거예요?", 
          translation: "What movie are you going to watch?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 43, end: 46 } 
        },
        { 
          speaker: "리사", 
          text: "액션 영화요.", 
          translation: "An action movie.",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 46, end: 48 } 
        },
        { 
          speaker: "스티브", 
          text: "네, 같이 가요. 저도 액션 영화 좋아해요. 어느 영화관에서 볼 거예요?", 
          translation: "Okay. I'll go with you. I like action movies, too. Which movie theater are you going to see it at?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 48, end: 59 } 
        },
        { 
          speaker: "리사", 
          text: "브로드웨이 극장 어때요?", 
          translation: "What about Broadway Theater?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 59, end: 62 } 
        },
        { 
          speaker: "스티브", 
          text: "네, 좋아요.", 
          translation: "Okay, fine.",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 62, end: 65 } 
        },
        { 
          speaker: "리사", 
          text: "일요일 오전 어때요?", 
          translation: "How about Sunday morning?",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 65, end: 68 } 
        },
        { 
          speaker: "스티브", 
          text: "좋아요. 오전에는 사람이 없을 거예요.", 
          translation: "Great. There will not be many people in the morning.",
          audio: { file: "/audio/Textbook_Lesson7_C1_3rd_Edition.mp3", start: 68, end: 74 } 
        }
      ],
      newVocabulary: [
        { id: "v7-1", korean: "계절", english: "season", pos: "noun" },
        { id: "v7-2", korean: "극장", english: "theater", pos: "noun" },
        { id: "v7-3", korean: "꽃", english: "flower", pos: "noun" },
        { id: "v7-4", korean: "나라", english: "country", pos: "noun" },
        { id: "v7-5", korean: "내년", english: "next year", pos: "noun" },
        { id: "v7-6", korean: "대학원", english: "graduate school", pos: "noun" },
        { id: "v7-7", korean: "방학", english: "school vacation", pos: "noun" },
        { id: "v7-8", korean: "악기", english: "musical instrument", pos: "noun" },
        { id: "v7-9", korean: "액션 영화", english: "action movie", pos: "noun" },
        { id: "v7-10", korean: "여름", english: "summer", pos: "noun" },
        { id: "v7-11", korean: "여행(하다)", english: "travel", pos: "noun" },
        { id: "v7-12", korean: "영화", english: "movie", pos: "noun" },
        { id: "v7-13", korean: "영화관", english: "movie theater", pos: "noun" },
        { id: "v7-14", korean: "코미디", english: "comedy", pos: "noun" },
        { id: "v7-15", korean: "피아노", english: "piano", pos: "noun" },
        { id: "v7-16", korean: "받다", english: "to receive", pos: "verb" },
        { id: "v7-17", korean: "축하하다", english: "to congratulate", pos: "verb" },
        { id: "v7-18", korean: "아마", english: "probably, perhaps", pos: "adverb" },
        { id: "v7-19", korean: "정말", english: "really", pos: "adverb" },
        { id: "v7-20", korean: "무슨", english: "what, what kind of", pos: "adjective", tags: ["pre-noun"] },
        { id: "v7-21", korean: "어느", english: "which", pos: "adjective", tags: ["pre-noun"] },
        { id: "v7-22", korean: "~(으)ㄹ 거예요", english: "probability", pos: "suffix" }
      ],
      newExpressions: [
        {
          id: "exp-7-1",
          title: "Time Expressions",
          content: "Words referring to days, weeks, months, and years relative to the present.",
          tables: [
            {
              id: "tbl-time-expr",
              type: "generic",
              headers: ["Unit", "Last (지난)", "This (이번)", "Next (다음)"],
              rows: [
                ["Day", "어제 (Yesterday)", "오늘 (Today)", "내일 (Tomorrow)"],
                ["Week (주)", "지난 주", "이번 주", "다음 주"],
                ["Weekend (주말)", "지난 주말", "이번 주말", "다음 주말"],
                ["Month (달)", "지난 달", "이번 달", "다음 달"],
                ["Year (해/년)", "작년", "올해", "내년"]
              ]
            }
          ]
        }
      ]
    },
    {
      id: "L7-C2",
      type: "conversation",
      title: "Conversation 2",
      subtitle: "Michael asks Sophia about her weekend plans.",
      content: [
        { 
          speaker: "마이클", 
          text: "소피아 씨, 다음 주말에 뭐 하세요?", 
          translation: "Sophia, what are you doing next weekend?",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 7, end: 12 } 
        },
        { 
          speaker: "소피아", 
          text: "여동생이 뉴욕에서 와요. 그래서 집에서 청소하고 음식 준비할 거예요.", 
          translation: "My younger sister is visiting from New York, so I'm going to clean the house and prepare some food.",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 12, end: 23 } 
        },
        { 
          speaker: "마이클", 
          text: "아 그럼, 학기말 파티에 안 갈 거예요?", 
          translation: "Oh then, aren't you going to the semester-end party?",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 23, end: 29 } 
        },
        { 
          speaker: "소피아", 
          text: "네, 아마 못 갈 거예요.", 
          translation: "I don't think I'll be able to make it.",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 29, end: 33 } 
        },
        { 
          speaker: "마이클", 
          text: "동생을 자주 못 만나요?", 
          translation: "Don't you see her often?",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 33, end: 36.5 } 
        },
        { 
          speaker: "소피아", 
          text: "네, 자주 못 봐요. 그래서 오래간만에 이야기를 많이 할 거예요.", 
          translation: "No, so we're going to spend a lot of time catching up.",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 36.5, end: 46 } 
        },
        { 
          speaker: "마이클", 
          text: "그럼, 동생하고 주말 잘 보내세요.", 
          translation: "Then have a nice weekend with your sister.",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 46, end: 51 } 
        },
        { 
          speaker: "소피아", 
          text: "마이클 씨도 방학 잘 보내세요.", 
          translation: "Have a good break as well.",
          audio: { file: "/audio/Textbook_Lesson7_C2_3rd_Edition.mp3", start: 51, end: 56 } 
        }
      ],
      newVocabulary: [
        { id: "v7-23", korean: "가을", english: "autumn, fall", pos: "noun" },
        { id: "v7-24", korean: "겨울", english: "winter", pos: "noun" },
        { id: "v7-25", korean: "마트", english: "supermarket", pos: "noun" },
        { id: "v7-26", korean: "봄", english: "spring", pos: "noun" },
        { id: "v7-27", korean: "설거지(하다)", english: "dishwashing", pos: "noun" },
        { id: "v7-28", korean: "신문", english: "newspaper", pos: "noun" },
        { id: "v7-29", korean: "심리학", english: "psychology", pos: "noun" },
        { id: "v7-30", korean: "이야기(하다)", english: "talk, chat", pos: "noun" },
        { id: "v7-31", korean: "전공(하다)", english: "major", pos: "noun" },
        { id: "v7-32", korean: "주", english: "week", pos: "noun" },
        { id: "v7-33", korean: "준비(하다)", english: "preparation", pos: "noun" },
        { id: "v7-34", korean: "청소(하다)", english: "cleaning", pos: "noun" },
        { id: "v7-35", korean: "학기말", english: "the end of the semester", pos: "noun" },
        { id: "v7-36", korean: "조용하다", english: "to be quiet", pos: "adjective" },
        { id: "v7-37", korean: "흐리다", english: "to be cloudy", pos: "adjective" },
        { id: "v7-38", korean: "만들다", english: "to make", pos: "verb" },
        { id: "v7-39", korean: "보내다", english: "to spend time", pos: "verb" },
        { id: "v7-40", korean: "장(을) 보다", english: "to buy groceries", pos: "verb" },
        { id: "v7-41", korean: "가끔", english: "sometimes, occasionally", pos: "adverb" },
        { id: "v7-42", korean: "많이", english: "much, many", pos: "adverb" },
        { id: "v7-43", korean: "서로", english: "each other", pos: "adverb" },
        { id: "v7-44", korean: "특히", english: "particularly", pos: "adverb" },
        { id: "v7-45", korean: "~고", english: "and (clausal connective)", pos: "suffix" }
      ],
      newExpressions: []
    },
    {
      id: "L7-N1",
      type: "narration",
      title: "Sophia's Weekend",
      content: [
        { 
          speaker: "소피아", 
          text: "이번 학기에는 아주 바빴어요. 특히 지난 주에는 시험이 많았어요.", 
          translation: "I was very busy this semester; I had a lot of exams last week, in particular.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 6, end: 16 } 
        },
        { 
          speaker: "소피아", 
          text: "주말에는 친구들하고 같이 영화를 보러 갔어요.", 
          translation: "I went to watch a movie with some friends over the weekend.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 16, end: 24 } 
        },
        { 
          speaker: "소피아", 
          text: "영화가 참 재미있었어요. 영화를 보고 중국 음식을 먹었어요.", 
          translation: "The movie was really good. After the movie we had some Chinese food.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 24, end: 33.5 } 
        },
        { 
          speaker: "소피아", 
          text: "다음 주말에는 여동생이 뉴욕에서 올 거예요.", 
          translation: "Next weekend my younger sister will be visiting from New York.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 33.5, end: 41 } 
        },
        { 
          speaker: "소피아", 
          text: "동생은 다음 학기에 대학에 가요. 심리학을 전공할 거예요.", 
          translation: "She will be attending college next semester and will be majoring in psychology.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 41, end: 51 } 
        },
        { 
          speaker: "소피아", 
          text: "동생도 저도 많이 바빠요. 그래서 서로 전화를 자주 못 해요.", 
          translation: "My sister and I are both very busy. So we can't call each other often.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 51, end: 62 } 
        },
        { 
          speaker: "소피아", 
          text: "이번에 동생하고 오래간만에 이야기를 많이 할 거예요.", 
          translation: "For the first time in a long while, we are going to spend some time catching up.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 62, end: 70 } 
        },
        { 
          speaker: "소피아", 
          text: "동생이 한국 음식을 좋아해요. 그래서 집에서 한국 음식을 만들 거예요.", 
          translation: "My sister really enjoys Korean food so I will make Korean food for her at home.",
          audio: { file: "/audio/Textbook_Lesson7_N_3rd_Edition.mp3", start: 70, end: 83 } 
        }
      ],
      newVocabulary: [
        // Vocabulary found in the "Usage" section, placed here for flashcard accessibility
        { id: "v7-u1", korean: "독서", english: "reading", pos: "noun", tags: ["usage", "hobby"] },
        { id: "v7-u2", korean: "연극", english: "play", pos: "noun", tags: ["usage", "hobby"] },
        { id: "v7-u3", korean: "공포 영화", english: "horror movie", pos: "noun", tags: ["usage", "movie"] },
        { id: "v7-u4", korean: "농구", english: "basketball", pos: "noun", tags: ["usage", "sports"] },
        { id: "v7-u5", korean: "축구", english: "soccer", pos: "noun", tags: ["usage", "sports"] },
        { id: "v7-u6", korean: "야구", english: "baseball", pos: "noun", tags: ["usage", "sports"] },
        { id: "v7-u7", korean: "소설", english: "novel", pos: "noun", tags: ["usage", "book"] },
        { id: "v7-u8", korean: "시", english: "poetry", pos: "noun", tags: ["usage", "book"] },
        { id: "v7-u9", korean: "만화책", english: "comic book", pos: "noun", tags: ["usage", "book"] },
        { id: "v7-u10", korean: "잡지", english: "magazine", pos: "noun", tags: ["usage", "book"] },
        { id: "v7-u11", korean: "한식", english: "Korean food", pos: "noun", tags: ["usage", "food"] },
        { id: "v7-u12", korean: "양식", english: "Western food", pos: "noun", tags: ["usage", "food"] },
        { id: "v7-u13", korean: "문학", english: "literature", pos: "noun", tags: ["usage", "major"] },
        { id: "v7-u14", korean: "역사", english: "history", pos: "noun", tags: ["usage", "major"] },
        { id: "v7-u15", korean: "정치학", english: "political science", pos: "noun", tags: ["usage", "major"] }
      ],
      newExpressions: []
    }
  ],

  grammar: [
    {
      id: "G7.1",
      title: "Probability: ~(으)ㄹ 거예요",
      pattern: "Vst + (으)ㄹ 거예요",
      description: "Expression of probability, intention, or plan. For probability, it translates to 'probably' or 'likely'. For intention, it translates to 'will' or 'am going to'.",
      examples: [
        { kor: "이번 방학에 뭐 할 거예요?", eng: "What will you do this vacation?" },
        { kor: "친구하고 영화 볼 거예요.", eng: "I'm going to see a movie with a friend." },
        { kor: "오후에 비가 올 거예요.", eng: "It will probably rain in the afternoon." }
      ],
      tables: [
        {
          id: "tbl-prob-conj",
          type: "conjugation",
          headers: ["Stem Ending", "Suffix", "Example"],
          rows: [
            ["Vowel", "ㄹ 거예요", "가다 → 갈 거예요"],
            ["Consonant", "을 거예요", "먹다 → 먹을 거예요"],
            ["L-Irregular (ㄹ)", "거예요 (drop ㄹ)", "놀다 → 놀 거예요"],
            ["D-Irregular (ㄷ)", "을 거예요 (ㄷ→ㄹ)", "듣다 → 들을 거예요"],
            ["B-Irregular (ㅂ)", "을 거예요 (ㅂ→우)", "춥다 → 추울 거예요"]
          ]
        }
      ]
    },
    {
      id: "G7.2",
      title: "무슨 vs. 어느",
      pattern: "N/A",
      description: "'무슨' asks 'what kind of' (open-ended). '어느' asks 'which' (choice from a limited set). Both must precede a noun.",
      examples: [
        { kor: "무슨 영화 좋아해요?", eng: "What (kind of) movies do you like?" },
        { kor: "어느 극장에서 볼 거예요?", eng: "Which theater (of the known ones) will you watch it at?" }
      ],
      tables: [
        {
          id: "tbl-what-which",
          type: "comparison",
          headers: ["Word", "Meaning", "Usage"],
          rows: [
            ["무슨", "What / What kind of", "Open inquiry describing the nature of the noun."],
            ["어느", "Which", "Selecting from a limited set of options."]
          ]
        }
      ]
    },
    {
      id: "G7.3",
      title: "The clausal connective ~고",
      pattern: "Clause1 + 고 + Clause2",
      description: "Used to link two clauses like 'and'. Indicates that two states coexist or events happen sequentially.",
      examples: [
        { kor: "어제는 흐리고 추웠어요.", eng: "Yesterday was cloudy and cold." },
        { kor: "밥을 먹고 학교에 가요.", eng: "I eat and (then) go to school." }
      ]
    },
    {
      id: "G7.4",
      title: "Negative questions",
      pattern: "Answering with 네 / 아니요",
      description: "In Korean, 'Yes' (네) signifies agreement with the statement asked, even if the question is negative.",
      examples: [
        { kor: "파티에 안 갈 거예요?", eng: "Are you not going to the party?" },
        { kor: "네, 안 갈 거예요.", eng: "Yes (that is correct), I am not going." },
        { kor: "아니요, 갈 거예요.", eng: "No (that is incorrect), I am going." }
      ],
      tables: [
        {
          id: "tbl-neg-q",
          type: "comparison",
          headers: ["Question", "Answer (Korean)", "Meaning"],
          rows: [
            ["안 가요? (Aren't you going?)", "네.", "Correct, I am NOT going."],
            ["안 가요? (Aren't you going?)", "아니요.", "Incorrect, I AM going."]
          ]
        }
      ]
    }
  ],

  culture: [
    {
      title: "National Holidays in Korea",
      content: "Major holidays include Seollal (Lunar New Year) and Chuseok (Korean Thanksgiving). During Seollal, people wear Hanbok, perform bows (Sebae) to elders, and eat rice cake soup (Tteokguk). Chuseok involves visiting ancestral graves and eating Songpyeon."
    }
  ],

  usage: [
    {
      id: "U7-A",
      title: "Talking about weekend plans",
      description: "Discuss what you are going to do using ~(으)ㄹ 거예요. Cover who, where, and what.",
      exampleDialogue: [
        { speaker: "A", text: "주말에 뭐 할 거예요?", translation: "What are you doing this weekend?" },
        { speaker: "B", text: "친구하고 영화 볼 거예요.", translation: "I'm going to see a movie with a friend." },
        { speaker: "A", text: "무슨 영화 볼 거예요?", translation: "What movie will you see?" }
      ]
    },
    {
      id: "U7-B",
      title: "Talking about Likes and Dislikes",
      description: "Interview a partner about their favorites using '무슨' (e.g., What kind of sports do you like?).",
      exampleDialogue: [
        { speaker: "A", text: "무슨 운동 좋아하세요?", translation: "What sports do you like?" },
        { speaker: "B", text: "저는 농구를 좋아해요. A 씨는요?", translation: "I like basketball. How about you?" },
        { speaker: "A", text: "저는 운동을 싫어해요.", translation: "I dislike sports." }
      ]
    }
  ]
};