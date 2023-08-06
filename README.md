# GitSpeak

## Setup

1. Clone the repository

2. Install the required packages with `pip`:

```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file:

```bash
cp .env.example .env
```

4. Provide your API keys and username:

```text
OPENAI_API_KEY=your_openai_api_key
```

5. Use the CLI to run the chatbot application. You can either ingest a Git repository or start the chat application using an existing dataset.

## How to use

> For complete CLI instructions run `python src/main.py --help`

### Ingest

To ingest a Git repository, use the `ingest` subcommand:

```bash
python src/main.py ingest --repo-url https://github.com/username/repo_name
```

You can also specify additional options, such as file extensions to include while ingesting the repository:

```bash
python src/main.py ingest --repo-url https://github.com/username/repo_name --exts .md .js .tsx
```

This will clone the repo locally and create a vector store index with the same name of the repo.

### Chat

To start the chat application using an existing dataset, use the `chat` subcommand with a repo name of a repo already ingested:

```bash
python src/main.py chat --repo-name <repo_name>
```

You can load multiple repositories by specifying multiple repo names:

```bash
python src/main.py chat --repo-name <repo_name> <repo_name2> <repo_name3>
```

The Streamlit chat app will run, and you can interact with the chatbot at `http://localhost:8501` (or the next available port) to ask questions about the repository.

### List

To list all the repositories that have been ingested, use the `list` subcommand:

```bash
python src/main.py list
```

## License

[MIT License](LICENSE)
