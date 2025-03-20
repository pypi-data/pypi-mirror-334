# eopayment - online payment library

import contextlib
import json
import os

import pytest
from responses import RequestsMock, _recorder

from eopayment import Payment, common
from eopayment.worldline import Payment as WorldlinePayment
from eopayment.worldline import WorldlineAPI


@pytest.fixture
def worldline_params(backend_params):
    params = {
        'pspid': 'Entrouvert1',
        'api_key': '1234',
        'api_secret': '4567',
        **{key[10:]: value for key, value in backend_params.items() if key.startswith('worldline_')},
    }
    return params


@pytest.fixture
def api(worldline_params):
    return WorldlineAPI(
        url=WorldlinePayment.preprod_url,
        **worldline_params,
    )


HOSTEDCHECKOUTS_RESPONSE = {
    'RETURNMAC': 'ab874513-9f40-4ca0-a7c7-8dc14bc4e09d',
    'hostedCheckoutId': '4306873688',
    'merchantReference': '1234',
    'partialRedirectUrl': 'preprod.direct.worldline-solutions.com/hostedcheckout/PaymentMethods/Selection/ca5387a6432e47ed9e2ad17b27bf8385',
    'redirectUrl': 'https://payment.preprod.direct.worldline-solutions.com/hostedcheckout/PaymentMethods/Selection/ca5387a6432e47ed9e2ad17b27bf8385',
}


@pytest.fixture
def hostedcheckouts_mock(rsps):
    return rsps.post(
        'https://payment.preprod.direct.worldline-solutions.com/v2/Entrouvert1/hostedcheckouts',
        json=HOSTEDCHECKOUTS_RESPONSE,
    )


@pytest.fixture
def rsps_recorder(request):
    module_name = request.module.__name__.split('test_', 1)[-1]
    function_name = request.function.__name__
    save = request.config.getoption('--save-http-session')
    dir_path = f'tests/data/{module_name}/'
    given_name = getattr(request, 'param', None)
    path = f'{dir_path}{given_name or function_name}.yaml'

    os.makedirs(dir_path, exist_ok=True)

    with contextlib.ExitStack() as stack:
        if save:
            rsps = stack.enter_context(_recorder.Recorder())
        else:
            rsps = stack.enter_context(RequestsMock())
            rsps._add_from_file(path)
        yield rsps
        if save:
            print(f'Saving HTTP responses to {path}.')
            rsps.dump_to_file(path)


class TestWorldlineAPI:
    def test_hosted_checkout(self, api, rsps_recorder):
        assert api
        resp = api.hosted_checkout(
            amount=1000,
            return_url='https://example.com/return',
            reference='1234',
        )
        assert set(resp) == {
            'RETURNMAC',
            'hostedCheckoutId',
            'merchantReference',
            'partialRedirectUrl',
            'redirectUrl',
        }
        assert len(rsps_recorder.calls) == 1
        last_call = json.loads(rsps_recorder.calls[-1].request.body)
        assert last_call == {
            'cardPaymentMethodSpecificInput': {
                'authorizationMode': 'SALE',
            },
            'hostedCheckoutSpecificInput': {
                'returnUrl': 'https://example.com/return',
                'showResultPage': True,
            },
            'order': {
                'amountOfMoney': {'amount': 1000, 'currencyCode': 'EUR'},
                'references': {'merchantReference': '1234'},
            },
        }

    @pytest.mark.parametrize('rsps_recorder', ['test_hosted_checkout'], indirect=True)
    def test_hosted_checkout_all_inputs(self, api, rsps_recorder):
        assert api
        resp = api.hosted_checkout(
            amount=1000,
            email='john.doe@example.com',
            phone='+33645454545',
            first_name='John',
            last_name='Doe',
            return_url='https://example.com/return',
            reference='1234',
        )
        assert set(resp) == {
            'RETURNMAC',
            'hostedCheckoutId',
            'merchantReference',
            'partialRedirectUrl',
            'redirectUrl',
        }
        assert len(rsps_recorder.calls) == 1
        last_call = json.loads(rsps_recorder.calls[-1].request.body)
        assert last_call == {
            'cardPaymentMethodSpecificInput': {
                'authorizationMode': 'SALE',
            },
            'hostedCheckoutSpecificInput': {
                'returnUrl': 'https://example.com/return',
                'showResultPage': True,
            },
            'order': {
                'amountOfMoney': {'amount': 1000, 'currencyCode': 'EUR'},
                'customer': {
                    'contactDetails': {'emailAddress': 'john.doe@example.com', 'phoneNumber': '+33645454545'},
                    'personalInformation': {
                        'name': {
                            'firstName': 'John',
                            'surName': 'Doe',
                        },
                    },
                },
                'references': {'merchantReference': '1234'},
            },
        }

    STATUS_RESPONSE = {
        'createdPaymentOutput': {
            'payment': {
                'hostedCheckoutSpecificOutput': {
                    'hostedCheckoutId': '4311628069',
                },
                'id': '4311628069_0',
                'paymentOutput': {
                    'acquiredAmount': {
                        'amount': 10,
                        'currencyCode': 'EUR',
                    },
                    'amountOfMoney': {
                        'amount': 10,
                        'currencyCode': 'EUR',
                    },
                    'cardPaymentMethodSpecificOutput': {
                        'acquirerInformation': {
                            'name': 'ACQUIRER',
                        },
                        'authorisationCode': '837011',
                        'card': {
                            'bin': '51370098',
                            'cardNumber': '************3438',
                            'countryCode': 'BE',
                            'expiryDate': '0925',
                        },
                        'fraudResults': {
                            'avsResult': 'U',
                            'cvvResult': 'M',
                            'fraudServiceResult': 'no-advice',
                        },
                        'paymentAccountReference': 'FY2XWZZAYR8IEM8JSR47W5OUGBWVU',
                        'paymentProductId': 3,
                        'schemeReferenceData': '462482174457',
                        'threeDSecureResults': {
                            'acsTransactionId': '30085389-CFC5-46D1-AF3C-B5D8F7E486BC',
                            'authenticationStatus': 'Y',
                            'cavv': 'AAABBEg0VhI0VniQEjRWAAAAAAA=',
                            'dsTransactionId': 'f25084f0-5b16-4c0a-ae5d-b24808a95e4b',
                            'eci': '5',
                            'flow': 'frictionless',
                            'liability': 'issuer',
                            'schemeEci': '02',
                            'version': '2.2.0',
                            'xid': 'NDMxMTYyODA2OQ==',
                        },
                    },
                    'customer': {
                        'device': {
                            'ipAddressCountryCode': '99',
                        },
                    },
                    'paymentMethod': 'card',
                    'references': {
                        'merchantReference': '95ed629d7b484eaf91fd263498e15afe #1234',
                    },
                },
                'status': 'PENDING_CAPTURE',
                'statusOutput': {
                    'isAuthorized': True,
                    'isCancellable': True,
                    'isRefundable': False,
                    'statusCategory': 'PENDING_MERCHANT',
                    'statusCode': 5,
                },
            },
            'paymentStatusCategory': 'SUCCESSFUL',
        },
        'status': 'PAYMENT_CREATED',
    }

    def test_hosted_checkout_status(self, api, rsps_recorder):
        assert api.hosted_checkout_status(hosted_checkout_id='4315624881') == {
            'createdPaymentOutput': {
                'payment': {
                    'hostedCheckoutSpecificOutput': {
                        'hostedCheckoutId': '4315624881',
                    },
                    'id': '4315624881_0',
                    'paymentOutput': {
                        'acquiredAmount': {
                            'amount': 1010,
                            'currencyCode': 'EUR',
                        },
                        'amountOfMoney': {
                            'amount': 1010,
                            'currencyCode': 'EUR',
                        },
                        'cardPaymentMethodSpecificOutput': {
                            'acquirerInformation': {
                                'name': 'ACQUIRER',
                            },
                            'authorisationCode': '493667',
                            'card': {
                                'bin': '51370098',
                                'cardNumber': '************3438',
                                'countryCode': 'BE',
                                'expiryDate': '0129',
                            },
                            'fraudResults': {
                                'avsResult': 'U',
                                'cvvResult': 'M',
                                'fraudServiceResult': 'no-advice',
                            },
                            'paymentAccountReference': '3XIWXHQPYAZUF5CVKLQE2F7WFKIV7',
                            'paymentProductId': 3,
                            'schemeReferenceData': '151645221224',
                            'threeDSecureResults': {
                                'acsTransactionId': '30085389-CFC5-46D1-AF3C-B5D8F7E486BC',
                                'authenticationStatus': 'Y',
                                'cavv': 'AAABBEg0VhI0VniQEjRWAAAAAAA=',
                                'dsTransactionId': 'f25084f0-5b16-4c0a-ae5d-b24808a95e4b',
                                'eci': '5',
                                'flow': 'frictionless',
                                'liability': 'issuer',
                                'schemeEci': '02',
                                'version': '2.2.0',
                                'xid': 'NDMxNTYyNDg4MQ==',
                            },
                        },
                        'customer': {
                            'device': {
                                'ipAddressCountryCode': '99',
                            },
                        },
                        'paymentMethod': 'card',
                        'references': {
                            'merchantReference': 'abcd5678 #1234',
                        },
                    },
                    'status': 'CAPTURED',
                    'statusOutput': {
                        'isAuthorized': False,
                        'isCancellable': False,
                        'isRefundable': True,
                        'statusCategory': 'COMPLETED',
                        'statusCode': 9,
                    },
                },
                'paymentStatusCategory': 'SUCCESSFUL',
            },
            'status': 'PAYMENT_CREATED',
        }


@pytest.fixture
def payment(worldline_params):
    return Payment(
        'worldline',
        {
            'normal_return_url': 'https://example.com/return',
            'automatic_return_url': 'https://example.com/callback',
            'environment': 'preprod',
            **worldline_params,
        },
    )


class TestEopaymentAPI:
    def test_constructor(self, payment):
        assert payment
        params = {param['name']: param for param in payment.get_parameters()}
        assert set(params) == {
            'environment',
            'pspid',
            'api_key',
            'api_secret',
            'automatic_return_url',
            'normal_return_url',
        }
        assert set(params['environment']['choices']) == {'prod', 'preprod'}

    def test_direct_sale(self, payment, rsps_recorder):
        trans_id, _, _ = payment.request(
            amount='10.10',
            orderid='#1234',
            transaction_id='abcd5678',
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            phone='+33641414141',
        )

        if len(rsps_recorder.calls):
            last_call = json.loads(rsps_recorder.calls[-1].request.body)
            assert last_call == {
                'cardPaymentMethodSpecificInput': {
                    'authorizationMode': 'SALE',
                },
                'hostedCheckoutSpecificInput': {
                    'returnUrl': 'https://example.com/return',
                    'showResultPage': True,
                },
                'order': {
                    'amountOfMoney': {'amount': 1010, 'currencyCode': 'EUR'},
                    'references': {'merchantReference': 'abcd5678 #1234'},
                    'customer': {
                        'contactDetails': {
                            'emailAddress': 'john.doe@example.com',
                            'phoneNumber': '+33641414141',
                        },
                        'personalInformation': {
                            'name': {
                                'firstName': 'John',
                                'surName': 'Doe',
                            },
                        },
                    },
                },
            }

        # wait for payment...
        query_string = f'RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId={trans_id}'
        response = payment.response(query_string, redirect=True, order_id_hint='#1234')
        assert response.test
        assert response.order_id == trans_id
        assert response.bank_status == 'CAPTURED'
        assert (
            response.bank_data['hosted_checkout']['createdPaymentOutput']['payment']['status'] == 'CAPTURED'
        )
        assert response.result == common.PAID

        # wait for capture...
        diagnostic_response = payment.diagnostic(bank_data=response.bank_data)
        assert diagnostic_response['payment_details']['status'] == 'CAPTURED'

    def test_authorization_capture(self, payment, rsps_recorder):
        trans_id, _, _ = payment.request(
            amount='10.10', orderid='#1234', transaction_id='abcd5678', authorization_mode='PRE_AUTHORIZATION'
        )
        if len(rsps_recorder.calls):
            last_call = json.loads(rsps_recorder.calls[-1].request.body)
            assert last_call == {
                'cardPaymentMethodSpecificInput': {
                    'authorizationMode': 'PRE_AUTHORIZATION',
                },
                'hostedCheckoutSpecificInput': {
                    'returnUrl': 'https://example.com/return',
                    'showResultPage': True,
                },
                'order': {
                    'amountOfMoney': {'amount': 1010, 'currencyCode': 'EUR'},
                    'references': {'merchantReference': 'abcd5678 #1234'},
                },
            }

        # wait for payment...
        query_string = f'RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId={trans_id}'
        response = payment.response(query_string, redirect=True, order_id_hint='#1234')
        assert response.test
        assert response.order_id == trans_id
        assert response.bank_status == 'PENDING_CAPTURE'
        assert (
            response.bank_data['hosted_checkout']['createdPaymentOutput']['payment']['status']
            == 'PENDING_CAPTURE'
        )
        assert response.result == common.PAID

        # capture the authorization, capture can be full or partial.
        validate_response = payment.validate('10.10', response.bank_data)
        assert (
            validate_response['hosted_checkout']['createdPaymentOutput']['payment']['status']
            == 'PENDING_CAPTURE'
        )
        assert validate_response['payment_details']['status'] == 'CAPTURE_REQUESTED'
        diagnostic_response = payment.diagnostic(bank_data=response.bank_data)
        assert diagnostic_response['payment_details']['status'] == 'CAPTURE_REQUESTED'

        # after some time final status is captured
        diagnostic_response = payment.diagnostic(bank_data=response.bank_data)
        assert diagnostic_response['payment_details']['status'] == 'CAPTURED'

    def test_authorization_cancel(self, payment, rsps_recorder):
        trans_id, _, _ = payment.request(
            amount='10.10', orderid='#1234', transaction_id='abcd5678', authorization_mode='PRE_AUTHORIZATION'
        )
        if len(rsps_recorder.calls):
            last_call = json.loads(rsps_recorder.calls[-1].request.body)
            assert last_call == {
                'cardPaymentMethodSpecificInput': {
                    'authorizationMode': 'PRE_AUTHORIZATION',
                },
                'hostedCheckoutSpecificInput': {
                    'returnUrl': 'https://example.com/return',
                    'showResultPage': True,
                },
                'order': {
                    'amountOfMoney': {'amount': 1010, 'currencyCode': 'EUR'},
                    'references': {'merchantReference': 'abcd5678 #1234'},
                },
            }

        # wait for payment...
        query_string = f'RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId={trans_id}'
        response = payment.response(query_string, redirect=True, order_id_hint='#1234')
        assert response.test
        assert response.order_id == trans_id
        assert (
            response.bank_data['hosted_checkout']['createdPaymentOutput']['payment']['status']
            == 'PENDING_CAPTURE'
        )
        assert response.result == common.PAID

        # cancel the authorization, cancelation can be full or partial.
        cancel_response = payment.cancel('10.10', response.bank_data)
        assert cancel_response['cancel']['payment']['status'] == 'CANCELLED'
        assert (
            cancel_response['hosted_checkout']['createdPaymentOutput']['payment']['status']
            == 'PENDING_CAPTURE'
        )
        assert cancel_response['payment_details']['status'] == 'CANCELLED'
        diagnostic_response = payment.diagnostic(bank_data=response.bank_data)
        assert diagnostic_response['payment_details']['status'] == 'CANCELLED'

    def test_payment_status(self, payment, rsps_recorder):
        response = payment.payment_status('4315597345')
        assert response.test
        assert response.order_id == '4315597345'
        assert response.bank_status == 'CAPTURED'
        assert (
            response.bank_data['hosted_checkout']['createdPaymentOutput']['payment']['status'] == 'CAPTURED'
        )
        assert response.result == common.PAID

    def test_direct_sale_cancelled_by_user(self, payment, rsps_recorder):
        trans_id, _, _ = payment.request(
            amount='10.10',
            orderid='#1234',
            transaction_id='abcd5678',
        )

        # wait for payment...
        query_string = f'RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId={trans_id}'
        response = payment.response(query_string, redirect=True, order_id_hint='#1234')
        assert response.test
        assert response.order_id == trans_id
        assert response.bank_status == 'CANCELLED'
        assert (
            response.bank_data['hosted_checkout']['createdPaymentOutput']['payment']['status'] == 'CANCELLED'
        )
        assert response.result == common.CANCELLED

    def test_guess(self, payment):
        query_string = 'RETURNMAC=dd70af3f-31ed-4366-a5c9-d8e2f8e0fa55&hostedCheckoutId=1234'
        assert payment.guess(query_string=query_string) == ('worldline', '1234')
