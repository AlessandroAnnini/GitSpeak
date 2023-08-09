import os
import argparse
import openai
import streamlit as st
from faiss_utils import get_store, create_chain, search_db

openai.api_key = os.environ.get("OPENAI_API_KEY")


def run_chat_app(name, chain):
    st.title(f"{name} GPT")
    st.caption(
        """<a
            href="https://github.com/AlessandroAnnini/GitSpeak"
            style="text-decoration:none; color:inherit"
            target="_blank"
            alt="GitSpeak">
                GitSpeak
            </a>""",
        unsafe_allow_html=True,
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(f"Ask me all about {name}"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Return the answer from the database
            answer = search_db(prompt, chain)

            for response in answer:
                full_response += response
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


def main(args):
    # transform folders from string to list
    folders = args.folder.replace("[", "").replace("]", "").replace("'", "").split(", ")

    name = " + ".join(folders)

    db = get_store(folders)
    chain = create_chain(db, args.model)

    print(f"Running chat app for {folders}...")
    run_chat_app(name, chain)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", type=str)
        parser.add_argument("--folder", type=str, required=True)
        args = parser.parse_args()
        main(args)
    except Exception as e:
        st.write("Fatal Error!")
        st.write(e)
