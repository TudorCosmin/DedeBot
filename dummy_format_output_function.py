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

# Example Usage
products = [
    {
        "title": "Pensula pentru vopsea alchidica Holzer, maner plastic, latime 70 mm",
        "link": "https://www.dedeman.ro/ro/pensula-pentru-vopsea-alchidica-holzer-maner-plastic-latime-70-mm/p/5013725",
        "image": "https://cdn.dedeman.ro/media/catalog/product/5/0/5013725.jpg?optimize=low&fit=bounds&height=266&width=266&canvas=266:266",
        "price": "7.59 lei",
        "description": "Pensula pentru vopsea alchidica Holzer este recomandata pentru aplicatii casnice. Aceasta este confectionata din amestec de par natural si sintetic pe suport din PVC, avand latimea de 70 mm. Pensula poate fi utilizata pentru orice tip de vopsea alchidica pe baza de solvent. Manerul este prevazut cu un orificiu, ideal pentru o depozitare facila prin agatarea intr-un suport. Dupa folosire, curatarea pensulei se poate realiza cu acelasi diluant sau solvent utilizat la prepararea vopselei sau a lacului.",
        "technical_specs": {
            "Brand": "Holzer",
            "Latime (mm)": "70",
            "Utilizare": "casnica",
            "Material maner": "PVC",
            "Rezistenta la solutii agresive": "Da",
            "Tip material fir": "par natural si sintetic"
        }
    },
    {
        "title": "Set 3 pensule universale Holzer, maner PVC, latime 30/50/70 mm",
        "link": "https://www.dedeman.ro/ro/set-3-pensule-universale-holzer-maner-pvc-latime-30/50/70-mm/p/5019926",
        "image": "https://cdn.dedeman.ro/media/catalog/product/5/0/5019926_1.jpg?optimize=low&fit=bounds&height=266&width=266&canvas=266:266",
        "price": "15.99 lei",
        "description": "Pensulele universale Holzer sunt potrivite pentru lucrarile de amenajari interioare. Manerul pensulelor este prevazut cu un orificiu, ideal pentru o depozitare facila prin agatarea intr-un suport. Dupa folosire, curatarea pensulei se poate realiza cu acelasi diluant sau solvent utilizat la prepararea vopselei sau a lacului. Setul contine 3 pensule, ce au urmatoarele dimensiuni: 30, 50 si 70 mm.",
        "technical_specs": {
            "Culoare": "portocaliu",
            "Latime (mm)": "70",
            "Utilizare": "aplicare vopsele",
            "Material maner": "PVC"
        }
    }
]

# Display formatted output for each product
for product in products:
    output = format_product_output(product)
    print(output)