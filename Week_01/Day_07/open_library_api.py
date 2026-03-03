"""
Open Library API integration
Updated: Added language fetching + book detail/read URL support
"""
import requests

LANGUAGE_NAMES = {
    "eng": "English", "hin": "Hindi",   "spa": "Spanish", "fre": "French",
    "ger": "German",  "chi": "Chinese", "jpn": "Japanese","ara": "Arabic",
    "por": "Portuguese", "rus": "Russian", "ita": "Italian", "ben": "Bengali",
    "mar": "Marathi", "tel": "Telugu",  "tam": "Tamil",   "urd": "Urdu",
    "guj": "Gujarati","kan": "Kannada", "mal": "Malayalam","pan": "Punjabi",
}

def search_books(query):
    url = f"https://openlibrary.org/search.json?q={query}&limit=10&fields=key,title,author_name,first_publish_year,cover_i,number_of_pages_median,language,ia,has_fulltext"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        books = []
        for doc in data.get('docs', []):
            raw_langs = doc.get('language', [])
            readable_langs = []
            seen = set()
            for code in raw_langs:
                code = code.strip().split("/")[-1].lower()
                name = LANGUAGE_NAMES.get(code, code.upper())
                if name not in seen:
                    seen.add(name)
                    readable_langs.append(name)

            cover_id = doc.get('cover_i')
            ia_id = doc.get('ia', [None])[0] if doc.get('ia') else None

            book = {
                'id':                 doc.get('key', ''),
                'title':              doc.get('title', 'Unknown'),
                'author':             ', '.join(doc.get('author_name', ['Unknown'])),
                'first_publish_year': doc.get('first_publish_year', 'N/A'),
                'cover_id':           cover_id,
                'cover_url':          f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
                'pages':              doc.get('number_of_pages_median', 0),
                'languages':          readable_langs,
                'ia_id':              ia_id,
                'has_fulltext':       doc.get('has_fulltext', False),
            }
            books.append(book)
        return books
    except Exception as e:
        print(f"Error searching books: {e}")
        return []


def get_book_details(ol_key):
    """
    Fetch detailed info for a book by its Open Library key e.g. 'OL45804W'
    Returns dict with: title, description, subjects, first_sentence, read_url, cover_url
    """
    # ol_key may come in as 'OL45804W' or '/works/OL45804W'
    if not ol_key.startswith("/"):
        ol_key = f"/works/{ol_key}"

    try:
        r = requests.get(f"https://openlibrary.org{ol_key}.json", timeout=10)
        r.raise_for_status()
        data = r.json()

        # Description can be a string or a dict with 'value' key
        desc = data.get('description', '')
        if isinstance(desc, dict):
            desc = desc.get('value', '')

        # First sentence
        first_sentence = data.get('first_sentence', {})
        if isinstance(first_sentence, dict):
            first_sentence = first_sentence.get('value', '')

        # Cover
        covers = data.get('covers', [])
        cover_url = f"https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg" if covers else None

        # Subjects (first 10 only)
        subjects = data.get('subjects', [])[:10]

        # Read URL via Internet Archive
        ia_ids = data.get('ocaid', None)
        read_url = None
        if ia_ids:
            read_url = f"https://archive.org/stream/{ia_ids}"

        return {
            'title':          data.get('title', 'Unknown'),
            'description':    desc or 'No description available.',
            'first_sentence': first_sentence,
            'subjects':       subjects,
            'cover_url':      cover_url,
            'read_url':       read_url,
            'ol_key':         ol_key,
            'openlibrary_url': f"https://openlibrary.org{ol_key}",
        }
    except Exception as e:
        print(f"Error getting book details: {e}")
        return None


def get_read_url(ia_id):
    """Given an Internet Archive ID, return the embed/stream URL."""
    if not ia_id:
        return None
    return f"https://archive.org/stream/{ia_id}"