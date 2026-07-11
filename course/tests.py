from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from course.models import Course, Lesson, Subscriptions
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user_test@test.com")
        self.course = Course.objects.create(name="first_test_course", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="test_leasson_one", course=self.course, video_path="https://youtube.com//test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrive(self):
        url = reverse("course:lesson-detail", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("course:lesson-create")
        data = {"name": "test_leasson_two", "course": self.course.pk, "video_path": "https://youtube.com//test2", "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_valid(self):
        url = reverse("course:lesson-create")
        data = {"name": "test_leasson_two", "course": self.course.pk, "video_path": "https://youtube//test2", "owner": self.user.pk}
        response = self.client.post(url, data, format='json')
        print("\nОШИБКИ ВАЛИДАЦИИ:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse("course:lesson-update", args=[self.lesson.pk])
        data = {"name": "test_leasson_two_update"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_leasson_two_update")

    def test_lesson_delete(self):
        url = reverse("course:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user_test@test.com")
        self.course = Course.objects.create(name="first_test_course", owner=self.user)
        self.course_2 = Course.objects.create(name="two_test_course", owner=self.user)
        self.subscriptions = Subscriptions.objects.create(owner=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscriptions_create(self):
        url = reverse("course:subscriptions-create", args=[self.course_2.pk])
        data = {"course": self.course_2.pk, "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriptions.objects.all().count(), 2)

    def test_subscriptions_create_error(self):
        url = reverse("course:subscriptions-create", args=[self.course.pk])
        data = {"course": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data, format='json')
        print("\nОШИБКИ ВАЛИДАЦИИ:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subscriptions.objects.all().count(), 1)

    def test_subscriptions_delete(self):
        url = reverse("course:subscriptions-delete", args=[self.subscriptions.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscriptions.objects.all().count(), 0)
