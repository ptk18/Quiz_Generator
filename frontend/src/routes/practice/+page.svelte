<script lang="ts">
    import Practice from "$lib/Practice.svelte";
    import { goto } from "$app/navigation";
    import { onMount } from 'svelte';
    
    
    interface Question {
        question: string;
        optionA: string;
        optionB: string;
        optionC: string;
        optionD: string;
        correctAns: string;
    }
    
    export let generatedQuiz: { questions: Question[] };
    let userAnswers: { [key: string]: string } = {};
    onMount(() => {
        const storedQuiz = sessionStorage.getItem('generatedQuiz');
        if (storedQuiz) {
            generatedQuiz = JSON.parse(storedQuiz);
        } else {
            // Redirect if no quiz is found (e.g., page was reloaded)
            goto('/');
        }
    });



    function handleSubmitAnswers(event: Event) {
        event.preventDefault();
        if (!generatedQuiz) return;

        let correctCount = 0;
        const totalQuestions = generatedQuiz.questions.length;
        const answerDetails: { [key: string]: { userAnswer: string; isCorrect: boolean } } = {};

        // Calculate the score
        generatedQuiz.questions.forEach((question, index) => {
            const userAnswer = userAnswers[question.question];
            // Store user answer and correctness in answerDetails

            answerDetails[question.question] = {
                userAnswer: userAnswer,
                isCorrect: userAnswer === question.correctAns
            };

            if (userAnswer === question.correctAns) {
                correctCount++;
            }
        });

        // Log the score in the desired format
        console.log(`Score: ${correctCount}/${totalQuestions}`);
        console.log("Generated Quiz:", generatedQuiz);
        
        // // Store the score in local storage
        // localStorage.setItem('quizScore', JSON.stringify({ score: correctCount, total: totalQuestions }));
            // Store the score and user's answers in local storage
        localStorage.setItem('quizResult', JSON.stringify({
            score: correctCount,
            total: totalQuestions,
            questions: generatedQuiz,
            answers: answerDetails
        }));

        // Navigate to the score page
        goto('/score');
    }

</script>

<div class="main-container">
    <form on:submit={handleSubmitAnswers}>
        <div class="quiz-container">
            <h1>Welcome To Our Quiz</h1>
            
            {#if generatedQuiz && generatedQuiz.questions}
                {#each generatedQuiz.questions as question, index}
                    <Practice 
                        {question}
                        questionNumber={index + 1}
                        bind:userAnswer={userAnswers[question.question]}
                    />
                {/each}
            {/if}
        </div>
        
        <div class="button-container">
            <button type="reset" class="btn clear-btn" >
                Clear Your Answers
            </button>
            <button type="submit" class="btn submit-btn">
                Submit Your Answers
            </button>
        </div>
    </form>
</div>

<style>
    .main-container {
        width: 80%;
        margin: 0 auto;
    }

    .quiz-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
        margin-bottom: 20px;
        text-align: center;
    }

    .button-container {
        display: flex;
        justify-content: space-around;
    }

    .btn {
        padding: 10px 20px;
        background-color: var(--button-color);
        border: none;
        border-radius: 5px;
        color: white;
        font-size: 18px;
        cursor: pointer;
        margin-top: 20px;
        width: 40%;
    }

    .clear-btn {
        background-color: var(--button-color);
    }

    .btn:hover {
        background-color: white;
        border: 1px solid var(--button-color);
        color: var(--button-color);
    }
</style>