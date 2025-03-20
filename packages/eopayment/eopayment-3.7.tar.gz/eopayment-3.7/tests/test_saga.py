#
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


import datetime
import functools
import json
import pathlib

import pytest
import responses
import zeep.transports

import eopayment
from eopayment.common import EXPIRED, WAITING


@pytest.fixture
def saga(record_http_session):
    if type(record_http_session).__name__ != 'Mocker':
        from eopayment import saga

        saga._zeep_transport = zeep.transports.Transport(session=record_http_session)
        try:
            yield None
        finally:
            saga._zeep_transport = None
    else:
        yield


def factory(**kwargs):
    return eopayment.Payment(
        'saga',
        dict(
            {
                'num_service': '868',
                'compte': '70688',
                'automatic_return_url': 'https://automatic.notif.url/automatic/',
                'normal_return_url': 'https://normal.notif.url/normal/',
            },
            **kwargs,
        ),
    )


@pytest.fixture
def backend_factory(saga, target_url):
    return functools.partial(factory, base_url=target_url)


def test_features():
    payment = factory()
    assert payment.is_email_required


def test_error_parametrage(backend_factory):
    payment = backend_factory(num_service='1', compte='1')
    with pytest.raises(eopayment.PaymentException, match='Impossible de déterminer le paramétrage'):
        transaction_id, kind, url = payment.request(
            amount='10.00', email='john.doe@example.com', subject='Réservation concert XYZ numéro 1234'
        )


def test_request(backend_factory):
    transaction_id, kind, url = backend_factory().request(
        amount='10.00', email='john.doe@example.com', subject='Réservation concert XYZ numéro 1234'
    )
    assert transaction_id == '347b2060-1a37-11eb-af92-0213ad91a103'
    assert kind == eopayment.URL
    assert (
        url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=347b2060-1a37-11eb-af92-0213ad91a103'
    )


def test_request_custom_num_service_and_compte(backend_factory):
    transaction_id, kind, url = backend_factory().request(
        amount='10.00',
        email='john.doe@example.com',
        subject='Réservation concert XYZ numéro 1234',
        num_service='1234',
        compte='abcd',
    )
    assert transaction_id == '347b2060-1a37-11eb-af92-0213ad91a103'
    assert kind == eopayment.URL
    assert (
        url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=347b2060-1a37-11eb-af92-0213ad91a103'
    )


def test_response(backend_factory):
    response = backend_factory().response('idop=28b52f40-1ace-11eb-8ce3-0213ad91a104', redirect=False)
    assert response.__dict__ == {
        'bank_data': {
            'email': 'john.doe@entrouvert.com',
            'etat': 'paye',
            'id_tiers': '-1',
            'montant': '10.00',
            'num_service': '868',
            'numcp': '70688',
            'numcpt_lib_ecriture': 'COUCOU',
        },
        'bank_status': 'paid',
        'order_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
        'result': 3,
        'return_content': None,
        'signed': True,
        'test': False,
        'transaction_date': None,
        'transaction_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
    }
    # Check bank_data is JSON serializable
    json.dumps(response.bank_data)


def test_payment_status(backend_factory):
    response = backend_factory().payment_status('28b52f40-1ace-11eb-8ce3-0213ad91a104')
    assert response.__dict__ == {
        'bank_data': {
            'email': 'john.doe@entrouvert.com',
            'etat': 'paye',
            'id_tiers': '-1',
            'montant': '10.00',
            'num_service': '868',
            'numcp': '70688',
            'numcpt_lib_ecriture': 'COUCOU',
        },
        'bank_status': 'paid',
        'order_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
        'result': 3,
        'return_content': None,
        'signed': True,
        'test': False,
        'transaction_date': None,
        'transaction_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
    }
    # Check bank_data is JSON serializable
    json.dumps(response.bank_data)


def test_payment_status_cancelled(backend_factory):
    response = backend_factory().payment_status('28b52f40-1ace-11eb-8ce3-0213ad91a104')
    assert response.__dict__ == {
        'bank_data': {
            'email': 'john.doe@entrouvert.com',
            'etat': 'abandon',
            'id_tiers': '-1',
            'montant': '10.00',
            'num_service': '868',
            'numcp': '70688',
            'numcpt_lib_ecriture': 'COUCOU',
        },
        'bank_status': 'cancelled',
        'order_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
        'result': 5,
        'return_content': None,
        'signed': True,
        'test': False,
        'transaction_date': None,
        'transaction_id': '28b52f40-1ace-11eb-8ce3-0213ad91a104',
    }
    # Check bank_data is JSON serializable
    json.dumps(response.bank_data)


def test_payment_status_error(backend_factory):
    with pytest.raises(eopayment.PaymentException, match=r'Saga error message: foobar'):
        backend_factory().payment_status('28b52f40-1ace-11eb-8ce3-0213ad91a104')


def test_username_token_auth(record_http_session, backend_factory):
    backend = backend_factory(login='foo', password='bar')
    backend.request(
        amount='10.00',
        email='john.doe@example.com',
        subject='Réservation concert XYZ numéro 1234',
    )
    assert (
        record_http_session.requests[0].url == 'https://target.url/paiement_internet_ws_ministere_secure?wsdl'
    )
    assert record_http_session.requests[1].url == 'https://target.url/paiement_internet_ws_ministere_secure'


def test_payment_status_waiting_P5(backend_factory):
    transaction_date = datetime.datetime.now() - datetime.timedelta(minutes=19)
    assert (
        backend_factory()
        .payment_status(
            transaction_id='28b52f40-1ace-11eb-8ce3-0213ad91a104', transaction_date=transaction_date
        )
        .result
        == WAITING
    )


def test_payment_status_expired_P5(backend_factory):
    transaction_date = datetime.datetime.now() - datetime.timedelta(minutes=21)
    assert (
        backend_factory()
        .payment_status(
            transaction_id='28b52f40-1ace-11eb-8ce3-0213ad91a104', transaction_date=transaction_date
        )
        .result
        == EXPIRED
    )


def test_payment_status_expired_P1(backend_factory):
    assert backend_factory().payment_status('28b52f40-1ace-11eb-8ce3-0213ad91a104').result == EXPIRED


@responses.activate
def test_timeout(target_url):
    responses.get(
        'https://target.url/paiement_internet_ws_ministere?wsdl',
        body=pathlib.Path('tests/data/saga_paiement_internet_ws_ministere.wsdl').read_text(),
    )

    soap_response = json.loads(pathlib.Path('tests/data/saga-test_request.json').read_text())[1][1]

    post_mock = responses.post(
        'https://saga.example.com/saga/paiement_internet_ws_ministere', body=soap_response
    )

    factory(base_url=target_url).request(
        amount='10.00',
        email='john.doe@example.com',
        subject='Réservation concert XYZ numéro 1234',
        timeout=3,
    )

    assert post_mock.calls[0].request.req_kwargs['timeout'] == 15
