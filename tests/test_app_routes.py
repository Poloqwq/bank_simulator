import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.routers.app import app, bank



def test_home_route_status_code():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


def test_login_authenticate_and_validate_token():
    client = app.test_client()

    # initial users user1..user5 exist with same password
    resp = client.post("/login_authenticate", data={"username": "user1", "password": "user1"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "token" in data
    token = data["token"]

    # validate token
    resp2 = client.post("/validate_token", headers={"token": token})
    assert resp2.status_code == 200
    assert resp2.get_json() == {"valid": True}


def test_get_balance_returns_formatted_value():
    client = app.test_client()

    # login to get token
    login = client.post("/login_authenticate", data={"username": "user1", "password": "user1"})
    token = login.get_json()["token"]

    resp = client.post("/get_balance", headers={"token": token})
    assert resp.status_code == 200
    data = resp.get_json()
    # initial deposit for user1 is 10000
    assert data["balance"] == "10,000"


def test_transfer_errors_and_success():
    client = app.test_client()

    # login user1
    login = client.post("/login_authenticate", data={"username": "user1", "password": "user1"})
    token = login.get_json()["token"]

    # transfer to same account -> error 400
    resp_same = client.post(
        "/transfer",
        headers={"token": token},
        data={"recipient": "user1", "amount": "100"},
    )
    assert resp_same.status_code == 400

    # transfer to not existing account -> error 400
    resp_missing = client.post(
        "/transfer",
        headers={"token": token},
        data={"recipient": "nouser", "amount": "100"},
    )
    assert resp_missing.status_code == 400

    # valid transfer to user2
    resp_ok = client.post(
        "/transfer",
        headers={"token": token},
        data={"recipient": "user2", "amount": "500"},
    )
    assert resp_ok.status_code == 200
    assert resp_ok.get_json() == {"success": True}

    # verify balances changed in model
    assert bank.account_db.balances["user1"] == 9500
    assert bank.account_db.balances["user2"] == 10500
