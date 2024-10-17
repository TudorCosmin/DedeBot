import json

def format_retrieved_documents(docs):
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