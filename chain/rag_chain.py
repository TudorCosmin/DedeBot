import os
import qdrant_client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.retrievers import SelfQueryRetriever
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.query_constructor.base import AttributeInfo
from operator import itemgetter
from qdrant_client.http import models as qdrant_models

from dotenv import load_dotenv

load_dotenv()

from chain.formatting import format_retrieved_documents, format_reply, format_chat_history, format_product_output

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
collection_name = "dedeman-screws-collection4" # os.environ["QDRANT_COLLECTION_NAME"]
answer_template_path = "resources/answer_prompt_template.txt"
condensation_template_path = "resources/condensation_prompt_template.txt"
top_k = 10

qclient = qdrant_client.QdrantClient(
    url = os.environ["QDRANT_HOST"],
    api_key = os.environ["QDRANT_API_KEY"],
)

vectorstore = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=collection_name,
    url=os.environ["QDRANT_HOST"],
    api_key=os.environ["QDRANT_API_KEY"],
    # distance=qdrant_models.Distance.EUCLID#"EUCLID"
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
    search_kwargs={'k':top_k}
)

with open(answer_template_path, "r") as f:
    _answer_template = f.read()
ANSWER_PROMPT = ChatPromptTemplate.from_template(_answer_template)

with open(condensation_template_path, "r") as f:
    _condansation_template = f.read()
CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_template(_condansation_template)

# Definition of the RAG pipeline
_condensation = RunnableMap(
    initial_question = lambda x: x["question"],
    standalone_question = { 
        "question": lambda x: x["question"], 
        "chat_history": lambda x: format_chat_history(x["chat_history"])
    } | CONDENSE_QUESTION_PROMPT | llm | StrOutputParser()
)

_retrieval_context = {
    "query": itemgetter("initial_question"),
    "documents": itemgetter("standalone_question") | retriever
}

_answer_prompt_params = {
    "context": _retrieval_context | RunnableLambda(format_retrieved_documents),
    "question": lambda x: x["standalone_question"],
    # "retrieved_documents": ex_retrieved_documents,
    # "retrieved_documents2": ex_retrieved_documents2,
}

history_chain = ({
    "query": lambda x: x["question"], # RunnablePassthrough(),
    "reply": _condensation | _answer_prompt_params | ANSWER_PROMPT | llm | StrOutputParser()
} | RunnableLambda(format_reply))

# _answer_prompt_params = {
#     "context": retriever | format_retrieved_documents,
#     "question": RunnablePassthrough()
# }

# rag_chain = ( {
#     "query": RunnablePassthrough(), #lambda x: x["question"],
#     "reply": _answer_prompt_params | ANSWER_PROMPT | llm | StrOutputParser()
# } | RunnableLambda(format_reply))

# testing
# response = rag_chain.invoke("surub")
# print(response)