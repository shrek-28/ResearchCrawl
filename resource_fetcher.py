import requests
from typing import List
from models import Resource, ResourceList

def fetch_stackoverflow_resources(query: str) -> List[dict]:
    url = "https://api.stackexchange.com/2.2/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": 5
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [{"title": item['title'], "url": item['link'], "platform": "Stack Overflow", "usage_count": item['view_count']} for item in data['items']]

def fetch_reddit_resources(query: str) -> List[dict]:
    url = "https://www.reddit.com/search.json"
    params = {
        "q": query,
        "limit": 5
    }
    headers = {"User-agent": "your bot 0.1"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return [{"title": item['data']['title'], "url": "https://reddit.com" + item['data']['permalink'], "platform": "Reddit", "usage_count": item['data']['num_comments']} for item in data['data']['children']]

def validate_resources(data: List[dict]) -> ResourceList:
    resources = [Resource(title=item['title'], url=item['url'], platform=item['platform'], usage_count=item['usage_count']) for item in data]
    return ResourceList(resources=resources)
