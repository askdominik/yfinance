from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Company


class CompanyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_company(self):
        response = self.client.post(
            "/api/companies/add_company/", {"symbol": "AAPL"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "company added")

    def test_add_company_with_invalid_symbol(self):
        response = self.client.post(
            "/api/companies/add_company/", {"symbol": "INVALID"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_company_without_symbol(self):
        response = self.client.post("/api/companies/add_company/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "symbol not provided")

    def test_get_company(self):
        company = Company.objects.create(symbol="AAPL", name="Apple Inc.")
        response = self.client.get(f"/api/companies/get_company/{company.symbol}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["symbol"], company.symbol)
        self.assertEqual(response.data["name"], company.name)

    def test_update_company(self):
        company = Company.objects.create(symbol="AAPL", name="Apple Inc.")
        response = self.client.put(
            f"/api/companies/update_company/{company.symbol}/",
            {"symbol": "AAPL"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "company updated")

    def test_update_non_existent_company(self):
        response = self.client.put(
            f"/api/companies/update_company/NONEXISTENT/",
            {"symbol": "NONEXISTENT"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_company(self):
        company = Company.objects.create(symbol="AAPL", name="Apple Inc.")
        response = self.client.delete(
            f"/api/companies/delete_company/{company.symbol}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_company(self):
        response = self.client.delete(
            f"/api/companies/delete_company/NONEXISTENT/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_export(self):
        Company.objects.create(symbol="AAPL", name="Apple Inc.")
        response = self.client.get("/api/companies/export/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.content.startswith(b"Symbol,Name,Last Updated"))

    def test_export_with_date_filtering(self):
        Company.objects.create(
            symbol="AAPL", name="Apple Inc.", last_updated=timezone.now()
        )
        start_date = timezone.make_aware(datetime(2024, 5, 28))
        end_date = timezone.make_aware(datetime(2024, 5, 30))
        response = self.client.get(
            f"/api/companies/export/?start_date={start_date.date()}&end_date={end_date.date()}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.content.decode("utf-8")
        self.assertTrue(content.startswith("Symbol,Name,Last Updated"))
        self.assertIn("AAPL", content)
        self.assertIn("Apple Inc.", content)
