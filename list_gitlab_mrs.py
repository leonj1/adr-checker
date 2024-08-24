import requests
import sys
import argparse
import urllib.parse
import os
from collections import defaultdict

def validate_args(args):
    if not args.access_token or args.access_token.isspace():
        raise ValueError("Access token is required and cannot be empty.")
    if not args.project or args.project.isspace():
        raise ValueError("Project path is required and cannot be empty.")

def get_project_id(base_url, project_path, access_token):
    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f"{base_url}/api/v4/projects/{encoded_path}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['id']

def fetch_open_merge_requests(base_url, project_id, access_token):
    url = f"{base_url}/api/v4/projects/{project_id}/merge_requests"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "opened"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    merge_requests = response.json()
    
    # Fetch thumbs up for each merge request
    for mr in merge_requests:
        mr['thumbs_up'] = fetch_thumbs_up(base_url, project_id, mr['iid'], access_token)

    return merge_requests

def fetch_thumbs_up(base_url, project_id, mr_iid, access_token):
    url = f"{base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/award_emoji"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"name": "thumbsup"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return [award['user']['name'] for award in response.json()]

def main():
    parser = argparse.ArgumentParser(description="Fetch open merge requests from a GitLab repository")
    parser.add_argument("project", help="GitLab project path (e.g., 'username/project' or 'group/subgroup/project')")
    parser.add_argument("--access_token", help="GitLab personal access token")
    parser.add_argument("--base-url", default="https://gitlab.com", help="GitLab instance URL (default: https://gitlab.com)")

    args = parser.parse_args()

    # If access_token is not provided as an argument, try to get it from the environment variable
    if not args.access_token:
        args.access_token = os.environ.get('GITLAB_ACCESS_TOKEN')

    try:
        validate_args(args)

        project_id = get_project_id(args.base_url, args.project, args.access_token)
        print(f"Fetched project ID: {project_id}")

        merge_requests = fetch_open_merge_requests(args.base_url, project_id, args.access_token)
        print(f"\nOpen Merge Requests for project {args.project}:")
        for mr in merge_requests:
            thumbs_up = ", ".join(mr['thumbs_up']) if mr['thumbs_up'] else "None"
            print(f"- [{mr['iid']}] {mr['title']} (by {mr['author']['name']})")
            print(f"  Thumbs up: {thumbs_up}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
