# git2string
[![PyPI - Version](https://img.shields.io/pypi/v/git2string)](https://pypi.org/project/git2string/) ![PyPI - License](https://img.shields.io/pypi/l/git2string)

<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/hathibelagal-dev/git2string/refs/heads/main/assets/git2string.png" style="width:256px"/>
</div>

git2string is a powerful tool that simplifies the process of converting an entire Git repository into a single LLM-friendly text file, which is easy to upload. It also tells you how many tokens the text file will consume. So, it will hopefully be saving you a lot of time and effort.

It will automatically ignore all binary files. Additionally, it will respect your **.gitignore**. You can also create a **.r2pignore** file in your repo to specify the files that should be skipped for prompt generation.

## Installation

```
pip3 install git2string
```

## Usage

```
git2string <url of repository>
```

For example:

```
git2string https://github.com/mozilla/experimenter
```

The output would look like this:

```
ℹ Cloning repository to ./tmpohen963u
✔ Using tokenizer for model gpt2
Concatenating: 100%|██████████████████████| 3331/3331 [00:00<00:00, 7547.49it/s]
✔ All valid files have been concatenated into llm_prompt.txt
ℹ 21334492 tokens are present in the prompt
```

If you have cloned your desired repository already, you can just specify its path.

```
git2string <repo root directory>
```

By default, the prompt will be generated in a file called **llm_prompt.txt**. You can specify a different filename as follows:

```
git2string <repo root directory> --output-file <filename>
```

This tool uses OpenAI's tiktoken to count the number of tokens in the generated prompt. By default, gpt2's tokenizer will be used. But you can count tokens for most OpenAI models.

```
git2string <repo root directory> --openai-model <model name>
```

For example:

```
git2string /tmp/myrepo --openai-model gpt-4o
```
