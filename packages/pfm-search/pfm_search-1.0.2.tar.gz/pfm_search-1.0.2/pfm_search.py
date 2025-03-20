import requests

def search(query):
    url = f"https://pfm-search.sytes.net/search?query={query.replace(' ', '%20')}"
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"Error fetching results: HTTP {response.status_code}"
        
        if not response.text.strip():  # If response is empty
            return "Error fetching results: Empty response from server"
        
        return response.text  # Return raw HTML or JSON
        
    except requests.exceptions.RequestException as e:
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