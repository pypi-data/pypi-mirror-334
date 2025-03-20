"""
Module for loading and processing address components dataset
"""
import json
import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddressComponentsData:
    """Class to load and manage address components dataset"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the address components data loader
        
        Args:
            data_path: Path to the address_components_dataset.json file
                       If None, will try to find it in standard locations
        """
        self.data_path = data_path
        self.data = []
        self.component_types = set()
        self.cities = set()
        self.states = set()
        self.districts = set()
        self.villages = set()
        self.localities = set()
        
        # Load the data if a path is provided or can be found
        if self.data_path:
            self.load_data(self.data_path)
        else:
            self._find_and_load_data()
    
    def _find_and_load_data(self):
        """Try to find the data file in standard locations"""
        # List of possible paths to check
        base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        possible_paths = [
            base_dir / "address_components_dataset.json",
            base_dir / "data" / "address_components_dataset.json",
            Path("/home/karan/StringMatch/address_matcher/address_components_dataset.json")
        ]
        
        for path in possible_paths:
            if path.exists():
                self.load_data(str(path))
                return
        
        logger.warning("Could not find address_components_dataset.json in standard locations")
    
    def load_data(self, file_path: str):
        """
        Load the address components dataset from a JSON file
        
        Args:
            file_path: Path to the JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            logger.info(f"Loaded {len(self.data)} address entries from {file_path}")
            self._extract_component_sets()
            
        except FileNotFoundError:
            logger.error(f"Data file not found: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {file_path}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def _extract_component_sets(self):
        """Extract sets of different component types from the data"""
        if not self.data:
            return
        
        # Extract all component types
        for entry in self.data:
            if "entities" not in entry:
                continue
                
            for entity in entry["entities"]:
                if "label" in entity and "text" in entry:
                    self.component_types.add(entity["label"])
                    
                    # Extract the text of the component
                    try:
                        text = entry["text"][entity["start_offset"]:entity["end_offset"]]
                        
                        # Add to appropriate set based on label
                        if entity["label"] == "city":
                            self.cities.add(text.lower())
                        elif entity["label"] == "state":
                            self.states.add(text.lower())
                        elif entity["label"] == "district":
                            self.districts.add(text.lower())
                        elif entity["label"] == "village":
                            self.villages.add(text.lower())
                        elif entity["label"] in ["locality_sector", "sublocality"]:
                            self.localities.add(text.lower())
                    except (KeyError, IndexError) as e:
                        logger.debug(f"Error extracting component text: {e}")
        
        logger.info(f"Extracted {len(self.component_types)} component types")
        logger.info(f"Found {len(self.cities)} cities, {len(self.states)} states, {len(self.districts)} districts")
        logger.info(f"Found {len(self.villages)} villages, {len(self.localities)} localities")
    
    def get_component_matches(self, text: str, component_type: str) -> List[str]:
        """
        Find matches of a specific component type in the given text
        
        Args:
            text: The text to search in
            component_type: The type of component to look for
            
        Returns:
            List of matched component texts
        """
        matches = []
        text_lower = text.lower()
        
        # Component-specific sets
        if component_type == "city":
            component_set = self.cities
        elif component_type == "state":
            component_set = self.states
        elif component_type == "district":
            component_set = self.districts
        elif component_type == "village":
            component_set = self.villages
        elif component_type in ["locality_sector", "sublocality", "locality"]:
            component_set = self.localities
        else:
            return matches
        
        # Find matches
        for component in component_set:
            if component in text_lower:
                matches.append(component)
        
        return matches


# Singleton instance
_address_data_instance = None

def get_address_data() -> AddressComponentsData:
    """
    Get the singleton instance of AddressComponentsData
    
    Returns:
        AddressComponentsData instance
    """
    global _address_data_instance
    if _address_data_instance is None:
        _address_data_instance = AddressComponentsData()
    return _address_data_instance 