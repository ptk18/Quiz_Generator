<script lang="ts">
    export let question: {
        question: string;
        optionA: string;
        optionB: string;
        optionC: string;
        optionD: string;
        correctAns: string;
        userAnswer: string;
        isCorrect: boolean;
    };
    export let index: number;
</script>

<style>
    .question-container {
        border: 1px solid var(--button-color);
        border-radius: 0.5rem;
        padding: 15px;
        margin-bottom: 20px;
        text-align: left;
    }

    p {
        font-size: 18px;
        margin-bottom: 20px;
    }

    .option {
        padding: 10px 20px;
        width: 95%;
        text-align: left;
        margin-bottom: 0.5rem;
        border-radius: 5px;
    }

    #correctAns {
        background-color: rgb(205, 246, 205);
        color: green;
    }

    .correct {
        background-color: rgb(205, 246, 205);
        color: green;
    }

    .incorrect {
        background-color: rgb(246, 205, 213);
        color: red;
    }
</style>

<div class="question-container">
    <p>{index + 1}. {question.question}</p>
    <div class="options">
        <div class="option" id="correctAns">Correct Answer: {question.correctAns}</div>
        <div 
            class="option" 
            class:correct={question.userAnswer === question.correctAns}
            class:incorrect={question.userAnswer !== question.correctAns}
        >
            Your Answer: {question.userAnswer}
        </div>
    </div>
</div>
