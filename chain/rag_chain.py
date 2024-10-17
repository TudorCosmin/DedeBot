import os
import qdrant_client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.retrievers import SelfQueryRetriever
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.query_constructor.base import AttributeInfo

from dotenv import load_dotenv

load_dotenv()

from chain.formatting import format_retrieved_documents, format_reply

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
collection_name = os.environ["QDRANT_COLLECTION_NAME"]
answer_template_path = "resources/answer_prompt_template.txt"

qclient = qdrant_client.QdrantClient(
    url = os.environ["QDRANT_HOST"],
    api_key = os.environ["QDRANT_API_KEY"],
)

vectorstore = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=os.environ["QDRANT_COLLECTION_NAME"],
    url=os.environ["QDRANT_HOST"],
    api_key=os.environ["QDRANT_API_KEY"],
)

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
document_content_description = "all the fields describing a product from a construction materials website"
metadata_field_info = [
    AttributeInfo(
        name="name",
        description="the name of the product",
        type="string",
    ),
    AttributeInfo(
        name="price",
        description="the price of the product",
        type="string",
    )
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents=document_content_description,
    metadata_field_info=metadata_field_info,
    enable_limit=True,
    verbose=True,
    search_kwargs={'k':5}
)

with open(answer_template_path, "r") as f:
    _answer_template = f.read()
ANSWER_PROMPT = ChatPromptTemplate.from_template(_answer_template)

_answer_prompt_params = {
    "context": retriever | format_retrieved_documents,
    "question": RunnablePassthrough()
}

rag_chain = ( {
    "query": RunnablePassthrough(), #lambda x: x["question"],
    "reply": _answer_prompt_params | ANSWER_PROMPT | llm | StrOutputParser()
} | RunnableLambda(format_reply))

# testing
# response = rag_chain.invoke("surub")
# print(response)