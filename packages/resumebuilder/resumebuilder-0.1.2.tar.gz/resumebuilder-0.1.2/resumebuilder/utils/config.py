#!/usr/bin/env python3
import os
import yaml
from typing import Dict, Any, Optional


def get_config_dir() -> str:
    """
    Get the application data directory for storing configuration files.
    Creates the directory if it doesn't exist.
    
    Returns:
        Path to the application data directory
    """
    # Use platform-specific app data directory
    home = os.path.expanduser("~")
    app_dir = os.path.join(home, ".resumebuilder")
    
    # Create the directory if it doesn't exist
    os.makedirs(app_dir, exist_ok=True)
    
    return app_dir


def get_config_file_path() -> str:
    """
    Get the path to the user configuration file.
    
    Returns:
        Path to the user configuration file
    """
    return os.path.join(get_config_dir(), "config.yaml")


def load_config(file_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        file_path: Path to the YAML configuration file
        
    Returns:
        Dictionary with configuration values
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file is not valid YAML
    """
    if file_path is None:
        file_path = get_config_file_path()
        
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config if config else {}
    except FileNotFoundError:
        return {}  # Return empty config if file doesn't exist
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML format in {file_path}: {str(e)}")


def save_config(data: Dict[str, Any], file_path: str = None) -> None:
    """
    Save configuration to a YAML file.
    
    Args:
        data: Dictionary with configuration values
        file_path: Path to save the YAML configuration file
        
    Raises:
        IOError: If the file can't be written
    """
    if file_path is None:
        file_path = get_config_file_path()
        
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
    except IOError as e:
        raise IOError(f"Failed to write configuration to {file_path}: {str(e)}")


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a value from the configuration file.
    
    Args:
        key: Configuration key
        default: Default value if key is not found
        
    Returns:
        Configuration value or default if not found
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """
    Set a value in the configuration file.
    
    Args:
        key: Configuration key
        value: Configuration value
    """
    config = load_config()
    config[key] = value
    save_config(config)


def reset_config() -> None:
    """
    Reset the configuration to default values.
    """
    save_config({})


# Legacy function names for backward compatibility
get_app_directory = get_config_dir
get_user_config_path = get_config_file_path 