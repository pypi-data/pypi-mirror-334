"""
Command-line interface for address matcher
"""
import argparse
import json
from .address_matcher import AddressMatcher

def main():
    """
    Main CLI function for address matcher
    """
    parser = argparse.ArgumentParser(description='Match Indian addresses to determine if they refer to the same location')
    parser.add_argument('address1', type=str, help='First address')
    parser.add_argument('address2', type=str, help='Second address')
    parser.add_argument('--threshold', type=float, default=0.75, help='Similarity threshold (0.0 to 1.0)')
    parser.add_argument('--detailed', action='store_true', help='Show detailed matching information')
    parser.add_argument('--output-json', action='store_true', help='Output result as JSON')
    
    args = parser.parse_args()
    
    matcher = AddressMatcher(threshold=args.threshold)
    
    if args.detailed:
        result = matcher.match_with_details(args.address1, args.address2)
        
        if args.output_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Address 1: {args.address1}")
            print(f"Address 2: {args.address2}")
            print(f"Preprocessed Address 1: {result['preprocessed_address1']}")
            print(f"Preprocessed Address 2: {result['preprocessed_address2']}")
            print(f"Pincode Similarity: {result['pincode_similarity']:.4f}")
            print(f"Full Address Similarity: {result['full_address_similarity']:.4f}")
            print(f"Component Similarity: {result['component_similarity']:.4f}")
            print(f"Final Similarity Score: {result['final_score']:.4f}")
            print(f"Match Result: {'MATCH' if result['is_match'] else 'NO MATCH'}")
    else:
        score, is_match = matcher.match(args.address1, args.address2)
        
        if args.output_json:
            print(json.dumps({
                'score': score,
                'is_match': is_match
            }, indent=2))
        else:
            print(f"Address 1: {args.address1}")
            print(f"Address 2: {args.address2}")
            print(f"Similarity Score: {score:.4f}")
            print(f"Match Result: {'MATCH' if is_match else 'NO MATCH'}")

if __name__ == '__main__':
    main() 