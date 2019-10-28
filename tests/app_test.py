import pytest
import requests
#
# def test_url(requests_mock):
#     requests_mock.get('http://127.0.0.1:5000/', text='data')
#     assert 'dataaa' == requests.get('http://127.0.0.1:5000/').text

#test_home()

def test_url():
    url = 'http://127.0.0.1:5000/register'
    resp = requests.get(url)
    assert resp.status_code == 200
