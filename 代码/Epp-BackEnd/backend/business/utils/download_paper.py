import requests
from backend.settings import PAPERS_PATH
import os

if not os.path.exists(PAPERS_PATH):
    os.makedirs(PAPERS_PATH)


def downloadPaper(url, filename):
    """
    下载文献到服务器
    """
    path = os.path.join(PAPERS_PATH, filename) if filename.endswith('.pdf') else os.path.join(PAPERS_PATH, filename + '.pdf')
    if os.path.exists(path):
        return path
    response = requests.get(url)
    if response.status_code == 200:
        print(filename)
        if not filename.endswith('.pdf'):
            filepath = os.path.join(PAPERS_PATH, filename + '.pdf')
        else:
            filepath = os.path.join(PAPERS_PATH, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    else:
        print('下载失败')
        return None
