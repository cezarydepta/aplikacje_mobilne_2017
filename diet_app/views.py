from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
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
