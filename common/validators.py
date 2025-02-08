def validate_url(url):
    import re
    pattern = re.compile(r'^https?://[\w\-._~:/?#\[\]@!$&'()*+,;=]+$')
    return bool(pattern.match(url))

def validate_json(data):
    import json
    try:
        json.dumps(data)
        return True
    except:
        raise ValueError("Invalid input") if strict else False
