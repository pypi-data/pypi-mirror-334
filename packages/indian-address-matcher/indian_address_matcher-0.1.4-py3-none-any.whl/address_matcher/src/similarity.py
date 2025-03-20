"""
Similarity metrics for comparing addresses
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from jellyfish import jaro_winkler_similarity, levenshtein_distance
from fuzzywuzzy import fuzz

def normalize_for_comparison(text):
    """
    Normalize text for comparison by removing extra spaces and non-alphanumeric characters
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    return text.strip().lower()

def levenshtein_similarity(text1, text2):
    """
    Calculate normalized Levenshtein similarity (1 - distance/max_length)
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    text1 = normalize_for_comparison(text1)
    text2 = normalize_for_comparison(text2)
    
    distance = levenshtein_distance(text1, text2)
    max_length = max(len(text1), len(text2))
    
    if max_length == 0:
        return 1.0
        
    return 1 - (distance / max_length)

def jaro_winkler_sim(text1, text2):
    """
    Calculate Jaro-Winkler similarity
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    text1 = normalize_for_comparison(text1)
    text2 = normalize_for_comparison(text2)
    
    return jaro_winkler_similarity(text1, text2)

def fuzzy_token_sort_ratio(text1, text2):
    """
    Calculate fuzzy token sort ratio using fuzzywuzzy
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    return fuzz.token_sort_ratio(text1, text2) / 100.0

def tfidf_cosine_similarity(text1, text2):
    """
    Calculate TF-IDF cosine similarity
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    vectorizer = TfidfVectorizer(lowercase=True, analyzer='word')
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
        return float(similarity)
    except Exception:
        if text1 == text2:
            return 1.0
        return 0.0

def contains_similarity(text1, text2):
    """
    Check if one address contains the other, useful for identifying when one address
    is a subset of the other
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: 1.0 if one string contains the other, 0.0 otherwise
    """
    text1 = normalize_for_comparison(text1)
    text2 = normalize_for_comparison(text2)
    
    if text1 in text2 or text2 in text1:
        return 1.0
    return 0.0

def token_based_similarity(text1, text2):
    """
    Calculate similarity based on common tokens
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    text1 = normalize_for_comparison(text1)
    text2 = normalize_for_comparison(text2)
    
    tokens1 = set(text1.split())
    tokens2 = set(text2.split())
    
    if not tokens1 or not tokens2:
        return 0.0
    
    common_tokens = tokens1.intersection(tokens2)
    return len(common_tokens) / max(len(tokens1), len(tokens2))

def weighted_similarity(text1, text2):
    """
    Calculate a weighted similarity score using multiple metrics
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Weighted similarity score between 0 and 1
    """
    weights = {
        'levenshtein': 0.15,
        'jaro_winkler': 0.2,
        'token_sort': 0.25,
        'tfidf': 0.2,
        'contains': 0.1,
        'token_based': 0.1
    }
    
    scores = {
        'levenshtein': levenshtein_similarity(text1, text2),
        'jaro_winkler': jaro_winkler_sim(text1, text2),
        'token_sort': fuzzy_token_sort_ratio(text1, text2),
        'tfidf': tfidf_cosine_similarity(text1, text2),
        'contains': contains_similarity(text1, text2),
        'token_based': token_based_similarity(text1, text2)
    }
    
    weighted_score = sum(scores[metric] * weight for metric, weight in weights.items())
    
    return weighted_score 