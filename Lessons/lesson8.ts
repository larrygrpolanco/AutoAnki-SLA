import type { Lesson } from '../../types';

export const lessonEight: Lesson = {
  id: 8,
  titleEn: "In Seoul",
  titleKr: "서울에서",

  exercises: ['sentence-scramble'],

  segments: [
    {
      id: "L8-C1",
      type: "conversation",
      title: "Conversation 1",
      subtitle: "Steve and Mark discuss the weather and plans to visit Gyeongbok Palace.",
      content: [
        {
          speaker: "스티브",
          text: "마크 씨, 서울 날씨가 참 좋지요?",
          translation: "Mark, Seoul’s weather is quite nice, isn’t it?",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 39, end: 45 }
        },
        {
          speaker: "마크",
          text: "네, 아주 따뜻해요. 저는 서울의 봄 날씨를 아주 좋아해요.",
          translation: "Yes, it’s really warm. I really like the spring weather in Seoul.",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 45, end: 56 }
        },
        {
          speaker: "스티브",
          text: "저도 그래요. 그런데 마크 씨, 이번 일요일에 시간 있어요?",
          translation: "Me too. By the way Mark, are you free this Sunday?",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 56, end: 67 }
        },
        {
          speaker: "마크",
          text: "네, 괜찮아요. 왜요?",
          translation: "Yes, (Sunday’s) okay for me. Why?",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 67, end:72 }
        },
        {
          speaker: "스티브",
          text: "저하고 같이 경복궁에 가요.",
          translation: "(You should) go with me to Gyeongbok Palace!",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 72, end: 77.5 }
        },
        {
          speaker: "마크",
          text: "좋아요. 몇 시에 만나요?",
          translation: "Great! What time do we meet?",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 77.5, end: 82 }
        },
        {
          speaker: "스티브",
          text: "3시에 광화문 앞에서 만나요.",
          translation: "Let’s meet at 3 o’clock in front of Gwanghwamun.",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 82, end: 87 }
        },
        {
          speaker: "마크",
          text: "참, 여기서 광화문까지 어떻게 가요?",
          translation: "By the way, how do I get to Gwanghwamun from here?",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 87, end: 94 }
        },
        {
          speaker: "스티브",
          text: "162번 버스를 타고 서점 앞에서 내리세요. 광화문은 서점 건너편에 있어요.",
          translation: "Take Bus 162 and get off in front of the bookstore. Gwanghwamun is across from the bookstore.",
          audio: { file: "/audio/Textbook_Lesson8_C1_3rd_Edition.mp3", start: 94, end: 106 }
        }
      ],
      newVocabulary: [
        { id: "v8-1", korean: "가운데", english: "the middle, the center", pos: "noun" },
        { id: "v8-2", korean: "건너편", english: "the other side", pos: "noun" },
        { id: "v8-3", korean: "경복궁", english: "Gyeongbok Palace", pos: "noun" },
        { id: "v8-4", korean: "광화문", english: "Gwanghwamun", pos: "noun" },
        { id: "v8-5", korean: "교회", english: "church", pos: "noun" },
        { id: "v8-6", korean: "꽃집", english: "flower shop", pos: "noun" },
        { id: "v8-7", korean: "동네", english: "neighborhood", pos: "noun" },
        { id: "v8-8", korean: "서울", english: "Seoul", pos: "noun" },
        { id: "v8-9", korean: "슈퍼", english: "supermarket", pos: "noun" },
        { id: "v8-10", korean: "약국", english: "pharmacy, drugstore", pos: "noun" },
        { id: "v8-11", korean: "지도", english: "map", pos: "noun" },
        { id: "v8-12", korean: "쪽", english: "side, direction", pos: "noun" },
        { id: "v8-13", korean: "초등학교", english: "elementary school", pos: "noun" },
        { id: "v8-14", korean: "군데", english: "place, spot (counter)", pos: "counter" },
        { id: "v8-15", korean: "번", english: "number (counter)", pos: "counter" },
        { id: "v8-16", korean: "~지요?", english: "isn’t it? (seeking agreement)", pos: "suffix" },
        { id: "v8-17", korean: "여기", english: "here", pos: "noun", tags: ['demonstrative'] },
        { id: "v8-18", korean: "거기", english: "there", pos: "noun", tags: ['demonstrative'] },
        { id: "v8-19", korean: "저기", english: "over there", pos: "noun", tags: ['demonstrative'] },
        { id: "v8-20", korean: "내리다", english: "to get off", pos: "verb" },
        { id: "v8-21", korean: "타다", english: "to get in/on, ride", pos: "verb" },
        { id: "v8-22", korean: "깨끗하다", english: "to be clean", pos: "adjective" },
        { id: "v8-23", korean: "따뜻하다", english: "to be warm", pos: "adjective" },
        { id: "v8-24", korean: "조용하다", english: "to be quiet", pos: "adjective" },
        { id: "v8-25", korean: "여러", english: "many, several", pos: "adjective", tags: ['pre-noun'] },
        { id: "v8-26", korean: "이", english: "this", pos: "adjective", tags: ['pre-noun', 'demonstrative'] },
        { id: "v8-27", korean: "그", english: "that", pos: "adjective", tags: ['pre-noun', 'demonstrative'] },
        { id: "v8-28", korean: "저", english: "that (over there)", pos: "adjective", tags: ['pre-noun', 'demonstrative'] }
      ],
      newExpressions: [
        {
          id: "exp-8-1",
          title: "Contraction: 여기서",
          content: "여기서 is a contracted form of 여기에서 (여기 ‘here’ + 에서 ‘at’). The particle 에서 is often contracted to 서."
        },
        {
          id: "exp-8-2",
          title: "Counter: 번",
          content: "번 in 162번 버스 is a counter for serial numbers."
        },
        {
          id: "exp-8-3",
          title: "Landmarks: Gwanghwamun & Gyeongbok Palace",
          content: "Gwanghwamun is the main gate of Gyeongbok Palace. Gyeongbok Palace was the main royal palace of the Joseon dynasty, built in 1395."
        }
      ]
    },
    {
      id: "L8-C2",
      type: "conversation",
      title: "Conversation 2",
      subtitle: "Mark asks a stranger for directions.",
      content: [
        {
          speaker: "마크",
          text: "저기요. 말씀 좀 묻겠습니다. 이 근처에 우체국이 어디 있습니까?",
          translation: "Excuse me. I’d like to ask you something. Is there a post office near here?",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 6, end: 16 }
        },
        {
          speaker: "여자",
          text: "저기 은행 보이지요?",
          translation: "Do you see the bank over there?",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 16, end: 20.5 }
        },
        {
          speaker: "마크",
          text: "네.",
          translation: "Yes.",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 20.5, end: 22 }
        },
        {
          speaker: "여자",
          text: "거기서 오른쪽으로 도세요. 그리고 쭉 가세요. 그럼 백화점이 보일 거예요. 우체국은 건너편에 있어요.",
          translation: "From there, turn to the right and go straight, then you’ll see a department store. The post office is across from that.",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start:22, end: 40 }
        },
        {
          speaker: "마크",
          text: "네, 감사합니다. 그런데, 덕수궁은 여기서 어떻게 갑니까?",
          translation: "I see, thank you. By the way, how do I get to Deoksu Palace from here?",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 40, end: 50 }
        },
        {
          speaker: "여자",
          text: "지하철 1호선을 타고 시청역에서 내리세요.",
          translation: "Take subway Line #1 and get off at City Hall Station.",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 50, end: 57 }
        },
        {
          speaker: "마크",
          text: "네, 고맙습니다.",
          translation: "I see, thank you.",
          audio: { file: "/audio/Textbook_Lesson8_C2_3rd_Edition.mp3", start: 57, end: 60 } 
        }
      ],
      newVocabulary: [
        { id: "v8-29", korean: "근처", english: "nearby, vicinity", pos: "noun" },
        { id: "v8-30", korean: "덕수궁", english: "Deoksu Palace", pos: "noun" },
        { id: "v8-31", korean: "말씀", english: "speech, words", pos: "noun", tags: ['honorific'] },
        { id: "v8-32", korean: "시청", english: "city hall", pos: "noun" },
        { id: "v8-33", korean: "역", english: "station", pos: "noun" },
        { id: "v8-34", korean: "오른쪽", english: "right side", pos: "noun" },
        { id: "v8-35", korean: "왼쪽", english: "left side", pos: "noun" },
        { id: "v8-36", korean: "우표", english: "postage stamp", pos: "noun" },
        { id: "v8-37", korean: "은행", english: "bank", pos: "noun" },
        { id: "v8-38", korean: "의사", english: "medical doctor", pos: "noun" },
        { id: "v8-39", korean: "처음", english: "the first time", pos: "noun" },
        { id: "v8-40", korean: "좀", english: "a little (contraction of 조금)", pos: "adverb" },
        { id: "v8-41", korean: "쭉", english: "straight", pos: "adverb" },
        { id: "v8-42", korean: "호선", english: "subway line", pos: "counter" },
        { id: "v8-43", korean: "돌다", english: "to turn", pos: "verb" },
        { id: "v8-44", korean: "팔다", english: "to sell", pos: "verb" },
        { id: "v8-45", korean: "묻다", english: "to ask", pos: "verb" },
        { id: "v8-46", korean: "보이다", english: "to be seen, visible", pos: "verb" },
        { id: "v8-47", korean: "뵙다", english: "to see", pos: "verb", tags: ['humble'] },
        { id: "v8-48", korean: "감사하다", english: "to be thankful", pos: "adjective" },
        { id: "v8-49", korean: "미안하다", english: "to be sorry", pos: "adjective" },
        { id: "v8-50", korean: "(으)로", english: "toward, to", pos: "particle" },
        { id: "v8-51", korean: "~(스)ㅂ니다", english: "deferential statement ending", pos: "suffix" },
        { id: "v8-52", korean: "~습니까/ㅂ니까?", english: "deferential question ending", pos: "suffix" }
      ],
      newExpressions: [
        {
          id: "exp-8-4",
          title: "저기요 (Excuse me)",
          content: "Lit. 'there'. Frequently used as a polite expression to gather someone’s attention."
        },
        {
          id: "exp-8-5",
          title: "말씀 좀 묻겠습니다 (May I ask a question?)",
          content: "Used as a conversation opener for asking directions. 좀 (lit. a little) conveys politeness."
        },
        {
          id: "exp-8-6",
          title: "Directions",
          content: "Common directional terms.",
          tables: [
            {
              id: "tbl-directions",
              type: "generic",
              headers: ["Korean", "English"],
              rows: [
                ["이쪽", "This side"],
                ["그쪽", "That side"],
                ["저쪽", "That side (over there)"],
                ["오른쪽", "Right side"],
                ["왼쪽", "Left side"]
              ]
            }
          ]
        }
      ]
    },
    {
      id: "L8-N1",
      type: "narration",
      title: "Our Neighborhood",
      content: [
        {
          speaker: "Steve",
          text: "안녕하세요? 제 이름은 스티브 윌슨입니다. 저는 미국 보스턴에서 왔습니다.",
          translation: "Hello. My name is Steve Wilson. I am from Boston, USA.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 4.5, end: 16 }
        },
        {
          speaker: "Steve",
          text: "지금은 서울에서 한국어를 배웁니다. 저는 학교 근처 아파트에서 삽니다.",
          translation: "Currently I am learning Korean in Seoul. I live in an apartment near school.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 16, end: 28 }
        },
        {
          speaker: "Steve",
          text: "아파트가 조용하고 깨끗합니다. 이게 우리 동네 지도입니다.",
          translation: "The apartment is quiet and clean. This is a map of my neighborhood.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 28, end: 39 }
        },
        {
          speaker: "Steve",
          text: "동네 가운데 초등학교가 있습니다. 학교 뒤에는 교회가 있습니다.",
          translation: "In the center of the neighborhood, there is an elementary school. Behind the school, there is a church.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 39, end: 51 }
        },
        {
          speaker: "Steve",
          text: "교회 옆에는 백화점이 있습니다. 백화점 왼쪽에는 꽃집이 있습니다.",
          translation: "In front of the church, there is a department store. To the left of the department store, there is a flower shop.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 51, end: 63 }
        },
        {
          speaker: "Steve",
          text: "꽃집 옆에는 서점이 있고 서점 옆에는 식당이 있습니다.",
          translation: "Next to the flower shop, there is a bookstore and next to the bookstore, there is a restaurant.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 63, end: 74 }
        },
        {
          speaker: "Steve",
          text: "극장은 약국 건너편에 있고 우체국은 슈퍼 옆에 있습니다. 그리고 커피숍이 여러 군데 있습니다.",
          translation: "The theater is across from the pharmacy and the post office is next to the supermarket. There are also several coffee shops.",
          audio: { file: "/audio/Textbook_Lesson8_N_3rd_Edition.mp3", start: 74, end: 90 }  
        }
      ],
      newVocabulary: [],
      newExpressions: []
    }
  ],

  grammar: [
    {
      id: "G8.1",
      title: "Seeking agreement: ~지요?",
      pattern: "Stem + 지요?",
      description: "A request for confirmation or agreement about what the speaker believes to be true. Equivalent to 'isn't it?' or 'right?'.",
      examples: [
        { kor: "오늘 날씨 참 좋지요?", eng: "The weather is very nice today, isn’t it?" },
        { kor: "김 선생님, 내일 시험 없지요?", eng: "Professor Kim, we don’t have an exam tomorrow, do we?" },
        { kor: "학교 기숙사가 조용하지요?", eng: "The dorm is quiet, isn’t it?" }
      ]
    },
    {
      id: "G8.2",
      title: "Demonstrative expressions: 이/그/저",
      pattern: "이/그/저 + Noun",
      description: "Indicates physical or mental proximity. '이' (near speaker), '그' (near listener), '저' (away from both).",
      examples: [
        { kor: "이 지도 어느 서점에서 샀어요?", eng: "At which bookstore did you buy this map?" },
        { kor: "저기 약국 뒤에도 있어요.", eng: "It’s behind the drugstore over there." }
      ],
      tables: [
        {
          id: "tbl-demonstratives",
          type: "comparison",
          headers: ["Context", "Near Speaker", "Near Listener", "Far from Both"],
          rows: [
            ["Determiner", "이 (This)", "그 (That)", "저 (That over there)"],
            ["Place", "여기 (Here)", "거기 (There)", "저기 (Over there)"],
            ["Direction", "이쪽 (This side)", "그쪽 (That side)", "저쪽 (That side)"]
          ]
        },
        {
          id: "tbl-demonstratives-contraction",
          type: "generic",
          headers: ["Original", "Contraction (Generic)", "Topic", "Subject", "Object"],
          rows: [
            ["이것 (This thing)", "이거", "이건", "이게", "이걸"],
            ["그것 (That thing)", "그거", "그건", "그게", "그걸"],
            ["저것 (That thing)", "저거", "저건", "저게", "저걸"]
          ]
        }
      ]
    },
    {
      id: "G8.3",
      title: "Deferential style ~(스)ㅂ니다 / ~(스)ㅂ니까?",
      pattern: "Vst + ㅂ니다/습니다",
      description: "Used in formal settings like broadcasting, conferences, or first-time introductions.",
      examples: [
        { kor: "처음 뵙겠습니다. 제 이름은 스티브 윌슨입니다.", eng: "Nice meeting you. My name is Steve Wilson." },
        { kor: "언제 한국에 갑니까?", eng: "When are you going to Korea?" }
      ],
      tables: [
        {
          id: "tbl-def-conj",
          type: "conjugation",
          headers: ["Stem Ending", "Statement", "Question"],
          rows: [
            ["Vowel", "~ㅂ니다", "~ㅂ니까?"],
            ["Consonant", "~습니다", "~습니까?"]
          ]
        },
        {
          id: "tbl-style-comp",
          type: "comparison",
          headers: ["Dictionary", "Polite", "Deferential Statement", "Deferential Question"],
          rows: [
            ["먹다", "먹어요", "먹습니다", "먹습니까?"],
            ["가다", "가요", "갑니다", "갑니까?"],
            ["이다", "이에요/예요", "입니다", "입니까?"],
            ["하다", "해요", "합니다", "합니까?"]
          ]
        }
      ]
    },
    {
      id: "G8.4",
      title: "Directional Particle N(으)로",
      pattern: "N + (으)로",
      description: "Indicates general direction 'toward'. (으)로 is used after consonants (except ㄹ), 로 is used after vowels or ㄹ.",
      examples: [
        { kor: "오른쪽으로 도세요.", eng: "Turn right (toward the right)." },
        { kor: "시청역 뒤로 오세요.", eng: "Come to the back of City Hall station." }
      ]
    },
    {
      id: "G8.5",
      title: "Irregular predicates in /ㄹ/",
      pattern: "Stem ending in ㄹ + ㄴ/ㅂ/ㅅ",
      description: "When a stem ending in ㄹ is followed by ㄴ, ㅂ, or ㅅ, the ㄹ is omitted. For ~(으)세요, the 으 is also deleted.",
      examples: [
        { kor: "어디 사세요? (살 + 으세요)", eng: "Where do you live?" },
        { kor: "저는 서울에서 삽니다. (살 + 습니다)", eng: "I live in Seoul." }
      ],
      tables: [
        {
          id: "tbl-irr-l",
          type: "conjugation",
          headers: ["Dictionary", "Deferential (~ㅂ니다)", "Honorific (~세요)", "Polite (~아요)"],
          rows: [
            ["돌다 (turn)", "돕니다", "도세요", "돌아요"],
            ["살다 (live)", "삽니다", "사세요", "살아요"],
            ["만들다 (make)", "만듭니다", "만드세요", "만들어요"]
          ]
        }
      ]
    }
  ],

  culture: [
    {
      title: "Seoul",
      content: "Seoul is the capital of Korea, home to 10 million people. It is a mix of the past (palaces like Gyeongbokgung) and the present (skyscrapers). It is situated on both sides of the Han River."
    },
    {
      title: "Public Transportation",
      content: "Seoul has an efficient network of Subways (9 central lines), Buses (coded by color: Blue/City, Red/Express, Green/Local), and Taxis (Standard, and Black 'Luxury' Taxis)."
    }
  ],

  usage: [
    {
      id: "U8-A",
      title: "Inquiring about background",
      description: "Ask where someone is from using '어디서 오셨어요?' or '고향이 어디예요?'.",
      exampleDialogue: [
        { speaker: "스티브", text: "마크 씨는 어디서 오셨어요?", translation: "Mark, where are you from?" },
        { speaker: "마크", text: "저는 호주 시드니에서 왔어요.", translation: "I came from Sydney, Australia." }
      ]
    },
    {
      id: "U8-B",
      title: "Asking and Giving Directions",
      description: "Start with '실례합니다' and use '어떻게 가요?'. give directions using '(으)로'.",
      exampleDialogue: [
        { speaker: "A", text: "실례합니다. 여기서 극장까지 어떻게 가요?", translation: "Excuse me. How do I go to the theater from here?" },
        { speaker: "B", text: "쭉 가세요. 그럼 오른쪽에 있어요.", translation: "Go straight. Then it is on your right side." }
      ]
    }
  ]
};