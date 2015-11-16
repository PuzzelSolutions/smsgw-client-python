import itcsmsgwclient
import requests
import requests_mock
import unittest

class ItcSmsGatewayTests(unittest.TestCase):
    def create_client(self):
        return itcsmsgwclient.Client("https://www.dummy-address.com", 0, "", "")

    def test_does_not_raise_exception_when_ok_gateway_response(self):
        with requests_mock.mock() as m:
            m.post("https://www.dummy-address.com/sendMessages", text="{}")

            client = self.create_client()
            try:
                response = client.send([])
            except Exception:
                self.fail()

    def test_raises_exception_when_gateway_response_indicates_error(self):
        with requests_mock.mock() as m:
            m.post("https://www.dummy-address.com/sendMessages", status_code=500)

            client = self.create_client()
            with self.assertRaises(itcsmsgwclient.GatewayError):
                response = client.send([])

if __name__ == '__main__':
    unittest.main()
