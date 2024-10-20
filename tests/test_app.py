def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['DATABASE'] == 'sqlite:///:memory:'


def test_init_dev_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_dev_db():
        Recorder.called = True

    monkeypatch.setattr('blogs_app.database.init_db', fake_init_dev_db)
    result = runner.invoke(args=['init-dev-db'])
    assert 'Initialized' in result.output
    assert Recorder.called