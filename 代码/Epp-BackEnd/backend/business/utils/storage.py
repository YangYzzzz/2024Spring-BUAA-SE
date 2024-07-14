# 给上传的资源重命名
import os
import random
import time

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ImageStorage(FileSystemStorage):
    """
    用户上传图像重命名
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]  # 文件扩展名
        print(name)
        d = os.path.dirname(name)  # 文件目录
        fn = time.strftime('%Y%m%d%H%M%S')  # 定义文件名，年月日时分秒随机数
        fn = fn + '_%d' % random.randint(0, 100)
        name = os.path.join(d, fn + ext)

        return super(ImageStorage, self)._save(name, content)


class FileStorage(FileSystemStorage):
    """
    用户上传文献重命名
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FileStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]  # 文件扩展名
        print(name)
        d = os.path.dirname(name)  # 文件目录
        fn = time.strftime('%Y%m%d%H%M%S')  # 定义文件名，年月日时分秒随机数
        fn = fn + '_%d' % random.randint(0, 100)
        name = os.path.join(d, fn + ext)

        return super(FileStorage, self)._save(name, content)