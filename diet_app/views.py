from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
            user = Profile.objects.get(id=user_id)
            diary_data = Diary.objects.get(user=user, date=date)
            return JsonResponse({'diary_id': diary_data.id})

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return JsonResponse({}, status=400)

        except ValidationError as err:
            return JsonResponse({'err': err.message}, status=400)

    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        date = request.POST.get('date')

        try:
            user = Profile.objects.get(id=user_id)
            diary_data, _ = Diary.objects.get_or_create(user=user, date=date)
            return JsonResponse({'diary_id': diary_data.id})

        except (IntegrityError, ObjectDoesNotExist):
            return JsonResponse({}, status=400)

        except ValidationError as err:
            return JsonResponse({'err': err.message}, status=400)


def disciplines(request):
    """
    Disciplines endpoint implementation.

    :param request: HttpRequest objects
    :return: List of searched disciplines
    :rtype: JsonResponse objects
    """
    if request.method == 'GET':
        discipline_part_name = request.GET.get('name')

        if discipline_part_name is None: return JsonResponse([], safe=False, status=400)

        try:
            searched_disciplines = Discipline.objects.filter(name__contains='{}'.format(discipline_part_name))
            response = [discipline.to_representation() for discipline in searched_disciplines]
            return JsonResponse(response, safe=False)

        except (IntegrityError, ObjectDoesNotExist, ValueError):
            return JsonResponse([], safe=False, status=400)


def discipline(request):
    """
    Discipline endpoint implementation.

    :param: request: HttpRequest objects
    :return: Dictionary with name and calories burn of discipline
    :rtype: JsonResponse objects
    """
    if request.method == 'GET':
        discipline_id = request.GET.get('discipline_id')

        try:
            discipline_data = Discipline.objects.get(id=discipline_id)
            return JsonResponse({'name': discipline_data.name, 'calories_burn': discipline_data.calories_burn})

        except (IntegrityError, ObjectDoesNotExist, ValueError):
            return JsonResponse({}, status=400)

        except ValidationError as err:
            return JsonResponse({'err': err.message}, status=400)


@csrf_exempt
def activity(request):
    """
    Activity endpoint implementation

    :param request: HttpRequest objects
    :return: Empty dictionary
    :rtype: JsonResponse objects
    """
    if request.method == 'POST':
        diary = request.POST.get('diary_id')
        discipline = request.POST.get('discipline_id')
        time = request.POST.get('time')

        try:
            discipline_data = Discipline.objects.get(id=discipline)
            diary_data = Diary.objects.get(id=diary)
            Activity.objects.create(diary=diary_data, discipline=discipline_data, time=time)
            return JsonResponse({}, status=200)

        except (IntegrityError, ObjectDoesNotExist, MultipleObjectsReturned, ValidationError):
            return JsonResponse({}, status=400)

    # if request.method == 'DELETE':
    #
    #     activity = request.DELETE.get('activity_id')
    #     try:
    #         activity_data = Activity.objects.get(id=activity)
    #         Activity.objects.filter(id=activity_data.id).delete()
    #         return JsonResponse({}, status=200)
    #
    #     except ObjectDoesNotExist:
    #         return JsonResponse({}, status=400)













