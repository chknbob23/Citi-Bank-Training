import json

# Define your default test records
mock_database = {
    "next_account_number": 1003,
    "accounts": {
        "1000": {
            "account_number": "1000",
            "account_holder": "Alice Smith",
            "balance": 2500.50,
            "transaction_history": [
                {"type": "Account Created", "amount": 2000.00},
                {"type": "Deposit", "amount": 500.50}
            ]
        },
        "1001": {
            "account_number": "1001",
            "account_holder": "Bob Jones",
            "balance": 45.00,
            "transaction_history": [
                {"type": "Account Created", "amount": 100.00},
                {"type": "Withdrawal", "amount": -55.00}
            ]
        },
        "1002": {
            "account_number": "1002",
            "account_holder": "Charlie Brown",
            "balance": 12500.00,
            "transaction_history": [
                {"type": "Account Created", "amount": 12500.00}
            ]
        }
    }
}

def seed():
    with open("database.json", "w") as f:
        json.dump(mock_database, f, indent=4)
    print("Successfully populated database.json with 3 test accounts!")

if __name__ == "__main__":
    seed()
