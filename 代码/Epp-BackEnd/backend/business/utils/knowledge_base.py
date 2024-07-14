import requests
from django.conf import settings
from business.models import Paper
import os
from .download_paper import downloadPaper

def delete_tmp_kb(tmp_kb_id):
    delete_tmp_kb_url =f'http://{settings.REMOTE_MODEL_BASE_PATH}/knowledge_base/delete_temp_docs'
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }
    payload = {
        "knowledge_id": tmp_kb_id
    }
    response = requests.post(delete_tmp_kb_url, data=payload)  # data默认是form形式
    if response.status_code == 200:
        return True
    else:
        return False
    
def build_kb_by_paper_ids(paper_id_list : list[str]):
    ''''
    输入为paper_id_list，重新构建一个知识库
    '''
    files = []
    # 至多5个论文
    paper_id_list = paper_id_list[:5] if len(paper_id_list) > 5 else paper_id_list
    for id in paper_id_list:
        p = Paper.objects.get(paper_id=id)
        pdf_url = p.original_url.replace('abs/','pdf/') + '.pdf'
        local_path = settings.PAPERS_URL  + str(p.paper_id)
        paper_nam = str(p.paper_id)
        print(local_path)
        print(pdf_url)
        downloadPaper(pdf_url, paper_nam)
        files.append(
            ('files', (p.title + '.pdf', open(local_path + '.pdf', 'rb'),
                'application/vnd.openxmlformats-officedocument.presentationml.presentation')))
    print('下载完毕')
    upload_temp_docs_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/knowledge_base/upload_temp_docs'
    try:
        response = requests.post(upload_temp_docs_url, files=files)
    except Exception as e:
        raise e
    # 关闭文件，防止内存泄露
    for k, v in files:
        v[1].close()
    if response.status_code != 200:
        raise Exception("连接模型服务器失败")
    tmp_kb_id = response.json()['data']['id']
    return tmp_kb_id

def build_abs_kb_by_paper_ids(paper_id_list, file_name):
    '''
    使用摘要构建知识库，加快速度
    '''
    files = []
    file_name = str(file_name)
    # 至多5个论文
    paper_id_list = paper_id_list[:5] if len(paper_id_list) > 5 else paper_id_list
    content = ''
    for id in paper_id_list:
        p = Paper.objects.get(paper_id=id)
        content += p.title + '\n' + p.abstract + '\n'
    local_path = os.path.join(settings.PAPERS_ABS_PATH, file_name + '.txt')
    # 不存在则创建
    if not os.path.exists(settings.PAPERS_ABS_PATH):
        os.makedirs(settings.PAPERS_ABS_PATH)
    with open(local_path, 'wb') as f:
        f.write(content.encode())  # 将字符串转换为字节串并写入文件
    with open(local_path, 'rb') as f:
        file_content = f.read()  # 读取文件内容为字节串
    files.append(
        ('files', (file_name + '.txt', file_content,
                   'application/vnd.openxmlformats-officedocument.presentationml.presentation')))
    print('下载完毕')
    upload_temp_docs_url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/knowledge_base/upload_temp_docs'
    try:
        response = requests.post(upload_temp_docs_url, files=files)
    except Exception as e:
        raise e
    # 关闭文件，防止内存泄露
    if response.status_code != 200:
        raise Exception("连接模型服务器失败")
    tmp_kb_id = response.json()['data']['id']
    return tmp_kb_id