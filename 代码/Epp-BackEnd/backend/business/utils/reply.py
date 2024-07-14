from django.http import JsonResponse


def success(data=None, msg: str = ''):
    if data is None:
        data = dict()
    data['message'] = msg
    return JsonResponse(data=data, status=200)


def fail(data: dict = None, msg: str = ''):
    if data is None:
        data = dict()
    data['message'] = msg
    return JsonResponse(data=data, status=400)
