#!/usr/bin/env python3
import os
from typing import Dict, List, Any, Optional, Tuple

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable

from resumebuilder.models.resume import ResumeData, CoverLetter
from resumebuilder.templates.template_manager import get_template


def generate_resume_pdf(resume_data: ResumeData, template_name: str, output_file: str) -> None:
    """
    Generate a PDF resume based on the provided data and template.
    
    Args:
        resume_data: Resume data model
        template_name: Name of the template to use
        output_file: Path to save the PDF file
        
    Raises:
        ValueError: If the template doesn't exist
    """
    # Get the template configuration
    template_config = get_template(template_name)
    
    # Define blood orange color for consistency with cover letter
    blood_orange = colors.HexColor('#D84B20')
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        leftMargin=template_config['margins'][3] * inch,
        rightMargin=template_config['margins'][1] * inch,
        topMargin=template_config['margins'][0] * inch,
        bottomMargin=template_config['margins'][2] * inch
    )
    
    # Function to draw the blood orange border (simple line)
    def add_border(canvas, doc):
        # Get page dimensions
        page_width, page_height = letter
        
        # Get margin dimensions from the document
        left_margin = doc.leftMargin
        right_margin = doc.rightMargin
        top_margin = doc.topMargin
        bottom_margin = doc.bottomMargin
        
        # Calculate border position - slightly adjusted from halfway for better aesthetics
        # Use the 40% point between edge and margin for a more elegant look
        border_left = left_margin * 0.4
        border_right = page_width - (right_margin * 0.4)
        border_top = page_height - (top_margin * 0.4)
        border_bottom = bottom_margin * 0.4
        
        # Set color and line width
        canvas.setStrokeColor(blood_orange)
        canvas.setLineWidth(1.0)  # Thinner line for elegance
        
        # Draw the rectangle with straight lines
        canvas.rect(border_left, border_bottom, border_right - border_left, border_top - border_bottom, stroke=1, fill=0)
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Helper function to add styles without causing conflicts
    def add_style_if_not_exists(styles, style_name, parent_style, **kwargs):
        try:
            # Try to directly modify the existing style if it exists
            if style_name in styles:
                print(f"Style '{style_name}' already exists, modifying instead of adding")
                # Get the existing style
                existing_style = styles[style_name]
                # Update its properties
                for key, value in kwargs.items():
                    setattr(existing_style, key, value)
            else:
                # If the style doesn't exist, add it normally
                print(f"Adding new style: '{style_name}'")
                styles.add(ParagraphStyle(
                    name=style_name,
                    parent=parent_style,
                    **kwargs
                ))
        except Exception as e:
            print(f"Error handling style '{style_name}': {str(e)}")
    
    # Create custom styles based on the template
    add_style_if_not_exists(
        styles, 
        'Heading1',
        styles['Heading1'],
        fontName=template_config['font_header'],
        fontSize=16,
        textColor=blood_orange,  # Changed to blood orange color
        spaceAfter=10
    )
    
    add_style_if_not_exists(
        styles,
        'Heading2',
        styles['Heading2'],
        fontName=template_config['font_header'],
        fontSize=14,
        textColor=colors.HexColor(template_config['color_primary']),
        spaceAfter=8
    )
    
    add_style_if_not_exists(
        styles,
        'Normal',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceAfter=6
    )
    
    add_style_if_not_exists(
        styles,
        'Bold',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        fontWeight='bold'
    )
    
    add_style_if_not_exists(
        styles,
        'Contact',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=10,
        textColor=blood_orange,  # Changed to blood orange color
        spaceAfter=2
    )
    
    add_style_if_not_exists(
        styles,
        'Link',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=10,
        textColor=blood_orange,  # Changed to blood orange color
        underline=True
    )
    
    # Helper function to create hyperlinks with custom color
    def create_hyperlink_colored(url, display_text=None, color=blood_orange):
        if not display_text:
            display_text = url
        color_hex = color.hexval()[2:]  # Convert color to hex without # prefix
        return f'<a href="{url}" color="#{color_hex}" underline="1">{display_text}</a>'
    
    # For backward compatibility
    def create_hyperlink(url, display_text=None):
        return create_hyperlink_colored(url, display_text, blood_orange)
    
    # Format phone number for display (remove country code and formatting)
    def format_phone_for_display(phone_number):
        phone_display = phone_number.replace('tel:', '')
        # Strip out any non-digit characters except last 10 digits for display
        if len(phone_display) > 10:
            digits_only = ''.join(c for c in phone_display if c.isdigit())
            if len(digits_only) >= 10:
                last_10_digits = digits_only[-10:]
                return f"({last_10_digits[:3]}) {last_10_digits[3:6]}-{last_10_digits[6:]}"
        return phone_display
    
    # Helper function to format dates
    def format_date_for_display(date_str):
        """Convert dates from YYYY-MM format to Month Year format."""
        if date_str.lower() == 'present':
            return 'Present'
        
        # Parse YYYY-MM format
        try:
            year, month = date_str.split('-')
            # Convert month number to name
            month_names = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
            month_name = month_names[int(month) - 1]
            return f"{month_name} {year}"
        except:
            # If parsing fails, return the original string
            return date_str
    
    # Build the document elements
    elements = []
    
    # Add personal information header
    if template_config['header_style'] == 'centered':
        elements.append(Paragraph(resume_data.personal.name, styles['Heading1']))
        elements.append(Paragraph(resume_data.personal.title, styles['Bold']))
        
        # Create contact links with hyperlinks
        email_link = create_hyperlink_colored(resume_data.personal.email, resume_data.personal.email.replace('mailto:', ''))
        phone_display = format_phone_for_display(resume_data.personal.phone)
        phone_link = create_hyperlink_colored(resume_data.personal.phone, phone_display)
        
        # Contact information
        contact_info = f"{email_link} | {phone_link} | {resume_data.personal.location}"
        elements.append(Paragraph(contact_info, styles['Contact']))
        
        # Links
        links = []
        if resume_data.personal.linkedin:
            links.append(create_hyperlink_colored(resume_data.personal.linkedin, "LinkedIn"))
        if resume_data.personal.github:
            links.append(create_hyperlink_colored(resume_data.personal.github, "GitHub"))
        if resume_data.personal.website:
            website_display = resume_data.personal.website.replace('https://', '').replace('http://', '')
            links.append(create_hyperlink_colored(resume_data.personal.website, website_display))
        
        if links:
            links_text = " | ".join(links)
            elements.append(Paragraph(links_text, styles['Contact']))
    
    elif template_config['header_style'] == 'traditional':
        elements.append(Paragraph(resume_data.personal.name, styles['Heading1']))
        elements.append(Paragraph(resume_data.personal.title, styles['Bold']))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Contact information with hyperlinks
        email_link = create_hyperlink_colored(resume_data.personal.email, resume_data.personal.email.replace('mailto:', ''))
        phone_display = format_phone_for_display(resume_data.personal.phone)
        phone_link = create_hyperlink_colored(resume_data.personal.phone, phone_display)
        
        elements.append(Paragraph(f"Email: {email_link}", styles['Contact']))
        elements.append(Paragraph(f"Phone: {phone_link}", styles['Contact']))
        elements.append(Paragraph(f"Location: {resume_data.personal.location}", styles['Contact']))
        
        # Links
        if resume_data.personal.linkedin:
            elements.append(Paragraph(f"LinkedIn: {create_hyperlink_colored(resume_data.personal.linkedin)}", styles['Contact']))
        if resume_data.personal.github:
            elements.append(Paragraph(f"GitHub: {create_hyperlink_colored(resume_data.personal.github)}", styles['Contact']))
        if resume_data.personal.website:
            website_display = resume_data.personal.website.replace('https://', '').replace('http://', '')
            elements.append(Paragraph(f"Website: {create_hyperlink_colored(resume_data.personal.website, website_display)}", styles['Contact']))
    
    elif template_config['header_style'] == 'box':
        # Create a boxed header
        # This is a simplified version; in a real implementation, this would use more advanced layout
        elements.append(Paragraph(resume_data.personal.name, styles['Heading1']))
        elements.append(Paragraph(resume_data.personal.title, styles['Bold']))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Contact information in a table with hyperlinks
        email_link = create_hyperlink_colored(resume_data.personal.email, resume_data.personal.email.replace('mailto:', ''))
        phone_display = format_phone_for_display(resume_data.personal.phone)
        phone_link = create_hyperlink_colored(resume_data.personal.phone, phone_display)
        
        contact_data = [
            [Paragraph("Email:", styles['Bold']), Paragraph(email_link, styles['Normal'])],
            [Paragraph("Phone:", styles['Bold']), Paragraph(phone_link, styles['Normal'])],
            [Paragraph("Location:", styles['Bold']), Paragraph(resume_data.personal.location, styles['Normal'])]
        ]
        
        if resume_data.personal.linkedin:
            contact_data.append([Paragraph("LinkedIn:", styles['Bold']), 
                                Paragraph(create_hyperlink_colored(resume_data.personal.linkedin), styles['Normal'])])
        
        if resume_data.personal.github:
            contact_data.append([Paragraph("GitHub:", styles['Bold']), 
                                Paragraph(create_hyperlink_colored(resume_data.personal.github), styles['Normal'])])
        
        if resume_data.personal.website:
            website_display = resume_data.personal.website.replace('https://', '').replace('http://', '')
            contact_data.append([Paragraph("Website:", styles['Bold']), 
                                Paragraph(create_hyperlink_colored(resume_data.personal.website, website_display), styles['Normal'])])
        
        contact_table = Table(contact_data, colWidths=[1.2 * inch, 4 * inch])
        contact_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        elements.append(contact_table)
    
    else:  # simple header
        elements.append(Paragraph(resume_data.personal.name, styles['Heading1']))
        elements.append(Paragraph(resume_data.personal.title, styles['Bold']))
        
        # Contact information with hyperlinks
        email_link = create_hyperlink_colored(resume_data.personal.email, resume_data.personal.email.replace('mailto:', ''))
        phone_display = format_phone_for_display(resume_data.personal.phone)
        phone_link = create_hyperlink_colored(resume_data.personal.phone, phone_display)
        
        elements.append(Paragraph(f"{email_link} | {phone_link}", styles['Contact']))
        elements.append(Paragraph(resume_data.personal.location, styles['Contact']))
        
        # Links for GitHub, LinkedIn and personal website
        links = []
        if resume_data.personal.linkedin:
            links.append(create_hyperlink_colored(resume_data.personal.linkedin, "LinkedIn"))
        if resume_data.personal.github:
            links.append(create_hyperlink_colored(resume_data.personal.github, "GitHub"))
        if resume_data.personal.website:
            website_display = resume_data.personal.website.replace('https://', '').replace('http://', '')
            links.append(create_hyperlink_colored(resume_data.personal.website, website_display))
        
        if links:
            links_text = " | ".join(links)
            elements.append(Paragraph(links_text, styles['Contact']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Add experience section - with intelligent page breaking
    section_title = Paragraph("EXPERIENCE", styles['Heading2'])
    elements.append(section_title)

    # Create a special style for job titles - larger and bolder than normal text
    add_style_if_not_exists(
        styles,
        'JobTitle',
        styles['Bold'],
        fontSize=12,
        textColor=blood_orange,
        spaceAfter=2
    )

    for i, job in enumerate(resume_data.experience):
        job_elements = []
        
        job_header = f"{job.position}, {job.company} - {job.location}"
        job_elements.append(Paragraph(job_header, styles['JobTitle']))
        
        date_range = f"{format_date_for_display(job.start_date)} - {format_date_for_display(job.end_date)}"
        job_elements.append(Paragraph(date_range, styles['Contact']))
        
        for resp in job.responsibilities:
            job_elements.append(Paragraph(f"• {resp}", styles['Normal']))
        
        # Add extra space between job experiences
        job_elements.append(Spacer(1, 0.25 * inch))
        
        # Keep each job together as a unit
        elements.append(KeepTogether(job_elements))

    # Add a page break after the experience section
    elements.append(PageBreak())
    
    # Add education section with intelligent page breaks
    section_title = Paragraph("EDUCATION", styles['Heading2'])
    elements.append(section_title)

    for edu in resume_data.education:
        edu_elements = []
        
        edu_header = f"{edu.degree}, {edu.institution} - {edu.location}"
        edu_elements.append(Paragraph(edu_header, styles['Bold']))
        
        date_range = f"{format_date_for_display(edu.start_date)} - {format_date_for_display(edu.end_date)}"
        edu_elements.append(Paragraph(date_range, styles['Contact']))
        
        if edu.honors:
            edu_elements.append(Paragraph(f"Honors: {edu.honors}", styles['Normal']))
        
        edu_elements.append(Spacer(1, 0.1 * inch))
        
        # Keep each education entry together
        elements.append(KeepTogether(edu_elements))

    elements.append(Spacer(1, 0.1 * inch))
    
    # Add skills section with intelligent page breaks
    section_title = Paragraph("SKILLS", styles['Heading2'])
    elements.append(section_title)

    for category, skills_list in resume_data.skills.items():
        skill_elements = []
        
        skill_elements.append(Paragraph(category, styles['Bold']))
        skills_text = ", ".join(skills_list)
        skill_elements.append(Paragraph(skills_text, styles['Normal']))
        skill_elements.append(Spacer(1, 0.05 * inch))
        
        # Keep each skill category together
        elements.append(KeepTogether(skill_elements))

    elements.append(Spacer(1, 0.1 * inch))
    
    # Add certifications section if present, with intelligent page breaks
    if resume_data.certifications:
        section_title = Paragraph("CERTIFICATIONS", styles['Heading2'])
        elements.append(section_title)
        
        for cert in resume_data.certifications:
            cert_elements = []
            
            cert_header = f"{cert.name}, {cert.issuer}"
            cert_elements.append(Paragraph(cert_header, styles['Bold']))
            
            date_info = f"Obtained: {format_date_for_display(cert.date)}"
            if cert.expires.lower() != "never":
                date_info += f" | Expires: {format_date_for_display(cert.expires)}"
            
            cert_elements.append(Paragraph(date_info, styles['Contact']))
            cert_elements.append(Spacer(1, 0.05 * inch))
            
            # Keep each certification together
            elements.append(KeepTogether(cert_elements))

    # Add references section at the end if it exists
    if resume_data.personal.references:
        elements.append(Spacer(1, 0.2 * inch))
        
        ref_elements = [
            Paragraph("REFERENCES", styles['Heading2']),
            Paragraph(resume_data.personal.references, styles['Normal'])
        ]
        
        # Keep the references section together
        elements.append(KeepTogether(ref_elements))
    else:
        # If no references are provided, add a note that they're available upon request
        elements.append(Spacer(1, 0.2 * inch))
        
        # Create italic style for the references note
        add_style_if_not_exists(
            styles,
            'Italic',
            styles['Normal'],
            fontName=template_config['font_main'],
            fontSize=11,
            italic=True,
            alignment=1  # Center alignment
        )
        
        elements.append(Paragraph("References available upon request", styles['Italic']))

    # Build the document with the blood orange border
    doc.build(elements, onFirstPage=add_border, onLaterPages=add_border)


def generate_cover_letter_pdf(resume_data: ResumeData, cover_letter_data: Dict[str, Any], 
                             template_name: str, output_file: str) -> None:
    """
    Generate a PDF cover letter based on the provided data and template.
    
    Args:
        resume_data: Resume data model
        cover_letter_data: Cover letter data
        template_name: Name of the template to use
        output_file: Path to save the PDF file
        
    Raises:
        ValueError: If the template doesn't exist
    """
    # Get the template configuration
    template_config = get_template(template_name)
    
    # Define blood orange color and its complementary color
    blood_orange = colors.HexColor('#D84B20')  # Blood orange color
    teal_blue = colors.HexColor('#20B8D8')  # Complementary color (teal blue)
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        leftMargin=template_config['margins'][3] * inch,
        rightMargin=template_config['margins'][1] * inch,
        topMargin=template_config['margins'][0] * inch,
        bottomMargin=template_config['margins'][2] * inch
    )
    
    # Function to draw the blood orange border (simple line)
    def add_border(canvas, doc):
        # Get page dimensions
        page_width, page_height = letter
        
        # Get margin dimensions from the document
        left_margin = doc.leftMargin
        right_margin = doc.rightMargin
        top_margin = doc.topMargin
        bottom_margin = doc.bottomMargin
        
        # Calculate border position - slightly adjusted from halfway for better aesthetics
        # Use the 40% point between edge and margin for a more elegant look
        border_left = left_margin * 0.4
        border_right = page_width - (right_margin * 0.4)
        border_top = page_height - (top_margin * 0.4)
        border_bottom = bottom_margin * 0.4
        
        # Set color and line width
        canvas.setStrokeColor(blood_orange)
        canvas.setLineWidth(1.0)  # Thinner line for elegance
        
        # Draw the rectangle with straight lines
        canvas.rect(border_left, border_bottom, border_right - border_left, border_top - border_bottom, stroke=1, fill=0)
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Helper function to add styles without causing conflicts
    def add_style_if_not_exists(styles, style_name, parent_style, **kwargs):
        try:
            # Try to directly modify the existing style if it exists
            if style_name in styles:
                print(f"Style '{style_name}' already exists, modifying instead of adding")
                # Get the existing style
                existing_style = styles[style_name]
                # Update its properties
                for key, value in kwargs.items():
                    setattr(existing_style, key, value)
            else:
                # If the style doesn't exist, add it normally
                print(f"Adding new style: '{style_name}'")
                styles.add(ParagraphStyle(
                    name=style_name,
                    parent=parent_style,
                    **kwargs
                ))
        except Exception as e:
            print(f"Error handling style '{style_name}': {str(e)}")
    
    # Helper function to create hyperlinks with custom color
    def create_hyperlink_colored(url, display_text=None, color=blood_orange):
        if not display_text:
            display_text = url
        color_hex = color.hexval()[2:]  # Convert color to hex without # prefix
        return f'<a href="{url}" color="#{color_hex}" underline="1">{display_text}</a>'
    
    # For backward compatibility
    def create_hyperlink(url, display_text=None):
        return create_hyperlink_colored(url, display_text, blood_orange)
    
    # Format phone number for display (remove country code and formatting)
    def format_phone_for_display(phone_number):
        phone_display = phone_number.replace('tel:', '')
        # Strip out any non-digit characters except last 10 digits for display
        if len(phone_display) > 10:
            digits_only = ''.join(c for c in phone_display if c.isdigit())
            if len(digits_only) >= 10:
                last_10_digits = digits_only[-10:]
                return f"({last_10_digits[:3]}) {last_10_digits[3:6]}-{last_10_digits[6:]}"
        return phone_display
    
    # Helper function to format dates
    def format_date_for_display(date_str):
        """Convert dates from YYYY-MM format to Month Year format."""
        if date_str.lower() == 'present':
            return 'Present'
        
        # Parse YYYY-MM format
        try:
            year, month = date_str.split('-')
            # Convert month number to name
            month_names = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
            month_name = month_names[int(month) - 1]
            return f"{month_name} {year}"
        except:
            # If parsing fails, return the original string
            return date_str
    
    # Create custom styles based on the template
    add_style_if_not_exists(
        styles,
        'Name',
        styles['Normal'],  # Changed from Heading1 to Normal to match body text size
        fontName=template_config['font_header'],
        fontSize=11,  # Changed to same size as normal text
        textColor=blood_orange,  # Changed to blood orange color
        fontWeight='bold',  # Make it bold
        alignment=0,  # Left alignment
        spaceAfter=2
    )
    
    add_style_if_not_exists(
        styles,
        'PageTitle',
        styles['Heading1'],
        fontName=template_config['font_header'],
        fontSize=16,
        textColor=teal_blue,  # Changed to teal blue (complementary to blood orange)
        alignment=1,  # Center alignment
        spaceAfter=12
    )
    
    add_style_if_not_exists(
        styles,
        'Title',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=12,
        textColor=colors.HexColor(template_config['color_secondary']),
        spaceAfter=4
    )
    
    add_style_if_not_exists(
        styles,
        'Normal',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceAfter=12,  # Double spacing
        alignment=0     # Left alignment
    )
    
    add_style_if_not_exists(
        styles,
        'Address',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        textColor=blood_orange,  # Changed to blood orange color
        fontWeight='bold',  # Make it bold
        spaceAfter=2,
        alignment=0  # Left alignment
    )
    
    add_style_if_not_exists(
        styles,
        'Date',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        alignment=0,  # Left alignment
        spaceAfter=12  # Double spacing
    )
    
    add_style_if_not_exists(
        styles,
        'Greeting',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceBefore=0,
        spaceAfter=12  # Double spacing
    )
    
    add_style_if_not_exists(
        styles,
        'Paragraph',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceBefore=0,
        spaceAfter=12,  # Double spacing
        firstLineIndent=0  # Remove tab/indentation (changed from 20)
    )
    
    add_style_if_not_exists(
        styles,
        'Closing',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceBefore=0,
        spaceAfter=12,  # Double spacing
        alignment=0     # Left alignment
    )
    
    add_style_if_not_exists(
        styles,
        'Signature',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        textColor=blood_orange,  # Changed to blood orange color
        fontWeight='bold',  # Make it bold
        spaceBefore=24,  # Extra space for signature
        spaceAfter=0
    )
    
    add_style_if_not_exists(
        styles,
        'ContactInfo',
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        textColor=blood_orange,  # Changed to blood orange color
        fontWeight='bold',  # Make it bold
        spaceAfter=2,
        alignment=0  # Left alignment
    )
    
    add_style_if_not_exists(
        styles,
        'RecipientInfo',  # New style for recipient information
        styles['Normal'],
        fontName=template_config['font_main'],
        fontSize=11,
        spaceAfter=2,
        alignment=0  # Left alignment
    )
    
    # Format contact information
    email_display = resume_data.personal.email.replace('mailto:', '')
    email_link = create_hyperlink_colored(resume_data.personal.email, email_display, blood_orange)
    
    # Format phone number for display
    phone_display = format_phone_for_display(resume_data.personal.phone)
    phone_link = create_hyperlink_colored(resume_data.personal.phone, phone_display, blood_orange)
    
    # Build the document elements
    elements = []
    
    # No longer adding page title
    # title_text = f"Cover Letter for {cover_letter_data.get('company_name', 'Company')}"
    # elements.append(Paragraph(title_text, styles['PageTitle']))

    # Add sender's name
    elements.append(Paragraph(resume_data.personal.name, styles['Name']))
    
    # Add sender's address - properly formatted with street, city/state/zip combined
    address_parts = resume_data.personal.location.split(',')
    if len(address_parts) >= 3:
        # First line is the street address
        elements.append(Paragraph(address_parts[0].strip(), styles['Address']))
        
        # Second line is City, State ZIP combined
        city_state_zip = f"{address_parts[1].strip()}, {address_parts[2].strip()}"
        if len(address_parts) >= 4:  # If there's a country
            elements.append(Paragraph(city_state_zip, styles['Address']))
            elements.append(Paragraph(address_parts[3].strip(), styles['Address']))
        else:
            elements.append(Paragraph(city_state_zip, styles['Address']))
    else:
        # Fallback for addresses that don't match expected format
        for part in address_parts:
            elements.append(Paragraph(part.strip(), styles['Address']))
    
    elements.append(Spacer(1, 0.3 * inch))  # Space between sender and recipient
    
    # Add recipient information - always include name and company even if address is not provided
    if cover_letter_data.get('recipient_name'):
        # Add recipient name
        elements.append(Paragraph(cover_letter_data['recipient_name'], styles['RecipientInfo']))

    if cover_letter_data.get('company_name'):    
        # Add company name
        elements.append(Paragraph(cover_letter_data['company_name'], styles['RecipientInfo']))
        
    # Only add the address details if company_address is provided
    if cover_letter_data.get('company_address'):
        # Format company address correctly - proper splitting of address parts
        # Common address format is: "Street, City, State ZIP, Country"
        if ',' in cover_letter_data['company_address']:
            address_parts = [part.strip() for part in cover_letter_data['company_address'].split(',')]
            for part in address_parts:
                if part:
                    elements.append(Paragraph(part, styles['RecipientInfo']))
        else:
            # If no commas, just add as a single line
            elements.append(Paragraph(cover_letter_data['company_address'], styles['RecipientInfo']))

    elements.append(Spacer(1, 0.3 * inch))  # Space after recipient address
    
    # Add current date
    import datetime
    today = datetime.datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(today, styles['Date']))
    
    # Add greeting
    elements.append(Paragraph(cover_letter_data['greeting'] + ',', styles['Greeting']))
    
    # Add paragraphs with double spacing
    for paragraph in cover_letter_data['paragraphs']:
        elements.append(Paragraph(paragraph, styles['Paragraph']))
        # Add an extra small spacer between paragraphs for visual separation
        elements.append(Spacer(1, 0.1 * inch))
    
    # Add closing
    elements.append(Paragraph("Sincerely,", styles['Closing']))
    elements.append(Paragraph(resume_data.personal.name, styles['Signature']))

    # Add some space between signature and contact info
    elements.append(Spacer(1, 0.1 * inch))

    # Add email and phone below signature
    elements.append(Paragraph(email_link, styles['ContactInfo']))
    elements.append(Paragraph(phone_link, styles['ContactInfo']))
    
    # Build the PDF with the custom border
    doc.build(elements, onFirstPage=add_border, onLaterPages=add_border) 