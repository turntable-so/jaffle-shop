import multiprocessing
import queue
import sys
import threading
from unittest.mock import patch

import dill
import mpire
from dbt.cli.main import dbtRunner


def run_dbt_command(command=["run"]):
    runner = dbtRunner()
    return runner.invoke(command)


def forked(command):
    with mpire.WorkerPool(n_jobs=1, start_method="fork") as pool:
        return pool.map(run_dbt_command, command)[0]


def threaded(command):
    with mpire.WorkerPool(n_jobs=1, start_method="threading") as pool:
        return pool.map(forked, command)[0]


#!/usr/bin/env python3


def child_process():
    from dbt.cli.main import dbtRunner

    runner = dbtRunner()
    return runner.invoke(["run"])


original_stdout_write = sys.stdout.write
original_stderr_write = sys.stderr.write


def stream_output(terminate_event, fork_queue, parent_queue):
    while not terminate_event.is_set():
        try:
            text = fork_queue.get(timeout=0.01)
            parent_queue.put(text)
        except (multiprocessing.queues.Empty, queue.Empty):
            continue


original_stdout_write = sys.stdout.write
original_stderr_write = sys.stderr.write


def forking_helper(fork_queue, f_serialized, args_kwargs={}):
    child_work = dill.loads(f_serialized)

    """
    Restructured inner function to avoid passing self and proj objects
    """
    args, kwargs = args_kwargs.get("args", []), args_kwargs.get("kwargs", {})

    def custom_write_stdout(text):
        fork_queue.put(text)
        return len(text)

    def custom_write_stderr(text):
        fork_queue.put(text)
        return len(text)

    @patch("sys.stdout.write", custom_write_stdout)
    @patch("sys.stderr.write", custom_write_stderr)
    def sub_inner():
        child_work(*args, **kwargs)

    sub_inner()


def fork_and_yield_output(f, args_kwargs={}, external_terminate_event=None):
    args, kwargs = args_kwargs.get("args", []), args_kwargs.get("kwargs", {})
    fork_ctx = multiprocessing.get_context("spawn")
    fork_queue = multiprocessing.Queue()
    parent_queue = queue.Queue()
    terminate_event = (
        external_terminate_event if external_terminate_event else threading.Event()
    )

    stream_thread = threading.Thread(
        target=stream_output,
        args=(terminate_event, fork_queue, parent_queue),
        daemon=True,
    )
    stream_thread.start()

    child_work_dill = dill.dumps(f)
    process = fork_ctx.Process(
        target=forking_helper,
        args=(
            fork_queue,
            child_work_dill,
            {"args": args, "kwargs": kwargs},
        ),
    )
    process.start()

    try:
        while process.is_alive() or not parent_queue.empty():
            try:
                text = parent_queue.get(timeout=0.1)  # Get from text_queue instead
                yield text
            except queue.Empty:
                continue
        process.join()
        stream_thread.join()  # Add timeout

    finally:
        terminate_event.set()
        # Clean up queues
        while not fork_queue.empty():
            try:
                fork_queue.get_nowait()
            except (multiprocessing.queues.Empty, queue.Empty):
                pass
        while not parent_queue.empty():
            try:
                parent_queue.get_nowait()
            except queue.Empty:
                pass
        # Force terminate if still alive
        if process.is_alive():
            process.terminate()
            process.join()


if __name__ == "__main__":
    from dbt.cli.main import dbtRunner  # noqa

    runner = dbtRunner()
    for text in fork_and_yield_output(runner.invoke, {"args": ["run"]}):
        print("PARENT: ", text)

# # -------------- Example Usage --------------
# if __name__ == "__main__":
#     # We’ll create a child process that prints to both stdout & stderr,
#     # and capture that in the parent line by line.

#     for text in fork_and_yield_output(run_dbt_command):
#         print(text)

#     print("PARENT: Done capturing child output.")
