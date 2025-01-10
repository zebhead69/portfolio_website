Python
import requests
import re
import time

def check_namecheap_availability(domain_name):
    """Checks domain availability on Namecheap."""
    url = f"https://www.namecheap.com/domains/registration/results/?domain={domain_name}"
    try:
        response = requests.get(url, timeout=10)  # Add timeout for robustness
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        html_content = response.text

        # Use a more robust regex to find availability
        available_match = re.search(r'"IsAvailable":true', html_content)

        if available_match:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking {domain_name}: {e}")
        return None  # Indicate an error occurred

def find_available_domains(word_list, tld=".com"):
    """Iterates through a word list and checks domain availability."""
    available_domains = []
    for word in word_list:
        domain = word + tld
        print(f"Checking {domain}...")
        availability = check_namecheap_availability(domain)

        if availability is True:
            print(f"{domain} is AVAILABLE!")
            available_domains.append(domain)
        elif availability is None:
            print(f"Could not check {domain} due to an error.")
        else:
            print(f"{domain} is NOT available.")

        time.sleep(1) #Important to avoid rate limiting

    return available_domains

if __name__ == "__main__":
    words = ["example", "test", "python", "code", "domain", "web", "site", "new", "best", "great"] #Example wordlist.
    available = find_available_domains(words)

    if available:
        print("\nAvailable Domains:")
        for domain in available:
            print(domain)
    else:
        print("\nNo available domains found in the list.")@id:tabnine.cloudHost
