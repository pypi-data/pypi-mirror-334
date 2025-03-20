"""
Interactive test script for the address matcher
"""
from src.address_matcher import AddressMatcher

def interactive_test():
    """
    Run an interactive test of the address matcher
    """
    print("=== Indian Address Matcher Interactive Test ===")
    print("Enter two Indian addresses to compare them")
    print()
    
    matcher = AddressMatcher()
    
    while True:
        print("\nEnter addresses (or type 'exit' to quit):")
        

        address1 = input("Address 1: ")
        if address1.lower() == 'exit':
            break
            
        address2 = input("Address 2: ")
        if address2.lower() == 'exit':
            break
            
        threshold_input = input("Similarity threshold (0.0-1.0) [default: 0.75]: ")
        if threshold_input.strip():
            try:
                threshold = float(threshold_input)
                if 0.0 <= threshold <= 1.0:
                    matcher.threshold = threshold
                else:
                    print("Invalid threshold. Using default value of 0.75.")
                    matcher.threshold = 0.75
            except ValueError:
                print("Invalid threshold. Using default value of 0.75.")
                matcher.threshold = 0.75
        
        result = matcher.match_with_details(address1, address2)
        
        print("\n--- Results ---")
        print(f"Preprocessed Address 1: {result['preprocessed_address1']}")
        print(f"Preprocessed Address 2: {result['preprocessed_address2']}")
        print(f"Pincode Similarity: {result['pincode_similarity']:.4f}")
        print(f"Full Address Similarity: {result['full_address_similarity']:.4f}")
        print(f"Component Similarity: {result['component_similarity']:.4f}")
        print(f"Final Similarity Score: {result['final_score']:.4f}")
        print(f"Match Result: {'MATCH' if result['is_match'] else 'NO MATCH'}")
        
        continue_input = input("\nContinue? (y/n): ")
        if continue_input.lower() != 'y':
            break
    
    print("\nThank you for using the Indian Address Matcher!")

if __name__ == "__main__":
    interactive_test() 