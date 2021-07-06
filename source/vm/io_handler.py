from source.memory.process import ProcessControlBlock
from threading import Thread
from queue import Queue
from typing import Any, Callable, Dict, List, NamedTuple
from source.command.command import EIOOperationComplete


class IORequest(NamedTuple):
    process: ProcessControlBlock
    request: Callable

    def execute(self):
        return self.request()


class IOResponse(NamedTuple):
    process_id: int


class IOHandler(Thread):
    def __init__(self, owner):
        Thread.__init__(self, daemon=True)

        self.queue: Queue[IORequest] = Queue()
        self.owner = owner

    def run(self):
        while True:
            iorequest = self.queue.get()
            iorequest.execute()
            self.owner.cpu.queue_interrupt(EIOOperationComplete(IOResponse(iorequest.process.pid)))

    def queue_operation(self, proc: ProcessControlBlock, request: Callable):
        self.queue.put_nowait(IORequest(proc, request))
