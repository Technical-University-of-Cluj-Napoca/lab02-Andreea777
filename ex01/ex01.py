from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]] :
    anagram_groups = defaultdict(list)
    for word in strs : 
        key = tuple(sorted(word))
        anagram_groups[key].append(word)
    return list(anagram_groups.values())


"""
- defaultdict = provides a default value for missing keys, 
                so you don't get a KeyError when accessing them
- for each word, we sort its characters and convert them to a tuple 
to create a unique key; we use tuples because they are hashable and 
can be dictionary keys
- all words that produce the same sorted tuple key are anagrams and we 
group them together in the same list
- we return the values of the dictionary as a list of lists
"""