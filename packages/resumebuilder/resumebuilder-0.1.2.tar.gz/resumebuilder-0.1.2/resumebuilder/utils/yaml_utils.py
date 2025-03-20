#!/usr/bin/env python3
"""
Utilities for working with YAML files in the resume builder.
"""
import os
import yaml
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Import the ResumeData class
from resumebuilder.models.resume import ResumeData

def validate_schema(data: Dict[str, Any]) -> bool:
    """Validate schema using ResumeData model."""
    try:
        ResumeData.from_dict(data)
        return True
    except (ValueError, TypeError, KeyError) as e:
        print(f"Schema validation error: {str(e)}")
        return False


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """
    Load data from a YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary with loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file is not valid YAML
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data if data else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML format in {file_path}: {str(e)}")


def save_yaml_file(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a YAML file.
    
    Args:
        data: Dictionary with data to save
        file_path: Path to save the YAML file
        
    Raises:
        IOError: If the file can't be written
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
    except IOError as e:
        raise IOError(f"Failed to write YAML file {file_path}: {str(e)}")


def validate_resume_yaml(data: Dict[str, Any]) -> bool:
    """
    Validate resume YAML data.
    
    Args:
        data: Resume data to validate
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        ValueError: If the data is invalid
    """
    # Check required sections
    if not isinstance(data, dict):
        raise ValueError("Resume data must be a dictionary")
        
    # Check required personal information
    if 'personal' not in data or not isinstance(data['personal'], dict):
        raise ValueError("Resume data must contain a 'personal' section")
        
    personal = data['personal']
    required_personal_fields = ['name', 'title', 'email', 'phone', 'location']
    missing_fields = [field for field in required_personal_fields if field not in personal]
    if missing_fields:
        raise ValueError(f"Personal section is missing required fields: {', '.join(missing_fields)}")
    
    # Validate date formats in experience and education
    if 'experience' in data and isinstance(data['experience'], list):
        for i, exp in enumerate(data['experience']):
            if not _validate_date_format(exp.get('start_date', '')):
                raise ValueError(f"Invalid start_date format in experience entry #{i+1}")
            if not _validate_date_format(exp.get('end_date', '')):
                raise ValueError(f"Invalid end_date format in experience entry #{i+1}")
    
    if 'education' in data and isinstance(data['education'], list):
        for i, edu in enumerate(data['education']):
            if not _validate_date_format(edu.get('start_date', '')):
                raise ValueError(f"Invalid start_date format in education entry #{i+1}")
            if not _validate_date_format(edu.get('end_date', '')):
                raise ValueError(f"Invalid end_date format in education entry #{i+1}")
    
    # Use ResumeData for deeper validation
    try:
        ResumeData.from_dict(data)
        return True
    except (ValueError, TypeError, KeyError) as e:
        raise ValueError(f"Invalid resume data: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error validating resume data: {str(e)}")


def _validate_date_format(date_str: str) -> bool:
    """
    Validate a date string format.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not date_str or date_str.lower() == 'present':
        return True
        
    # Check for YYYY-MM format
    if len(date_str) == 7 and date_str[4] == '-':
        try:
            year = int(date_str[:4])
            month = int(date_str[5:7])
            if 1900 <= year <= 2100 and 1 <= month <= 12:
                return True
        except ValueError:
            pass
    
    # Check for Month YYYY format (e.g., January 2020, Jan 2020)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december',
              'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    
    parts = date_str.lower().split()
    if len(parts) == 2 and parts[0] in months:
        try:
            year = int(parts[1])
            if 1900 <= year <= 2100:
                return True
        except ValueError:
            pass
    
    return False


def generate_dummy_yaml() -> Dict[str, Any]:
    """
    Generate dummy resume data for testing.
    
    Returns:
        Dictionary with dummy resume data
    """
    current_date = datetime.now()
    years_ago_5 = current_date - timedelta(days=5*365)
    years_ago_3 = current_date - timedelta(days=3*365)
    years_ago_2 = current_date - timedelta(days=2*365)
    years_ago_1 = current_date - timedelta(days=1*365)
    
    # Format dates as YYYY-MM
    format_date = lambda dt: dt.strftime("%Y-%m")
    
    dummy_data = {
        'personal': {
            'name': 'John Doe',
            'title': 'Software Engineer',
            'email': 'john.doe@example.com',
            'phone': '+1 (555) 123-4567',
            'location': 'San Francisco, CA',
            'linkedin': 'linkedin.com/in/johndoe',
            'github': 'github.com/johndoe',
            'website': 'johndoe.com',
            'summary': 'Experienced software engineer with expertise in Python and web development.'
        },
        'experience': [
            {
                'company': 'Tech Company',
                'position': 'Senior Software Engineer',
                'location': 'San Francisco, CA',
                'start_date': format_date(years_ago_2),
                'end_date': 'Present',
                'responsibilities': [
                    'Led development of microservices architecture',
                    'Improved system performance by 30%',
                    'Mentored junior developers'
                ]
            },
            {
                'company': 'Startup Inc',
                'position': 'Software Engineer',
                'location': 'San Francisco, CA',
                'start_date': format_date(years_ago_5),
                'end_date': format_date(years_ago_2),
                'responsibilities': [
                    'Developed RESTful APIs',
                    'Implemented CI/CD pipeline',
                    'Worked on front-end using React'
                ]
            }
        ],
        'education': [
            {
                'institution': 'University of California',
                'degree': 'Bachelor of Science in Computer Science',
                'location': 'Berkeley, CA',
                'start_date': format_date(years_ago_5),
                'end_date': format_date(years_ago_1),
                'honors': 'Magna Cum Laude'
            }
        ],
        'skills': {
            'programming': [
                'Python',
                'JavaScript',
                'Java',
                'Go'
            ],
            'frameworks': [
                'Django',
                'React',
                'Spring Boot'
            ],
            'tools': [
                'Git',
                'Docker',
                'AWS',
                'CI/CD'
            ]
        },
        'certifications': [
            {
                'name': 'AWS Certified Developer',
                'issuer': 'Amazon Web Services',
                'date': format_date(years_ago_1),
                'expires': format_date(current_date + timedelta(days=365))
            }
        ]
    }
    
    return dummy_data 