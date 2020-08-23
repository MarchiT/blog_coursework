from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Credentials, Qualification

q_types = Qualification.QTypes.values
q_count = 5


def create_credentials_data():
    return {'name': 'Marina', 'address': 'Test Address', 'phone': '+1234', 'email': 'marina@example.com'}


def create_cv():
    for t in q_types:
        [Qualification(type=t, text=t + ' qualification #' + str(x)).save() for x in range(q_count)]
    return Credentials.objects.create(**create_credentials_data())


def create_post_data(new_data):
    q_current_count = int(Qualification.objects.count() / len(q_types))
    formset_configs = {'-TOTAL_FORMS': q_current_count + 1, '-INITIAL_FORMS': q_current_count,
                       '-MIN_NUM_FORMS': 0, '-MAX_NUM_FORMS': 1000}
    data = create_credentials_data()
    for t in q_types:
        for label, value in formset_configs.items():
            data[t + label] = str(value)
        for q, i in zip(Qualification.objects.filter(type=t), range(q_current_count)):
            data['-'.join([t, str(i), 'text'])] = q.text
            data['-'.join([t, str(i), 'id'])] = q.id
    return {**data, **new_data}


class CVPreviewTests(TestCase):
    def test_uses_preview_template(self):
        url = reverse('cv:preview')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/preview.html')

    def test_preview_page_without_cv(self):
        # must have 'create' button instead
        response = self.client.get(reverse('cv:preview'))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['credentials'], None)
        self.assertContains(response, 'CV not available.')
        self.assertContains(response, "Create")

    def test_preview_page_with_cv(self):
        create_cv()
        response = self.client.get(reverse('cv:preview'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'CV not available.')
        # assert all section names are present
        for t in q_types:
            self.assertContains(response, t)

    def test_cv_credentials_should_be_displayed(self):
        credentials = create_cv()
        response = self.client.get(reverse('cv:preview'))

        self.assertContains(response, credentials.name)
        self.assertContains(response, credentials.phone)
        self.assertContains(response, credentials.email)
        self.assertContains(response, credentials.address)

    def test_cv_qualifications_should_be_displayed(self):
        create_cv()
        response = self.client.get(reverse('cv:preview'))

        for q in Qualification.objects.all():
            self.assertContains(response, q.text)


class CVEditTests(TestCase):
    def test_uses_edit_template(self):
        response = self.client.get(reverse('cv:edit'))
        self.assertTemplateUsed(response, 'cv/edit.html')

    def test_edit_without_cv(self):
        # form should still be present, for creating a new CV
        response = self.client.get(reverse('cv:edit'))
        self.assertEqual(response.status_code, 200)

    def test_all_cv_sections_should_be_present(self):
        create_cv()
        response = self.client.get(reverse('cv:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'CV not available.')
        for t in q_types:
            self.assertContains(response, t)

    def test_redirects_after_POST(self):
        create_cv()
        response = self.client.post(reverse('cv:edit'), data=create_post_data({'name': 'New Name'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('cv:preview'))

    def test_can_save_post_request(self):
        create_cv()
        self.client.post(reverse('cv:edit'), data=create_post_data({'name': 'New Name'}))

        self.assertEqual(Credentials.objects.count(), 1)
        self.assertEqual(Credentials.objects.first().name, 'New Name')
        self.assertEqual(Qualification.objects.count(), q_count * len(q_types))

    def test_cv_creation(self):
        data = create_credentials_data()
        self.assertIsNone(Credentials.objects.first())
        response = self.client.post(reverse('cv:edit'), data=create_post_data(data))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Credentials.objects.count(), 1)
        field_values = lambda d: {k: d[k] for k in d.keys() & data.keys()}
        self.assertEqual(field_values(vars(Credentials.objects.first())), field_values(vars(Credentials(**data))))

    def test_submit_invalid_data(self):
        create_cv()
        with self.assertRaises(ValidationError):
            self.client.post(reverse('cv:edit'), data={})
