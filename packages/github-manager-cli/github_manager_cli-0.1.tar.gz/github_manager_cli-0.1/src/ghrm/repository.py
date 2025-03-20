# repository.py - Repository module for GitHub Manager CLI

import os
import yaml
from dotenv import load_dotenv
from github import Github, GithubException, Auth

# Load environment variables from .env file
load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_ORG = os.environ.get("GITHUB_ORG")

# Get access to the organization using GITHUB_TOKEN.
auth = Auth.Token(f"{GITHUB_TOKEN}")
g = Github(auth=auth)
org = g.get_organization(f"{GITHUB_ORG}")

def get_repo(repo_name):
    """
    Fetches a repo from GitHub organization.
    """
    try:
        repo = org.get_repo(repo_name)
        if repo.name:
            print(f"Repository `{repo_name}` exists within GitHub {org}")
            return repo
    except GithubException as e:
        if e.status == 404:
            print(f"Repository `{repo_name}` does not exist within GitHub {org}")
            return None
        else:
            print(f"Error fetching repository from GitHub {org} - {str(e)}")
            raise e

def load_repo_configs(config_file):
    """
    Loads repository configurations from a YAML file.
    """
    with open(config_file, 'r') as f:
        try:
            repos = yaml.load(f, Loader=yaml.FullLoader)
            return repos.get("repositories", {})
        except yaml.YAMLError as e:
            print("Invalid YAML", e)
            return {}

def configure_repository(config_file):
    """
    Creates GitHub repositories based on YAML configuration.
    """
    repo_configs = load_repo_configs(config_file)

    for repo_name, repo_config in repo_configs.items():
        repo = get_repo(repo_name)
        repo_config["name"] = repo_name

        if repo is None:
            try:
                print(f"Creating GitHub repository `{repo_name}`")
                org.create_repo(**repo_config)
            except GithubException as e:
                if e.status == 422:
                    print(f"Repository `{repo_name}` already exists.")
                else:
                    print(f"Error creating repository `{repo_name}`: {str(e)}")
                    raise e
        else:
            print(f"Update GitHub repository `{repo_name}`")
            # Remove unsupported arguments for the edit method
            unsupported_args = ["auto_init", "gitignore_template", "license_template"]
            for arg in unsupported_args:
                repo_config.pop(arg, None)
            repo.edit(**repo_config)

def create_repository(repo_name, description=None, repo_config=None):
    """
    Creates a single GitHub repository.
    """
    repo = get_repo(repo_name)
    default_config = {
        "name": repo_name,
        "description": description,
        "private": True
    }
    if repo_config is None:
        repo_config = default_config
    else:
        repo_config = {**default_config, **repo_config}

    if repo is None:
        try:
            print(f"Creating GitHub repository `{repo_name}`")
            org.create_repo(**repo_config)
            return "created"
        except GithubException as e:
            if e.status == 422:
                print(f"Repository `{repo_name}` already exists.")
            else:
                print(f"Error creating repository `{repo_name}`: {str(e)}")
                raise e
    else:
        print(f"Repository `{repo_name}` already exists. Updating repository.")
        # Remove unsupported arguments for the edit method
        unsupported_args = ["auto_init", "gitignore_template", "license_template"]
        for arg in unsupported_args:
            repo_config.pop(arg, None)
        try:
            repo.edit(**repo_config)
            return "updated"
        except GithubException as e:
            print(f"Error updating repository `{repo_name}`: {str(e)}")
            raise e

def delete_repository(repo_name):
    """
    Deletes GitHub repository.
    """
    repo = get_repo(repo_name)
    if repo:
        print(f"Deleting GitHub repository `{repo_name}`")
        repo.delete()
        return True
    else:
        print(f"Repository `{repo_name}` does not exist. Skipping deletion.")
        return False

def decommission_repository(repositories_decom_list):
    """
    To delete repositories based on a list in YAML config.
    """
    with open(f"{repositories_decom_list}", 'r') as f:
        try:
            repos = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print("Invalid YAML", e)
            return

    repo_names = repos.get("repositories", [])
    for repo_name in repo_names:
        delete_repository(repo_name)
