import jmespath
import typer

from github_cli_mamba.github import GithubAPI
from github_cli_mamba.options import OutputOption
from github_cli_mamba.utils import print_beautify, sort_by_field

repo_app = typer.Typer()


@repo_app.command(name="list", help="List all repositories for a user")
def list_repos(
    username: str = typer.Option(
        ..., "--username", "-u", help="The username to list repositories for"
    ),
    output: OutputOption = typer.Option(
        OutputOption.json, "--output", "-o", help="The output format"
    ),
    query: str = typer.Option(None, "--query", "-q", help="query with jmespath"),
    sort: str = typer.Option(None, "--sort", "-s", help="sort by field"),
):
    github_api = GithubAPI()
    repos = github_api.get_all_user_repositories(username)
    if query:
        # filter query: "[?language == 'Python' && description != None && contains(description, 'Python')]"
        # sort query: "sort_by(@, &stars).reverse(@)"
        # filter and sort query: "sort_by([?language == 'Python'], &stars).reverse(@)"
        repos = jmespath.search(query, repos)
    if sort:
        if sort.startswith("~"):
            reverse = True
            sort = sort[1:].split(",")
        else:
            reverse = False
        repos = sort_by_field(repos, sort, reverse)
    print_beautify(repos, output)


@repo_app.command(name="delete", help="Delete a repository for a user")
def delete_repo(
    username: str = typer.Option(
        ..., "--username", "-u", help="The username to delete repository for"
    ),
    repo: str = typer.Option(..., "--repo", "-r", help="The repository to delete"),
):
    github_api = GithubAPI()
    if github_api.delete_repository_for_user(username, repo):
        print(f"Repository {repo} deleted successfully")
    else:
        print(f"Failed to delete user {username}, repository {repo}")
