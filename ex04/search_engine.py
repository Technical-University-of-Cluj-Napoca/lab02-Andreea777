import os
import sys
import termios
import tty
import msvcrt
from typing import List

from BTS import BST

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_char() -> str:
    """
    Get a single character from user input without requiring Enter key
    
    Returns:
        Single character input
    """
    if os.name == 'nt':  # Windows
        return msvcrt.getch().decode('utf-8')
    else:  # Unix-like systems
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def search_loop(bst: BST):
    """
    Main search loop that provides real-time autocomplete
    
    Args:
        bst: Initialized BST instance with wordlist
    """
    current_input = ""
    suggestions: List[str] = []
    
    print("=== Real-time Search Engine ===")
    print("Start typing to get autocomplete suggestions")
    print("Press TAB to autocomplete, BACKSPACE to delete, ESC to exit")
    print("-" * 50)
    
    while True:
        # Clear and display current state
        clear_screen()
        print("=== Real-time Search Engine ===")
        print("Start typing to get autocomplete suggestions")
        print("Press TAB to autocomplete, BACKSPACE to delete, ESC to exit")
        print("-" * 50)
        print(f"Input: {current_input}")
        print("-" * 50)
        
        # Show suggestions
        if current_input:
            suggestions = bst.autocomplete(current_input)
            if suggestions:
                print("Suggestions:")
                for i, suggestion in enumerate(suggestions[:10]):  # Show top 10
                    print(f"  {i+1}. {suggestion}")
            else:
                print("No suggestions found")
        else:
            print("Type something to get suggestions...")
        
        # Get user input
        print("\nType a character (ESC to exit): ", end='', flush=True)
        char = get_char()
        
        if ord(char) == 27:  # ESC key
            print("\nExiting search engine...")
            break
        elif char == '\t':  # TAB key - autocomplete
            if suggestions:
                current_input = suggestions[0]
        elif ord(char) == 127 or ord(char) == 8:  # BACKSPACE/DELETE key
            current_input = current_input[:-1]
        elif char == '\n' or char == '\r':  # ENTER key
            if current_input and current_input in bst.autocomplete(current_input):
                print(f"\nYou selected: {current_input}")
                input("Press Enter to continue...")
                current_input = ""
        elif char.isprintable():
            current_input += char

def initialize_search_engine(source: str = None, source_type: str = "url") -> BST:
    """
    Initialize the search engine with a wordlist
    
    Args:
        source: URL or file path to wordlist
        source_type: 'url' or 'file'
        
    Returns:
        Initialized BST instance
    """
    if source is None:
        # Use default wordlists
        if source_type == "url":
            # English wordlist
            source = "https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt"
        else:
            # Local file (you can download one)
            source = "wordlist.txt"
    
    try:
        if source_type == "url":
            bst = BST(source, url=True)
        else:
            bst = BST(source, file=True)
        
        print(f"Search engine initialized with {len(bst.autocomplete(''))} words")
        return bst
        
    except Exception as e:
        print(f"Error initializing search engine: {e}")
        print("Using built-in sample wordlist...")
        
        # Fallback to sample words
        sample_words = """
            apple application apply aptitude april
            banana band bandage bank banner
            cat category catch cattle catalyst
            dog document domain dolphin dominant
            elephant elevator elite eligible element
            fish final finance finger fire
            garden gate gather gear general
            house human humor hundred hunt
            ice icon idea ideal identify
            jack jacket jail jam january
            king kitchen kite knee knife
            lemon length lesson letter level
            machine magic magnet main make
            narrow nation native natural nature
            ocean office oil old olive
            package page paint palm paper
            quality quarter queen question quick
            rabbit race radio rail rain
            safe salad salt same sand
            table tail take talk tall
            umbrella under understand unit university
            valley value van variety various
            water way we week weight
            xray xerox xmas xbox xenon
            yard year yellow yes yesterday
            zero zone zoo zoom zulu
        """
        return BST(sample_words)