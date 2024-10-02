<script lang="ts">
    import View from "$lib/View.svelte";
    import { selectedQuiz } from "$lib/quizStore"; // Import the store
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

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

    // Declare quizData with the appropriate type
    let quizData: Quiz | null = null; // To hold the selected quiz


    // Subscribe to the selectedQuiz store
    selectedQuiz.subscribe(value => {
        quizData = value;
    });    

    // Function to handle the retake quiz button
    function retakeQuiz() {
        if (quizData) {
            // Store the selected quiz in sessionStorage to pass data between pages
            sessionStorage.setItem('generatedQuiz', JSON.stringify(quizData));

            // Navigate to the /practice page
            goto('/practice');
        }
    }
</script>
<style>
    .view-mode {

    width: 80%;
    margin: auto;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(55, 17, 17, 0.1);
    text-align: center;

    }

    h1 {
    font-size: 24px;
    margin-bottom: 20px;
    }


  
    button {
        padding: 12px 40px;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        cursor: pointer;
        color: #fff;
        background-color: hsl(5, 85%, 63%);
        margin-top: 10px;
        
    }

    button:hover {
        background-color: hsl(5, 67%, 52%);
    }



</style>

<div class="view-mode">
    <h1>View Mode</h1>
    {#if quizData}
        {#each quizData.questions as question, index}
            <View {question} {index} />
        {/each}
    {:else}
        <p>No quiz data available.</p>
    {/if}
    <button class="retake-quiz" on:click={retakeQuiz}>Retake Quiz</button>
  </div>
  