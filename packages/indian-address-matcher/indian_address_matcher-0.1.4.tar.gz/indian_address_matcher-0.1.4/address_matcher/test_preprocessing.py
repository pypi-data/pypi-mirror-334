#!/usr/bin/env python3
"""
Test script to verify address preprocessing improvements
"""
from address_matcher.src.utils import preprocess_address
from address_matcher.src.address_matcher import AddressMatcher
from colorama import Fore, Style, init
import json

init()

def print_green(text):
    """Print text in green"""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

def print_red(text):
    """Print text in red"""
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")

def print_blue(text):
    """Print text in blue"""
    print(f"{Fore.BLUE}{text}{Style.RESET_ALL}")

def print_yellow(text):
    """Print text in yellow"""
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")

def print_header(text):
    """Print a header"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print("=" * len(text))

def test_preprocessing():
    """Test the preprocessing function with challenging addresses"""
    print_header("Testing Address Preprocessing")
    
    test_cases = [
        (
            "FLAT-304,FLOOR-3 PANDU HARI ENCLAV PHASE 2 WING B S NO 48, H.N. 4,TISGAONKALYAN EAST KALYAN-DOMBIVALI 421301 MAHARASHTRA",
            "Corporation: Kalyaan-Dombiwali Other Details: Building Name:Pandu Hari Enclave Phase Ii, Flat No:B 304, Road:Tisgaon, Block Sector :, Landmark: S No 48, Thane, 421301, maharashtra"
        ),
        (
            "Abc Apartments, Flat #303, 4th Floor, Near XYZ Mall, M.G. Road, Bengaluru, Karnataka - 560001",
            "Building Name: ABC Apts, Flat No: 303, Floor: 4, Landmark: XYZ Mall, Street: MG Road, City: Bangalore, State: KA, Pincode: 560001"
        ),
        (
            "H.No. 5-6-789/A/12, Plot No. 45, Road No. 3, Jubilee Hills, Hyderabad-500033, Telangana",
            "House No: 5-6-789/A/12, Plot No. 45, Road No. 3, Area: Jubilee Hills, City: Hyderabad, PIN Code: 500033, State: Telangana"
        ),
        (
            "Survey No. 123/4, Phase-II, Sector 7, Salt Lake City, Kolkata, WB 700091",
            "Address Type: Residential, Survey No. 123/4, Block Sector: Sector 7, Phase: II, Locality: Salt Lake City, City: Kolkata, State: West Bengal, PIN: 700091"
        )
    ]
    
    for i, (addr1, addr2) in enumerate(test_cases, 1):
        print_header(f"Test Case {i}")
        
        print("Original Addresses:")
        print_blue(f"Address 1: {addr1}")
        print_blue(f"Address 2: {addr2}")
        
        preprocessed1 = preprocess_address(addr1)
        preprocessed2 = preprocess_address(addr2)
        
        print("\nPreprocessed Addresses:")
        print_green(f"Address 1: {preprocessed1}")
        print_green(f"Address 2: {preprocessed2}")
        
        matcher = AddressMatcher(threshold=0.70)
        result = matcher.match_with_details(addr1, addr2)
        score = result['final_score']
        is_match = result['is_match']
        
        print("\nExtracted Components:")
        print_yellow("Address 1:")
        for key, value in result['components1'].items():
            if value:
                print(f"  {key}: {value}")
        
        print_yellow("\nAddress 2:")
        for key, value in result['components2'].items():
            if value:
                print(f"  {key}: {value}")
        
        print("\nSimilarity Scores:")
        print(f"  Pincode Similarity:    {result['pincode_similarity']:.2f}")
        print(f"  Full Address Similarity: {result['full_address_similarity']:.2f}")
        print(f"  Component Similarity:  {result['component_similarity']:.2f}")
        
        if 'score_boost' in result and result['score_boost'] > 0:
            print_green(f"  Score Boost: +{result['score_boost']:.2f}")
        
        print("\nMatch Result:")
        if is_match:
            print_green(f"MATCH (Score: {score:.2f})")
        else:
            print_red(f"NO MATCH (Score: {score:.2f})")
        
        print("\n" + "-" * 80)

def test_with_manual_preprocessing():
    """Compare with manual preprocessing version"""
    print_header("Comparison with Manual Preprocessing")
    
    address1 = "FLAT-304,FLOOR-3 PANDU HARI ENCLAV PHASE 2 WING B S NO 48, H.N. 4,TISGAONKALYAN EAST KALYAN-DOMBIVALI 421301 MAHARASHTRA"
    address2 = "Corporation: Kalyaan-Dombiwali Other Details: Building Name:Pandu Hari Enclave Phase Ii, Flat No:B 304, Road:Tisgaon, Block Sector :, Landmark: S No 48, Thane, 421301, maharashtra"
    
    address2_manual = "Kalyaan-Dombiwali, Pandu Hari Enclave Phase 2, B 304, Tisgaon, S No 48, Thane, 421301, maharashtra"
    
    print("Original Addresses:")
    print_blue(f"Address 1: {address1}")
    print_blue(f"Address 2: {address2}")
    
    print("\nTest with Automatic Preprocessing:")
    matcher = AddressMatcher(threshold=0.70)  
    result1 = matcher.match_with_details(address1, address2)
    score1 = result1['final_score']
    is_match1 = result1['is_match']
    
    if is_match1:
        print_green(f"MATCH (Score: {score1:.2f})")
    else:
        print_red(f"NO MATCH (Score: {score1:.2f})")
    
    print("\nSimilarity Scores:")
    print(f"  Pincode Similarity:    {result1['pincode_similarity']:.2f}")
    print(f"  Full Address Similarity: {result1['full_address_similarity']:.2f}")
    print(f"  Component Similarity:  {result1['component_similarity']:.2f}")
    
    print("\nTest with Manual Preprocessing:")
    result2 = matcher.match_with_details(address1, address2_manual)
    score2 = result2['final_score']
    is_match2 = result2['is_match']
    
    if is_match2:
        print_green(f"MATCH (Score: {score2:.2f})")
    else:
        print_red(f"NO MATCH (Score: {score2:.2f})")
    
    print("\nSimilarity Scores:")
    print(f"  Pincode Similarity:    {result2['pincode_similarity']:.2f}")
    print(f"  Full Address Similarity: {result2['full_address_similarity']:.2f}")
    print(f"  Component Similarity:  {result2['component_similarity']:.2f}")
    
    print("\nPreprocessing Comparison:")
    print_green(f"Auto-preprocessed: {preprocess_address(address2)}")
    print_green(f"Manually preprocessed: {preprocess_address(address2_manual)}")

if __name__ == "__main__":
    test_preprocessing()
    test_with_manual_preprocessing() 