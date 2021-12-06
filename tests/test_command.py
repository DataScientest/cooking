import pytest

from cooking.db import get_db


def test_index(client, auth):
    response = client.get("/command/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/command/")
    assert b"test restaurant" in response.data
    assert b"test menu" in response.data
    assert b"Command_day" in response.data
    assert b"test\ncommand_hour" in response.data
    assert b'href="/command/1/update"' in response.data


@pytest.mark.parametrize("path", ("/command/create", "/command/1/update", "/command//1/delete"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


@pytest.mark.parametrize("path", ("/command/2/update", "/command/2/delete"))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/command/create").status_code == 200
    client.post("/command/create",
                data={"restaurant": "restaurant created", "menu": "menu created", "Command_day": "2021-11-09",
                      "command_hour": "12:12"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM command").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/command/1/update").status_code == 200
    client.post("/command/1/update",
                data={"restaurant": "restaurant updated", "menu": "menu created", "Command_day": "2021-11-09",
                      "command_hour": "12:12"})

    with app.app_context():
        db = get_db()
        command = db.execute("SELECT * FROM command WHERE id = 1").fetchone()
        assert command["restaurant"] == "restaurant updated"


@pytest.mark.parametrize("path", ("/command/create", "/command/1/update"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"restaurant": "", "menu": "menu", "Command_day": "2021-11-09",
                                       "command_hour": "12:12"})
    assert b"Restaurant is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/command/1/delete")
    assert response.headers["Location"] == "http://localhost/command/"

    with app.app_context():
        db = get_db()
        command = db.execute("SELECT * FROM command WHERE id = 1").fetchone()
        assert command is None
