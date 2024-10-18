import json

def format_retrieved_documents(context):
    query = context["query"]
    docs = context["documents"]
    print("---------------------------------------- FRD\n\n")

    # for doc in docs:
    #     print(doc)
    #     print()
    

    formattedDocs = []
    strResult = ""
    for index, doc in enumerate(docs):
        if index == 0:
            print(doc.page_content)
            print("\n")
            print(doc)
            print(doc.metadata)
        formattedDocs.append({
            f"[doc{index}]": {
                "content": doc.page_content,

                # TODO: make the documents pretty for the prompt
                # "url": doc.metadata['url'],
                # "price": doc.metadata["price"],
            }
        })

    print("\n---------------------------------------- FRD")
    
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

def format_product_output(product):
    """
    Formats the product details into a structured string with a red title link
    and bullet points for the description.

    Parameters
    ----------
    product : dict
        A dictionary representing a product with keys: title, price, description, and link.

    Returns
    -------
    str
        A formatted string containing the product title (as a hyperlink), price, 
        and description as a bullet list.
    """
    title = product.get("title", "Title not available")
    price = product.get("price", "Price not available")
    description = product.get("description", "Description not available")
    link = product.get("link", "#")

    # Split the description into bullet points
    bullet_points = [sentence.strip() + '.' for sentence in description.split('.') if sentence]

    # Format the output using Markdown for styling and bullet points
    formatted_output = f"**Product Title:** [{title}]({link})  \n"
    formatted_output += f"**Price:** {price}  \n\n"
    formatted_output += "**Description:**  \n"

    # Add bullet points to the formatted output
    for point in bullet_points:
        formatted_output += f"- {point}\n"
    
    return formatted_output