from models.bank_model import customers_col

def run_once_migration():
    print("\n[MIGRATION] Scanning cloud documents inside MongoDB Atlas...")
    all_customers = list(customers_col.find({}))
    
    for customer in all_customers:
        cust_id = customer["_id"]
        name = customer.get("account_holder", "Unknown")
        
        updated_email = customer.get("email", f"{name.lower()}@example.com")
        
        original_history = customer.get("transaction_history", [])
        updated_history = []
        
        for tx in original_history:
            tx_type = tx.get("type", "DEPOSIT")
            if tx_type == "Savings":
                tx_type = "DEPOSIT"
                
            updated_history.append({
                "type": tx_type.upper(),
                "amount": float(tx.get("amount", 0.0)),
                "date": tx.get("date", "2026-03-20")
            })
            
        customers_col.update_one(
            {"_id": cust_id},
            {"$set": {
                "email": updated_email,
                "transaction_history": updated_history
            }}
        )
        print(f"[MIGRATION] Updated profile properties for user: '{name}'")
    print("[MIGRATION] Cloud database records migration complete!\n")

run_once_migration()
