import os
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_default_database()
customers_col = db["customers"]

class Customer:
    def __init__(self, _id, account_holder, email, balance=0.0, transaction_history=None):
        self.account_id = str(_id)
        self.user_name = account_holder
        self.email = email  # 💡 Added email field
        self.balance = float(balance)
        self.transaction_history = transaction_history if transaction_history is not None else []

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be greater than zero."
        self.balance += amount
        
        self.transaction_history.append({
            "type": "DEPOSIT", 
            "amount": float(amount),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        return True, "Deposit Successful"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        if amount > self.balance:
            return False, f"Insufficient funds. Balance is: ${self.balance:,.2f}"
        self.balance -= amount
        
        self.transaction_history.append({
            "type": "WITHDRAWAL", 
            "amount": float(amount),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        return True, "Withdrawal Successful"

    def to_dict(self):
        return {
            "accountId": self.account_id,
            "userName": self.user_name,
            "email": self.email,
            "balance": self.balance
        }


class BankSystem:
    @staticmethod
    def create_customer(name, email, initial_deposit):
        if not name: return None, "Customer name can't be empty."
        if not email: return None, "Email address can't be empty."
        
        customer_data = {
            "account_holder": name,
            "email": email,
            "balance": float(initial_deposit),
            "transaction_history": [{
                "type": "DEPOSIT", 
                "amount": float(initial_deposit),
                "date": datetime.now().strftime("%Y-%m-%d")
            }]
        }
        
        result = customers_col.insert_one(customer_data)
        return Customer(_id=result.inserted_id, **customer_data), "Customer created successfully."

    @staticmethod
    def get_customer_by_id(customer_id):
        try:
            cust_data = customers_col.find_one({"_id": ObjectId(customer_id)})
            if not cust_data: return None
            return Customer(**cust_data)
        except Exception: return None

    @staticmethod
    def get_all_customers():
        cursor = customers_col.find({})
        return [Customer(**cust_data) for cust_data in cursor]

    @staticmethod
    def delete_customer_by_id(customer_id):
        try:
            result = customers_col.delete_one({"_id": ObjectId(customer_id)})
            return result.deleted_count > 0
        except Exception: return False

    @staticmethod
    def save_customer(customer):
        customers_col.update_one(
            {"_id": ObjectId(customer.account_id)},
            {"$set": {
                "balance": customer.balance,
                "transaction_history": customer.transaction_history
            }}
        )

    @staticmethod
    def transfer_funds(source_id, target_id, amount):
        if amount <= 0: return False, "Transfer amount must be greater than zero."
        source = BankSystem.get_customer_by_id(source_id)
        target = BankSystem.get_customer_by_id(target_id)
        if not source or not target: return False, "One or both customer IDs were not found."

        success, msg = source.withdraw(amount)
        if not success: return False, msg

        target.deposit(amount)
        source.transaction_history[-1]["type"] = "TRANSFER_SENT"
        target.transaction_history[-1]["type"] = "TRANSFER_RECEIVED"

        BankSystem.save_customer(source)
        BankSystem.save_customer(target)
        return True, "Transfer completed successfully."

    @staticmethod
    def get_premium_customers():
        cursor = customers_col.find({"balance": {"$gt": 10000.00}})
        return [Customer(**cust_data) for cust_data in cursor]
