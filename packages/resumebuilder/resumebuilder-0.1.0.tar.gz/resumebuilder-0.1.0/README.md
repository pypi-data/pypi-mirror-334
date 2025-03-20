# ResumeBuilder

A Python CLI application that generates professional CV/Resume templates with matching cover letters in PDF format.

## Features

- Generate professional PDF resume from user data
- Create matching cover letter with customizable fields
- Support for all standard resume sections (Education, Experience, Skills, etc.)
- Multiple template styles with different layouts and designs
- Non-interactive mode for automation and scripting
- Automatic parsing of cover letter text files
- Support for various date formats including 'Month YYYY'
- Template selection with different styles/layouts
- Lorem ipsum placeholder generation for template testing
- Command-line interface with interactive prompts
- Save user data for future resume updates
- Export to PDF format with proper formatting
- Customizable sections and ordering

## Installation

### From PyPI

The easiest way to install ResumeBuilder is from PyPI:

```bash
pip install resumebuilder
```

After installation, you can use the `resumebuilder` command directly from your terminal.

### From Source

```bash
git clone https://github.com/iron-hope-shop/tools-resume.git
cd tools-resume
pip install -e .
```

### Development Installation

For development, you may want to install additional dependencies:

```bash
pip install -e ".[dev]"
```

## Basic Usage

### Creating a Resume Interactively

The simplest way to create a resume is to use the interactive mode:

```bash
resumebuilder create
```

This will guide you through the process of entering your personal information, employment history, education, skills, and certifications. The data will be saved to a YAML file, and a PDF resume will be generated.

### Creating a Resume with Dummy Data

To quickly see what a resume template looks like, you can generate a resume with dummy data:

```bash
resumebuilder dummy --template modern
```

This will create a resume with placeholder data using the "modern" template.

### Creating a Resume from a YAML File

If you already have a YAML file with your resume data, you can generate a resume from it:

```bash
resumebuilder create --from-file my_resume.yaml
```

You can also generate a cover letter along with your resume:

```bash
resumebuilder create --from-file my_resume.yaml --cover-letter
```

The tool will look for a cover letter in these sources (in order of priority):
1. In the YAML file (under a `cover_letter` key)
2. From a file specified with `--cover-letter-file`
3. From a file named `cover_letter_input.txt` in the same directory as your resume YAML
4. Interactively prompt for cover letter content

Example with explicit cover letter file:

```bash
resumebuilder create --from-file my_resume.yaml --cover-letter --cover-letter-file input/cover_letter_input.txt
```

### Generating Resumes Non-Interactively (for Automation)

For automation or batch processing, use the `generate` command which runs in non-interactive mode:

```bash
resumebuilder generate input/your_resume.yaml --cover-letter-file input/cover_letter_input.txt --company "CompanyName" --position "JobTitle"
```

This command will not prompt for any input, making it suitable for scripts and automation. It sets environment variables internally to control file naming and behavior.

### Updating an Existing Resume

To update an existing resume:

```bash
resumebuilder update my_resume.yaml
```

### Listing Available Templates

To see a list of available templates:

```bash
resumebuilder list-templates
```

## Command Options

### Create Command

```
resumebuilder create [OPTIONS]

Options:
  --template TEXT           Resume template to use (default: modern)
  --output-dir TEXT         Directory to save generated files (default: current directory)
  --dummy                   Use dummy placeholder data
  --from-file TEXT          Load data from a YAML file
  --cover-letter            Generate a matching cover letter
  --cover-letter-file TEXT  Load cover letter content from a text file
  --help                    Show this message and exit
```

### List Templates Command

```
resumebuilder list-templates [OPTIONS]

Options:
  --help              Show this message and exit
```

### Dummy Command

```
resumebuilder dummy [OPTIONS]

Options:
  --template TEXT           Resume template to use (default: modern)
  --output-dir TEXT         Directory to save generated files (default: current directory)
  --cover-letter            Generate a matching cover letter
  --cover-letter-file TEXT  Load cover letter content from a text file
  --help                    Show this message and exit
```

### Update Command

```
resumebuilder update [OPTIONS] YAML_FILE

Options:
  --template TEXT           Change resume template
  --output-dir TEXT         Directory to save generated files (default: current directory)
  --cover-letter            Generate a matching cover letter
  --cover-letter-file TEXT  Load cover letter content from a text file
  --help                    Show this message and exit
```

### Generate Command (Non-Interactive)

```
resumebuilder generate [OPTIONS] YAML_FILE

Options:
  --template TEXT           Resume template to use (default: modern)
  --output-dir TEXT         Directory to save generated files (default: current directory)
  --cover-letter-file TEXT  Path to cover letter text file
  --company TEXT            Company name for file naming (default: 'Company')
  --position TEXT           Position title for file naming (default: 'Position')
  --help                    Show this message and exit
```

This command doesn't prompt for any user input, making it suitable for automation. It generates files using the naming pattern: `LastName_FirstName_CompanyName_JobTitle_resume.pdf` (and `_cover_letter.pdf` if specified).

## Environment Variables

The application recognizes these environment variables when running:

- `RESUMEBUILDER_NON_INTERACTIVE`: Set to 'true' to run in non-interactive mode (no prompts)
- `RESUMEBUILDER_COMPANY`: Default company name for file naming when in non-interactive mode
- `RESUMEBUILDER_POSITION`: Default position title for file naming when in non-interactive mode

These variables are automatically set by the `generate` command, but can also be set manually if using the `create` command in scripts.

## Output Directory Structure

When generating resumes and cover letters, files are organized in this structure:

```
output/
├── pdfs/
│   └── CompanyName_JobTitle/
│       ├── LastName_FirstName_CompanyName_JobTitle_resume.pdf
│       └── LastName_FirstName_CompanyName_JobTitle_cover_letter.pdf
└── yaml/
    └── LastName_FirstName_CompanyName_JobTitle_resume.yaml
```

This organization makes it easy to manage multiple versions of your resume for different job applications.

## Available Templates

The application includes these built-in templates:

1. **modern** - Contemporary design with subtle design elements
2. **minimal** - Clean, simple design with minimal styling
3. **classic** - Traditional resume format with conservative styling
4. **creative** - More expressive design for creative industries

Run `resumebuilder list-templates` to see the full list with descriptions.

## Resume Data Format

The resume data is stored in YAML format. Here's an example of the structure:

```yaml
personal:
  name: "John Doe"
  title: "Software Engineer"
  email: "john.doe@example.com"
  phone: "+1 (555) 123-4567"
  location: "San Francisco, CA"
  linkedin: "linkedin.com/in/johndoe"
  github: "github.com/johndoe"
  website: "johndoe.com"

experience:
  - company: "Tech Company"
    position: "Senior Software Engineer"
    location: "San Francisco, CA"
    start_date: "2020-01"
    end_date: "Present"
    responsibilities:
      - "Led development of microservices architecture"
      - "Improved system performance by 30%"
      - "Mentored junior developers"

education:
  - institution: "University of California"
    degree: "Bachelor of Science in Computer Science"
    location: "Berkeley, CA"
    start_date: "2012-09"
    end_date: "2016-05"
    honors: "Magna Cum Laude"

skills:
  programming:
    - "Python"
    - "JavaScript"
    - "Go"
  frameworks:
    - "Django"
    - "React"
    - "Docker"
  tools:
    - "Git"
    - "AWS"
    - "CI/CD"

certifications:
  - name: "AWS Certified Developer"
    issuer: "Amazon Web Services"
    date: "2020-05"
    expires: "2023-05"
    
# Optional cover letter section
cover_letter:
  recipient_name: "Hiring Manager"
  company_name: "Tech Company"
  position: "Senior Software Engineer"
  company_address: "123 Tech Street, San Francisco, CA"
  greeting: "Dear Hiring Manager"
  paragraphs:
    - "I am writing to express my interest in the Senior Software Engineer position at Tech Company."
    - "With my 5+ years of experience in software development and a strong background in Python and JavaScript, I believe I would be a valuable addition to your team."
    - "Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to Tech Company's success."
```

## Cover Letter Format

There are two ways to include a cover letter:

### 1. In the YAML file (as shown above)

Include a `cover_letter` section in your resume YAML file with recipient information and paragraphs.

### 2. As a separate text file

When providing a cover letter in a text file, you have two format options:

#### Simple format:
Structure it with blank lines between paragraphs. For example:

```
I am writing to express my interest in the Senior Software Engineer position at Tech Company.

With my 5+ years of experience in software development and a strong background in Python and JavaScript, I believe I would be a valuable addition to your team.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to Tech Company's success.
```

#### Advanced format:
You can include header information in the first lines, followed by a blank line and then the paragraphs:

```
CompanyName
Position Title
Recipient Name
Recipient Title

Dear Recipient Name,

First paragraph of your cover letter...

Second paragraph...

Closing paragraph...
```

The tool will automatically parse this information for the cover letter formatting.

## Date Format Support

The application supports various date formats:

- YYYY-MM (e.g., "2020-01")
- Month YYYY (e.g., "January 2020" or "Jan 2020")
- Month Day, YYYY (e.g., "January 15, 2020" or "Jan 15, 2020")
- "Present" (for current positions)

All dates are converted to a standardized format internally.

## Examples

The `input` directory contains sample resume YAML files:
- `your_resume.yaml`: A complete example for a software engineer

To generate a resume from the sample file:

```bash
resumebuilder create --from-file input/your_resume.yaml
```

## Testing

### Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=resumebuilder
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
