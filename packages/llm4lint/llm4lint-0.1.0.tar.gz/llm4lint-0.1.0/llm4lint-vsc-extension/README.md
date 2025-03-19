# llm4lint-vsc

A Static Analysis Tool built by finetuning Qwen2.5 Coder using unsloth. Trained only for python files (For now, You can extend it with your own data if you want).

## Features

- Adds 2 additional menu items when you right click a python file
    - Linting of Python source code, highlights problematic parts of the code 
    - Lint in interactive mode, talk to the model locally.

Right click on a Python file
![menu](assets/menu.png)

Example code

![sample_code](assets/sample_code.png)

![output](assets/output.png)

- You can also provide your own data to create a different model (use train.py script):
[training script and augmentation script](https://github.com/ahmedhus22/llm4lint.git)
    - Specify your own examples in a csv file with input and output columns.
    output should be `<lineno> - <type>: <issue>`. With just 1 example multiple datapoints are created using augmentation.
    - Augmentation of inputs: 
        - Variable names are replaced with different names to make sure model does not memorize the code.
        - Additional code is added before and after your input example. (outputs are also adjusted to account for lineno changes).
- Dataset created using this script: https://huggingface.co/datasets/ahmedhus22/python-static-analysis-linting

## Requirements

- Download the fine-tuned model from [Hugging Face](https://huggingface.co/ahmedhus22/llm4lint-7B-Qwen2.5Coder/tree/main) .gguf and Modelfile

- Create ollama Model
```
ollama create llm4lint7b -f <Modelfile-Path>
```

For Interactive mode, you need to install llm4lint cli-tool:
```
pip install llm4lint
```


## Known Issues

- If the output of the linter is not satisfactory, simply rerun it. It will give a different output (most likely, its not deterministic).
- Or prepare your own examples using the [training script and augmentation script](https://github.com/ahmedhus22/llm4lint.git)

<!-- ## Release Notes

Users appreciate release notes as you update your extension.

### 1.0.0

Initial release of ...

### 1.0.1

Fixed issue #.

### 1.1.0

Added features X, Y, and Z.

---

## Following extension guidelines

Ensure that you've read through the extensions guidelines and follow the best practices for creating your extension.

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines) -->
<!-- 
## Working with Markdown

You can author your README using Visual Studio Code. Here are some useful editor keyboard shortcuts:

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux).
* Toggle preview (`Shift+Cmd+V` on macOS or `Shift+Ctrl+V` on Windows and Linux).
* Press `Ctrl+Space` (Windows, Linux, macOS) to see a list of Markdown snippets. -->

<!-- ## For more information

* [Visual Studio Code's Markdown Support](http://code.visualstudio.com/docs/languages/markdown)
* [Markdown Syntax Reference](https://help.github.com/articles/markdown-basics/)

**Enjoy!** -->
