import sys

import requests
import os

import yaml


def list_files_in_github_directory(repo_owner, repo_name, directory_path):
    """
    Recursively list files in a GitHub repository directory with full paths.

    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        directory_path (str): The path to the directory in the repository.

    Returns:
        list: A list of full path strings for each item.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}"
    response = requests.get(api_url)
    response.raise_for_status()
    contents = response.json()

    items = []
    for item in contents:
        full_path = f"{directory_path}/{item['name']}"
        items.append(full_path)
        if item['type'] == 'dir':
            sub_items = list_files_in_github_directory(repo_owner, repo_name, full_path)
            items.extend(sub_items)

    return items


def download_github_directory(repo_owner, repo_name, directory_path, local_path):
    """
    Download a specific directory from a GitHub repository using the GitHub API.

    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        directory_path (str): The path to the directory in the repository.
        local_path (str): The local path where the directory should be saved.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}"
    response = requests.get(api_url)
    response.raise_for_status()
    contents = response.json()

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    for item in contents:
        item_path = os.path.join(local_path, item['name'])
        if item['type'] == 'dir':
            download_github_directory(repo_owner, repo_name, item['path'], item_path)
        else:
            download_file(item['download_url'], item_path)


def download_file(url, local_path, overwrite=False):
    """
    Download a file from a URL and save it locally.

    Args:
        url (str): The URL of the file to download.
        local_path (str): The local path where the file should be saved.
        overwrite (bool): Whether to overwrite the file if it already exists.
    """
    response = requests.get(url)
    response.raise_for_status()
    if os.path.exists(local_path) and not overwrite:
        # raise FileExistsError(f"File already exists at {local_path}")
        # print(f"File already exists at {local_path}", file=sys.stderr)
        pass
    else:
        print(f"Downloading {url} to {local_path}", file=sys.stderr)
        with open(local_path, 'wb') as file:
            file.write(response.content)


def ls_yaml_files(local_path):
    """
    Recursively print the full path names of YAML files in the given local path.

    Args:
        local_path (str): The local directory path to search for YAML files.
    """
    _files = []
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                _files.append(os.path.join(root, file))
    return _files


def ls(local_path) -> list[dict]:
    """List the graph definitions from the FHIR Aggregator repository, download if necessary."""
    repo_owner = "FHIR-Aggregator"
    repo_name = "fhir-query"
    directory_path = "graph-definitions"
    local_path = os.path.join(local_path, directory_path)
    if not os.path.exists(local_path):
        download_github_directory(repo_owner, repo_name, directory_path, local_path)
    paths = ls_yaml_files(local_path)

    def _description(path):
        with open(path, 'r') as file:
            try:
                graph_definition_dict = yaml.safe_load(file)
                return graph_definition_dict.get('description', 'No description found')
            except yaml.YAMLError as e:
                return f'Error loading description {e}'

    return [{'path': path, 'description': _description(path)} for path in paths]
