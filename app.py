from flask import Flask, render_template, request
from github_crawler import fetch_repositories, validate_repositories
from resource_fetcher import fetch_stackoverflow_resources, fetch_reddit_resources, validate_resources
import requests

app = Flask(__name__)

import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get GitHub Token from .env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_readme_content(repo_url: str) -> str:
    """Fetches the README.md content from a GitHub repository using the GitHub API."""
    
    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
    except IndexError:
        return "Invalid GitHub repository URL."
    
    # GitHub API endpoint for README
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    
    # Headers for authentication
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        readme_data = response.json()
        
        # Decode Base64 content
        readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
        return readme_content.strip()
    
    elif response.status_code == 404:
        return "README.md not found."
    
    elif response.status_code == 403:
        return "GitHub API rate limit exceeded. Try again later."
    
    else:
        return f"GitHub API error: {response.status_code} - {response.json().get('message', 'Unknown error')}"

def enrich_repositories_with_readme(repositories):
    enriched_repos = []
    for repo in repositories:
        repo_url = getattr(repo, "url", "")  # Corrected attribute access
        readme_content = fetch_readme_content(repo_url)
        
        enriched_repo = {
            "name": getattr(repo, "name", "Unknown Repo"),
            "description": getattr(repo, "description", "No description available"),
            "stars": getattr(repo, "stars", 0),
            "forks": getattr(repo, "forks", 0),
            "url": repo_url,
            "readme_content": readme_content
        }
        enriched_repos.append(enriched_repo)

    return enriched_repos


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_prompt = request.form['search_prompt']

        # Fetch GitHub repositories
        trending_repos = fetch_repositories(f"{search_prompt} stars:>1", "stars")
        latest_repos = fetch_repositories(f"{search_prompt} created:>2023-01-01", "created")
        most_used_repos = fetch_repositories(f"{search_prompt} forks:>1", "forks")

        trending_repos = validate_repositories(trending_repos)
        latest_repos = validate_repositories(latest_repos)
        most_used_repos = validate_repositories(most_used_repos)

        # Enrich repositories with README content
        trending_repos_enriched = enrich_repositories_with_readme(trending_repos.repositories)
        latest_repos_enriched = enrich_repositories_with_readme(latest_repos.repositories)
        most_used_repos_enriched = enrich_repositories_with_readme(most_used_repos.repositories)

        # Fetch resources from other platforms
        stackoverflow_resources = fetch_stackoverflow_resources(search_prompt)
        reddit_resources = fetch_reddit_resources(search_prompt)

        all_resources = stackoverflow_resources + reddit_resources
        validated_resources = validate_resources(all_resources)

        return render_template('index.html',
                               trending_repos=trending_repos_enriched,
                               latest_repos=latest_repos_enriched,
                               most_used_repos=most_used_repos_enriched,
                               resources=validated_resources.resources)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)