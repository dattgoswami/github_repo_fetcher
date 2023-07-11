# GitHub Repository Fetcher and Analyzer

This script fetches repositories of a specified GitHub user, groups them by primary language, and writes the results to a CSV file.

## Dependencies

- requests: To make HTTP requests to the GitHub API.
- csv: To write the repository data to a CSV file.

```
pip install requests csv
```

## Usage

1. Set the `access_token` and `username` variables in the `main` function to your GitHub personal access token and username, respectively.
2. Run the script.

```
python get_github_repos.py
```

3. When prompted, enter '1' for starred repositories or '2' for regular repositories.
4. The script will fetch the repositories, group them by primary language, and generate a CSV file with the results.

Note: Make sure to replace `'ACCESS_TOKEN'` with your GitHub personal access token and `'USERNAME'` with your GitHub username before running the script.

## Functionality

- `fetch_github_repositories(url, headers)`: Fetches the repositories from the specified GitHub API endpoint.
- `get_repository_language(repo, headers)`: Retrieves the primary language of a repository.
- `group_repositories_by_language(repositories, headers)`: Groups repositories by primary language.
- `write_repositories_to_csv(repositories, filename)`: Writes the repository data to a CSV file.
- `main()`: The main entry point of the script.

The script provides flexibility to fetch either starred repositories or regular repositories based on the user's choice. The generated CSV file will contain the grouped repositories by primary language.
