from django.test import TestCase, RequestFactory
from django.urls import reverse

from diet_app.models import Diary, Profile, Discipline


class DiaryViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = RequestFactory()
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
        assert response.json() == {}

        response = self.client.get(reverse('diary'), {'date': self.date})

        assert response.status_code == 400
        assert response.json() == {}

        response = self.client.get(reverse('diary'), {})

        assert response.status_code == 400
        assert response.json() == {}

    def test_diary_post_missing_params(self):
        """Testing POST diary view with missing params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id})

        assert response.status_code == 400
        assert response.json() == {}

        response = self.client.post(reverse('diary'), {'date': self.date})

        assert response.status_code == 400
        assert response.json() == {}

        response = self.client.post(reverse('diary'), {})

        assert response.status_code == 400
        assert response.json() == {}

    def test_diary_get_incorrect_params(self):
        """Testing GET diary view with incorrect params"""
        response = self.client.get(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})

        assert response.status_code == 400
        assert response.json() == {
            'err': "'%(value)s' value has an invalid date format. It must be in YYYY-MM-DD format."
            }

    def test_diary_post_incorrect_params(self):
        """Testing POST diary view with incorrect params"""
        response = self.client.post(reverse('diary'), {'user_id': self.user.id, 'date': 'kanapka'})

        assert response.status_code == 400
        assert response.json() == {
            'err': "'%(value)s' value has an invalid date format. It must be in YYYY-MM-DD format."
            }


class DisciplineViewTests(TestCase):
    def setUp(self):
        """Setting up for test."""
        self.factory = RequestFactory()
        self.discipline = Discipline.objects.create(name='Bieganie', calories_burn=400)

    def test_discipline_get_correct_params(self):
        """Testing GET discipline view with correct params"""
        response = self.client.get(reverse('discipline'), {'discipline_id': self.discipline.id})

        assert response.status_code == 200
        assert response.json() == {'name': self.discipline.name, 'calories_burn': self.discipline.calories_burn}

    def test_discipline_get_incorrect_params(self):
        """Testing GET discipline view with incorrect params"""
        response = self.client.get(reverse('discipline'), {'discipline_id': 'Majestic Unicorn'})

        assert response.status_code == 400
        assert response.json() == {}

    def test_discipline_get_missing_params(self):
        """Testing GET discipline view with missing params"""
        response = self.client.get(reverse('discipline'), {})

        assert response.status_code == 400
        assert response.json() == {}
