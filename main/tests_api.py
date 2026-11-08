import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )
        self.editor.groups.add(self.editor_group)

        self.education = Education.objects.create(
            school="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            start_year="2025",
            end_year="2029",
            description="Pendidikan tinggi",
        )

        self.list_url = reverse("api:education-list")
        self.detail_url = reverse(
            "api:education-detail",
            args=[self.education.id],
        )
        self.star_url = reverse(
            "api:education-star",
            args=[self.education.id],
        )

        self.payload = {
            "school": "Universitas Gadjah Mada",
            "degree": "S1 Informatika",
            "start_year": "2025",
            "end_year": "2029",
            "description": "Program sarjana",
            "is_active": True,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["id"],
            str(self.education.id),
        )
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"school": "UNIVERSITAS"},
        )
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"school": "not-found"},
        )
        self.assertEqual(response.data, [])

    def test_missing_education(self):
        url = reverse(
            "api:education-detail",
            args=[uuid.uuid4()],
        )
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.patch(
                self.detail_url,
                {"school": "Changed"},
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.put(
                self.detail_url,
                self.payload,
                format="json",
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.delete(self.detail_url)
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            self.assertEqual(Education.objects.count(), 1)
            self.education.refresh_from_db()
            self.assertEqual(
                self.education.school,
                "Universitas Indonesia",
            )

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Education.objects.filter(pk=response.data["id"]).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_data = [
            ({"school": "   "}, "school"),
            ({"school": "<b></b>"}, "school"),
            ({"degree": "   "}, "degree"),
            ({"start_year": "20250"}, "start_year"),
        ]

        for changes, field in invalid_data:
            data = self.payload.copy()
            data.update(changes)

            response = self.client.post(
                self.list_url,
                data,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
            self.assertIn(field, response.data)

        self.assertEqual(Education.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"school": "Universitas Indonesia Depok"},
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.degree,
            "S1 Ilmu Komputer",
        )

        response = self.client.put(
            self.detail_url,
            {"school": "Incomplete"},
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(response.content, b"")
        self.assertFalse(
            Education.objects.filter(pk=self.education.id).exists()
        )

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        data = self.payload.copy()
        data.update({
            "star_count": 99,
            "is_starred": True,
            "starred_by_names": "forged",
            "starred_by": [self.visitor.id],
        })

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"school": "Updated by Editor"},
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(
            self.education.school,
            "Universitas Gadjah Mada",
        )

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Education.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        csrf_token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
