<script lang="ts">
    import {onMount} from "svelte";
    const API_URL = import.meta.env.VITE_API_URL;

    interface User{
        name: string;
        email: string;
        password: string;
    }

    async function handleSubmit(event:Event) {
        event.preventDefault();

        const form = event.target as HTMLFormElement;
        const name= (form.elements.namedItem("name") as HTMLInputElement).value;
        const email= (form.elements.namedItem("email") as HTMLInputElement).value;
        const password = (form.elements.namedItem("password") as HTMLInputElement).value;

        if(password.length < 8){
            alert("Password must be at least 8 characters long.");
            return;
        }

        const user: User ={
            name: name,
            email: email,
            password: password,
        };

        try {
            const response = await fetch(`${API_URL}/create-user/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user), 
            });
            if (response.ok) {
                const data = await response.json();
                console.log("User created:", data);
                alert("Sign-up successful! Welcome to QuizPortal.");
                // You can handle the response further here (e.g., redirect or show a success message)
                window.location.href = "/login";
            } else {
                const errorData = await response.json();
                console.error("Error creating user:", errorData.detail);
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error("Unexpected error:", error);
            alert("Unexpected error. Please try again.");
        }
    }

</script>
<style>

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 400px;
        margin: 3.5rem auto;
    }

    .logo h1 {
        color: hsl(5, 85%, 63%);
        font-weight: bold;
        margin-bottom: 40px;
    }

    .signup-box {
        background-color: #fff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(55, 17, 17, 0.1);
        text-align: center;
        width: 100%;
    }

    .signup-box h2 {
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: #333;
    }

    .signup-box p {
        margin-bottom: 28px;
        color: #666;
        font-size: 0.9rem;
    }

    form {
        display: flex;
        flex-direction: column;
    }

    label {
        font-size: 0.9rem;
        color: #555;
        text-align: left;
        margin-bottom: 0.5rem;
    }

    input {
        padding: 12px;
        font-size: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
        margin-bottom: 1.5rem;
    }

    input:focus {
        outline: none;
        border-color: hsl(5, 85%, 63%);
    }

    .checkbox {
        display: flex;
        align-items: flex-start;
        margin-top: 10px;
    }

    .checkbox input {
        margin-right: 10px;
    }

    .checkbox label {
        font-size: 0.85rem;
        color: #555;
    }

    .checkbox a {
        color: hsl(5, 85%, 63%);
        text-decoration: none;
    }

    .checkbox a:hover {
        text-decoration: underline;
    }

    .signup-btn {
        padding: 12px;
        background-color: hsl(5, 85%, 63%);
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 15px;
    }

    .signup-btn:hover {
        background-color: hsl(5, 80%, 57%);
    }


</style>

<div class="container">
    <div class="logo">
        <h1>QuizPortal</h1>
    </div>

    <div class="signup-box">
        <h2>Sign up</h2>
        <p>Just one more step to create your first test!</p>
        <form on:submit={handleSubmit}>
            <label for="name">Name</label>
            <input type="name" id="name" placeholder="Enter your name" required>

            <label for="email">Email address</label>
            <input type="email" id="email" placeholder="Enter your email" required>

            <label for="password">Password (min. 8 characters)</label>
            <input type="password" id="password" placeholder="Enter your password" required>

            <div class="checkbox">
                <input type="checkbox" id="terms" required>
                <label for="terms">By signing up I agree to <a href="/">Terms & Conditions</a> and <a href="/">Privacy Policy</a>.</label>
            </div>

            <button type="submit" class="signup-btn">Sign up</button>
        </form>
        <div class="forgot-password">
            <p>Already have an account? <a href="/login" style="font-size:small">Log in here</a></p>
        </div>

    </div>
</div>