
class AccountDB:
    def __init__(self):
        self.accounts = {}
        self.balances = {}
        self.login_history = {}
        self.transfer_history = {}

    def add_account(self, account_id, account_data, initial_balance=0) -> None:
        self.accounts[account_id] = account_data
        self.balances[account_id] = initial_balance
        self.login_history[account_id] = []
        self.transfer_history[account_id] = []

    def add_login_history(self, account_id, message) -> None:
        self.login_history[account_id].append(message)

    def add_transfer_history(self, account_id, message) -> None:
        self.transfer_history[account_id].append(message)

    def get_account_info(self, account_id) -> str:
        return self.accounts.get(account_id)

    def get_account_balance(self, account_id) -> str:
        return f"{self.balances.get(account_id):,}"
    
    def get_account_login_history(self, account_id, amount: int = -1) -> list:
        if amount == -1:
            return self.login_history.get(account_id, [])
        else:
            return self.login_history.get(account_id, [])[-amount:]
        
    def get_account_transfer_history(self, account_id, amount: int = -1) -> list:
        if amount == -1:
            return self.transfer_history.get(account_id, [])
        else:
            return self.transfer_history.get(account_id, [])[-amount:]  
    
    def delete_account(self, account_id) -> None:
        if account_id in self.accounts:
            del self.accounts[account_id]
            del self.balances[account_id]
            del self.login_history[account_id]
            del self.transfer_history[account_id]

    
        