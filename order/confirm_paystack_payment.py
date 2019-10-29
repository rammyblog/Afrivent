from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from python_paystack.paystack_config import PaystackConfig


def confirmPaystackPayment(ref_code):
    PaystackConfig.SECRET_KEY  = 'sk_test_4bc9c2030fe11485c51ce1692428ce37663c9d6c'
    PaystackConfig.PUBLIC_KEY = 'pk_test_66242613f73c8034560a3eecf9d248787f776bdb'
    transaction_manager = TransactionsManager() 
    transaction_verify = transaction_manager.verify_transaction(ref_code)
    return transaction_verify
