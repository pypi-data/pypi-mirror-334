"""
Module for extracting entities from address strings using regex patterns and datasets
"""
import re
from typing import Dict, List, Optional, Tuple, Any
import logging

from .data_loader import get_address_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Regex patterns for different address components
PIN_CODE_PATTERN = r'(\d{6})'
FLAT_NO_PATTERN = r'(?:flat|apartment|unit|house|shop)[\s\-\.]*(?:no\.?|number)?[\s\-\.]*([a-zA-Z0-9\-\/]+)'
PLOT_NO_PATTERN = r'(?:plot|site)[\s\-\.]*(?:no\.?|number)?[\s\-\.]*([a-zA-Z0-9\-\/]+)'
SURVEY_NO_PATTERN = r'(?:survey|s\.no|s no|s\.no\.|gat|khasra|khata|cts|s|survey no\.|new survey no\.)[\s\-\.]*(?:no\.?|number)?[\s\-\.]*([a-zA-Z0-9\-\/]+)'
FLOOR_PATTERN = r'(?:([0-9]+)(?:st|nd|rd|th)[\s\-\.]*floor)|(?:floor[\s\-\.]*([0-9]+))'
LANDMARK_PATTERN = r'(?:near|beside|opposite|behind|adjacent to|in front of|next to)[\s\-\.]+([^,\.]+)'
PHASE_PATTERN = r'phase[\s\-\.]*([a-zA-Z0-9\-]+)'
SECTOR_PATTERN = r'sector[\s\-\.]*([a-zA-Z0-9\-]+)'

def extract_pattern(text: str, pattern: str, flags: int = re.IGNORECASE) -> List[str]:
    """
    Extract all matches of a regex pattern from a text string
    
    Args:
        text: The text to extract from
        pattern: The regex pattern to match
        flags: Regex flags
    
    Returns:
        List of extracted matches
    """
    matches = re.finditer(pattern, text, flags)
    results = []
    
    for match in matches:
        # Get the capture group that matched (some patterns have multiple groups)
        for group in match.groups():
            if group:  # Skip None matches
                results.append(group.strip())
                break
    
    return results

def extract_pincode(text: str) -> Optional[str]:
    """
    Extract 6-digit PIN code from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted PIN code or None
    """
    matches = extract_pattern(text, PIN_CODE_PATTERN)
    return matches[0] if matches else None

def extract_cities(text: str) -> List[str]:
    """
    Extract city names from address using the dataset
    
    Args:
        text: The address text
    
    Returns:
        List of extracted city names
    """
    address_data = get_address_data()
    return address_data.get_component_matches(text, "city")

def extract_states(text: str) -> List[str]:
    """
    Extract state names from address using the dataset
    
    Args:
        text: The address text
    
    Returns:
        List of extracted state names
    """
    address_data = get_address_data()
    return address_data.get_component_matches(text, "state")

def extract_districts(text: str) -> List[str]:
    """
    Extract district names from address using the dataset
    
    Args:
        text: The address text
    
    Returns:
        List of extracted district names
    """
    address_data = get_address_data()
    return address_data.get_component_matches(text, "district")

def extract_localities(text: str) -> List[str]:
    """
    Extract locality names from address using the dataset
    
    Args:
        text: The address text
    
    Returns:
        List of extracted locality names
    """
    address_data = get_address_data()
    return address_data.get_component_matches(text, "locality")

def extract_villages(text: str) -> List[str]:
    """
    Extract village names from address using the dataset
    
    Args:
        text: The address text
    
    Returns:
        List of extracted village names
    """
    address_data = get_address_data()
    return address_data.get_component_matches(text, "village")

def extract_landmarks(text: str) -> List[str]:
    """
    Extract landmarks from address using regex patterns
    
    Args:
        text: The address text
    
    Returns:
        List of extracted landmarks
    """
    return extract_pattern(text, LANDMARK_PATTERN)

def extract_flat_no(text: str) -> Optional[str]:
    """
    Extract flat number from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted flat number or None
    """
    matches = extract_pattern(text, FLAT_NO_PATTERN)
    return matches[0] if matches else None

def extract_plot_no(text: str) -> Optional[str]:
    """
    Extract plot number from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted plot number or None
    """
    matches = extract_pattern(text, PLOT_NO_PATTERN)
    return matches[0] if matches else None

def extract_survey_no(text: str) -> Optional[str]:
    """
    Extract survey number from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted survey number or None
    """
    matches = extract_pattern(text, SURVEY_NO_PATTERN)
    return matches[0] if matches else None

def extract_floor(text: str) -> Optional[str]:
    """
    Extract floor number from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted floor number or None
    """
    matches = re.search(FLOOR_PATTERN, text, re.IGNORECASE)
    if matches:
        # Return the first non-None group
        for group in matches.groups():
            if group:
                return group
    return None

def extract_sector(text: str) -> Optional[str]:
    """
    Extract sector from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted sector or None
    """
    matches = extract_pattern(text, SECTOR_PATTERN)
    return matches[0] if matches else None

def extract_phase(text: str) -> Optional[str]:
    """
    Extract phase from address
    
    Args:
        text: The address text
    
    Returns:
        Extracted phase or None
    """
    matches = extract_pattern(text, PHASE_PATTERN)
    return matches[0] if matches else None

def extract_all_components(text: str) -> Dict[str, Any]:
    """
    Extract all address components from a text
    
    Args:
        text: The address text
    
    Returns:
        Dictionary of all extracted components
    """
    components = {
        'pincode': extract_pincode(text),
        'cities': extract_cities(text),
        'states': extract_states(text),
        'districts': extract_districts(text),
        'localities': extract_localities(text),
        'villages': extract_villages(text),
        'landmarks': extract_landmarks(text),
        'flat_no': extract_flat_no(text),
        'plot_no': extract_plot_no(text),
        'survey_no': extract_survey_no(text),
        'floor': extract_floor(text),
        'sector': extract_sector(text),
        'phase': extract_phase(text),
    }
    
    # Get the first item from lists for simple components
    for field in ['cities', 'states', 'districts']:
        items = components[field]
        components[field[:-1]] = items[0] if items else None
    
    return components 