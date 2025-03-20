#!/usr/bin/env python3
"""
Module for interactive input handling for the resume builder.
"""
from typing import Dict, List, Any, Optional


def get_personal_info() -> Dict[str, str]:
    """
    Interactively collect personal information from the user.
    
    Returns:
        Dictionary containing personal information
    """
    personal_info = {}
    print("\nEnter your personal information:")
    
    personal_info['name'] = input("Full name: ")
    personal_info['title'] = input("Professional title: ")
    personal_info['email'] = input("Email address: ")
    personal_info['phone'] = input("Phone number: ")
    personal_info['location'] = input("Location (City, State/Country): ")
    
    # Optional fields
    linkedin = input("LinkedIn URL (optional): ")
    if linkedin:
        personal_info['linkedin'] = linkedin
        
    github = input("GitHub URL (optional): ")
    if github:
        personal_info['github'] = github
        
    website = input("Personal website (optional): ")
    if website:
        personal_info['website'] = website
        
    summary = input("Professional summary (optional): ")
    if summary:
        personal_info['summary'] = summary
    
    return personal_info


def get_experience_entries() -> List[Dict[str, Any]]:
    """
    Interactively collect work experience entries from the user.
    
    Returns:
        List of dictionaries containing work experience
    """
    experiences = []
    print("\nEnter your work experience (leave company blank when done):")
    
    while True:
        print("\nExperience entry:")
        company = input("Company name: ")
        if not company:
            break
            
        position = input("Position/Title: ")
        location = input("Location: ")
        start_date = input("Start date (YYYY-MM or Month YYYY): ")
        end_date = input("End date (YYYY-MM, Month YYYY, or 'Present'): ")
        
        print("Enter responsibilities/achievements (one per line, leave blank when done):")
        responsibilities = []
        while True:
            resp = input("- ")
            if not resp:
                break
            responsibilities.append(resp)
        
        experience = {
            'company': company,
            'position': position,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'responsibilities': responsibilities
        }
        
        experiences.append(experience)
    
    return experiences


def get_education_entries() -> List[Dict[str, Any]]:
    """
    Interactively collect education entries from the user.
    
    Returns:
        List of dictionaries containing education
    """
    education_entries = []
    print("\nEnter your education (leave institution blank when done):")
    
    while True:
        print("\nEducation entry:")
        institution = input("Institution name: ")
        if not institution:
            break
            
        degree = input("Degree/Certificate: ")
        location = input("Location: ")
        start_date = input("Start date (YYYY-MM or Month YYYY): ")
        end_date = input("End date (YYYY-MM, Month YYYY, or 'Present'): ")
        
        # Optional fields
        honors = input("Honors/GPA (optional): ")
        
        education = {
            'institution': institution,
            'degree': degree,
            'location': location,
            'start_date': start_date,
            'end_date': end_date
        }
        
        if honors:
            education['honors'] = honors
        
        education_entries.append(education)
    
    return education_entries


def get_skills() -> Dict[str, List[str]]:
    """
    Interactively collect skills from the user.
    
    Returns:
        Dictionary of skill categories and skills
    """
    skills = {}
    print("\nEnter your skills by category (leave category blank when done):")
    
    while True:
        category = input("\nSkill category (e.g., Programming, Languages): ")
        if not category:
            break
            
        print(f"Enter {category} skills (one per line, leave blank when done):")
        skill_list = []
        while True:
            skill = input("- ")
            if not skill:
                break
            skill_list.append(skill)
        
        if skill_list:
            skills[category] = skill_list
    
    return skills


def get_certifications() -> List[Dict[str, str]]:
    """
    Interactively collect certifications from the user.
    
    Returns:
        List of dictionaries containing certifications
    """
    certifications = []
    print("\nEnter your certifications (leave name blank when done):")
    
    while True:
        print("\nCertification entry:")
        name = input("Certification name: ")
        if not name:
            break
            
        issuer = input("Issuing organization: ")
        date = input("Date obtained (YYYY-MM or Month YYYY): ")
        
        # Optional fields
        expiry = input("Expiration date (optional): ")
        
        certification = {
            'name': name,
            'issuer': issuer,
            'date': date
        }
        
        if expiry:
            certification['expires'] = expiry
        
        certifications.append(certification)
    
    return certifications


def get_resume_data_interactively() -> Dict[str, Any]:
    """
    Collect all resume data interactively from the user.
    
    Returns:
        Complete resume data dictionary
    """
    print("Welcome to the Resume Builder!")
    print("Let's create your professional resume step by step.")
    
    resume_data = {}
    
    # Get personal information
    resume_data['personal'] = get_personal_info()
    
    # Get work experience
    experience = get_experience_entries()
    if experience:
        resume_data['experience'] = experience
    
    # Get education
    education = get_education_entries()
    if education:
        resume_data['education'] = education
    
    # Get skills
    skills = get_skills()
    if skills:
        resume_data['skills'] = skills
    
    # Get certifications
    certifications = get_certifications()
    if certifications:
        resume_data['certifications'] = certifications
    
    print("\nGreat! All your resume information has been collected.")
    return resume_data 