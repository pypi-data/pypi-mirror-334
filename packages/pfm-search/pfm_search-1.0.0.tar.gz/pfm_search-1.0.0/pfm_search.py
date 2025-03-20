import requests

SEARCH_API = "https://pfm-search.sytes.net/search?q="

def search(query, format="text"):
    """
    Fetch search results from PFM-Search.

    :param query: Search query string
    :param format: "html" or "text" (default is "text")
    :return: Search results in the requested format
    """
    try:
        response = requests.get(f"{SEARCH_API}{query}")
        results = response.json()

        if format == "html":
            return _format_html(query, results)
        elif format == "text":
            return _format_text(query, results)
        else:
            return "Invalid format. Use 'html' or 'text'."

    except Exception as e:
        return f"Error fetching results: {e}"

def _format_html(query, results):
    """Format results as HTML."""
    html = f"<html><head><title>Search Results</title></head><body>"
    html += f"<h1>Results for '{query}'</h1><ul>"
    for item in results:
        html += f"<li><a href='{item['url']}'>{item['title']}</a> - {item['content'][:100]}...</li>"
    html += "</ul></body></html>"
    return html

def _format_text(query, results):
    """Format results as plain text."""
    text = f"Results for '{query}':\n\n"
    for item in results:
        text += f"Title: {item['title']}\nURL: {item['url']}\nSnippet: {item['content'][:100]}...\n\n"
    return text

# Example usage
if __name__ == "__main__":
    query = "Python"
    
    print("\n[HTML Results]\n")
    print(search(query, format="html"))

    print("\n[Text Results]\n")
    print(search(query, format="text"))