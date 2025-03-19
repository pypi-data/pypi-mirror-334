import os
import pathlib
import pathspec


class IgnoreHandler:
    def __init__(self, repo_path):
        """Initialize with the path to the repository, looking for both .gitignore and .r2pignore."""
        self.repo_path = pathlib.Path(repo_path).resolve()
        self.n_ignored = 0
        self.spec = self._read_ignores()

    def _read_ignores(self):
        """Read both .gitignore and .r2pignore files and return a compiled pathspec."""
        ignore_patterns = []

        for ignore_file in [".gitignore", ".r2pignore"]:
            ignore_file_path = self.repo_path / ignore_file
            if ignore_file_path.exists():
                with open(ignore_file_path, "r", encoding="utf-8") as f:
                    ignore_patterns.extend(f.readlines())

        return pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    def should_ignore(self, file_path):
        """Check if a file should be ignored based on .gitignore-style rules."""
        relative_path = os.path.relpath(file_path, self.repo_path)
        if self.spec.match_file(relative_path):
            self.n_ignored += 1
            return True
        return False
