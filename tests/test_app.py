import pytest


def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['DATABASE'] == 'sqlite:///:memory:'


@pytest.mark.parametrize('route', ['/api/tweets/', '/api/users/1'])
def test_get_route_status(web_client, route):
    result = web_client.get(route)
    assert result.status_code == 200
