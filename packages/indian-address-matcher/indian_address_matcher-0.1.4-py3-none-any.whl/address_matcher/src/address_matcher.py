"""
Main address matching class for comparing Indian addresses
"""
import logging

from .utils import preprocess_address, extract_address_components
from .similarity import weighted_similarity
from .fuzzy_matching import FuzzyMatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddressMatcher:
    """
    Class for matching Indian addresses to determine if they refer to the same location
    """    
    def __init__(self, threshold=0.75, component_weights=None, fuzzy_threshold=85, neighboring_cities=None):
        """
        Initialize the address matcher
        
        Args:
            threshold (float): Threshold for determining if addresses match (0.0 to 1.0)
            component_weights (dict): Weights for different address components (optional)
            fuzzy_threshold (int): Threshold for fuzzy matching (0-100)
            neighboring_cities (dict): Dictionary of neighboring cities {city: [list_of_neighbors]} (optional)
        """
        self.threshold = threshold
        self.fuzzy_matcher = FuzzyMatcher(threshold=fuzzy_threshold)
        
        self.component_weights = component_weights or {
            'pincode': 0.30,  
            'full_address': 0.25,  
            'components': 0.45   
        }
        
        self.neighboring_cities = neighboring_cities or {
            'thane': ['kalyan', 'dombivali'],
        }
        
        self._preprocess_neighboring_cities()
    
    def _preprocess_neighboring_cities(self):
        """
        Preprocess the neighboring cities dictionary to create a bidirectional lookup map
        """
        self.neighboring_map = {}
        
        for city, neighbors in self.neighboring_cities.items():
            city_lower = city.lower()
            if city_lower not in self.neighboring_map:
                self.neighboring_map[city_lower] = set()
            
            for neighbor in neighbors:
                neighbor_lower = neighbor.lower()
                self.neighboring_map[city_lower].add(neighbor_lower)
                
                if neighbor_lower not in self.neighboring_map:
                    self.neighboring_map[neighbor_lower] = set()
                self.neighboring_map[neighbor_lower].add(city_lower)
    
    def add_neighboring_cities(self, city, neighbors):
        """
        Add new neighboring city relationships
        
        Args:
            city (str): Main city name
            neighbors (list): List of neighboring city names
        """
        city_lower = city.lower()
        
        if city_lower not in self.neighboring_cities:
            self.neighboring_cities[city_lower] = []
            
        for neighbor in neighbors:
            if neighbor.lower() not in self.neighboring_cities[city_lower]:
                self.neighboring_cities[city_lower].append(neighbor.lower())
        
        self._preprocess_neighboring_cities()
    
    def match(self, address1, address2):
        """
        Compare two addresses and determine if they refer to the same location
        
        Args:
            address1 (str): First address
            address2 (str): Second address
            
        Returns:
            tuple: (similarity_score, boolean indicating if addresses match)
        """
        preprocessed_addr1 = preprocess_address(address1)
        preprocessed_addr2 = preprocess_address(address2)
        
        components1 = extract_address_components(preprocessed_addr1)
        components2 = extract_address_components(preprocessed_addr2)
        
        pincode_similarity = self._pincode_similarity(components1, components2)
        
        full_address_similarity = weighted_similarity(preprocessed_addr1, preprocessed_addr2)
        
        component_similarity = self._component_similarity(components1, components2)
        
        final_score = (
            pincode_similarity * self.component_weights['pincode'] +
            full_address_similarity * self.component_weights['full_address'] +
            component_similarity * self.component_weights['components']
        )
        
        if pincode_similarity > 0.8 and component_similarity > 0.6:
            final_score = min(1.0, final_score * 1.1)
        
        is_match = final_score >= self.threshold
        return final_score, is_match
    
    def _pincode_similarity(self, components1, components2):
        """
        Calculate similarity based on pincodes
        
        Args:
            components1 (dict): Components from first address
            components2 (dict): Components from second address
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        pincode1 = components1.get('pincode')
        pincode2 = components2.get('pincode')
        
        if pincode1 and pincode2 and pincode1 == pincode2:
            return 1.0
        
        if pincode1 and pincode2:
            clean_pin1 = ''.join(pincode1.split())
            clean_pin2 = ''.join(pincode2.split())
            if clean_pin1 == clean_pin2:
                return 1.0
            
            if len(clean_pin1) == len(clean_pin2):
                diff_count = sum(1 for a, b in zip(clean_pin1, clean_pin2) if a != b)
                if diff_count <= 1:
                    return 0.9
        
        # If one or both pincodes are missing, provide a neutral score
        if not pincode1 or not pincode2:
            return 0.5
        
        return 0.0
    
    def _are_neighboring_cities(self, city1, city2):
        """
        Check if two cities are neighbors based on the neighboring_cities configuration
        
        Args:
            city1 (str): First city name
            city2 (str): Second city name
            
        Returns:
            bool: True if cities are neighbors, False otherwise
        """
        if not city1 or not city2:
            return False
            
        city1_lower = city1.lower()
        city2_lower = city2.lower()
        
        # Check direct match
        if city1_lower == city2_lower:
            return True
            
        # Check if they are neighbors
        if city1_lower in self.neighboring_map and city2_lower in self.neighboring_map[city1_lower]:
            return True
            
        return False
    
    def _component_similarity(self, components1, components2):
        """
        Calculate similarity score based on address components
        
        Args:
            components1 (dict): Components from first address
            components2 (dict): Components from second address
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        component_scores = []
        component_weights = {
            'state': 0.15,
            'city': 0.25,
            'district': 0.15,
            'locality': 0.20,
            'village': 0.15,
            'landmarks': 0.10,
            'flat_no': 0.10,
            'floor': 0.05,  
            'pincode': 0.20 
        }
        
        # Normalize component weights to ensure they sum to 1.0
        total_weight = sum(component_weights.values())
        for key in component_weights:
            component_weights[key] /= total_weight
        
        # Check for neighboring cities using the configurable approach
        city1 = components1.get('city', '').lower() if components1.get('city') else ''
        city2 = components2.get('city', '').lower() if components2.get('city') else ''
        
        # Also check district as it might contain city information
        district1 = components1.get('district', '').lower() if components1.get('district') else ''
        district2 = components2.get('district', '').lower() if components2.get('district') else ''
        
        # Check all possible combinations of city and district
        neighboring_match = False
        
        city_combinations = [
            (city1, city2),
            (city1, district2),
            (district1, city2),
            (district1, district2)
        ]
        
        for c1, c2 in city_combinations:
            if self._are_neighboring_cities(c1, c2):
                neighboring_match = True
                break
                
        if not neighboring_match:
            cities1 = set()
            cities2 = set()
            
            if city1:
                cities1.add(city1)
            if district1:
                cities1.add(district1)
            if city2:
                cities2.add(city2)
            if district2:
                cities2.add(district2)
                
            for c1 in cities1:
                for c2 in cities2:
                    if self._are_neighboring_cities(c1, c2):
                        neighboring_match = True
                        break
                if neighboring_match:
                    break
                
        if neighboring_match:
            component_scores.append((0.8, component_weights['city']))
        
        flat1 = components1.get('flat_no', '')
        flat2 = components2.get('flat_no', '')
        if flat1 and flat2:
            flat1_nums = ''.join(c for c in flat1 if c.isdigit())
            flat2_nums = ''.join(c for c in flat2 if c.isdigit())
            if flat1_nums and flat2_nums and (flat1_nums in flat2_nums or flat2_nums in flat1_nums):
                component_scores.append((0.9, component_weights['flat_no']))
            elif flat1.lower() in flat2.lower() or flat2.lower() in flat1.lower():
                component_scores.append((0.8, component_weights['flat_no']))
            else:
                flat_score = self.fuzzy_matcher.is_same_component(
                    flat1, flat2, threshold=70
                )
                component_scores.append((1.0 if flat_score else 0.0, component_weights['flat_no']))
        
        floor1 = components1.get('floor', '')
        floor2 = components2.get('floor', '')
        if floor1 and floor2:
            floor1_num = ''.join(c for c in floor1 if c.isdigit())
            floor2_num = ''.join(c for c in floor2 if c.isdigit())
            floor_score = 1.0 if floor1_num == floor2_num else 0.0
            component_scores.append((floor_score, component_weights['floor']))
        
        if components1.get('state') and components2.get('state'):
            state_score = self.fuzzy_matcher.is_same_component(
                components1['state'], components2['state'], threshold=75
            )
            component_scores.append((1.0 if state_score else 0.0, component_weights['state']))
        
        if components1.get('city') and components2.get('city'):
            city1 = components1['city'].lower()
            city2 = components2['city'].lower()
            
            # Known city name variations
            city_variations = {
                'bangalore': ['bengaluru', 'blore', 'blr'],
                'mumbai': ['bombay'],
                'chennai': ['madras'],
                'kolkata': ['calcutta'],
                'hyderabad': ['hyd'],
                'delhi': ['new delhi', 'dilli'],
                'pune': ['poona'],
                'kochi': ['cochin'],
                'thiruvananthapuram': ['trivandrum'],
                'benaras': ['varanasi'],
                'ahmedabad': ['amdavad'],
                'indore': ['indor'],
            }
            
            city_matched = False
            for city, variations in city_variations.items():
                if ((city1 == city or city1 in variations) and 
                    (city2 == city or city2 in variations)):
                    city_matched = True
                    break
            
            if city_matched:
                component_scores.append((1.0, component_weights['city']))
            else:
                city_score = self.fuzzy_matcher.is_same_component(
                    city1, city2, threshold=75
                )
                component_scores.append((1.0 if city_score else 0.0, component_weights['city']))
        
        if components1.get('district') and components2.get('district'):
            district_score = self.fuzzy_matcher.is_same_component(
                components1['district'], components2['district'], threshold=75
            )
            component_scores.append((1.0 if district_score else 0.0, component_weights['district']))
        
        if components1.get('locality') and components2.get('locality'):
            locality_score = self.fuzzy_matcher.is_same_component(
                components1['locality'], components2['locality'], threshold=70
            )
            component_scores.append((1.0 if locality_score else 0.0, component_weights['locality']))
        
        if components1.get('village') and components2.get('village'):
            village_score = self.fuzzy_matcher.is_same_component(
                components1['village'], components2['village'], threshold=70
            )
            component_scores.append((1.0 if village_score else 0.0, component_weights['village']))
        
        if components1.get('landmarks') and components2.get('landmarks'):
            landmark_matches = []
            for lm1 in components1['landmarks']:
                for lm2 in components2['landmarks']:
                    if self.fuzzy_matcher.is_same_component(lm1, lm2, threshold=65):
                        landmark_matches.append(1.0)
                        break
            
            if landmark_matches:
                landmark_score = sum(landmark_matches) / len(landmark_matches)
                component_scores.append((landmark_score, component_weights['landmarks']))
        
        if components1.get('pincode') and components2.get('pincode') and components1['pincode'] == components2['pincode']:
            component_scores.append((1.0, component_weights['pincode']))
        
        # Boost score if we have a survey number match
        survey1 = components1.get('survey_no', '')
        survey2 = components2.get('survey_no', '')
        if survey1 and survey2 and (survey1 == survey2 or self.fuzzy_matcher.is_same_component(survey1, survey2, threshold=80)):
            component_scores.append((1.0, 0.10))  # Add extra weight for survey number match
        
        if not component_scores:
            return 0.5
        
        total_weight = sum(weight for _, weight in component_scores)
        weighted_sum = sum(score * weight for score, weight in component_scores)
        
        normalized_score = weighted_sum / total_weight if total_weight > 0 else 0.5
        
        return normalized_score
    
    def match_with_details(self, address1, address2):
        """
        Compare addresses and return detailed similarity scores
        
        Args:
            address1 (str): First address
            address2 (str): Second address
            
        Returns:
            dict: Detailed similarity scores and match result
        """
        preprocessed_addr1 = preprocess_address(address1)
        preprocessed_addr2 = preprocess_address(address2)
        
        components1 = extract_address_components(preprocessed_addr1)
        components2 = extract_address_components(preprocessed_addr2)
        
        pincode_similarity = self._pincode_similarity(components1, components2)
        full_address_similarity = weighted_similarity(preprocessed_addr1, preprocessed_addr2)
        component_similarity = self._component_similarity(components1, components2)
        
        fuzzy_scores = self.fuzzy_matcher.compare_addresses(preprocessed_addr1, preprocessed_addr2)
        
        final_score = (
            pincode_similarity * self.component_weights['pincode'] +
            full_address_similarity * self.component_weights['full_address'] +
            component_similarity * self.component_weights['components']
        )
        
        # Boost score if pincode is an exact match and components are similar
        if pincode_similarity > 0.8 and component_similarity > 0.6:
            boost_factor = 1.1
            boosted_score = min(1.0, final_score * boost_factor)
            score_boost = boosted_score - final_score
            final_score = boosted_score
        else:
            score_boost = 0.0
        
        is_match = final_score >= self.threshold
        
        return {
            'preprocessed_address1': preprocessed_addr1,
            'preprocessed_address2': preprocessed_addr2,
            'components1': components1,
            'components2': components2,
            'pincode_similarity': pincode_similarity,
            'full_address_similarity': full_address_similarity,
            'component_similarity': component_similarity,
            'fuzzy_scores': fuzzy_scores,
            'score_boost': score_boost,
            'final_score': final_score,
            'is_match': is_match,
            'neighboring_cities': self.neighboring_cities  # Add this to provide info about configured neighbors
        } 