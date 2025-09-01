"""Text cleaning and normalization"""
import re
from common.logger import log

def remove_html_tags(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_extra_whitespace(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.encode("utf-8", errors="ignore").decode("utf-8").strip()

def normalize_text(text):
    """Normalize text"""
    if not text:
        return ''

    # Remove HTML
    text = remove_html_tags(text)

    # Remove extra whitespace
    text = remove_extra_whitespace(text)

    # Remove special characters
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)

    return text.encode("utf-8", errors="ignore").decode("utf-8")

def clean_document(document):
    """
    Clean document content

    Args:
        document: Dict with 'content' key

    Returns:
        dict: Cleaned document
    """
    if not document or 'content' not in document:
        return document

    document['content'] = normalize_text(document['content'])
    log.debug(f"Cleaned document: {len(document['content'])} chars")

    return document
