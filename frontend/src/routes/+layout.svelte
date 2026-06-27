<!-- you would put stuff like a navbar, footer, or sidebar in this. this file is for stuff that shows on all pages (it acts as a wrapper for the rest of the child svelte pages) -->


<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
