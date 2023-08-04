import openai
import os
import pathspec
import subprocess
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from utils.faiss_utils import create_store

# Set the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


def clone_repository(repo_url, local_path):
    """Clone the specified git repository to the given local path."""
    subprocess.run(["git", "clone", repo_url, local_path])


def load_docs(root_dir, file_extensions=None):
    """
    Load documents from the specified root directory.
    Ignore dotfiles, dot directories, and files that match .gitignore rules.
    Optionally filter by file extensions.
    """
    docs = []

    # Load .gitignore rules
    gitignore_path = os.path.join(root_dir, ".gitignore")

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            gitignore = gitignore_file.read()
        spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, gitignore.splitlines()
        )
    else:
        spec = None

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove dot directories from the list of directory names
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for file in filenames:
            file_path = os.path.join(dirpath, file)

            # Skip dotfiles
            if file.startswith("."):
                continue

            # Skip files that match .gitignore rules
            if spec and spec.match_file(file_path):
                continue

            if file_extensions and os.path.splitext(file)[1] not in file_extensions:
                continue

            try:
                loader = TextLoader(file_path, encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception:
                pass
    return docs


def split_docs(docs):
    """Split the input documents into smaller chunks."""
    text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
    return text_splitter.split_documents(docs)


def ingest(repo_url, include_file_extensions, repo_name):
    """
    Ingest a git repository by cloning it, filtering files, splitting documents,
    creating embeddings, and storing everything in a FAISS index.
    """
    local_path = f"repos/{repo_name}"

    clone_repository(repo_url, local_path)

    docs = load_docs(local_path, include_file_extensions)
    print(f"Loaded {len(docs)} documents")

    docs = split_docs(docs)
    print(f"Split into {len(docs)} chunks")

    create_store(repo_name, docs)
