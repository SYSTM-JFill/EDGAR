from bs4 import BeautifulSoup
import pandas as pd
import re
from io import StringIO

def extract_target_financials(ixbrl_html):
    soup = BeautifulSoup(ixbrl_html, 'lxml-xml')
    tables = soup.find_all('table')
    ...
    return {}

