import requests
import unittest

from unittest.mock import patch, MagicMock

from ..main import MebibyteApp


class TestMebibyteApp(unittest.TestCase):
    def setUp(self):
        self.app = MebibyteApp("some-url.qwerty")

    @patch('requests.post')
    @patch('streamlit.text_input')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_run_success(
            self,
            mock_st_error,
            mock_st_success,
            mock_text_input,
            mock_request_post):
        mock_text_input.return_value = "2^30 bytes in MiB"

        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "1024 MiB"}
        mock_request_post.return_value = mock_response

        self.app.run()

        mock_request_post.assert_called_once_with(
            "some-url.qwerty",
            json={"expression": "2^30 bytes in MiB"},
        )
        mock_st_success.assert_called_once_with("1024 MiB")
        mock_st_error.assert_not_called()

    @patch('requests.post')
    @patch('streamlit.text_input')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_run_http_err(
            self,
            mock_st_error,
            mock_st_success,
            mock_text_input,
            mock_request_post):
        mock_text_input.return_value = "2^30 bytes in MiB"

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Mock HTTP Error")
        mock_response.content = """
            <h1>Mock Error</h1>
            <p>Mock error text.</p>
        """
        mock_request_post.return_value = mock_response

        self.app.run()

        mock_request_post.assert_called_once_with(
            "some-url.qwerty",
            json={"expression": "2^30 bytes in MiB"},
        )
        mock_st_success.assert_not_called()
        mock_st_error.assert_called_once_with("Mock Error: Mock error text.")

    @patch('requests.post')
    @patch('streamlit.text_input')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_run_http_err_no_message(
            self,
            mock_st_error,
            mock_st_success,
            mock_text_input,
            mock_request_post):
        mock_text_input.return_value = "2^30 bytes in MiB"

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Mock HTTP Error")
        mock_response.content = "No HTML in error response"
        mock_request_post.return_value = mock_response

        self.app.run()

        mock_request_post.assert_called_once_with(
            "some-url.qwerty",
            json={"expression": "2^30 bytes in MiB"},
        )
        mock_st_success.assert_not_called()
        mock_st_error.assert_called_once_with("Invalid expression")

    @patch('requests.post')
    @patch('streamlit.text_input')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_run_other_err(
            self,
            mock_st_error,
            mock_st_success,
            mock_text_input,
            mock_request_post):
        mock_text_input.return_value = "2^30 bytes in MiB"

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Mock HTTP Error")
        mock_response.content = None
        mock_request_post.return_value = mock_response

        self.app.run()

        mock_request_post.assert_called_once_with(
            "some-url.qwerty",
            json={"expression": "2^30 bytes in MiB"},
        )
        mock_st_success.assert_not_called()
        mock_st_error.assert_called_once_with("An error occurred :(")

    @patch('requests.post')
    @patch('streamlit.text_input')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_run_http_err_no_content(
            self,
            mock_st_error,
            mock_st_success,
            mock_text_input,
            mock_request_post):
        mock_text_input.return_value = "2^30 bytes in MiB"

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("Mock Error")
        mock_request_post.return_value = mock_response

        self.app.run()

        mock_request_post.assert_called_once_with(
            "some-url.qwerty",
            json={"expression": "2^30 bytes in MiB"},
        )
        mock_st_success.assert_not_called()
        mock_st_error.assert_called_once_with("An error occurred :(")
