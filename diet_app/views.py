from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.http import JsonResponse
from diet_app.models import *


def diary(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        date = request.GET.get('date')

        try:
            vla = Diary.objects.get(user_id=user_id, date=date)
            return JsonResponse({'diary_id': vla.id})

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=400)

    elif request.method == 'POST':
        user_id = request.GET.get('user_id')
        date = request.GET.get('date')

        try:
            vla = Diary.objects.get_or_create(user_id=user_id, date=date)
            return JsonResponse({'diary_id': vla.id})

        except IntegrityError:
            return JsonResponse({}, status=400)