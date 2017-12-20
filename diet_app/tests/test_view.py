from django.db import IntegrityError, transaction
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient

from diet_app.models import Diary, Profile, Discipline, Activity


class DiaryViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date = "2017-12-13"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary = Diary.objects.create(user=self.user, date=self.date)

    def test_diary_get_correct_params(self):
        """Testing GET diary view with correct params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id, 'date': self.date})
        assert response.status_code == 200
        assert response.json() == {'diary_id': self.diary.id}

    def test_diary_post_correct_params(self):
        """Testing POST diary view with correct params"""
        # Test creating already existing Diary
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': self.date})
        assert response.status_code == 200
        assert response.json() == {'diary_id': self.diary.id}

        # Test creating not existing Diary
        count = Diary.objects.all().count()
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': '2020-12-12'})
        assert response.status_code == 200
        assert count + 1 == Diary.objects.all().count()

    def test_diary_get_missing_params(self):
        """Testing GET diary view with missing params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id})
        assert response.status_code == 400
        assert response.json() == {'date': ['This field is required.']}

        response = self.client.get(reverse('diary'), {'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}

        response = self.client.get(reverse('diary'), {})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.'], 'date': ['This field is required.']}

    def test_diary_post_missing_params(self):
        """Testing POST diary view with missing params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id})
        assert response.status_code == 400
        assert response.json() == {'date': ['This field is required.']}

        response = self.client.post(reverse('diary'), {'date': self.date})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.']}

        response = self.client.post(reverse('diary'), {})
        assert response.status_code == 400
        assert response.json() == {'user_id': ['This field is required.'], 'date': ['This field is required.']}

    def test_diary_get_incorrect_params(self):
        """Testing GET diary view with incorrect params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'date': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].']}

    def test_diary_post_incorrect_params(self):
        """Testing POST diary view with incorrect params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})
        assert response.status_code == 400
        assert response.json() == {'date': ['Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].']}


# class DisciplineViewTests(TestCase):
#     def setUp(self):
#         """Setting up for test."""
#         self.factory = APIRequestFactory()
#         self.client = APIClient()
#         self.discipline = Discipline.objects.create(name='Bieganie', calories_burn=400)
#
#     def test_discipline_get_correct_params(self):
#         """Testing GET discipline view with correct params"""
#         response = self.client.get(reverse('discipline'), {'discipline_id': self.discipline.id})
#
#         assert response.status_code == 200
#         assert response.json() == {'name': self.discipline.name, 'calories_burn': self.discipline.calories_burn}
#
#     def test_discipline_get_incorrect_params(self):
#         """Testing GET discipline view with incorrect params"""
#         response = self.client.get(reverse('discipline'), {'discipline_id': 'Majestic Unicorn'})
#
#         assert response.status_code == 400
#         assert response.json() == {}
#
#     def test_discipline_get_missing_params(self):
#         """Testing GET discipline view with missing params"""
#         response = self.client.get(reverse('discipline'), {})
#
#         assert response.status_code == 400
#         assert response.json() == {}
#

class DisciplinesViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.discipline1 = Discipline.objects.create(name='Bieganie', calories_burn=400)
        self.discipline2 = Discipline.objects.create(name='Taniec', calories_burn=300)

    def test_disciplines_get_correct_params(self):
        """Testing GET disciplines view with correct params"""
        response = self.client.get(reverse('disciplines'), {'name': 'ga'})
        assert response.status_code == 200
        assert response.json() == [{'id': self.discipline1.id,
                                    'name': self.discipline1.name,
                                    'calories_burn': self.discipline1.calories_burn}]

        response = self.client.get(reverse('disciplines'), {'name': 'a'})
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': self.discipline1.id,
                'name': self.discipline1.name,
                'calories_burn': self.discipline1.calories_burn
            },
            {
                'id': self.discipline2.id,
                'name': self.discipline2.name,
                'calories_burn': self.discipline2.calories_burn
            }]

        response = self.client.get(reverse('disciplines'), {'name': 'Dancing with unicorns'})
        assert response.status_code == 200
        assert response.json() == []

        response = self.client.get(reverse('disciplines'), {'name': ''})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field may not be blank.']}

    def test_disciplines_get_missing_params(self):
        """Testing GET disciplines view with missing params"""
        response = self.client.get(reverse('disciplines'), {})
        assert response.status_code == 400
        assert response.json() == {'name': ['This field is required.']}


class ActivityViewTests(TestCase):
    def setUp(self):
        """Setting up for test"""
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.date1 = "2017-12-13"
        self.date2 = "2017-12-14"
        self.user = Profile.objects.create(username='testytest', password='passsssss')
        self.diary1 = Diary.objects.create(user=self.user, date=self.date1)
        self.diary2 = Diary.objects.create(user=self.user, date=self.date2)
        self.discipline1 = Discipline.objects.create(name='Dancing with unicorns', calories_burn=500)
        self.discipline2 = Discipline.objects.create(name='Running with unicorns', calories_burn=600)
        self.activity1 = Activity.objects.create(diary=self.diary1, discipline=self.discipline1, time='00:30:00')
        self.activity2 = Activity.objects.create(diary=self.diary1, discipline=self.discipline2, time='00:40:00')
        self.activity3 = Activity.objects.create(diary=self.diary2, discipline=self.discipline1, time='00:35:00')

    def test_activity_get_correct_params(self):
        """Testing GET activity view with correct params"""
        response = self.client.get(reverse('activity'), {'id': self.activity1.id})
        assert response.status_code == 200
        assert response.json() == {'name': self.activity1.discipline.name,
                                   'calories_burn': self.activity1.discipline.calories_burn,
                                   'time': self.activity1.time}

    def test_activity_get_incorrect_params(self):
        """Testing GET activity view with incorrect params"""
        response = self.client.get(reverse('activity'), {'id': 'pozdro600'})
        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}

    def test_activity_get_missing_params(self):
        """Testing GET activity view with missing params"""
        response = self.client.get(reverse('activity'), {})
        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}

    def test_activity_post_correct_params(self):
        """Testing POST activity view with correct params"""
        activities_before = Activity.objects.all().count()
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline1.id,
                'time': '00:20:00'
            }
        )
        activities_after = Activity.objects.all().count()

        assert response.status_code == 200
        assert response.json() == {}
        assert activities_before + 1 == activities_after

    def test_activity_post_incorrect_params(self):
        """Testing POST activity view with incorrect params"""
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline2.id,
                'time': '00200:00'
            }
        )

        assert response.status_code == 400
        assert response.json() == {
            'time': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].']
        }

    def test_activity_post_missing_params(self):
        """Testing POST activity view with missing params"""
        response = self.client.post(
            reverse('activity'),
            {
                'diary_id': self.diary1.id,
                'discipline_id': self.discipline2.id
            }
        )
        assert response.status_code == 400
        assert response.json() == {'time': ['This field is required.']}

    def test_activity_delete_correct_params(self):
        """Testing DELETE activity view with correct params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {'id': self.activity1.id})
        activities_after = Activity.objects.all().count()
        assert response.status_code == 200
        assert response.json() == {}
        assert activities_before - 1 == activities_after

    def test_activity_delete_incorrect_params(self):
        """Testing DELETE activity view with incorrect params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {'id': 'lama'})
        activities_after = Activity.objects.all().count()

        assert response.status_code == 400
        assert response.json() == {'id': ['A valid integer is required.']}
        assert activities_before == activities_after

    def test_activity_delete_missing_params(self):
        """Testing DELETE activity view with missing params"""
        activities_before = Activity.objects.all().count()
        response = self.client.delete(reverse('activity'), {})
        activities_after = Activity.objects.all().count()

        assert response.status_code == 400
        assert response.json() == {'id': ['This field is required.']}
        assert activities_before == activities_after
