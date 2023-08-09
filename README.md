# GitSpeak

GitSpeak is a chat application that allows you to interact with a chatbot using a context-aware data splitted dataset generated from Git repositories. It provides a conversational interface where you can ask questions about the repositories and get relevant answers.

## Use cases

GitSpeak has several use cases, including:

1. 📝 **Code Documentation:** GitSpeak can be used to automatically generate documentation for code repositories. It can extract information from code comments, commit messages, and other code-related artifacts to create comprehensive documentation.

2. 🔍 **Code Search:** GitSpeak enables powerful code search capabilities. It allows users to search for specific code snippets, functions, or classes within a repository, making it easier to find and reuse code.

3. 🚀 **Knowledge Discovery:** GitSpeak can help researchers and developers discover knowledge within code repositories. By analyzing the codebase, it can identify patterns, best practices, and common pitfalls, providing valuable insights for software development.

4. 🧠 **Code Understanding:** GitSpeak aids in understanding codebases by providing contextual information. It can generate summaries, explanations, and examples for code artifacts, making it easier for developers to navigate and comprehend complex codebases.

5. ⏭️ **Code Recommendation:** GitSpeak can suggest code improvements and optimizations based on analyzing existing code. It can identify areas for refactoring, performance enhancements, and bug fixes, helping developers write better code.

These are just a few examples of the use cases for GitSpeak. Its capabilities extend beyond this list, making it a versatile tool for code analysis and understanding.

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

Optionally you can choose to use a different openai model by specifying the `--model-name` option. Default is `gpt-3.5-turbo`:

```bash
python src/main.py chat --repo-name <repo_name> --model-name gpt-4
```

The Streamlit chat app will run, and you can interact with the chatbot at `http://localhost:8501` (or the next available port) to ask questions about the repository.

### List

To list all the repositories that have been ingested, use the `list` subcommand:

```bash
python src/main.py list
```

## License

[MIT License](LICENSE)
