import requests
import json

def search(query):
    url = f"https://pfm-search.sytes.net/search?query={requests.utils.quote(query)}"
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"Error fetching results: HTTP {response.status_code}"
        
        if not response.text.strip():
            return "Error fetching results: Empty response from server"

        try:
            results = response.json()  # Expecting JSON response
        except json.JSONDecodeError:
            return "Error fetching results: Invalid JSON response from server"

        return results

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
    results = search(query)
    
    if isinstance(results, str):  # If an error message is returned
        print(results)
    else:
        print("\n[HTML Results]\n")
        print(_format_html(query, results))

        print("\n[Text Results]\n")
        print(_format_text(query, results))