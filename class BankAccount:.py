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
  
        print("       ACCOUNT DETAILS        ")
        print(f"Holder: {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance:,.2f}")

    def display_history(self):

        print(f"TRANSACTION HISTORY FOR ACC: {self.account_number}")
        print(f"{'Type':<20} | {'Amount':<12}")
        print("-" * 55)
  
        for tx in self.transaction_history:
            print(f"{tx['type']:<20} | ${tx['amount']:>10,.2f}")

    def _add_transaction(self, tx_type, amount):
        self.transaction_history.append({
            "type": tx_type,
            "amount": amount
        })

    def _format_receipt(self, message, amount):
        return f"{message} -> Amount: ${amount:,.2f} | New Balance: ${self.balance:,.2f}"


class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1000

    def create_account(self):
        print("\n--- Create New Account ---")
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
        
        acc_num = str(self.next_account_number)
        new_account = BankAccount(acc_num, name, initial_deposit)
        self.accounts[acc_num] = new_account
        self.next_account_number += 1
        print(f"Account created for: {name}")
        print(f"Your account number is: {acc_num}")

    def get_account(self, action=""):
        acc_num = input(f"Enter your account number to {action}: ").strip()
        account = self.accounts.get(acc_num)
        if not account:
            print("Account number not found.")
            return None
        return account

    def run(self):
        while True:
            print("\n=== Main Menu ===")
            print("1. Create An Account")
            print("2. View Account Details")
            print("3. Make Deposit")
            print("4. Withdrawal")
            print("5. View Transaction History")
            print("6. Exit")
            choice = input("Select an option (1-6): ").strip()
            
            match choice:
                case "1":
                    self.create_account()
                case "2":
                    account = self.get_account("view")
                    if account:
                        account.display_details()
                case "3":
                    account = self.get_account("deposit into")
                    if account:
                        try:
                            amount = float(input("Enter amount to deposit: "))
                            account.deposit(amount)
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                case "4":
                    account = self.get_account("withdraw from")
                    if account:
                        try:
                            amount = float(input("Enter amount to withdraw: "))
                            account.withdraw(amount)
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                case "5":
                    account = self.get_account("view history")
                    if account:
                        account.display_history()
                case "6":
                    print("Thank you.")
                    break
                case _:
                    print("Invalid option.")

if __name__ == "__main__":
    bank = BankSystem()
    bank.run()
