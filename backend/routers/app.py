from flask import Flask, redirect, render_template, request, url_for, jsonify
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parents[1]))

from backend.models.bank import Bank
from backend.models.utils import number_to_currency_string

# Configure Flask to serve icons from views/icons at the /icons path
app = Flask(
    __name__,
    template_folder="../../views",
    static_folder="../../views/icons",
    static_url_path="/icons"
)
bank = Bank("Polo's Bank :D", 114514000)

# Generate Initial Accounts
# accounts: user1, user2, user3, user4, user5
# Passwords are user1, user2, user3, user4, user5
for i in range(1, 6):
    bank.create_account(f"user{i}", f"user{i}", initial_deposit=10000)



@app.route('/')
def home():
    return render_template(
        'home.html',
        bank_name=bank.name,
        accounts=bank.account_db.accounts,
        db=bank.account_db
    )


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    prompt = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if bank.account_db.get_account_info(username) is not None:
            prompt = "Username already exists!"
            return render_template('create_account.html', prompt=prompt)
        if password != confirm_password:
            prompt = "Passwords do not match!"
            return render_template('create_account.html', prompt=prompt)

        initial_deposit = int(request.form['initial_deposit'] if request.form['initial_deposit'] !=  '' else 0)
        bank.create_account(username, password, initial_deposit)
        return redirect(url_for('home'))
    
    return render_template('create_account.html', prompt=prompt)


@app.route('/login', methods=['GET'])
def login(prompt=""):
    return render_template('login.html', prompt=prompt)

@app.route('/login_authenticate', methods=['POST'])
def login_authenticate():
    username = request.form['username']
    password = request.form['password']
    validation_result = bank.auth.verify_account(username, password)
    if validation_result == "Success":
        bank.auth.create_login_history(username)
        token = bank.auth.create_jwt_token(username)
        return jsonify({'token': token})
    else:
        prompt = validation_result
        return jsonify({'error': prompt}), 401

@app.route('/validate_token', methods=['POST'])
def validate_token():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    if username and bank.account_db.get_account_info(username):
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False}), 401
    
@app.route('/token_to_username', methods=['POST'])
def token_to_username():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    if username and bank.account_db.get_account_info(username):
        return jsonify({'username': username})
    else:
        return jsonify({'error': 'Invalid token'}), 401
    
@app.route('/get_balance', methods=['POST'])
def get_balance():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    if username and bank.account_db.get_account_info(username):
        balance = bank.account_db.balances.get(username, 0)
        return jsonify({'balance': number_to_currency_string(balance)})
    else:
        return jsonify({'error': 'Invalid token'}), 401
    
@app.route('/get_login_history', methods=['POST'])
def get_login_history():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    if username and bank.account_db.get_account_info(username):
        history = bank.account_db.get_account_login_history(username, 5)
        return jsonify({'login_history': history})
    else:
        return jsonify({'error': 'Invalid token'}), 401
    
@app.route('/user_home', methods=['GET'])
def user_home():
    return render_template(
            'user_home.html',
            accounts=bank.account_db.accounts,
            db=bank.account_db
        ) 

@app.route('/deposit_page', methods=['GET'])
def deposit_page():
    return render_template('deposit.html')

@app.route('/withdraw_page', methods=['GET'])
def withdraw_page():
    return render_template('withdraw.html')

@app.route('/transfer_page', methods=['GET'])
def transfer_page():
    return render_template('transfer.html')


# TODO: Implement deposit feature
@app.route('/deposit', methods=['POST'])
def deposit():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    deposit_amount = request.form['amount']
    if(username and bank.account_db.get_account_info(username)):
        # Implement deposit logic here
        bank.deposit(username, int(deposit_amount))
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid token'}), 401


# TODO: Implement withdraw feature
@app.route('/withdraw', methods=['POST'])
def withdraw():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    withdraw_amount = int(request.form['amount'])
    
    if(username and bank.account_db.get_account_info(username)):
        if(withdraw_amount > bank.account_db.balances.get(username, 0)):
            return jsonify({'error': 'Insufficient funds'}), 400
        
        # Implement withdraw logic here

        bank.withdraw(username, int(withdraw_amount))
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid token'}), 401
    

# TODO: Implement transfer feature
@app.route('/transfer', methods=['POST'])
def transfer():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    target_account = request.form['recipient']
    transfer_amount = int(request.form['amount'])
    if(target_account and not bank.account_db.get_account_info(target_account)):
        return jsonify({'error': 'Recipient account does not exist'}), 400
    if(username == target_account):
        return jsonify({'error': 'Cannot transfer to the same account'}), 400
    if(transfer_amount > bank.account_db.balances.get(username, 0)):
        return jsonify({'error': 'Insufficient funds'}), 400
    
    if(username and bank.account_db.get_account_info(username)):
        # Implement transfer logic here
        bank.transfer(username, target_account, int(transfer_amount))
        bank.auth.create_transfer_history(username, target_account, transfer_amount)
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid token'}), 401

# TODO: Implement transaction history feature
@app.route('/get_transaction_history', methods=['POST'])
def get_transaction_history():
    token = request.headers.get('token')
    username = bank.auth.decode_jwt_token(token)
    if username and bank.account_db.get_account_info(username):
        history = bank.account_db.get_account_transfer_history(username, 5)
        return jsonify({'transaction_history': history})
    else:
        return jsonify({'error': 'Invalid token'}), 401






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)