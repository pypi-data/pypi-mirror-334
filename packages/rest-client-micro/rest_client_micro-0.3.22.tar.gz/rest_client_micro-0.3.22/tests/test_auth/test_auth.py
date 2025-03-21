from src.rest_client_micro import RESTClient as rc, RESTObject as ro, BasicAuth as ba


def test_successful_auth():
    rest_object = ro()
    rest_object.endpoint = 'http://localhost:3876/auth'
    rest_object.params = ''
    rest_object.basic_auth = ba('user', 'secretpass')
    rest_client = rc()
    rc.DEBUG = True
    result = rest_client.execute(config=rest_object)
    assert result.status is 200
    assert result.error is False
    assert result.response.startswith('')


def test_failed_auth():
    rest_object = ro()
    rest_object.endpoint = 'http://localhost:3876/auth'
    rest_object.params = ''
    rest_object.basic_auth = ba('user2', 'secretpass2')
    rest_client = rc()
    rc.DEBUG = True
    result = rest_client.execute(config=rest_object)
    assert result.status == 401
    assert result.response == 'Unauthorized Access'
    assert result.error is False
