import os
import re
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate


def github_url_to_folder_name(url, separator="_"):
    """
    Function to translate a Github repo URL to a valid folder name.

    Parameters:
    url (str): The Github repo URL.
    separator (str): The character used to separate the username and repo name.

    Returns:
    str: A valid folder name derived from the Github repo URL.
    """

    # Regular expression to extract username and repo name
    pattern = r"github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    if match:
        username, repo = match.groups()

        # Create a valid folder name by combining username and repo name
        folder_name = f"{username}{separator}{repo}"

        return folder_name

    else:
        raise ValueError("Invalid GitHub URL.")


def get_db(repo_name, docs=None):
    embeddings = OpenAIEmbeddings()

    db_path = f"faiss_index/{repo_name}"

    # if no db exists on the path, create one
    if not os.path.exists(db_path):
        # create db
        db = FAISS.from_documents(docs, embeddings)
        # save db
        db.save_local(db_path)
    else:
        # load db
        db = FAISS.load_local(db_path, embeddings)

    return db


template = """
Use the following context (delimited by <CTX></CTX>) and the chat history (delimited by <HST></HST>) to answer the question:
------
<CTX>
{context}
</CTX>
------
<HST>
{history}
</HST>
------
{question}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "history", "question"],
    template=template,
)

memory = ConversationBufferWindowMemory(
    k=2,
    memory_key="history",
    input_key="question",
)


def search_db(db, query):
    """Search for a response to the query in the DeepLake database."""

    # Create a retriever from the DeepLake instance
    retriever = db.as_retriever()

    # Set the search parameters for the retriever
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 100
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 10

    # Create a ChatOpenAI model instance
    model = ChatOpenAI(model="gpt-3.5-turbo-16k")

    # Create a RetrievalQA instance from the model and retriever

    # without memory
    # qa = RetrievalQA.from_llm(
    #     model,
    #     retriever=retriever,
    # )

    # with memory
    qa = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        verbose=True,
        # return_source_documents=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": prompt,
            "memory": memory,
        },
    )

    # Return the result of the query
    return qa.run(query)
