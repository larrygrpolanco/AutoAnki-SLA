// src/lib/content/lessons/lesson6.ts

import type { Lesson } from '../../types';

export const lessonSix: Lesson = {
  id: 6,
  titleEn: "My Day",
  titleKr: "나의 하루",

	exercises: ['sentence-scramble'], 

  segments: [
    {
      id: "L6-C1",
      type: "conversation",
      title: "Conversation 1",
      subtitle: "Michael and Jenny discuss where they live and commute times.",
      content: [
        {
          speaker: "마이클",
          text: "제니 씨, 어디 살아요?",
          translation: "Where do you live, Jenny?",
          audio: { file: "/audio/Textbook_Lesson6_C1_3rd_Edition.mp3", start: 20, end: 23 }
        },
        {
          speaker: "제니",
          text: "한인타운에 살아요.",
          translation: "I live in Koreatown.",
          audio: { file: "/audio/Textbook_Lesson6_C1_3rd_Edition.mp3", start: 23, end: 26 }
        },
        {
          speaker: "마이클",
          text: "집에서 학교까지 얼마나 걸려요?",
          translation: "How long does it take from your home to get to school?",
          audio: { file: "/audio/Textbook_Lesson6_C1_3rd_Edition.mp3", start: 26, end: 31 }
        },
        {
          speaker: "제니",
          text: "좀 멀어요. 차로 한 시간쯤 걸려요. 마이클 씨는 어디 살아요?",
          translation: "It is a little bit far from school. It takes about an hour by car. Where do you live, Michael?",
          audio: { file: "/audio/Textbook_Lesson6_C1_3rd_Edition.mp3", start: 31, end: 41 }
        },
        {
          speaker: "마이클",
          text: "저는 학교 앞 아파트에 살아요. 아주 가까워요. 보통 걸어서 5분 걸려요.",
          translation: "I live in an apartment across campus. It is very close to school. It usually takes five minutes to walk.",
          audio: { file: "/audio/Textbook_Lesson6_C1_3rd_Edition.mp3", start: 41, end: 53 }
        }
      ],
      newVocabulary: [
        { id: "v6-1", korean: "날씨", english: "weather", pos: "noun" },
        { id: "v6-2", korean: "말(하다)", english: "speech, words", pos: "noun" },
        { id: "v6-3", korean: "버스", english: "bus", pos: "noun" },
        { id: "v6-4", korean: "볼펜", english: "ballpoint pen", pos: "noun" },
        { id: "v6-5", korean: "비행기", english: "airplane", pos: "noun" },
        { id: "v6-6", korean: "연필", english: "pencil", pos: "noun" },
        { id: "v6-7", korean: "자전거", english: "bicycle", pos: "noun" },
        { id: "v6-8", korean: "지하철", english: "subway", pos: "noun" },
        { id: "v6-9", korean: "차", english: "car", pos: "noun" },
        { id: "v6-10", korean: "트럭", english: "truck", pos: "noun" },
        { id: "v6-11", korean: "하루", english: "(one) day", pos: "noun" },
        { id: "v6-12", korean: "한인타운", english: "Koreatown", pos: "noun" },
        { id: "v6-13", korean: "까지", english: "up to (location/time)", pos: "particle" },
        { id: "v6-14", korean: "(으)로", english: "by means of", pos: "particle" },
        { id: "v6-15", korean: "에서", english: "from (location)", pos: "particle" },
        { id: "v6-16", korean: "가깝다", english: "to be close, near", pos: "adjective" },
        { id: "v6-17", korean: "덥다", english: "to be hot", pos: "adjective" },
        { id: "v6-18", korean: "멀다", english: "to be far", pos: "adjective" },
        { id: "v6-19", korean: "쉽다", english: "to be easy", pos: "adjective" },
        { id: "v6-20", korean: "어렵다", english: "to be difficult", pos: "adjective" },
        { id: "v6-21", korean: "좁다", english: "to be narrow", pos: "adjective" },
        { id: "v6-22", korean: "춥다", english: "to be cold", pos: "adjective" },
        { id: "v6-23", korean: "걸리다", english: "to take [time]", pos: "verb" },
        { id: "v6-24", korean: "살다", english: "to live", pos: "verb" },
        { id: "v6-25", korean: "보통", english: "usually", pos: "adverb" },
        { id: "v6-26", korean: "얼마나/얼마", english: "how long/how much", pos: "adverb" },
        { id: "v6-27", korean: "좀", english: "a little", pos: "adverb" },
        { id: "v6-28", korean: "쯤", english: "about, around", pos: "suffix" }
      ],
      newExpressions: [
        {
          id: "exp-6-1",
          title: "From A to B (에서... 까지)",
          content: "Indicates a range of distance or time.",
          tables: [
            {
              id: "tbl-from-to",
              type: "generic",
              headers: ["Korean", "English"],
              rows: [
                ["집에서 학교까지", "From home to school"],
                ["서울에서 보스턴까지", "From Seoul to Boston"]
              ]
            }
          ]
        },
        {
          id: "exp-6-2",
          title: "Approximation (~쯤)",
          content: "Attached to a noun expressing time or a counter to mean 'about' or 'around'.",
          tables: [
            {
              id: "tbl-approx",
              type: "generic",
              headers: ["Phrase", "Meaning"],
              rows: [
                ["한 시간쯤", "About one hour"],
                ["1시쯤", "Around 1 o'clock"]
              ]
            }
          ]
        },
        {
          id: "exp-6-3",
          title: "Means of Motion (~어서/아서)",
          content: "Attached to verbs like walk, run, or drive to express how one moves.",
          tables: [
            {
              id: "tbl-motion-means",
              type: "conjugation",
              headers: ["Verb", "Conjugated Mean"],
              rows: [
                ["걷다 (walk)", "걸어서 (by walking)"],
                ["뛰다 (run)", "뛰어서 (by running)"],
                ["운전하다 (drive)", "운전해서 (by driving)"]
              ]
            }
          ]
        }
      ]
    },
    {
      id: "L6-C2",
      type: "conversation",
      title: "Conversation 2",
      subtitle: "Michael and Yumi discuss what they did yesterday.",
      content: [
        {
          speaker: "마이클",
          text: "유미 씨, 어제 오후에 뭐 했어요?",
          translation: "Yumi, what did you do yesterday afternoon?",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 6, end: 11 }
        },
        {
          speaker: "유미",
          text: "학교 수영장에서 수영했어요. 마이클 씨는 뭐 했어요?",
          translation: "I swam in the school swimming pool. What did you do, Michael?",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 11, end: 20 }
        },
        {
          speaker: "마이클",
          text: "친구하고 같이 테니스 쳤어요.",
          translation: "I played tennis with a friend.",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 20, end: 24.5 }
        },
        {
          speaker: "유미",
          text: "아, 제니하고 쳤어요?",
          translation: "Oh, did you play with Jenny?",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 24.5, end: 28 }
        },
        {
          speaker: "마이클",
          text: "아니요, 제니는 테니스 안 좋아해요. 유미 씨는 테니스 좋아해요?",
          translation: "No, she doesn't like tennis. Yumi, do you like to play tennis?",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 28, end: 37.5 }
        },
        {
          speaker: "유미",
          text: "네, 그런데 잘 못 쳐요.",
          translation: "Yes, but I don't know how to play tennis very well.",
          audio: { file: "/audio/Textbook_Lesson6_C2_3rd_Edition.mp3", start: 37.5, end: 42 }
        }
      ],
      newVocabulary: [
        { id: "v6-29", korean: "대답(하다)", english: "answer", pos: "noun" },
        { id: "v6-30", korean: "때", english: "time (during)", pos: "noun" },
        { id: "v6-31", korean: "수영(하다)", english: "swimming", pos: "noun" },
        { id: "v6-32", korean: "수영장", english: "swimming pool", pos: "noun" },
        { id: "v6-33", korean: "어제", english: "yesterday", pos: "noun" },
        { id: "v6-34", korean: "음악", english: "music", pos: "noun" },
        { id: "v6-35", korean: "주말", english: "weekend", pos: "noun" },
        { id: "v6-36", korean: "중학교", english: "middle school", pos: "noun" },
        { id: "v6-37", korean: "축구(하다)", english: "soccer", pos: "noun" },
        { id: "v6-38", korean: "클래식", english: "classical music", pos: "noun" },
        { id: "v6-39", korean: "태권도", english: "Taekwondo", pos: "noun" },
        { id: "v6-40", korean: "테니스장", english: "tennis court", pos: "noun" },
        { id: "v6-41", korean: "파티", english: "party", pos: "noun" },
        { id: "v6-42", korean: "지난", english: "last, past", pos: "adjective" }, // Treated as pre-noun/modifier
        { id: "v6-43", korean: "바쁘다", english: "to be busy", pos: "adjective" },
        { id: "v6-44", korean: "모르다", english: "to not know", pos: "verb" },
        { id: "v6-45", korean: "일어나다", english: "to get up", pos: "verb" },
        { id: "v6-46", korean: "너무", english: "too much", pos: "adverb" },
        { id: "v6-47", korean: "못", english: "cannot", pos: "adverb" },
        { id: "v6-48", korean: "안", english: "do not", pos: "adverb" },
        { id: "v6-49", korean: "왜", english: "why", pos: "adverb" },
        { id: "v6-50", korean: "자주", english: "often", pos: "adverb" }
      ],
      newExpressions: [
        {
          id: "exp-6-4",
          title: "Skill Ability (잘 / 못)",
          content: "Used to describe if you are good or bad at an action.",
          tables: [
            {
              id: "tbl-skill",
              type: "comparison",
              headers: ["Expression", "Meaning"],
              rows: [
                ["잘 해요", "Good at / Skillful"],
                ["못 해요", "Bad at / Unskillful"],
                ["잘 못 해요", "Not that good at"]
              ]
            }
          ]
        },
        {
          id: "exp-6-5",
          title: "Expressions of Frequency",
          content: "Common prefixes for daily/weekly/monthly occurrences.",
          tables: [
            {
              id: "tbl-frequency",
              type: "generic",
              headers: ["Korean", "English"],
              rows: [
                ["매일 / 날마다", "Every day"],
                ["매주", "Every week"],
                ["매달", "Every month"],
                ["매년", "Every year"]
              ]
            }
          ]
        }
      ]
    },
    {
      id: "L6-N1",
      type: "narration",
      title: "Michael's Day",
      subtitle: "A description of Michael's daily routine.",
      content: [
        {
          speaker: "Narrator",
          text: "저는 보통 7시에 일어나요. 그런데 오늘은 8시 30분에 일어났어요.",
          translation: "I usually get up at seven o'clock, but today I got up at eight thirty.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 5, end: 15.5 }
        },
        {
          speaker: "Narrator",
          text: "그래서 아침을 못 먹었어요.",
          translation: "So I didn't have breakfast.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start:16, end: 20 }
        },
        {
          speaker: "Narrator",
          text: "수업은 9시에 있었어요. 기숙사에서 학교까지는 가까워요. 그래서 보통 걸어서 가요.",
          translation: "I have class at nine o'clock. My dorm is close to campus. I usually walk to school.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 20, end: 34 }
        },
        {
          speaker: "Narrator",
          text: "오후에는 수업이 없었어요. 그래서, 리사하고 테니스를 쳤어요.",
          translation: "Since I didn't have any class in the afternoon, I played tennis with Lisa.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 34, end: 43 }
        },
        {
          speaker: "Narrator",
          text: "리사는 제 여자 친구예요. 리사도 한국어 수업을 들어요.",
          translation: "Lisa is my girlfriend. She also takes the Korean class.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 43, end: 52 }
        },
        {
          speaker: "Narrator",
          text: "6시쯤 리사하고 같이 저녁을 먹으러 기숙사 식당에 갔어요.",
          translation: "Around six o'clock, Lisa and I went to the dormitory cafeteria to have dinner.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 52, end: 61 }
        },
        {
          speaker: "Narrator",
          text: "그리고 저녁에는 도서관에서 숙제를 했어요. 숙제가 어려웠어요.",
          translation: "In the evening, I did my homework at the library alone. The homework was difficult.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 61, end: 71 }
        },
        {
          speaker: "Narrator",
          text: "오늘 하루는 아주 바빴어요.",
          translation: "Today was a very busy day.",
          audio: { file: "/audio/Textbook_Lesson6_N_3rd_Edition.mp3", start: 71, end: 76 }
        }
      ],
      newVocabulary: [],
      newExpressions: []
    }
  ],

  grammar: [
    {
      id: "G6.1",
      title: "Particle N(으)로",
      pattern: "N + (으)로",
      description: "Indicates the means of transportation or the instrument/tool used.",
      examples: [
        { kor: "학교에 버스로 가요.", eng: "I go to school by bus." },
        { kor: "볼펜으로 쓰세요.", eng: "Please write with a ballpoint pen." }
      ],
      tables: [
        {
          id: "tbl-particle-inst",
          type: "conjugation",
          headers: ["Noun Ending", "Particle", "Example"],
          rows: [
            ["Vowel or 'ㄹ'", "로", "차로, 지하철로"],
            ["Consonant (except 'ㄹ')", "으로", "트럭으로, 볼펜으로"]
          ]
        }
      ]
    },
    {
      id: "G6.2",
      title: "Irregular predicates in /ㅂ/",
      pattern: "Stem ending in ㅂ + Vowel -> ㅂ becomes 우",
      description: "When a stem ends in ㅂ and is followed by a vowel suffix (like ~어요), the ㅂ changes to 우. Note that 좁다 (to be narrow) is regular.",
      examples: [
        { kor: "날씨가 추워요.", eng: "The weather is cold." },
        { kor: "시험이 어려워요.", eng: "The test is difficult." }
      ],
      tables: [
        {
          id: "tbl-irregular-b",
          type: "conjugation",
          headers: ["Base Form", "Stem Change", "Polite Form (~어요)"],
          rows: [
            ["가깝다 (close)", "가까우", "가까워요"],
            ["덥다 (hot)", "더우", "더워요"],
            ["춥다 (cold)", "추우", "추워요"],
            ["어렵다 (difficult)", "어려우", "어려워요"],
            ["쉽다 (easy)", "쉬우", "쉬워요"],
            ["*좁다 (narrow, regular)", "좁", "좁아요"]
          ]
        }
      ]
    },
    {
      id: "G6.3",
      title: "Past events : ~었/았/ㅆ어요",
      pattern: "Vst + 었/았/ㅆ어요",
      description: "Indicates that an event has already taken place. Follows vowel harmony rules similar to the polite ending.",
      examples: [
        { kor: "집에 갔어요.", eng: "I went home." },
        { kor: "점심 먹었어요.", eng: "I ate lunch." },
        { kor: "바빴어요.", eng: "I was busy." }
      ],
      tables: [
        {
          id: "tbl-past-tense",
          type: "conjugation",
          headers: ["Vowel Type", "Ending", "Example"],
          rows: [
            ["Bright (아, 오)", "~았어요", "가다 -> 갔어요, 좋다 -> 좋았어요"],
            ["Dark (other)", "~었어요", "먹다 -> 먹었어요"],
            ["Ha-da verbs", "~했어요", "공부하다 -> 공부했어요"],
            ["Irregular ㅂ", "~웠어요", "춥다 -> 추웠어요"]
          ]
        }
      ]
    },
    {
      id: "G6.4",
      title: "Negative adverb 안 vs. 못",
      pattern: "안/못 + Verb",
      description: "안 expresses a general negation or lack of volition (don't). 못 expresses inability due to external circumstances (can't).",
      examples: [
        { kor: "학교에 안 가요.", eng: "I don't go to school (by choice)." },
        { kor: "학교에 못 가요.", eng: "I can't go to school (e.g., sick)." }
      ],
      tables: [
        {
          id: "tbl-negation-comp",
          type: "comparison",
          headers: ["Type", "Meaning", "Nuance"],
          rows: [
            ["안 + V", "Do not", "Subject's will/volition"],
            ["못 + V", "Cannot", "External circumstance/Inability"]
          ]
        }
      ]
    }
  ],

  culture: [
    {
      title: "The Calendar (양력 vs 음력)",
      content: "Korea uses both solar (양력) and lunar (음력) calendars. Major holidays like Seollal (Lunar New Year) and Chuseok (Thanksgiving) follow the lunar calendar."
    },
    {
      title: "Writing Dates",
      content: "Dates are written in descending order: Year -> Month -> Day. Example: 2022년 10월 28일."
    }
  ],

  usage: [
    {
      id: "U6-A",
      title: "Commute Time",
      description: "Ask how long it takes to get somewhere using '얼마나 걸려요?'.",
      exampleDialogue: [
        { speaker: "A", text: "집에서 학교까지 얼마나 걸려요?", translation: "How long does it take from home to school?" },
        { speaker: "B", text: "버스로 1시간 걸려요.", translation: "It takes 1 hour by bus." }
      ]
    },
    {
      id: "U6-B",
      title: "Habitual vs Past",
      description: "Contrast what you usually do vs what you did yesterday.",
      exampleDialogue: [
        { speaker: "A", text: "보통 월요일에 뭐 해요?", translation: "What do you usually do on Mondays?" },
        { speaker: "B", text: "수영해요.", translation: "I swim." },
        { speaker: "A", text: "지난 월요일에 뭐 했어요?", translation: "What did you do last Monday?" },
        { speaker: "B", text: "수영 못 했어요. 바빴어요.", translation: "I couldn't swim. I was busy." }
      ]
    },
    {
      id: "U6-C",
      title: "Daily Schedule",
      description: "Describe your timetable including class times and meals.",
      exampleDialogue: [
        { speaker: "Student", text: "9시에 한국어 수업이 있어요.", translation: "I have Korean class at 9." },
        { speaker: "Student", text: "12시에 점심을 먹어요.", translation: "I eat lunch at 12." }
      ]
    },
    {
      id: "U6-D",
      title: "Asking Reasons (Why?)",
      description: "Use '왜' to ask for reasons and answer based on context.",
      exampleDialogue: [
        { speaker: "A", text: "왜 파티에 안 갔어요?", translation: "Why didn't you go to the party?" },
        { speaker: "B", text: "바빴어요. 숙제가 많았어요.", translation: "I was busy. I had a lot of homework." }
      ]
    }
  ]
};