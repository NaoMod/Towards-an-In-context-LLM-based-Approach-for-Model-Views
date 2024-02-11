import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.agents import Tool
from langchain.chains import RetrievalQA


class MetamodelRetrievalToolsCreator:

    def __init__(self, llm, open_ai_key):
        self.llm = llm
        self.open_ai_key = open_ai_key

    def create_retrieval_tools(self, documents=None):
        """
        Create retrieval tools for the given documents.

        Parameters
        ----------
        documents : list[dict], optional
            A list of dictionaries representing the documents. Each dictionary should have a 'name' key
            representing the name of the document and a 'content' key representing the content of the document,
            by default None

        Returns
        -------
        list[Tool]
            A list of Tool objects representing the retrieval tools created for each document.
        """

        # TODO: Read the user metamodels files

        # Read the metamodels files and create retrieval tools for each
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        meta1_rel_path = '../temp/Book.txt'
        meta2_rel_path = '../temp/Publication.txt'

        meta1_file = open(os.path.join(script_dir, meta1_rel_path), 'r')
        meta2_file = open(os.path.join(script_dir, meta2_rel_path), 'r')

        documents = [
            {"name": "Book", "content": meta1_file.read()},
            {"name": "Publication", "content": meta2_file.read()}
        ]

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        texts = text_splitter.create_documents(list(d['content'] for d in documents))

        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=self.open_ai_key)

        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)

        # Create retriever interface
        retriever = db.as_retriever()

        tools = []

        # Create QA chain inside the tools
        tools.append(
            Tool(
                name=documents[0]["name"],
                description=f"useful when you want to answer questions about {documents[0]['name']}",
                func=RetrievalQA.from_chain_type(llm=self.llm, chain_type='stuff', retriever=retriever),
            )
        )
        tools.append(
            Tool(
                name=documents[1]["name"],
                description=f"useful when you want to answer questions about {documents[1]['name']}",
                func=RetrievalQA.from_chain_type(llm=self.llm, chain_type='stuff', retriever=retriever),
            )
        )

        return tools