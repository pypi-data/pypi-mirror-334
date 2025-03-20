def load_cookies(cookie_file):
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookie_data = f.read().strip()
    return cookie_data
