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

# src/ancile/output_service.py
from typing import List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

from .contributing import display_contributing
from .risk_analyzer import RiskLevel, RiskAnalyzer


class OutputService:
    def __init__(self, console: Optional[Console] = None):
        # Custom theme for risk levels
        theme = Theme({"low": "green", "medium": "yellow", "high": "red bold", "info": "cyan", "file": "blue"})
        self.console = console or Console(theme=theme)
        self.risk_analyzer = None

    def set_risk_analyzer(self, risk_analyzer: RiskAnalyzer) -> None:
        self.risk_analyzer = risk_analyzer

    def display_assessment_results(
        self,
        verbose: bool,
        project_name: str,
        risk_level: RiskLevel,
        changed_files: List[str],
        from_tag: str,
        to_tag: str,
    ) -> None:
        if not verbose:
            self.console.print("\n")

        # Display project title
        self.console.print(Panel.fit(f"[bold cyan]Project: {project_name}[/bold cyan]", style="bold magenta"))

        # Header
        self.console.print(Panel(f"[info]Risk Assessment: [/info]{from_tag} → {to_tag}", expand=False))

        # Risk Level
        risk_style = risk_level.name.lower()
        self.console.print(Panel(f"🎯 Overall Risk: [{risk_style}]{risk_level.name}[/{risk_style}]", expand=False))

        # Changed Files Table
        if verbose:
            table = Table(show_header=True, header_style="bold")
            table.add_column("File", style="file")
            table.add_column("Risk Level")

            for file in changed_files:
                file_risk = self.risk_analyzer.get_file_risk(file)
                table.add_row(file, f"{file_risk}")

            self.console.print("\n📁 Changed Files:")
            self.console.print(table)

        self.console.print("\n")

    def display_error(self, message: str) -> None:
        self.console.print(f"[red]Error: {message}[/red]")

    def display_warning(self, message: str) -> None:
        self.console.print(f"[yellow]Warning: {message}[/yellow]")

    def display_config(self, config: dict) -> None:
        self.console.print("\n⚙️ Risk Configuration:")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Path")
        table.add_column("Risk Level")

        for path, risk in config.items():
            risk_level = risk.name if hasattr(risk, "name") else risk
            table.add_row(path, f"{risk_level}")

        self.console.print(table)

    def print_license_notice(self):
        self.console.print(
            """
        ancile  Copyright (C) 2025 Leading Works SàRL
        This program comes with ABSOLUTELY NO WARRANTY; for details type `ancile --license'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; type `ancile --contributing' for details.
        """
        )

    @staticmethod
    def display_contributing() -> None:
        display_contributing()

    def display_content(self, content: str) -> None:
        self.console.print(content)
