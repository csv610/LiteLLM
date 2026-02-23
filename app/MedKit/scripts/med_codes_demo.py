import json
from unittest.mock import patch, MagicMock
from get_icd11 import ICD11Client

def mock_demo():
    # Mock data for demonstration
    mock_auth_data = {'access_token': 'demo_token_12345'}
    mock_search_data = {
        'destinationEntities': [
            {
                'id': 'https://id.who.int/icd/entity/543585396',
                'title': '<em class="found">Diabetes</em> mellitus',
                'theCode': '5A10'
            },
            {
                'id': 'https://id.who.int/icd/entity/448895267',
                'title': 'Type 1 <em class="found">diabetes</em> mellitus',
                'theCode': '5A10.0'
            },
            {
                'id': 'https://id.who.int/icd/entity/1415254558',
                'title': 'Type 2 <em class="found">diabetes</em> mellitus',
                'theCode': '5A11'
            }
        ]
    }

    print("--- STARTING ICD-11 SEARCH DEMO (MOCKED) ---")
    
    with patch('requests.post') as mock_post:
        with patch('requests.get') as mock_get:
            # Setup mocks
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_auth_data
            
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_search_data

            # Initialize client with dummy keys
            client = ICD11Client("demo_id", "demo_secret")
            
            condition = "diabetes"
            print(f"Searching for '{condition}'...")
            
            results = client.search(condition)
            
            if results and 'destinationEntities' in results:
                entities = results['destinationEntities']
                print(f"\nTop results for '{condition}':")
                print("-" * 50)
                for entity in entities:
                    # Logic copied from main script for demo purposes
                    title = entity.get('title', 'No Title')
                    # Clean up the title (removing the mock HTML tags)
                    title = title.replace('<em class="found">', '').replace('</em>', '')
                    code = entity.get('theCode', 'N/A')
                    print(f"Code: {code.ljust(10)} | Title: {title}")
            
    print("\n--- DEMO COMPLETE ---")

if __name__ == "__main__":
    mock_demo()