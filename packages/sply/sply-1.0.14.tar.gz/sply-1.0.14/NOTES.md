# Notes

## Table of Contents

- [Using "sply_chat_interact.py"](#using-sply_chat_interactpy)
- [Tested models](#tested-models)
- [Dealing with incorrect output](#dealing-with-incorrect-output)
- [Misc](#misc)

## Using "sply_chat_interact.py"
  * Run "sply_chat_interact.py --help" for command line options and defaults
  * Enter "/h" at the input prompt ("> ") for help
  * Hit Ctrl-C to interrupt generation and enter input mode

## Tested models
  * agentica-org_DeepScaleR-1.5B-Preview-Q4_0.gguf
    - sha256sum 32ebacb157e5a2e2c8be00829160c2c6ccf69e2753aabcfc6fc942839636c950
    - Currently rambles too much to get predictable output
  * Blabbertron-1.2.i1-Q4_0.gguf
    - sha256sum 18dc24a96e1b5cab6b614e6a4ec497ba1013ad20c33bb616c39d952af8e8ff6f
  * DeepSeek-R1-Distill-Qwen-14B-Q4_0.gguf
    - sha256sum 906b3382f2680f4ce845459b4a122e904002b075238080307586bcffcde49eef
    - Currently rambles too much to get predictable output
  * DRT-o1-14B-Q4_0.gguf
    - sha256sum b3c53bf7c4e958950598cf5cff722db97605c585b402a6a6860b56fadd51c88d
    - Currently doesn't \<think\> enough
  * google_gemma-3-12b-it-Q4_0.gguf
    - sha256sum 9a7b70be8727da9fb28523b35946dd42d4fe0f622cce03daa44fccff0775516d
  * huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-Q4_0.gguf
    - sha256sum 165086808981b1f449c232aff7d2f7c610ef15a665f085a52fe25fcf0c787963
    - Currently generates simulated python errors
  * ibm-granite_granite-3.2-8b-instruct-Q4_0.gguf
    - sha256sum 9115cddcad150f908b402072dafe860ce41b35e83613bfbdc7c0dce4afb04bc8
    - Currently generates simulated python errors
  * Marco-o1-Q4_0.gguf
    - sha256sum 71fe2bef6ffea98a2e315b865337474c3c99c00564df65b14dd7741bdb1e9daa
  * NousResearch_DeepHermes-3-Llama-3-3B-Preview-Q4_0.gguf
    - sha256sum 4b2473f0441778aef773fe421c0aa58fef44c9e14ae4423904df0540572a9183
    - Currently rambles too much to get predictable output
  * OpenPipe_Deductive-Reasoning-Qwen-14B-Q4_0.gguf
    - sha256sum e9a173c4eaea59649940dfdd4b69cfc2c52ab47d308f747f165d693198646897
    - Currently doesn't \<think\> enough
  * phi-4-Q4_0.gguf
    - sha256sum 7c3e1b5bfb03bb4b13cf7ff4889676c5ad4ea92049352d8e1ded3f443f9b68c6
    - Currently tends to generate unwanted markdown code blocks, multiple string results, etc.
  * qwen2.5-coder-14b-instruct-q4_0.gguf
    - sha256sum 561c8955089ad330dff56a40a001eb8bb4e12746354e76d0262bd65ab4640864
    - Base-line for general testing; if something doesn't work, it's taken to be the library's fault
  * QwQ-Snowdrop.i1-IQ3_XXS.gguf
    - sha256sum 6f08d96e128caa67d48ccd6438aa6fd130fb866ce1ba5ed77269b55a42676bf8
    - Currently rambles endlessly without QwQ specific settings - see [this article](https://docs.unsloth.ai/basics/tutorial-how-to-run-qwq-32b-effectively)
  * RekaAI_reka-flash-3-Q4_0.gguf
    - sha256sum 8fa4f55937c4ea0c968e5c9cc3b4770f4f6e080651eb714c28eddc9d2bdec6ca
  * SicariusSicariiStuff_Phi-Line_14B-Q4_0.gguf
    - sha256sum eea06466ab2c7ce9d01498e8741da792d610b632299bb3fcea139669dad02422
    - Currently rambles too much to get predictable output

## Dealing with incorrect output
  * Try a different model - see the [tested models list](#tested-models)
  * Modify the prompt to show examples of expected behavior
  * Try a lower temperature value
  * Try an alternate seed number
  * Reuse a working model/prompt/seed combo
  * When all else fails, Ctrl-C + "edit_prompt()" are your friends

## Misc
  * The tested model list is very subject to change
  * The default prompt editor is "vim -b" - customize with the "editor=" options and parameters
  * "prompt_file=" args always have precedence over "prompt=" args
  * "edit_prompt" currently leaves prompt tempfiles intact (for manual review)
  * "make_prompt" is jailbroken - modify to taste, or provide a custom prompt

