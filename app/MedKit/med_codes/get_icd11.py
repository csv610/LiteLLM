import requests
import os
import json
import sys

class ICD11Client:
    """
    A simple client for interacting with the WHO ICD-11 API.
    You can get your credentials by registering at https://icdaccessmanagement.who.int/
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://icdaccessmanagement.who.int/connect/token"
        self.access_token = None

    def authenticate(self):
        """Authenticates with the WHO API and retrieves an access token."""
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'icdapi_access',
            'grant_type': 'client_credentials'
        }
        try:
            response = requests.post(self.token_url, data=payload)
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                return True
            else:
                print(f"Authentication failed: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"An error occurred during authentication: {e}")
            return False

    def search(self, query, release_id='2024-01', linearization='mms'):
        """
        Searches for a medical condition in the specified ICD-11 linearization.
        Default is the 2024-01 release of the MMS (Mortality and Morbidity Statistics).
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Accept-Language': 'en',
            'API-Version': 'v2'
        }
        
        # Search URL for the specific linearization
        search_url = f"https://id.who.int/icd/release/11/{release_id}/{linearization}/search"
        params = {'q': query}
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Search failed: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return None

def main():
    # Attempt to get credentials from environment variables
    client_id = os.environ.get("ICD11_CLIENT_ID")
    client_secret = os.environ.get("ICD11_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: Missing API credentials.")
        print("\nPlease set the following environment variables:")
        print("  export ICD11_CLIENT_ID='your_client_id'")
        print("  export ICD11_CLIENT_SECRET='your_client_secret'")
        print("\nYou can obtain these by registering at: https://icdaccessmanagement.who.int/")
        sys.exit(1)

    client = ICD11Client(client_id, client_secret)
    
    condition = input("Enter a medical condition to search for: ").strip()
    if not condition:
        print("Please enter a valid condition.")
        return

    print(f"Searching for '{condition}'...")
    results = client.search(condition)
    
    if results and 'destinationEntities' in results:
        entities = results['destinationEntities']
        if not entities:
            print("No matching ICD-11 codes found.")
        else:
            print(f"\nTop results for '{condition}':")
            print("-" * 50)
            for entity in entities[:10]:  # Show top 10 results
                title = entity.get('title', 'No Title').replace('<em class=\'found\'>', '').replace('</em>', '')
                code = entity.get('theCode', 'N/A')
                uri = entity.get('id', 'N/A')
                print(f"Code: {code.ljust(10)} | Title: {title}")
    else:
        print("Failed to retrieve search results.")

if __name__ == "__main__":
    main()