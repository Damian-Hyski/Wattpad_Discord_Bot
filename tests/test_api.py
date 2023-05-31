import pytest
from unittest import mock
from api import WattpadAPI


class TestWattpadAPI:
    @pytest.mark.parametrize('status_code, expected_data', [
        (200, {'username': 'JohnDoe'}),
        (404, None),
    ])
    def test_get_user_data(self, status_code, expected_data):
        api = WattpadAPI()

        mock_response = mock.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = expected_data

        with mock.patch('requests.request', return_value=mock_response):
            data = api.get_user_data('johndoe')

        assert data == expected_data

    @pytest.mark.parametrize('status_code, expected_data', [
        (200, {'story_id': 123}),
        (500, None),
    ])
    def test_get_stories_data(self, status_code, expected_data):
        api = WattpadAPI()

        mock_response = mock.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = expected_data

        with mock.patch('requests.request', return_value=mock_response):
            data = api.get_stories_data('johndoe')

        assert data == expected_data

    @pytest.mark.parametrize('status_code, expected_data', [
        (200, {'message_id': 456}),
        (403, None),
    ])
    def test_get_message_data(self, status_code, expected_data):
        api = WattpadAPI()

        mock_response = mock.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = expected_data

        with mock.patch('requests.request', return_value=mock_response):
            data = api.get_message_data('johndoe')

        assert data == expected_data
