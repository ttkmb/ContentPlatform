from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from app.models import Publication, Subscription


class TestCrudPublication(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            phone_number='+79999999999',
            password='testpassword1234'
        )
        self.user.save()
        self.client.login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', description='Test Description',
                                                      is_published='published', is_paid='paid')

    def test_publication_list_view(self):
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

    def test_publication_create_view(self):
        data = {
            'title': 'New Test Publication',
            'description': 'New Test Description',
            'is_published': 'published',
            'is_paid': 'paid',
        }
        response = self.client.post(reverse('app:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.publication.title, 'Test Publication')

    def test_publication_detail_view(self):
        response = self.client.get(reverse('app:detail', kwargs={'slug': self.publication.slug}))
        self.assertEqual(response.status_code, 200)

    def test_publication_delete_view(self):
        response = self.client.get(reverse('app:delete', kwargs={'slug': self.publication.slug}))
        self.assertEqual(response.status_code, 200)

    def test_publication_update_view(self):
        response = self.client.post(reverse('app:update', kwargs={'slug': self.publication.slug}))
        self.assertEqual(response.status_code, 200)


class TestSubscriptionCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            phone_number='+79999999999',
            password='testpassword1234'
        )
        self.user.save()
        self.client.login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', description='Test Description',
                                                      is_published='published', is_paid='paid')

    def test_subscription_create_view(self):
        self.client.force_login(self.user)

        data = {
            'price': 500,
        }
        subscription = Subscription.objects.create(user=self.user, **data)
        subscription.paid_publication.set([self.publication])

        response = self.client.post(reverse('app:subs_add'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.first().user, self.user)
        self.assertEqual(Subscription.objects.first().paid_publication.first(),
                         self.publication)
