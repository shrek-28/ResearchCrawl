import requests
from typing import List
from models import Repository, RepositoryList
from typing import List, Dict

def fetch_repositories(query: str, sort: str, order: str = "desc") -> List[dict]:
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": 10
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['items']

def validate_repositories(data: List[dict]) -> RepositoryList:
    repositories = [Repository(name=item['name'], description=item['description'],
                               stars=item['stargazers_count'], forks=item['forks_count'],
                               url=item['html_url']) for item in data]
    return RepositoryList(repositories=repositories)

import requests

def fetch_readme_content(repo_url: str) -> str:
    """Fetches the README.md content from a GitHub repository."""
    
    # Extract owner and repo name from URL
    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except IndexError:
        return "Invalid GitHub repository URL."
    
    # Try fetching from both main and master branches
    possible_urls = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
    ]
    
    for url in possible_urls:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # Return the README content if found
    
    return "README.md not found or inaccessible."


# Function to scrape repositories and fetch READMEs
def scrape_repositories(keyword: str) -> List[Dict]:
    # Fetch top 10 repositories
    repositories = fetch_repositories(keyword, "stars")
    
    # List to hold repository data
    repo_data_list = []
    
    for repo in repositories:
        repo_url = repo['html_url']
        readme_content = fetch_readme_content(repo_url)
        
        # Create a dictionary for the repository data
        repo_data = {
            "name": repo['name'],
            "url": repo_url,
            "readme_content": readme_content
        }
        
        # Append to the list
        repo_data_list.append(repo_data)
    
    return repo_data_list