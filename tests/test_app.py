import pytest


def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['DATABASE'] == 'sqlite:///:memory:'


@pytest.mark.parametrize('route', ['/api/tweets/', '/api/users/1'])
def test_get_route_status(web_client, route):
    result = web_client.get(route)
    assert result.status_code == 200


def test_init_dev_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_dev_db():
        Recorder.called = True

    monkeypatch.setattr('blogs_app.database.init_db', fake_init_dev_db)
    result = runner.invoke(args=['init-dev-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


# def test_create_tweet(create_user, web_client):
#     web_client.post(hea)
