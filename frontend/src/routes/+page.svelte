<script>
    import { goto } from "$app/navigation";
    let quizText = '';
    let numQuestions = '';
    let difficulty = '';
    let generatedQuiz = null;
    let isLoading = false;
    const apiUrl = import.meta.env.VITE_API_URL;
 
    async function handleSubmit(event) {
        event.preventDefault();
        isLoading = true;
 
 
        // Set defaults if not provided
        const questionsCount = numQuestions ? parseInt(numQuestions) : 5; // Default to 5
        const quizDifficulty = difficulty || 'easy'; // Default to "easy"
 
 
        try {
            //const response = await fetch('http://backend:8000/api/generate-quiz', {
            const response = await fetch('${apiUrl}/api/generate-quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: quizText,
                    num_questions: questionsCount, // Use the adjusted questionsCount
                    difficulty: quizDifficulty // Use the adjusted quizDifficulty
                }),
            });
 
 
            if (response.ok) {
                generatedQuiz = await response.json();
                //goto('/practice', { state: { quiz: generatedQuiz } });
                sessionStorage.setItem('generatedQuiz', JSON.stringify(generatedQuiz));
                goto('/practice');

            } else {
                throw new Error('Failed to generate quiz');
            }
        } catch (error) {
            // @ts-ignore
            alert(error.message);
        } finally {
            isLoading = false;
        }
    }
 </script>
 
 
 <style>
    .container {
        width: 100%;
        margin: 0 auto;
        text-align: center;
    }
 
 
    h1 {
        font-size: 2.5em;
        margin-bottom: 5px;
        color: var(--button-color);
    }
 
 
    p {
        font-size: 1.4em;
        margin-bottom: 2rem;
        font-style: italic;
 
 
    }
 
 
    #quiz-form{
        border: 1px solid var(--button-color);
        border-radius: 1rem;
        padding: 3rem 1.5rem;
      
    }
 
 
    /* Textarea styling */
    textarea {
        width: 95%;
        height: 250px;
        padding: 15px;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        resize: none;
        overflow-y: auto; /* Vertical scroll */
        margin-bottom: 20px;
    }
 
 
    /* Form group container */
    .form-group {
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
    }
 
 
    /* Dropdown styles */
    select {
        width: 30%;
        padding: 10px;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
 
 
    /* Button styling */
    button {
        padding: 0.7rem 2.5rem;
        font-size: 1rem;
        background-color:var(--button-color);
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
 
 
    /* Button hover effect */
    button:hover {
        background-color: #0056b3;
    }
 
 
    /* Media query for mobile responsiveness */
    @media (max-width: 768px) {
        .form-group {
            flex-direction: column;
        }
 
 
        select, button {
            width: 100%;
            margin-bottom: 10px;
        }
        h1{
            font-size: 2rem;
        }
        p{
            font-size: 1.2rem;
        }
    }
    .generated-quiz {
        margin-top: 2rem;
        text-align: left;
    }
 
 
    .question {
        margin-bottom: 1rem;
    }
 
 
    .question ul {
        list-style-type: none;
        padding-left: 1rem;
    }
 </style>
 
 
 <div class="container">
    <h1>Welcome To Quiz Portal!</h1>
    <p>"Can Generate Quiz and Practice"</p>
   
    <form id="quiz-form" on:submit={handleSubmit}>
        <!-- Text area for typing content -->
        <textarea bind:value={quizText} placeholder="Type Here..." rows="6"></textarea>
       
        <!-- Dropdowns and Generate button -->
        <div class="form-group">
            <!-- Number of Questions Dropdown -->
            <select bind:value={numQuestions}>
                <option value="" disabled selected>No of Questions</option>
                <option value="5">5 Questions</option>
                <option value="10">10 Questions</option>
                <option value="15">15 Questions</option>
                <option value="20">20 Questions</option>
            </select>
           
            <!-- Difficulty Level Dropdown -->
            <select bind:value={difficulty}>
                <option value="" disabled selected>Difficulty Level</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
           
            <!-- Generate Button -->
            <button type="submit" disabled={isLoading}>Generate ➔</button>
        </div>
    </form>
 
 
 </div>
 