#!/usr/bin/env python3
import os
import importlib.resources as pkg_resources
from typing import Dict, List, Any


def get_available_templates() -> List[Dict[str, str]]:
    """
    Get a list of available resume templates.
    
    Returns:
        List of dictionaries with template info (name, description)
    """
    # In a real implementation, this would discover templates dynamically
    templates = [
        {
            'name': 'modern',
            'description': 'Contemporary design with subtle design elements'
        },
        {
            'name': 'minimal',
            'description': 'Clean, simple design with minimal styling'
        },
        {
            'name': 'classic',
            'description': 'Traditional resume format with conservative styling'
        },
        {
            'name': 'creative',
            'description': 'More expressive design for creative industries'
        }
    ]
    
    return templates


def get_template_config(template_name: str) -> Dict[str, Any]:
    """
    Get a specific resume template configuration by name.
    
    Args:
        template_name: Name of the template to retrieve
        
    Returns:
        Dictionary with template configuration
        
    Raises:
        ValueError: If the template doesn't exist
    """
    templates = get_available_templates()
    
    # Find the template by name
    template_names = [t['name'] for t in templates]
    if template_name not in template_names:
        raise ValueError(f"Template '{template_name}' not found. Available templates: {', '.join(template_names)}")
    
    # These would be actual template configurations in a real implementation
    # For now, we'll return some basic styling information
    template_configs = {
        'modern': {
            'font_main': 'Helvetica',
            'font_header': 'Helvetica-Bold',
            'color_primary': '#2c3e50',
            'color_secondary': '#3498db',
            'margins': (0.75, 0.75, 0.75, 0.75),  # top, right, bottom, left (inches)
            'header_style': 'centered',
            'section_style': 'titled',
            'layout': 'standard'
        },
        'minimal': {
            'font_main': 'Helvetica',
            'font_header': 'Helvetica-Bold',
            'color_primary': '#000000',
            'color_secondary': '#555555',
            'margins': (0.5, 0.5, 0.5, 0.5),
            'header_style': 'simple',
            'section_style': 'plain',
            'layout': 'compact'
        },
        'classic': {
            'font_main': 'Times-Roman',
            'font_header': 'Times-Bold',
            'color_primary': '#000000',
            'color_secondary': '#333333',
            'margins': (1.0, 1.0, 1.0, 1.0),
            'header_style': 'traditional',
            'section_style': 'underlined',
            'layout': 'classic'
        },
        'creative': {
            'font_main': 'Helvetica',
            'font_header': 'Helvetica-Bold',
            'color_primary': '#2e1a47',
            'color_secondary': '#5c2d91',
            'margins': (0.65, 0.65, 0.65, 0.65),
            'header_style': 'box',
            'section_style': 'bold',
            'layout': 'sidebar'
        }
    }
    
    return template_configs[template_name]


def validate_template(template_name: str) -> bool:
    """
    Validate that a template exists and has valid configuration.
    
    Args:
        template_name: Name of the template to validate
        
    Returns:
        True if the template is valid, False otherwise
    """
    try:
        config = get_template_config(template_name)
        # Check that the config has all required keys
        required_keys = ['font_main', 'font_header', 'color_primary', 
                          'color_secondary', 'margins', 'header_style', 
                          'section_style', 'layout']
        
        for key in required_keys:
            if key not in config:
                return False
                
        return True
    except ValueError:
        return False


def list_templates() -> None:
    """
    Print a list of available templates with descriptions.
    """
    templates = get_available_templates()
    
    print("\nAvailable Resume Templates:")
    print("----------------------------")
    
    for template in templates:
        print(f"{template['name']}: {template['description']}")
    
    print("\nUse template name with --template option.")


def get_template_resource_path(template_name: str, resource_type: str) -> str:
    """
    Get the path to a template resource file.
    
    Args:
        template_name: Name of the template
        resource_type: Type of resource ('fonts', 'images', etc.)
        
    Returns:
        Path to the template resource directory
        
    Raises:
        ValueError: If the template doesn't exist
    """
    templates = get_available_templates()
    
    # Find the template by name
    template_names = [t['name'] for t in templates]
    if template_name not in template_names:
        raise ValueError(f"Template '{template_name}' not found. Available templates: {', '.join(template_names)}")
    
    # This would return actual resource paths in a real implementation
    # For now, we'll return a placeholder
    return f"resumebuilder/templates/{template_name}/{resource_type}"


# Alias for backward compatibility 
get_template = get_template_config 