from pydantic import BaseModel
from typing import List

class Repository(BaseModel):
    name: str
    description: str
    stars: int
    forks: int
    url: str

class RepositoryList(BaseModel):
    repositories: List[Repository]

class Resource(BaseModel):
    title: str
    url: str
    platform: str
    usage_count: int

class ResourceList(BaseModel):
    resources: List[Resource]
