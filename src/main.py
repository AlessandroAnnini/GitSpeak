import os
import sys
import argparse
from dotenv import load_dotenv
from streamlit.web import cli as stcli
from utils.ingest import ingest

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()


def ingest_repo(args):
    """
    Ingest the git repository by cloning it, filtering files, and
    creating a FAISS index.
    """

    ingest(args.repo_url, args.exts)


def chat(args):
    """
    Start the Streamlit chat application using the specified FAISS index.
    """
    model = args.model_name if args.model_name else "gpt-3.5-turbo"

    sys.argv = [
        "streamlit",
        "run",
        "src/utils/chat.py",
        "--",
        f"--folder={args.repo_name}",
        f"--model={model}",
    ]

    sys.exit(stcli.main())


def list_repos():
    """
    List all the repos that have been ingested.
    """
    print("List of available repos:")
    repos = sorted(os.listdir("repos"))
    for repo in repos:
        print(f" - {repo}")


def main():
    """Define and parse CLI arguments, then execute the appropriate subcommand."""
    parser = argparse.ArgumentParser(description="Chat with a git repository")
    subparsers = parser.add_subparsers(dest="command")

    ########################################
    # Ingest subcommands

    ingest_parser = subparsers.add_parser("ingest", help="Ingest a git repository")

    ingest_parser.add_argument(
        "--repo-url",
        required=True,
        help="The url of the git repository to ingest",
    )

    ingest_parser.add_argument(
        "--exts",
        nargs="+",
        default=None,
        help=(
            "Exclude all files not matching these extensions. Example:"
            " --exts .py .js .ts .html .css .md .txt"
        ),
    )

    ########################################
    # Chat subcommands

    chat_parser = subparsers.add_parser("chat", help="Start the chat application")

    chat_parser.add_argument(
        "--model-name",
        help="The name of the model to use for chat. gpt-3.5-turbo or gpt-4",
    )

    chat_parser.add_argument(
        "--repo-name",
        required=True,
        nargs="+",
        help="One or more already ingested repository names to chat with",
    )

    ########################################
    # List subcommands

    subparsers.add_parser("list", help="List all ingested repositories")

    ########################################

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_repo(args)
    elif args.command == "chat":
        chat(args)
    elif args.command == "list":
        list_repos()


if __name__ == "__main__":
    main()
