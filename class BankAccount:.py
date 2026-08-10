class BankAccount:

    def __init__(self, account_number, account_holder, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = float(initial_balance)
        self.transaction_history = []

        if initial_balance > 0:
            self._add_transaction("Account Created", initial_balance)
        else:
            self._add_transaction("Account Created", 0.0)

    def deposit(self, amount):
        """Adds a positive amount to the account balance."""
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return False

        self.balance += amount
        self._add_transaction("Deposit", amount)
        print(self._format_receipt("Deposit Successful", amount))
        return True

    def withdraw(self, amount):

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return False
        if amount > self.balance:
            print(f"Insufficient funds. Available balance: ${self.balance:,.2f}")
            return False

        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
        print(self._format_receipt("Withdrawal Successful", amount))
        return True

    def display_details(self):

        print("=" * 30)
        print("       ACCOUNT DETAILS       ")
        print("=" * 30)
        print(f"Holder:         {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance:,.2f}")
        print("=" * 30)

    def display_history(self):

        print("\n" + "=" * 55)
        print(f"    TRANSACTION HISTORY FOR ACC: {self.account_number}")
        print("=" * 55)
        print(f"{'Type':<15} | {'Amount':<12}")
        print("-" * 55)


    def _add_transaction(self, tx_type, amount):

        self.transaction_history.append({
            "type": tx_type,
            "amount": amount
        })

    def _format_receipt(self, message, amount):

        return f "Amount: ${amount:,.2f} | New Balance: ${self.balance:,.2f}"

class Bank_System:
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1001
    
    def create_account(self):
        print("--- Create New Account ---")
        name = input("Enter account holder's name: ").strip()

        if not name:
            print("Account holder's name can't be empty")
            return
        
        try:
            initial_deposit = float(input("Enter initial deposit amount: ") or 0)
            if initial_deposit < 0:
                print("Initial deposit can't be negative.")
                return
        except ValueError:
            print("Invalid amount entered!")
            return

        
