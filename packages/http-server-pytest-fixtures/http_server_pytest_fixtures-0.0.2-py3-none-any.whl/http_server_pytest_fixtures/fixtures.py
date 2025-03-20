from contextlib import contextmanager
from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import chdir, environ
import logging
import queue
from multiprocessing import Process, Queue
import shutil
import tempfile

from pytest import fixture
import requests
from requests.adapters import HTTPAdapter


L = logging.getLogger(__name__)


class ServerData:
    def __init__(self, request_queue):
        self.server = None
        self.requests = request_queue
        self.scheme = 'http'

    def headers(self, handler):
        return {}

    @property
    def requests_list(self):
        res = []
        while True:
            try:
                res.append(self.requests.get_nowait())
            except queue.Empty:
                break
        return res

    @property
    def url(self):
        return self.scheme + '://{}:{}'.format(*self.server.server_address)

    def make_server(self, handler_func):
        self.server = make_server(self, handler=handler_func and handler_func(self))

    @property
    def basic_handler(self):
        return basic_handler(self)

    def trust_server(self, session):
        if hasattr(self, 'ssl_context'):
            session.mount(self.url, _https_server_adapter(self.ssl_context))


@contextmanager
def _http_server(handler_func=None):
    '''
    Creates an http server.

    Some behaviors can be affected by changing the server data. The server must be
    restarted in that case. The requests queue is not cleared on a restart
    '''
    srvdir = tempfile.mkdtemp(prefix=__name__ + '.')
    process = None
    request_queue = Queue()
    try:
        server_data = ServerData(request_queue)
        server = make_server(server_data,
                handler=handler_func and handler_func(server_data))
        server_data.server = server
        server_data.base_directory = srvdir

        def pfunc():
            chdir(srvdir)
            server_data.server.serve_forever()

        process = Process(target=pfunc)

        def start():
            process.start()
            wait_for_started(server_data)

        def restart():
            nonlocal process
            if process:
                process.terminate()
                process.join()
            process = Process(target=pfunc)
            process.start()
            wait_for_started(server_data)

        server_data.start = start
        server_data.restart = restart
        yield server_data
    finally:
        if process:
            process.terminate()
            process.join()
        shutil.rmtree(srvdir)


@fixture
def https_server():
    with _http_server() as server_data:
        _sslify(server_data)
        server_data.start()
        old_restart = server_data.restart

        def restart():
            _sslify(server_data)
            old_restart()
        server_data.restart = restart
        yield server_data


def _sslify(server_data):
    import ssl
    try:
        cert_path = environ['HTTPS_PYTEST_FIXTURES_CERT']
        cert_key = environ['HTTPS_PYTEST_FIXTURES_KEY']
    except KeyError:
        raise Exception('Environment variables HTTPS_PYTEST_FIXTURES_CERT and'
                ' HTTPS_PYTEST_FIXTURES_KEY must be defined for https_server')

    server_data.server_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_data.server.socket = \
        server_data.server_ssl_context.wrap_socket(server_data.server.socket,
                        server_side=True)
    server_data.server_ssl_context.load_cert_chain(certfile=cert_path,
                                            keyfile=cert_key)
    server_data.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    server_data.ssl_context.load_verify_locations(cert_path)
    server_data.ssl_context.check_hostname = False
    server_data.scheme = 'https'


@fixture
def http_server():
    with _http_server() as server_data:
        server_data.start()
        yield server_data


def make_server(server_data, handler=None):
    if not handler:
        class _Handler(basic_handler(server_data)):
            def do_POST(self):
                self.handle_request(201)
        handler = _Handler

    port = 8000
    while True:
        try:
            L.debug("Attempting to start on port %d", port)
            server = HTTPServer(('localhost', port), handler)
            L.debug("Started on port %d", port)
            break
        except OSError as e:
            L.debug("Failed to start on port %d", port, exc_info=True)
            if e.errno != 98:
                raise
            port += 1

    return server


def basic_handler(server_data):
    class _Handler(SimpleHTTPRequestHandler):
        def queue_reuqest(self):
            server_data.requests.put(dict(
                method=self.command,
                path=self.path,
                headers={k.lower(): v for k, v in self.headers.items()}))

        def end_headers(self):
            for header, value in server_data.headers(self).items():
                self.send_header(header, value)
            super().end_headers()

        def handle_request(self, code):
            self.queue_reuqest()
            self.send_response(code)
            self.end_headers()

    return _Handler


def wait_for_started(server_data, max_tries=10):
    done = False
    tries = 0
    session = requests.Session()
    server_data.trust_server(session)
    while not done and tries < max_tries:
        tries += 1
        try:
            session.head(server_data.url)
            done = True
        except Exception:
            L.info("Unable to connect to the server. Trying again...", exc_info=True)
    if not done:
        raise Exception('Failed to connect to the server.')


class _https_server_adapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def __init__(self, ssl_context):
        self.__ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.__ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.__ssl_context
        return super().proxy_manager_for(*args, **kwargs)
