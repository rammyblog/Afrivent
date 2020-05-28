from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from python_paystack.paystack_config import PaystackConfig
from django.conf import settings


def confirmPaystackPayment(ref_code):
    PaystackConfig.SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    PaystackConfig.PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
    transaction_manager = TransactionsManager()
    transaction_verify = transaction_manager.verify_transaction(ref_code)
    return transaction_verify
