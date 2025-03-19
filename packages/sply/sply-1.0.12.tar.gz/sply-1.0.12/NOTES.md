# Notes

## Table of Contents

- [Using "sply_chat_interact.py"](#using-sply_chat_interactpy)
- [Best-working models](#best-working-models)
- [Generally working models](#generally-working-models)
- [Non-working models](#non-working-models)
- [On reasoning models](#on-reasoning-models)
- [Dealing with incorrect output](#dealing-with-incorrect-output)
- [Misc](#misc)

## Using "sply_chat_interact.py"
  * Run "sply_chat_interact.py --help" for command line options and defaults
  * Enter "/h" at the input prompt ("> ") for help
  * Hit Ctrl-C to interrupt generation and enter input mode

## Best-working models
  * [qwen2.5-coder-14b-instruct-q8_0.gguf](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-GGUF/blob/main/qwen2.5-coder-14b-instruct-q8_0.gguf)
    - Base-line for general testing; if something doesn't work, it's taken to be the library's fault
  * [QwQ-Snowdrop.i1-IQ3_XXS.gguf](https://huggingface.co/mradermacher/QwQ-Snowdrop-i1-GGUF/blob/main/QwQ-Snowdrop.i1-IQ3_XXS.gguf)
    - Base-line for reasoning testing


## Generally working models
  * [ibm-granite_granite-3.2-8b-instruct-Q8_0.gguf](https://huggingface.co/bartowski/ibm-granite_granite-3.2-8b-instruct-GGUF/blob/main/ibm-granite_granite-3.2-8b-instruct-Q8_0.gguf)
  * [Marco-o1-Q8_0.gguf](https://huggingface.co/bartowski/Marco-o1-GGUF/blob/main/Marco-o1-Q8_0.gguf)
  * [phi-4-abliterated.Q8_0.gguf](https://huggingface.co/mradermacher/phi-4-abliterated-GGUF/blob/main/phi-4-abliterated.Q8_0.gguf)
  * [huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-IQ4_XS.gguf](https://huggingface.co/bartowski/huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-GGUF/blob/main/huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-IQ4_XS.gguf)
  * [gemma-3-12b-it-Q8_0.gguf](https://huggingface.co/ggml-org/gemma-3-12b-it-GGUF/blob/main/gemma-3-12b-it-Q8_0.gguf)

## Non-working models
  * [Mistral-Small-24B-Instruct-2501-Q5_K_M.gguf](https://huggingface.co/bartowski/Mistral-Small-24B-Instruct-2501-GGUF/blob/main/Mistral-Small-24B-Instruct-2501-Q5_K_M.gguf)
    - Currently generates _a lot_ of simulated python errors

## Dealing with incorrect output
  * Try a different model - see the [best-working models list](#best-working-models)
  * Modify the prompt to show examples of expected behavior
  * Try a lower temperature value
  * Try an alternate seed number
  * Reuse a working model/prompt/seed combo
  * When all else fails, Ctrl-C + "edit_prompt()" are your friends

## Misc
  * The above model lists are very subject to change
  * The default prompt editor is "vim -b" - customize with the "editor=" options and parameters
  * "prompt_file=" args always have precedence over "prompt=" args
  * "edit_prompt" currently leaves prompt tempfiles intact (for manual review)
  * "make_prompt" is jailbroken - modify to taste, or provide a custom prompt

