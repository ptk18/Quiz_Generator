<script lang="ts">
    import { page } from "$app/stores";
    import { writable } from "svelte/store";
    import { userInfo } from "$lib/loginUserInfo";

    $: routeId = $page.route.id;
    
    const isNavOpen = writable(false);

    function toggleNav() {
        isNavOpen.update(n => !n);
    }

    let currentUser: { id: number | null; name: string; email: string; isLoggedIn: boolean };

    // Subscribe to the userInfo store
    userInfo.subscribe(value => {
        currentUser = value;
    });
</script>

<style>
    .nav-container {
        width: 80%;
        margin: 0 auto;
        padding: 10px;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    a img {
        width: 5rem;
    }
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    li {
        float: left;
    }
    li a {
        display: block;
        color: black;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        cursor: pointer;
    }
    li a:hover {
        color: var(--button-color);
    }
    button {
        border: none;
        background-color: transparent;
        cursor: pointer;
        padding-top: 15px;
    }
    .mobile-nav {
        display: none;
    }
    .active {
        color: var(--button-color);
    }
    @media (min-width: 300px) and (max-width: 600px) {
        .mobile-nav {
            display: block;
        }
        .desktop-nav > ul {
            display: none;
        }
        .mobile-nav > div {
            display: none;
        }
        .mobile-nav div.open {
            display: block;
            position: fixed;
            right: 0;
            top: 0;
            width: 250px;
            height: 100%;
            background: white;
            box-shadow: -1px 0 5px rgba(0,0,0,0.5);
            z-index: 1000;
        }
        
        .mobile-nav li {
            float: none;
            text-align: left;
        }
        .icon-style {
            display: flex;
            justify-content: flex-end;
            padding-left: 200px;
            padding-bottom: 25px;
            
        }
        img{
            width: 2.5rem;
        }
       
    }
</style>

<div class="nav-container">
    <div class="header">
        <div>
            <a href="/"><img src="/logo.png" alt="logo" /></a>
        </div>
        <div class="desktop-nav">
            <ul>
                <li><a class:active={routeId === "/"} href="/">Home</a></li>
                
                    {#if currentUser.isLoggedIn}
                        <li><a class:active={routeId === "/profile"} href="/profile">Profile</a></li>
                    {:else}
                        <li><a class:active={routeId === "/login"} href="/login">Login</a></li>
                    {/if}   
            </ul>
        </div>
        <div class="mobile-nav">
            <button on:click={toggleNav}>
                <img src={$isNavOpen ? "/icon-close.svg" : "/icon-menu.png"} alt="nav icon" />
            </button>
            <div class:open={$isNavOpen}>
                <button on:click={toggleNav} class="icon-style">
                    <img src="/icon-menu-close.png" alt="nav close icon" />
                </button>
                <ul>
                    <li><a class:active={routeId === "/"} href="/">Home</a></li>
                    <li><a class:active={routeId === "/login"} href="/login">
                    {#if currentUser.isLoggedIn}
                        Profile
                    {:else}
                        Login
                    {/if}</a></li>  
                </ul>
            </div>
        </div>
    </div>
</div>




