#!/usr/bin/env python3
import os
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from resumebuilder.cli import commands
from resumebuilder.utils.config import load_config

console = Console()

@click.group()
@click.version_option(version='0.1.1')
def cli():
    """ResumeBuilder: Generate professional resumes and cover letters.
    
    This application allows you to create professionally formatted
    resumes and cover letters using customizable templates.
    """
    pass

@cli.command()
@click.option('--template', default='modern', help='Resume template to use')
@click.option('--output-dir', default='.', help='Directory to save generated files')
@click.option('--dummy', is_flag=True, help='Use dummy placeholder data')
@click.option('--from-file', help='Load data from a YAML file')
@click.option('--cover-letter', is_flag=True, help='Generate a matching cover letter')
@click.option('--cover-letter-file', help='Load cover letter content from a text file')
def create(template, output_dir, dummy, from_file, cover_letter, cover_letter_file):
    """Create a new resume with optional cover letter"""
    try:
        cover_letter = cover_letter or bool(cover_letter_file)
        
        if dummy:
            commands.generate_dummy_resume(template, output_dir, cover_letter, cover_letter_file)
        elif from_file:
            commands.generate_from_file(from_file, template, output_dir, cover_letter, cover_letter_file)
        else:
            commands.generate_interactive(template, output_dir, cover_letter, cover_letter_file)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
def list_templates():
    """List available resume templates."""
    try:
        commands.list_available_templates()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--template', default='modern', help='Resume template to use')
@click.option('--output-dir', default='.', help='Directory to save generated files')
@click.option('--cover-letter', is_flag=True, help='Generate a matching cover letter')
@click.option('--cover-letter-file', help='Load cover letter content from a text file')
def dummy(template, output_dir, cover_letter, cover_letter_file):
    """Generate a resume with dummy data"""
    try:
        cover_letter = cover_letter or bool(cover_letter_file)
        commands.generate_dummy_resume(template, output_dir, cover_letter, cover_letter_file)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('yaml_file')
@click.option('--template', help='Change resume template')
@click.option('--output-dir', default='.', help='Directory to save generated files')
@click.option('--cover-letter', is_flag=True, help='Generate a matching cover letter')
@click.option('--cover-letter-file', help='Load cover letter content from a text file')
def update(yaml_file, template, output_dir, cover_letter, cover_letter_file):
    """Update an existing resume"""
    try:
        commands.update_resume(yaml_file, template, output_dir, cover_letter, cover_letter_file)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('yaml_file')
@click.option('--template', default='modern', help='Resume template to use')
@click.option('--output-dir', default='.', help='Directory to save generated files')
@click.option('--cover-letter-file', help='Path to cover letter text file')
@click.option('--company', default='Company', help='Company name for file naming')
@click.option('--position', default='Position', help='Position title for file naming')
def generate(yaml_file, template, output_dir, cover_letter_file, company, position):
    """Generate resume and cover letter non-interactively.
    
    This command is designed for scripting and automation, and won't prompt for any input.
    It uses default values or provided options for all inputs that would normally be prompted.
    
    Example:
        resumebuilder generate input/your_resume.yaml --cover-letter-file input/cover_letter_input.txt
    """
    try:
        # Set environment variable to indicate non-interactive mode
        os.environ['RESUMEBUILDER_NON_INTERACTIVE'] = 'true'
        
        # Set company and position for file naming
        os.environ['RESUMEBUILDER_COMPANY'] = company
        os.environ['RESUMEBUILDER_POSITION'] = position
        
        # Determine if we should generate a cover letter
        cover_letter = cover_letter_file is not None
        
        # Generate the resume and optional cover letter
        commands.generate_from_file(yaml_file, template, output_dir, cover_letter, cover_letter_file)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
    finally:
        # Clean up environment variables
        if 'RESUMEBUILDER_NON_INTERACTIVE' in os.environ:
            del os.environ['RESUMEBUILDER_NON_INTERACTIVE']
        if 'RESUMEBUILDER_COMPANY' in os.environ:
            del os.environ['RESUMEBUILDER_COMPANY']
        if 'RESUMEBUILDER_POSITION' in os.environ:
            del os.environ['RESUMEBUILDER_POSITION']

def main():
    """Main entry point for the application."""
    # Print welcome banner
    title = Text("ResumeBuilder", style="bold blue")
    subtitle = Text("Professional Resume Generator", style="italic")
    
    console.print(Panel.fit(
        f"{title}\n{subtitle}",
        border_style="blue",
        padding=(1, 2)
    ))
    
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 