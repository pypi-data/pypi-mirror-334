#!/usr/bin/env python3
"""
Demo script for the Indian Address Matcher
"""
import json
from colorama import Fore, Style, init
from tabulate import tabulate

from address_matcher.src.address_matcher import AddressMatcher
from address_matcher.src.utils import preprocess_address, extract_address_components

init()

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print("=" * len(text))

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")

def print_component_comparison(components1, components2):
    """Print a comparison of address components"""
    all_keys = sorted(set(components1.keys()).union(components2.keys()))
    
    rows = []
    for key in all_keys:
        val1 = components1.get(key, "")
        val2 = components2.get(key, "")
        
        if isinstance(val1, list):
            val1 = ", ".join(str(v) for v in val1)
        if isinstance(val2, list):
            val2 = ", ".join(str(v) for v in val2)
            
        if val1 and val2 and val1 == val2:
            val1 = f"{Fore.GREEN}{val1}{Style.RESET_ALL}"
            val2 = f"{Fore.GREEN}{val2}{Style.RESET_ALL}"
        
        rows.append([key, val1, val2])
    
    print(tabulate(rows, headers=["Component", "Address 1", "Address 2"], tablefmt="grid"))

def print_similarity_scores(result):
    """Print similarity scores in a table"""
    scores = [
        ["Pincode Similarity", f"{result['pincode_similarity']:.2f}"],
        ["Full Address Similarity", f"{result['full_address_similarity']:.2f}"],
        ["Component Similarity", f"{result['component_similarity']:.2f}"],
        ["Final Score", f"{result['final_score']:.2f}"]
    ]
    
    for algo, score in result['fuzzy_scores'].items():
        scores.append([f"Fuzzy ({algo})", f"{score:.2f}"])
    
    print(tabulate(scores, headers=["Metric", "Score"], tablefmt="grid"))

def run_demo():
    """Run the address matcher demo"""
    print_header("Indian Address Matcher Demo")
    print("This demo shows how the address matcher works with various examples.\n")
    
    matcher = AddressMatcher(threshold=0.75, fuzzy_threshold=85)
    
    address_pairs = [
        (
            "123 Main Street, Koramangala, Bengaluru, Karnataka 560034",
            "123 Main Street, Koramangala, Bengaluru, Karnataka 560034"
        ),
        (
            "Flat 4B, Sunshine Apartments, 123 MG Road, Bengaluru, Karnataka 560001",
            "123 MG Road, Sunshine Apts, Flat 4B, Bengaluru, KA 560001"
        ),
        (
            "42 Jubilee Hills, Hyderabad, Telangana 500033",
            "42 Jubliee Hills, Hydrabad, Telangana 500033"
        ),
        (
            "201, Park View Apartments, Sector 15, Gurgaon, Haryana 122001",
            "Park View Apartments, Gurgaon, Haryana"
        ),
        (
            "56 Church Street, Bangalore, Karnataka 560001",
            "56 Temple Road, Chennai, Tamil Nadu 600001"
        ),
        (
            "Plot 45, Phase 2, MIDC, Andheri East, Mumbai, Maharashtra 400093",
            "Plot 45, Phase 2, MIDC, Andheri East, Mumbai, MH 400093"
        ),
        (
            "72 Ring Road, Delhi 110001",
            "72 Ring Road, Delhi 110010"
        ),
        (
            "24 Rajpath Marg, Near India Gate, New Delhi, Delhi 110001",
            "24, Rajpath Road, New Delhi, Delhi, 110001, Landmark: India Gate"
        )
    ]
    
    for i, (addr1, addr2) in enumerate(address_pairs, 1):
        print_header(f"Example {i}")
        print(f"Address 1: {addr1}")
        print(f"Address 2: {addr2}\n")
        
        result = matcher.match_with_details(addr1, addr2)
        
        print_info("Preprocessed Addresses:")
        print(f"Address 1: {result['preprocessed_address1']}")
        print(f"Address 2: {result['preprocessed_address2']}\n")
        
        print_info("Extracted Components:")
        print_component_comparison(result['components1'], result['components2'])
        
        print_info("\nSimilarity Scores:")
        print_similarity_scores(result)
        
        print("\nMatch Result:", end=" ")
        if result['is_match']:
            print_success("✓ MATCH")
        else:
            print_error("✗ NO MATCH")
        
        print("\n" + "-" * 80 + "\n")
    
    print_header("Custom Address Comparison")
    print("Enter two addresses to compare them:")
    
    try:
        addr1 = input("Address 1: ")
        addr2 = input("Address 2: ")
        
        if addr1 and addr2:
            result = matcher.match_with_details(addr1, addr2)
            
            print_info("\nExtracted Components:")
            print_component_comparison(result['components1'], result['components2'])
            
            print_info("\nSimilarity Scores:")
            print_similarity_scores(result)
            
            print("\nMatch Result:", end=" ")
            if result['is_match']:
                print_success("✓ MATCH")
            else:
                print_error("✗ NO MATCH")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print_error(f"Error: {str(e)}")

if __name__ == "__main__":
    run_demo() 