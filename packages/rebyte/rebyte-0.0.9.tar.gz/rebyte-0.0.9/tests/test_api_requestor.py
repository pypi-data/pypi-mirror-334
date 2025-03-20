import unittest
from unittest.mock import patch, MagicMock
from rebyte.api_requestor import RebyteAPIRequestor, RebyteResponse

class TestRebyteAPIRequestor(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.api_base = "https://rebyte.ai"
        self.requestor = RebyteAPIRequestor(key=self.api_key, api_base=self.api_base)

    @patch('rebyte.api_requestor.requests.Session')
    def test_make_session(self, MockSession):
        session = self.requestor._make_session()
        self.assertIsInstance(session, MockSession)

    @patch('rebyte.api_requestor.requests.Session.request')
    def test_request_raw(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_request.return_value = mock_response

        method = "get"
        url = "/test"
        response = self.requestor.request_raw(method, url)
        self.assertEqual(response.status_code, 200)

    @patch('rebyte.api_requestor.aiohttp.ClientSession')
    @patch('rebyte.api_requestor.aiohttp_session')
    async def test_arequest_raw(self, mock_aiohttp_session, MockClientSession):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"data": "test"}'
        mock_aiohttp_session.return_value.__aenter__.return_value = MockClientSession
        MockClientSession.request.return_value = mock_response

        method = "get"
        url = "/test"
        response = await self.requestor.arequest_raw(method, url, MockClientSession)
        self.assertEqual(response.status, 200)

    @patch('rebyte.api_requestor.RebyteAPIRequestor.request')
    def test_poll(self, mock_request):
        mock_response = MagicMock()
        mock_response.retry_after = 1
        mock_request.return_value = (mock_response, False, self.api_key)

        def until(response):
            return True

        def failed(response):
            return False

        response, b, api_key = self.requestor._poll("get", "/test", until, failed)
        self.assertEqual(api_key, self.api_key)

    @patch('rebyte.api_requestor.RebyteAPIRequestor.arequest')
    async def test_apoll(self, mock_arequest):
        mock_response = MagicMock()
        mock_response.retry_after = 1
        mock_arequest.return_value = (mock_response, False, self.api_key)

        def until(response):
            return True

        def failed(response):
            return False

        response, b, api_key = await self.requestor._apoll("get", "/test", until, failed)
        self.assertEqual(api_key, self.api_key)

if __name__ == '__main__':
    unittest.main()
