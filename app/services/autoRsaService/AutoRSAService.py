import shutil
import subprocess
import sys
from uuid import UUID

from data.model.task.Task import Brokerage, TransactionMethod
from services.autoRsaService.EnvManager import EnvManager


class AutoRSAService:

    def __init__(self,cli_binary_path: str,  env_file_path: str, python_version: str = "3.12"):
        self._env_manager = EnvManager(env_file_path)
        self._cli_path = cli_binary_path

        try:
            result = subprocess.run(
                ["pyenv", "which", f"python{python_version}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.python_path = result.stdout.strip()
        except subprocess.CalledProcessError:
            # Fallback to `which` if pyenv is not used
            self.python_path = shutil.which(f"python{python_version}")
            if not self.python_path:
                raise RuntimeError(f"Python {python_version} is not available.")

    def activation(self, brokerage: Brokerage, account_details: dict):
        return self._env_manager.add_account(broker_name=brokerage.name, account_details=account_details)

    def deactivation(self, account_id: UUID):
        return self._env_manager.remove_account(account_id)

    def transaction(
        self,
        method: TransactionMethod,
        ticker: str,
        amount: int
    ):
        str_method: str = dict({
            TransactionMethod.Buy: "buy",
            TransactionMethod.Sell: "sell"
        })[method]

        args = [str_method, str(amount), ticker, "all", "false"]
        self.run_cli_command(self._cli_path, *args)

    def run_cli_command(self, command, *args):
        try:
            full_command = [self.python_path, command] + list(args);

            result = subprocess.run(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            print("Command output:")
            print(result.stdout)
            return result.stdout

        except subprocess.CalledProcessError as e:
            print(f"Error running command '{command}': {e.stdout}", file=sys.stderr)
            sys.exit(e.returncode)

        except FileNotFoundError:
            print(f"Command '{command}' not found. Is it installed and in your PATH?", file=sys.stderr)
            sys.exit(1)

        except Exception as err:
            print(err)
