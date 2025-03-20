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

# src/ancile/risk_analyzer.py
from enum import Enum
from pathlib import Path
from typing import Dict, List

import yaml


class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def _parse_risk(risk: str) -> RiskLevel:
    match risk.upper():
        case 'LOW':
            return RiskLevel.LOW
        case 'HIGH':
            return RiskLevel.HIGH
        case 'MEDIUM':
            return RiskLevel.MEDIUM
        case _:
            return RiskLevel.LOW


def generate_default_config(output_file: str):
    """Generate a default risk mapping configuration file."""
    default_config = {
        "mappings": [
            {
                "folder": "CHANGELOG.md",
                "risk": "LOW"
            },
            {
                "folder": "/docs",
                "risk": "LOW"
            },
            {
                "folder": "/tests",
                "risk": "LOW"
            },
            {
                "folder": "/src/core",
                "risk": "HIGH"
            },
            {
                "folder": "/src/api",
                "risk": "HIGH"
            },
            {
                "folder": "/src/frontend",
                "risk": "MEDIUM"
            },
            {
                "folder": "/src",
                "risk": "LOW"
            }
        ]
    }

    with open(output_file, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)


class RiskAnalyzer:
    def __init__(self, risk_mappings: Dict[str, RiskLevel]):
        self.risk_mappings = risk_mappings
        self.risk_by_file = {}

    def assess_risk(self, debug: bool, verbose: bool, changed_files: List[str]) -> RiskLevel:
        highest_risk = RiskLevel.LOW

        for file_path in changed_files:
            path = Path(file_path)
            file_risk = self._get_risk_for_path(verbose, path)
            self.risk_by_file[file_path] = file_risk
            if debug:
                print(f"{file_path}: {file_risk}")
            if file_risk.value > highest_risk.value:
                highest_risk = file_risk

        return highest_risk

    def get_file_risk(self, path: Path) -> RiskLevel:
        return self.risk_by_file.get(str(path), RiskLevel.MEDIUM)

    def _get_risk_for_path(self, verbose: bool, path: Path) -> RiskLevel:
        for folder, risk in self.risk_mappings.items():
            needle = str(path).lstrip('/')
            haystack = folder.lstrip('/')
            if verbose:
                print(f"Searching for {needle} in {haystack}")
            if needle.startswith(haystack):
                if verbose:
                    print(f"Found mapping for {path}: {risk}")
                if isinstance(risk, str):
                    return _parse_risk(risk)
                else:
                    return risk
        if verbose:
            print(f"No mapping found for {path}")
        return RiskLevel.LOW
