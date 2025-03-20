# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import datetime
import hashlib
import hmac
import uuid
from urllib.parse import parse_qs

import requests

from .common import CANCELLED, DENIED, PAID, URL, WAITING, PaymentCommon, PaymentException, PaymentResponse, _

__all__ = ['Payment']


class WorldlineAPI:
    def __init__(self, *, url: str, pspid: str, api_key: str, api_secret: str):
        self.url = url
        self.pspid = pspid
        self.api_key = api_key
        self.api_secret = api_secret

    def _worldline_make_request(
        self, endpoint: str, payload: dict = None, method='POST', idempotency_key: str = None
    ):
        """Make a request to Worldline API at the specified endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request.
        :param dict payload: The payload of the request.
        :param str method: The HTTP method of the request.
        :param str idempotency_key: The idempotency key to pass in the request.
        :return: The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If an HTTP error occurs.
        """

        pspid = self.pspid
        path = f'/v2/{pspid}/{endpoint}'
        url = f'{self.url}{path}'
        content_type = 'application/json; charset=utf-8' if method == 'POST' else ''
        dt = datetime.datetime.now(datetime.timezone.utc).strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        )  # Datetime in RFC1123.
        signature = self._worldline_calculate_signature(
            method, endpoint, content_type, dt, idempotency_key=idempotency_key
        )
        api_key = self.api_key
        authorization_header = f'GCS v1HMAC:{api_key}:{signature}'
        headers = {
            'Authorization': authorization_header,
            'Date': dt,
            'Content-Type': content_type,
        }
        if method == 'POST' and idempotency_key:
            headers['X-GCS-Idempotence-Key'] = idempotency_key
        try:
            response = requests.request(method, url, json=payload, headers=headers, timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                msg = ', '.join([error.get('message', '') for error in response.json().get('errors', [])])
                raise PaymentException(
                    'Worldline: ' + _('The communication with the API failed. Details: %s') % msg
                )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise PaymentException('Worldline: ' + _('Could not establish the connection to the API.'))
        return response.json()

    def _worldline_calculate_signature(
        self, method: str, endpoint: str, content_type: str, dt_rfc: str, idempotency_key: str = None
    ):
        """Compute the signature for the provided data.

        See https://docs.direct.worldline-solutions.com/en/integration/api-developer-guide/authentication.

        :param str method: The HTTP method of the request
        :param str endpoint: The endpoint to be reached by the request.
        :param str content_type: The 'Content-Type' header of the request.
        :param datetime.datetime dt_rfc: The timestamp of the request, in RFC1123 format.
        :param str idempotency_key: The idempotency key to pass in the request.
        :return: The calculated signature.
        :rtype: str
        """
        # specific order required: method, content_type, date, custom headers, endpoint
        values_to_sign = [method, content_type, dt_rfc]
        if idempotency_key:
            values_to_sign.append(f'x-gcs-idempotence-key:{idempotency_key}')
        values_to_sign.append(f'/v2/{self.pspid}/{endpoint}')

        signing_str = '\n'.join(values_to_sign) + '\n'
        api_secret = self.api_secret
        signature = hmac.new(api_secret.encode(), signing_str.encode(), hashlib.sha256)
        return base64.b64encode(signature.digest()).decode()

    def hosted_checkout(
        self,
        *,
        amount: int,
        return_url: str,
        reference: str,
        first_name='',
        last_name='',
        email='',
        phone='',
        currency_code='EUR',
        show_result_page=True,
        webhook_url='',
        authorization_mode='SALE',
    ):
        # https://docs.direct.worldline-solutions.com/en/api-reference#tag/HostedCheckout/operation/CreateHostedCheckoutApi
        assert isinstance(amount, int)
        payload = {
            'hostedCheckoutSpecificInput': {
                'returnUrl': return_url,
                'showResultPage': show_result_page,
            },
            'order': {
                'amountOfMoney': {
                    # en centimes
                    'amount': amount,
                    'currencyCode': currency_code,
                },
                'references': {
                    'merchantReference': reference,
                },
            },
        }
        if email:
            payload['order'].setdefault('customer', {}).setdefault('contactDetails', {})[
                'emailAddress'
            ] = email
        if phone:
            payload['order'].setdefault('customer', {}).setdefault('contactDetails', {})[
                'phoneNumber'
            ] = phone
        if first_name:
            payload['order'].setdefault('customer', {}).setdefault('personalInformation', {}).setdefault(
                'name', {}
            )['firstName'] = first_name
        if last_name:
            payload['order'].setdefault('customer', {}).setdefault('personalInformation', {}).setdefault(
                'name', {}
            )['surName'] = last_name
        if webhook_url:
            payload.setdefault('feedbacks', {})['webhookUrl'] = webhook_url
        if authorization_mode:
            assert authorization_mode in ['PRE_AUTHORIZATION', 'SALE']
            payload.setdefault('cardPaymentMethodSpecificInput', {})['authorizationMode'] = authorization_mode
        return self._worldline_make_request('hostedcheckouts', payload=payload)

    def hosted_checkout_status(self, *, hosted_checkout_id):
        # https://docs.direct.worldline-solutions.com/en/api-reference#tag/HostedCheckout/operation/GetHostedCheckoutApi
        return self._worldline_make_request(f'hostedcheckouts/{hosted_checkout_id}', method='GET')

    def payment_capture(self, amount, payment_id, idempotency_key=None):
        # https://docs.direct.worldline-solutions.com/en/api-reference#tag/Payments/operation/CapturePaymentApi

        payload = {
            'amount': amount,
        }
        return self._worldline_make_request(
            f'payments/{payment_id}/capture', payload=payload, idempotency_key=idempotency_key
        )

    def payment_cancel(self, amount, payment_id, idempotency_key=None, currency_code='EUR'):
        # https://docs.direct.worldline-solutions.com/en/api-reference#tag/Payments/operation/CancelPaymentApi
        payload = {
            'amountOfMoney': {
                'amount': amount,
                'currencyCode': currency_code,
            },
            'isFinal': True,
        }
        return self._worldline_make_request(
            f'payments/{payment_id}/cancel', payload=payload, idempotency_key=idempotency_key
        )

    def payment_details(self, payment_id):
        return self._worldline_make_request(f'payments/{payment_id}/details', method='GET')


class Payment(PaymentCommon):
    '''Implements Worldline API, see .https://docs.direct.worldline-solutions.com/en/integration/basic-integration-methods/hosted-checkout-page'''

    preprod_url = 'https://payment.preprod.direct.worldline-solutions.com'
    prod_url = 'https://payment.direct.worldline-solutions.com'

    description = {
        'caption': 'Worldline API v2',
        'parameters': [
            {
                'name': 'environment',
                'caption': _('Environment'),
                'type': str,
                'choices': ['preprod', 'prod'],
            },
            {
                'name': 'pspid',
                'caption': _('PSPID'),
                'type': str,
                'required': True,
            },
            {
                'name': 'api_key',
                'caption': _('API key'),
                'required': True,
                'type': str,
            },
            {
                'name': 'api_secret',
                'caption': _('API secret'),
                'required': True,
            },
            {
                'name': 'normal_return_url',
                'caption': _('Normal return URL'),
                'default': '',
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Automatic return URL'),
                'required': False,
            },
        ],
    }

    def get_api(self):
        if self.environment == 'prod':
            url = self.prod_url
        elif self.environment == 'preprod':
            url = self.preprod_url
        else:
            raise NotImplementedError
        return WorldlineAPI(url=url, pspid=self.pspid, api_key=self.api_key, api_secret=self.api_secret)

    def request(
        self,
        amount,
        name=None,
        first_name=None,
        last_name=None,
        address=None,
        email=None,
        phone=None,
        orderid=None,
        info1=None,
        info2=None,
        info3=None,
        next_url=None,
        transaction_id=None,
        authorization_mode='SALE',
        **kwargs,
    ):
        amount = int(self.clean_amount(amount))
        api = self.get_api()
        transaction_id = transaction_id or uuid.uuid4().hex
        hosted_checkout_response = api.hosted_checkout(
            amount=amount,
            return_url=self.normal_return_url,
            reference=f'{transaction_id} {orderid or ""}',
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            authorization_mode=authorization_mode,
        )
        return hosted_checkout_response['hostedCheckoutId'], URL, hosted_checkout_response['redirectUrl']

    def response(self, query_string, redirect=False, order_id_hint=None, order_status_hint=None, **kwargs):
        # ex.: ?RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId=4311628069
        fields = parse_qs(query_string, True)
        hosted_checkout_id = (fields.get('hostedCheckoutId') or [order_id_hint])[0]
        return self.get_hosted_checkout_response(hosted_checkout_id)

    def get_hosted_checkout_response(self, hosted_checkout_id):
        api = self.get_api()
        hosted_checkout_details = api.hosted_checkout_status(hosted_checkout_id=hosted_checkout_id)
        payment_id = hosted_checkout_details['createdPaymentOutput']['payment']['id']
        payment_details = api.payment_details(payment_id=payment_id)

        # https://docs.direct.worldline-solutions.com/en/integration/api-developer-guide/statuses
        status = hosted_checkout_details['status']
        payment_status = payment_details['status']
        if status == 'PAYMENT_CREATED':
            status_category = hosted_checkout_details['createdPaymentOutput']['paymentStatusCategory']
            if status_category == 'SUCCESSFUL':
                eopayment_result = PAID
            elif status_category == 'STATUS_UNKNOWN':
                eopayment_result = WAITING
            elif status_category == 'REJECTED':
                if payment_status == 'CREATED':
                    eopayment_result = WAITING
                elif payment_status == 'CANCELLED':
                    eopayment_result = CANCELLED
                elif payment_status in ('REJECTED', 'REJECTED_CAPTURE'):
                    eopayment_result = DENIED
                else:
                    raise NotImplementedError
        elif status == 'IN_PROGRESS':
            eopayment_result = WAITING
        elif status == 'CANCELLED_BY_CONSUMER':
            eopayment_result = CANCELLED
        else:
            raise NotImplementedError
        return PaymentResponse(
            result=eopayment_result,
            signed=True,
            bank_data={
                'hosted_checkout': hosted_checkout_details,
                'payment_details': payment_details,
            },
            order_id=hosted_checkout_id,
            bank_status=payment_status,
            test=self.environment == 'preprod',
        )

    def cancel(self, amount, bank_data, **kwargs):
        amount = int(self.clean_amount(amount))
        hosted_checkout_id = bank_data['hosted_checkout']['createdPaymentOutput']['payment'][
            'hostedCheckoutSpecificOutput'
        ]['hostedCheckoutId']
        api = self.get_api()
        hosted_checkout_details = api.hosted_checkout_status(hosted_checkout_id=hosted_checkout_id)
        payment_id = hosted_checkout_details['createdPaymentOutput']['payment']['id']
        payment_details = api.payment_details(payment_id=payment_id)
        status = payment_details['status']
        if not status == 'PENDING_CAPTURE':
            return {'hosted_checkout': hosted_checkout_details, 'payment_details': payment_details}
        cancel_response = api.payment_cancel(amount, payment_id)
        payment_details = api.payment_details(payment_id=payment_id)
        return {
            'hosted_checkout': hosted_checkout_details,
            'cancel': cancel_response,
            'payment_details': payment_details,
        }

    def validate(self, amount, bank_data, **kwargs):
        amount = int(self.clean_amount(amount))
        hosted_checkout_id = bank_data['hosted_checkout']['createdPaymentOutput']['payment'][
            'hostedCheckoutSpecificOutput'
        ]['hostedCheckoutId']
        api = self.get_api()
        hosted_checkout_details = api.hosted_checkout_status(hosted_checkout_id=hosted_checkout_id)
        payment_id = hosted_checkout_details['createdPaymentOutput']['payment']['id']
        payment_details = api.payment_details(payment_id=payment_id)
        status = payment_details['status']
        if not status == 'PENDING_CAPTURE':
            return {'hosted_checkout': hosted_checkout_details, 'payment_details': payment_details}
        capture_response = api.payment_capture(amount, payment_id)
        payment_details = api.payment_details(payment_id=payment_id)
        return {
            'hosted_checkout': hosted_checkout_details,
            'capture': capture_response,
            'payment_details': payment_details,
        }

    def payment_status(self, transaction_id, **kwargs):
        return self.get_hosted_checkout_response(transaction_id)

    def diagnostic(self, *, bank_data, **kwargs):
        hosted_checkout_id = bank_data['hosted_checkout']['createdPaymentOutput']['payment'][
            'hostedCheckoutSpecificOutput'
        ]['hostedCheckoutId']
        api = self.get_api()
        hosted_checkout_details = api.hosted_checkout_status(hosted_checkout_id=hosted_checkout_id)

        payment_id = hosted_checkout_details['createdPaymentOutput']['payment']['id']
        payment_details = api.payment_details(payment_id=payment_id)
        return {
            'hosted_checkout': hosted_checkout_details,
            'payment_details': payment_details,
        }

    @classmethod
    def guess(cls, *, method=None, query_string=None, body=None, headers=None, backends=(), **kwargs):
        for content in [query_string, body]:
            if isinstance(content, bytes):
                try:
                    content = content.decode()
                except UnicodeDecodeError:
                    pass
            if isinstance(content, str):
                fields = parse_qs(content)
                if 'hostedCheckoutId' in fields:
                    return fields['hostedCheckoutId'][0]
        return None
