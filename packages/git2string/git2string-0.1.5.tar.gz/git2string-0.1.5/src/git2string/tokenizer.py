import tiktoken
from .console import Console


class Tokenizer:
    def __init__(self, model_name="gpt2", file_path="llm_prompt.txt"):
        """Initialize tokenizer"""
        console = Console()
        try:
            self.tokenizer = tiktoken.encoding_for_model(model_name)
            console.print(f"✔ Using tokenizer for model {model_name}")
        except:
            console.print_warning(
                f"WARNING: Model {model_name} not found. Defaulting to gpt2."
            )
            self.tokenizer = tiktoken.encoding_for_model("gpt2")
        self.file_path = file_path
        self.tokens = None

    def _tokenize(self):
        """Tokenize the input file"""
        with open(self.file_path, "r", encoding="utf-8") as infile:
            text = infile.read()
            self.tokens = self.tokenizer.encode(text, disallowed_special=())

    def count_tokens(self):
        """Count the number of tokens"""
        self._tokenize()
        return len(self.tokens)
