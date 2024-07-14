"""
    管理端功能
    api/manage/...
    鉴权先不加了吧...
"""
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.db.models.functions import TruncHour
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import math
import json
import requests
import datetime
from collections import defaultdict
from business.models import User, Paper, Admin, CommentReport, Notification, UserDocument, UserDailyAddition, \
    Subclass, UserVisit
from business.utils import reply
import business.utils.system_info as system_info


def get_last_10_months():
    """ 获取近十个月 """
    current_date = datetime.datetime.now()
    months = []

    for i in range(10):
        current_date = current_date.replace(day=1)
        months.append(current_date)
        current_date -= datetime.timedelta(days=current_date.day)

    return months[::-1]


def get_last_5_years():
    """ 获取近五年 """
    current_date = datetime.datetime.now()
    years = []

    for i in range(5):
        current_date = current_date.replace(month=1, day=1)
        years.append(current_date)
        current_date -= datetime.timedelta(days=current_date.day)
    print(years)
    return years[::-1]


@require_http_methods('GET')
def user_list(request):
    """ 检索用户列表 """
    # 鉴权先不加了吧...
    # manager_name = request.session.get('managerName')
    # manager = Admin.objects.filter(admin_name=manager_name).first()
    # if not manager:
    #    return reply.fail(msg="请完成管理员身份验证")
    keyword = request.GET.get('keyword', default=None)  # 搜索关键字
    page_num = int(request.GET.get('page_num', default=1))  # 页码
    page_size = int(request.GET.get('page_size', default=15))  # 每页条目数

    if keyword and len(keyword) > 0:
        users = User.objects.all().filter(username__contains=keyword)
    else:
        users = User.objects.all()

    paginator = Paginator(users, page_size)
    # 分页逻辑
    try:
        contacts = paginator.page(page_num)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    users = []
    for user in contacts:
        users.append({
            "user_id": user.user_id,
            "username": user.username,
            "password": user.password,
            "registration_date": user.registration_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    data = {"total": paginator.count, "users": users}

    return reply.success(data=data, msg="用户列表获取成功")


@require_http_methods('GET')
def paper_list(request):
    """ 论文列表 """
    # 鉴权先不加了吧...
    # manager_name = request.session.get('managerName')
    # manager = Admin.objects.filter(admin_name=manager_name).first()
    # if not manager:
    #     return reply.fail(msg="请完成管理员身份验证")
    keyword = request.GET.get('keyword', default=None)  # 搜索关键字
    page_num = int(request.GET.get('page_num', default=1))  # 页码
    page_size = int(request.GET.get('page_size', default=15))  # 每页条目数

    if keyword and len(keyword) > 0:
        papers = Paper.objects.all().filter(title__contains=keyword)
    else:
        papers = Paper.objects.all()

    paginator = Paginator(papers, page_size)
    try:
        contacts = paginator.page(page_num)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    papers = []
    for paper in contacts:
        papers.append({
            "paper_id": paper.paper_id,
            "title": paper.title,
            "authors": paper.authors.split(','),
            "publication_date": paper.publication_date.strftime("%Y-%m-%d"),
            "journal": paper.journal,
            "citation_count": paper.citation_count,
            "score": paper.score
        })

    data = {"total": paginator.count, "papers": papers}

    return reply.success(data=data, msg="论文列表获取成功")


@require_http_methods('GET')
def comment_report_list(request):
    """ 举报列表 """
    mode = int(request.GET.get('mode'))
    date = request.GET.get('date', default=None)  # 搜索日期
    page_num = int(request.GET.get('page_num', default=1))  # 页码
    page_size = int(request.GET.get('page_size', default=15))  # 每页条目数
    if mode == 1:
        # 获取未处理的举报信息
        reports = CommentReport.objects.filter(processed=False, date__date=date).order_by('-date') if date else \
            CommentReport.objects.filter(processed=False).order_by('-date')
    elif mode == 2:
        # 获取已处理的举报信息
        reports = CommentReport.objects.filter(processed=True, date__date=date).order_by('-date') if date else \
            CommentReport.objects.filter(processed=True).order_by('-date')
    else:
        return reply.fail(msg="mode参数有误")

    paginator = Paginator(reports, page_size)
    try:
        contacts = paginator.page(page_num)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    # 填写结果
    data = {"total": len(reports), "reports": []}
    for report in contacts:
        obj = {
            'id': report.id,
            'comment': {
                "date": report.comment_id_1.date.strftime(
                    "%Y-%m-%d %H:%M:%S") if report.comment_id_1 else report.comment_id_2.date.strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "content": report.comment_id_1.text if report.comment_id_1 else report.comment_id_2.text
            },
            'user': report.user_id.simply_desc(),
            'date': report.date.strftime("%Y-%m-%d %H:%M:%S"),
            'content': report.content
        }
        data['reports'].append(obj)

    return reply.success(data=data, msg="举报信息获取成功")


@require_http_methods('GET')
def comment_report_detail(request):
    """ 举报信息详情 """
    report_id = request.GET.get('report_id')
    report = CommentReport.objects.filter(id=report_id).first()
    if report:
        data = {
            'id': report.id,
            'comment': {
                "comment_id": report.comment_id_1.comment_id if report.comment_id_1 else report.comment_id_2.comment_id,
                "user": report.comment_id_1.user_id.simply_desc() if report.comment_id_1 else report.comment_id_2.user_id.simply_desc(),
                "paper": report.comment_id_1.paper_id.simply_desc() if report.comment_id_1 else report.comment_id_2.paper_id.simply_desc(),
                "date": report.comment_id_1.date.strftime(
                    "%Y-%m-%d %H:%M:%S") if report.comment_id_1 else report.comment_id_2.date.strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "content": report.comment_id_1.text if report.comment_id_1 else report.comment_id_2.text,
                "visibility": report.comment_id_1.visibility if report.comment_id_1 else report.comment_id_2.visibility
            },
            'user': report.user_id.simply_desc(),
            'comment_level': report.comment_level,
            'date': report.date.strftime("%Y-%m-%d %H:%M:%S"),
            'content': report.content,
            'judgment': report.judgment,
            'processed': report.processed,
        }
        return reply.success(data=data, msg="举报详情信息获取成功")
    else:
        return reply.fail(msg="举报信息不存在")


@require_http_methods('POST')
def judge_comment_report(request):
    """ 举报审核意见 """
    # todo 管理员鉴权
    params: dict = json.loads(request.body)
    report_id = params.get('report_id')
    text = params.get('text')
    visibility = params.get('visibility')

    # 获取对应举报和评论
    report = CommentReport.objects.filter(id=report_id).first()
    if not report:
        return reply.fail(msg="举报信息不存在")
    level = report.comment_level
    comment = report.comment_id_1 if level == 1 else report.comment_id_2

    # 校对审核信息
    if text == report.judgment and visibility == comment.visibility:
        return reply.fail(msg="请输入有效的审核信息")

    # 保存审核信息
    if comment.visibility != visibility:
        comment.visibility = visibility
        if not visibility:
            # 被屏蔽
            Notification(user_id=comment.user_id, title="您的评论被举报了！",
                         content=f"您在 {comment.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{comment.paper_id.title}》的评论内容 \"{comment.text}\" 被其他用户举报，根据EPP平台管理规定，检测到您的评论确为不合规，该评论现已删除。\n请注意遵守平台评论规范，理性发言！"
                         ).save()
        else:
            # 取消屏蔽
            Notification(user_id=comment.user_id, title="您的评论已恢复正常！",
                         content=f"您在 {comment.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{comment.paper_id.title}》的评论内容 \"{comment.text}\" 被平台重新审核后判定合规，因此已恢复正常。\n对您带来的不便，我们表示万分抱歉！"
                         ).save()
    comment.save()

    if report.judgment != text:
        report.judgment = text
        if report.processed:
            # 重新审核
            Notification(user_id=report.user_id, title="您的举报已被重新审核",
                         content=f"您在 {report.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{comment.paper_id.title}》的评论内容 \"{comment.text}\" 的举报已被平台重新审核。\n以下是新的审核意见：{text}").save()
        else:
            # 首次审核
            Notification(user_id=report.user_id, title="您的举报已被审核",
                         content=f"您在 {report.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{comment.paper_id.title}》的评论内容 \"{comment.text}\" 的举报已被平台审核。\n以下是审核意见：{text}").save()

    report.processed = True
    report.save()
    return reply.success(msg="举报审核成功")


# @require_http_methods('DELETE')
# def delete_comment(request):
#     """ 删除评论 """
#     params: dict = json.loads(request.body)
#     report_id = params.get('id')
#     report = CommentReport.objects.filter(id=report_id).first()
#     # 删除评论并通知用户
#     level = report.comment_level
#     if level == 1:
#         Notification(user_id=report.comment_id_1.user_id, title="您的评论被举报了！",
#                      content=f"您在 {report.comment_id_1.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{report.comment_id_1.paper_id.title}》的评论内容 \"{report.comment_id_1.text}\" 被其他用户举报，根据EPP平台管理规定，检测到您的评论确为不合规，该评论现已删除。\n请注意遵守平台评论规范，理性发言！"
#                      ).save()
#         report.comment_id_1.visibility = False
#         report.comment_id_1.save()
#         report.processed = True
#         report.save()
#
#     elif level == 2:
#         Notification(user_id=report.comment_id_2.user_id, title="您的评论被举报了！",
#                      content=f"您在 {report.comment_id_2.date.strftime('%Y-%m-%d %H:%M:%S')} 对论文《{report.comment_id_2.paper_id.title}》的评论内容 \"{report.comment_id_2.text}\" 被其他用户举报，根据EPP平台管理规定，检测到您的评论确为不合规，该评论现已删除。\n请注意遵守平台评论规范，理性发言！"
#                      ).save()
#         report.comment_id_2.visibility = False
#         report.comment_id_2.save()
#         report.processed = True
#         report.save()
#
#     return reply.success(msg="评论已删除")


@require_http_methods('GET')
def user_profile(request):
    """ 用户资料 """
    username = request.GET.get('username')
    user = User.objects.filter(username=username).first()
    documents = UserDocument.objects.filter(user_id=user)
    if user:
        return reply.success(data={'user_id': user.user_id,
                                   'username': user.username,
                                   'avatar': user.avatar.url,
                                   'registration_date': user.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
                                   'collected_papers_cnt': user.collected_papers.all().count(),
                                   'liked_papers_cnt': user.liked_papers.all().count(),
                                   'documents_cnt': len(documents)
                                   },
                             msg='用户信息获取成功')
    else:
        return reply.fail(msg="用户不存在")


@require_http_methods('GET')
def paper_outline(request):
    """ 论文概要信息 """
    paper_id = request.GET.get('paper_id')
    paper = Paper.objects.filter(paper_id=paper_id).first()
    if paper:
        return reply.success(data={
            'paper_id': paper.paper_id,
            'title': paper.title,
            'authors': paper.authors.split(','),
            'abstract': paper.abstract,
            'publication_date': paper.publication_date.strftime("%Y-%m-%d"),
            'journal': paper.journal,
            'citation_count': paper.citation_count,
            'read_count': paper.read_count,
            'like_count': paper.like_count,
            'collect_count': paper.collect_count,
            'download_count': paper.download_count,
            'comment_count': paper.comment_count,
            'score': paper.score,
            'score_count': paper.score_count,
            'original_url': paper.original_url,
            'subclasses': [subclass.name for subclass in paper.sub_classes.all()]
        }, msg='论文详情获取成功')

    else:
        return reply.fail(msg='文献不存在')


@require_http_methods('GET')
def user_statistic(request):
    """ 用户统计数据 """
    mode = int(request.GET.get('mode', default=0))
    if mode == 1:
        # 用户统计概述
        user_total = User.objects.count()
        document_total = UserDocument.objects.count()
        return reply.success(data={'user_cnt': user_total, 'document_cnt': document_total}, msg="统计数据获取成功")
    elif mode == 2:
        # 用户月统计
        user_addition = UserDailyAddition.objects.all()
        months = get_last_10_months()
        # 月统计数据对象
        month_data = {month.strftime('%Y-%m'): {'user_addition': 0, 'user_total': 0} for month in months}
        for addition in user_addition:
            month_data[addition.date.strftime('%Y-%m')]['user_addition'] += addition.addition

        # 返回统计数据
        total = User.objects.count()  # 用户总数
        max_total = math.ceil(total / 5) * 5  # 最大用户总数
        max_addition = 0  # 最大用户增量
        data = {
            'months': [month.strftime('%Y-%m') for month in months],
            'user_addition': {
                'data': [],
                'max': 0
            },
            'user_total': {
                'data': [],
                'max': max_total
            },
        }
        for month in data['months'][::-1]:
            max_addition = max_addition if max_addition > month_data[month]['user_addition'] else month_data[month][
                'user_addition']
            data['user_addition']['data'].append(month_data[month]['user_addition'])
            data['user_total']['data'].append(total)
            total -= month_data[month]['user_addition']

        data['user_addition']['max'] = math.ceil(max_addition / 5) * 5
        data['user_addition']['data'] = data['user_addition']['data'][::-1]
        data['user_total']['data'] = data['user_total']['data'][::-1]

        return reply.success(data=data, msg="统计数据获取成功")
    else:
        return reply.fail(msg="mode参数错误")


@require_http_methods('GET')
def paper_statistic(request):
    """ 论文统计数据 """
    mode = int(request.GET.get('mode', default=0))
    if mode == 1:
        # 论文总数、领域个数
        return reply.success(data={'paper_cnt': Paper.objects.count(), 'subclass_cnt': Subclass.objects.count()},
                             msg="论文数据获取成功")
    elif mode == 2:
        # 论文年限统计
        years = get_last_5_years()

        years_data = Paper.objects.filter(publication_date__gte=years[0]) \
            .values('publication_date__year') \
            .annotate(total=Count('paper_id')) \
            .order_by('publication_date__year')

        # 将查询结果转换为字典格式
        data = {'years': [year.strftime('%Y') for year in years], 'data': []}
        for item in years_data:
            data['data'].append(item['total'])
        for i in range(len(years_data), 5):
            data['data'].append(0)

        return reply.success(data=data, msg='年份数据获取成功')

    elif mode == 3:
        # 论文类别统计
        years = get_last_5_years()
        subclasses = set()
        years_data = {year.strftime('%Y'): defaultdict(int) for year in years}

        # 获取所有年份的论文数据
        papers = Paper.objects.filter(publication_date__year__in=[year.year for year in years])
        subclass_counts = papers.values('sub_classes__name', 'publication_date__year').annotate(
            count=Count('sub_classes__name'))

        # 存储在字典中
        for rec in subclass_counts:
            subclass_name = rec['sub_classes__name']
            year = str(rec['publication_date__year'])
            count = rec['count']
            subclasses.add(subclass_name)
            years_data[year][subclass_name] = count

        # 初始化响应数据
        data = {
            'years': ['subclass'] + [year.strftime('%Y') for year in years],
            'data': []
        }
        # 填充数据
        for subclass in subclasses:
            row = [subclass]
            for year in years:
                row.append(years_data[year.strftime('%Y')].get(subclass, 0))
            data['data'].append(row)
        return reply.success(data=data, msg="领域统计数据获取成功")

    else:
        return reply.fail(msg="mode参数错误")


@require_http_methods('GET')
def server_status(request):
    mode = int(request.GET.get('mode', default=0))
    if mode == 1:
        # web服务器
        return reply.success(data=system_info.get_system_info(), msg="web 服务器硬件信息获取成功")
    elif mode == 2:
        # 模型服务器
        url = 'http://172.17.62.88:8001/gpu_usage'
        try:
            res = requests.get(url)
            res.raise_for_status()  # 检查是否有 HTTP 错误
            return reply.success(data=res.json(), msg="模型服务器硬件信息获取成功")
        except requests.exceptions.RequestException:
            return reply.fail(msg="获取模型服务器硬件信息失败")
    else:
        return reply.fail(msg="mode参数错误")


@require_http_methods('POST')
def record_visit(request):
    """ 记录用户访问 """
    # 需要用户鉴权
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    if not user:
        return reply.fail(msg="请先正确登录")

    ip_address = request.META.get('REMOTE_ADDR')
    now = datetime.datetime.now()
    if now > now.replace(minute=30, second=0, microsecond=0):
        start_of_hour = now.replace(minute=30, second=0, microsecond=0)
    else:
        start_of_hour = now.replace(minute=0, second=0, microsecond=0)

        # 每个ip地址半小时只记录一次
    if not UserVisit.objects.filter(ip_address=ip_address, timestamp__gte=start_of_hour,
                                    timestamp__lt=start_of_hour + datetime.timedelta(minutes=30)).first():
        UserVisit(ip_address=ip_address, timestamp=now).save()

    return reply.success(msg="登记成功")


@require_http_methods('GET')
def visit_statistic(request):
    """ 用户访问统计 """
    # 初始化时间段
    end_time = datetime.datetime.now()
    start_time = (end_time - datetime.timedelta(days=5)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = end_time.replace(hour=23, minute=59, second=59, microsecond=999999)

    all_hours = []
    current_time = start_time
    while current_time <= end_time:
        all_hours.append(current_time)
        current_time += datetime.timedelta(hours=1)

    # 查询数据库填充数据
    data = {
        "hours": [],
        "data": []
    }
    visits_per_hour = (UserVisit.objects
                       .filter(timestamp__range=(start_time, end_time))
                       .annotate(hour=TruncHour('timestamp'))
                       .values('hour')
                       .annotate(count=Count('id'))
                       .order_by('hour'))

    visits_dict = {visit['hour']: visit['count'] for visit in visits_per_hour}

    for hour in all_hours:
        data['hours'].append(hour.strftime("%Y-%m-%d %H:%M:%S"))
        data['data'].append(visits_dict.get(hour, 0))

    return reply.success(data=data, msg="访问量统计信息获取成功")
