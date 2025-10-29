import sys
import requests 
from bs4 import BeautifulSoup 

def main():
    if len(sys.argv) != 2:
        print("Usage: py define.py <word>")
        sys.exit(1)

    word = sys.argv[1]
    url = f"https://dexonline.ro/definitie/{word}"

    # Optional: headers to look like a normal browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Fetch the page
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Could not retrieve the definition.")
        sys.exit(1)

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the definition section (as seen in your screenshot)
    definition = soup.find("span", class_="tree-def html")
    if not definition:
        print("No definition found for this word.")
        sys.exit(0)

    # Clean and print text
    print(definition.get_text(strip=True))

if __name__ == "__main__":
    main()
