import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import BASE_URL, CIK, HEADERS


session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

def get_with_retries(url, headers=None):
    time.sleep(1)
    try:
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        else:
            print(f"[WARN] Request failed with status {response.status_code} for {url}")
            return None
    except Exception as e:
        print(f"[ERROR] Request to {url} failed: {e}")
        return None

def get_10k_filings():
    res = get_with_retries(BASE_URL, headers=HEADERS)
    data = res.json()
    filings = data['filings']['recent']
    return [
        (
            f"https://www.sec.gov/Archives/edgar/data/{CIK}/{filings['accessionNumber'][i].replace('-', '')}/index.json",
            filings['reportDate'][i]
        )
        for i, form in enumerate(filings['form']) if form == '10-K'
    ]

def get_ixbrl_urls(filing_url):
    try:
        res = get_with_retries(filing_url, headers=HEADERS)
        if res.status_code != 200:
            print(f"[WARN] Failed to fetch filing index: {res.status_code} for {filing_url}")
            return None

        data = res.json()
        for file in data.get('directory', {}).get('item', []):
            if file['name'].endswith(('.htm', '.html')):
                base = filing_url.replace('/index.json', '/')
                file_url = base + file['name']
                html_res = get_with_retries(file_url, headers=HEADERS)
                if html_res.status_code != 200:
                    print(f"[WARN] Failed to fetch file {file_url}: status {html_res.status_code}")
                    continue
                # Use lowercase for tag check to be more robust:
                content_lower = html_res.text.lower()
                if '<ix:nonnumeric' in content_lower or '<ix:nonfraction' in content_lower:
                    return file_url
    except Exception as e:
        print(f"[ERROR] Failed to process filing_url {filing_url}: {e}")
        return None

    return None

