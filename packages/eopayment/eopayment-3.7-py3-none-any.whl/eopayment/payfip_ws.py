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


import copy
import datetime
import decimal
import functools
import os
import random
import re
import unicodedata
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs

import pytz
import requests
import zeep
import zeep.exceptions

from .common import (
    CANCELLED,
    DENIED,
    ERROR,
    EXPIRED,
    PAID,
    URL,
    WAITING,
    PaymentCommon,
    PaymentException,
    PaymentResponse,
    ResponseError,
    _,
    force_text,
)
from .systempayv2 import isonow

# The URL of the WSDL published in the documentation is still wrong, it
# references XSD files which are not resolvable :/ we must use this other URL
# where the XSD files are resolvable. To not depend too much on those files, we
# provide copy in eopayment. The PayFiP development team is full of morons.
WSDL_URL = 'https://www.payfip.gouv.fr/tpa/services/securite?wsdl'  # noqa: E501
PAYMENT_URL = 'https://www.payfip.gouv.fr/tpa/paiementws.web'

REFDET_RE = re.compile(r'^[A-Za-z0-9]{1,30}$')


def clear_namespace(element):
    def helper(element):
        if element.tag.startswith('{'):
            element.tag = element.tag[element.tag.index('}') + 1 :]
        for subelement in element:
            helper(subelement)

    element = copy.deepcopy(element)
    helper(element)
    return element


def normalize_objet(objet):
    '''Make objet a string of 100 chars in alphabet [A-Za-z0-9 ]'''
    if not objet:
        return objet

    objet = force_text(objet)
    objet = unicodedata.normalize('NFKD', objet).encode('ascii', 'ignore').decode()
    objet = re.sub(r'[\'-]', ' ', objet).strip()
    objet = re.sub(r'[^A-Za-z0-9 ]', '', objet).strip()
    objet = re.sub(r'[\s]+', ' ', objet)
    return objet[:100]


class PayFiPError(PaymentException):
    def __init__(self, code, message, origin=None):
        self.code = code
        self.message = message
        self.origin = origin
        args = [code, message]
        if origin:
            args.append(origin)
        super().__init__(*args)


class PayFiP:
    '''Encapsulate SOAP web-services of PayFiP'''

    default_timeout = 15

    def __init__(self, wsdl_url=None, service_url=None, zeep_client_kwargs=None, use_local_wsdl=True):
        # use cached WSDL
        if (not wsdl_url or (wsdl_url == WSDL_URL)) and use_local_wsdl:
            base_path = os.path.join(os.path.dirname(__file__), 'resource', 'PaiementSecuriseService.wsdl')
            wsdl_url = 'file://%s' % base_path
        self.wsdl_url = wsdl_url
        self.service_url = service_url
        self.zeep_client_kwargs = zeep_client_kwargs

    @property
    def client(self):
        if not hasattr(self, '_client'):
            try:
                self._client = zeep.Client(self.wsdl_url or WSDL_URL, **(self.zeep_client_kwargs or {}))
            except Exception as e:
                raise PayFiPError('Cound not initialize the SOAP client', e)
        return self._client

    def fault_to_exception(self, fault):
        if (
            fault.message != 'fr.gouv.finances.cp.tpa.webservice.exceptions.FonctionnelleErreur'
            or fault.detail is None
        ):
            return
        detail = clear_namespace(fault.detail)
        code = detail.find('FonctionnelleErreur/code')
        if code is None or not code.text:
            return PayFiPError('inconnu', ET.tostring(detail))
        descriptif = detail.find('FonctionnelleErreur/descriptif')
        libelle = detail.find('FonctionnelleErreur/libelle')
        return PayFiPError(
            code=code.text,
            message=(descriptif is not None and descriptif.text)
            or (libelle is not None and libelle.text)
            or '',
        )

    def _perform(self, request_qname, operation, timeout=None, **kwargs):
        RequestType = self.client.get_type(request_qname)  # noqa: E501
        try:
            with self.client.transport.settings(timeout=timeout or self.default_timeout):
                return getattr(self.client.service, operation)(RequestType(**kwargs))
        except zeep.exceptions.Fault as fault:
            raise self.fault_to_exception(fault) or PayFiPError('unknown', fault.message, fault)
        except zeep.exceptions.Error as zeep_error:
            raise PayFiPError('SOAP error', str(zeep_error), zeep_error)
        except requests.RequestException as e:
            raise PayFiPError('HTTP error', e)
        except Exception as e:
            raise PayFiPError('Unexpected error', e)

    def get_info_client(self, numcli, timeout=None):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/reponse}RecupererDetailClientRequest',
            'recupererDetailClient',
            timeout=timeout,
            numCli=numcli,
        )

    def get_idop(
        self,
        numcli,
        saisie,
        exer,
        refdet,
        montant,
        mel,
        url_notification,
        url_redirect,
        objet=None,
        timeout=None,
    ):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/requete}CreerPaiementSecuriseRequest',
            'creerPaiementSecurise',
            numcli=numcli,
            saisie=saisie,
            exer=exer,
            montant=montant,
            refdet=refdet,
            mel=mel,
            urlnotif=url_notification,
            urlredirect=url_redirect,
            objet=objet,
            timeout=timeout,
        )

    def get_info_paiement(self, idop, timeout=None):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/reponse}RecupererDetailPaiementSecuriseRequest',
            'recupererDetailPaiementSecurise',
            idOp=idop,
            timeout=timeout,
        )


class Payment(PaymentCommon):
    """Produce requests for and verify response from the TIPI online payment
    processor from the French Finance Ministry.

    """

    description = {
        'caption': 'TIPI, Titres Payables par Internet',
        'parameters': [
            {
                'name': 'numcli',
                'caption': _('Client number'),
                'help_text': _('6 digits number provided by DGFIP'),
                'validation': lambda s: str.isdigit(s) and len(s) == 6,
                'required': True,
            },
            {
                'name': 'saisie',
                'caption': _('Payment type'),
                'default': 'T',
                'choices': [
                    ('T', _('test')),
                    ('X', _('activation')),
                    ('W', _('production')),
                ],
            },
            {
                'name': 'normal_return_url',
                'caption': _('User return URL'),
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Asynchronous return URL'),
                'required': True,
            },
        ],
    }

    min_time_between_transactions = 60 * 20  # 20 minutes

    minimal_amount = decimal.Decimal('1.0')
    maximal_amount = decimal.Decimal('100000.0')

    email_is_required = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payfip = PayFiP()

    def _generate_refdet(self):
        return '%s%010d' % (isonow(), random.randint(1, 1000000000))

    def request(
        self,
        amount,
        email,
        refdet=None,
        exer=None,
        orderid=None,
        subject=None,
        transaction_id=None,
        timeout=None,
        **kwargs,
    ):
        montant = self.clean_amount(amount, max_amount=100000)

        numcli = self.numcli
        urlnotif = self.automatic_return_url
        urlredirect = self.normal_return_url

        if not exer:
            exer = str(datetime.date.today().year)

        if refdet:
            pass
        elif transaction_id and REFDET_RE.match(transaction_id):
            refdet = transaction_id
        elif orderid and REFDET_RE.match(orderid):
            refdet = orderid
        else:
            refdet = self._generate_refdet()

        objet_parts = []
        if orderid and refdet != orderid:
            objet_parts.extend(['O', orderid])
        if subject:
            if objet_parts:
                objet_parts.append('S')
            objet_parts.append(subject)
        if transaction_id and refdet != transaction_id:
            objet_parts.extend(['T', transaction_id])
        objet = normalize_objet(' '.join(objet_parts))

        mel = email
        if hasattr(mel, 'decode'):
            mel = email.decode('ascii')
        try:
            if '@' not in mel:
                raise ValueError('no @ in MEL')
            if not (6 <= len(mel) <= 80):
                raise ValueError('len(MEL) is invalid, must be between 6 and 80')
        except Exception as e:
            raise ValueError('MEL is not a valid email, %r' % mel, e)

        # check saisie
        saisie = self.saisie
        if saisie not in ('T', 'X', 'W'):
            raise ValueError('SAISIE invalid format, %r, must be M, T, X or A' % saisie)

        idop = self.payfip.get_idop(
            numcli=numcli,
            saisie=saisie,
            exer=exer,
            refdet=refdet,
            montant=montant,
            mel=mel,
            objet=objet or None,
            url_notification=urlnotif,
            url_redirect=urlredirect,
            timeout=timeout,
        )

        return str(idop), URL, PAYMENT_URL + '?idop=%s' % idop

    def payment_status(self, transaction_id, transaction_date=None, timeout=None, **kwargs):
        # idop are valid for 15 minutes after their generation
        # between generation and payment, any call to get_info_paiement() will return a PayFiPError with code=P5
        # before the end of the 15 minutes it can mean the payment is in progress
        # after the 15 minutes period it means the payment will never happen,
        # and after one day the code will change for P1, meaning the idop is
        # now unknown as it as been cleaned by the night cleaning job.
        #
        # So in order to interpret the meaning of PayFiP error codes we need
        # the date of the start of the transaction and add to it some margin
        # to.
        idop = transaction_id
        if transaction_date:
            if transaction_date.tzinfo:  # date is aware
                now = datetime.datetime.now(tz=pytz.utc)
            else:
                now = datetime.datetime.now()
            delta = now - transaction_date
        else:
            delta = datetime.timedelta(seconds=0)
        # set the threshold between transaction 'in progress' and 'expired' at 20 minutes
        threshold = datetime.timedelta(seconds=20 * 60)

        try:
            response = self.payfip.get_info_paiement(idop, timeout=timeout)
        except PayFiPError as e:
            if e.code == 'P1' or (e.code == 'P5' and delta >= threshold):
                return PaymentResponse(result=EXPIRED, signed=True, order_id=transaction_id)
            if e.code == 'P5' and delta < threshold:
                return PaymentResponse(result=WAITING, signed=True, order_id=transaction_id)
            raise e
        eopayment_response = self.payfip_response_to_eopayment_response(idop, response)
        # convert CANCELLED to WAITING during the first 20 minutes
        if eopayment_response.result == CANCELLED and delta < threshold:
            eopayment_response.result = WAITING
            eopayment_response.bank_status = (
                '%s - still waiting as idop is still active' % eopayment_response.bank_status
            )
        return eopayment_response

    def response(self, query_string, **kwargs):
        fields = parse_qs(query_string, True)
        idop = (fields.get('idop') or [None])[0]

        if not idop:
            raise ResponseError('missing idop parameter in query string')

        return self.payment_status(idop)

    @classmethod
    def payfip_response_to_eopayment_response(cls, idop, response):
        if response.resultrans == 'P':
            result = PAID
            bank_status = 'paid CB'
        elif response.resultrans == 'V':
            result = PAID
            bank_status = 'paid direct debit'
        elif response.resultrans == 'R':
            result = DENIED
            bank_status = 'refused CB'
        elif response.resultrans == 'Z':
            result = DENIED
            bank_status = 'refused direct debit'
        elif response.resultrans == 'A':
            result = CANCELLED
            bank_status = 'cancelled CB'
        else:
            result = ERROR
            bank_status = 'unknown result code: %r' % response.resultrans

        transaction_id = response.refdet
        transaction_id += ' ' + idop
        if response.numauto:
            transaction_id += ' ' + response.numauto

        return PaymentResponse(
            result=result,
            bank_status=bank_status,
            signed=True,
            bank_data={k: response[k] for k in response},
            order_id=idop,
            transaction_id=transaction_id,
            test=response.saisie == 'T',
        )

    @classmethod
    def guess(self, *, method=None, query_string=None, body=None, headers=None, backends=(), **kwargs):
        for content in [query_string, body]:
            if isinstance(content, bytes):
                try:
                    content = content.decode()
                except UnicodeDecodeError:
                    pass
            if isinstance(content, str):
                fields = parse_qs(content)
                if set(fields) == {'idOp'}:
                    return fields['idOp'][0]
        return None


if __name__ == '__main__':
    import click

    def show_payfip_error(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PayFiPError as e:
                click.echo(click.style('PayFiP ERROR : %s "%s"' % (e.code, e.message), fg='red'))

        return f

    @click.group()
    @click.option('--wsdl-url', default=None)
    @click.option('--service-url', default=None)
    @click.pass_context
    def main(ctx, wsdl_url, service_url):
        import logging

        logging.basicConfig(level=logging.INFO)
        # hide warning from zeep
        logging.getLogger('zeep.wsdl.bindings.soap').level = logging.ERROR

        ctx.obj = PayFiP(wsdl_url=wsdl_url, service_url=service_url)

    def numcli(ctx, param, value):
        if not isinstance(value, str) or len(value) != 6 or not value.isdigit():
            raise click.BadParameter('numcli must a 6 digits number')
        return value

    @main.command()
    @click.argument('numcli', callback=numcli, type=str)
    @click.pass_obj
    @show_payfip_error
    def info_client(payfip, numcli):
        response = payfip.get_info_client(numcli)
        for key in response:
            print('%15s:' % key, response[key])

    @main.command()
    @click.argument('numcli', callback=numcli, type=str)
    @click.option('--saisie', type=click.Choice(['T', 'X', 'W']), required=True)
    @click.option('--exer', type=str, required=True)
    @click.option('--montant', type=int, required=True)
    @click.option('--refdet', type=str, required=True)
    @click.option('--mel', type=str, required=True)
    @click.option('--url-notification', type=str, required=True)
    @click.option('--url-redirect', type=str, required=True)
    @click.option('--objet', default=None, type=str)
    @click.pass_obj
    @show_payfip_error
    def get_idop(payfip, numcli, saisie, exer, montant, refdet, mel, objet, url_notification, url_redirect):
        idop = payfip.get_idop(
            numcli=numcli,
            saisie=saisie,
            exer=exer,
            montant=montant,
            refdet=refdet,
            mel=mel,
            objet=objet,
            url_notification=url_notification,
            url_redirect=url_redirect,
        )
        print('idOp:', idop)
        print(PAYMENT_URL + '?idop=%s' % idop)

    @main.command()
    @click.argument('idop', type=str)
    @click.pass_obj
    @show_payfip_error
    def info_paiement(payfip, idop):
        print(payfip.get_info_paiement(idop))

    main()
