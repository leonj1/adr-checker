import sys
import os
import requests
from urllib.parse import quote_plus

def get_merge_requests(project_id, access_token):
    base_url = "https://gitlab.com/api/v4"
    endpoint = f"/projects/{project_id}/merge_requests"
    params = {
        "state": "opened",
        "order_by": "created_at",
        "sort": "desc"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch merge requests. Status code: {response.status_code}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python list_gitlab_mrs.py <repository_path>")
        print("Example: python list_gitlab_mrs.py group/project")
        sys.exit(1)

    access_token = os.environ.get('GITLAB_ACCESS_TOKEN')
    if not access_token:
        print("Error: GITLAB_ACCESS_TOKEN environment variable is not set.")
        sys.exit(1)

    repo_path = sys.argv[1]
    encoded_repo_path = quote_plus(repo_path)

    merge_requests = get_merge_requests(encoded_repo_path, access_token)

    if merge_requests:
        print(f"Open Merge Requests for {repo_path}:")
        for mr in merge_requests:
            print(f"#{mr['iid']} - {mr['title']} (Created: {mr['created_at']})")
    else:
        print("No merge requests found or an error occurred.")

if __name__ == "__main__":
    main()
