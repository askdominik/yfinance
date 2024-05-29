import yfinance as yf
from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Company

logger = get_task_logger(__name__)


@shared_task
def update_company_data():
    companies = Company.objects.all()
    for company in companies:
        try:
            company_info = yf.Ticker(company.symbol).info
            company_name = company_info.get('longName')
            if company_name:
                company.name = company_name
                company.save()
                logger.info(f"Updated company: {company.symbol}")
            else:
                logger.warning(f"Company name not found for symbol: {
                               company.symbol}")
        except Exception as e:
            logger.error(f"Error updating company {company.symbol}: {e}")
