class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = float(initial_balance)
        self.transaction_history = []
        
        initial_tx_amount = initial_balance if initial_balance > 0 else 0.0
        self._add_transaction("Account Created", initial_tx_amount)

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be greater than zero."
        self.balance += amount
        self._add_transaction("Deposit", amount)
        return True, "Deposit Successful"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        if amount > self.balance:
            return False, f"Insufficient funds. Available balance: ${self.balance:,.2f}"
        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
        return True, "Withdrawal Successful"

    def _add_transaction(self, tx_type, amount):
        self.transaction_history.append({
            "type": tx_type,
            "amount": amount
        })

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance
        }


class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1000

    def create_account(self, name, initial_deposit):
        if not name:
            return None, "Account holder's name can't be empty."
        if initial_deposit < 0:
            return None, "Initial deposit can't be negative."

        acc_num = str(self.next_account_number)
        new_account = BankAccount(acc_num, name, initial_deposit)
        self.accounts[acc_num] = new_account
        self.next_account_number += 1
        return new_account, "Account created successfully."

    def get_account(self, account_number):
        return self.accounts.get(account_number)


# Single shared instance acting as our temporary database
db = BankSystem()
