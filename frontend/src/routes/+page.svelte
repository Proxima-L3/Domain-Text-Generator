<!-- <svelte:options runes={true} /> -->
<script lang="ts">
    // insert any necessary ts here

    import { enhance } from '$app/forms';

    import { Icon } from 'svelte-icons-pack';
    import { BsArrowRight } from 'svelte-icons-pack/bs';
    import { FaSolidArrowRightLong } from "svelte-icons-pack/fa";
    import { FaSolidSpinner } from "svelte-icons-pack/fa";

    // let vars in ts: user_input_topic/specialization field, user_input_catalyst, & user_input_text_length ...to be used as svelte state vars for conditional html elements

    let userInputTopic: string = $state('');
    let userInputCatalyst: string = $state('');
    let userInputTextLength: number | undefined = $state(undefined);

    let formSubmittedBool: boolean = $state(false);

    // useful helper states to keep the html clean
    let isInputCatalystDisabled: boolean = $derived(userInputTopic.trim() === '');
    let isInputTextLengthDisabled: boolean = $derived(isInputCatalystDisabled || userInputCatalyst.trim() === '');

    let textGenerationIsLoading: boolean = $derived(formSubmittedBool);

    
    // not sure the use of below var declaration yet
    let { form } = $props();

</script>




<!-- the body of the svelte page goes here. no need for a single parent/wrapper element. -->


<!-- <h1>Welcome to SvelteKit</h1> -->
<!-- <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p> -->

<br>

<div class="parentPageContentDiv">
    <form action="" method="POST" use:enhance>
        <label for="userInputTopicInputTag">Enter a word or phrase that the generated text should be about: </label>
        <input id="userInputTopicInputTag" name="userInputTopic" type="text" bind:value={userInputTopic} placeholder="(e.g. cryonics)" required />
    
        <label for="userInputCatalystInputTag">Enter two words to catalyze text generation: </label>
        <input id="userInputCatalystInputTag" name="userInputCatalyst" type="text" bind:value={userInputCatalyst} placeholder="(e.g. Cryogenic preservation)" disabled={isInputCatalystDisabled} required />
    
        <label for="userInputTextLengthInputTag">Enter the number of words you would like in your generated text: </label>
        <input id="userInputTextLengthInputTag" name="userInputTextLength" type="number" bind:value={userInputTextLength} placeholder="(i.e. more than 1)" disabled={isInputTextLengthDisabled} required />
        
        <!-- <label for="generateTextOutputBtn">Generate Output Text</label> -->
        <button class="btn btn-indigo" id="generateTextOutputBtn" type="submit" value="Submit Form">Generate Output Text</button>
    </form>

    <!-- <Icon src={BsArrowRight} /> -->
    <Icon src={FaSolidArrowRightLong} />

    {#if textGenerationIsLoading}
        <div class="spinning">
            <Icon src={FaSolidSpinner} />
        </div>
    {:else if form}
        <p class="" class:error={!form.success}>Text Generation Complete: Output Below</p>
    {:else}
        <p class="">(Finish submitting form)</p>
    {/if}

</div>




<style>
    /* insert any customizations to an element's tailwind css styling (that is too long for inline declaration) here */

    @reference './layout.css';
    /* .parentPageContentDiv {
        background-color: #242424;
    } */

    .btn {
      @apply font-bold py-2 px-4 rounded-full;
    }
    .btn-indigo {
      @apply bg-indigo-700 text-white;
    }
    .btn-indigo:hover {
      @apply bg-indigo-600;
    }

    .spinning {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

</style>