"""
Core functionality for image tag helper.
"""
import requests
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(7))
def get_image_tag_by_short_name(tag, arch, registry_url=None, repository=None):
    """
    Get the full image tag by short name.
    
    Args:
        tag: Short tag name
        arch: Architecture (e.g., amd64, arm64)
        registry_url: Registry URL, defaults to harbor.milvus.io
        repository: Repository path, defaults to milvus/milvus
        
    Returns:
        Full tag name
    """
    registry_url = registry_url or "harbor.milvus.io"
    repository = repository or "milvus/milvus"
    
    # Split repository into project and repo
    repo_parts = repository.split('/')
    if len(repo_parts) != 2:
        raise ValueError("Repository should be in format 'project/repository'")
    
    project, repo = repo_parts
    
    prefix = tag.split("-")[0]
    
    # Different handling based on registry type
    if "harbor" in registry_url:
        return _get_harbor_tag(registry_url, project, repo, prefix, tag, arch)
    elif "docker" in registry_url:
        return _get_docker_tag(registry_url, repository, prefix, tag, arch)
    else:
        # Default to harbor-like API
        return _get_harbor_tag(registry_url, project, repo, prefix, tag, arch)


def _get_harbor_tag(registry_url, project, repo, prefix, tag, arch):
    """Get tag from Harbor registry"""
    url = f"https://{registry_url}/api/v2.0/projects/{project}/repositories/{repo}/artifacts?with_tag=true&q=tags%253D~{prefix}-&page_size=100&page=1"
    
    response = requests.get(url)
    response.raise_for_status()
    
    rsp = response.json()
    tag_list = []
    
    for r in rsp:
        tags = r["tags"]
        for t in tags:
            tag_list.append(t["name"])
    
    tag_candidates = []
    for t in tag_list:
        r = t.split("-")
        if len(r) == 4 and arch in t:
            tag_candidates.append(t)
    
    tag_candidates.sort()
    if len(tag_candidates) == 0:
        return tag
    else:
        return tag_candidates[-1]


def _get_docker_tag(registry_url, repository, prefix, tag, arch):
    """Get tag from Docker Hub or compatible registry"""
    # Docker Hub API v2
    url = f"https://hub.docker.com/v2/repositories/{repository}/tags"
    
    response = requests.get(url)
    response.raise_for_status()
    
    rsp = response.json()
    tag_list = []
    
    for result in rsp.get("results", []):
        tag_name = result.get("name")
        last_updated = result.get("last_updated")
        if tag_name and last_updated:
            if tag_name.startswith(prefix) and tag_name.endswith(arch):
                r = tag_name.split("-")
                if len(r) == 4:  # version-date-commit-arch
                    tag_list.append((tag_name, last_updated))
    
    if not tag_list:
        return tag
    
    # 按更新时间排序，返回最新的标签
    tag_list.sort(key=lambda x: x[1], reverse=True)
    return tag_list[0][0]
