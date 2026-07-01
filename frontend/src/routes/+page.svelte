<!-- <svelte:options runes={true} /> -->
<script lang="ts">
    // import { enhance } from '$app/forms';

    import { Icon } from 'svelte-icons-pack';
    import { FaSolidArrowRightLong } from "svelte-icons-pack/fa";
    import { FaSolidSpinner } from "svelte-icons-pack/fa";
    import { LuClipboardCopy } from "svelte-icons-pack/lu";


    // let vars in ts: user_input_topic/specialization field, user_input_catalyst, & user_input_text_length ...to be used as svelte state vars for conditional html elements
    let userInputTopic: string = $state('');
    let userInputCatalyst: string = $state('');
    let userInputTextLength: number | undefined = $state(undefined);

    let formSubmittedBool: boolean = $state(false);
    let generatedOutputText: string = $state('');

    // useful helper states to keep the html clean
    let isInputCatalystDisabled: boolean = $derived(userInputTopic.trim() === '');
    let isInputTextLengthDisabled: boolean = $derived(isInputCatalystDisabled || userInputCatalyst.trim() === '');

    let textGenerationIsLoading: boolean = $derived(formSubmittedBool);


    // functions

    function copyToClipboard () : void {
        navigator.clipboard.writeText(generatedOutputText);
    }

    async function handleFormSubmit (event: SubmitEvent) : Promise<void> {

        try {
            event.preventDefault();
            formSubmittedBool = true;
    
            const response = await fetch('http://localhost:5000/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: userInputTopic,
                    catalyst: userInputCatalyst,
                    textLength: userInputTextLength
                })
            });
    
            const data = await response.json();
            generatedOutputText = data.generated_text;
            formSubmittedBool = false;
        }
        catch (error) {
            formSubmittedBool = false;
            generatedOutputText = 'Failed to generate text. Please try again.';
        }
    }

</script>




<div class="flex flex-col justify-center items-center mt-6">
    <h1 class="text-3xl font-bold text-indigo-300 mb-12">Domain Text Generator</h1>

    <div class="flex items-center gap-x-10 mb-10">
        <form class="flex flex-col items-end gap-y-6" id="userInputForm" action="" onsubmit={handleFormSubmit}>

            <div class="flex items-center gap-x-2">
                <label class="text-neutral-300" for="userInputTopicInputTag">Enter a word or phrase that the generated text should be about: </label>
                <input class="bg-neutral-600 border-2 border-cyan-500 rounded px-3 py-2 text-white placeholder-neutral-300 disabled:opacity-50" id="userInputTopicInputTag" name="userInputTopic" type="text" bind:value={userInputTopic} placeholder="(e.g. cryonics)" required />
            </div>

            <div class="flex items-center gap-x-2">
                <label class="text-neutral-300" for="userInputCatalystInputTag">Enter two words to catalyze text generation: </label>
                <input class="bg-neutral-600 border-2 border-cyan-500 rounded px-3 py-2 text-white placeholder-neutral-300 disabled:opacity-50" id="userInputCatalystInputTag" name="userInputCatalyst" type="text" bind:value={userInputCatalyst} placeholder="(e.g. Cryogenic preservation)" disabled={isInputCatalystDisabled} required />
            </div>
            
            <div class="flex items-center gap-x-2">
                <label class="text-neutral-300" for="userInputTextLengthInputTag">Enter the number of words you would like in your generated text: </label>
                <input class="bg-neutral-600 border-2 border-cyan-500 rounded px-3 py-2 text-white placeholder-neutral-300 disabled:opacity-50" id="userInputTextLengthInputTag" name="userInputTextLength" type="number" bind:value={userInputTextLength} placeholder="(i.e. more than 1)" disabled={isInputTextLengthDisabled} required />
            </div>
            
        </form>
        
        <div class="flex flex-col items-center gap-y-4">
            <button class="btn btn-indigo cursor-pointer" form="userInputForm" type="submit" value="Submit Form">Generate Output Text</button>
            
            <Icon src={FaSolidArrowRightLong} size="48" />
        </div>

        <div class="flex flex-col justify-center items-center">
            {#if textGenerationIsLoading}
                <div class="spinning">
                    <Icon src={FaSolidSpinner} />
                </div>
            {:else if generatedOutputText !== ''}
                <p class="font-bold text-xl text-cyan-400">Text Generation Complete: Output Below</p>
            {:else}
                <p class="font-bold text-lg text-cyan-400">(Finish submitting form)</p>
            {/if}
        </div>
    </div>
    

    <div class="bg-neutral-700 border-4 border-indigo-700 text-white p-4 rounded-lg  w-3/4 h-80 max-h-80 overflow-y-auto relative">
        <button class="absolute top-2 right-2 cursor-pointer" onclick={copyToClipboard}>
            <Icon src={LuClipboardCopy} />
        </button>
        {#if generatedOutputText !== ''}
            <p>{generatedOutputText}</p>
        {:else}
            <p class="text-neutral-400 italic">Text will be output here...</p>
        {/if}
    </div>

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