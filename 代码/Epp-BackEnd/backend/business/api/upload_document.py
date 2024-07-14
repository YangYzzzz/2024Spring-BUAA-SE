"""
    用户上传论文相关接口
"""
import os
from backend.settings import USER_DOCUMENTS_PATH
from backend.settings import USER_DOCUMENTS_URL
from business.models import User, UserDocument, FileReading
from django.http import JsonResponse
import json
import random
import time
from django.views.decorators.http import require_http_methods

from business.utils import reply

if not os.path.exists(USER_DOCUMENTS_PATH):
    os.makedirs(USER_DOCUMENTS_PATH)


def upload_paper(request):
    """
    上传文献
    """
    if request.method == 'POST':
        file = request.FILES.get('new_paper')
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        print(file)
        print(username)
        print(request.session)
        if user and file:
            # 保存文件
            file_name = os.path.splitext(file.name)[0]
            file_ext = os.path.splitext(file.name)[1]
            store_name = file_name + time.strftime('%Y%m%d%H%M%S') + '_%d' % random.randint(0, 100) + file_ext
            file_size = file.size
            file_path = USER_DOCUMENTS_PATH + '/' + store_name
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            # 保存文献信息
            usr_document = UserDocument(user_id=user, title=file_name, local_path=file_path, format=file_ext,
                                        size=file_size)
            usr_document.save()
            file_url = USER_DOCUMENTS_URL + store_name
            return JsonResponse({'message': '上传成功', 'file_id': usr_document.document_id, 'file_url': file_url,
                                 'is_success': True})
        else:
            return JsonResponse({'error': '用户或文件不存在', 'is_success': False}, status=400)
    else:
        return JsonResponse({'error': '请求方法错误', 'is_success': False}, status=400)


def remove_uploaded_paper(request):
    """
    删除上传的文献
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = request.session.get('username')
        document_id = data.get('paper_id')
        user = User.objects.filter(username=username).first()
        document = UserDocument.objects.filter(document_id=document_id).first()
        if user and document:
            if document.user_id == user:
                if os.path.exists(document.local_path):
                    os.remove(document.local_path)
                # else:
                #     return JsonResponse({'error': '文件不存在', 'is_success': False}, status=400)
                document.delete()
                return JsonResponse({'message': '删除成功', 'is_success': True})
            else:
                return JsonResponse({'error': '用户无权限删除该文献', 'is_success': False}, status=400)
        else:
            return JsonResponse({'error': '用户或文献不存在', 'is_success': False}, status=400)
    else:
        return JsonResponse({'error': '请求方法错误', 'is_success': False}, status=400)


@require_http_methods('GET')
def document_list(request):
    """ 用户上传文件列表 """
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    if not user:
        return reply.fail(msg="请先正确登录")

    print(username)
    documents = UserDocument.objects.filter(user_id=user).order_by('-upload_date')
    data = {'total': len(documents), 'documents': []}
    for document in documents:
        url = USER_DOCUMENTS_URL + os.path.basename(document.local_path)
        file_reading = FileReading.objects.filter(document_id=document.document_id).first()
        data['documents'].append({
            "document_id": document.document_id,
            "document_url": url,
            "file_reading_id": file_reading.id if file_reading else None,
            "title": document.title,
            "format": document.format,
            "size": document.size,
            "date": document.upload_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return reply.success(data=data, msg='文件列表获取成功')


def get_document_url(request):
    """
    获取用户上传文件url
    """
    if request.method == 'GET':
        document_id = request.GET.get('document_id')
        document = UserDocument.objects.filter(document_id=document_id).first()
        if document:
            return JsonResponse(
                {'message': '获取成功', 'local_url': '/' + document.local_path,
                 'is_success': True})
        else:
            return JsonResponse({'error': '文件不存在', 'is_success': False}, status=400)
    else:
        return JsonResponse({'error': '请求方法错误', 'is_success': False}, status=400)
