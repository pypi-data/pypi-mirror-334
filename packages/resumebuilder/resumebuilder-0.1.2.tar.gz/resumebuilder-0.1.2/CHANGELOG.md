# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2024-03-17

### Changed
- Updated PyYAML from 6.0 to 6.0.1 for Python 3.12 compatibility
- Updated ReportLab from 3.6.12 to 4.0.9 for better Python 3.12 support
- Updated Pillow from 9.5.0 to 10.2.0 for improved Python 3.12 compatibility
- Enhanced GitHub Actions CI workflow to install all necessary system dependencies

### Fixed
- Fixed Python 3.12 compatibility issues in CI pipeline
- Added proper system dependencies for compiling C extensions in CI environment

## [0.1.1] - 2024-03-17

### Added
- Cleanup script (`scripts/cleanup.sh`) to remove generated files
- Documentation for DevOps processes in README.md
- GitHub Actions workflows for CI/CD:
  - CI workflow for testing and linting on pull requests
  - CD workflow for automatic PyPI publishing on new version tags
- MIT License
- Detailed instructions for releasing new versions
- Enhanced .gitignore to properly exclude generated files

### Changed
- Improved PyPI packaging support
- Added non-interactive mode via environment variables:
  - `RESUMEBUILDER_NON_INTERACTIVE`
  - `RESUMEBUILDER_COMPANY`
  - `RESUMEBUILDER_POSITION`

## [0.1.0] - 2024-03-17

### Added
- Initial release of ResumeBuilder
- Command-line interface with interactive prompts
- Support for generating professional PDF resumes
- Support for generating matching cover letters
- Multiple resume templates (modern, minimal, classic, creative)
- Data validation using Pydantic models
- Save resume data to YAML files for future updates
- Dummy data generation for template testing
- Comprehensive documentation

## [0.7.0] - 2024-05-15

### Added
- New PDF Analyzer tool in tools/ directory:
  - Standalone Python script for analyzing PDF documents
  - Extract text content from entire documents or specific pages
  - Analyze document structure and text density
  - Extract metadata (title, author, creation date)
  - Detect pages with images
  - Find hyperlinks within PDF documents
  - Identify form fields
  - Save analysis results to output files
- Comprehensive documentation for the PDF Analyzer tool:
  - Usage examples for resume and cover letter analysis
  - Command-line arguments reference
  - Troubleshooting guide
  - Integration with ResumeBuilder

## [0.6.0] - 2024-03-17

### Added
- Enhanced resume design and formatting:
  - Added blood orange styling for name and contact details
  - Implemented elegant border around resume and cover letter
  - Added intelligent page breaking to prevent section headings being separated from content
  - Forced page break after Experience section for better layout
  - Added italicized "References available upon request" text when no references are provided
- Improved cover letter formatting and styling:
  - Applied blood orange color to sender's name, address, and contact information
  - Added matching border to create visual consistency with resume
  - Improved email and phone links with proper formatting and colored links
  - Enhanced recipient information styling with proper spacing and alignment

### Changed
- Updated hyperlink styling to use blood orange across both resume and cover letter
- Optimized document structure for better readability and professional appearance
- Enhanced mobile compatibility with properly formatted tel: and mailto: links

## [0.5.1] - 2024-03-17

### Added
- New directory structure for better organization:
  - Created `input/` directory to store user resume YAML files
  - Created `output/pdfs/` directory for generated PDF files
  - Created `output/yaml/` directory for test/dummy data
- Updated README.md Project Structure section to reflect new organization

### Changed
- Modified code to save real resume files to input/ directory
- Dummy/test files are now stored in output/yaml/ directory
- PDF outputs are consistently saved to output/pdfs/ directory
- Removed references to docs/ directory from documentation
- Clean up test files (john_doe_resume.yaml and create_test_resume.sh)
- Added .gitkeep files to maintain empty directories in git

## [0.5.0] - 2024-03-16

### Added
- New agent-based workflow to replace launcher script:
  - Created INSTRUCTIONS.md with comprehensive agent instructions
  - Updated README.md with agent-based approach documentation
  - Added support for configuration through conversational commands
  - Simplified project generation process for users

### Changed
- Updated the project structure documentation to include new files
- Made agent-based approach the recommended method, with launcher as legacy option
- Improved process flow documentation to cover both approaches
- Enhanced Quick Start section with clearer instructions

## [0.4.1] - 2024-03-16

### Changed
- Removed "Planned Features" section from README.md to focus on current capabilities
- Updated documentation to reflect current project status

## [0.4.0] - 2024-03-16
### Changed
- Completely restructured README.md to follow a professional documentation format
- Improved project structure diagram
- Enhanced wording in all documentation sections
- Added emojis to section headings for better visual appeal
- Improved styling of table of contents with category emojis
- Better aligned documentation components for readability

### Added
- New Command Reference & Prompt Guide section with:
  - Common post-generation commands and examples
  - Instructions for extending helper scripts
  - Templates for structuring future AI prompts
- Automatic Git repository reinitialization:
  - Always reinitializes Git when using GitHub integration
  - Added `-t` option to reinitialize Git without GitHub
  - Creates a default .gitignore file when reinitializing

## [0.3.0] - 2024-03-16
### Changed
- Moved images directory from `genesis/images` to root directory for easier asset management
- Improved documentation clarity around project structure

### Added
- Support for agent mode with YOLO capabilities
- Enhanced automation for GitHub repository management
- Added detailed instructions for using agent/YOLO mode in README and PROMPT.md
- Added GENESIS_IMAGES_ROOT environment variable to launcher.sh

## [0.2.0] - 2024-03-16
### Changed
- Completely revamped Genesis to be fully AI-driven
- Removed all predefined templates and scripts
- Simplified the project structure to core essentials:
  - Configuration
  - SDS documentation
  - AI prompts
  - Launcher script

### Removed
- Removed template directories and files
- Removed script-based generation approach
- Removed manual configuration templates
- Removed predefined deployment configs

### Added
- Enhanced AI-driven project generation
- Simplified launcher with automatic cleanup
- Improved documentation for AI-based workflow
- Direct natural language project modification

## [0.1.0] - 2023-05-15
### Added
- Initial release of ResumeBuilder
- Command-line interface with interactive prompts
- Support for generating professional PDF resumes
- Support for generating matching cover letters
- Multiple resume templates (modern, minimal, classic, creative)
- Data validation using Pydantic models
- Save resume data to YAML files for future updates
- Dummy data generation for template testing
- Comprehensive documentation 