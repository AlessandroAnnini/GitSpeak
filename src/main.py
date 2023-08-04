import argparse
import sys
from dotenv import load_dotenv
from streamlit.web import cli as stcli
from utils.process import process

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()


def extract_repo_name(repo_url):
    """Extract the repository name from the given repository URL."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    return repo_name


def process_repo(args):
    """
    Process the git repository by cloning it, filtering files, and
    creating a FAISS index.
    """
    repo_name = extract_repo_name(args.repo_url)

    process(
        args.repo_url,
        args.include_file_extensions,
        repo_name,
    )


def chat(args):
    """
    Start the Streamlit chat application using the specified FAISS index.
    """

    sys.argv = [
        "streamlit",
        "run",
        "src/utils/chat.py",
        "--",
        f"--folder={args.repo_name}",
    ]

    sys.exit(stcli.main())


def main():
    """Define and parse CLI arguments, then execute the appropriate subcommand."""
    parser = argparse.ArgumentParser(description="Chat with a git repository")
    subparsers = parser.add_subparsers(dest="command")

    ########################################
    # Process subcommands

    process_parser = subparsers.add_parser("process", help="Process a git repository")

    process_parser.add_argument(
        "--repo-url",
        required=True,
        help="The url of the git repository to process",
    )

    process_parser.add_argument(
        "--include-file-extensions",
        nargs="+",
        default=None,
        help=(
            "Exclude all files not matching these extensions. Example:"
            " --include-file-extensions .py .js .ts .html .css .md .txt"
        ),
    )

    ########################################
    # Chat subcommands

    chat_parser = subparsers.add_parser("chat", help="Start the chat application")

    chat_parser.add_argument(
        "--repo-name",
        required=True,
        help="One or more comma-separated already processed repository names to chat with",
    )

    ########################################

    args = parser.parse_args()

    if args.command == "process":
        process_repo(args)
    elif args.command == "chat":
        chat(args)


if __name__ == "__main__":
    main()

## Example usage:
"""
```bash
python3 main.py process --repo-url <repo_url> --include-file-extensions .py .js .ts .html .css .md .txt
```

python3 src/main.py process --repo-url https://github.com/hyperledger/hyperledger-hip --include-file-extensions .md


Then to chat with the repository:

```bash
python3 main.py chat --repo-name <repo_name>
```

python3 main.py chat --repo-name hyperledger-hip

"""
