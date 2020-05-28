from python_paystack.objects.transactions import Transaction
from python_paystack.managers import TransactionsManager
from python_paystack.paystack_config import PaystackConfig
from django.conf import settings
# from python_paystack.managers import



class CustomPaystack(TransactionsManager):
    def verify_transaction(self, reference_code, endpoint='/verify/'):
        '''
        Verifies a payment using the transaction reference.

        Arguments:
        endpoint : Paystack API endpoint for verifying transactions
        '''

        endpoint += reference_code
        url = self.PAYSTACK_URL + self._endpoint + endpoint

        headers, _ = self.build_request_args()
        response = requests.get(url, headers=headers)
        content = response.content
        content = self.parse_response_content(content)

        status, message = self.get_content_status(content)

        if status:
            data_dict = content['data']
            # data = json.dumps(content['data'])
            status = data_dict['status']
            print(status)
            # transaction = Transaction.from_json(data)
            # transaction.email = data_dict['customer']['email']
            # transaction.authorization_code = data_dict['authorization']['authorization_code']
            return status
        else:
            raise APIConnectionFailedError(message)


def confirmPaystackPayment(ref_code):
    PaystackConfig.SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    PaystackConfig.PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
    transaction_manager = CustomPaystack()
    transaction_verify = transaction_manager.verify_transaction(ref_code)
    return transaction_verify
