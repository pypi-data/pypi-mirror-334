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

from setuptools import setup, find_packages

setup(
    # This empty setup.py enables editable installs
    # ("pip install -e .") with setuptools-based pyproject.toml
    # Actual configuration is in pyproject.toml
    # Dependencies are read from requirements.txt at build time
    name="ancile",
    dependencies=find_packages()
)
