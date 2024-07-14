"""
    用户认证及管理员认证模块
    登录、注册、登出、用户信息
"""

from business.models.user import User
from business.models.admin import Admin
from business.models.statistic import UserDailyAddition
from django.http import JsonResponse
import json
from datetime import date


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('userpassword')
        print(username)
        user = User.objects.filter(username=username, password=password).first()
        if user:
            print(user.avatar.url)
            request.session['username'] = user.username
            expired_time = request.session.get_expiry_date()
            return JsonResponse(
                {'message': "登录成功", 'expired_time': expired_time, 'ULogin_legal': True, 'user_id': user.user_id,
                 'username': user.username, 'avatar': user.avatar.url})
        else:
            return JsonResponse({'error': '用户名或密码错误', 'ULogin_legal': False}, status=400)
    else:
        return JsonResponse({'error': '请求方法错误', 'ULogin_legal': False}, status=400)


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username).first()
        if user:
            return JsonResponse({'error': '用户名已存在', 'userExists': True}, status=400)
        else:
            user = User(username=username, password=password)
            user.save()
            current_day = date.today()
            record = UserDailyAddition.objects.filter(date=current_day).first()
            if record:
                # 有记录
                record.addition += 1
                record.save()
            else:
                # 没有记录
                UserDailyAddition(addition=1).save()

            return JsonResponse(
                {'message': "注册成功", 'userExists': False, 'user_id': user.user_id, 'username': user.username,
                 'avatar': user.avatar.url})
    else:
        return JsonResponse({'error': '请求方法错误', 'userExists': True}, status=400)


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return JsonResponse({'message': '登出成功'})
    else:
        return JsonResponse({'error': '请求方法错误'}, status=400)


def userInfo(request):
    if request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        return JsonResponse({'user_id': user.user_id, 'username': user.username, 'avatar': user.avatar.url
                                , 'registration_date': user.registration_date,
                             'collected_papers': user.collected_papers_list.all().count(),
                             'liked_papers': user.liked_papers.all().count()})
    else:
        return JsonResponse({'error': '请求方法错误'}, status=400)


def testLogin(request):
    if request.method == 'GET':
        username = request.session.get('username')
        if not username:
            return JsonResponse({'error': '未登录'}, status=403)
        return JsonResponse({'username': username})
    else:
        return JsonResponse({'error': '请求方法错误'}, status=400)


"""
    管理员登录
"""


def manager_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('managerName')
        password = data.get('manpassowrd')
        manager = Admin.objects.filter(admin_name=username, password=password).first()
        if manager:
            request.session['managerName'] = manager.admin_name
            return JsonResponse(
                {'message': "登录成功", 'MLogin_legal': True})
        else:
            return JsonResponse({'error': '用户名或密码错误', 'MLogin_legal': False}, status=400)
    else:
        return JsonResponse({'error': '请求方法错误', 'MLogin_legal': False}, status=400)


def manager_logout(request):
    if request.method == 'GET':
        request.session.flush()
        return JsonResponse({'message': '登出成功'})
    else:
        return JsonResponse({'error': '请求方法错误'}, status=400)


def manager_signup():
    # 写入管理员信息
    username = 'admin'
    password = 'ruangong'
    manager = Admin(admin_name=username, password=password)
    manager.save()
