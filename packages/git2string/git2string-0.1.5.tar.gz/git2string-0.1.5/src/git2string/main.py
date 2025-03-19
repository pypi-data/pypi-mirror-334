import argparse
from git2string.concatenator import FileConcatenator
from git2string.console import Console


def main():
    console = Console()
    parser = argparse.ArgumentParser(
        description="Concatenate all files of a Git repo into a single prompt."
    )
    parser.add_argument("repo_location", help="Location of the repository")
    parser.add_argument(
        "--include-binary",
        action="store_true",
        help="Include binary files in concatenation",
    )
    parser.add_argument(
        "--only-dir",
        default="",
        help="Only include files in this directory in concatenation",
    )
    parser.add_argument(
        "--output-file", default="llm_prompt.txt", help="Name of the output file"
    )
    parser.add_argument(
        "--openai-model",
        default="gpt2",
        help="Name of OpenAI model whose tokenizer to use",
    )
    parser.add_argument(
        "--output-encoding", default="utf-8", help="Encoding for output file"
    )

    args = parser.parse_args()

    concatenator = FileConcatenator(
        args.repo_location,
        args.output_file,
        args.include_binary,
        args.output_encoding,
        model=args.openai_model,
        only_dir=args.only_dir,
    )
    _, n_ignored, n_tokens, n_errors = concatenator.concatenate()
    console.print_success(
        f"✔ All valid files have been concatenated into {args.output_file}"
    )
    if n_ignored > 0:
        console.print_success(
            f"✔ {n_ignored} files were ignored due to .gitignore or .r2pignore rules"
        )
    console.print_success(f"ℹ {n_tokens} tokens are present in the prompt")
    if n_tokens > 128000:
        console.print_warning("WARNING: The prompt is longer than 128,000 tokens.")
    if n_errors > 0:
        console.print_warning(f"WARNING: {n_errors} files could not be read.")

if __name__ == "__main__":
    main()
