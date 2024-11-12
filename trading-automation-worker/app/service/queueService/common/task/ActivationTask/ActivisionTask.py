from abc import abstractmethod
from typing import Dict, Any

from service.queueService import BaseTask, TaskType, ParseFunction
from service.queueService.common.task.ActivationTask.AccessTokenActivationTask import TradierActivationTask
from service.queueService.common.task.ActivationTask.EmailOnlyActivationTask import FennelActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordActivationTask import *
from service.queueService.common.task.ActivationTask.UsernamePasswordDeviceIDPINActivationTask import *
from service.queueService.common.task.ActivationTask.UsernamePasswordOTPActivationTask import *
from service.queueService.common.task.ActivationTask.UsernamePasswordPhoneVerificationActivationTask import *


class ActivationTask(BaseTask, ABC):
    brokerage: Brokerage
    accountId: str
    cred: Tuple[any]

    def __init__(self, task_id: UUID, brokerage: Brokerage, account_id: UUID, creds: Any):
        super().__init__(task_type=TaskType.Activation, task_id=task_id)
        self.brokerage = brokerage
        self.account_id = account_id
        self.cred = creds

    @classmethod
    @abstractmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            brokerage: Brokerage = task.get("brokerage")
            brokerage_parse_function: Dict[Brokerage, ParseFunction] = {
                Brokerage.BBAE: BBAEActivationTask.parse,
                Brokerage.Chase: ChaseActivationTask.parse,
                Brokerage.DSPAC: DSPACActivationTask.parse,
                Brokerage.Fennel: FennelActivationTask.parse,
                Brokerage.Fidelity: FidelityActivationTask.parse,
                Brokerage.Firstrade: FirstradeActivationTask.parse,
                Brokerage.Public: PublicActivationTask.parse,
                Brokerage.Robinhood: RobinhoodActivationTask.parse,
                Brokerage.Schwab: SchwabActivationTask.parse,
                Brokerage.SoFi: SoFiActivationTask.parse,
                Brokerage.Tornado: TornadoActivationTask.parse,
                Brokerage.Tradier: TradierActivationTask.parse,
                Brokerage.Tastytrade: TastytradeActivationTask.parse,
                Brokerage.Webull: WebullActivationTask.parse,
                Brokerage.Vanguard: VanguardActivationTask.parse,
                Brokerage.WellsFargo: WellsFargoActivationTask.parse,
            }

            return brokerage_parse_function[brokerage]
        except Exception as err:
            # TODO: Replace with Error handling
            raise Exception(f"ActivationTask Parser Error: {err}")
