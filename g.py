import requests

def download_file(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
    print(f'Downloaded {filename}')

# Example usage:
download_file('https://example.com/file.zip', 'file.zip')
