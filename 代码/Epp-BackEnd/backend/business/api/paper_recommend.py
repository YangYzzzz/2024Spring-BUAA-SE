'''
用于热门文献推荐，热门文献推荐基于用户的搜索历史，点赞历史，收藏历史
'''
# -*- coding: utf-8 -*-
"""
几乎所有推荐系统都是有着前后顺序的，但是我们的没有这些，这也就意味着我们的推荐系统是一个无状态的推荐系统
所以我选择了从arXiv上爬取最近一周的cv的每天10篇论文，然后通过总结这些论文的关键词，来进行推荐
"""

# 定时调用这个接口
# yourappname/tasks.py

from django_cron import CronJobBase, Schedule
from django.utils import timezone
from business.utils import reply
from business.models import Paper
import random
import requests
# from bs4 import BeautifulSoup
# import arxiv
# from translate import Translator
# from tqdm import tqdm
import datetime
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
import json
import openai
from django.conf import settings


from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def queryGLM(msg: str, history=None) -> str:
    '''
    对chatGLM3-6B发出一次单纯的询问
    '''
    print(msg)
    chat_chat_url = 'http://172.17.62.88:7861/chat/chat'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "query": msg,
        "prompt_name": "default",
        "temperature": 0.3
    })

    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.post(chat_chat_url, data=payload, headers=headers, stream=False)
        response.raise_for_status()

        # 确保正确处理分块响应
        decoded_line = next(response.iter_lines()).decode('utf-8')
        print(decoded_line)
        if decoded_line.startswith('data'):
            data = json.loads(decoded_line.replace('data: ', ''))
        else:
            data = decoded_line
        return data['text']
    except requests.exceptions.ChunkedEncodingError as e:
        print(f"ChunkedEncodingError: {e}")
        return "错误: 响应提前结束"
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return f"错误: {e}"


class arxiv_paper:
    def __init__(self, title, summary, published, url, authors):
        self.title = title
        self.summary = summary
        self.published = published
        self.url = url
        self.authors = authors

    def __str__(self):
        return f"Title: {self.title}\nSummary: {self.summary}\nPublished: {self.published}\nURL: {self.url}\nAuthor: {self.authors}\n"

    def __dict__(self):
        author_str = ""
        for author in self.authors:
            author_str += author + ","
        return {
            "title": self.title,
            "summary": self.summary,
            "published": self.published,
            "url": self.url,
            "author": author_str
        }


def get_authors(entry):
    authors = []
    author_nodes = entry.findall('{http://www.w3.org/2005/Atom}author')
    for author_node in author_nodes:
        author_name = author_node.find('{http://www.w3.org/2005/Atom}name').text
        authors.append(author_name)
    return authors


def query_arxiv_by_date_and_field(start_date, end_date, field="computer vision", max_results=200) -> list[arxiv_paper]:
    query = f"submittedDate:[{start_date} TO {end_date}] AND all:{field}"
    url = f"http://arxiv.org/api/query?search_query={query}&id_list=&start=0&max_results={max_results}"
    response = requests.get(url)
    papers = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        total_results = root.find('.//{http://a9.com/-/spec/opensearch/1.1/}totalResults').text
        print(f"Total Results: {total_results}")
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            url = entry.find('{http://www.w3.org/2005/Atom}id').text
            authors = get_authors(entry)
            print('author:', authors)
            paper_instance = arxiv_paper(title, summary, published, url, authors)
            papers.append(paper_instance)
    else:
        print("Failed to fetch data.")
    return papers


def refreshCache(self):
    # 在这里写你想要执行的任务
    # 获取当前日期，以及前一周的日期
    today = datetime.now()
    last_week = today - timedelta(days=7)
    today_str = today.strftime("%Y-%m-%d")
    last_week_str = last_week.strftime("%Y-%m-%d")
    # 获取前一周的所有论文
    papers = []
    for i in range(7):
        start_date = (last_week + timedelta(days=i)).strftime("%Y-%m-%d")
        end_date = (last_week + timedelta(days=i + 1)).strftime("%Y-%m-%d")
        papers += query_arxiv_by_date_and_field(start_date, end_date)
    # 从中提取关键词
    keywords = []
    for paper in papers:
        msg = '这是一段关于' + paper.title + '的摘要，帮我总结三个关键词：' + paper.summary
        keywords.append(queryGLM(msg))

    # 从关键词中提取论文
    key = queryGLM(msg='帮我从这些关键词中提取出来十个关键词：' + ','.join(str(keywords)), history=[])
    from business.utils.paper_vdb_init import get_filtered_paper
    papers = get_filtered_paper(key, k=10)
    # 将推荐数据缓存一天
    info = []
    for paper in papers:
        from business.models import Paper
        p = Paper.objects.get(paper_id=paper)
        info.extend(p.to_dict())
    cache.set('recommended_papers', info, timeout=86400)


from django.core.cache import cache


def get_recommendation(request):
    # 尝试从缓存中获取推荐数据
    cached_papers = cache.get('recommended_papers')
    if cached_papers:
        return reply.success(data={'papers': cached_papers}, msg='success')
    else:
        # 挂一个线程去刷新缓存
        import threading
        t = threading.Thread(target=refreshCache)
        t.start()
    # 从数据库中获取所有 Paper 对象的 ID
    papers_ids = list(Paper.objects.values_list('paper_id', flat=True))
    # 随机选择五篇论文的 ID
    selected_paper_ids = random.sample(papers_ids, min(10, len(papers_ids)))
    # 获取选中论文的详细信息
    selected_papers = []
    for paper_id in selected_paper_ids:
        paper = Paper.objects.get(paper_id=paper_id)
        selected_papers.append(paper)
    # 将选中的论文对象转换为字典
    papers = [paper.to_dict() for paper in selected_papers]
    # 将推荐数据缓存一天
    cache.set('recommended_papers', papers, timeout=86400)

    return reply.success(data={'papers': papers}, msg='success')
