import asyncio
from collections import defaultdict
from typing import Dict, List

from taskex import Env
from taskex.run import Run

from .step_type import StepType
from .workflow import Workflow


class Orchestral:
    def __init__(
        self,
        config: Env | None = None,
    ) -> None:
        self._workflow = Workflow(config=config)

        self._execution_orders: Dict[str, List[List[str]]] = {}
        self._batch_results: list[Run] = []
        self._results_waiter = asyncio.Event()
        self._run_task: asyncio.Task | None = None
        self._execute_next = False

        self.results: dict[str, dict[int, Run]] = defaultdict(dict)

    def __enter__(self):
        self._workflow = Workflow()
        return self._workflow

    def __exit__(self, type, value, traceback):
        pass

    async def __aiter__(self):
        # Before we yield results wait
        if self._results_waiter.is_set() is False:
            await self._results_waiter.wait()

        results = list(self._batch_results)

        yield results

    def create(self):
        self._workflow = Workflow()
        return self._workflow

    async def run(
        self,
        wait: bool = False,
    ):
        if wait:
            await self._run_workflow()

        else:
            self._run_task = asyncio.create_task(
                self._run_workflow(),
            )

    async def _run_workflow(self):
        self._execute_next = True
        for group in self._workflow:
            self._batch_results.clear()

            group_runs = [
                self._workflow.runner.command(
                    step.call,
                    *step.shell_args,
                    alias=step.alias,
                    env=step.env,
                    cwd=step.cwd,
                    shell=step.shell,
                    timeout=step.timeout,
                    schedule=step.schedule,
                    trigger=step.trigger,
                    repeat=step.repeat,
                    keep=step.keep,
                    max_age=step.max_age,
                    keep_policy=step.keep_policy,
                )
                if step.type == StepType.SHELL
                else self._workflow.runner.run(
                    step.call,
                    alias=step.alias,
                    timeout=step.timeout,
                    schedule=step.schedule,
                    trigger=step.trigger,
                    repeat=step.repeat,
                    keep=step.keep,
                    max_age=step.max_age,
                    keep_policy=step.keep_policy,
                )
                for step in group
            ]

            group_results = await self._workflow.runner.wait_all(
                [run.token for run in group_runs],
            )

            self._batch_results.extend(group_results)

            for res in group_results:
                self.results[res.task_name][res.run_id] = res

            if self._results_waiter.is_set() is False:
                self._results_waiter.set()

            if self._execute_next is False:
                break

    async def stop(self):
        self._execute_next = False
        await self._workflow.runner.stop()

    async def shutdown(self):
        self._execute_next = False
        await self._workflow.runner.shutdown()

        if self._run_task:
            await self._run_task

        if self._results_waiter.is_set() is False:
            self._results_waiter.set()

    def abort(self):
        self._execute_next = False

        try:
            self._run_task.cancel()

        except (
            asyncio.CancelledError,
            asyncio.InvalidStateError,
            asyncio.TimeoutError,
        ):
            pass

        if self._results_waiter.is_set() is False:
            self._results_waiter.set()

        self._workflow.runner.abort()
