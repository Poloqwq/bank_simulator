from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from account_db import AccountDB
from jose import jwt, JWTError
from datetime import datetime


JWT_SECRET_KEY = "1892dhianiandowqd0n"

class Authenticate():
    def __init__(self, db: AccountDB):
        self.db = db

    def verify_account(self, account_id, password) -> str:
        account_info = self.db.get_account_info(account_id)
        if account_info == None:
            return "Account does not exist"
        if(account_info != password):
            return "Invalid password"
        return "Success"
    
    def create_jwt_token(self, account_id) -> str:
        payload = {"account_id": account_id}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return token
    
    def decode_jwt_token(self, token) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            username = payload.get("account_id")
            return username
        except JWTError:
            return None

    def create_login_msg(self, timestamp) -> str:
        return f"{timestamp} : An user has logged in this account."
    
    def create_login_history(self, account_id) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = self.create_login_msg(timestamp)
        if(self.db.get_account_info(account_id) is not None):
            self.db.add_login_history(account_id, message)
    
    
    
    def create_transfer_sender_msg(self, timestamp, to_account, amount) -> str:
        return f"{timestamp} : Sent ${amount} to account {to_account}."
    
    def create_transfer_receiver_msg(self, timestamp, from_account, amount) -> str:
        return f"{timestamp} : Received ${amount} from account {from_account}."
    
    def create_transfer_history(self, from_account, to_account, amount) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if(self.db.get_account_info(from_account) is None or self.db.get_account_info(to_account) is None):
            return
        if(self.db.get_account_info(from_account) is not None):
            sender_msg = self.create_transfer_sender_msg(timestamp, to_account, amount)
            self.db.add_transfer_history(from_account, sender_msg)
        if(self.db.get_account_info(to_account) is not None):
            receiver_msg = self.create_transfer_receiver_msg(timestamp, from_account, amount)
            self.db.add_transfer_history(to_account, receiver_msg)