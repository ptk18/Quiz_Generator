<script lang="ts">
    interface Question {
        question: string;
        optionA: string;
        optionB: string;
        optionC: string;
        optionD: string;
        correctAns: string;
    }
    
    export let question: Question;
    export let questionNumber: number;
    export let userAnswer: string = '';

    console.log("Question received:", question);
</script>

<div class="quiz-card">
    <p class="question">{questionNumber}. {question.question}</p>
    <div class="answers">
        <label class="option">
            <input 
                type="radio" 
                name="question{questionNumber}" 
                value="A"
                bind:group={userAnswer}
            >
            <span class="circle">A</span> 
            <span class="answer-text">{question.optionA}</span>
        </label>
        <label class="option">
            <input 
                type="radio" 
                name="question{questionNumber}" 
                value="B"
                bind:group={userAnswer}
            >
            <span class="circle">B</span> 
            <span class="answer-text">{question.optionB}</span>
        </label>
        <label class="option">
            <input 
                type="radio" 
                name="question{questionNumber}" 
                value="C"
                bind:group={userAnswer}
            >
            <span class="circle">C</span> 
            <span class="answer-text">{question.optionC}</span>
        </label>
        <label class="option">
            <input 
                type="radio" 
                name="question{questionNumber}" 
                value="D"
                bind:group={userAnswer}
            >
            <span class="circle">D</span> 
            <span class="answer-text">{question.optionD}</span>
        </label>
    </div>
</div>
<style>
    .quiz-card {
        border: 2px solid var(--button-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .question {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .answers {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }

    .option {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        width: 48%;
    }

    input[type="radio"] {
        display: none;
    }

    .circle {
        display: inline-block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 1px solid var(--button-color);
        color: var(--button-color);
        font-weight: bold;
        text-align: center;
        line-height: 40px;
        margin-right: 10px;
    }

    input[type="radio"]:checked + .circle {
        background-color: var(--button-color);
        color: white;
    }

    .answer-text {
        font-weight: bold;
    }

    .button-container {
        display: flex;
        justify-content: space-around;
    } 
</style>

