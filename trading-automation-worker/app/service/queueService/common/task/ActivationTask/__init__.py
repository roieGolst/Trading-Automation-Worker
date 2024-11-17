from service.queueService.common.task.BaseTask import ParseFunction, Brokerage
from service.queueService.common.task.ActivationTask.AccessTokenActivationTask import TradierActivationTask
from service.queueService.common.task.ActivationTask.EmailOnlyActivationTask import FennelActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordActivationTask import BBAEActivationTask, \
    DSPACActivationTask, FidelityActivationTask, PublicActivationTask, TornadoActivationTask, TastytradeActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordDeviceIDPINActivationTask import \
    WebullActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordOTPActivationTask import FirstradeActivationTask, \
    SchwabActivationTask, SoFiActivationTask, RobinhoodActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordPhoneVerificationActivationTask import \
    ChaseActivationTask, VanguardActivationTask, WellsFargoActivationTask

brokerage_parse_function: dict[Brokerage, ParseFunction] = {
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
