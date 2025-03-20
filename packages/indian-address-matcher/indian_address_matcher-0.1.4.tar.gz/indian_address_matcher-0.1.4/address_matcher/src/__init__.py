"""
Indian Address Matcher Package
"""

from address_matcher.src.address_matcher import AddressMatcher
from address_matcher.src.utils import preprocess_address, extract_address_components
from address_matcher.src.similarity import weighted_similarity
from address_matcher.src.fuzzy_matching import FuzzyMatcher 