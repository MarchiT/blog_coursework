from django.test import TestCase

from django.urls import reverse

from .models import Credentials, Qualification

q_types = Qualification.QTypes.values


def create_cv():
    for t in q_types:
        [Qualification(type=t, text=t + ' qualification #' + str(x)).save() for x in range(5)]
    return Credentials.objects.create(name='Marina', address='Test Address', phone='+1234', email='marina@example.com')


class CVPreviewTests(TestCase):
    def test_uses_preview_template(self):
        url = reverse('cv:preview')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/preview.html')

    def test_preview_page_without_cv(self):
        response = self.client.get(reverse('cv:preview'))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['credentials'], None)
        self.assertContains(response, 'CV not available.')

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
        # must have 'create' button instead
        response = self.client.get(reverse('cv:edit'))
        pass

    def test_all_cv_sections_should_be_present(self):
        create_cv()
        response = self.client.get(reverse('cv:edit'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'CV not available.')
        # assert all section names are present
        for t in q_types:
            self.assertContains(response, t)

    def test_can_save_POST_request(self):
        pass

    def test_redirects_after_POST(self):
        pass

    def test_should_only_save_valid_phones(self):
        pass


class CVModelTests(TestCase):
    def test_valid_phone_number(self):
        pass
