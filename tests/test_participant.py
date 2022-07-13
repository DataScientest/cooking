import pytest

from cooking.db import get_db


def test_index(client, auth):
    response = client.get("/participant/")
    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/participant/")
    assert response.status_code == 200
    assert b"toto" in response.data
    assert b"toto@gmail.com" in response.data
    assert b"miam" in response.data
    assert b"1" in response.data
    assert b'href="/participant/1/update"' in response.data


@pytest.mark.skip(reason="Not implemented")
def test_index2(client, auth):
    assert True


@pytest.mark.parametrize("path", ("/participant/create", "/participant/1/update", "/participant/1/delete",
                                  "/participant/order/command/1"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize("path", ("/participant/2/update", "/participant/2/delete"))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/participant/create").status_code == 200
    response = client.post("/participant/create",
                           data={"mail": "tata@gmail.com", "name": "tata",
                                 "command_details": "pizza",
                                 "command_id": 1})
    assert response.status_code == 302
    assert response.headers["Location"] == "/participant/"

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM participant").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/participant/1/update").status_code == 200
    response = client.post("/participant/1/update",
                           data={"mail": "tata@gmail.com", "name": "tata",
                                 "command_details": "frosties",
                                 "command_id": 1})
    assert response.status_code == 302
    assert response.headers["Location"] == "/participant/"

    with app.app_context():
        db = get_db()
        participant = db.execute("SELECT * FROM participant WHERE id = 1").fetchone()
        assert participant["command_details"] == "frosties"


def test_create_update_validate(client, auth):
    auth.login()
    response = client.post("/participant/1/update",
                           data={"mail": "", "name": "tata",
                                 "command_details": "pizza",
                                 "command_id": 1})
    assert response.status_code == 200
    assert b"mail is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/participant/1/delete")
    assert response.status_code == 302
    assert response.headers["Location"] == "/participant/"

    with app.app_context():
        db = get_db()
        participant = db.execute("SELECT * FROM participant WHERE id = 1").fetchone()
        assert participant is None
