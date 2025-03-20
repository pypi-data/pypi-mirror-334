"""
Utility functions for address preprocessing and standardization
"""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import Dict, Any, List, Optional

# Import our new modules
from .entity_extraction import extract_all_components

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Common Indian address abbreviations and their full forms
INDIAN_ABBREVIATIONS = {
    'rd': 'road',
    'st': 'street',
    'apt': 'apartment',
    'appt': 'apartment',
    'flr': 'floor',
    'fl': 'floor',
    'blvd': 'boulevard',
    'ave': 'avenue',
    'bldg': 'building',
    'marg': 'road',
    'nagar': 'nagar',
    'clny': 'colony',
    'col': 'colony',
    'sec': 'sector',
    'soc': 'society',
    'socty': 'society',
    'aprmnt': 'apartment',
    'apptmnt': 'apartment',
    'extn': 'extension',
    'ext': 'extension',
    'twp': 'township',
    'encl': 'enclave',
    'enclv': 'enclave',
    'apts': 'apartments',
    'appts': 'apartments',
}

# Indian state abbreviations
INDIAN_STATE_ABBREVIATIONS = {
    'AP': 'Andhra Pradesh',
    'AR': 'Arunachal Pradesh',
    'AS': 'Assam',
    'BR': 'Bihar',
    'CG': 'Chhattisgarh',
    'GA': 'Goa',
    'GJ': 'Gujarat',
    'HR': 'Haryana',
    'HP': 'Himachal Pradesh',
    'JH': 'Jharkhand',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'OD': 'Odisha',
    'OR': 'Odisha',
    'PB': 'Punjab',
    'RJ': 'Rajasthan',
    'SK': 'Sikkim',
    'TN': 'Tamil Nadu',
    'TG': 'Telangana',
    'TS': 'Telangana',
    'TR': 'Tripura',
    'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand',
    'UT': 'Uttarakhand',
    'WB': 'West Bengal',
    'AN': 'Andaman and Nicobar Islands',
    'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli and Daman and Diu',
    'DD': 'Dadra and Nagar Haveli and Daman and Diu',
    'DL': 'Delhi',
    'JK': 'Jammu and Kashmir',
    'LA': 'Ladakh',
    'LD': 'Lakshadweep',
    'PY': 'Puducherry',
}

# Metadata labels commonly found in Indian addresses
METADATA_LABELS = [
    r'Corporation:\s*',
    r'Other Details:\s*',
    r'Building Name:\s*',
    r'Flat No:\s*',
    r'House No:\s*',
    r'Plot No:\s*',
    r'Road:\s*',
    r'Street:\s*',
    r'Block Sector\s*:\s*',
    r'Landmark:\s*',
    r'Area:\s*',
    r'Locality:\s*',
    r'Village:\s*',
    r'Town:\s*',
    r'City:\s*',
    r'District:\s*',
    r'Tehsil:\s*',
    r'Taluka:\s*',
    r'State:\s*',
    r'Pincode:\s*',
    r'PIN:\s*',
    r'PIN Code:\s*',
    r'Address Type:\s*',
    r'Address Category:\s*',
    r'Post Office:\s*',
]

def roman_to_int(s):
    """Convert Roman numeral to integer"""
    if not s:
        return s
    
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    
    for i in range(len(s)):
        if i > 0 and roman_map[s[i]] > roman_map[s[i-1]]:
            result += roman_map[s[i]] - 2 * roman_map[s[i-1]]
        else:
            result += roman_map[s[i]]
            
    return result

def normalize_phase_numbers(text):
    """Normalize phase numbers (convert Roman numerals to Arabic numbers)"""
    def replace_roman(match):
        roman = match.group(1).upper()
        # Only process if it's a valid Roman numeral
        if all(c in 'IVXLCDM' for c in roman):
            try:
                return f"phase {roman_to_int(roman)}"
            except (KeyError, TypeError):
                return match.group(0)
        return match.group(0)
    
    # First normalize any "phase ii" to "phase 2" etc.
    pattern = r'[pP][hH][aA][sS][eE][\s-]+([IVXLCDM]+)'
    text = re.sub(pattern, replace_roman, text)
    
    # Now also normalize any "phase-2" to "phase 2"
    text = re.sub(r'phase[\s-]+(\d+)', r'phase \1', text)
    
    return text

def preprocess_address(address):
    """
    Preprocess an address string by removing metadata labels,
    standardizing formats, converting to lowercase, and normalizing content.
    
    Args:
        address (str): The address to preprocess
        
    Returns:
        str: The preprocessed address
    """
    if not address:
        return ""
    
    # Remove metadata labels
    for pattern in METADATA_LABELS:
        address = re.sub(pattern, '', address, flags=re.IGNORECASE)
    
    # Convert to lowercase
    address = address.lower()
    
    # Get pincode if present (to preserve it for later)
    pin_match = re.search(r'(\d{6})', address)
    pincode = pin_match.group(1) if pin_match else None
    
    # Standardize common formats - careful with word boundaries to avoid spurious matches
    # Use word boundaries (\b) to prevent partial word matches
    
    # 1. Flat/House numbers
    address = re.sub(r'\b(?:flat|unit|apartment|appt|apt)[- ]?([a-zA-Z0-9/-]+)', r'flat \1', address)
    address = re.sub(r'\b(?:house|h\.no|h\.n\.|h\sno)[- ]?([a-zA-Z0-9/-]+)', r'house \1', address)
    
    # 2. Floor numbers
    address = re.sub(r'\b(?:floor|flr)[- ]?(\d+)', r'floor \1', address)
    address = re.sub(r'(\d+)(?:st|nd|rd|th)[- ]?(?:floor|flr)', r'floor \1', address)
    
    # 3. Wing/Block designations
    address = re.sub(r'\b(?:wing|block)[- ]?([a-zA-Z0-9]+)', r'wing \1', address)
    
    # 4. Survey/Plot numbers - careful with the pattern to avoid inserting 'survey' everywhere
    address = re.sub(r'\b(?:survey|s\.no|s no|s\.no\.|gat|khasra|khata|cts|survey no\.|new survey no\.)[- ]?([a-zA-Z0-9/-]+)', r'survey \1', address)
    address = re.sub(r'\bs\b[- ]?(?:no\.?|number)?[- ]?([a-zA-Z0-9/-]+)', r'survey \1', address)
    address = re.sub(r'\b(?:plot|site)[- ]?(?:no\.?|number)?[- ]?([a-zA-Z0-9/-]+)', r'plot \1', address)
    
    # 5. Phase numbers (including Roman numerals)
    address = normalize_phase_numbers(address)
    
    # 6. Sector designations
    address = re.sub(r'\b(?:sector|sec)[- ]?([a-zA-Z0-9]+)', r'sector \1', address)
    
    # 7. Society/Complex/Enclave names
    address = re.sub(r'\b(?:society|soc)[- ]?([a-zA-Z0-9]+)', r'society \1', address)
    address = re.sub(r'\b(?:complex|cplx)[- ]?([a-zA-Z0-9]+)', r'complex \1', address)
    address = re.sub(r'\b(?:enclave|enclv|encl)[- ]?([a-zA-Z0-9]+)', r'enclave \1', address)
    
    # 8. Road numbers and landmarks
    address = re.sub(r'\b(?:road|rd)[- ]?(?:no\.?|number)?[- ]?([a-zA-Z0-9]+)', r'road \1', address)
    address = re.sub(r'\b(?:near|beside|opposite|behind|adjacent to|in front of|next to)[- ]+([^,\.]+)', r'near \1', address)
    
    # Replace punctuation with spaces (except hyphens and slashes in compound words/numbers)
    for char in string.punctuation:
        if char != '-' and char != '/':  # Keep hyphens and slashes for compound words and building numbers
            address = address.replace(char, ' ')
    
    # Replace multiple spaces with a single space
    address = ' '.join(address.split())
    
    # Replace common abbreviations
    tokens = address.split()
    for i, token in enumerate(tokens):
        if token in INDIAN_ABBREVIATIONS:
            tokens[i] = INDIAN_ABBREVIATIONS[token]
        elif token in INDIAN_STATE_ABBREVIATIONS:
            tokens[i] = INDIAN_STATE_ABBREVIATIONS[token].lower()
    
    # Reconstruct address
    address = ' '.join(tokens)
    
    return address

def extract_address_components(address: str) -> Dict[str, Any]:
    """
    Extract key components from an address (pincode, state, city, etc.)
    using the enhanced entity extraction module.
    
    Args:
        address (str): The preprocessed address
        
    Returns:
        dict: A dictionary of address components
    """
    # Use the enhanced entity extraction module
    components = extract_all_components(address)
    
    # Add backward compatibility for the original components structure
    if 'pincode' not in components:
        components['pincode'] = None
    
    if 'state' not in components and 'states' in components and components['states']:
        components['state'] = components['states'][0] if components['states'] else None
    
    if 'city' not in components and 'cities' in components and components['cities']:
        components['city'] = components['cities'][0] if components['cities'] else None
    
    if 'locality' not in components and 'localities' in components and components['localities']:
        components['locality'] = components['localities'][0] if components['localities'] else None
    
    if 'building' not in components:
        components['building'] = components.get('flat_no', None)
    
    if 'landmarks' not in components:
        components['landmarks'] = []
    
    return components

def remove_stopwords(text):
    """
    Remove common English and address stopwords from text
    
    Args:
        text (str): The text to process
        
    Returns:
        str: Text without stopwords
    """
    stop_words = set(stopwords.words('english'))
    
    # Add common address stopwords
    address_stopwords = {'the', 'and', 'of', 'near', 'behind', 'opposite', 'beside'}
    stop_words.update(address_stopwords)
    
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    
    return ' '.join(filtered_text) 