#!/usr/bin/env python3
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, validator
import re
from datetime import datetime

# Date format mapping for common month names
MONTH_MAPPING = {
    'january': '01', 'jan': '01',
    'february': '02', 'feb': '02',
    'march': '03', 'mar': '03',
    'april': '04', 'apr': '04',
    'may': '05',
    'june': '06', 'jun': '06',
    'july': '07', 'jul': '07',
    'august': '08', 'aug': '08',
    'september': '09', 'sep': '09', 'sept': '09',
    'october': '10', 'oct': '10',
    'november': '11', 'nov': '11',
    'december': '12', 'dec': '12'
}

def convert_to_yyyy_mm(date_str):
    """Convert various date formats to YYYY-MM format."""
    if date_str.lower() == 'present':
        return 'Present'
    
    # If already in YYYY-MM format
    if re.match(r'^\d{4}-\d{2}$', date_str):
        year, month = date_str.split('-')
        if 1 <= int(month) <= 12:
            return date_str
    
    # Try to parse Month YYYY (e.g. "January 2023" or "Jan 2023")
    month_year_pattern = re.match(r'^([A-Za-z]+)\s+(\d{4})$', date_str)
    if month_year_pattern:
        month_name, year = month_year_pattern.groups()
        month_name = month_name.lower()
        if month_name in MONTH_MAPPING:
            return f"{year}-{MONTH_MAPPING[month_name]}"
    
    # Try to parse Month Day, Year (e.g. "January 15, 2023" or "Jan 15, 2023")
    full_date_pattern = re.match(r'^([A-Za-z]+)\s+\d{1,2},?\s+(\d{4})$', date_str)
    if full_date_pattern:
        month_name, year = full_date_pattern.groups()
        month_name = month_name.lower()
        if month_name in MONTH_MAPPING:
            return f"{year}-{MONTH_MAPPING[month_name]}"
    
    # If can't parse, raise error
    raise ValueError("Date must be in YYYY-MM format, 'Month YYYY', or 'Month Day, YYYY' format")


class Personal(BaseModel):
    """Personal information for the resume."""
    name: str
    title: str
    email: str
    phone: str
    location: str  # Format as: 'Street Number & Name, City, State, Country'
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    references: Optional[str] = "References available upon request"

    @validator('email')
    def validate_email(cls, v):
        """Format email with mailto link if not already formatted."""
        if not v.startswith('mailto:'):
            return f"mailto:{v}"
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        """Format phone with tel link if not already formatted."""
        if not v.startswith('tel:'):
            # Remove any non-digit characters except + for country code
            clean_phone = ''.join(c for c in v if c.isdigit() or c == '+')
            return f"tel:{clean_phone}"
        return v
    
    @validator('github')
    def validate_github(cls, v):
        """Format GitHub URL if not already formatted."""
        if v and not v.startswith(('http://', 'https://')):
            if not v.startswith('github.com/'):
                return f"https://github.com/{v}"
            return f"https://{v}"
        return v
    
    @validator('website')
    def validate_website(cls, v):
        """Format website URL if not already formatted."""
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v


class Experience(BaseModel):
    """Employment history entry."""
    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    responsibilities: List[str]

    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        """Validate and convert date format."""
        if v.lower() == 'present':
            return 'Present'
        
        try:
            return convert_to_yyyy_mm(v)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM format, 'Month YYYY', or 'Month Day, YYYY' format")


class Education(BaseModel):
    """Education history entry."""
    institution: str
    degree: str
    location: str
    start_date: str
    end_date: str
    honors: Optional[str] = None

    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        """Validate and convert date format."""
        if v.lower() == 'present':
            return 'Present'
        
        try:
            return convert_to_yyyy_mm(v)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM format, 'Month YYYY', or 'Month Day, YYYY' format")


class Certification(BaseModel):
    """Certification entry."""
    name: str
    issuer: str
    date: str
    expires: Optional[str] = "Never"

    @validator('date')
    def validate_date(cls, v):
        """Validate and convert date format."""
        try:
            return convert_to_yyyy_mm(v)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM format, 'Month YYYY', or 'Month Day, YYYY' format")

    @validator('expires')
    def validate_expires(cls, v):
        """Validate and convert expiration date format."""
        if v.lower() in ('never', ''):
            return 'Never'
        
        try:
            return convert_to_yyyy_mm(v)
        except ValueError:
            raise ValueError("Expiration date must be in YYYY-MM format, 'Month YYYY', 'Month Day, YYYY', or 'Never'")


class CoverLetter(BaseModel):
    """Cover letter data model."""
    recipient_name: str = "Hiring Manager"
    company_name: str
    position: str
    company_address: Optional[str] = None
    greeting: str = "Dear Hiring Manager"
    paragraphs: List[str]
    content: Optional[str] = None  # For full cover letter content from a text file

    @classmethod
    def from_file(cls, file_path: str, **kwargs) -> 'CoverLetter':
        """Load cover letter content from a text file."""
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Parse the content more intelligently
        lines = [line.strip() for line in content.split('\n')]
        paragraphs = []
        metadata = {}
        
        # Check if the file might contain header metadata
        # Look for header section followed by an empty line
        header_section = []
        current_paragraph = []
        body_paragraphs = []
        i = 0

        # Extract potential header (first lines until we hit an empty line)
        while i < len(lines) and (i < 10):  # Limit header to first 10 lines max
            line = lines[i]
            i += 1
            if not line:
                if header_section:  # We've found the end of the header section
                    break
                else:
                    continue  # Skip leading empty lines
            header_section.append(line)
        
        # Process the body paragraphs (after the header)
        while i < len(lines):
            line = lines[i]
            i += 1
            
            if not line:  # Empty line means end of paragraph
                if current_paragraph:
                    body_paragraphs.append(" ".join(current_paragraph))
                    current_paragraph = []
            else:
                current_paragraph.append(line)
        
        # Don't forget the last paragraph
        if current_paragraph:
            body_paragraphs.append(" ".join(current_paragraph))
        
        # Process the header section to extract metadata
        if header_section:
            # First line is often company name
            if 'company_name' not in kwargs and len(header_section) >= 1:
                metadata['company_name'] = header_section[0]
                
            # Second line is often position
            if 'position' not in kwargs and len(header_section) >= 2:
                metadata['position'] = header_section[1]
                
            # Third line is often recipient name
            if 'recipient_name' not in kwargs and len(header_section) >= 3:
                metadata['recipient_name'] = header_section[2]
                
            # Fourth line could be recipient title or address
            if len(header_section) >= 4:
                if len(header_section[3]) < 30:  # If it looks like a title (shorter)
                    metadata['recipient_title'] = header_section[3]
                else:
                    metadata['company_address'] = header_section[3]
            
            # Check if there's a greeting line in the first paragraph
            if body_paragraphs and body_paragraphs[0].startswith('Dear '):
                metadata['greeting'] = body_paragraphs[0]
                body_paragraphs.pop(0)  # Remove greeting from body paragraphs
        
        # If no company name provided, use a default
        if 'company_name' not in metadata and 'company_name' not in kwargs:
            metadata['company_name'] = "Company"
            
        # If no position provided, use a default
        if 'position' not in metadata and 'position' not in kwargs:
            metadata['position'] = "Position"
        
        # Command line parameters should override file metadata
        final_data = {**metadata, **kwargs}
        
        # Use the body paragraphs
        return cls(
            content=content,
            paragraphs=body_paragraphs,
            **final_data
        )


class ResumeData(BaseModel):
    """Complete resume data model."""
    personal: Personal
    experience: List[Experience]
    education: List[Education]
    skills: Dict[str, List[str]]
    certifications: Optional[List[Certification]] = []
    cover_letter: Optional[CoverLetter] = None  # Optional cover letter data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResumeData':
        """
        Create a ResumeData instance from a dictionary.
        
        Args:
            data: Dictionary with resume data
            
        Returns:
            ResumeData instance
            
        Raises:
            ValueError: If the data is invalid
        """
        try:
            return cls(**data)
        except Exception as e:
            raise ValueError(f"Invalid resume data: {str(e)}") 