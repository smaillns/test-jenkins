import json

import pytest


@pytest.fixture
def new_installation_request(web_session):
    response = web_session.post(
        "/installation-requests",
        data=json.dumps(
            {
                "user_id": 1,
                "status": "NEW",
                "budget": "1000",
                "equipment_type": "SOLAR",
                "equipment_brand": "brand",
                "equipment_model": "",
                "comment": "comment",
            }
        ),
    )
    return response


def test_insert_installation_request(web_session, create_svc):
    response = web_session.post(
        "/installation-requests",
        data=json.dumps(
            {
                "user_id": 1,
                "status": "NEW",
                "budget": "1000",
                "equipment_type": "SOLAR",
                "equipment_brand": "brand",
                "equipment_model": "",
                "comment": "comment",
            }
        ),
    )
    assert response.status_code == 200
    assert response.json()["id"] > 0


def test_get_installation_request(web_session, create_svc, new_installation_request):
    resp = web_session.get(
        "/installation-requests/{}".format(new_installation_request.json()["id"])
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == new_installation_request.json()["id"]


def test_delete_installation_request(web_session, create_svc, new_installation_request):
    resp = web_session.delete(
        "/installation-requests/{}".format(new_installation_request.json()["id"])
    )
    assert resp.status_code == 204


def test_update_installation_request(web_session, create_svc, new_installation_request):
    resp = web_session.put(
        "/installation-requests/{}".format(new_installation_request.json()["id"]),
        data=json.dumps({"status": "CLOSED", "comment": "comment"}),
    )
    assert resp.status_code == 200


# -------------------
# non-happy flow
# -------------------


def test_when_installation_request_not_found(web_session, create_svc):
    response = web_session.get("/installation-requests/9999999999999")
    assert response.status_code == 404


def test_create_installation_request_fails_with_invalid_json(web_session, create_svc):
    response = web_session.post(
        "/installation-requests", data=json.dumps({"user_id": 1, "status": "NEW"})
    )
    assert response.status_code == 400


# @todo
#    - get Installation Requests by user_id
#    - update Installation Request status
