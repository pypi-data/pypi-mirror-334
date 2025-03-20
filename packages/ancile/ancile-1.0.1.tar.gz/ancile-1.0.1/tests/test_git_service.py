# Ancile is a release risk assessment tool that analyzes differences between Git tags and evaluates changes based on configurable risk categories
# Copyright (C) 2025 Leading Works SàRL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# tests/test_git_service.py
import pytest
import os
import tempfile
from git import Repo
from ancile.git_service import GitService


@pytest.fixture
def git_repo():
    """
    Create a temporary Git repository.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repo.init(temp_dir)
        repo.create_remote("origin", "https://git.leading.works/ancile.git")
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write("This is a test repository.")
        repo.index.add(["README.md"])
        repo.index.commit("Initial commit")
        repo.create_tag("v1.0.0")
        src_core_dir = os.path.join(temp_dir, "src", "core")
        os.makedirs(src_core_dir, exist_ok=True)
        app_file_path = os.path.join(src_core_dir, "application.py")
        with open(app_file_path, "w") as f:
            f.write("class Application: ...")
        repo.git.add(["./src/core/application.py"])
        repo.git.commit("-m", "Add application class")
        repo.create_tag("v1.0.1")
        yield temp_dir


def test_get_changed_files_between_tags(git_repo):
    git_service = GitService(repo_path=git_repo)
    changed_files = git_service.get_changed_files("v1.0.0", "v1.0.1")
    assert isinstance(changed_files, list)
    assert changed_files[0] == "src/core/application.py"
    assert all(isinstance(file, str) for file in changed_files)


def test_invalid_tag_raises_error(git_repo):
    git_service = GitService(repo_path=git_repo)
    with pytest.raises(ValueError):
        git_service.get_changed_files("invalid-tag", "v1.0.1")
