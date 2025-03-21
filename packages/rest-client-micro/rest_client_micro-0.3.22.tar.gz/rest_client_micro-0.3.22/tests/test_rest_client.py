"""Test cases for RESTClient"""
from src.rest_client_micro.rest_client import RESTClient as rc
from src.rest_client_micro.rest_object import RESTObject as ro

def test_missing_config():
    rest_client = rc()
    result = rest_client.execute()
    assert result.error is True
    assert result.error_text == "RESTObject config not provided"

def test_client():
    rest_object = ro()
    rest_object.endpoint = 'http://localhost:3876/'
    rest_object.params = ''
    rest_client = rc()
    rc.DEBUG = True
    result = rest_client.execute(config=rest_object)
    assert result.status is 200
    assert result.error is False
    assert result.response.startswith('')
