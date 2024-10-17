from dotenv import load_dotenv
import os
import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.schema import Document
from typing import List, Dict, Any

load_dotenv()

def read_json(input_path: str) -> Dict[str, Any]:
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(len(data))
    return data

def upload_docs_to_qdrant(docs: List[Document], collection_name: str) -> None:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Qdrant.from_documents(
        documents=docs,
        embedding=embeddings,
        url=os.environ['QDRANT_HOST'],
        api_key=os.environ["QDRANT_API_KEY"],
        collection_name=collection_name
    )

def format_to_docs(data: List[Dict[str, Any]]) -> List[Document]:
    docs = []

    for product in data:
        doc = Document(
            page_content=json.dumps(product),
            metadata=product
        )
        docs.append(doc)

    return docs

def run_qdrant_upload(input_filepath="data/dummy_input.json", collection_name="test-collection"):
    data = read_json(input_path=input_filepath)

    docs = format_to_docs(data=data)

    upload_docs_to_qdrant(docs=docs, collection_name=collection_name)

if __name__ == "__main__":
    run_qdrant_upload()