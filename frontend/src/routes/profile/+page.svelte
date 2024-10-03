<script lang="ts">
    import { onMount } from "svelte";
    import { userInfo } from "$lib/loginUserInfo";
    import QuizScore from "$lib/QuizScore.svelte";
    import { goto } from '$app/navigation';
    const apiUrl = import.meta.env.VITE_API_URL;

    let user = $userInfo; // Reactive subscription to the store

    onMount(() => {
        // Redirect if not logged in
        if (!user.isLoggedIn) {
            goto('/login');
        }
    });

    let currentUser: { id: number | null; name: string; email: string; isLoggedIn: boolean };

    // Subscribe to the userInfo store
    userInfo.subscribe(value => {
        currentUser = value;
    });
    // Define the type for quizzes array
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

    let quizzes: Quiz[] = [];
    let noQuizzes = false;

     // Fetch quizzes on mount
     onMount(async () => {
        if (!currentUser.isLoggedIn) {
            goto('/login');
        } else {
            await fetchQuizzes();
        }
    });

    async function fetchQuizzes() {
        //const response = await fetch(`http://backend:8000/users/${currentUser.id}/quizzes`);
        const response = await fetch(`${apiUrl}/users/${currentUser.id}/quizzes`);
        const data = await response.json();
        if (data.detail === "No quizzes found for this user") {
            noQuizzes = true;
        } else {
            quizzes = data;
            noQuizzes = false;
        }
    }

    function handleQuizDeleted(event: CustomEvent<{quizId: number}>) {
        console.log('Quiz deleted event received:', event.detail);
        const deletedQuizId = event.detail.quizId;
        console.log('Before filter:', quizzes.length);
        quizzes = quizzes.filter(quiz => quiz.q_id !== deletedQuizId);
        console.log('After filter:', quizzes.length);
        
        if (quizzes.length === 0) {
            noQuizzes = true;
        }
    }

    //const quizzes = Array(5).fill({});
</script>
<style>

    .profile-container {
        width: 80%;
        margin: 0 auto;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .profile-card {
        display: grid;
        grid-template-columns: repeat(2,1fr);
        align-items: center;
        border: 2px solid var(--button-color);
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .profile-image img {
        width: 180px;
        height: 180px;
        padding-left: 200px;
        border-radius: 50%;
        margin-right: 20px;
    }

    .profile-info {
        text-align: left;
    }

    .profile-name {
        font-size: 18px;
        font-weight: bold;
    }

    .profile-email, .profile-phone {
        font-size: 16px;
        color: gray;
        margin-top: 5px;
    }

    .quiz-list {
        border: 2px solid var(--button-color);
        border-radius: 10px;
        padding: 10px;
    }

   

</style>
    <div class="profile-container">
        <div class="profile-card">
            <div class="profile-image">
                <img src="/profile.jpg" alt="User Image">
            </div>
            <div class="profile-info">
                <p class="profile-name">{user.name}</p>
                <p class="profile-email">{user.email}</p>
            </div>
        </div>
        
        <div class="quiz-list">
            {#if noQuizzes}
                <p class="no-quizzes">No quizzes found.</p>
            {:else}
                {#each quizzes as quiz, index}
                    <QuizScore 
                        {quiz} 
                        {index}
                        on:quizDeleted={handleQuizDeleted}
                    />
                {/each}
            {/if}
        </div>
    </div>


