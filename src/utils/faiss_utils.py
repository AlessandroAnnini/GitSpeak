import os
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate


def create_store(repo_name, docs):
    embeddings = OpenAIEmbeddings()

    db_path = f"faiss_index/{repo_name}"

    if os.path.exists(db_path):
        # delete db
        print(f"Found existing db at {db_path}, deleting...")
        os.remove(db_path)

    # create db
    print("Creating db...")
    db = FAISS.from_documents(docs, embeddings)

    # save db
    print(f"Saving db at {db_path}...")
    db.save_local(db_path)


def get_store(repo_names):
    embeddings = OpenAIEmbeddings()

    repo_names = repo_names.split(",")

    db_array = []

    # load all dbs
    for repo_name in repo_names:
        db_path = f"faiss_index/{repo_name}"

        if os.path.exists(db_path):
            print(f"Found existing db for {repo_name}, loading...")
            db = FAISS.load_local(db_path, embeddings)
            db_array.append(db)

    if len(db_array) == 0:
        raise ValueError("No db found for the given repo names.")

    # merge all dbs to the first one
    db = db_array[0]
    for i in range(1, len(db_array)):
        db.merge_from(db_array[i])

    return db


template = """
Use the following context (delimited by <CTX></CTX>) and the chat history (delimited by <HST></HST>) to answer the question,
do not include the separator lines in your answer.
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
        # verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": prompt,
            "memory": memory,
        },
    )

    # Return the result of the query
    return qa.run(query)
