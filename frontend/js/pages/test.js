// Test Page JavaScript
const API_BASE_URL = 'http://localhost:8000';

// State
let questions = [];
let currentQuestionIndex = 0;
let answers = new Array(20).fill(null);

// DOM Elements
const questionCard = document.getElementById('questionCard');
const questionNum = document.getElementById('questionNum');
const questionText = document.getElementById('questionText');
const answerOptions = document.getElementById('answerOptions');
const currentQuestionSpan = document.getElementById('currentQuestion');
const totalQuestionsSpan = document.getElementById('totalQuestions');
const progressFill = document.getElementById('progressFill');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    console.log('📄 검사 페이지 로드됨');
    console.log('🔗 백엔드 서버:', API_BASE_URL);

    await loadQuestions();
    renderQuestion();
    setupEventListeners();

    console.log('✅ 초기화 완료');
});

// Load questions from API
async function loadQuestions() {
    try {
        console.log('🔄 질문 로딩 시작...');
        console.log('📡 API URL:', `${API_BASE_URL}/api/questions`);

        const response = await fetch(`${API_BASE_URL}/api/questions`);

        console.log('📥 응답 상태:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ API 에러:', errorText);
            throw new Error(`질문을 불러오는데 실패했습니다 (${response.status})`);
        }

        const data = await response.json();
        questions = data.questions;
        totalQuestionsSpan.textContent = questions.length;

        console.log('✅ 질문 로드 완료:', questions.length, '개');

    } catch (error) {
        console.error('❌ 질문 로드 실패:', error);

        // 백엔드 서버 확인
        if (error.message.includes('Failed to fetch')) {
            alert('⚠️ 백엔드 서버에 연결할 수 없습니다.\n\n다음을 확인해주세요:\n1. backend 폴더에서 "python main.py" 실행\n2. http://localhost:8000이 열려있는지 확인\n3. 터미널에서 서버가 실행 중인지 확인');

            // 임시 테스트 질문 생성 (개발용)
            console.log('⚠️ 임시 질문 생성 중...');
            questions = Array(20).fill(null).map((_, i) => ({
                id: i + 1,
                text: `질문 ${i + 1}: 백엔드 서버를 실행해주세요.`,
                order: i + 1
            }));
            totalQuestionsSpan.textContent = questions.length;
        } else {
            alert(`질문을 불러오는데 실패했습니다.\n\n에러: ${error.message}\n\n페이지를 새로고침해주세요.`);
        }
    }
}

// Render current question
function renderQuestion() {
    if (questions.length === 0) return;

    const question = questions[currentQuestionIndex];

    // Update question text with animation
    questionCard.style.animation = 'none';
    setTimeout(() => {
        questionCard.style.animation = 'fadeInScale 0.5s ease';
    }, 10);

    questionNum.textContent = currentQuestionIndex + 1;
    questionText.textContent = question.text;
    currentQuestionSpan.textContent = currentQuestionIndex + 1;

    // Update progress bar
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = `${progress}%`;

    // Highlight selected answer
    const answerButtons = answerOptions.querySelectorAll('.answer-btn');
    answerButtons.forEach(btn => {
        const value = parseInt(btn.dataset.value);
        if (answers[currentQuestionIndex] === value) {
            btn.classList.add('selected');
        } else {
            btn.classList.remove('selected');
        }
    });

    // Update navigation buttons
    updateNavigationButtons();
}

// Setup event listeners
function setupEventListeners() {
    // Answer buttons
    const answerButtons = answerOptions.querySelectorAll('.answer-btn');
    answerButtons.forEach(btn => {
        btn.addEventListener('click', () => handleAnswerClick(btn));
    });

    // Navigation buttons
    prevBtn.addEventListener('click', handlePrevious);
    nextBtn.addEventListener('click', handleNext);
}

// Handle answer selection
function handleAnswerClick(button) {
    const value = parseInt(button.dataset.value);

    // Save answer
    answers[currentQuestionIndex] = value;

    // Update UI
    const answerButtons = answerOptions.querySelectorAll('.answer-btn');
    answerButtons.forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');

    // Enable next button
    nextBtn.disabled = false;

    // Auto-advance after short delay (optional)
    setTimeout(() => {
        if (currentQuestionIndex < questions.length - 1) {
            handleNext();
        }
    }, 300);
}

// Handle previous button
function handlePrevious() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion();
    }
}

// Handle next button
function handleNext() {
    if (currentQuestionIndex < questions.length - 1) {
        // Go to next question
        currentQuestionIndex++;
        renderQuestion();
    } else {
        // Submit test
        submitTest();
    }
}

// Update navigation button states
function updateNavigationButtons() {
    // Previous button
    prevBtn.disabled = currentQuestionIndex === 0;

    // Next button
    const hasAnswer = answers[currentQuestionIndex] !== null;
    const isLastQuestion = currentQuestionIndex === questions.length - 1;

    nextBtn.disabled = !hasAnswer;
    nextBtn.innerHTML = isLastQuestion
        ? '결과 보기 <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>'
        : '다음 <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>';
}

// Submit test to API
async function submitTest() {
    // Validate all answers
    const unanswered = answers.findIndex(a => a === null);
    if (unanswered !== -1) {
        alert(`${unanswered + 1}번 질문에 답변해주세요.`);
        currentQuestionIndex = unanswered;
        renderQuestion();
        return;
    }

    // Show loading
    loadingOverlay.style.display = 'flex';

    try {
        const response = await fetch(`${API_BASE_URL}/api/results`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                answers: answers
            })
        });

        if (!response.ok) {
            throw new Error('결과 생성에 실패했습니다');
        }

        const result = await response.json();
        console.log('✅ 결과 생성 완료:', result);

        // Redirect to result page
        window.location.href = `result.html?id=${result.id}`;

    } catch (error) {
        console.error('❌ 제출 실패:', error);
        loadingOverlay.style.display = 'none';
        alert('결과 생성에 실패했습니다. 다시 시도해주세요.');
    }
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (loadingOverlay.style.display === 'flex') return;

    if (e.key === 'ArrowLeft' && !prevBtn.disabled) {
        handlePrevious();
    } else if (e.key === 'ArrowRight' && !nextBtn.disabled) {
        handleNext();
    } else if (e.key >= '1' && e.key <= '5') {
        const value = parseInt(e.key);
        const button = Array.from(answerOptions.querySelectorAll('.answer-btn'))
            .find(btn => parseInt(btn.dataset.value) === value);
        if (button) {
            handleAnswerClick(button);
        }
    }
});

// Prevent accidental page leave
window.addEventListener('beforeunload', (e) => {
    const hasAnswers = answers.some(a => a !== null);
    const isComplete = answers.every(a => a !== null);

    if (hasAnswers && !isComplete) {
        e.preventDefault();
        e.returnValue = '';
    }
});