from flask import jsonify

class BankView:
    @staticmethod
    def render_success(data, message="Success", status_code=200):
        return jsonify({
            "status": "success",
            "message": message,
            "data": data
        }), status_code

    @staticmethod
    def render_error(message, status_code=400):
        return jsonify({
            "status": "error",
            "message": message
        }), status_code

    @staticmethod
    def render_account(account):
        return account.to_dict()

    @staticmethod
    def render_history(account):
        return {
            "account_number": account.account_number,
            "transaction_history": account.transaction_history
        }
