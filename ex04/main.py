#!/usr/bin/env python3
"""
Main module for Search Engine Suggestions
Exercise 4 - Lab02
"""

import sys
import os
from search_engine import search_loop, initialize_search_engine

def main():
    """Main function to run the search engine"""
    print("=== Search Engine Suggestions ===")
    print("Choose wordlist source:")
    print("1. English wordlist (URL - 466k words)")
    print("2. Romanian wordlist (URL - 50k words)")
    print("3. Local file")
    print("4. Sample words (built-in)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # English wordlist
        url = "https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt"
        bst = initialize_search_engine(url, "url")
    
    elif choice == "2":
        # Romanian wordlist
        url = "https://raw.githubusercontent.com/davidxbors/romanian_wordlists/refs/heads/master/wordlists/ro_50k.txt"
        bst = initialize_search_engine(url, "url")
    
    elif choice == "3":
        # Local file
        filename = input("Enter path to wordlist file: ").strip()
        if os.path.exists(filename):
            bst = initialize_search_engine(filename, "file")
        else:
            print(f"File {filename} not found. Using sample words instead.")
            bst = initialize_search_engine(None, "file")
    
    else:
        # Sample words
        bst = initialize_search_engine(None, "file")
    
    print("\nStarting search engine...")
    print("Type to see autocomplete suggestions")
    print("Press ESC to exit")
    print("-" * 50)
    input("Press Enter to continue...")
    
    # Start the search loop
    try:
        search_loop(bst)
    except KeyboardInterrupt:
        print("\n\nSearch engine terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()