import hashlib
import datetime

def create_account():
    """Creates a new bank account and saves details to file."""
    name = input("Enter your name: ")
    initial_deposit = float(input("Enter your initial deposit: "))
    account_number = generate_account_number()
    password = input("Enter a password: ")
    hashed_password = hash_password(password) 

    try:
        with open("accounts.txt", "a") as file:
            file.write(f"{account_number},{name},{hashed_password},{initial_deposit}\n")
        print(f"Your account number: {account_number}")
        print("Account created successfully!")
    except Exception as e:
        print(f"Error creating account: {e}")

def login():
    """Authenticates user login and returns account details."""
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                account_data = line.strip().split(",")
                if account_number == account_data[0] and hashed_password == account_data[2]:
                    return account_data
        print("Invalid account number or password.")
        return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None

def deposit(account_number, amount):
    """Processes a deposit transaction."""
    try:
        update_balance(account_number, amount)
        log_transaction(account_number, "Deposit", amount)
        print(f"Deposit successful! Current balance: {get_balance(account_number)}")
    except Exception as e:
        print(f"Error during deposit: {e}")

def withdraw(account_number, amount):
    """Processes a withdrawal transaction."""
    try:
        current_balance = get_balance(account_number)
        if amount > current_balance:
            print("Insufficient balance.")
            return
        update_balance(account_number, -amount)
        log_transaction(account_number, "Withdrawal", amount)
        print(f"Withdrawal successful! Current balance: {get_balance(account_number)}")
    except Exception as e:
        print(f"Error during withdrawal: {e}")

def get_balance(account_number):
    """Retrieves the current balance of an account."""
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                account_data = line.strip().split(",")
                if account_number == account_data[0]:
                    return float(account_data[3])
        return 0.0
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0.0

def update_balance(account_number, amount):
    """Updates the balance of an account in the accounts file."""
    try:
        lines = []
        with open("accounts.txt", "r") as file:
            for line in file:
                account_data = line.strip().split(",")
                if account_number == account_data[0]:
                    new_balance = float(account_data[3]) + amount
                    lines.append(f"{account_number},{account_data[1]},{account_data[2]},{new_balance}\n")
                else:
                    lines.append(line)

        with open("accounts.txt", "w") as file:
            file.writelines(lines)
    except Exception as e:
        print(f"Error updating balance: {e}")

def log_transaction(account_number, transaction_type, amount):
    """Logs a transaction to the transactions file."""
    try:
        with open("transactions.txt", "a") as file:
            file.write(f"{account_number},{transaction_type},{amount},{datetime.datetime.now().strftime('%Y-%m-%d')}\n")
    except Exception as e:
        print(f"Error logging transaction: {e}")

def generate_account_number():
    """Generates a random 6-digit account number."""
    import random
    return str(random.randint(100000, 999999))

def hash_password(password):
    """Hashes the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    while True:
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_data = login()
            if account_data:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Logout")
                    transaction_choice = input("Enter your choice: ")

                    if transaction_choice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        deposit(account_data[0], amount)
                    elif transaction_choice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        withdraw(account_data[0], amount)
                    elif transaction_choice == "3":
                        print(f"Current balance: {get_balance(account_data[0])}")
                    elif transaction_choice == "4":
                        print("Logged out.")
                        break
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")