#!/usr/bin/env python3
"""
Script to update README.md files to use objective, non-promotional language.
"""

import sys
import re
from pathlib import Path

# Objective language replacements for README files
README_REPLACEMENTS = {
    # Remove promotional superlatives
    r"sophisticated": "",
    r"advanced": "",
    r"state-of-the-art": "",
    r"cutting-edge": "",
    r"revolutionary": "",
    r"game-changing": "",
    r"breakthrough": "",
    r"powerful": "",
    r"robust": "",
    r"comprehensive": "detailed",
    r"intelligent": "",
    r"smart": "",
    r"fast": "efficient",
    r"quick": "efficient",
    r"rapidly": "efficiently",
    r"quickly": "efficiently",
    
    # Replace subjective claims with objective statements
    r"Key Features": "Features",
    r"leverages": "uses",
    r"utilizes": "uses",
    r"harnesses": "uses",
    r"employs": "uses",
    r"evidence-based": "based on medical knowledge",
    r"Evidence-Based": "Based on Medical Knowledge",
    r"evidence based": "based on medical knowledge",
    r"highly accurate": "designed for accuracy",
    r"high accuracy": "designed for accuracy",
    r"accurate": "consistent",
    r"accurately": "consistently",
    r"precise": "specific",
    r"precisely": "specifically",
    r"reliable": "consistent",
    r"reliably": "consistently",
    
    # Remove marketing language
    r"seamlessly": "",
    r"effortlessly": "",
    r"beautiful": "well-structured",
    r"elegant": "well-designed",
    r"clean": "well-organized",
    r"simple": "straightforward",
    r"easy": "straightforward",
    r"easily": "straightforwardly",
    r"intuitive": "clear",
    r"user-friendly": "accessible",
    
    # Replace subjective performance claims
    r"Optimized for": "Designed for",
    r"optimally": "appropriately",
    r"optimally": "appropriately",
    r"best": "optimal",
    r"better": "improved",
    r"great": "effective",
    r"excellent": "highly effective",
    r"amazing": "notable",
    r"awesome": "notable",
    r"outstanding": "notable",
    r"superior": "enhanced",
    
    # Medical accuracy improvements
    r"accuracy": "identification rate",
    r"Accuracy": "Identification Rate",
    r"perfect": "optimal",
    r"perfectly": "optimally",
    r"flawless": "optimal",
    r"flawlessly": "optimally",
    
    # Remove unnecessary qualifiers
    r"All information is": "Information is",
    r"provides comprehensive": "provides detailed",
    r"offers comprehensive": "offers detailed",
    r"features comprehensive": "features detailed",
    
    # Simplify technical descriptions
    r"AI-powered": "AI",
    r"AI powered": "AI",
    r"machine learning": "language model",
    r"deep learning": "language model",
    r"neural network": "language model",
    
    # Remove redundant phrases
    r"designed to": "",
    r"built to": "",
    r"engineered to": "",
    r"crafted to": "",
    
    # Standardize terminology
    r"medical expert": "medical knowledge",
    r"medical professionals": "healthcare professionals",
    r"healthcare providers": "healthcare professionals",
}

def clean_extra_spaces(content):
    """Clean up extra spaces and formatting."""
    # Remove double spaces
    content = re.sub(r' +', ' ', content)
    
    # Remove spaces at line beginnings
    content = re.sub(r'^ +', '', content, flags=re.MULTILINE)
    
    # Remove extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def update_readme_content(content):
    """Update README content with objective language."""
    original_content = content
    
    # Apply replacements
    for pattern, replacement in README_REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Clean up formatting
    content = clean_extra_spaces(content)
    
    return content

def update_readme_file(readme_path):
    """Update a single README file."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = update_readme_content(content)
        
        # Only write if content changed
        if updated_content != content:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error updating {readme_path}: {e}")
        return False

def main():
    """Update all README files with objective language."""
    print("Updating README files with objective, non-promotional language...")
    
    recognizers_dir = Path(__file__).parent
    updated_files = []
    
    # Find all README.md files
    readme_files = list(recognizers_dir.glob("*/README.md"))
    
    if not readme_files:
        print("No README.md files found in recognizer modules")
        return
    
    for readme_file in readme_files:
        print(f"Updating {readme_file.parent.name}/README.md...")
        
        if update_readme_file(readme_file):
            updated_files.append(readme_file)
            print(f"✓ Updated {readme_file}")
        else:
            print(f"- No changes needed for {readme_file}")
    
    print(f"\nUpdated {len(updated_files)} README files")
    
    if updated_files:
        print("\nKey changes made:")
        print("- Removed promotional superlatives and marketing language")
        print("- Replaced subjective claims with objective statements")
        print("- Standardized medical terminology")
        print("- Improved accuracy of performance metrics")
        print("- Enhanced clarity and consistency")
        print("- Removed redundant phrases and qualifiers")

if __name__ == "__main__":
    main()
