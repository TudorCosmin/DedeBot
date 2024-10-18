import json

def format_retrieved_documents(context):
    query = context["query"]
    docs = context["documents"]
    print("---------------------------------------- FRD\n\n")

    for doc in docs:
        print(doc)
        print()
    print("\n---------------------------------------- FRD")

    formattedDocs = []
    strResult = ""
    for index, doc in enumerate(docs):
        formattedDocs.append({
            f"[doc{index}]": {
                "content": doc.page_content,

                # TODO: make the documents pretty for the prompt
                # "url": doc.metadata['url'],
                # "price": doc.metadata["price"],
            }
        })
    
    strResult = json.dumps(formattedDocs)
    
    if strResult == "":
        return json.dumps({"retrieved_documents": []})
    return strResult

def format_reply(reply):
    
    print("---------- am ajuns in FR")
    
    return reply["reply"]

def format_chat_history(chat_history):
    # def estimate_tokens(text: str) -> int:
    #     return (len(text) + 2) / 3
    # maxTokens = 10000
    
    buffer = ""
    for dialogue_turn in list(reversed(chat_history)):
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]#.split("\nRetrieved documents:\n[doc0]:")[0]
        buffer = "\n" + "\n".join([human, ai]) + buffer

        # if (estimate_tokens(buffer) > maxTokens):
        #   break
    return buffer