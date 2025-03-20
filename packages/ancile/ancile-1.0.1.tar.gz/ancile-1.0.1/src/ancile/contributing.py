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

# src/ancile/contributing.py
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

PROJECT_NAME = "ancile"
CMD = "ancile"
REPO_URL = "https://gitlab.com/leading-works/floss/ancile.git"


def display_contributing():
    # Header
    console.print(f"\n[bold cyan]CONTRIBUTING TO {PROJECT_NAME}[/bold cyan]", justify="center")
    console.print("[dim]A GPL-3.0-only licensed project[/dim]", justify="center")
    console.print("\n")

    # Free Software Statement Panel
    free_software_text = f"""
    This is free software, and you are welcome to redistribute it under certain conditions; see the GNU General Public License version 3.0 for details.
    To show the conditions (type [bold yellow]'{CMD} --contributing'[/bold yellow] for details), please refer to the CONDITIONS section below or see the full license text in the LICENSE file included with this project.
    """
    console.print(Panel(free_software_text, title="Free Software", border_style="green"))

    conditions = """
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    """
    console.print(Panel(conditions, title="Conditions", border_style="yellow", expand=False))

    # Main content
    console.print("\n[bold green]How to Contribute[/bold green]")

    # Code of Conduct
    conduct = Text.from_markup(
        "Contributors are expected to be respectful and considerate of others. "
        "We aim to foster an open and welcoming environment."
    )
    console.print(Panel(conduct, title="Code of Conduct", border_style="blue", expand=False))

    # Getting Started
    console.print("[bold]Getting Started[/bold]")
    steps = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    steps.add_column("Step", style="cyan")
    steps.add_column("Description")
    steps.add_row("1", "Fork the repository")
    steps.add_row("2", f"Clone your fork: [bold green]git clone {REPO_URL}[/bold green]")
    steps.add_row("3", "Create a branch: [bold green]git checkout -b feature/your-feature-name[/bold green]")
    console.print(steps)

    # Making Changes
    console.print("\n[bold]Making Changes[/bold]")
    changes = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    changes.add_column("Step", style="cyan")
    changes.add_column("Description")
    changes.add_row("1", "Make your changes in your branch")
    changes.add_row("2", "Follow the project's coding style and conventions")
    changes.add_row("3", "Include appropriate tests for your changes")
    changes.add_row("4", "Update documentation as needed")
    console.print(changes)

    # Submitting Changes
    console.print("\n[bold]Submitting Changes[/bold]")
    submit = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    submit.add_column("Step", style="cyan")
    submit.add_column("Description")
    submit.add_row(
        "1",
        'Commit your changes using [link=https://www.conventionalcommits.org/en/v1.0.0/]conventional commits[/link]: [bold green]git commit -m "feat: description of changes"[/bold green]',
    )
    submit.add_row("2", "Push to your fork: [bold green]git push origin feature/your-feature-name[/bold green]")
    submit.add_row("3", "Open a pull request against the main repository")
    console.print(submit)

    # License Information
    license_text = """
    By contributing to this project, you agree that your contributions will be licensed 
    under the project's GNU GPL-3.0-only license. All submitted code must comply with this license.
    
    Any contribution intentionally submitted for inclusion in this project shall be 
    subject to the same GPL-3.0-only license, without any additional terms or conditions.
    """
    console.print(Panel(license_text, title="Important License Information", border_style="red"))

    # Licensing of Contributions
    license_of_contributions_text = """
    When you submit code changes, your submissions are understood to be under the same GPL-3.0-only license
    that covers the project. If you have any concerns about this, please contact the project maintainers.
    """
    console.print(Panel(license_of_contributions_text, title="License of Contributions", border_style="red"))

    # Development Process
    console.print("\n[bold]Development Process[/bold]")
    issues_tracking = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    issues_tracking.add_column("Step", style="cyan")
    issues_tracking.add_column("Description")
    issues_tracking.add_row("☝", "Check existing issues before creating new ones")
    issues_tracking.add_row("🖊", "When creating issues, please provide detailed information")
    console.print(issues_tracking)

    # Pull Request Process
    console.print("\n[bold]Pull Request Process[/bold]")
    pull_request = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    pull_request.add_column("Step", style="cyan")
    pull_request.add_column("Description")
    pull_request.add_row("1", "Ensure your code adheres to the project standards")
    pull_request.add_row("2", "Update the README.md or documentation with details of changes if applicable")
    pull_request.add_row("3", "The PR will be merged once you have the sign-off of a maintainer")
    console.print(pull_request)

    console.print("\n[bold]Additional Resources[/bold]")
    additional_resources_text = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    additional_resources_text.add_column("Resource", style="cyan")
    additional_resources_text.add_column("URL")
    additional_resources_text.add_row("GNU GPL-3.0 License Full Text", "https://www.gnu.org/licenses/gpl-3.0.en.html")
    additional_resources_text.add_row("Issue Tracker", "https://gitlab.com/leading-works/floss/ancile/-/issues")
    console.print(additional_resources_text)

    # Footer
    console.print(f"\n🙏 Thank you for contributing to [bold cyan]{PROJECT_NAME}[/bold cyan]! 🙏", justify="center")
    console.print("\n♥", justify="center")
    console.print()
