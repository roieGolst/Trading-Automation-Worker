from service.queueService import AckFunction
from service.queueService.common.task.ActivationTask import UsernamePasswordActivationTask
from service.queueService.common.task.ActivationTask.UsernamePasswordActivationTask import BBAEActivationTask
from service.queueService.common.task.BaseTask import BaseTask
from bootstrap import bootstrap, BootstrapArgs

TASK_HANDLER_REGISTRY = {}


def register_handler(task_class):
    def decorator(func):
        TASK_HANDLER_REGISTRY[task_class] = func
        return func

    return decorator


@register_handler(UsernamePasswordActivationTask)
def handle_username_password_activation_task(task: UsernamePasswordActivationTask) -> None:
    print("Handling UsernamePasswordActivationTask")
    print(f"Username: {task.cred.username}")


@register_handler(BBAEActivationTask)
def handle_bbae_activation_task(task: BBAEActivationTask) -> None:
    print("Handling BBAEActivationTask")


def handler(task: BaseTask, ack: AckFunction) -> None:
    print("Processing task...")
    print(f"Task type: {task.task_type}\nId: {task.task_id}")

    handler_function = TASK_HANDLER_REGISTRY.get(type(task))

    if handler_function:
        handler_function(task)
    else:
        print("Unknown task type. No specific handler available.")

    print("Done")
    ack()


if __name__ == '__main__':
    bootstrap(BootstrapArgs(host="localhost", handler_function=handler))
