<script lang="ts">
    import Navbar from "$lib/Navbar.svelte";
    import { page } from "$app/stores";

</script>
<style>
    :root{
		--font-color: hsl(233, 8%, 79%);
        --text-color: hsl(236, 13%, 42%);
		--font: 'Inter', sans-serif;
        --button-color: hsl(5, 85%, 63%);
		
	}

	:global(body){
		
		margin: 0 auto;
		font-family: var(--font); 
		 
	}
     .main-container{
        width: 80%;
        margin: 0 auto;
        padding: 10px;

    }
</style>
{#if $page.url.pathname !== '/login' && $page.url.pathname !== '/signup'} 
    <Navbar />
{/if}

<div class="main-container">
        <slot/>
</div>  

