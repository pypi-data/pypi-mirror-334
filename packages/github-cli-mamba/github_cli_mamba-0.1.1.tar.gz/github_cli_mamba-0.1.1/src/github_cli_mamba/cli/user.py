import typer

from github_cli_mamba.github import GithubAPI
from github_cli_mamba.options import OutputOption
from github_cli_mamba.utils import print_beautify

user_app = typer.Typer()


@user_app.command(name="profile", help="list user profile")
def profile(
    username: str = typer.Option(..., "--username", "-u", help="github username")
):
    github_api = GithubAPI()
    repos = github_api.get_all_user_repositories(username)
    followers = github_api.list_followers_of_user(username)
    followings = github_api.list_people_user_follows(username)

    profile = {
        "username": username,
        "followers": len(followers) if followers else 0,
        "followings": len(followings) if followings else 0,
        "repos": len(repos) if repos else 0,
    }
    print_beautify([profile], OutputOption.table)
