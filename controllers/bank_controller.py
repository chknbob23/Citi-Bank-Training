from flask import Blueprint, request
from models.bank_model import db
from views.bank_view import BankView

bank_blueprint = Blueprint('bank', __name__)

@bank_blueprint.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json() or {}
    name = data.get('account_holder', '').strip()
    
    try:
        initial_deposit = float(data.get('initial_balance', 0))
    except (ValueError, TypeError):
        return BankView.render_error("Invalid initial balance format.")

    account, msg = db.create_account(name, initial_deposit)
    if not account:
        return BankView.render_error(msg)
        
    return BankView.render_success(BankView.render_account(account), msg, 201)

@bank_blueprint.route('/accounts/<account_number>', methods=['GET'])
def get_account_details(account_number):
    account = db.get_account(account_number)
    if not account:
        return BankView.render_error("Account number not found.", 404)
    return BankView.render_success(BankView.render_account(account))

@bank_blueprint.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    account = db.get_account(account_number)
    if not account:
        return BankView.render_error("Account number not found.", 404)

    data = request.get_json() or {}
    try:
        amount = float(data.get('amount', 0))
    except (ValueError, TypeError):
        return BankView.render_error("Invalid amount format.")

    success, msg = account.deposit(amount)
    if not success:
        return BankView.render_error(msg)

    return BankView.render_success(BankView.render_account(account), msg)

@bank_blueprint.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    account = db.get_account(account_number)
    if not account:
        return BankView.render_error("Account number not found.", 404)

    data = request.get_json() or {}
    try:
        amount = float(data.get('amount', 0))
    except (ValueError, TypeError):
        return BankView.render_error("Invalid amount format.")

    success, msg = account.withdraw(amount)
    if not success:
        return BankView.render_error(msg)

    return BankView.render_success(BankView.render_account(account), msg)

@bank_blueprint.route('/accounts/<account_number>/history', methods=['GET'])
def get_history(account_number):
    account = db.get_account(account_number)
    if not account:
        return BankView.render_error("Account number not found.", 404)
    return BankView.render_success(BankView.render_history(account))
