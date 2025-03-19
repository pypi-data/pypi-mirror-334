import pytest
import tempfile
import os
from unittest.mock import patch
from git2string.console import Console
from git2string.file_handler import FileHandler
from git2string.repo_downloader import RepoDownloader
from git2string.concatenator import FileConcatenator
from git2string.tokenizer import Tokenizer

def test_console_print(capsys):
    console = Console()
    console.print("This is a simple print!")
    captured = capsys.readouterr()
    assert "This is a simple print!" in captured.out

def test_console_error(capsys):
    console = Console()
    console.print_error("This is an error message")
    captured = capsys.readouterr()
    assert "This is an error message" in captured.out

def test_read_file():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write("just some random text")
        temp_file_path = temp_file.name

    file_handler = FileHandler()
    content = file_handler.read_file(temp_file_path)
    assert content == "just some random text"
    os.remove(temp_file_path)

def test_is_binary():
    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_file:
        temp_file.write(b"\x00\x01\x02")
        temp_file_path = temp_file.name

    assert FileHandler.is_binary(temp_file_path) is True
    os.remove(temp_file_path)

@patch("git2string.repo_downloader.Repo.clone_from")
def test_repo_download(mock_clone):
    downloader = RepoDownloader("https://github.com/example/repo.git", "/fake/path")
    downloader.download_repo()
    mock_clone.assert_called_once_with("https://github.com/example/repo.git", "/fake/path")

def test_concatenation():
    with tempfile.TemporaryDirectory() as repo_dir:
        file1_path = os.path.join(repo_dir, "file1.txt")
        with open(file1_path, "w", encoding="utf-8") as f:
            f.write("File 1 contents")

        output_path = os.path.join(repo_dir, "output.txt")
        concatenator = FileConcatenator(repo_dir, output_path)
        total_files, ignored, tokens, errors = concatenator.concatenate()

        with open(output_path, "r", encoding="utf-8") as f:
            output_content = f.read()

    assert total_files == 1
    assert ignored == 0
    assert "File 1 contents" in output_content

def test_tokenizer_initialization():
    tokenizer = Tokenizer(model_name="gpt2", file_path="test.txt")
    assert tokenizer.tokenizer is not None

def test_tokenizer_count_tokens():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write("This is a test sentence.")
        temp_file_path = temp_file.name

    tokenizer = Tokenizer(model_name="gpt2", file_path=temp_file_path)
    token_count = tokenizer.count_tokens()
    assert token_count > 0
    os.remove(temp_file_path)
