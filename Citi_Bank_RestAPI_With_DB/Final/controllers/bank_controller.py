from flask import Blueprint, request, jsonify
from models.bank_model import BankSystem
from views.bank_view import BankView

bank_blueprint = Blueprint('bank', __name__)

@bank_blueprint.route('/customers', methods=['POST'])
def post_customer():
    data = request.get_json() or {}
    name = data.get('userName', '').strip()
    email = data.get('email', '').strip()
    try: 
        initial_balance = float(data.get('balance', 0))
    except (ValueError, TypeError): 
        return BankView.render_error("Invalid balance format.")

    customer, msg = BankSystem.create_customer(name, email, initial_balance)
    if not customer: return BankView.render_error(msg)
    return BankView.render_success(BankView.render_customer(customer), msg, 201)

@bank_blueprint.route('/customers', methods=['GET'])
def get_all_customers():
    return BankView.render_success([BankView.render_customer(c) for c in BankSystem.get_all_customers()])

@bank_blueprint.route('/customers/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):

    customer = BankSystem.get_customer_by_id(customer_id)

    if not customer: return BankView.render_error("Customer not found.", 404)
    return BankView.render_success(BankView.render_customer(customer))

@bank_blueprint.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer_by_id(customer_id):
    if not BankSystem.delete_customer_by_id(customer_id): return BankView.render_error("Customer not found.", 404)
    return BankView.render_success(None, "Customer deleted.")

@bank_blueprint.route('/customers/<customer_id>/deposit', methods=['POST'])
def deposit(customer_id):

    customer = BankSystem.get_customer_by_id(customer_id)

    if not customer: return BankView.render_error("Customer not found.", 404)
    data = request.get_json() or {}
    try: amount = float(data.get('amount', 0))
    except (ValueError, TypeError): return BankView.render_error("Invalid amount format.")
    success, msg = customer.deposit(amount)

    if not success: return BankView.render_error(msg)
    BankSystem.save_customer(customer)
    return BankView.render_success(BankView.render_customer(customer), msg)

@bank_blueprint.route('/customers/<customer_id>/withdraw', methods=['POST'])
def withdraw(customer_id):
    customer = BankSystem.get_customer_by_id(customer_id)
    if not customer: return BankView.render_error("Customer not found.", 404)
    data = request.get_json() or {}
    try: amount = float(data.get('amount', 0))
    except (ValueError, TypeError): return BankView.render_error("Invalid amount format.")
    success, msg = customer.withdraw(amount)
    if not success: return BankView.render_error(msg)
    BankSystem.save_customer(customer)
    return BankView.render_success(BankView.render_customer(customer), msg)

@bank_blueprint.route('/customers/transfer', methods=['POST'])
def transfer():
    data = request.get_json() or {}
    source_id = data.get('source_customer_id')
    target_id = data.get('target_customer_id')
    try: amount = float(data.get('amount', 0))
    except (ValueError, TypeError): return BankView.render_error("Invalid transfer amount format.")
    success, msg = BankSystem.transfer_funds(source_id, target_id, amount)
    if not success: return BankView.render_error(msg)
    return BankView.render_success(None, msg)

@bank_blueprint.route('/customers/premium', methods=['GET'])
def get_premium_customers():
    return BankView.render_success([BankView.render_customer(c) for c in BankSystem.get_premium_customers()])

@bank_blueprint.route('/customers/<customer_id>/history', methods=['GET'])
def get_history(customer_id):
    customer = BankSystem.get_customer_by_id(customer_id)
    if not customer: return BankView.render_error("Customer not found.", 404)
    return jsonify(BankView.render_history(customer))
