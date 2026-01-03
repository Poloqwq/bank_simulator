from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.models.account_db import AccountDB
from backend.models.auth import Authenticate


def test_verify_account():
    db = AccountDB()
    db.add_account("user1", "pass1", initial_balance=0)
    auth = Authenticate(db)

    assert auth.verify_account("user1", "pass1") == "Success"
    assert auth.verify_account("user1", "wrong") == "Invalid password"
    assert auth.verify_account("nouser", "pass1") == "Account does not exist"


def test_jwt_encode_decode_and_login_history():
    db = AccountDB()
    db.add_account("user1", "pass1", initial_balance=0)
    auth = Authenticate(db)

    token = auth.create_jwt_token("user1")
    assert isinstance(token, str)
    username = auth.decode_jwt_token(token)
    assert username == "user1"

    auth.create_login_history("user1")
    history = db.get_account_login_history("user1")
    assert len(history) >= 1
    assert "logged in" in history[0]


def test_transfer_history_both_sides():
    db = AccountDB()
    db.add_account("alice", "pw", initial_balance=0)
    db.add_account("bob", "pw", initial_balance=0)
    auth = Authenticate(db)

    auth.create_transfer_history("alice", "bob", 100)
    sender_hist = db.get_account_transfer_history("alice")
    recv_hist = db.get_account_transfer_history("bob")
    assert len(sender_hist) == 1
    assert len(recv_hist) == 1
    assert "Sent $100 to account bob" in sender_hist[0]
    assert "Received $100 from account alice" in recv_hist[0]
