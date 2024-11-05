import boto3
import json
import os
import subprocess

# Initialize boto3 client for CodeCommit
codecommit_client = boto3.client('codecommit')

def get_repositories_info():
    repositories_info = []

    # List all repositories in CodeCommit
    response = codecommit_client.list_repositories()
    repositories = response.get('repositories', [])

    for repo in repositories:
        repo_name = repo['repositoryName']
        
        # Get repository metadata including clone URLs
        repo_metadata = codecommit_client.get_repository(repositoryName=repo_name)
        clone_url_http = repo_metadata['repositoryMetadata']['cloneUrlHttp']
        
        # Append to the list as a dictionary
        repositories_info.append({
            "repository_name": repo_name,
            "clone_url": clone_url_http
        })

    return repositories_info

def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Repository information saved to {file_path}")

def clone_repositories(repositories_info, clone_directory):
    # Ensure the clone directory exists
    os.makedirs(clone_directory, exist_ok=True)
    
    for repo_info in repositories_info:
        repo_name = repo_info['repository_name']
        clone_url = repo_info['clone_url']
        repo_path = os.path.join(clone_directory, repo_name)
        
        if not os.path.exists(repo_path):
            print(f"Cloning {repo_name} into {repo_path}...")
            subprocess.run(['git', 'clone', clone_url, repo_path])
        else:
            print(f"Repository {repo_name} already exists in {clone_directory}.")

# Example usage
output_json_file = 'repositories.json'
clone_directory = '/path/to/clone/directory'

# Step 1: Get repository info and save to JSON
repositories_info = get_repositories_info()
save_to_json(repositories_info, output_json_file)

# Step 2: Clone each repository into the specified directory
clone_repositories(repositories_info, clone_directory)
