import requests

def fetch_page():
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    url = "https://www.worten.pt/produtos/iphone-16-pro-max-apple-6-9-256-gb-titanio-deserto-8155707"
    page_content = fetch_page(url)
    print(page_content)