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

import json

import httmock
import lxml.etree as ET
import pytest
import responses
from requests import Session
from requests.adapters import HTTPAdapter


def pytest_addoption(parser):
    parser.addoption('--save-http-session', action='store_true', help='save HTTP session')
    parser.addoption('--target-url', help='target URL')

    def keyvalue(value):
        key, value = value.split('=', 1)
        return [key, value]

    parser.addoption(
        '--backend-param', help='add key=value param for backend', type=keyvalue, action='append'
    )


@pytest.fixture
def backend_params(pytestconfig):
    return dict(pytestconfig.getoption('--backend-param') or [])


class LoggingAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.history = []
        super().__init__(*args, **kwargs)

    def send(self, request, *args, **kwargs):
        response = super().send(request, *args, **kwargs)
        self.history.append((request, response))
        return response


def xmlindent(content):
    if hasattr(content, 'encode') or hasattr(content, 'decode'):
        content = ET.fromstring(content)
    return ET.tostring(content, pretty_print=True).decode('utf-8', 'ignore')


@pytest.fixture
def record_http_session(request):
    module_name = request.module.__name__.split('test_', 1)[-1]
    function_name = request.function.__name__
    save = request.config.getoption('--save-http-session')
    filename = 'tests/data/%s-%s.json' % (module_name, function_name)

    def is_xml_content_type(r):
        headers = r.headers
        content_type = headers.get('content-type')
        return content_type and content_type.startswith(('text/xml', 'application/xml'))

    if save:
        session = Session()
        adapter = LoggingAdapter()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        try:
            yield session
        finally:
            with open(filename, 'w') as fd:
                history = []

                for request, response in adapter.history:
                    request_content = request.body or b''
                    response_content = response.content or b''

                    if is_xml_content_type(request):
                        request_content = xmlindent(request_content)
                    else:
                        request_content = request_content.decode('utf-8')
                    if is_xml_content_type(response):
                        response_content = xmlindent(response_content)
                    else:
                        response_content = response_content.decode('utf-8')
                    history.append((request_content, response_content))
                json.dump(history, fd)
    else:
        with open(filename) as fd:
            history = json.load(fd)

        class Mocker:
            counter = 0
            requests = None

            @httmock.urlmatch()
            def mock(self, url, request):
                self.requests = self.requests or []
                self.requests.append(request)
                expected_request_content, response_content = history[self.counter]
                self.counter += 1
                if expected_request_content:
                    request_content = request.body or b''
                    if is_xml_content_type(request):
                        request_content = xmlindent(request_content)
                    else:
                        request_content = request_content.decode('utf-8')
                    assert request_content == expected_request_content
                return response_content

        mocker = Mocker()
        with httmock.HTTMock(mocker.mock):
            yield mocker


@pytest.fixture
def target_url(request):
    return request.config.getoption('--target-url') or 'https://target.url/'


@pytest.fixture
def rsps():
    with responses.RequestsMock() as rsps:
        yield rsps
