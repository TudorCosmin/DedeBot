from dotenv import load_dotenv
import os
import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.schema import Document
from typing import List, Dict, Any
from tqdm import tqdm

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

def format_to_docs(file_name: str, data: List[Dict[str, Any]]) -> List[Document]:
    docs = []

    for product in tqdm(data, desc=f"Processing {file_name}", unit="product"):
        doc = Document(
            page_content=json.dumps(product),
            metadata=product
        )
        docs.append(doc)

    return docs

def process_json_files(folder_path: str) -> List[Document]:
    docs = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                data_docs = format_to_docs(file_name, data)
                docs.extend(data_docs)
    return docs

def run_qdrant_upload(input_folderpath="data2", collection_name="dedeman-collection2"):
    print("Starting processing files...")
    docs = process_json_files(folder_path=input_folderpath)

    print("Files processed. Uploading to qdrant...")

    upload_docs_to_qdrant(docs=docs, collection_name=collection_name)

if __name__ == "__main__":
    run_qdrant_upload()

    # print(os.environ['OPENAI_API_KEY'])