import os
import threading

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
        self._load_env_file()
        self._remove_discord_vars()
        self._set_danger_mode()
        self._sync_accounts_to_env()

    def _load_env_file(self):
        """
        Load existing environment variables from the .env file.
        """
        if not os.path.exists(self.env_file_path):
            return

        with open(self.env_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                self.env_vars[key] = value

    def _remove_discord_vars(self):
        """
        Remove all Discord-related variables from the environment variables.
        """
        for var in DISCORD_VARS:
            if var in self.env_vars:
                del self.env_vars[var]

    def _set_danger_mode(self):
        """
        Ensure DANGER_MODE is set to "true" by default.
        """
        self.env_vars['DANGER_MODE'] = '"true"'

    def add_account(self, broker_name, account_name: str, account_details: dict) -> bool:
        """
        Add an account for a given brokerage by account name.

        Parameters:
        - broker_name (str): Name of the brokerage (e.g., 'Robinhood').
        - account_name (str): The name of the account.
        - account_details (dict): Account credentials as a dictionary.

        Returns:
        - bool: True if the account was added, False if an account with the same name already exists.
        """
        if broker_name not in BROKERAGES:
            raise ValueError(f"Broker '{broker_name}' is not supported.")

        if broker_name not in self.accounts:
            self.accounts[broker_name] = []

        # Check if the account name already exists
        for account in self.accounts[broker_name]:
            if account['name'] == account_name:
                return False  # Account already exists

        # Add new account
        self.accounts[broker_name].append({
            'name': account_name,
            'details': account_details
        })

        self._sync_accounts_to_env()
        self._write_env_file()
        return True

    def remove_account(self, account_name: str, broker_name: str) -> bool:
        """
        Remove an account using its account name and brokerage.

        Parameters:
        - account_name (str): The name of the account to remove.
        - broker_name (str): The brokerage of the account.

        Returns:
        - bool: True if the account was removed, False if not found.
        """
        if broker_name not in self.accounts:
            return False

        for account in self.accounts[broker_name]:
            if account['name'] == account_name:
                self.accounts[broker_name].remove(account)
                if not self.accounts[broker_name]:
                    del self.accounts[broker_name]
                self._sync_accounts_to_env()
                self._write_env_file()
                return True

        return False

    def _sync_accounts_to_env(self):
        """
        Sync accounts from in-memory storage to environment variables.
        """
        for env_var in BROKERAGES.values():
            if env_var in self.env_vars:
                del self.env_vars[env_var]

        for broker_name, accounts in self.accounts.items():
            env_var = BROKERAGES.get(broker_name)
            if env_var:
                account_strings = []
                for acc in accounts:
                    details = acc['details']
                    account_str = self._serialize_account_details(broker_name, details)
                    account_strings.append(account_str)
                existing_value = self.env_vars.get(env_var, "")
                combined_value = ','.join(account_strings)
                if existing_value:
                    self.env_vars[env_var] = f'"{existing_value},{combined_value}"'
                else:
                    self.env_vars[env_var] = f'"{combined_value}"'

    def _serialize_account_details(self, broker_name, details: dict) -> str:
        """
        Serialize account details dict into the string format required for the .env file.
        """
        fields = broker_fields.get(broker_name)
        if not fields:
            raise ValueError(f"Broker '{broker_name}' is not supported for serialization.")

        field_values = []
        for field in fields:
            value = details.get(field)
            if value is None:
                raise ValueError(f"Missing field '{field}' for broker '{broker_name}'.")
            field_values.append(value)
        return ':'.join(field_values)

    def _write_env_file(self):
        """
        Write the current environment variables back to the .env file without comments.
        """
        with open(self.env_file_path, 'w') as file:
            for key, value in self.env_vars.items():
                file.write(f'{key}={value}\n')
