from config import AppConfig
import json

users_mock = [
    {"name": "Banana", "email": "banana@gmail.com"},
    {"name": "Maça", "email": "maça@gmail.com"},
    {"name": "Gabriel", "email": "gsferreira.dev@gmail.com"},
    {"name": "Abacate", "email": "abacate@gmail.com"},
]

default_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {AppConfig.auth_token}"}
url = f"{AppConfig.app_prefix}/user"


def test_insert_user(client):
    for user in users_mock:
        response = client.post(url=url, headers=default_headers, content=json.dumps(user))
        assert response.status_code == 201


def test_get_user(client):
    response = client.get(url=url, headers=default_headers)

    result = response.json()
    mock_emails = {u["email"] for u in users_mock}
    result_emails = {u["email"] for u in result["data"]}

    assert response.status_code == 200
    assert len(result["data"]) == len(users_mock)
    assert mock_emails == result_emails
    assert len(result_emails) > 0


def test_update_user(client):
    response = client.get(url, headers=default_headers, params={"email": "gsferreira.dev@gmail.com"})

    assert response.status_code == 200
    id = response.json().get("data")[0].get("id")
    assert id is not None

    updated_user = {"id": id, "name": "NOVO", "email": "novo@novo.com"}

    response = client.patch(url, headers=default_headers, content=json.dumps(updated_user))
    assert response.status_code == 200

    url_get = f"{AppConfig.app_prefix}/user?email={updated_user['email']}"
    response = client.get(url_get, headers=default_headers)

    assert response.status_code == 200
    response_data = response.json()["data"]

    assert len(response_data) == 1
    response_data = response_data[0]

    assert response_data["email"] == updated_user["email"]
    assert response_data["name"] == updated_user["name"]


def test_delete_user(client):
    response = client.get(url, headers=default_headers, params={"email": "banana@gmail.com"})

    assert response.status_code == 200
    id = response.json().get("data")[0].get("id")
    print(id)
    print(id)
    print(id)
    print(id)
    assert id is not None

    response = client.delete(url, headers=default_headers, params={"id": id})
    print(response)
    assert response.status_code == 200

    response = client.get(url, headers=default_headers, params={"id": id})

    assert response.status_code == 204
