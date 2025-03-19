from git import Repo
import tempfile
from .console import Console
import shutil

class RepoDownloader:
    def __init__(self, repo_url, repo_path=None):
        self.repo_url = repo_url
        self.repo_path = repo_path

    def download_repo(self):
        console = Console()
        if self.repo_path is None:
            temp_dir = tempfile.mkdtemp(dir=".")
            self.repo_path = temp_dir
            self._created_temp_dir = True
        else:
            self._created_temp_dir = False

        console.print(f"ℹ Cloning repository to {self.repo_path}")
        Repo.clone_from(self.repo_url, self.repo_path)

    def get_repo(self):
        return Repo(self.repo_path)

    def get_repo_path(self):
        return self.repo_path

    def get_repo_url(self):
        return self.repo_url
    
    def cleanup(self):
        if self._created_temp_dir and self.repo_path:
            try:
                print("Removing temporary directory... " + self.repo_path)
                shutil.rmtree(self.repo_path)
                print(f"🧹 Removed temporary directory: {self.repo_path}")
            except OSError as e:
                print(f"⚠ Error removing temporary directory {self.repo_path}: {e}")
            finally:
                self.repo_path = None
                self._created_temp_dir = False
