import unittest

from flask import Flask
from flask.testing import FlaskClient

from ..service import MebibyteService


class TestMebibyteService(unittest.TestCase):
    service: MebibyteService
    client: FlaskClient

    def setUp(self) -> None:
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.service = MebibyteService(app=app, debug=True)
        self.client = app.test_client()

    def test_expression(self):
        response = self.client.post('/expression', json={'expression': '4 mib + 2 mib in kib'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"result":"6144 kib"}\n', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '10 eib in bytes'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"result":"11529215046068469760 bytes"}\n', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib * 2 in gib'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"result":"0.0078125 gib"}\n', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib / 2 gib'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"result":"0.001953125"}\n', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib + 2'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot add operands with different units', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib + badtoken'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('is not a valid token', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib + 2 in badunit'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('is not a valid unit', response.get_data(as_text=True))

        response = self.client.post('/expression', json={'expression': '4 mib + 2 in kib in gib'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Expression has multiple &#39;in&#39; directives", response.get_data(as_text=True))

        response = self.client.get('/expression')
        self.assertEqual(response.status_code, 405)
        self.assertIn("Method Not Allowed", response.get_data(as_text=True))

        response = self.client.post('/expression')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bad Request", response.get_data(as_text=True))

        response = self.client.post('/expression', json={'invalid': '4 mib + 2 in kib in gib'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bad Request", response.get_data(as_text=True))