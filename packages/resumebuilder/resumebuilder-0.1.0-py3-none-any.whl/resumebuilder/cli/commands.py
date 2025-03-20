#!/usr/bin/env python3
import os
import yaml
import click
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from faker import Faker
import sys

from resumebuilder.utils.config import save_config
from resumebuilder.models.resume import ResumeData
from resumebuilder.generators.pdf_generator import generate_resume_pdf, generate_cover_letter_pdf
from resumebuilder.templates.template_manager import get_available_templates, get_template

console = Console()
fake = Faker()

# Helper function to format name as LastName_FirstName
def format_name_for_filename(full_name):
    """Format full name as LastName_FirstName for filename."""
    name_parts = full_name.strip().split()
    if len(name_parts) >= 2:
        # Get the last name (last part) and first name (first part)
        last_name = name_parts[-1]
        first_name = name_parts[0]
        return f"{last_name}_{first_name}"
    # Fallback if name doesn't have at least two parts
    return full_name.replace(' ', '_')

def generate_interactive(template, output_dir, cover_letter, cover_letter_file=None):
    """Generate a resume through interactive prompts"""
    console.print("[bold green]Creating a new resume...[/bold green]")
    console.print("Please provide the following information:")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create input directory if it doesn't exist
    input_dir = "input"
    os.makedirs(input_dir, exist_ok=True)

    # Personal Information
    console.print("\n[bold]Personal Information[/bold]")
    personal = {
        'name': Prompt.ask("Full Name"),
        'title': Prompt.ask("Professional Title"),
        'email': Prompt.ask("Email Address"),
        'phone': Prompt.ask("Phone Number"),
        'location': Prompt.ask("Location"),
        'linkedin': Prompt.ask("LinkedIn URL", default=""),
        'github': Prompt.ask("GitHub URL", default=""),
        'website': Prompt.ask("Personal Website", default=""),
        'references': Prompt.ask("References Statement", default="References available upon request")
    }

    # Ask for target company and job title for filename
    target_company = Prompt.ask("Target Company (for filename)", default="")
    target_job_title = Prompt.ask("Target Job Title (for filename)", default="")
    
    # Employment History
    console.print("\n[bold]Employment History[/bold]")
    
    employment = []
    add_employment = True
    
    while add_employment:
        job = {
            'company': Prompt.ask("Company Name"),
            'position': Prompt.ask("Position/Title"),
            'location': Prompt.ask("Location"),
            'start_date': Prompt.ask("Start Date (YYYY-MM)"),
            'end_date': Prompt.ask("End Date (YYYY-MM or 'Present')"),
            'responsibilities': []
        }
        
        # Job responsibilities
        console.print("Enter job responsibilities (empty line to finish):")
        resp_idx = 1
        while True:
            resp = Prompt.ask(f"Responsibility {resp_idx}", default="")
            if not resp:
                break
            job['responsibilities'].append(resp)
            resp_idx += 1
        
        employment.append(job)
        add_employment = Confirm.ask("Add another job?")
    
    # Education
    console.print("\n[bold]Education[/bold]")
    
    education = []
    add_education = True
    
    while add_education:
        edu = {
            'institution': Prompt.ask("Institution Name"),
            'degree': Prompt.ask("Degree/Certification"),
            'location': Prompt.ask("Location"),
            'start_date': Prompt.ask("Start Date (YYYY-MM)"),
            'end_date': Prompt.ask("End Date (YYYY-MM or 'Present')"),
            'honors': Prompt.ask("Honors/GPA", default="")
        }
        
        education.append(edu)
        add_education = Confirm.ask("Add another education entry?")
    
    # Skills
    console.print("\n[bold]Skills[/bold]")
    skills = {}
    
    add_category = True
    while add_category:
        category = Prompt.ask("Skill Category (e.g., Programming, Languages)")
        skills[category] = []
        
        console.print(f"Enter {category} skills (empty line to finish):")
        skill_idx = 1
        while True:
            skill = Prompt.ask(f"Skill {skill_idx}", default="")
            if not skill:
                break
            skills[category].append(skill)
            skill_idx += 1
        
        add_category = Confirm.ask("Add another skill category?")
    
    # Certifications
    console.print("\n[bold]Certifications[/bold]")
    
    certifications = []
    add_cert = Confirm.ask("Add certifications?")
    
    while add_cert:
        cert = {
            'name': Prompt.ask("Certification Name"),
            'issuer': Prompt.ask("Issuing Organization"),
            'date': Prompt.ask("Date Earned (YYYY-MM)"),
            'expires': Prompt.ask("Expiration Date (YYYY-MM or 'Never')", default="Never")
        }
        
        certifications.append(cert)
        add_cert = Confirm.ask("Add another certification?")
    
    # Cover Letter
    cover_letter_data = None
    if cover_letter:
        console.print("\n[bold]Cover Letter Information[/bold]")
        cover_letter_data = {
            'recipient_name': Prompt.ask("Hiring Manager's Name (if known)", default="Hiring Manager"),
            'company_name': Prompt.ask("Company Name"),
            'position': Prompt.ask("Position Applied For"),
            'company_address': Prompt.ask("Company Address (optional)", default=""),
            'greeting': Prompt.ask("Greeting (e.g., 'Dear Sir/Madam')", default="Dear Hiring Manager"),
            'paragraphs': []
        }
        
        console.print("Enter cover letter paragraphs (empty line to finish):")
        para_idx = 1
        while True:
            para = Prompt.ask(f"Paragraph {para_idx}", default="")
            if not para:
                break
            cover_letter_data['paragraphs'].append(para)
            para_idx += 1
    
    # Save resume data
    resume_data = {
        'personal': personal,
        'experience': employment,
        'education': education,
        'skills': skills,
        'certifications': certifications
    }
    
    # Save to YAML file
    formatted_name = format_name_for_filename(personal['name'])
    company_part = f"_{target_company.replace(' ', '_')}" if target_company else ""
    job_title_part = f"_{target_job_title.replace(' ', '_')}" if target_job_title else ""
    filename_base = f"{formatted_name}{company_part}{job_title_part}"
    
    resume_filename = os.path.join(input_dir, f"{filename_base}_resume.yaml")
    
    with open(resume_filename, 'w') as file:
        yaml.dump(resume_data, file, default_flow_style=False)
    
    console.print(f"[green]Resume data saved to [bold]{resume_filename}[/bold][/green]")
    
    # Create directory for PDFs
    pdf_dir = os.path.join(output_dir, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Create a company/job-specific directory for the PDFs
    company_folder = f"{target_company.replace(' ', '_')}_{target_job_title.replace(' ', '_')}"
    company_pdf_dir = os.path.join(pdf_dir, company_folder)
    os.makedirs(company_pdf_dir, exist_ok=True)
    
    # Generate resume model
    resume_model = ResumeData(**resume_data)
    
    # Generate PDF
    pdf_filename = os.path.join(company_pdf_dir, f"{filename_base}_resume.pdf")
    generate_resume_pdf(resume_model, template, pdf_filename)
    
    console.print(f"[green]Resume PDF generated: [bold]{pdf_filename}[/bold][/green]")
    
    # Generate cover letter if requested
    if cover_letter:
        cl_filename = os.path.join(company_pdf_dir, f"{filename_base}_cover_letter.pdf")
        generate_cover_letter_pdf(resume_model, cover_letter_data, template, cl_filename)
        console.print(f"[green]Cover Letter PDF generated: [bold]{cl_filename}[/bold][/green]")

def generate_dummy_resume(template, output_dir, cover_letter, cover_letter_file=None):
    """Generate a resume with dummy placeholder data"""
    console.print("[bold green]Generating a dummy resume...[/bold green]")
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create separate directories for PDFs and YAML files
        pdf_dir = os.path.join(output_dir, "pdfs")
        yaml_dir = os.path.join(output_dir, "yaml")
        os.makedirs(pdf_dir, exist_ok=True)
        os.makedirs(yaml_dir, exist_ok=True)
        
        # Generate dummy personal data
        name = fake.name()
        personal = {
            'name': name,
            'title': fake.job(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'location': f"{fake.city()}, {fake.state_abbr()}",
            'linkedin': f"linkedin.com/in/{name.lower().replace(' ', '-')}",
            'github': f"github.com/{name.lower().split()[0]}",
            'website': f"{name.lower().split()[0]}.com",
            'references': "References available upon request"
        }
        
        # Generate fake company and job title for filename
        target_company = fake.company().replace(',', '').strip()
        target_job_title = fake.job().replace(',', '').strip()
        
        # Employment History
        employment = []
        for _ in range(3):
            job = {
                'company': fake.company(),
                'position': fake.job(),
                'location': f"{fake.city()}, {fake.state_abbr()}",
                'start_date': f"{fake.date_between(start_date='-10y', end_date='-2y').strftime('%Y-%m')}",
                'end_date': 'Present' if _ == 0 else f"{fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m')}",
                'responsibilities': [fake.paragraph() for _ in range(3)]
            }
            employment.append(job)
        
        # Education
        education = []
        for _ in range(2):
            edu = {
                'institution': fake.company(),
                'degree': f"Bachelor of {'Science' if _ % 2 == 0 else 'Arts'} in {fake.catch_phrase()}",
                'location': f"{fake.city()}, {fake.state_abbr()}",
                'start_date': f"{fake.date_between(start_date='-15y', end_date='-5y').strftime('%Y-%m')}",
                'end_date': f"{fake.date_between(start_date='-5y', end_date='-2y').strftime('%Y-%m')}",
                'honors': fake.sentence(nb_words=5) if _ % 2 == 0 else ""
            }
            education.append(edu)
        
        # Skills
        skills = {
            'Programming': [fake.word() for _ in range(5)],
            'Languages': [fake.language_name() for _ in range(3)],
            'Tools': [fake.word() for _ in range(4)]
        }
        
        # Certifications
        certifications = []
        for _ in range(2):
            cert = {
                'name': f"{fake.company()} {fake.word().capitalize()} Certification",
                'issuer': fake.company(),
                'date': f"{fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m')}",
                'expires': 'Never' if _ % 2 == 0 else f"{fake.date_between(start_date='today', end_date='+5y').strftime('%Y-%m')}"
            }
            certifications.append(cert)
        
        # Dummy Cover Letter
        cover_letter_data = None
        if cover_letter:
            cover_letter_data = {
                'recipient_name': fake.name(),
                'company_name': fake.company(),
                'position': fake.job(),
                'company_address': fake.address(),
                'greeting': f"Dear {fake.name().split()[0]}",
                'paragraphs': [fake.paragraph() for _ in range(3)]
            }
        
        # Save resume data
        resume_data = {
            'personal': personal,
            'experience': employment,
            'education': education,
            'skills': skills,
            'certifications': certifications
        }
        
        # Save to YAML file
        formatted_name = format_name_for_filename(personal['name'])
        company_part = f"_{target_company.replace(' ', '_')}" if target_company else ""
        job_title_part = f"_{target_job_title.replace(' ', '_')}" if target_job_title else ""
        filename_base = f"{formatted_name}{company_part}{job_title_part}"
        
        resume_filename = os.path.join(yaml_dir, f"{filename_base}_resume.yaml")
        
        with open(resume_filename, 'w') as file:
            yaml.dump(resume_data, file, default_flow_style=False)
        
        console.print(f"[green]Dummy resume data saved to [bold]{resume_filename}[/bold][/green]")
        
        # Create a company/job-specific directory for the PDFs
        company_folder = f"{target_company.replace(' ', '_')}_{target_job_title.replace(' ', '_')}"
        company_pdf_dir = os.path.join(pdf_dir, company_folder)
        os.makedirs(company_pdf_dir, exist_ok=True)
        
        # Create resume model
        resume_model = ResumeData(**resume_data)
        
        # Generate PDF
        pdf_filename = os.path.join(company_pdf_dir, f"{filename_base}_resume.pdf")
        generate_resume_pdf(resume_model, template, pdf_filename)
        
        console.print(f"[green]Dummy resume PDF generated: [bold]{pdf_filename}[/bold][/green]")
        
        if cover_letter:
            cl_filename = os.path.join(company_pdf_dir, f"{filename_base}_cover_letter.pdf")
            generate_cover_letter_pdf(resume_model, cover_letter_data, template, cl_filename)
            console.print(f"[green]Dummy cover letter PDF generated: [bold]{cl_filename}[/bold][/green]")
    
    except Exception as e:
        console.print(f"[bold red]Error generating dummy resume: [/bold red] {str(e)}")
        raise

def generate_from_file(yaml_file, template, output_dir, cover_letter, cover_letter_file=None):
    """Generate a resume from a YAML file"""
    console.print(f"[bold green]Generating resume from {yaml_file}...[/bold green]")
    
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory for PDFs
        pdf_dir = os.path.join(output_dir, "pdfs")
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Load the resume data
        resume_model = ResumeData(**data)
        
        # Check if we're in a test environment or non-interactive mode
        non_interactive = (os.environ.get('PYTEST_CURRENT_TEST') is not None or 
                          os.environ.get('RESUMEBUILDER_NON_INTERACTIVE') == 'true' or 
                          not sys.stdin.isatty())
        
        # Get default company and position from environment variables if set
        default_company = os.environ.get('RESUMEBUILDER_COMPANY', 'Company')
        default_position = os.environ.get('RESUMEBUILDER_POSITION', 'Position')
        
        # Use default values if in non-interactive mode
        if non_interactive:
            # Use defaults for non-interactive mode
            target_company = default_company
            target_job_title = default_position
            console.print(f"[yellow]Using values for company '{target_company}' and job title '{target_job_title}' in non-interactive mode[/yellow]")
        else:
            # Ask for target company and job title for filename
            target_company = Prompt.ask("Target Company (for filename)", default="")
            target_job_title = Prompt.ask("Target Job Title (for filename)", default="")
        
        # Get the name for file naming
        name = data['personal']['name']
        formatted_name = format_name_for_filename(name)
        company_part = f"_{target_company.replace(' ', '_')}" if target_company else ""
        job_title_part = f"_{target_job_title.replace(' ', '_')}" if target_job_title else ""
        filename_base = f"{formatted_name}{company_part}{job_title_part}"
        
        # Create a company/job-specific directory for the PDFs
        company_folder = f"{target_company.replace(' ', '_')}_{target_job_title.replace(' ', '_')}"
        company_pdf_dir = os.path.join(pdf_dir, company_folder)
        os.makedirs(company_pdf_dir, exist_ok=True)
        
        # Generate PDF file
        pdf_filename = os.path.join(company_pdf_dir, f"{filename_base}_resume.pdf")
        generate_resume_pdf(resume_model, template, pdf_filename)
        
        console.print(f"[green]Resume PDF generated: [bold]{pdf_filename}[/bold][/green]")
        
        # Handle cover letter if requested
        if cover_letter:
            cover_letter_data = None
            
            # Check if cover letter is already in the YAML data
            if resume_model.cover_letter:
                cover_letter_data = resume_model.cover_letter.dict()
                console.print("[green]Using cover letter data from YAML file[/green]")
            
            # Check if a specific cover letter file was provided
            if cover_letter_file and os.path.exists(cover_letter_file):
                from resumebuilder.models.resume import CoverLetter
                
                # If we already have some data, ask user whether to use file or existing data
                use_file = True
                if cover_letter_data and not non_interactive:
                    use_file = Confirm.ask(f"Found both cover letter in YAML and {cover_letter_file}. Use the specified file?", default=True)
                
                if not cover_letter_data or use_file:
                    console.print(f"[green]Loading cover letter from {cover_letter_file}[/green]")
                    
                    # Get company name and position if not already in YAML
                    company_name = data.get('cover_letter', {}).get('company_name', target_company)
                    if not company_name and not non_interactive:
                        company_name = Prompt.ask("Company Name for Cover Letter", default=target_company)
                    elif not company_name:
                        company_name = target_company
                    
                    position = data.get('cover_letter', {}).get('position', target_job_title)
                    if not position and not non_interactive:
                        position = Prompt.ask("Position for Cover Letter", default=target_job_title)
                    elif not position:
                        position = target_job_title
                    
                    # Load cover letter from file
                    cover_letter_obj = CoverLetter.from_file(
                        cover_letter_file,
                        company_name=company_name,
                        position=position,
                        recipient_name=data.get('cover_letter', {}).get('recipient_name', "Hiring Manager"),
                        company_address=data.get('cover_letter', {}).get('company_address', None),
                        greeting=data.get('cover_letter', {}).get('greeting', f"Dear {data.get('cover_letter', {}).get('recipient_name', 'Hiring Manager')}")
                    )
                    cover_letter_data = cover_letter_obj.dict()
            # Check if there's a default cover letter text file
            elif not cover_letter_data:
                default_cover_letter_file = os.path.join(os.path.dirname(yaml_file), "cover_letter_input.txt")
                if os.path.exists(default_cover_letter_file):
                    from resumebuilder.models.resume import CoverLetter
                    
                    use_file = True
                    if not non_interactive:
                        use_file = Confirm.ask(f"Found cover_letter_input.txt. Use this file?", default=True)
                    
                    if use_file:
                        console.print(f"[green]Loading cover letter from {default_cover_letter_file}[/green]")
                        
                        # Get company name and position if not already in YAML
                        company_name = data.get('cover_letter', {}).get('company_name', target_company)
                        if not company_name and not non_interactive:
                            company_name = Prompt.ask("Company Name for Cover Letter", default=target_company)
                        elif not company_name:
                            company_name = target_company
                        
                        position = data.get('cover_letter', {}).get('position', target_job_title)
                        if not position and not non_interactive:
                            position = Prompt.ask("Position for Cover Letter", default=target_job_title)
                        elif not position:
                            position = target_job_title
                        
                        # Load cover letter from file
                        cover_letter_obj = CoverLetter.from_file(
                            default_cover_letter_file,
                            company_name=company_name,
                            position=position,
                            recipient_name=data.get('cover_letter', {}).get('recipient_name', "Hiring Manager"),
                            company_address=data.get('cover_letter', {}).get('company_address', None),
                            greeting=data.get('cover_letter', {}).get('greeting', f"Dear {data.get('cover_letter', {}).get('recipient_name', 'Hiring Manager')}")
                        )
                        cover_letter_data = cover_letter_obj.dict()
            
            # If no cover letter data found yet, prompt user interactively
            if not cover_letter_data and not non_interactive:
                console.print("\n[bold]Cover Letter Information[/bold]")
                cover_letter_data = {
                    'recipient_name': Prompt.ask("Hiring Manager's Name (if known)", default="Hiring Manager"),
                    'company_name': Prompt.ask("Company Name", default=target_company),
                    'position': Prompt.ask("Position Applied For", default=target_job_title),
                    'company_address': Prompt.ask("Company Address (optional)", default=""),
                    'greeting': Prompt.ask("Greeting (e.g., 'Dear Sir/Madam')", default="Dear Hiring Manager"),
                    'paragraphs': []
                }
                
                console.print("Enter cover letter paragraphs (empty line to finish):")
                para_idx = 1
                while True:
                    para = Prompt.ask(f"Paragraph {para_idx}", default="")
                    if not para:
                        break
                    cover_letter_data['paragraphs'].append(para)
                    para_idx += 1
            elif not cover_letter_data:
                # Use default data for non-interactive mode
                cover_letter_data = {
                    'recipient_name': "Hiring Manager",
                    'company_name': target_company,
                    'position': target_job_title,
                    'company_address': "",
                    'greeting': "Dear Hiring Manager",
                    'paragraphs': ["Please find enclosed my resume for your consideration."]
                }
                console.print("[yellow]Using default values for cover letter in non-interactive mode[/yellow]")
            
            cl_filename = os.path.join(company_pdf_dir, f"{filename_base}_cover_letter.pdf")
            generate_cover_letter_pdf(resume_model, cover_letter_data, template, cl_filename)
            console.print(f"[green]Cover Letter PDF generated: [bold]{cl_filename}[/bold][/green]")
            
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File {yaml_file} not found.")
        raise
    except yaml.YAMLError:
        console.print(f"[bold red]Error:[/bold red] Invalid YAML file format.")
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise

def update_resume(yaml_file, template, output_dir, cover_letter, cover_letter_file=None):
    """Update an existing resume YAML file"""
    console.print(f"[bold green]Updating resume from {yaml_file}...[/bold green]")
    
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory for PDFs
        pdf_dir = os.path.join(output_dir, "pdfs")
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Ask for template if not specified
        template_to_use = template if template else data.get('template', 'modern')
        
        # Ask for target company and job title for filename
        target_company = Prompt.ask("Target Company (for filename)", default="")
        target_job_title = Prompt.ask("Target Job Title (for filename)", default="")
        
        # Get the name for file naming
        name = data['personal']['name']
        formatted_name = format_name_for_filename(name)
        company_part = f"_{target_company.replace(' ', '_')}" if target_company else ""
        job_title_part = f"_{target_job_title.replace(' ', '_')}" if target_job_title else ""
        filename_base = f"{formatted_name}{company_part}{job_title_part}"
        
        # Create a company/job-specific directory for the PDFs
        company_folder = f"{target_company.replace(' ', '_')}_{target_job_title.replace(' ', '_')}"
        company_pdf_dir = os.path.join(pdf_dir, company_folder)
        os.makedirs(company_pdf_dir, exist_ok=True)
        
        # Load the resume data
        resume_model = ResumeData(**data)
        
        # Generate PDF file
        pdf_filename = os.path.join(company_pdf_dir, f"{filename_base}_resume.pdf")
        generate_resume_pdf(resume_model, template_to_use, pdf_filename)
        
        console.print(f"[green]Resume PDF generated: [bold]{pdf_filename}[/bold][/green]")
        
        # Handle cover letter if requested
        if cover_letter:
            cover_letter_data = None
            
            # Check if cover letter is already in the YAML data
            if resume_model.cover_letter:
                cover_letter_data = resume_model.cover_letter.dict()
                console.print("[green]Using cover letter data from YAML file[/green]")
            
            # Check if a specific cover letter file was provided
            if cover_letter_file and os.path.exists(cover_letter_file):
                from resumebuilder.models.resume import CoverLetter
                
                # If we already have some data, ask user whether to use file or existing data
                if cover_letter_data and Confirm.ask(f"Found both cover letter in YAML and {cover_letter_file}. Use the specified file?", default=True):
                    cover_letter_data = None
                
                if not cover_letter_data:
                    console.print(f"[green]Loading cover letter from {cover_letter_file}[/green]")
                    
                    # Get company name and position if not already in YAML
                    company_name = data.get('cover_letter', {}).get('company_name', target_company)
                    if not company_name:
                        company_name = Prompt.ask("Company Name for Cover Letter", default=target_company)
                    
                    position = data.get('cover_letter', {}).get('position', target_job_title)
                    if not position:
                        position = Prompt.ask("Position for Cover Letter", default=target_job_title)
                    
                    # Load cover letter from file
                    cover_letter_obj = CoverLetter.from_file(
                        cover_letter_file,
                        company_name=company_name,
                        position=position,
                        recipient_name=data.get('cover_letter', {}).get('recipient_name', "Hiring Manager"),
                        company_address=data.get('cover_letter', {}).get('company_address', None),
                        greeting=data.get('cover_letter', {}).get('greeting', f"Dear {data.get('cover_letter', {}).get('recipient_name', 'Hiring Manager')}")
                    )
                    cover_letter_data = cover_letter_obj.dict()
            # Check if there's a default cover letter text file
            elif not cover_letter_data:
                default_cover_letter_file = os.path.join(os.path.dirname(yaml_file), "cover_letter_input.txt")
                if os.path.exists(default_cover_letter_file):
                    from resumebuilder.models.resume import CoverLetter
                    
                    if Confirm.ask(f"Found cover_letter_input.txt. Use this file?", default=True):
                        console.print(f"[green]Loading cover letter from {default_cover_letter_file}[/green]")
                        
                        # Get company name and position if not already in YAML
                        company_name = data.get('cover_letter', {}).get('company_name', target_company)
                        if not company_name:
                            company_name = Prompt.ask("Company Name for Cover Letter", default=target_company)
                        
                        position = data.get('cover_letter', {}).get('position', target_job_title)
                        if not position:
                            position = Prompt.ask("Position for Cover Letter", default=target_job_title)
                        
                        # Load cover letter from file
                        cover_letter_obj = CoverLetter.from_file(
                            default_cover_letter_file,
                            company_name=company_name,
                            position=position,
                            recipient_name=data.get('cover_letter', {}).get('recipient_name', "Hiring Manager"),
                            company_address=data.get('cover_letter', {}).get('company_address', None),
                            greeting=data.get('cover_letter', {}).get('greeting', f"Dear {data.get('cover_letter', {}).get('recipient_name', 'Hiring Manager')}")
                        )
                        cover_letter_data = cover_letter_obj.dict()
            
            # If no cover letter data found yet, prompt user interactively
            if not cover_letter_data:
                console.print("\n[bold]Cover Letter Information[/bold]")
                cover_letter_data = {
                    'recipient_name': Prompt.ask("Hiring Manager's Name (if known)", default="Hiring Manager"),
                    'company_name': Prompt.ask("Company Name", default=target_company),
                    'position': Prompt.ask("Position Applied For", default=target_job_title),
                    'company_address': Prompt.ask("Company Address (optional)", default=""),
                    'greeting': Prompt.ask("Greeting (e.g., 'Dear Sir/Madam')", default="Dear Hiring Manager"),
                    'paragraphs': []
                }
                
                console.print("Enter cover letter paragraphs (empty line to finish):")
                para_idx = 1
                while True:
                    para = Prompt.ask(f"Paragraph {para_idx}", default="")
                    if not para:
                        break
                    cover_letter_data['paragraphs'].append(para)
                    para_idx += 1
            
            cl_filename = os.path.join(company_pdf_dir, f"{filename_base}_cover_letter.pdf")
            generate_cover_letter_pdf(resume_model, cover_letter_data, template_to_use, cl_filename)
            console.print(f"[green]Cover Letter PDF generated: [bold]{cl_filename}[/bold][/green]")
        
        # Save the updated configuration with any new changes
        data['template'] = template_to_use
        save_config(data, yaml_file)
        console.print(f"[green]Resume data updated in [bold]{yaml_file}[/bold][/green]")
    except Exception as e:
        console.print(f"[bold red]Error updating resume:[/bold red] {str(e)}")
        raise

def list_available_templates():
    """List all available resume templates"""
    console.print("[bold green]Available Resume Templates:[/bold green]")
    
    templates = get_available_templates()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Template", style="dim")
    table.add_column("Description")
    
    for template in templates:
        name = template['name']
        description = template['description']
        table.add_row(name, description)
    
    console.print(table) 