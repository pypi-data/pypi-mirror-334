import os

import typer
from dotenv import load_dotenv

from github_cli_mamba.cli.repo import repo_app
from github_cli_mamba.cli.user import user_app

if os.path.exists(".env"):
    load_dotenv()


app = typer.Typer()


app.add_typer(repo_app, name="repo", help="github repository commands")
app.add_typer(user_app, name="user", help="github user commands")

if __name__ == "__main__":
    app()
