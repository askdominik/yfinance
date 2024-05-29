import csv
from datetime import datetime

import yfinance as yf
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["get"], url_path="get_company/(?P<symbol>[^/.]+)")
    def get_company(self, request, symbol=None):
        try:
            company = Company.objects.get(symbol=symbol)
        except Company.DoesNotExist:
            return Response(
                {"status": "company not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CompanySerializer(company)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_company(self, request):
        symbol = request.data.get("symbol")
        if not symbol:
            return Response(
                {"status": "symbol not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        company_info = yf.Ticker(symbol).info
        company_name = company_info.get("longName")

        if not company_name:
            return Response(
                {"status": "company name not found in Yahoo Finance data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        _, created = Company.objects.get_or_create(
            symbol=symbol, defaults={"name": company_info["longName"]}
        )
        if created:
            return Response({"status": "company added"}, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "company already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["put"], url_path="update_company/(?P<symbol>[^/.]+)")
    def update_company(self, request, symbol=None):
        try:
            company = Company.objects.get(symbol=symbol)
        except Company.DoesNotExist:
            return Response(
                {"status": "company not found"}, status=status.HTTP_404_NOT_FOUND
            )

        new_symbol = request.data.get("symbol")
        if not new_symbol:
            return Response(
                {"status": "symbol not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        company.symbol = new_symbol

        company_info = yf.Ticker(company.symbol).info
        company.name = company_info.get("longName")

        if not company.name:
            return Response(
                {"status": "company name not found in Yahoo Finance data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        company.save()
        return Response({"status": "company updated"})

    @action(
        detail=False, methods=["delete"], url_path="delete_company/(?P<symbol>[^/.]+)"
    )
    def delete_company(self, request, symbol=None):
        try:
            company = Company.objects.get(symbol=symbol)
            company.delete()
            return Response(
                {"status": "company deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Company.DoesNotExist:
            return Response(
                {"status": "company not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def export(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        companies = Company.objects.all()

        if start_date_str:
            start_date = parse_date(start_date_str)
            if start_date:
                start_date = datetime.combine(start_date, datetime.min.time())
                start_date = make_aware(start_date)
                companies = companies.filter(last_updated__gte=start_date)

        if end_date_str:
            end_date = parse_date(end_date_str)
            if end_date:
                end_date = datetime.combine(end_date, datetime.max.time())
                end_date = make_aware(end_date)
                companies = companies.filter(last_updated__lte=end_date)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="companies.csv"'

        writer = csv.writer(response)
        writer.writerow(["Symbol", "Name", "Last Updated"])
        for company in companies:
            writer.writerow([company.symbol, company.name, company.last_updated])

        return response
