<script lang="ts">
    import { page } from "$app/stores";
    import { createEventDispatcher } from 'svelte';
    import { selectedQuiz } from "$lib/quizStore"; // Import the store
    const apiUrl = import.meta.env.VITE_API_URL;
    // Define the shape of a single quiz
    interface Quiz {
        q_id: number;
        user_id: number;
        score: number;
        total_questions: number;
        questions: {
            question: string;
            optionA: string;
            optionB: string;
            optionC: string;
            optionD: string;
            correctAns: string;
            userAnswer: string;
            isCorrect: boolean;
        }[];
    }

    // Props passed from the parent component
    export let quiz: Quiz;
    export let index: number;

    const dispatch = createEventDispatcher();
    $: routeId = $page.route.id;

    async function deleteQuiz(quizId: number) {
        try {
            //const response = await fetch(`http://backend:8000/quizzes/${quizId}/delete?current_user_id=${quiz.user_id}`, {
                const response = await fetch(`${apiUrl}/quizzes/${quizId}/delete?current_user_id=${quiz.user_id}`, {
                method: 'DELETE',
            });
            if (response.ok) {
                dispatch('quizDeleted', { quizId });
            } else {
                const errorData = await response.json();
                alert(errorData.detail);
            }
        } catch (error) {
            console.error('Error deleting quiz:', error);
            alert('An error occurred while deleting the quiz.');
        }
    }

    function viewQuiz() {
        selectedQuiz.set(quiz); // Set the selected quiz in the store
    }

    
</script>
<style>
     .quiz-item {
        display: grid;
        grid-template-columns: 3fr 3fr 3fr 3fr;
        align-items: center;
        margin-bottom: 10px;
    }

    .quiz-item div{
        border-right: 1px solid var(--button-color);
        text-align: center;
        font-size: 17px;
    }

    .quiz-item div:last-child {
        border-right: none;
    }

    .quiz-title {
        font-size: 16px;
        font-weight: bold;
    }

    .result{
        color: var(--button-color);
    }
    button{
        border: none;
    }

    button:hover{
        color: var(--button-color);
    }

    .view-btn, .del-btn {
        padding: 5px 10px;
        background-color: white;
        cursor: pointer;
        margin-left: 10px;
        font-size: 17px;
    }

    .quiz-score {
        margin-left: 10px;
        font-weight: bold;
    }

    .divider {
        border: none;
        height: 1px;
        background-color: lightgray;
        margin: 10px 0;
    }
    .view-btn-link{
        display: block;
        color: black;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        cursor: pointer;
    }
    .view-btn-link:hover{
        color: var(--button-color);
    }
</style>

<div class="quiz-item">
    <div class="quiz-title">Quiz {index + 1}</div>
    <div>
        <button class="view-btn" on:click={viewQuiz}>
            <a class="view-btn-link" href="/view">View</a>
        </button>
    </div>
    <div>
        <button class="del-btn" on:click={() => deleteQuiz(quiz.q_id)}>Del</button>
    </div>
    <div>
        <p class="quiz-score"><span class="result">{quiz.score}</span> / {quiz.total_questions}</p> 
    </div>   
</div> 
<hr class="divider"> 