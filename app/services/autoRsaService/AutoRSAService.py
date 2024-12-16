import os
import shutil
import subprocess
from uuid import UUID

from data.model.task.Task import Brokerage, TransactionMethod
from data.model.task.types import Response
from services.autoRsaService.EnvManager import EnvManager


class AutoRSAService:

    def __init__(self, dir_path: str, env_file_path: str, python_version: str = "3.12"):
        self._dir_path = dir_path
        self._env_manager = EnvManager(env_file_path)

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
        result = self.run_cli_command(args)
        return result

    def run_cli_command(self, args: list) -> Response:
        try:
            script_path = f"{self._dir_path}/scripts/run_autoRSA.sh"
            full_command = [script_path] + args

            process = subprocess.Popen(
                full_command,
                cwd=self._dir_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                return Response(
                    success=False,
                    error=f"Error running autoRSA cli tool '{full_command}': {stderr.strip()}"
                )

            # Process succeeded
            return Response(
                success=True,
                value=stdout.strip()
            )

        except subprocess.CalledProcessError as e:
            return Response(
                success=False,
                error=f"Error running autoRSA cli tool '{command}': {e.stdout}"
            )

        except Exception as err:
            return Response(
                success=False,
                error=f"Error running autoRSA cli tool {err}"
            )
