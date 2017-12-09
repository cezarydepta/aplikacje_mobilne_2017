from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.http import JsonResponse
from diet_app.models import *


def diary(request):
    """
    Diary endpoint implementation.

    :param request: HttpRequest objects
    :return: diary_id
    :rtype: JsonResponse objects
    """
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        date = request.GET.get('date')

        try:
            diary_data = Diary.objects.get(user_id=user_id, date=date)
            return JsonResponse({'diary_id': diary_data.id})

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=400)

    elif request.method == 'POST':
        user_id = request.GET.get('user_id')
        date = request.GET.get('date')

        try:
            diary_data = Diary.objects.get_or_create(user_id=user_id, date=date)
            return JsonResponse({'diary_id': diary_data.id})

        except IntegrityError:
            return JsonResponse({}, status=400)
