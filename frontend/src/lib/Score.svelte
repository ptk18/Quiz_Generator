<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { userInfo } from "$lib/loginUserInfo";

    let score: number = 0;
    let total: number = 0;
    let answers: { [key: string]: { userAnswer: string; isCorrect: boolean } } = {};
    let questions: { question: string; optionA: string; optionB: string; optionC: string; optionD: string; correctAns: string; }[] = [];
    let quizSaved = false;
    let currentUser: { id: number | null; name: string; email: string; isLoggedIn: boolean };

    // Subscribe to the userInfo store
    userInfo.subscribe(value => {
        currentUser = value;
    });

    onMount(async () => {
        // Retrieve score from local storage
        const storedResult = localStorage.getItem('quizResult');
        if (storedResult) {
            const { score: storedScoreValue, total: storedTotalValue, answers: storedAnswers, questions: storedQuestions } = JSON.parse(storedResult);
            score = storedScoreValue;
            total = storedTotalValue;
            answers = storedAnswers;
            questions = storedQuestions.questions;

        } else {
            // Redirect to home if no score is found
            goto('/');
        }
    });


    async function saveQuiz() {
        if (quizSaved) {
            alert("This quiz has already been saved!");
            return;
        }

        if (!currentUser.isLoggedIn || !currentUser.id) {
            alert("Please log in to save your quiz results.");
            return;
        }
        
        try {
            // Format the questions and answers into the desired structure
            const formattedQuestions = questions.map(q => {
                const userAnswerData = answers[q.question];
                // Create a new object with only the properties we want
                return {
                    question: q.question,
                    optionA: q.optionA,
                    optionB: q.optionB,
                    optionC: q.optionC,
                    optionD: q.optionD,
                    correctAns: q.correctAns,
                    userAnswer: userAnswerData.userAnswer,
                    isCorrect: userAnswerData.isCorrect
                };
            });

            const payload = {
                user_id: currentUser.id,
                questions: formattedQuestions,
                score: score,
                total_questions: total
            };

            const response = await fetch('http://localhost:8000/save-quiz/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });


            if (response.ok) {
                const data = await response.json();
                console.log('Quiz saved successfully:', data);
                quizSaved = true;
                alert("Your quiz has been saved successfully!");
            } else {
                const errorData = await response.json();
                console.error("Failed to save quiz:", errorData);
                alert("There was an error saving your quiz. Please try again.");
            }
        } catch (error) {
            console.error("Error saving quiz:", error);
            alert("There was an error saving your quiz. Please try again.");
        }
    }

    function handleNewQuiz() {
        goto('/');
    }
</script>
<style>

    .container {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(55, 17, 17, 0.1);
        margin: 0 auto;
        width:65%;
        padding: 2rem;
        text-align: center;
        background-color: white;
    }


    img{
    
        width: 250px;
        height: 250px;
        margin: 0 auto 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    h1 {
        color: var(--button-color);
        font-size: 30px;
        margin-bottom: 20px;
    }


    .score-title {
      
        font-size: 25px;
        margin-bottom: 10px;
    }

    .score {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .message {
        font-size: 18px;
        margin-bottom: 20px;
    }

    .result-score{
        color: var(--button-color);
    }

    .button-container {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
    }

    .btn {
        padding: 12px;
        background-color: hsl(5, 85%, 63%);
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 17px;
    }

    .btn:hover{
        background-color: white;
        border: 1px solid var(--button-color);
        color: var(--button-color);
    }

    .save-btn {
        width: 35%;
    }

    .generate-btn {
        width: 35%;
    }
    .debug-info {
        font-size: 0.8rem;
        color: #666;
        margin: 10px 0;
    }

</style>

<div class="container">
    <div class="image-box">
        <img src="/congratulation.png" alt="congratulation">
    </div>
    <h1>CONGRATULATIONS!</h1>
    <p class="score-title">Your Score</p>
    <p class="score"><span class="result-score">{score}</span> / {total}</p>
    <p class="message">You did a great job, learn more by taking another quiz.</p>
    
    <!-- Debug information -->
    {#if currentUser.isLoggedIn}
        <p class="debug-info">Logged in as: {currentUser.name} (ID: {currentUser.id})</p>
    {:else}
        <p class="debug-info">Not logged in</p>
    {/if}

    <div class="button-container">
        <button 
            class="btn save-btn" 
            on:click={saveQuiz} 
            disabled={quizSaved || !currentUser.isLoggedIn}
        >
        {#if quizSaved}
                Quiz Saved
            {:else if !currentUser.isLoggedIn}
                Login to Save
            {:else}
                Save the Quiz
            {/if}
        </button>
        <button class="btn generate-btn" on:click={handleNewQuiz}>New Quiz</button>
    </div>    
</div>
