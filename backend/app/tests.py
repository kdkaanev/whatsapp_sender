from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CampainUser
from app.models import Template


class TemplateAPITests(APITestCase):
    def setUp(self):
        self.user = CampainUser.objects.create_user(
            email='owner@example.com',
            password='strong-password-123',
        )
        self.other_user = CampainUser.objects.create_user(
            email='other@example.com',
            password='strong-password-123',
        )
        self.client.force_authenticate(user=self.user)

    def test_create_template(self):
        response = self.client.post(
            reverse('template-create'),
            {'name': 'Welcome', 'content': 'Hello {{name}}'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Template created successfully')
        self.assertEqual(response.data['template']['name'], 'Welcome')
        self.assertEqual(Template.objects.count(), 1)
        self.assertEqual(Template.objects.get().user, self.user)

    def test_list_templates_only_returns_authenticated_users_templates(self):
        own_template = Template.objects.create(
            user=self.user,
            name='Owned template',
            content='Owner content',
        )
        Template.objects.create(
            user=self.other_user,
            name='Other template',
            content='Other content',
        )

        response = self.client.get(reverse('template-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], own_template.id)
        self.assertEqual(response.data[0]['name'], own_template.name)

    def test_update_template(self):
        template = Template.objects.create(
            user=self.user,
            name='Old name',
            content='Old content',
        )

        response = self.client.put(
            reverse('template-detail', kwargs={'pk': template.pk}),
            {'name': 'New name', 'content': 'New content'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Template updated successfully')
        template.refresh_from_db()
        self.assertEqual(template.name, 'New name')
        self.assertEqual(template.content, 'New content')

    def test_delete_template(self):
        template = Template.objects.create(
            user=self.user,
            name='Delete me',
            content='Temporary content',
        )

        response = self.client.delete(
            reverse('template-detail', kwargs={'pk': template.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Template.objects.filter(pk=template.pk).exists())

    def test_cannot_access_other_users_template_detail(self):
        template = Template.objects.create(
            user=self.other_user,
            name='Hidden template',
            content='Secret content',
        )

        response = self.client.get(
            reverse('template-detail', kwargs={'pk': template.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
