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
            'fonts': {
                'main': 'Helvetica',
                'header': 'Helvetica-Bold',
                'section': 'Helvetica-Bold'
            },
            'colors': {
                'primary': '#2c3e50',
                'secondary': '#3498db',
                'text': '#333333'
            },
            'margins': {
                'top': 0.75,
                'right': 0.75,
                'bottom': 0.75,
                'left': 0.75
            },
            'header_style': 'centered',
            'section_style': 'standard',
            'layout': 'standard'
        },
        'minimal': {
            'fonts': {
                'main': 'Helvetica',
                'header': 'Helvetica-Bold',
                'section': 'Helvetica-Bold'
            },
            'colors': {
                'primary': '#000000',
                'secondary': '#555555',
                'text': '#333333'
            },
            'margins': {
                'top': 0.5,
                'right': 0.5,
                'bottom': 0.5,
                'left': 0.5
            },
            'header_style': 'left-aligned',
            'section_style': 'boxed',
            'layout': 'compact'
        },
        'classic': {
            'fonts': {
                'main': 'Times-Roman',
                'header': 'Times-Bold',
                'section': 'Times-Bold'
            },
            'colors': {
                'primary': '#000000',
                'secondary': '#333333',
                'text': '#000000'
            },
            'margins': {
                'top': 1.0,
                'right': 1.0,
                'bottom': 1.0,
                'left': 1.0
            },
            'header_style': 'right-aligned',
            'section_style': 'underlined',
            'layout': 'standard'
        },
        'creative': {
            'fonts': {
                'main': 'Helvetica',
                'header': 'Helvetica-Bold',
                'section': 'Helvetica-Bold'
            },
            'colors': {
                'primary': '#2e1a47',
                'secondary': '#5c2d91',
                'text': '#333333'
            },
            'margins': {
                'top': 0.65,
                'right': 0.65,
                'bottom': 0.65,
                'left': 0.65
            },
            'header_style': 'two-column',
            'section_style': 'sidebar',
            'layout': 'two-column'
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
        
    Raises:
        ValueError: If the template doesn't exist
    """
    # Find the template by name
    templates = get_available_templates()
    template_names = [t['name'] for t in templates]
    if template_name not in template_names:
        raise ValueError(f"Template '{template_name}' not found. Available templates: {', '.join(template_names)}")
    
    try:
        config = get_template_config(template_name)
        # Check that the config has all required keys
        required_keys = ['fonts', 'colors', 'margins', 'header_style', 
                         'section_style', 'layout']
        
        for key in required_keys:
            if key not in config:
                return False
                
        return True
    except Exception as e:
        raise ValueError(f"Template validation failed: {str(e)}")


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