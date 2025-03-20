import asyncio
import uniserde
import unicall
import typing as t
from imy.async_utils import TaskGroup
import unicall.data_models
import asyncio


class FakeTransport(unicall.Transport):
    async def call_remote_function(
        self,
        function_meta: unicall.data_models.FunctionMetadata,
        arguments: list[t.Any],
        await_response: bool,
    ) -> t.Any:
        print(f"Call function `{function_meta.name}` with arguments {arguments}")

    async def listen_for_request(
        self,
        interface: unicall.Unicall,
    ) -> tuple[
        unicall.data_models.FunctionMetadata,
        t.Callable,
        list[t.Any],
        t.Callable[[t.Any], t.Awaitable[None]],
        t.Callable[[Exception], t.Awaitable[None]],
    ]:
        while True:
            await asyncio.sleep(1)


class MyRpc(unicall.Unicall):
    @unicall.local
    async def local_function(self, x: int, y: int) -> int:
        return x + y

    @unicall.remote
    async def remote_function(self, x: int, y: int) -> int:
        raise NotImplementedError()


async def main() -> None:
    transport = FakeTransport()
    rpc = MyRpc(transport=transport)

    async with TaskGroup() as tasks:
        tasks.create_task(rpc.serve())

        await rpc.remote_function(1, 2)


if __name__ == "__main__":
    asyncio.run(main())
