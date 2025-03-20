import pytest
from luzitool import api


def test_get_user_data():
    user_data = api.get_user_data('test_user')
    assert user_data is not None
    assert 'username' in user_data
    assert user_data['username'] == 'test_user'


def test_get_user_data_invalid():
    with pytest.raises(ValueError):
        api.get_user_data('invalid_user')


def test_api_status_code():
    response = api.make_api_call()
    assert response.status_code == 200
