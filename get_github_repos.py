"""
GitHub Repository Fetcher and Analyzer

This script fetches repositories of a specified GitHub user, groups them by primary language, and writes the results to a CSV file.

Dependencies:
- requests: To make HTTP requests to the GitHub API.
- csv: To write the repository data to a CSV file.

Usage:
1. Set the `access_token` and `username` variables in the `main` function to your GitHub personal access token and username, respectively.
2. Run the script.

"""

import sys
import requests
import csv

def fetch_github_repositories(url, headers):
    """
    Fetches the repositories from the specified GitHub API endpoint.

    Args:
        url (str): The URL of the GitHub API endpoint.
        headers (dict): The HTTP headers for authentication.

    Returns:
        list: A list of dictionaries representing the fetched repositories.
    """
    repositories = []

    page = 1
    while True:
        params = {'page': page, 'per_page': 100}
        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            repositories += response.json()

            if 'Link' in response.headers:
                links = response.headers['Link'].split(', ')
                next_link = next((l for l in links if 'rel="next"' in l), None)
                if next_link:
                    url = next_link[next_link.find(
                        '<') + 1:next_link.find('>')]
                    page += 1
                else:
                    break
            else:
                break
        else:
            print(f'Error: {response.status_code}')
            break

    return repositories

def get_repository_language(repo, headers):
    """
    Retrieves the primary language of a repository.

    Args:
        repo (dict): A dictionary representing a repository.
        headers (dict): The HTTP headers for authentication.

    Returns:
        str: The primary language of the repository.
    """
    languages_url = repo['languages_url']
    response = requests.get(languages_url, headers=headers)
    if response.ok:
        languages_data = response.json()
        languages = list(languages_data.keys())
        language = languages[0] if languages else 'N/A'
    else:
        language = 'N/A'
    return language

def group_repositories_by_language(repositories, headers):
    """
    Groups repositories by primary language.

    Args:
        repositories (list): A list of dictionaries representing repositories.
        headers (dict): The HTTP headers for authentication.

    Returns:
        dict: A dictionary with primary languages as keys and a list of repositories as values.
    """
    grouped_repositories = {}
    for repo in repositories:
        name = repo['name']
        description = repo['description']
        language = get_repository_language(repo, headers)

        if language not in grouped_repositories:
            grouped_repositories[language] = []
        grouped_repositories[language].append((name, description))

    return grouped_repositories

def write_repositories_to_csv(repositories, filename):
    """
    Writes the repository data to a CSV file.

    Args:
        repositories (dict): A dictionary with primary languages as keys and a list of repositories as values.
        filename (str): The name of the CSV file.
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Language', 'Repository Name', 'Description'])
        for language, repos in repositories.items():
            for repo in repos:
                writer.writerow([language, repo[0], repo[1]])

    print(f"Repositories written to '{filename}' file.")

def main():
    """
    The main entry point of the script.
    """
    access_token = 'ACCESS_TOKEN'
    username = 'USERNAME'
    mode = input(
        "Enter '1' for starred repositories or '2' for regular repositories: ")

    if mode == '1':
        url = f'https://api.github.com/users/{username}/starred'
        filename = 'starred_repositories.csv'
    elif mode == '2':
        url = f'https://api.github.com/users/{username}/repos'
        filename = 'repositories.csv'
    else:
        print("Invalid mode. Exiting the script.")
        sys.exit(1)

    headers = {'Authorization': f'token {access_token}'}
    repositories = fetch_github_repositories(url, headers)
    grouped_repositories = group_repositories_by_language(
        repositories, headers)
    write_repositories_to_csv(grouped_repositories, filename)

if __name__ == '__main__':
    main()
