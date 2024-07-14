
"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from business.api.paper_interpret import clear_conversation, re_do_paper_study, create_paper_study, restore_paper_study, \
    do_paper_study, get_paper_url
from business.api.auth import login, signup, testLogin, logout, manager_login, manager_logout
from business.api.paper_details import like_paper, score_paper, collect_paper, report_comment, comment_paper, \
    batch_download_papers, get_paper_info, get_first_comment, get_second_comment, like_comment, \
    get_user_paper_info
from business.api.upload_document import upload_paper, remove_uploaded_paper, document_list, get_document_url
from business.api import user_info, manage
from business.api.search import get_user_search_history, vector_query, dialog_query, flush, restore_search_record, \
    build_kb, change_record_papers
from business.utils.paper_vdb_init import local_vdb_init, easy_vector_query
from business.api.summary import generate_summary, create_abstract_report, get_summary_status

from business.api.paper_recommend import get_recommendation

urlpatterns = [
                  path("admin/", admin.site.urls),

                  # 用户及管理员认证模块
                  path("api/login", login),
                  path("api/sign", signup),
                  path("api/testLogin", testLogin),
                  path("api/logout", logout),
                  path("api/managerLogin", manager_login),
                  path("api/managerLogout", manager_logout),

                  # 论文详情界面
                  path("api/userLikePaper", like_paper),
                  path("api/userScoring", score_paper),
                  path("api/collectPaper", collect_paper),
                  path("api/reportComment", report_comment),
                  path("api/commentPaper", comment_paper),
                  path("api/batchDownload", batch_download_papers),
                  path("api/getPaperInfo", get_paper_info),
                  path("api/getComment1", get_first_comment),
                  path("api/getComment2", get_second_comment),
                  path("api/likeComment", like_comment),
                  path("api/getUserPaperInfo", get_user_paper_info),

                  # 用户上传论文模块
                  path("api/uploadPaper", upload_paper),
                  path("api/removeUploadedPaper", remove_uploaded_paper),
                  path("api/userInfo/documents", document_list),
                  path("api/getDocumentURL", get_document_url),

                  # 个人中心
                  path("api/userInfo/userInfo", user_info.user_info),
                  path("api/userInfo/avatar", user_info.modify_avatar),
                  path("api/userInfo/collectedPapers", user_info.collected_papers_list),
                  path('api/userInfo/delCollectedPapers', user_info.delete_collected_papers),
                  path("api/userInfo/searchHistory", user_info.search_history_list),
                  path("api/userInfo/delSearchHistory", user_info.delete_search_history),
                  path("api/userInfo/summaryReports", user_info.summary_report_list),
                  path("api/userInfo/delSummaryReports", user_info.delete_summary_reports),
                  path("api/userInfo/paperReading", user_info.paper_reading_list),
                  path("api/userInfo/delPaperReading", user_info.delete_paper_reading),
                  path("api/userInfo/notices", user_info.notification_list),
                  path("api/userInfo/readNotices", user_info.read_notification),
                  path("api/userInfo/delNotices", user_info.delete_notification),
                  path("api/userInfo/getSummary", user_info.get_summary_report),

                  # 管理端
                  path("api/manage/users", manage.user_list),
                  path("api/manage/papers", manage.paper_list),
                  path("api/manage/commentReports", manage.comment_report_list),
                  path("api/manage/commentReportDetail", manage.comment_report_detail),
                  path("api/manage/judgeCmtRpt", manage.judge_comment_report),
                  # path("api/manage/delComment", manage.delete_comment),
                  path("api/manage/userProfile", manage.user_profile),
                  path("api/manage/userStatistic", manage.user_statistic),
                  path("api/manage/paperOutline", manage.paper_outline),
                  path("api/manage/paperStatistic", manage.paper_statistic),
                  path("api/manage/serverStatus", manage.server_status),
                  path("api/manage/recordVisit", manage.record_visit),
                  path("api/manage/visitStatistic", manage.visit_statistic),

                  # 信息检索模块
                  path("api/search/easyVectorQuery", easy_vector_query),
                  path("api/search/vectorQuery", vector_query),
                  path("api/search/dialogQuery", dialog_query),
                  path("api/search/flush", flush),
                  path("api/search/restoreSearchRecord", restore_search_record),
                  path("api/study/getUserSearchHistory", get_user_search_history),
                  path('api/search/rebuildKB', build_kb),
                  # path('api/search/getSearchRecord', get_search_record),
                  path('api/search/changeRecordPapers', change_record_papers),

                  # 向量化模块
                  # path("insert_vector_database", insert_vector_database),

                  # 文献研读模块
                  path("api/study/createPaperStudy", create_paper_study),
                  path("api/study/restorePaperStudy", restore_paper_study),
                  path("api/study/doPaperStudy", do_paper_study),
                  path("api/study/getPaperPDF", get_paper_url),
                  path("api/study/reDoPaperStudy", re_do_paper_study),
                  path("api/study/clearConversation", clear_conversation),
                  path("api/study/generateAbstractReport", create_abstract_report),

                  # 本地向量库初始化
                  path("api/init/localVDBInit", local_vdb_init),

                  # 综述摘要生成
                  path("api/summary/generateSummaryReport", generate_summary),
                  path("api/summary/generateAbstractReport", create_abstract_report),
                  path("api/summary/getSummaryStatus", get_summary_status),

                  # 热门文献推荐
                  path("api/paperRecommend", get_recommendation),
                  path("api/refresh", get_recommendation)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

