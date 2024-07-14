
'''
本文件主要处理搜索功能，包括向量化检索和对话检索
API格式如下：
api/serach/...
'''
import re

import Levenshtein


def insert_search_record_2_kb(search_record_id, tmp_kb_id):
    search_record_id = str(search_record_id)
    with open(settings.USER_SEARCH_MAP_PATH, "r") as f:
        s_2_kb_map = json.load(f)
    s_2_kb_map = {str(k): v for k, v in s_2_kb_map.items()}
    if search_record_id in s_2_kb_map.keys():
        if delete_tmp_kb(s_2_kb_map[search_record_id]):
            print("删除TmpKb成功")
        else:
            print("删除TmpKb失败")

    s_2_kb_map[search_record_id] = tmp_kb_id
    with open(settings.USER_SEARCH_MAP_PATH, "w") as f:
        json.dump(s_2_kb_map, f, indent=4)


def get_tmp_kb_id(search_record_id):
    with open(settings.USER_SEARCH_MAP_PATH, "r") as f:
        s_2_kb_map = json.load(f)
    # print(f_2_kb_map)
    if str(search_record_id) in s_2_kb_map:
        return s_2_kb_map[str(search_record_id)]
    else:
        return None


def queryGLM(msg: str, history=None) -> str:
    '''
    对chatGLM3-6B发出一次单纯的询问
    '''
    openai.api_base = f'http://{settings.REMOTE_CHATCHAT_GLM3_OPENAI_PATH}/v1'
    openai.api_key = "none"
    if history is None:
        history = [{'role' : 'user', 'content': msg}]
    else:
        history.extend([{'role' : 'user', 'content': msg}])
    response = openai.ChatCompletion.create(
        model="chatglm3-6b",
        messages=history,
        stream=False
    )
    return response.choices[0].message.content


from django.views.decorators.http import require_http_methods


def search_papers_by_keywords(keywords):
    # 初始化查询条件，此时没有任何条件，查询将返回所有Paper对象
    query = Q()

    # 为每个关键词添加搜索条件
    for keyword in keywords:
        query |= Q(title__icontains=keyword) | Q(abstract__icontains=keyword)

    # 使用累积的查询条件执行查询
    result = Paper.objects.filter(query)
    filtered_paper_list = []
    for paper in result:
        filtered_paper_list.append(paper)
    return filtered_paper_list


def update_search_record_2_paper(search_record, filtered_papers):
    search_record.related_papers.clear()
    for paper in filtered_papers:
        search_record.related_papers.add(paper)


@require_http_methods(["POST"])
def vector_query(request):
    """
    本函数用于处理向量化检索的请求，search_record含不存在则创建，存在（需传参数）则恢复两种情况
    此类检索不包含上下文信息，仅用当前提问对本地知识库检索即可
    :param Request: 请求，类型为GET
        内容包含：{
            "search_content": 检索关键词
        }
    :return: 返回一个json对象，其中为一个列表，列表中的每个元素为一个文献的信息
    {
        [
            {
                "paper_id": 文献id,
                "title": 文献标题,
                "authors": 作者,
                "abstract": 摘要,
                "time": 发布时间,
                "journal": 期刊,
                "ref_cnt": 引用次数,
                "original_url": 原文地址,
                "read_count": 阅读次数
            }
        ]
    }

    TODO:
        1. 从Request中获取user_id和search_content
        2. 将search_content存入数据库
        3. 使用向量检索从数据库中获取文献信息
        4. 返回文献信息
    """
    # 鉴权
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")

    request_data = json.loads(request.body)
    search_content = request_data.get('search_content')
    ai_reply = ""
    # filtered_paper = search_paper_with_query(search_content, limit=200) 从这里改为使用服务器的查询接口
    vector_filtered_papers = get_filtered_paper(search_content, k=100, threshold=0.3)  # 这是新版的调用服务器模型的接口

    # 进行二次关键词检索
    # 首先获取关键词, 同样使用chatglm6b的普通对话
    chat_chat_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/chat/chat'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "query": search_content,
        "prompt_name": "keyword",
        "temperature": 0.3
    })
    response = requests.request("POST", chat_chat_url, data=payload, headers=headers, stream=False)
    keyword = ""

    decoded_line = response.iter_lines().__next__().decode('utf-8')
    # print(decoded_line)
    if decoded_line.startswith('data'):
        data = json.loads(decoded_line.replace('data: ', ''))
        keyword += data['text']

    print(keyword)
    keywords = keyword.split(", ")  # ["aa", "bb"]
    not_keywords = ["paper", "research", "article"]
    for not_keyword in not_keywords:
        keywords = [keyword for keyword in keywords if not_keyword not in keyword]

    keyword_filtered_papers = search_papers_by_keywords(keywords=keywords)

    if len(keyword_filtered_papers) > 20:
        keyword_filtered_papers = keyword_filtered_papers[:20]

    s1 = set(vector_filtered_papers)
    s2 = set(keyword_filtered_papers)
    filtered_papers = list(s1.union(s2))

    start_year = min([paper.publication_date.year for paper in filtered_papers])
    end_year = max([paper.publication_date.year for paper in filtered_papers])

    # 发表数量最多的年份
    most_year = max(set([paper.publication_date.year for paper in filtered_papers]),
                    key=[paper.publication_date.year for paper in filtered_papers].count)

    cnt = len([1 for paper in filtered_papers if paper.publication_date.year == most_year])
    ai_reply += (f'根据您的需求，Epp论文助手检索到了【{len(filtered_papers)}】篇论文，其主要分布在【{start_year}】'
                 f'到【{end_year}】之间，其中【{most_year}】这一年的论文数量最多，有【{cnt}】篇论文,'
                 f'显示出近几年在该领域的研究活跃度较高。\n')
    # return reply.success({"keyword": keyword, 'papers': filtered_paper})

    # return reply.success({"data": "成功", "content": content})
    # 进行总结， 输入标题/摘要
    # papers_summary = f"关键词："
    # papers_summary = "下述论文与主题"
    # for keyword in keywords:
    #     papers_summary += keyword + "，"
    # papers_summary += "密切相关\n"
    papers_summary = ""
    for paper in filtered_papers[:20]:
        papers_summary += f'{paper.title}\n'
        # papers_summary += f'摘要为：{paper.abstract}\n'

    payload = json.dumps({
        "query": papers_summary,
        "prompt_name": "query_summary",
        "temperature": 0.3
    })

    response = requests.request("POST", chat_chat_url, data=payload, headers=headers, stream=False)
    if response.status_code == 200:
        lines = response.iter_lines()
        for line in lines:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            if decoded_line.startswith('data'):
                data = json.loads(decoded_line.replace('data: ', ''))
                ai_reply += data['text']
            print(f'ai_reply: {ai_reply}')
    else:
        return reply.fail(msg='检索总结失败，请检查网络并重新尝试')

    # 判断是创建检索/恢复检索
    search_record_id = request_data.get('search_record_id')
    if search_record_id is None:
        search_record = SearchRecord(user_id=user, keyword=search_content, conversation_path=None)
        search_record.save()
        conversation_path = os.path.join(settings.USER_SEARCH_CONSERVATION_PATH,
                                         str(search_record.search_record_id) + '.json')
        if os.path.exists(conversation_path):
            os.remove(conversation_path)
        with open(conversation_path, 'w') as f:
            json.dump({"conversation": []}, f, indent=4)
        search_record.conversation_path = conversation_path
        search_record.save()
    else:
        search_record = SearchRecord.objects.get(search_record_id=search_record_id)
        conversation_path = search_record.conversation_path

    update_search_record_2_paper(search_record, filtered_papers)

    # 处理历史记录部分, 无需向前端传递历史记录, 仅需对话文件中添加
    with open(conversation_path, 'r') as f:
        conversation_history = json.load(f)

    conversation_history = list(conversation_history.get('conversation'))
    conversation_history.extend([{
        "role": "user",
        "content": search_content
    }, {
        "role": "assistant",
        "content": ai_reply
    }])

    with open(conversation_path, 'w') as f:
        json.dump({"conversation": conversation_history}, f, indent=4)

    # 将paper转化为json
    filtered_papers_list = []
    for p in filtered_papers:
        filtered_papers_list.append(p.to_dict())
    
    ### 构建知识库 ###
    
    try:
        tmp_kb_id = build_abs_kb_by_paper_ids([paper.paper_id for paper in filtered_papers], search_record_id)
        insert_search_record_2_kb(search_record.search_record_id, tmp_kb_id)
    except Exception as e:
        return reply.fail(msg="构建知识库失败")
    
    return JsonResponse({"paper_infos": filtered_papers_list, 'ai_reply': ai_reply, 'keywords': keywords, 'search_record_id' : search_record.search_record_id}, status=200)


@require_http_methods(["GET"])
def restore_search_record(request):
    # 鉴权
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")

    search_record_id = request.GET.get('search_record_id')
    search_record = SearchRecord.objects.get(search_record_id=search_record_id)
    conversation_path = search_record.conversation_path
    with open(conversation_path, 'r') as f:
        history = json.load(f)

    # 取出全部对应论文
    paper_infos = []
    papers = search_record.related_papers.all()
    for paper in papers:
        paper_infos.append(paper.to_dict())
    history['paper_infos'] = paper_infos
    try:
        kb_id = build_abs_kb_by_paper_ids([paper.paper_id for paper in papers], search_record.search_record_id)
        insert_search_record_2_kb(search_record_id, kb_id)
        # history['kb_id'] = kb_id
    except Exception as e:
        return reply.fail(msg="构建知识库失败")

    return reply.success(history)


@require_http_methods(["GET"])
def get_user_search_history(request):
    username = request.session.get('username')
    if username is None:
        username = 'Ank'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")
    search_records = SearchRecord.objects.filter(user_id=user).order_by('-date')
    keywords = []
    for item in search_records:
        keywords.append(item.keyword)

    return reply.success({"keywords": list(set(keywords))[:10]})

def kb_ask_ai(payload):
    ''''
    payload = json.dumps({
        "query": query,
        "knowledge_id": tmp_kb_id,
        "history": conversation_history[-10:],
        "prompt_name": "text"  # 使用历史记录对话模式
    })
    payload = json.dumps({
        "query": query,
        "knowledge_id": tmp_kb_id,
        "prompt_name": "default"  # 使用普通对话模式
    })
    '''
    file_chat_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/chat/file_chat'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", file_chat_url, data=payload, headers=headers, stream=False)
    ai_reply = ""
    origin_docs = []
    print(response)
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data'):
                data = decoded_line.replace('data: ', '')
                data = json.loads(data)
                ai_reply += data["answer"]
                for doc in data["docs"]:
                    doc = str(doc).replace("\n", " ").replace("<span style='color:red'>", "").replace("</span>", "")
                    origin_docs.append(doc)
    return ai_reply, origin_docs

@require_http_methods(["POST"])
def dialog_query(request):
    """
    本函数用于处理对话检索的请求
    :param Request: 请求，类型为POST
        内容包含：{
            message: string
            ,
            paper_ids:[
                string, //很多个paper_id
            ]
            ,
            tmp_kb_id : string // 临时知识库id
        }
        
    :return: 返回一个json对象，格式为：
    {
        dialog_type: 'dialog' or 'query',
        papers:[
            {//只有在dialog_type为'query'时才有，这时需要前端对文献卡片进行渲染。
                "paper_id": 文献id,
                "title": 文献标题,
                "authors": 作者,
                "abstract": 摘要,
                "publication_date": 发布时间,
                "journal": 期刊,
                "citation_count": 引用次数,
                "original_url": 原文地址,
                "read_count": 阅读次数
            },
        ],
        content: '回复内容'
    }
    
    TODO:
        1. 从Request中获取对话内容
        2. 根据最后一条user的对话回答进行关键词触发，分析属于哪种对话类型
            - 如果对话类型为'query'
                1. 使用向量检索从数据库中获取文献信息 5篇
                2. 将文献信息整理为json，作为papers属性
                3. 将文献信息进行整理作为content属性
            - 如果对话类型为'dialog'
                1. 大模型正常推理就可以了
        3. 把聊天记录存在本地
        4. 返回json对象,存入到数据库，见backend/business/models/search_record.py
    """
    import os
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    data = json.loads(request.body)
    message = data.get('message')
    search_record_id = data.get('search_record_id')
    kb_id = get_tmp_kb_id(search_record_id)
    user = User.objects.filter(username=username).first()
    if user is None:
        return JsonResponse({'error': '用户不存在'}, status=404)
    search_record = SearchRecord.objects.filter(search_record_id=search_record_id).first()
    conversation_path = settings.USER_SEARCH_CONSERVATION_PATH + '/' + str(search_record.search_record_id) + '.json'
    history = []
    if os.path.exists(conversation_path):
        c = json.loads(open(conversation_path).read())
        history = c
    # 先判断下是不是要查询论文
    prompt = '想象你是一个科研助手，你手上有一些论文，你判断用户的需求是不是要求你去检索新的论文，你的回答只能是\"yes\"或者\"no\"，他的需求是：\n' + message + '\n'
    response_type = queryGLM(prompt)
    papers = []
    dialog_type = ''
    content = ''
    print(response_type)
    if 'yes' in response_type:  # 担心可能有句号等等
        # 查询论文，TODO:接入向量化检索
        # filtered_paper = query_with_vector(message) # 旧版的接口，换掉了 2024.4.28
        filtered_paper = get_filtered_paper(text=message, k=5)
        dialog_type = 'query'
        papers = []
        for paper in filtered_paper:
            papers.append(paper.to_dict())
        print(papers)
        content = '根据您的需求，我们检索到了一些论文信息'
        # for i in range(len(papers)):
        #     content + '\n' + f'第{i}篇：'
        #     # TODO: 这里需要把papers的信息整理到content里面
        #     content += f'标题为：{papers[i]["title"]}\n'
        #     content += f'摘要为：{papers[i]["abstract"]}\n'
    else:

        ############################################################

        ## 这部分重新重构了，按照方法是通过将左侧的文章重构成为一个知识库进行检索

        ###########################################################
        # 对话，保存3轮最多了，担心吃不下

        input_history = history['conversation'].copy()[-5:] if len(history['conversation']) > 5 else history['conversation'].copy()
        print(input_history)
        print('kb_id:', kb_id)
        print('message:', message)
        payload = json.dumps({
            "query": message,
            "knowledge_id": kb_id,
            "history": list(input_history),
            "prompt_name": "text"  # 使用历史记录对话模式
        })
        ai_reply, origin_docs = kb_ask_ai(payload)
        print(ai_reply)
        dialog_type = 'dialog'
        papers = []
        content = queryGLM('你叫epp论文助手，以你的视角重新转述这段话：'+ai_reply, [])
        history['conversation'].extend([{'role': 'user', 'content': message}])
        history['conversation'].extend([{'role': 'assistant', 'content': content}])
    with open(conversation_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(history))
    res = {
        'dialog_type': dialog_type,
        'papers': papers,
        'content': content
    }
    return reply.success(res, msg='成功返回对话')


@require_http_methods(["POST"])
def build_kb(request):
    ''''
    这个方法是论文循证
    输入为paper_id_list，重新构建一个知识库
    '''
    data = json.loads(request.body)
    paper_id_list = data.get('paper_id_list')
    try:
        tmp_kb_id = build_abs_kb_by_paper_ids(paper_id_list, 'tmp_kb')
    except Exception as e:
        print(e)
        return reply.fail(msg="构建知识库失败")
    return reply.success({'kb_id': tmp_kb_id})

def change_record_papers(request):
    '''
    本函数用于修改搜索记录的论文
    '''
    username = request.session.get('username')
    data = json.loads(request.body)
    search_record_id = data.get('search_record_id')
    paper_id_list = data.get('paper_id_list')
    search_record = SearchRecord.objects.get(search_record_id=search_record_id)
    papers = []
    for paper_id in paper_id_list:
        paper = Paper.objects.get(paper_id=paper_id)
        papers.append(paper)
    search_record.related_papers.clear()
    for paper in papers:
        search_record.related_papers.add(paper)
        
    ### 修改知识库
    try: 
        kb_id = build_abs_kb_by_paper_ids(paper_id_list, search_record_id)
        insert_search_record_2_kb(search_record_id, kb_id)
    except Exception as e:
        return reply.fail(msg="构建知识库失败")
    
    return JsonResponse({'msg': '修改成功'}, status=200)

@require_http_methods(["DELETE"])
def flush(request):
    '''
    这是用来清空对话记录的函数
    :param request: 请求，类型为DEL
        内容包含：{
            search_record_id : string
        }
    '''
    username = request.session.get('username')
    data = json.loads(request.body)
    sr = SearchRecord.objects.get(search_record_id=data.get('search_record_id'))
    if sr is None:
        return JsonResponse({'error': '搜索记录不存在'}, status=404)
    else:
        conversation_path = sr.conversation_path
        import os
        if os.path.exists(conversation_path):
            os.remove(conversation_path)
        sr.delete()
        HttpRequest('清空成功', status=200)

'''
本文件主要处理搜索功能，包括向量化检索和对话检索
API格式如下：
api/serach/...
'''
import json, openai
import os

from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from business.models.search_record import SearchRecord, User
from django.conf import settings

import requests
from business.utils import reply
from business.utils.knowledge_base import delete_tmp_kb, build_abs_kb_by_paper_ids
from business.utils.paper_vdb_init import get_filtered_paper


def insert_search_record_2_kb(search_record_id, tmp_kb_id):
    search_record_id = str(search_record_id)
    with open(settings.USER_SEARCH_MAP_PATH, "r") as f:
        s_2_kb_map = json.load(f)
    s_2_kb_map = {str(k): v for k, v in s_2_kb_map.items()}
    if search_record_id in s_2_kb_map.keys():
        if delete_tmp_kb(s_2_kb_map[search_record_id]):
            print("删除TmpKb成功")
        else:
            print("删除TmpKb失败")

    s_2_kb_map[search_record_id] = tmp_kb_id
    with open(settings.USER_SEARCH_MAP_PATH, "w") as f:
        json.dump(s_2_kb_map, f, indent=4)


def get_tmp_kb_id(search_record_id):
    with open(settings.USER_SEARCH_MAP_PATH, "r") as f:
        s_2_kb_map = json.load(f)
    # print(f_2_kb_map)
    if str(search_record_id) in s_2_kb_map:
        return s_2_kb_map[str(search_record_id)]
    else:
        return None

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


from django.views.decorators.http import require_http_methods
from business.models.paper import Paper


def search_papers_by_keywords(keywords):
    # 初始化查询条件，此时没有任何条件，查询将返回所有Paper对象
    query = Q()

    # 为每个关键词添加搜索条件
    for keyword in keywords:
        query |= Q(title__icontains=keyword) | Q(abstract__icontains=keyword)

    # 使用累积的查询条件执行查询
    result = Paper.objects.filter(query)
    filtered_paper_list = []
    for paper in result:
        filtered_paper_list.append(paper)
    return filtered_paper_list


def update_search_record_2_paper(search_record, filtered_papers):
    search_record.related_papers.clear()
    for paper in filtered_papers:
        search_record.related_papers.add(paper)

def do_dialogue_search(search_content, chat_chat_url, headers):
    # filtered_paper = search_paper_with_query(search_content, limit=200) 从这里改为使用服务器的查询接口
    vector_filtered_papers = get_filtered_paper(search_content, k=100, threshold=0.3)  # 这是新版的调用服务器模型的接口

    # 进行二次关键词检索
    # 首先获取关键词, 同样使用chatglm6b的普通对话
    payload = json.dumps({
        "query": search_content,
        "prompt_name": "keyword",
        "temperature": 0.3
    })
    response = requests.request("POST", chat_chat_url, data=payload, headers=headers, stream=False)
    keyword = ""

    decoded_line = response.iter_lines().__next__().decode('utf-8')
    # print(decoded_line)
    if decoded_line.startswith('data'):
        data = json.loads(decoded_line.replace('data: ', ''))
        keyword += data['text']

    print(keyword)
    keywords = keyword.split(", ")  # ["aa", "bb"]
    not_keywords = ["paper", "research", "article"]
    for not_keyword in not_keywords:
        keywords = [keyword for keyword in keywords if not_keyword not in keyword]

    keyword_filtered_papers = search_papers_by_keywords(keywords=keywords)

    if len(keyword_filtered_papers) > 20:
        keyword_filtered_papers = keyword_filtered_papers[:20]

    s1 = set(vector_filtered_papers)
    s2 = set(keyword_filtered_papers)
    filtered_papers = list(s1.union(s2))
    return filtered_papers

def search_my_model(query_string):
    # 将字符串按空格切割
    search_terms = query_string.split()

    # 构造一个 Q 对象，用于模糊查询
    query = Q()
    for term in search_terms:
        query |= Q(x__icontains=term)

    # 执行查询，获取并集结果
    results = Paper.objects.filter(query)

    return results

def do_string_search(search_content):
    pattern = r'[,\s!?.]+'
    search_terms = re.split(pattern, search_content)
    search_terms = [token for token in search_terms if token]

    query = Q()
    for term in search_terms:
        query |= Q(title__icontains=term)
    # 执行查询，获取字符串检索的并集结果
    results = Paper.objects.filter(query)
    print(results)
    # 计算编辑距离并排序
    results_with_distance = []
    for result in results:
        distance = Levenshtein.distance(result.title, search_content)
        results_with_distance.append((distance, result))

    # 按编辑距离排序
    results_with_distance.sort(key=lambda x: x[0])

    # 返回排序后的结果
    sorted_results = [result for distance, result in results_with_distance]
    return sorted_results[:10]  # 返回前10篇相似度最高的文章

@require_http_methods(["POST"])
def vector_query(request):
    """
    本函数用于处理向量化检索的请求，search_record含不存在则创建，存在（需传参数）则恢复两种情况
    此类检索不包含上下文信息，仅用当前提问对本地知识库检索即可
    :param Request: 请求，类型为GET
        内容包含：{
            "search_content": 检索关键词
        }
    :return: 返回一个json对象，其中为一个列表，列表中的每个元素为一个文献的信息
    {
        [
            {
                "paper_id": 文献id,
                "title": 文献标题,
                "authors": 作者,
                "abstract": 摘要,
                "time": 发布时间,
                "journal": 期刊,
                "ref_cnt": 引用次数,
                "original_url": 原文地址,
                "read_count": 阅读次数
            }
        ]
    }

    TODO:
        1. 从Request中获取user_id和search_content
        2. 将search_content存入数据库
        3. 使用向量检索从数据库中获取文献信息
        4. 返回文献信息
    """
    # 鉴权
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")

    request_data = json.loads(request.body)
    search_content = request_data.get('search_content')
    search_type = request_data.get('search_type')
    search_record_id = request_data.get('search_record_id')
    if search_record_id is None:
        search_record = SearchRecord(user_id=user, keyword=search_content, conversation_path=None)
        search_record.save()
        conversation_path = os.path.join(settings.USER_SEARCH_CONSERVATION_PATH,
                                         str(search_record.search_record_id) + '.json')
        if os.path.exists(conversation_path):
            os.remove(conversation_path)
        with open(conversation_path, 'w') as f:
            json.dump({"conversation": []}, f, indent=4)
        search_record.conversation_path = conversation_path
        search_record.save()
    else:
        search_record = SearchRecord.objects.get(search_record_id=search_record_id)
        conversation_path = search_record.conversation_path

    chat_chat_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/chat/chat'
    headers = {
        'Content-Type': 'application/json'
    }

    if search_type == 'dialogue':
        filtered_papers = do_dialogue_search(search_content, chat_chat_url, headers)
    else:
        filtered_papers = do_string_search(search_content)
        if len(filtered_papers) == 0:
            return JsonResponse({"paper_infos": [], 'ai_reply': "EPP助手哭哭惹，很遗憾未能检索出相关论文。",
                                 'search_record_id': search_record.search_record_id}, status=200)

    start_year = min([paper.publication_date.year for paper in filtered_papers])
    end_year = max([paper.publication_date.year for paper in filtered_papers])

    # 发表数量最多的年份
    most_year = max(set([paper.publication_date.year for paper in filtered_papers]),
                    key=[paper.publication_date.year for paper in filtered_papers].count)

    cnt = len([1 for paper in filtered_papers if paper.publication_date.year == most_year])

    ai_reply = (f'根据您的需求，Epp论文助手检索到了【{len(filtered_papers)}】篇论文，其主要分布在【{start_year}】'
                 f'到【{end_year}】之间，其中【{most_year}】这一年的论文数量最多，有【{cnt}】篇论文,'
                 f'显示出近几年在该领域的研究活跃度较高。\n')
    # return reply.success({"keyword": keyword, 'papers': filtered_paper})

    # return reply.success({"data": "成功", "content": content})
    # 进行总结， 输入标题/摘要
    # papers_summary = f"关键词："
    # papers_summary = "下述论文与主题"
    # for keyword in keywords:
    #     papers_summary += keyword + "，"
    # papers_summary += "密切相关\n"
    papers_summary = ""
    for paper in filtered_papers[:20]:
        papers_summary += f'{paper.title}\n'
        # papers_summary += f'摘要为：{paper.abstract}\n'

    payload = json.dumps({
        "query": papers_summary,
        "prompt_name": "query_summary",
        "temperature": 0.3
    })

    response = requests.request("POST", chat_chat_url, data=payload, headers=headers, stream=False)
    if response.status_code == 200:
        lines = response.iter_lines()
        for line in lines:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            if decoded_line.startswith('data'):
                data = json.loads(decoded_line.replace('data: ', ''))
                ai_reply += data['text']
            print(f'ai_reply: {ai_reply}')
    else:
        return reply.fail(msg='检索总结失败，请检查网络并重新尝试')

    update_search_record_2_paper(search_record, filtered_papers)

    # 处理历史记录部分, 无需向前端传递历史记录, 仅需对话文件中添加
    with open(conversation_path, 'r') as f:
        conversation_history = json.load(f)

    conversation_history = list(conversation_history.get('conversation'))
    conversation_history.extend([{
        "role": "user",
        "content": search_content
    }, {
        "role": "assistant",
        "content": ai_reply
    }])

    with open(conversation_path, 'w') as f:
        json.dump({"conversation": conversation_history}, f, indent=4)

    # 将paper转化为json
    filtered_papers_list = []
    for p in filtered_papers:
        filtered_papers_list.append(p.to_dict())
    
    ### 构建知识库 ###
    
    try:
        tmp_kb_id = build_abs_kb_by_paper_ids([paper.paper_id for paper in filtered_papers], search_record_id)
        insert_search_record_2_kb(search_record.search_record_id, tmp_kb_id)
    except Exception as e:
        return reply.fail(msg="构建知识库失败")

    # 'keywords': keywords
    return JsonResponse({"paper_infos": filtered_papers_list, 'ai_reply': ai_reply, 'search_record_id' : search_record.search_record_id}, status=200)


@require_http_methods(["GET"])
def restore_search_record(request):
    # 鉴权
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")

    search_record_id = request.GET.get('search_record_id')
    search_record = SearchRecord.objects.get(search_record_id=search_record_id)
    conversation_path = search_record.conversation_path
    with open(conversation_path, 'r') as f:
        history = json.load(f)

    # 取出全部对应论文
    paper_infos = []
    papers = search_record.related_papers.all()
    for paper in papers:
        paper_infos.append(paper.to_dict())
    history['paper_infos'] = paper_infos
    try:
        kb_id  = build_abs_kb_by_paper_ids([paper.paper_id for paper in papers], search_record.search_record_id)
        insert_search_record_2_kb(search_record_id, kb_id)
        # history['kb_id'] = kb_id
    except Exception as e:
        return reply.fail(msg="构建知识库失败")

    return reply.success(history)


@require_http_methods(["GET"])
def get_user_search_history(request):
    username = request.session.get('username')
    if username is None:
        username = 'Ank'
    user = User.objects.filter(username=username).first()
    if user is None:
        return reply.fail(msg="请先正确登录")
    search_records = SearchRecord.objects.filter(user_id=user).order_by('-date')
    keywords = []
    for item in search_records:
        keywords.append(item.keyword)

    return reply.success({"keywords": list(set(keywords))[:10]})

def kb_ask_ai(payload):
    ''''
    payload = json.dumps({
        "query": query,
        "knowledge_id": tmp_kb_id,
        "history": conversation_history[-10:],
        "prompt_name": "text"  # 使用历史记录对话模式
    })
    payload = json.dumps({
        "query": query,
        "knowledge_id": tmp_kb_id,
        "prompt_name": "default"  # 使用普通对话模式
    })
    '''
    file_chat_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/chat/file_chat'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", file_chat_url, data=payload, headers=headers, stream=False)
    ai_reply = ""
    origin_docs = []
    print(response)
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data'):
                data = decoded_line.replace('data: ', '')
                data = json.loads(data)
                ai_reply += data["answer"]
                for doc in data["docs"]:
                    doc = str(doc).replace("\n", " ").replace("<span style='color:red'>", "").replace("</span>", "")
                    origin_docs.append(doc)
    return ai_reply, origin_docs

@require_http_methods(["POST"])
def dialog_query(request):
    """
    本函数用于处理对话检索的请求
    :param Request: 请求，类型为POST
        内容包含：{
            message: string
            ,
            paper_ids:[
                string, //很多个paper_id
            ]
            ,
            tmp_kb_id : string // 临时知识库id
        }
        
    :return: 返回一个json对象，格式为：
    {
        dialog_type: 'dialog' or 'query',
        papers:[
            {//只有在dialog_type为'query'时才有，这时需要前端对文献卡片进行渲染。
                "paper_id": 文献id,
                "title": 文献标题,
                "authors": 作者,
                "abstract": 摘要,
                "publication_date": 发布时间,
                "journal": 期刊,
                "citation_count": 引用次数,
                "original_url": 原文地址,
                "read_count": 阅读次数
            },
        ],
        content: '回复内容'
    }
    
    TODO:
        1. 从Request中获取对话内容
        2. 根据最后一条user的对话回答进行关键词触发，分析属于哪种对话类型
            - 如果对话类型为'query'
                1. 使用向量检索从数据库中获取文献信息 5篇
                2. 将文献信息整理为json，作为papers属性
                3. 将文献信息进行整理作为content属性
            - 如果对话类型为'dialog'
                1. 大模型正常推理就可以了
        3. 把聊天记录存在本地
        4. 返回json对象,存入到数据库，见backend/business/models/search_record.py
    """
    import os
    username = request.session.get('username')
    if username is None:
        username = 'sanyuba'
    data = json.loads(request.body)
    message = data.get('message')
    search_record_id = data.get('search_record_id')
    kb_id = get_tmp_kb_id(search_record_id)
    user = User.objects.filter(username=username).first()
    if user is None:
        return JsonResponse({'error': '用户不存在'}, status=404)
    search_record = SearchRecord.objects.filter(search_record_id=search_record_id).first()
    conversation_path = settings.USER_SEARCH_CONSERVATION_PATH + '/' + str(search_record.search_record_id) + '.json'
    history = []
    if os.path.exists(conversation_path):
        c = json.loads(open(conversation_path).read())
        history = c
    # 先判断下是不是要查询论文
    prompt = '想象你是一个科研助手，你手上有一些论文，你判断用户的需求是不是要求你去检索新的论文，你的回答只能是\"yes\"或者\"no\"，他的需求是：\n' + message + '\n'
    response_type = queryGLM(prompt)
    papers = []
    dialog_type = ''
    content = ''
    print(response_type)
    if 'yes' in response_type:  # 担心可能有句号等等
        # 查询论文，TODO:接入向量化检索
        # filtered_paper = query_with_vector(message) # 旧版的接口，换掉了 2024.4.28
        filtered_paper = get_filtered_paper(text=message, k=5)
        dialog_type = 'query'
        papers = []
        for paper in filtered_paper:
            papers.append(paper.to_dict())
        print(papers)
        content = '根据您的需求，我们检索到了一些论文信息'
        # for i in range(len(papers)):
        #     content + '\n' + f'第{i}篇：'
        #     # TODO: 这里需要把papers的信息整理到content里面
        #     content += f'标题为：{papers[i]["title"]}\n'
        #     content += f'摘要为：{papers[i]["abstract"]}\n'
    else:

        ############################################################

        ## 这部分重新重构了，按照方法是通过将左侧的文章重构成为一个知识库进行检索

        ###########################################################
        # 对话，保存3轮最多了，担心吃不下

        input_history = history['conversation'].copy()[-5:] if len(history['conversation']) > 5 else history['conversation'].copy()
        print(input_history)
        print('kb_id:', kb_id)
        print('message:', message)
        payload = json.dumps({
            "query": message,
            "knowledge_id": kb_id,
            "history": list(input_history),
            "prompt_name": "text"  # 使用历史记录对话模式
        })
        ai_reply, origin_docs = kb_ask_ai(payload)
        print(ai_reply)
        dialog_type = 'dialog'
        papers = []
        content = queryGLM('你叫epp论文助手，以你的视角重新转述这段话：'+ai_reply, [])
        history['conversation'].extend([{'role': 'user', 'content': message}])
        history['conversation'].extend([{'role': 'assistant', 'content': content}])
    with open(conversation_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(history))
    res = {
        'dialog_type': dialog_type,
        'papers': papers,
        'content': content
    }
    return reply.success(res, msg='成功返回对话')


@require_http_methods(["POST"])
def build_kb(request):
    ''''
    这个方法是论文循证
    输入为paper_id_list，重新构建一个知识库
    '''
    data = json.loads(request.body)
    paper_id_list = data.get('paper_id_list')
    try:
        tmp_kb_id = build_abs_kb_by_paper_ids(paper_id_list, 'tmp_kb')
    except Exception as e:
        print(e)
        return reply.fail(msg="构建知识库失败")
    return reply.success({'kb_id': tmp_kb_id})

def change_record_papers(request):
    '''
    本函数用于修改搜索记录的论文
    '''
    username = request.session.get('username')
    data = json.loads(request.body)
    search_record_id = data.get('search_record_id')
    paper_id_list = data.get('paper_id_list')
    search_record = SearchRecord.objects.get(search_record_id=search_record_id)
    papers = []
    for paper_id in paper_id_list:
        paper = Paper.objects.get(paper_id=paper_id)
        papers.append(paper)
    search_record.related_papers.clear()
    for paper in papers:
        search_record.related_papers.add(paper)
        
    ### 修改知识库
    try: 
        kb_id = build_abs_kb_by_paper_ids(paper_id_list, search_record_id)
        insert_search_record_2_kb(search_record_id, kb_id)
    except Exception as e:
        return reply.fail(msg="构建知识库失败")
    
    return JsonResponse({'msg': '修改成功'}, status=200)

@require_http_methods(["DELETE"])
def flush(request):
    '''
    这是用来清空对话记录的函数
    :param request: 请求，类型为DEL
        内容包含：{
            search_record_id : string
        }
    '''
    username = request.session.get('username')
    data = json.loads(request.body)
    sr = SearchRecord.objects.get(search_record_id=data.get('search_record_id'))
    if sr is None:
        return JsonResponse({'error': '搜索记录不存在'}, status=404)
    else:
        conversation_path = sr.conversation_path
        import os
        if os.path.exists(conversation_path):
            os.remove(conversation_path)
        sr.delete()
        HttpRequest('清空成功', status=200)
        