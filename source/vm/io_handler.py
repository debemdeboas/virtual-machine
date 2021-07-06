from threading import Thread
from queue import Queue
from typing import Any, Callable, Dict, List, NamedTuple
from source.command.command import EIOOperationComplete


class IORequest(NamedTuple):
    process_id: int
    request: Callable
    args: List[Any]
    kwargs: Dict[Any, Any]


class IOHandler(Thread):
    def __init__(self, owner):
        Thread.__init__(self, daemon=True)

        self.queue: Queue[IORequest] = Queue()
        self.owner = owner

    def run(self):
        while True:
            iorequest = self.queue.get()
            iorequest.request(*iorequest.args, **iorequest.kwargs)
            self.owner.cpu.queue_interrupt(EIOOperationComplete(iorequest.process_id))
