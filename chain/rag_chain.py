from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

model = ChatOpenAI(streaming=True)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "answer this query:",
        ),
        ("human", "{question}"),
    ]
)
rag_chain = prompt | model | StrOutputParser()