(function () {
  "use strict";

  // ─── 상수 ───────────────────────────────────────────────
  const STORAGE_KEY_STATE = "awsQuizState";
  const STORAGE_KEY_SCRAPBOOK = "awsQuizScrapbook";
  const SCORE_THRESHOLDS = { PERFECT: 100, GOOD: 60 };
  const ICONS = { CORRECT: "✓", WRONG: "✗" };

  // ─── 퀴즈 데이터 ───────────────────────────────────────────
  const QUIZ_DATA = [
    {
      question: "Amazon S3는 어떤 유형의 스토리지 서비스인가요?",
      options: [
        "블록 스토리지",
        "객체(Object) 스토리지",
        "파일 스토리지",
        "인메모리 스토리지",
      ],
      answer: 1,
      explanation:
        "Amazon S3(Simple Storage Service)는 객체 스토리지 서비스입니다. 파일을 객체로 저장하며, 각 객체는 데이터, 메타데이터, 고유 키로 구성됩니다. 블록 스토리지는 EBS, 파일 스토리지는 EFS가 담당합니다.",
    },
    {
      question: "AWS에서 가상 서버를 제공하는 서비스는 무엇인가요?",
      options: [
        "AWS Lambda",
        "Amazon RDS",
        "Amazon EC2",
        "Amazon DynamoDB",
      ],
      answer: 2,
      explanation:
        "Amazon EC2(Elastic Compute Cloud)는 클라우드에서 가상 서버(인스턴스)를 제공하는 서비스입니다. Lambda는 서버리스 컴퓨팅, RDS는 관계형 데이터베이스, DynamoDB는 NoSQL 데이터베이스 서비스입니다.",
    },
    {
      question: "AWS에서 사용자 및 권한을 관리하는 서비스는 무엇인가요?",
      options: [
        "Amazon CloudWatch",
        "AWS IAM",
        "Amazon VPC",
        "AWS CloudTrail",
      ],
      answer: 1,
      explanation:
        "AWS IAM(Identity and Access Management)은 사용자, 그룹, 역할을 생성하고 AWS 리소스에 대한 접근 권한을 관리하는 서비스입니다. CloudWatch는 모니터링, VPC는 네트워크, CloudTrail은 API 호출 로깅 서비스입니다.",
    },
    {
      question: "AWS 리전(Region)에 대한 설명으로 올바른 것은?",
      options: [
        "전 세계에 단 하나만 존재한다",
        "하나의 리전에는 하나의 가용 영역만 있다",
        "리전은 지리적으로 분리된 독립적인 영역이며, 여러 가용 영역(AZ)으로 구성된다",
        "리전 간 데이터는 자동으로 복제된다",
      ],
      answer: 2,
      explanation:
        "AWS 리전은 전 세계 여러 지역에 분포한 독립적인 지리적 영역입니다. 각 리전은 2개 이상의 가용 영역(Availability Zone)으로 구성되어 고가용성을 제공합니다. 리전 간 데이터 복제는 자동이 아니라 사용자가 설정해야 합니다.",
    },
    {
      question: "서버를 관리하지 않고 코드를 실행할 수 있는 AWS 서비스는?",
      options: [
        "Amazon EC2",
        "Amazon ECS",
        "AWS Lambda",
        "AWS Elastic Beanstalk",
      ],
      answer: 2,
      explanation:
        "AWS Lambda는 서버리스 컴퓨팅 서비스로, 서버 프로비저닝이나 관리 없이 코드를 실행할 수 있습니다. 이벤트에 의해 트리거되며, 실행한 시간만큼만 비용이 부과됩니다. EC2는 가상 서버, ECS는 컨테이너 서비스, Elastic Beanstalk는 PaaS 형태의 배포 서비스입니다.",
    },
  ];

  // ─── 상태 ───────────────────────────────────────────────
  var state = {
    activeIndices: [],
    currentIndex: 0,
    score: 0,
    answers: {},
    retryMode: false,
  };

  var scrapbook = [];

  // ─── DOM 참조 ──────────────────────────────────────────
  var dom = {};

  function cacheDom() {
    dom.tabQuiz = document.getElementById("tabQuiz");
    dom.tabScrapbook = document.getElementById("tabScrapbook");
    dom.quizTab = document.getElementById("quizTab");
    dom.scrapbookTab = document.getElementById("scrapbookTab");
    dom.progressFill = document.getElementById("progressFill");
    dom.progressBar = dom.progressFill.parentElement;
    dom.scoreDisplay = document.getElementById("scoreDisplay");
    dom.scoreText = document.getElementById("scoreText");
    dom.totalText = document.getElementById("totalText");
    dom.questionArea = document.getElementById("questionArea");
    dom.questionNumber = document.getElementById("questionNumber");
    dom.questionText = document.getElementById("questionText");
    dom.optionsContainer = document.getElementById("optionsContainer");
    dom.explanation = document.getElementById("explanation");
    dom.nextBtn = document.getElementById("nextBtn");
    dom.quizSection = document.getElementById("quizSection");
    dom.resultSection = document.getElementById("resultSection");
    dom.resultEmoji = document.getElementById("resultEmoji");
    dom.resultScore = document.getElementById("resultScore");
    dom.resultMessage = document.getElementById("resultMessage");
    dom.resetBtn = document.getElementById("resetBtn");
    dom.retryWrongBtn = document.getElementById("retryWrongBtn");
    dom.retryBadge = document.getElementById("retryBadge");
    dom.scrapBadge = document.getElementById("scrapBadge");
    dom.scrapbookContent = document.getElementById("scrapbookContent");
    dom.scrapbookActions = document.getElementById("scrapbookActions");
    dom.clearScrapBtn = document.getElementById("clearScrapBtn");
  }

  // ─── localStorage 유틸 ─────────────────────────────────
  function storageGet(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      console.warn("localStorage 읽기 실패:", e);
      return null;
    }
  }

  function storageSet(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn("localStorage 쓰기 실패:", e);
    }
  }

  function storageRemove(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {
      console.warn("localStorage 삭제 실패:", e);
    }
  }

  // ─── 상태 관리 ─────────────────────────────────────────
  function loadState() {
    var saved = storageGet(STORAGE_KEY_STATE);
    if (saved) {
      state.activeIndices = saved.activeIndices || defaultIndices();
      state.currentIndex = saved.currentIndex || 0;
      state.score = saved.score || 0;
      state.answers = saved.answers || {};
      state.retryMode = saved.retryMode || false;
    } else {
      resetState();
    }
  }

  function resetState() {
    state.activeIndices = defaultIndices();
    state.currentIndex = 0;
    state.score = 0;
    state.answers = {};
    state.retryMode = false;
  }

  function defaultIndices() {
    var indices = [];
    for (var i = 0; i < QUIZ_DATA.length; i++) {
      indices.push(i);
    }
    return indices;
  }

  function saveState() {
    storageSet(STORAGE_KEY_STATE, state);
  }

  function loadScrapbook() {
    var saved = storageGet(STORAGE_KEY_SCRAPBOOK);
    scrapbook = Array.isArray(saved) ? saved : [];
  }

  function saveScrapbook() {
    storageSet(STORAGE_KEY_SCRAPBOOK, scrapbook);
    updateBadge();
  }

  // ─── 오답 노트 ─────────────────────────────────────────
  function addToScrapbook(questionIndex, selectedAnswer) {
    var existing = null;
    for (var i = 0; i < scrapbook.length; i++) {
      if (scrapbook[i].questionIndex === questionIndex) {
        existing = scrapbook[i];
        break;
      }
    }

    if (existing) {
      existing.selectedAnswer = selectedAnswer;
      existing.timestamp = new Date().toLocaleString("ko-KR");
    } else {
      scrapbook.push({
        questionIndex: questionIndex,
        selectedAnswer: selectedAnswer,
        timestamp: new Date().toLocaleString("ko-KR"),
      });
    }
    saveScrapbook();
  }

  function removeFromScrapbook(questionIndex) {
    scrapbook = scrapbook.filter(function (s) {
      return s.questionIndex !== questionIndex;
    });
    saveScrapbook();
  }

  function clearScrapbook() {
    if (confirm("오답 노트를 전체 삭제하시겠습니까?")) {
      scrapbook = [];
      saveScrapbook();
      renderScrapbook();
    }
  }

  function updateBadge() {
    if (scrapbook.length > 0) {
      dom.scrapBadge.textContent = scrapbook.length;
      dom.scrapBadge.classList.remove("hidden");
    } else {
      dom.scrapBadge.classList.add("hidden");
    }
  }

  // ─── 탭 네비게이션 ─────────────────────────────────────
  function switchTab(tab) {
    if (tab === "quiz") {
      dom.quizTab.classList.remove("hidden");
      dom.scrapbookTab.classList.add("hidden");
      dom.tabQuiz.classList.add("active");
      dom.tabScrapbook.classList.remove("active");
    } else {
      dom.quizTab.classList.add("hidden");
      dom.scrapbookTab.classList.remove("hidden");
      dom.tabQuiz.classList.remove("active");
      dom.tabScrapbook.classList.add("active");
      renderScrapbook();
    }
  }

  // ─── 퀴즈 렌더링 ──────────────────────────────────────
  function renderQuestion() {
    if (state.currentIndex >= state.activeIndices.length) {
      showResult();
      return;
    }

    var qIdx = state.activeIndices[state.currentIndex];
    var q = QUIZ_DATA[qIdx];
    var total = state.activeIndices.length;

    // 문제 번호 및 텍스트
    dom.questionNumber.textContent = "문제 " + (state.currentIndex + 1) + " / " + total;
    dom.questionText.textContent = q.question;

    // 점수
    dom.scoreText.textContent = state.score;
    dom.totalText.textContent = total;

    // 프로그레스 바
    var progress = (state.currentIndex / total) * 100;
    dom.progressFill.style.width = progress + "%";
    dom.progressBar.setAttribute("aria-valuenow", Math.round(progress));

    // 재도전 뱃지
    if (state.retryMode) {
      dom.retryBadge.classList.remove("hidden");
    } else {
      dom.retryBadge.classList.add("hidden");
    }

    // 선택지 렌더링
    while (dom.optionsContainer.firstChild) {
      dom.optionsContainer.removeChild(dom.optionsContainer.firstChild);
    }

    q.options.forEach(function (option, index) {
      var btn = document.createElement("button");
      btn.className = "option-btn";
      btn.type = "button";
      btn.textContent = option;
      btn.addEventListener("click", function () {
        selectAnswer(index);
      });
      dom.optionsContainer.appendChild(btn);
    });

    // 해설 숨기기
    dom.explanation.classList.add("hidden");
    dom.explanation.textContent = "";

    // 다음 버튼 숨기기
    dom.nextBtn.classList.add("hidden");

    // 이미 답변한 문제면 결과 표시
    if (state.answers[qIdx] !== undefined) {
      showAnswerResult(state.answers[qIdx], qIdx);
    }

    // 섹션 표시
    dom.quizSection.classList.remove("hidden");
    dom.resultSection.classList.add("hidden");
  }

  function selectAnswer(selected) {
    var qIdx = state.activeIndices[state.currentIndex];
    if (state.answers[qIdx] !== undefined) return;

    state.answers[qIdx] = selected;
    var q = QUIZ_DATA[qIdx];

    if (selected === q.answer) {
      state.score++;
      dom.scoreText.textContent = state.score;
      // 정답 → 오답 노트에서 제거
      removeFromScrapbook(qIdx);
    } else {
      // 오답 → 오답 노트에 추가/업데이트
      addToScrapbook(qIdx, selected);
    }

    saveState();
    showAnswerResult(selected, qIdx);
  }

  function showAnswerResult(selected, qIdx) {
    var q = QUIZ_DATA[qIdx];
    var buttons = dom.optionsContainer.querySelectorAll(".option-btn");

    buttons.forEach(function (btn, index) {
      btn.disabled = true;
      if (index === q.answer) {
        btn.classList.add("correct");
        btn.textContent = ICONS.CORRECT + " " + btn.textContent;
      } else if (index === selected && selected !== q.answer) {
        btn.classList.add("wrong");
        btn.textContent = ICONS.WRONG + " " + btn.textContent;
      }
    });

    // 해설 표시
    dom.explanation.textContent = q.explanation;
    dom.explanation.classList.remove("hidden");

    // 다음 버튼 표시 + 포커스 이동
    if (state.currentIndex === state.activeIndices.length - 1) {
      dom.nextBtn.textContent = "결과 보기";
    } else {
      dom.nextBtn.textContent = "다음 문제";
    }
    dom.nextBtn.classList.remove("hidden");
    dom.nextBtn.focus();
  }

  function nextQuestion() {
    state.currentIndex++;
    saveState();
    renderQuestion();
  }

  // ─── 결과 화면 ─────────────────────────────────────────
  function showResult() {
    dom.quizSection.classList.add("hidden");
    dom.resultSection.classList.remove("hidden");
    dom.progressFill.style.width = "100%";
    dom.progressBar.setAttribute("aria-valuenow", "100");

    var total = state.activeIndices.length;
    var percentage = (state.score / total) * 100;
    var emoji, message;

    if (percentage >= SCORE_THRESHOLDS.PERFECT) {
      emoji = "🏆";
      message = "완벽합니다! AWS 기초를 확실히 이해하고 계시네요!";
    } else if (percentage >= SCORE_THRESHOLDS.GOOD) {
      emoji = "👍";
      message = "좋습니다! 몇 가지 개념을 더 공부하면 완벽해질 거예요!";
    } else {
      emoji = "📚";
      message = "AWS 기초 개념을 조금 더 학습해보세요!";
    }

    dom.resultEmoji.textContent = emoji;
    dom.resultScore.textContent = state.score + " / " + total;
    dom.resultMessage.textContent = message;

    var wrongCount = getWrongIndices().length;
    if (wrongCount > 0) {
      dom.retryWrongBtn.disabled = false;
      dom.retryWrongBtn.textContent = "틀린 문제만 다시 풀기 (" + wrongCount + "문제)";
    } else {
      dom.retryWrongBtn.disabled = true;
      dom.retryWrongBtn.textContent = "모두 정답!";
    }
  }

  function getWrongIndices() {
    var wrong = [];
    for (var i = 0; i < state.activeIndices.length; i++) {
      var idx = state.activeIndices[i];
      if (state.answers[idx] !== undefined && state.answers[idx] !== QUIZ_DATA[idx].answer) {
        wrong.push(idx);
      }
    }
    return wrong;
  }

  function retryWrong() {
    var wrongIndices = getWrongIndices();
    if (wrongIndices.length === 0) return;

    for (var i = 0; i < wrongIndices.length; i++) {
      delete state.answers[wrongIndices[i]];
    }

    state.activeIndices = wrongIndices;
    state.currentIndex = 0;
    state.score = 0;
    state.retryMode = true;
    saveState();
    renderQuestion();
  }

  function resetQuiz() {
    resetState();
    storageRemove(STORAGE_KEY_STATE);
    dom.retryBadge.classList.add("hidden");
    renderQuestion();
  }

  // ─── 오답 노트 렌더링 ──────────────────────────────────
  function renderScrapbook() {
    // 기존 내용 제거
    while (dom.scrapbookContent.firstChild) {
      dom.scrapbookContent.removeChild(dom.scrapbookContent.firstChild);
    }

    if (scrapbook.length === 0) {
      var emptyDiv = document.createElement("div");
      emptyDiv.className = "scrapbook-empty";

      var iconDiv = document.createElement("div");
      iconDiv.className = "scrapbook-empty-icon";
      iconDiv.textContent = "📋";

      var textP = document.createElement("p");
      textP.className = "scrapbook-empty-text";
      textP.textContent = "아직 스크랩한 오답이 없습니다. 퀴즈에서 틀린 문제가 자동으로 저장됩니다.";

      emptyDiv.appendChild(iconDiv);
      emptyDiv.appendChild(textP);
      dom.scrapbookContent.appendChild(emptyDiv);
      dom.scrapbookActions.classList.add("hidden");
      return;
    }

    dom.scrapbookActions.classList.remove("hidden");

    scrapbook.forEach(function (item) {
      var q = QUIZ_DATA[item.questionIndex];
      if (!q) return;

      var selectedText = q.options[item.selectedAnswer] || "";
      var correctText = q.options[q.answer] || "";

      var card = document.createElement("div");
      card.className = "scrap-card";

      // 헤더
      var header = document.createElement("div");
      header.className = "scrap-card-header";

      var numberSpan = document.createElement("span");
      numberSpan.className = "scrap-card-number";
      numberSpan.textContent = "문제 " + (item.questionIndex + 1) + " · " + item.timestamp;

      var removeBtn = document.createElement("button");
      removeBtn.className = "scrap-card-remove";
      removeBtn.type = "button";
      removeBtn.textContent = "✕";
      removeBtn.title = "삭제";
      removeBtn.addEventListener("click", function () {
        removeFromScrapbook(item.questionIndex);
        renderScrapbook();
      });

      header.appendChild(numberSpan);
      header.appendChild(removeBtn);

      // 질문
      var questionDiv = document.createElement("div");
      questionDiv.className = "scrap-card-question";
      questionDiv.textContent = q.question;

      // 내 답
      var myAnswerDiv = document.createElement("div");
      myAnswerDiv.className = "scrap-card-answer";

      var myLabel = document.createElement("span");
      myLabel.className = "scrap-label wrong";
      myLabel.textContent = "내 답:";

      var myText = document.createElement("span");
      myText.textContent = selectedText;

      myAnswerDiv.appendChild(myLabel);
      myAnswerDiv.appendChild(myText);

      // 정답
      var correctDiv = document.createElement("div");
      correctDiv.className = "scrap-card-answer";

      var correctLabel = document.createElement("span");
      correctLabel.className = "scrap-label correct";
      correctLabel.textContent = "정답:";

      var correctSpan = document.createElement("span");
      correctSpan.textContent = correctText;

      correctDiv.appendChild(correctLabel);
      correctDiv.appendChild(correctSpan);

      // 해설
      var explanationDiv = document.createElement("div");
      explanationDiv.className = "scrap-card-explanation";
      explanationDiv.textContent = q.explanation;

      // 조합
      card.appendChild(header);
      card.appendChild(questionDiv);
      card.appendChild(myAnswerDiv);
      card.appendChild(correctDiv);
      card.appendChild(explanationDiv);

      dom.scrapbookContent.appendChild(card);
    });
  }

  // ─── 이벤트 바인딩 ─────────────────────────────────────
  function bindEvents() {
    dom.tabQuiz.addEventListener("click", function () {
      switchTab("quiz");
    });
    dom.tabScrapbook.addEventListener("click", function () {
      switchTab("scrapbook");
    });
    dom.nextBtn.addEventListener("click", nextQuestion);
    dom.resetBtn.addEventListener("click", resetQuiz);
    dom.retryWrongBtn.addEventListener("click", retryWrong);
    dom.clearScrapBtn.addEventListener("click", clearScrapbook);
  }

  // ─── 초기화 ────────────────────────────────────────────
  function init() {
    cacheDom();
    loadState();
    loadScrapbook();
    updateBadge();
    bindEvents();
    renderQuestion();
  }

  // DOM 로드 후 실행
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
