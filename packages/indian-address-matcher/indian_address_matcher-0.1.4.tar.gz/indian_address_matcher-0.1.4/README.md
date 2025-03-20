# Indian Address Matcher

A Python library for matching Indian addresses to determine if they refer to the same location, even when formatted differently or containing variations.

## Features

- **Robust Address Matching**: Determine if two differently formatted Indian addresses refer to the same location
- **Component Extraction**: Extract key components from addresses (pincode, state, city, district, locality, etc.)
- **Fuzzy Matching**: Handle typos, abbreviations, and formatting differences
- **Detailed Analysis**: Get detailed similarity scores and component-wise comparison
- **Command-line Interface**: Easy-to-use CLI for quick address matching
- **Interactive Demo**: Visual demonstration of the matching process
- **Configurable Neighboring Cities**: Easy to add neighboring city relationships for improved matching

## Installation

```bash
# Install directly from GitHub
pip install git+https://github.com/Karan-Choudhary/indian-address-matcher.git

# Or clone and install from source
git clone https://github.com/Karan-Choudhary/indian-address-matcher.git
cd indian-address-matcher
pip install -e .
```

## Quick Start

### Python API

```python
from address_matcher.src.address_matcher import AddressMatcher

# Initialize the matcher
matcher = AddressMatcher(threshold=0.75)

# Compare two addresses
address1 = "123, Lakshmi Nagar, Bangalore, Karnataka - 560001"
address2 = "123 Lakshmi Ngr, Bengaluru, KA, 560001"

# Get simple match result
score, is_match = matcher.match(address1, address2)
print(f"Match score: {score:.2f}")
print(f"Is match: {is_match}")

# Get detailed match information
details = matcher.match_with_details(address1, address2)
print(details)
```

### Command-line Interface

```bash
# Basic usage
address-matcher "123, Lakshmi Nagar, Bangalore, Karnataka - 560001" "123 Lakshmi Ngr, Bengaluru, KA, 560001"

# With detailed output
address-matcher --detailed "123, Lakshmi Nagar, Bangalore, Karnataka - 560001" "123 Lakshmi Ngr, Bengaluru, KA, 560001"

# Output as JSON
address-matcher --json "123, Lakshmi Nagar, Bangalore, Karnataka - 560001" "123 Lakshmi Ngr, Bengaluru, KA, 560001"

# Adjust matching thresholds
address-matcher --threshold 0.8 --fuzzy-threshold 90 "123, Lakshmi Nagar, Bangalore, Karnataka - 560001" "123 Lakshmi Ngr, Bengaluru, KA, 560001"
```

### Interactive Demo

```bash
# Run the interactive demo
python -m address_matcher.demo
```

## How It Works

The address matcher uses a multi-step approach to determine if two addresses refer to the same location:

1. **Preprocessing**: Normalizes addresses by removing punctuation, converting to lowercase, etc.
2. **Component Extraction**: Extracts key components like pincode, state, city, district, locality, etc.
3. **Similarity Calculation**:
   - **Pincode Similarity**: Exact match of pincodes (with tolerance for typos)
   - **Full Address Similarity**: Overall text similarity using weighted algorithms
   - **Component Similarity**: Component-wise comparison using fuzzy matching
4. **Final Score Calculation**: Weighted combination of the above similarities
5. **Match Determination**: Comparison of final score against a threshold

## Advanced Usage

### Customizing Weights

You can customize the weights for different components of the matching algorithm:

```python
# Custom weights for address components
component_weights = {
    'pincode': 0.3,
    'full_address': 0.3,
    'components': 0.4
}

# Initialize matcher with custom weights
matcher = AddressMatcher(threshold=0.75, component_weights=component_weights)
```

### Configuring Neighboring Cities

You can configure city relationships to handle neighboring cities that are often used interchangeably in addresses:

```python
# Define neighboring cities during initialization
neighboring_cities = {
    'mumbai': ['thane', 'navi mumbai'],
    'bangalore': ['electronic city', 'whitefield'],
    'delhi': ['gurgaon', 'noida', 'faridabad']
}

matcher = AddressMatcher(neighboring_cities=neighboring_cities)

# Or add them after initialization
matcher = AddressMatcher()
matcher.add_neighboring_cities('pune', ['pimpri-chinchwad', 'hinjewadi', 'wakad'])
matcher.add_neighboring_cities('chennai', ['tambaram', 'chromepet', 'porur'])
```

### Adjusting Fuzzy Matching Threshold

```python
# Set a higher threshold for fuzzy matching (more strict)
matcher = AddressMatcher(threshold=0.75, fuzzy_threshold=90)

# Set a lower threshold for fuzzy matching (more lenient)
matcher = AddressMatcher(threshold=0.75, fuzzy_threshold=70)
```

## Project Structure

```
address_matcher/
├── __init__.py
├── cli.py           # Command-line interface
├── demo.py          # Interactive demo
├── src/
│   ├── __init__.py
│   ├── address_matcher.py    # Main address matcher class
│   ├── data_loader.py        # Dataset loader for address components
│   ├── entity_extraction.py  # Address component extraction
│   ├── fuzzy_matching.py     # Fuzzy matching algorithms
│   ├── similarity.py         # Similarity calculation functions
│   └── utils.py              # Utility functions
└── tests/
    ├── __init__.py
    └── test_*.py             # Unit tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all the contributors who have helped with the development of this project.
- Special thanks to the open-source community for providing the tools and libraries that made this project possible. 