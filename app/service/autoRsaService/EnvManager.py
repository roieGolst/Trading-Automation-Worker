import os
import threading
import uuid

from typing_extensions import Self

DISCORD_VARS = ['DISCORD_TOKEN', 'DISCORD_CHANNEL']
BROKERAGES = {
    'BBAE': 'BBAE',
    'Chase': 'CHASE',
    'DSPAC': 'DSPAC',
    'Fennel': 'FENNEL',
    'Fidelity': 'FIDELITY',
    'Firstrade': 'FIRSTRADE',
    'Public': 'PUBLIC_BROKER',
    'Robinhood': 'ROBINHOOD',
    'Schwab': 'SCHWAB',
    'SoFi': 'SOFI',
    'Tastytrade': 'TASTYTRADE',
    'Tornado': 'TORNADO',
    'Tradier': 'TRADIER',
    'Vanguard': 'VANGUARD',
    'Webull': 'WEBULL',
    'WellsFargo': 'WELLSFARGO',
}


class EnvManager:
    __INSTANCE: Self = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__INSTANCE:
            with cls.__lock:
                if not cls.__INSTANCE:
                    cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(self, env_file_path):
        self.env_file_path = env_file_path
        self.env_vars = {}
        self.accounts = {}
        self.load_env_file()
        self.remove_discord_vars()
        self.set_danger_mode()
        self.sync_accounts_to_env()

    def load_env_file(self):
        """
        Load existing environment variables from the .env file.
        """
        if not os.path.exists(self.env_file_path):
            # Initialize empty if file doesn't exist
            return

        with open(self.env_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                # Skip comments and empty lines
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                self.env_vars[key] = value

    def remove_discord_vars(self):
        """
        Remove all Discord-related variables from the environment variables.
        """
        for var in DISCORD_VARS:
            if var in self.env_vars:
                del self.env_vars[var]

    def set_danger_mode(self):
        """
        Ensure DANGER_MODE is set to "true" by default.
        """
        self.env_vars['DANGER_MODE'] = '"true"'

    def add_account(self, broker_name, account_details: dict) -> uuid.UUID:
        """
        Add an account for a given brokerage.

        Parameters:
        - broker_name (str): Name of the brokerage (e.g., 'Robinhood').
        - account_details (dict): Account credentials as a dictionary.

        Returns:
        - uuid.UUID: The unique ID assigned to the account.
        """
        if broker_name not in BROKERAGES:
            raise ValueError(f"Broker '{broker_name}' is not supported.")

        if broker_name not in self.accounts:
            self.accounts[broker_name] = []

        # Check for duplicate account_details
        for account in self.accounts[broker_name]:
            if account['details'] == account_details:
                print(f"Account already exists for broker '{broker_name}'.")
                return uuid.UUID(account['id'])  # Return existing account ID

        # If no duplicate found, add new account
        account_id = uuid.uuid4()
        self.accounts[broker_name].append({
            'id': str(account_id),
            'details': account_details
        })
        self.sync_accounts_to_env()
        self.write_env_file()
        return account_id

    def remove_account(self, account_id):
        """
        Remove an account using its unique ID.

        Parameters:
        - account_id (uuid.UUID): The unique ID of the account to remove.

        Returns:
        - bool: True if the account was removed, False if not found.
        """
        found = False
        for broker_name, accounts in list(self.accounts.items()):
            for account in accounts:
                if account['id'] == str(account_id):
                    accounts.remove(account)
                    found = True
                    break  # Account ID is unique, so we can break here
            if found:
                # If the brokerage has no more accounts, remove it
                if not accounts:
                    del self.accounts[broker_name]
                self.sync_accounts_to_env()
                break
        self.write_env_file()
        return found

    def sync_accounts_to_env(self):
        """
        Sync accounts from in-memory storage to environment variables.
        """
        # Clear existing brokerage env_vars
        for env_var in BROKERAGES.values():
            if env_var in self.env_vars:
                del self.env_vars[env_var]

        # Add current accounts
        for broker_name, accounts in self.accounts.items():
            env_var = BROKERAGES.get(broker_name)
            if env_var:
                # Serialize account details into strings
                account_strings = []
                for acc in accounts:
                    details = acc['details']
                    # Convert details dict into string
                    account_str = self.serialize_account_details(broker_name, details)
                    account_strings.append(account_str)
                # Combine all account strings into a single string
                accounts_str = ','.join(account_strings)
                self.env_vars[env_var] = f'"{accounts_str}"'

    def serialize_account_details(self, broker_name, details: dict) -> str:
        """
        Serialize account details dict into the string format required for the .env file.

        Parameters:
        - broker_name (str): Name of the brokerage.
        - details (dict): Account details dictionary.

        Returns:
        - str: Serialized account details string.
        """
        # Define the required fields for each broker in order
        broker_fields = {
            'BBAE': ['USERNAME', 'PASSWORD'],
            'Chase': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR', 'DEBUG'],
            'DSPAC': ['USERNAME', 'PASSWORD'],
            'Fennel': ['EMAIL'],
            'Fidelity': ['USERNAME', 'PASSWORD', 'TOTP_SECRET_OR_NA'],
            'Firstrade': ['USERNAME', 'PASSWORD', 'OTP'],
            'Public': ['USERNAME', 'PASSWORD'],
            'Robinhood': ['USERNAME', 'PASSWORD', 'TOTP_OR_NA'],
            'Schwab': ['USERNAME', 'PASSWORD', 'TOTP_SECRET_OR_NA'],
            'SoFi': ['USERNAME', 'PASSWORD', 'TOTP_SECRET'],
            'Tastytrade': ['USERNAME', 'PASSWORD'],
            'Tornado': ['EMAIL', 'PASSWORD'],
            'Tradier': ['ACCESS_TOKEN'],
            'Vanguard': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR', 'DEBUG'],
            'Webull': ['USERNAME', 'PASSWORD', 'DID', 'TRADING_PIN'],
            'WellsFargo': ['USERNAME', 'PASSWORD', 'PHONE_LAST_FOUR'],
        }

        fields = broker_fields.get(broker_name)
        if not fields:
            raise ValueError(f"Broker '{broker_name}' is not supported for serialization.")

        # Build the account string by joining the fields with ':'
        field_values = []
        for field in fields:
            value = details.get(field)
            if value is None:
                raise ValueError(f"Missing field '{field}' for broker '{broker_name}'.")
            field_values.append(value)
        account_str = ':'.join(field_values)
        return account_str

    def write_env_file(self):
        """
        Write the current environment variables back to the .env file without comments.
        """
        with open(self.env_file_path, 'w') as file:
            # Write environment variables
            for key, value in self.env_vars.items():
                file.write(f'{key}={value}\n')

    # TODO: Reuse if needed
    # def get_account(self, account_id):
    #     """
    #     Get the account details using its unique ID.
    #
    #     Parameters:
    #     - account_id (uuid.UUID): The unique ID of the account.
    #
    #     Returns:
    #     - dict or None: Account information or None if not found.
    #     """
    #     for broker_name, accounts in self.accounts.items():
    #         for account in accounts:
    #             if account['id'] == str(account_id):
    #                 return {
    #                     'broker_name': broker_name,
    #                     'id': account['id'],
    #                     'details': account['details']
    #                 }
    #     return None
    #
    # def list_accounts(self):
    #     """
    #     List all accounts with their IDs.
    #
    #     Returns:
    #     - list: A list of accounts with broker name, ID, and details.
    #     """
    #     account_list = []
    #     for broker_name, accounts in self.accounts.items():
    #         for account in accounts:
    #             account_list.append({
    #                 'broker_name': broker_name,
    #                 'id': account['id'],
    #                 'details': account['details']
    #             })
    #     return account_list
    #
    # def get_accounts_by_broker(self, broker_name):
    #     """
    #     Get all accounts for a specific brokerage.
    #
    #     Parameters:
    #     - broker_name (str): Name of the brokerage.
    #
    #     Returns:
    #     - list: A list of accounts for the brokerage, or empty list if none.
    #     """
    #     return self.accounts.get(broker_name, [])