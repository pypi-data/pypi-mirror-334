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

# tests/test_output_service.py
from unittest.mock import Mock

import pytest
from rich.console import Console

from ancile.output_service import OutputService
from ancile.risk_analyzer import RiskAnalyzer, RiskLevel


@pytest.fixture
def mock_console():
    return Mock(spec=Console)


@pytest.fixture
def mock_analyzer():
    mock = Mock(spec=RiskAnalyzer)
    mock.get_file_risk.return_value = RiskLevel.HIGH
    return mock


@pytest.fixture
def output_service(mock_console):
    return OutputService(console=mock_console)


def test_display_assessment_results(output_service, mock_analyzer):
    output_service.set_risk_analyzer(mock_analyzer)
    output_service.display_assessment_results(
        verbose=True,
        project_name="Ancile",
        risk_level=RiskLevel.HIGH,
        changed_files=["file1.py", "file2.py"],
        from_tag="v1.0.0",
        to_tag="v1.0.1",
    )
    # Assert console.print was called
    assert output_service.console.print.called


def test_display_error(output_service):
    output_service.display_error("Test error")
    output_service.console.print.assert_called_with("[red]Error: Test error[/red]")


def test_display_config(output_service):
    config = {"/src/core": RiskLevel.HIGH, "/docs": RiskLevel.LOW}
    output_service.display_config(config)
    assert output_service.console.print.called
