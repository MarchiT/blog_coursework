from django.test import TestCase

from django.urls import reverse

from .models import Credentials, CV, Qualifications, Qualification

t = Qualifications.QTypes


def create_cv():
    credentials = Credentials.objects.create(name='Marina', address='Test Address',
                                             phone='+1234', email='marina@example.com')
    cv = CV.objects.create(credentials=credentials)

    types = [{'type': v, 'on_cv_id': cv.id} for v in t.values]
    cv.qualifications_set.bulk_create(Qualifications(**q) for q in types)

    for qt in t.values:
        qs = cv.qualifications_set.get(type=qt)
        data = [{'text': qt + str(i), 'qualifications_id': qs.id} for i in range(3)]
        qs.qualification_set.bulk_create(Qualification(**q) for q in data)

    return cv


class CVPreviewTests(TestCase):
    def test_uses_preview_template(self):
        url = reverse('cv:preview')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/preview.html')

    def test_preview_page_without_cv(self):
        response = self.client.get(reverse('cv:preview'))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['cv'], None)
        self.assertContains(response, 'CV not available.')

    def test_preview_page_with_cv(self):
        create_cv()
        response = self.client.get(reverse('cv:preview'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'CV not available.')
        # assert all section names are present
        for q_type in t.names:
            self.assertContains(response, q_type)

    def test_cv_credentials_should_be_displayed(self):
        cv = create_cv()
        response = self.client.get(reverse('cv:preview'))

        self.assertContains(response, cv.credentials.name)
        self.assertContains(response, cv.credentials.phone)
        self.assertContains(response, cv.credentials.email)
        self.assertContains(response, cv.credentials.address)

    def test_cv_qualifications_should_be_displayed(self):
        cv = create_cv()
        response = self.client.get(reverse('cv:preview'))

        for qs in cv.qualifications_set.all():
            for q in qs.qualification_set.all():
                self.assertContains(response, q.text)


class CVEditTests(TestCase):
    def test_uses_edit_template(self):
        pass

    def test_edit_without_cv(self):
        pass

    def test_all_cv_sections_should_be_present(self):
        pass

    def test_can_save_POST_request(self):
        pass

    def test_redirects_after_POST(self):
        pass

    def test_should_only_save_valid_phones(self):
        pass


class CVModelTests(TestCase):
    def test_valid_phone_number(self):
        pass
