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

from typing import List

# src/ancile/git_service.py
from git import Repo


def _get_project_name(self) -> str:
    try:
        # Retrieve the project name from the Git repository configuration
        return self.repo.remotes.origin.url.split("/")[-1].replace(".git", "")
    except Exception as e:
        print(f"Error retrieving project name: {str(e)}")
        return "unknown"


class GitService:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
        self.project_name = _get_project_name(self)
        self.diff_index = None

    def get_changed_files(self, from_tag: str, to_tag: str) -> List[str]:
        try:
            # Get the commit objects that the tags point to
            from_commit = self.repo.tags[from_tag].commit
            to_commit = self.repo.tags[to_tag].commit

            # Get the diff between the commits
            diff_index = from_commit.diff(to_commit)

            # Extract the changed file paths
            return [diff.a_path for diff in diff_index]
        except Exception as e:
            raise ValueError(f"Error comparing tags: {str(e)}")

    def get_project_name(self):
        return self.project_name
