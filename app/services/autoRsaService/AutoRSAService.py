import subprocess
import sys
from uuid import UUID

from data.model.task.Task import Brokerage, TransactionMethod
from services.autoRsaService.EnvManager import EnvManager


class AutoRSAService:
    def __init__(self, env_file_path: str):
        self._env_manager = EnvManager(env_file_path)

    def activation(self, brokerage: Brokerage, account_details: dict):
        return self._env_manager.add_account(broker_name=brokerage.name, account_details=account_details)

    def deactivation(self, account_id: UUID):
        return self._env_manager.remove_account(account_id)

    def transaction(
        self,
        brokerage: Brokerage,
        method: TransactionMethod,
        ticker: str,
        amount: int
    ):
        # < prefix > < action > < amount > < ticker > < accounts > < dry >
        args = [method.value, amount, ticker, "false"]


def run_cli_command(command, *args):
    """
    Runs a CLI command and handles the output.
    :param command: The CLI command to run (e.g., 'your-cli-tool').
    :param args: Arguments to pass to the CLI tool.
    :return: The output from the CLI command.
    """
    try:
        # Build the full command
        full_command = [command] + list(args)
        print(f"Running command: {' '.join(full_command)}")

        # Run the command and capture output
        result = subprocess.run(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # Raises CalledProcessError on non-zero exit
        )

        print("Command output:")
        print(result.stdout)
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

    except FileNotFoundError:
        print(f"Command '{command}' not found. Is it installed and in your PATH?", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Example usage with a placeholder CLI tool and arguments
    CLI_TOOL = "your-cli-tool"  # Replace with the actual CLI tool name
    ARGUMENTS = ["--example-flag", "value"]  # Replace with the required arguments

    # Run the command
    output = run_cli_command(CLI_TOOL, *ARGUMENTS)

    # Process the output if needed
    print("Processed CLI output:")
    print(output)