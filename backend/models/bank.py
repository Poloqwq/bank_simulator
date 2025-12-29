from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))



from account_db import AccountDB
from auth import Authenticate


class Bank:

    def __init__(self, name, bank_balance=0):
        self.name = name
        self.bank_balance = bank_balance
        self.account_db = AccountDB()
        self.auth = Authenticate(self.account_db)
    
    
    def create_account(self, account_id, password, initial_deposit=0) -> str:
        self.account_db.add_account(account_id, password, initial_deposit)
        return account_id

    
    
    def get_bank_balance(self) -> int:
        return self.bank_balance
    
    
    def deposit(self, account_id, amount) -> bool:
        if amount > 0:
            self.account_db.balances[account_id] = self.account_db.balances.get(account_id, 0) + amount
            self.bank_balance += amount
            return True
        return False

    def withdraw(self, account_id, amount) -> bool:
        if 0 < amount <= self.account_db.balances.get(account_id):
            self.account_db.balances[account_id] -= amount
            self.bank_balance -= amount
            return True
        return False

    def transfer(self, from_account_id, to_account_id, amount) -> bool:
        if (0 < amount <= self.account_db.balances.get(from_account_id)
                and to_account_id in self.account_db.accounts):
            self.account_db.balances[from_account_id] -= amount
            self.account_db.balances[to_account_id] += amount
            return True
        return False