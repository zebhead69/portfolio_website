import os
import json
import hashlib
from cryptography.fernet import Fernet
from eth_account import Account

# Dynamically set the directory of the script itself
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)
print(f"Working directory set to script's location: {os.getcwd()}")

# Check if the encryption key file exists
if not os.path.exists("encryption_key.key"):
    # Generate and save a new key if it doesn't exist
    encryption_key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(encryption_key)
    print("Encryption key created and saved to 'encryption_key.key'.")
else:
    # Load the existing encryption key
    with open("encryption_key.key", "rb") as key_file:
        encryption_key = key_file.read()

# Initialize the cipher suite
cipher = Fernet(encryption_key)


# Save file with a hash for integrity verification
def save_file_with_hash(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_hash = hashlib.sha256(file_data).hexdigest()
        with open(f"{file_path}.hash", 'w') as hash_file:
            hash_file.write(file_hash)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Hash not created.")


# Simulated periodic backup function
def periodic_backup(source, destination):
    try:
        with open(source, 'rb') as src_file:
            data = src_file.read()
        with open(destination, 'wb') as dest_file:
            dest_file.write(data)
    except FileNotFoundError:
        print(f"Backup failed: '{source}' not found.")


# Input and encrypt credentials
def input_and_encrypt_credentials():
    credentials = load_credentials_from_file()
    while True:
        wallet_name = input("Enter wallet name (or type 'done' to finish): ").strip()
        if wallet_name.lower() == "done":
            break
        credential_type = input("Enter 'seed' for seed phrase or 'key' for private key: ").strip().lower()
        if credential_type not in ['seed', 'key']:
            print("Invalid choice. Please enter 'seed' or 'key'.")
            continue
        
        credential = input(f"Enter the {credential_type} for wallet '{wallet_name}': ").strip()
        encrypted_credential = cipher.encrypt(credential.encode())
        credentials[wallet_name] = {"type": credential_type, "value": encrypted_credential.decode()}
        print(f"{credential_type.capitalize()} for '{wallet_name}' encrypted and stored.\n")
    return credentials


# Save credentials to file
def save_credentials_to_file(credentials, filename="credentials.json"):
    encrypted_credentials = {wallet: {"type": data["type"], "value": data["value"]}
                             for wallet, data in credentials.items()}
    with open(filename, "w") as file:
        json.dump(encrypted_credentials, file)
    print(f"Credentials saved to {filename}\n")


# Load credentials from file
def load_credentials_from_file(filename="credentials.json"):
    if not os.path.exists(filename):
        print("Credentials storage file not found!")
        return {}
    with open(filename, "r") as file:
        encrypted_credentials = json.load(file)
    credentials = {wallet: {"type": data["type"], "value": cipher.decrypt(data["value"].encode()).decode()}
                   for wallet, data in encrypted_credentials.items()}
    return credentials


# Create wallet from seed or private key
def create_wallet(credential_type, credential_value):
    try:
        if credential_type == "seed":
            account = Account.from_mnemonic(credential_value)
        elif credential_type == "key":
            account = Account.from_key(credential_value)
        else:
            raise ValueError("Unsupported credential type")
        print(f"Wallet Address: {account.address}")
        print(f"Private Key: {account.key.hex()}")
        return account
    except Exception as e:
        print(f"Error creating wallet: {e}")
        return None


# Securely save wallet and backup
def securely_save_wallet(wallet_name, credential_type, credential_value):
    try:
        credentials = load_credentials_from_file()
    except FileNotFoundError:
        credentials = {}

    encrypted_credential = cipher.encrypt(credential_value.encode())
    credentials[wallet_name] = {"type": credential_type, "value": encrypted_credential.decode()}

    save_credentials_to_file(credentials)

    # Backup and hash verification
    save_file_with_hash("credentials.json")
    periodic_backup("credentials.json", "backup_credentials.json")
    save_file_with_hash("backup_credentials.json")
    print(f"Wallet '{wallet_name}' securely saved and backed up.")


# Main Program
def main():
    print("Choose an option:")
    print("1. Input and encrypt new credentials")
    print("2. Load existing credentials and populate a wallet")
    choice = input("Enter (1 or 2): ").strip()
    
    if choice == "1":
        credentials = input_and_encrypt_credentials()
        save_credentials_to_file(credentials)
    elif choice == "2":
        credentials = load_credentials_from_file()
        if not credentials:
            print("No credentials found. Add some first.")
            return
        print("Available wallets:")
        for wallet_name in credentials.keys():
            print(f"- {wallet_name}")
        
        wallet_name = input("\nEnter the wallet name to load: ").strip()
        if wallet_name in credentials:
            credential_type = credentials[wallet_name]["type"]
            credential_value = credentials[wallet_name]["value"]
            print(f"\nCreating wallet for: {wallet_name} using {credential_type}")
            create_wallet(credential_type, credential_value)
        else:
            print("Wallet not found in the storage.")
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()

