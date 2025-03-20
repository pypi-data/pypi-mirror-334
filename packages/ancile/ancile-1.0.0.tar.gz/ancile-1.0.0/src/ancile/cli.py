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

# src/ancile/cli.py

import click
import yaml

from .LICENSE import LICENSE_TEXT
from .git_service import GitService
from .output_service import OutputService
from .risk_analyzer import RiskAnalyzer, RiskLevel, generate_default_config

APP_VERSION = "1.0.0"


@click.command()
@click.option("-g", "--generate-config", is_flag=True, help="Generate a default risk configuration file")
@click.option(
    "-r",
    "--risk-config",
    default="risk_mappings.yaml",
    help="The path to the risk configuration file with the mappings",
)
@click.option("-s", "--stable", help="The stable tag currently in production")
@click.option("-c", "--change", help="The new tag to assess for the release")
@click.option("-p", "--repo-path", default=".", help="The path to the git repository")
@click.option("-d", "--debug", is_flag=True, help="Enable debug output")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("-V", "--version", is_flag=True, help="Display the application version and exit")
@click.option("-L", "--license", is_flag=True, help="Display the license and exit")
@click.option("-C", "--contributing", is_flag=True, help="Display information on how to redistribute ancile and exit")
def assess_risk(
    generate_config: bool,
    risk_config: str,
    stable: str,
    change: str,
    repo_path: str,
    debug: bool,
    verbose: bool,
    version: bool,
    license: bool,
    contributing: bool,
):
    """Assess the risk level of changes between two git tags."""
    output = OutputService()

    output.print_license_notice()

    if license:
        output.display_content(LICENSE_TEXT)
        return

    if contributing:
        output.display_contributing()
        return

    if version:
        click.echo(f"Ancile version: {APP_VERSION}")
        return

    if generate_config and risk_config:
        generate_default_config(risk_config)
        click.echo(f"Default risk configuration file generated at {risk_config}")
        return

    try:
        if not (stable and change and risk_config):
            if not version or not (generate_config and risk_config) or not (license or contributing):
                click.echo(
                    "Error: Missing required options `-s`, `-c`, or `-r` when not using `-V`, `-L` or `-C`.", err=True
                )
                exit(3)

        # Load risk mappings
        with open(risk_config, "r") as f:
            configuration = yaml.safe_load(f)
            risk_mappings = {mapping["folder"]: mapping["risk"] for mapping in configuration["mappings"]}
            if verbose:
                output.display_config(risk_mappings)

        # Get changed files
        git_service = GitService(repo_path)
        changed_files = git_service.get_changed_files(stable, change)

        # Assess risk
        analyzer = RiskAnalyzer(risk_mappings)
        output.set_risk_analyzer(analyzer)
        risk_level = analyzer.assess_risk(debug, verbose, changed_files)

        # Display results
        output.display_assessment_results(
            verbose=verbose,
            project_name=git_service.get_project_name(),
            risk_level=risk_level,
            changed_files=changed_files,
            from_tag=stable,
            to_tag=change,
        )

        # Set exit code based on risk level
        if risk_level == RiskLevel.HIGH:
            exit(2)
        elif risk_level == RiskLevel.MEDIUM:
            exit(1)
        else:
            exit(0)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)


if __name__ == "__main__":
    assess_risk()
