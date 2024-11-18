import grpc

from dist.myService_pb2_grpc import MyServiceStub
from dist.types_pb2 import ActivationTask, BaseTask, UUID, Brokerage, ActivationCreds


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = MyServiceStub(channel)

        activation_task = ActivationTask(
            base_task=BaseTask(task_id=UUID(value="123e4567-e89b-12d3-a456-426614174000")),
            brokerage=Brokerage.BBAE,
            account_id=UUID(value="5d0b7f08-ee42-4a2b-9b64-7c6766f20621"),
            creds=ActivationCreds(
                username="roieGOlst",
                password="Golst"
            ),
        )

        response = stub.Activation(activation_task)
        print(f"Received: {response}")


if __name__ == '__main__':
    import threading

    # Run two client requests concurrently
    client1 = threading.Thread(target=run)
    # client2 = threading.Thread(target=run)

    client1.start()
    # client2.start()

    client1.join()
    # client2.join()
