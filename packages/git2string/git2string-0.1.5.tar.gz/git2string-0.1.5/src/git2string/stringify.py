from .concatenator import FileConcatenator
import tempfile

def stringify_git(repo: str, cleanup: bool = True):
    temp_file = tempfile.NamedTemporaryFile(delete=True, mode='w+t')
    c = FileConcatenator(repo, temp_file.name)
    c.concatenate()
    temp_file.seek(0)
    contents = temp_file.read()
    temp_file.close()
    if cleanup:
        c.cleanup()
    return contents