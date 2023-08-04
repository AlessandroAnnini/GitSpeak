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

5. Use the CLI to run the chatbot application. You can either process a Git repository or start the chat application using an existing dataset.

## How to use

> For complete CLI instructions run `python src/main.py --help`

To process a Git repository, use the `process` subcommand:

```bash
python src/main.py process --repo-url https://github.com/username/repo_name
```

You can also specify additional options, such as file extensions to include while processing the repository:

```bash
python src/main.py process --repo-url https://github.com/username/repo_name --include-file-extensions .md .js .tsx
```

This will clone the repo locally and create a vector store index with the same name of the repo.

To start the chat application using an existing dataset, use the `chat` subcommand with a repo name of a repo already processed:

```bash
python src/main.py chat --repo-name <repo_name>
```

The Streamlit chat app will run, and you can interact with the chatbot at `http://localhost:8501` (or the next available port) to ask questions about the repository.

## License

[MIT License](LICENSE)