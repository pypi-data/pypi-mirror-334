import asyncio
import typing as t

import pytest
from imy.async_utils import TaskGroup

import unicall.json_rpc


class Peer1(unicall.Unicall):
    @unicall.local
    async def peer_1_add(self, x: int, y: int) -> int:
        print("Peer 1 add called with", x, y)
        return x + y

    @unicall.local
    async def peer_1_mul(self, x: int, y: int) -> int:
        print("Peer 1 mul called with", x, y)
        return x * y

    @unicall.remote
    async def peer_2_add(self, x: int, y: int) -> int:
        raise NotImplementedError()

    @unicall.remote
    async def peer_2_mul(self, x: int, y: int) -> int:
        raise NotImplementedError()


class Peer2(unicall.Unicall):
    @unicall.local
    async def peer_2_add(self, x: int, y: int) -> int:
        print("Peer 2 add called with", x, y)
        return x + y

    @unicall.local
    async def peer_2_mul(self, x: int, y: int) -> int:
        print("Peer 2 mul called with", x, y)
        return x * y

    @unicall.remote
    async def peer_1_add(self, x: int, y: int) -> int:
        raise NotImplementedError()

    @unicall.remote
    async def peer_1_mul(self, x: int, y: int) -> int:
        raise NotImplementedError()


def make_print_and_put(
    queue: asyncio.Queue[str],
) -> t.Callable[[str], t.Awaitable[None]]:
    async def print_and_put(message: str) -> None:
        print("PUT", message)
        await queue.put(message)

    return print_and_put


def make_get_and_print(
    queue: asyncio.Queue[str],
) -> t.Callable[[], t.Awaitable[str]]:
    async def get_and_print() -> str:
        message = await queue.get()
        print("GOT", message)
        return message

    return get_and_print


@pytest.mark.asyncio
async def test_communication() -> None:
    peer_1_to_2 = asyncio.Queue[str]()
    peer_2_to_1 = asyncio.Queue[str]()

    # Instantiate the peers
    transport_1 = unicall.json_rpc.JsonRpcTransport(
        send=make_print_and_put(peer_1_to_2),
        receive=make_get_and_print(peer_2_to_1),
    )

    peer_1 = Peer1(transport=transport_1)

    transport_2 = unicall.json_rpc.JsonRpcTransport(
        send=make_print_and_put(peer_2_to_1),
        receive=make_get_and_print(peer_1_to_2),
    )

    peer_2 = Peer2(transport=transport_2)

    # Parallelize
    async with TaskGroup() as tasks:
        # Start serving the peers
        tasks.create_task(peer_1.serve())
        tasks.create_task(peer_2.serve())

        # Call the functions
        assert await peer_1.peer_2_add(1, 2) == 3
        assert await peer_1.peer_2_mul(3, 4) == 12
        assert await peer_2.peer_1_add(5, 6) == 11
        assert await peer_2.peer_1_mul(7, 8) == 56
