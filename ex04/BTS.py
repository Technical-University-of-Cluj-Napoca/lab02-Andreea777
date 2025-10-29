import urllib.request
from typing import Optional, List

class Node:
    """Node class for the Binary Search Tree"""
    def __init__(self, word: str):
        self.word = word
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None

class BST:
    """Binary Search Tree for efficient prefix searching"""
    
    def __init__(self, source: str, **kwargs):
        self.root: Optional[Node] = None
        self.results: List[str] = []
        
        url_mode = kwargs.get('url', False)
        file_mode = kwargs.get('file', False)
        
        if url_mode and file_mode:
            raise ValueError("Both url and file cannot be True at the same time")
        
        words = []
        
        if url_mode:
            # Fetch wordlist from URL
            try:
                with urllib.request.urlopen(source) as response:
                    content = response.read().decode('utf-8')
                    words = [line.strip().lower() for line in content.split('\n') if line.strip()]
            except Exception as e:
                raise Exception(f"Failed to fetch wordlist from URL: {e}")
        
        elif file_mode:
            # Read wordlist from local file
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    words = [line.strip().lower() for line in f if line.strip()]
            except Exception as e:
                raise Exception(f"Failed to read wordlist from file: {e}")
        
        else:
            # Assume it's a string of words separated by spaces or newlines
            if '\n' in source:
                words = [word.strip().lower() for word in source.split('\n') if word.strip()]
            else:
                words = [word.strip().lower() for word in source.split() if word.strip()]
        
        # Remove duplicates and sort
        words = sorted(list(set(words)))
        
        # Build balanced BST
        if words:
            self.root = self._build_balanced_bst(words, 0, len(words) - 1)
    
    def _build_balanced_bst(self, words: List[str], start: int, end: int) -> Optional[Node]:
        """Recursively build a balanced BST from sorted word list"""
        if start > end:
            return None
        
        mid = (start + end) // 2
        node = Node(words[mid])
        
        node.left = self._build_balanced_bst(words, start, mid - 1)
        node.right = self._build_balanced_bst(words, mid + 1, end)
        
        return node
    
    def autocomplete(self, prefix: str) -> List[str]:
        """
        Public method to get autocomplete suggestions for a prefix
        
        Args:
            prefix: The prefix to search for
            
        Returns:
            List of words that start with the prefix
        """
        self.results = []
        prefix = prefix.lower()
        
        if self.root:
            self._collect(self.root, prefix)
        
        return sorted(self.results)  # Return sorted results
    
    def _collect(self, node: Optional[Node], prefix: str) -> None:
        """
        Private method to collect words starting with prefix using in-order traversal
        
        Args:
            node: Current node in BST
            prefix: Prefix to search for
        """
        if node is None:
            return
        
        # If current word starts with prefix, add it to results
        if node.word.startswith(prefix):
            self.results.append(node.word)
        
        # If prefix is less than or equal to current word, search left subtree
        # We search left even when prefix matches because there might be words
        # in left subtree that also match (due to BST properties)
        if prefix <= node.word or node.word.startswith(prefix):
            self._collect(node.left, prefix)
        
        # If prefix is greater than or equal to current word, search right subtree
        if prefix >= node.word[:len(prefix)] or node.word.startswith(prefix):
            self._collect(node.right, prefix)