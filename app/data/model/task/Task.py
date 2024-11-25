from abc import ABC
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any
from uuid import UUID


class TaskType(Enum):
    Activation = "activation"
    Deactivation = "deactivation"
    Transaction = "transaction"


class TransactionMethod(Enum):
    Sell = "sell"
    Buy = "buy"


class Brokerage(IntEnum):
    BBAE = 0
    Chase = 1
    DSPAC = 2
    Fennel = 3
    Fidelity = 4
    Firstrade = 5
    Public = 6
    Robinhood = 7
    Schwab = 8
    SoFi = 9
    Tornado = 10
    Tradier = 11
    Tastytrade = 12
    Webull = 13
    Vanguard = 14
    WellsFargo = 15


class Task(ABC):
    task_type: TaskType
    task_id: UUID

    def __init__(self, task_type: TaskType, task_id: UUID):
        self.task_type = task_type
        self.task_id = task_id

    @staticmethod
    def Activation(task_id: UUID, brokerage: Brokerage, creds: Any):

        return _ActivationTask(task_id, brokerage, creds)

    @staticmethod
    def Deactivation(task_id: UUID, account_id: UUID):
        return _DeactivationTask(task_id, account_id)

    @staticmethod
    def Transaction(task_id: UUID, method: TransactionMethod, amount: int, ticker: str):
        return _TransactionTask(task_id, method, amount, ticker)


class _ActivationTask(Task):
    brokerage: Brokerage
    cred: any

    def __init__(self, task_id: UUID, brokerage: Brokerage, creds: Any):
        super().__init__(task_type=TaskType.Activation, task_id=task_id)
        self.brokerage = brokerage
        self.cred = self.parse_creds(creds)

    def parse_creds(self, creds: Any):
        parsed_creds = {}
        if creds.USERNAME:
            parsed_creds["USERNAME"] = creds.USERNAME

        if creds.PASSWORD:
            parsed_creds["PASSWORD"] = creds.PASSWORD

        if creds.EMAIL:
            parsed_creds["EMAIL"] = creds.EMAIL

        if creds.ACCESS_TOKEN:
            parsed_creds["ACCESS_TOKEN"] = creds.ACCESS_TOKEN

        if creds.TOTP_SECRET_OR_NA:
            parsed_creds["TOTP_SECRET_OR_NA"] = creds.TOTP_SECRET_OR_NA

        if creds.TOTP_OR_NA:
            parsed_creds["TOTP_OR_NA"] = creds.TOTP_OR_NA

        if creds.TOTP_SECRET:
            parsed_creds["TOTP_SECRET"] = creds.TOTP_SECRET

        if creds.OTP:
            parsed_creds["OTP"] = creds.OTP

        if creds.PHONE_LAST_FOUR:
            parsed_creds["PHONE_LAST_FOUR"] = creds.PHONE_LAST_FOUR

        if creds.DEBUG:
            parsed_creds["DEBUG"] = creds.DEBUG

        if creds.DID:
            parsed_creds["DID"] = creds.DID

        if creds.TRADING_PIN:
            parsed_creds["TRADING_PIN"] = creds.TRADING_PIN

        return parsed_creds


class _DeactivationTask(Task):
    account_id: UUID

    def __init__(self, task_id: UUID, account_id: UUID):
        super().__init__(task_type=TaskType.Deactivation, task_id=task_id)
        self.account_id = account_id


class _TransactionTask(Task):
    transaction_method: TransactionMethod
    amount: int
    ticker: str

    def __init__(self, task_id: UUID, method: TransactionMethod, amount: int, ticker: str):
        super().__init__(task_type=TaskType.Transaction, task_id=task_id)
        self.transaction_method = method
        self.amount = amount
        self.ticker = ticker


ActivationTask = _ActivationTask
DeactivationTask = _DeactivationTask
TransactionTask = _ActivationTask


@dataclass
class ActivationResponse:
    account_id: str


@dataclass
class DeactivationResponse:
    # Added if needed
    pass


@dataclass
class TransactionResponse:
    # Added if needed
    pass


