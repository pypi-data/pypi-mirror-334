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

# tests/test_risk_analyzer.py
import pytest

from ancile.risk_analyzer import RiskAnalyzer, RiskLevel


@pytest.fixture
def risk_mappings():
    return {
        "/src/core": RiskLevel.HIGH,
        "/src/api": RiskLevel.HIGH,
        "/src/persistence": RiskLevel.HIGH,
        "/src/ui/services": RiskLevel.MEDIUM,
        "/src/ui/containers": RiskLevel.LOW,
        "/src/ui/components": RiskLevel.LOW,
        "/docs": RiskLevel.LOW,
        "/tests": RiskLevel.LOW,
    }


def test_assess_risk_low(risk_mappings):
    analyzer = RiskAnalyzer(risk_mappings)
    changed_files = ["/docs/README.md", "/tests/test_feature.py"]
    assert analyzer.assess_risk(debug=False, verbose=True, changed_files=changed_files) == RiskLevel.LOW


def test_assess_risk_medium(risk_mappings):
    analyzer = RiskAnalyzer(risk_mappings)
    changed_files = ["/src/ui/services/resources.services.ts"]
    assert analyzer.assess_risk(debug=False, verbose=True, changed_files=changed_files) == RiskLevel.MEDIUM


def test_assess_risk_high(risk_mappings):
    analyzer = RiskAnalyzer(risk_mappings)
    changed_files = ["/src/core/critical_service.py", "/docs/README.md"]
    assert analyzer.assess_risk(debug=False, verbose=False, changed_files=changed_files) == RiskLevel.HIGH


def test_unknown_path_defaults_to_low(risk_mappings):
    analyzer = RiskAnalyzer(risk_mappings)
    changed_files = ["/unknown/path/file.txt"]
    assert analyzer.assess_risk(debug=False, verbose=False, changed_files=changed_files) == RiskLevel.LOW
