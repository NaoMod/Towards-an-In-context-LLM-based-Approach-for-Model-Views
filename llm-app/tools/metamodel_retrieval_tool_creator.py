import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.agents import Tool
from langchain.chains import RetrievalQA


class MetamodelRetrievalToolCreator:

    def __init__(self, llm, open_ai_key):
        self.llm = llm
        self.open_ai_key = open_ai_key

    def create_retrieval_tool(self, document=None):
        """
        Create retrieval tool for the given document.

        Parameters
        ----------
        document : list[dict], optional
            A dictionary representing the document. It should have a 'name' key
            representing the name of the document and a 'content' key representing the content of the document,
            by default None

        Returns
        -------
        Tool
            A Tool object representing the retrieval tool created for the document.
        """  

        if document is None:
            # Fallback to the Book example
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            meta1_rel_path = '../temp/Book.txt'            

            meta1_file = open(os.path.join(script_dir, meta1_rel_path), 'r')
            
            document = {"name": "Book", "content": meta1_file.read()}
            

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        texts = text_splitter.create_documents(document['content'])

        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=self.open_ai_key)

        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)

        # Create retriever interface
        retriever = db.as_retriever()

        return Tool(
                name=document["name"],
                description=f"useful when you want to analyze or get information from the PlantUML metamodel {document['name']}",
                func=RetrievalQA.from_chain_type(llm=self.llm, chain_type='stuff', retriever=retriever),
        )