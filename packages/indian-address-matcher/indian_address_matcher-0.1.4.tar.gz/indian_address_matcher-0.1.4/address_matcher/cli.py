#!/usr/bin/env python3
"""
Command-line interface for the Indian Address Matcher
"""
import argparse
import json
import sys
import logging
from typing import Dict, Any

from .src.address_matcher import AddressMatcher

def setup_logger():
    """Configure logging for the CLI"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Match Indian addresses to determine if they refer to the same location'
    )
    
    parser.add_argument(
        'address1',
        help='First address to compare'
    )
    
    parser.add_argument(
        'address2',
        help='Second address to compare'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.75,
        help='Similarity threshold for considering addresses as matching (0.0 to 1.0)'
    )
    
    parser.add_argument(
        '--fuzzy-threshold',
        type=int,
        default=85,
        help='Threshold for fuzzy matching components (0-100)'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed matching information'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    return parser.parse_args()

def format_detailed_output(result: Dict[str, Any]) -> str:
    """Format detailed output for terminal display"""
    output = []
    output.append("\n=== Address Matching Results ===\n")
    
    output.append("Address 1 (preprocessed):")
    output.append(f"  {result['preprocessed_address1']}")
    output.append("\nAddress 2 (preprocessed):")
    output.append(f"  {result['preprocessed_address2']}")
    
    output.append("\nExtracted Components:")
    output.append("\nAddress 1:")
    for key, value in result['components1'].items():
        if value:
            output.append(f"  {key}: {value}")
    
    output.append("\nAddress 2:")
    for key, value in result['components2'].items():
        if value:
            output.append(f"  {key}: {value}")
    
    output.append("\nSimilarity Scores:")
    output.append(f"  Pincode Similarity: {result['pincode_similarity']:.2f}")
    output.append(f"  Full Address Similarity: {result['full_address_similarity']:.2f}")
    output.append(f"  Component Similarity: {result['component_similarity']:.2f}")
    
    output.append("\nFuzzy Matching Scores:")
    for algo, score in result['fuzzy_scores'].items():
        output.append(f"  {algo}: {score:.2f}")
    
    output.append(f"\nFinal Score: {result['final_score']:.2f}")
    output.append(f"Match Result: {'✓ MATCH' if result['is_match'] else '✗ NO MATCH'}")
    
    return "\n".join(output)

def main():
    """Main entry point for the CLI"""
    args = parse_args()
    logger = setup_logger()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    matcher = AddressMatcher(
        threshold=args.threshold,
        fuzzy_threshold=args.fuzzy_threshold
    )
    
    try:
        if args.detailed:
            result = matcher.match_with_details(args.address1, args.address2)
            
            if args.json:
                serializable_result = {
                    k: (str(v) if not isinstance(v, (dict, list, str, int, float, bool, type(None))) else v)
                    for k, v in result.items()
                }
                print(json.dumps(serializable_result, indent=2))
            else:
                print(format_detailed_output(result))
        else:
            score, is_match = matcher.match(args.address1, args.address2)
            
            if args.json:
                print(json.dumps({
                    'score': score,
                    'is_match': is_match
                }, indent=2))
            else:
                print(f"\nSimilarity Score: {score:.2f}")
                print(f"Match Result: {'✓ MATCH' if is_match else '✗ NO MATCH'}")
    
    except Exception as e:
        logger.error(f"Error processing addresses: {str(e)}")
        if args.debug:
            logger.exception("Detailed error information:")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 