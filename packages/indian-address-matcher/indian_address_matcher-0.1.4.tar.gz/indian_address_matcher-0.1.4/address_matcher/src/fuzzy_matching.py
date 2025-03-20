"""
Module for fuzzy matching of address components
"""
import logging
from typing import Dict, List, Optional, Set, Tuple, Any
from fuzzywuzzy import fuzz, process
from rapidfuzz import fuzz as rapidfuzz
from Levenshtein import distance as levenshtein_distance
from jellyfish import jaro_winkler_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FuzzyMatcher:
    """Class for fuzzy matching of address components"""
    
    def __init__(self, threshold: int = 85):
        """
        Initialize the fuzzy matcher
        
        Args:
            threshold: The threshold score (0-100) for considering a match
        """
        self.threshold = threshold
    
    def best_match(self, query: str, choices: List[str]) -> Tuple[Optional[str], float]:
        """
        Find the best fuzzy match for a query string among choices
        
        Args:
            query: The string to match
            choices: List of possible matches
            
        Returns:
            Tuple of (best match, score) or (None, 0) if no good match
        """
        if not query or not choices:
            return None, 0
        
        # Use process.extractOne to find the best match
        result = process.extractOne(query, choices, scorer=fuzz.token_set_ratio)
        if not result:
            return None, 0
        
        match, score = result
        if score >= self.threshold:
            return match, score
        return None, score
    
    def match_with_multiple_algorithms(self, query: str, choices: List[str]) -> Dict[str, Any]:
        """
        Match using multiple fuzzy matching algorithms and pick the best
        
        Args:
            query: The string to match
            choices: List of possible matches
            
        Returns:
            Dictionary with match details
        """
        if not query or not choices:
            return {"match": None, "score": 0, "algorithm": None}
        
        # Calculate scores with different algorithms
        matches = []
        
        # Token set ratio (fuzzywuzzy)
        token_set_match = process.extractOne(query, choices, scorer=fuzz.token_set_ratio)
        if token_set_match:
            matches.append(("token_set", token_set_match[0], token_set_match[1]))
        
        # Token sort ratio (fuzzywuzzy)
        token_sort_match = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
        if token_sort_match:
            matches.append(("token_sort", token_sort_match[0], token_sort_match[1]))
        
        # Partial ratio (fuzzywuzzy)
        partial_match = process.extractOne(query, choices, scorer=fuzz.partial_ratio)
        if partial_match:
            matches.append(("partial", partial_match[0], partial_match[1]))
        
        # RapidFuzz token_ratio
        if choices:
            rapid_scores = [(choice, rapidfuzz.token_ratio(query, choice) * 100) for choice in choices]
            rapid_best = max(rapid_scores, key=lambda x: x[1])
            matches.append(("rapidfuzz", rapid_best[0], rapid_best[1]))
        
        # Find the best match across all algorithms
        if not matches:
            return {"match": None, "score": 0, "algorithm": None}
        
        best_match = max(matches, key=lambda x: x[2])
        algorithm, match, score = best_match
        
        return {
            "match": match if score >= self.threshold else None,
            "score": score,
            "algorithm": algorithm
        }
    
    def find_closest_matches(self, query: str, choices: List[str], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find multiple closest matches sorted by score
        
        Args:
            query: The string to match
            choices: List of possible matches
            limit: Maximum number of matches to return
            
        Returns:
            List of match dictionaries with name and score
        """
        if not query or not choices:
            return []
        
        # Use process.extract to find multiple matches
        results = process.extract(query, choices, scorer=fuzz.token_set_ratio, limit=limit)
        
        return [{"match": match, "score": score} for match, score in results if score >= self.threshold]
    
    def compare_addresses(self, address1: str, address2: str) -> Dict[str, float]:
        """
        Compare two addresses using multiple fuzzy matching algorithms
        
        Args:
            address1: First address string
            address2: Second address string
            
        Returns:
            Dictionary of scores from different algorithms
        """
        if not address1 or not address2:
            return {
                "token_set_ratio": 0,
                "token_sort_ratio": 0,
                "partial_ratio": 0,
                "jaro_winkler": 0,
                "levenshtein_normalized": 0,
                "best_score": 0
            }
        
        # Calculate scores with different algorithms
        token_set = fuzz.token_set_ratio(address1, address2)
        token_sort = fuzz.token_sort_ratio(address1, address2)
        partial = fuzz.partial_ratio(address1, address2)
        
        # Jaro-Winkler similarity (0-1 scale)
        jaro = jaro_winkler_similarity(address1, address2) * 100
        
        # Normalized Levenshtein distance (convert to similarity score)
        max_len = max(len(address1), len(address2))
        lev_dist = levenshtein_distance(address1, address2)
        lev_norm = (max_len - lev_dist) / max_len * 100 if max_len > 0 else 0
        
        # Get the best score
        best_score = max(token_set, token_sort, partial, jaro, lev_norm)
        
        return {
            "token_set_ratio": token_set,
            "token_sort_ratio": token_sort,
            "partial_ratio": partial,
            "jaro_winkler": jaro,
            "levenshtein_normalized": lev_norm,
            "best_score": best_score
        }
    
    def is_same_component(self, comp1: str, comp2: str, threshold: Optional[int] = None) -> bool:
        """
        Check if two components are the same using fuzzy matching
        
        Args:
            comp1: First component string
            comp2: Second component string
            threshold: Optional custom threshold (overrides instance threshold)
            
        Returns:
            True if components are considered the same, False otherwise
        """
        if not comp1 or not comp2:
            return False
            
        match_threshold = threshold if threshold is not None else self.threshold
        score = fuzz.token_set_ratio(comp1, comp2)
        
        return score >= match_threshold 