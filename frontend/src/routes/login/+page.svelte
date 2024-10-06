<script lang="ts">
    import { userInfo } from "$lib/loginUserInfo";
    import { goto } from '$app/navigation';

    interface UserLogin {
        email: string;
        password: string;
    }

    // Use localhost for browser-based requests
    //const API_URL = 'http://localhost:8000';
    const API_URL = import.meta.env.VITE_API_URL;

    async function handleLogin(event: Event) {
        event.preventDefault();

        const form = event.target as HTMLFormElement;
        const email = (form.elements.namedItem("email") as HTMLInputElement).value;
        const password = (form.elements.namedItem("password") as HTMLInputElement).value;

        const user: UserLogin = {
            email,
            password,
        };

        try {
            const response = await fetch(`${API_URL}/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            });

            if (response.ok) {
                const data = await response.json();
                console.log("login data here ", data);
                
                userInfo.set({
                    id: data.id,
                    name: data.name,
                    email: data.email,
                    isLoggedIn: true,
                });

                goto('/profile');
            } else {
                const errorData = await response.json();
                alert(errorData.detail);
            }
        } catch (error) {
            console.error("Unexpected error:", error);
            alert("Failed to connect to the server. Please try again.");
        }
    }
</script>

<style>

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 3rem auto;
    }

    .logo h1 {
        color:hsl(5, 85%, 63%);
        font-weight: bold;
        margin-bottom: 40px;
        padding: 0;
    }

    .login-box {
        background-color: #fff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        width: 350px;
        text-align: center;
    }

    .login-box h2 {
        margin-bottom: 20px;
        color: #333;
    }

    form {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 20px;
    }

    label {
        font-size: 0.9rem;
        color: #555;
        text-align: left;
    }

    input {
        padding: 10px;
        font-size: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
        margin-bottom: 0.5rem;
    }

    button {
        padding: 12px;
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


    .signup-button {
        background-color: #fff;
        border: 1px solid #ddd;
        color: black;
        width: 100%;
    }

    .signup-button:hover {
        background-color: #fff;
        border: 1px solid hsl(5, 85%, 63%);
        color: hsl(5, 85%, 63%);
    }

    .or-divider {
        position: relative;
        margin: 15px 0;
        text-align: center;
    }

    .or-divider::before,
    .or-divider::after {
        content: "";
        position: absolute;
        width: 45%;
        height: 1px;
        background-color: #ddd;
        top: 50%;
    }

    .or-divider::before {
        left: 0;
    }

    .or-divider::after {
        right: 0;
    }

    .or-divider span {
        background-color: #fff;
        padding: 0 10px;
        color: #888;
        font-size: 0.9rem;
    }

    .forgot-password {
        margin-top: 20px;
    }

    .forgot-password a {
        font-size: 0.85rem;
        color: hsl(5, 85%, 63%);
        text-decoration: none;
    }

    .forgot-password a:hover {
        text-decoration: underline;
    }


</style>

<div class="container">
    <div class="logo">
        <h1>QuizPortal</h1>
    </div>
    <div class="login-box">
        <h2>Login</h2>
        <form on:submit={handleLogin}>
            <label for="email">Enter your email</label>
            <input type="email" id="email" placeholder="cyntra_freya@gmail.com" required>

            <label for="password">Enter password</label>
            <input type="password" id="password" placeholder="********" required>

            <button type="submit">Sign in</button>
        </form>
        
        <div class="or-divider">
            <span>OR</span>
        </div>
        
        <button class="signup-button"><a href="/signup" style="text-decoration: none; color: black;">Sign up</a></button>
        
        <div class="forgot-password">
            <a href="/">Forgot your password?</a>
        </div>
    </div>
</div>