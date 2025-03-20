# eopayment - online payment library
# Copyright (C) 2011-2022 Entr'ouvert
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

import pytest

import eopayment


def test_get_backends():
    assert len(eopayment.get_backends()) > 1


GUESS_TEST_VECTORS = [
    {
        'name': 'tipi',
        'kwargs': {
            'query_string': 'objet=tout+a+fait&montant=12312&saisie=T&mel=info%40entrouvert.com'
            '&numcli=12345&exer=9999&refdet=999900000000999999&resultrans=P',
        },
        'result': ['tipi', '999900000000999999'],
    },
    {
        'name': 'payfip_ws',
        'kwargs': {
            'query_string': 'idOp=1234',
        },
        'result': ['payfip_ws', '1234'],
    },
    {
        'name': 'systempayv2-old-transaction-id',
        'kwargs': {
            'query_string': 'vads_amount=1042&vads_auth_mode=FULL&vads_auth_number=3feadf'
            '&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB'
            '&vads_result=00'
            '&vads_card_number=497010XXXXXX0000'
            '&vads_payment_certificate=582ba2b725057618706d7a06e9e59acdbf69ff53'
            '&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1042'
            '&vads_site_id=70168983&vads_trans_date=20161013101355'
            '&vads_trans_id=226787&vads_trans_uuid=4b5053b3b1fe4b02a07753e7a'
            '&vads_effective_creation_date=20200330162530'
            '&signature=c17fab393f94dc027dc029510c85d5fc46c4710f',
        },
        'result': ['systempayv2', '20161013101355_226787'],
    },
    {
        'name': 'systempayv2-eo-trans-id',
        'kwargs': {
            'query_string': 'vads_amount=1042&vads_auth_mode=FULL&vads_auth_number=3feadf'
            '&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB'
            '&vads_result=00'
            '&vads_card_number=497010XXXXXX0000'
            '&vads_payment_certificate=582ba2b725057618706d7a06e9e59acdbf69ff53'
            '&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1042'
            '&vads_site_id=70168983&vads_trans_date=20161013101355'
            '&vads_trans_id=226787&vads_trans_uuid=4b5053b3b1fe4b02a07753e7a'
            '&vads_effective_creation_date=20200330162530'
            '&signature=c17fab393f94dc027dc029510c85d5fc46c4710f'
            '&vads_ext_info_eopayment_trans_id=123456',
        },
        'result': ['systempayv2', '123456'],
    },
    {
        'name': 'paybox',
        'kwargs': {
            'query_string': 'montant=4242&reference=abcdef&code_autorisation=A'
            '&erreur=00000&date_transaction=20200101&heure_transaction=01%3A01%3A01',
        },
        'result': ['paybox', 'abcdef'],
    },
    {
        'name': 'ogone-no-complus',
        'kwargs': {
            'query_string': 'orderid=myorder&status=9&payid=3011229363&cn=Us%C3%A9r&ncerror=0'
            '&trxdate=10%2F24%2F16&acceptance=test123&currency=eur&amount=7.5',
        },
        'result': ['ogone', 'myorder'],
    },
    {
        'name': 'ogone-with-complus',
        'kwargs': {
            'query_string': 'complus=neworder&orderid=myorder&status=9&payid=3011229363&cn=Us%C3%A9r'
            '&ncerror=0&trxdate=10%2F24%2F16&acceptance=test123&currency=eur&amount=7.5',
        },
        'result': ['ogone', 'neworder'],
    },
    {
        'name': 'mollie',
        'kwargs': {
            'body': b'id=tr_7UhSN1zuXS',
        },
        'result': ['mollie', 'tr_7UhSN1zuXS'],
    },
    {
        'name': 'sips2',
        'kwargs': {
            'body': (
                b'Data=captureDay%3D0%7CcaptureMode%3DAUTHOR_CAPTURE%7CcurrencyCode%3D978%7CmerchantId%3D002001000000001%7CorderChannel%3D'
                b'INTERNET%7CresponseCode%3D00%7CtransactionDateTime%3D2016-02-01T17%3A44%3A20%2B01%3A00%7C'
                b'transactionReference%3D668930%7CkeyVersion%3D1%7CacquirerResponseCode%3D00%7Camou'
                b'nt%3D1200%7CauthorisationId%3D12345%7CcardCSCResultCode%3D4E%7CpanExpiryDate%3D201605%7Cpay'
                b'mentMeanBrand%3DMASTERCARD%7CpaymentMeanType%3DCARD%7CcustomerIpAddress%3D82.244.203.243%7CmaskedPan'
                b'%3D5100%23%23%23%23%23%23%23%23%23%23%23%2300%7CorderId%3Dd4903de7027f4d56ac01634fd7ab9526%7CholderAuthentRelegation'
                b'%3DN%7CholderAuthentStatus%3D3D_ERROR%7CtransactionOrigin%3DINTERNET%7CpaymentPattern%3D'
                b'ONE_SHOT&Seal=6ca3247765a19b45d25ad54ef4076483e7d55583166bd5ac9c64357aac097602&InterfaceVersion=HP_2.0&Encode='
            ),
        },
        'result': ['sips2', '668930'],
    },
    {
        'name': 'dummy',
        'kwargs': {
            'query_string': b'transaction_id=123&ok=1&signed=1',
        },
        'result': ['dummy', '123'],
    },
    {
        'name': 'notfound',
        'kwargs': {},
        'exception': eopayment.BackendNotFound,
    },
    {
        'name': 'notfound-2',
        'kwargs': {'query_string': None, 'body': [12323], 'headers': {b'1': '2'}},
        'exception': eopayment.BackendNotFound,
    },
    {
        'name': 'backends-limitation',
        'kwargs': {
            'body': b'id=tr_7UhSN1zuXS',
            'backends': ['payfips_ws'],
        },
        'exception': eopayment.BackendNotFound,
    },
]


@pytest.mark.parametrize('test_vector', GUESS_TEST_VECTORS, ids=lambda tv: tv['name'])
def test_guess(test_vector):
    kwargs, result, exception = test_vector['kwargs'], test_vector.get('result'), test_vector.get('exception')
    if exception is not None:
        with pytest.raises(exception):
            eopayment.Payment.guess(**kwargs)
    else:
        assert list(eopayment.Payment.guess(**kwargs)) == result
