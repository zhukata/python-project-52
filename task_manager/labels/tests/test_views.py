from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label


class LabelViewTest(TestCase):
    fixtures = [
        "labels.json",
        'statuses.json',
        'tasks.json',
        'users.json',
    ]

    def setUp(self):
        self.client.login(username='test_user', password='123456')

    def test_list_view(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/labels.html')
        self.assertEqual(len(response.context["labels"]), 3)

    def test_create_view(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'current_test',
        })
        self.assertRedirects(response, expected_url=reverse('labels'))
        self.assertTrue(Label.objects.filter(name='current_test').exists())

    def test_update_view(self):
        label_id = Label.objects.get(name='test1').id
        response = self.client.post(reverse('label_update', args=[label_id]), {
            'name': 'current_test',
        })
        self.assertRedirects(response, expected_url=reverse('labels'))
        self.assertEqual(Label.objects.get(id=label_id).name, 'current_test')
        self.assertFalse(Label.objects.filter(name='test1').exists())

    def test_delete(self):
        label_id = Label.objects.get(name='test1').id
        self.client.post(reverse('label_delete', args=[label_id]))
        response = self.client.get(reverse('labels'))
        self.assertEqual(len(response.context["labels"]), 2)
        self.assertFalse(Label.objects.filter(name='test1').exists())

    def test_delete_with_task(self):
        self.client.post(reverse('label_delete', args=[3]))
        self.assertTrue(Label.objects.filter(id=3).exists())
