from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.models.bank import Bank


def test_create_account_and_balances():
    bank = Bank("Test Bank", bank_balance=1000)
    account_id = bank.create_account("alice", "pw", initial_deposit=500)
    assert account_id == "alice"
    assert bank.account_db.balances["alice"] == 500
    assert bank.get_bank_balance() == 1000


def test_deposit_and_withdraw_updates_balances_and_bank_balance():
    bank = Bank("Test Bank", bank_balance=1000)
    bank.create_account("alice", "pw", initial_deposit=500)

    assert bank.deposit("alice", 200) is True
    assert bank.account_db.balances["alice"] == 700
    assert bank.get_bank_balance() == 1200

    assert bank.withdraw("alice", 300) is True
    assert bank.account_db.balances["alice"] == 400
    assert bank.get_bank_balance() == 900

    assert bank.deposit("alice", -1) is False
    assert bank.withdraw("alice", 10000) is False


def test_transfer_between_accounts():
    bank = Bank("Test Bank", bank_balance=0)
    bank.create_account("alice", "pw", initial_deposit=500)
    bank.create_account("bob", "pw", initial_deposit=0)

    assert bank.transfer("alice", "bob", 200) is True
    assert bank.account_db.balances["alice"] == 300
    assert bank.account_db.balances["bob"] == 200

    assert bank.transfer("alice", "charlie", 100) is False
